#!/usr/bin/env bash
#
# Development environment bootstrap.
#
# Sets up everything scripts/verify.sh needs. Arch/CachyOS is the primary
# target and gets the full desktop tier; other distributions get the core tier
# and a note about what is missing.
#
# Usage:
#   scripts/bootstrap-dev.sh            install packages, then create .venv
#   scripts/bootstrap-dev.sh --no-sudo  skip system packages (containers, CI)
#   scripts/bootstrap-dev.sh --dry-run  print what would be installed
#
# The script asks for sudo only for system packages and prints the exact
# command first. Nothing is installed outside the package manager and .venv.

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

NO_SUDO=0
DRY_RUN=0
for arg in "$@"; do
    case "$arg" in
        --no-sudo) NO_SUDO=1 ;;
        --dry-run) DRY_RUN=1 ;;
        -h|--help) sed -n '2,18p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "unknown argument: $arg" >&2; exit 2 ;;
    esac
done

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }
note() { printf '  %s\n' "$*"; }

run_cmd() {
    printf '  $ %s\n' "$*"
    [ "$DRY_RUN" = "1" ] && return 0
    "$@"
}

# Containers run as root and often have no sudo installed.
SUDO=sudo
[ "$(id -u)" = "0" ] && SUDO=""
run_root() { run_cmd ${SUDO:+"$SUDO"} "$@"; }

# Arch keeps PySide6 and Kirigami as distribution packages that cannot be
# installed from PyPI, so the virtual environment inherits site packages
# rather than trying to rebuild the Qt stack.
VENV_ARGS=(--system-site-packages)
PYTHON=python3

# ------------------------------------------------------------------ packages --

if [ "$NO_SUDO" = "1" ]; then
    say "Skipping system packages (--no-sudo)"
elif command -v pacman >/dev/null 2>&1; then
    say "Arch/CachyOS detected — installing the full desktop tier"
    run_root pacman -S --needed --noconfirm \
        python \
        python-pyside6 \
        kirigami \
        qt6-declarative \
        qt6-wayland \
        desktop-file-utils \
        appstream \
        shellcheck
    note "Optional adapters exercised by palette providers: just, mise,"
    note "playerctl, fd, ripgrep. Install them when you work on those issues."
elif command -v apt-get >/dev/null 2>&1; then
    say "Debian/Ubuntu detected — installing the core tier"
    run_root apt-get update -qq
    run_root apt-get install -y --no-install-recommends \
        python3.12 \
        python3.12-venv \
        desktop-file-utils \
        appstream \
        qt6-declarative-dev-tools \
        shellcheck \
        libegl1 libgl1 libxkbcommon0 libdbus-1-3 libfontconfig1
    note "Kirigami 6 is not packaged here. QML that imports org.kde.kirigami"
    note "cannot be linted or run on this machine; those checks report SKIP."
    note "Use an Arch container or the reference workstation for them."
    note "The lib* packages are what PySide6 loads at import time, including"
    note "under QT_QPA_PLATFORM=offscreen."
    # PySide6 comes from PyPI here, so an isolated environment is correct.
    VENV_ARGS=()
    command -v python3.12 >/dev/null 2>&1 && PYTHON=python3.12
else
    say "Unknown distribution — skipping system packages"
    note "Install: Python 3.12+, desktop-file-utils, appstream, qmllint and,"
    note "for the desktop tier, PySide6 and Kirigami 6."
fi

# ------------------------------------------------------------------- python --

say "Creating .venv"
if [ ! -d .venv ]; then
    run_cmd "$PYTHON" -m venv "${VENV_ARGS[@]}" .venv
else
    note ".venv already exists — reusing it"
fi

say "Installing the verification toolchain"
run_cmd .venv/bin/python -m pip install --upgrade --quiet pip
run_cmd .venv/bin/python -m pip install --quiet -r requirements-dev.txt

if [ -f pyproject.toml ]; then
    say "Installing the package in editable mode"
    run_cmd .venv/bin/python -m pip install --quiet -e .
else
    note "No pyproject.toml yet — skipping the editable install."
fi

say "Done"
note "Activate with:  source .venv/bin/activate"
note "Verify with:    scripts/verify.sh"
