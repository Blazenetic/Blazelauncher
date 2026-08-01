# Task runner for Blazelauncher.
#
# These are thin wrappers. scripts/verify.sh is the definition of the
# verification contract, so that CI, a contributor and an agent all run exactly
# the same checks. Add a recipe here only when it wraps something that already
# works on its own.

default:
    @just --list

# Install system packages and create .venv (Arch gets the desktop tier).
bootstrap:
    scripts/bootstrap-dev.sh

# The full verification contract; skips checks whose tooling is absent.
verify:
    scripts/verify.sh

# Only the checks that run on any Linux with Python 3.12.
verify-core:
    scripts/verify.sh --tier core

# Qt, QML, desktop-entry and AppStream checks.
verify-desktop:
    scripts/verify.sh --tier desktop

# What CI runs: missing tooling is a failure rather than a skip.
verify-strict:
    scripts/verify.sh --strict

fmt:
    ruff format .
    ruff check --fix .

test *ARGS:
    pytest {{ARGS}}

# Qt tests, headless. Never point these at a real session.
test-gui *ARGS:
    QT_QPA_PLATFORM=offscreen pytest -m gui {{ARGS}}
