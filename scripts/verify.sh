#!/usr/bin/env bash
#
# The canonical verification contract for Blazelauncher.
#
# This script is the single definition of "the checks pass". CI runs it, the
# justfile wraps it and contributors — human or agent — should run it before
# opening a pull request. Do not invent a parallel set of commands.
#
# Usage:
#   scripts/verify.sh              run every check whose tooling is present
#   scripts/verify.sh --strict     treat missing tooling as a failure (CI)
#   scripts/verify.sh --tier core  run only the tier that works anywhere
#
# Tiers:
#   core     Python-only: format, lint, types, import contracts, unit tests.
#            Runs on any Linux with Python 3.12 and requirements-dev.txt.
#   desktop  Qt, QML, Kirigami, desktop-entry and AppStream validation.
#            Needs distribution packages; see scripts/bootstrap-dev.sh.
#
# Checks whose subject does not exist yet (no src/, no QML, no fixtures) report
# SKIP rather than failing. That keeps the harness honest while the repository
# is still being built out, and each check switches itself on as its subject
# lands.

set -uo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 2

STRICT=0
TIER="all"

while [ $# -gt 0 ]; do
    case "$1" in
        --strict) STRICT=1 ;;
        --tier) TIER="${2:-all}"; shift ;;
        --tier=*) TIER="${1#--tier=}" ;;
        -h|--help) sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
    shift
done

if [ "$TIER" != "all" ] && [ "$TIER" != "core" ] && [ "$TIER" != "desktop" ]; then
    echo "unknown tier: $TIER (expected core, desktop or all)" >&2
    exit 2
fi

PASSED=(); FAILED=(); SKIPPED=()

if [ -t 1 ]; then
    C_OK=$'\033[32m'; C_BAD=$'\033[31m'; C_SKIP=$'\033[33m'; C_OFF=$'\033[0m'
else
    C_OK=""; C_BAD=""; C_SKIP=""; C_OFF=""
fi

have() { command -v "$1" >/dev/null 2>&1; }
has_src() { [ -d src/blazelauncher ]; }

# QtGui is the honest test: PySide6 can import while the platform libraries it
# needs (libEGL, libGL, libxkbcommon) are missing.
qt_usable() { python3 -c "import PySide6.QtGui" >/dev/null 2>&1; }

# Distributions keep qmllint off PATH (Arch and Debian both use /usr/lib/qt6),
# and PySide6 ships its own copy.
find_qmllint() {
    local candidate
    for candidate in qmllint pyside6-qmllint /usr/lib/qt6/bin/qmllint; do
        if command -v "$candidate" >/dev/null 2>&1; then
            command -v "$candidate"
            return 0
        fi
    done
    return 1
}

pass() { PASSED+=("$1"); printf '%s  ok%s   %s\n' "$C_OK" "$C_OFF" "$1"; }
fail() { FAILED+=("$1"); printf '%s FAIL%s  %s\n' "$C_BAD" "$C_OFF" "$1"; }

# A skip is a failure under --strict only when the tooling is absent. A skip
# because the subject does not exist yet is always benign.
skip() {
    local name="$1" reason="$2" kind="${3:-subject}"
    if [ "$STRICT" = "1" ] && [ "$kind" = "tooling" ]; then
        FAILED+=("$name (missing tooling: $reason)")
        printf '%s FAIL%s  %s — required tooling missing: %s\n' \
            "$C_BAD" "$C_OFF" "$name" "$reason"
    else
        SKIPPED+=("$name")
        printf '%s skip%s %s — %s\n' "$C_SKIP" "$C_OFF" "$name" "$reason"
    fi
}

run() {
    local name="$1"; shift
    printf '\n\033[1m▸ %s\033[0m\n' "$name"
    if "$@"; then pass "$name"; else fail "$name"; fi
}

# pytest exits 5 when nothing matched the selection, which is a skip here.
run_pytest() {
    local name="$1"; shift
    printf '\n\033[1m▸ %s\033[0m\n' "$name"
    "$@"
    local rc=$?
    case "$rc" in
        0) pass "$name" ;;
        5) skip "$name" "no tests matched yet" ;;
        *) fail "$name" ;;
    esac
}

# ---------------------------------------------------------------- core tier --

