#!/usr/bin/env bash
#
# Prepare a Claude Code on the web session so that scripts/verify.sh actually
# runs. Without this an agent has no toolchain, cannot check its own work and
# has to fall back on asserting that the code is correct.
#
# Local machines are left alone: developers use scripts/bootstrap-dev.sh, which
# knows about Arch and the desktop tier.

set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
    exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "${BASH_SOURCE[0]}")/../..}"

# Qt imports these at load time, even under QT_QPA_PLATFORM=offscreen.
QT_RUNTIME_LIBRARIES=(
    libegl1
    libgl1
    libxkbcommon0
    libdbus-1-3
    libfontconfig1
)

# desktop-file-validate and appstreamcli are packaged here; Kirigami 6 is not.
DESKTOP_TOOLING=(
    desktop-file-utils
    appstream
    qt6-declarative-dev-tools
    shellcheck
)

if command -v apt-get >/dev/null 2>&1; then
    # A broken third-party repository must not take the whole session with it.
    sudo apt-get update -qq || echo "apt-get update reported errors; continuing"
    sudo apt-get install -y -qq --no-install-recommends \
        "${QT_RUNTIME_LIBRARIES[@]}" "${DESKTOP_TOOLING[@]}" \
        || echo "system package install incomplete; some checks will report SKIP"
fi

PYTHON=python3
command -v python3.12 >/dev/null 2>&1 && PYTHON=python3.12

if [ ! -d .venv ]; then
    "$PYTHON" -m venv .venv
fi

.venv/bin/python -m pip install --quiet --upgrade pip
.venv/bin/python -m pip install --quiet -r requirements-dev.txt

if [ -f pyproject.toml ]; then
    .venv/bin/python -m pip install --quiet -e .
fi

# Put the environment on PATH for the rest of the session so that `pytest`,
# `ruff` and `mypy` resolve without an explicit activate step.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
    {
        echo "export VIRTUAL_ENV=$PWD/.venv"
        echo "export PATH=$PWD/.venv/bin:\$PATH"
        # qmllint lives outside PATH on Debian-family images.
        echo "export PATH=\$PATH:/usr/lib/qt6/bin"
    } >> "$CLAUDE_ENV_FILE"
fi

echo "Environment ready. Run scripts/verify.sh before opening a pull request."
echo "Kirigami 6 is not available here: QML and Kirigami checks report SKIP"
echo "and are covered by the Arch container job in CI."