if [ "$TIER" = "all" ] || [ "$TIER" = "core" ]; then
    if have ruff; then
        run "ruff format --check" ruff format --check .
        run "ruff check" ruff check .
    else
        skip "ruff" "ruff is not installed" tooling
        skip "ruff format" "ruff is not installed" tooling
    fi

    # The harness itself is code, and a broken verify.sh fails open.
    if have shellcheck; then
        shopt -s nullglob
        shell_scripts=(scripts/*.sh .claude/hooks/*.sh)
        shopt -u nullglob
        run "shellcheck" shellcheck "${shell_scripts[@]}"
    else
        skip "shellcheck" "shellcheck is not installed" tooling
    fi

    if ! have mypy; then
        skip "mypy" "mypy is not installed" tooling
    elif has_src; then
        run "mypy" mypy src tests
    else
        run "mypy (tests only)" mypy
    fi

    if ! has_src; then
        skip "import contracts" "src/blazelauncher does not exist yet"
    fi

    if has_src; then
        if have lint-imports; then
            run "import contracts" lint-imports
        else
            skip "import contracts" "import-linter is not installed" tooling
        fi
    fi

    if have pytest; then
        # pytest-qt imports QtGui while configuring, which fails on a machine
        # without the Qt runtime libraries. The core tier has to run there
        # anyway, so disable the plugin rather than losing the whole suite.
        core_args=()
        qt_usable || core_args+=(-p no:qt)
        run_pytest "pytest (core)" pytest "${core_args[@]}" \
            -m "not gui and not kirigami"
    else
        skip "pytest (core)" "pytest is not installed" tooling
    fi
fi

# ------------------------------------------------------------- desktop tier --

if [ "$TIER" = "all" ] || [ "$TIER" = "desktop" ]; then
    if have pytest && qt_usable; then
        # Offscreen keeps Qt tests headless. Never run these against a real
        # session: a stray window on a contributor's desktop is a test smell.
        run_pytest "pytest (gui, offscreen)" \
            env QT_QPA_PLATFORM=offscreen pytest -m "gui and not kirigami"
    else
        skip "pytest (gui, offscreen)" "PySide6 is not importable" tooling
    fi

    qmllint_bin="$(find_qmllint)"
    if [ -z "$qmllint_bin" ]; then
        skip "qmllint" "qmllint is not installed" tooling
    elif [ ! -d src/blazelauncher/qml ]; then
        skip "qmllint" "no QML yet"
    else
        # Kirigami imports cannot resolve without the distribution packages, so
        # this check belongs to the desktop tier and will report unresolved
        # imports anywhere Kirigami 6 is absent.
        # shellcheck disable=SC2016  # $1 is the inner shell's argument
        run "qmllint" bash -c \
            'find src/blazelauncher/qml -name "*.qml" -print0 |
                xargs -0 -r "$1"' _ "$qmllint_bin"
    fi

    if ! have desktop-file-validate; then
        skip "desktop-file-validate" "desktop-file-utils is not installed" tooling
    else
        shopt -s nullglob
        entries=(data/*.desktop tests/fixtures/desktop/valid/*.desktop)
        shopt -u nullglob
        if [ ${#entries[@]} -eq 0 ]; then
            skip "desktop-file-validate" "no desktop entries to validate yet"
        else
            run "desktop-file-validate" desktop-file-validate "${entries[@]}"
        fi
    fi

    if ! have appstreamcli; then
        skip "appstreamcli" "appstream is not installed" tooling
    else
        shopt -s nullglob
        metainfo=(data/*.metainfo.xml)
        shopt -u nullglob
        if [ ${#metainfo[@]} -eq 0 ]; then
            skip "appstreamcli" "no AppStream metadata yet"
        else
            run "appstreamcli" appstreamcli validate "${metainfo[@]}"
        fi
    fi
fi

# ------------------------------------------------------------------ summary --

printf '\n\033[1m── summary ──\033[0m\n'
printf '%s  ok%s   %d\n' "$C_OK" "$C_OFF" "${#PASSED[@]}"
printf '%s skip%s  %d\n' "$C_SKIP" "$C_OFF" "${#SKIPPED[@]}"
printf '%s FAIL%s  %d\n' "$C_BAD" "$C_OFF" "${#FAILED[@]}"

if [ ${#FAILED[@]} -gt 0 ]; then
    printf '\nfailed:\n'
    printf '  - %s\n' "${FAILED[@]}"
    exit 1
fi

exit 0
