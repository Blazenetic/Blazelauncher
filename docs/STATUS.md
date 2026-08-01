# Status

The single place to find out where the project actually is. Every pull request
updates it; the maintainer corrects it on merge.

This file exists because most contributors here start with no memory of the
last change. Issues describe intended outcomes and pull requests describe
individual changes, but neither answers "what is true in the repository right
now, and what should I not be surprised by". That is this file's only job.

**Last updated:** 2026-08-01, after the verification harness landed.

## Where the project is

Planning and harness. There is no application code yet: `src/blazelauncher`
does not exist. The product contract, architecture, palette specification and
roadmap are written, and the checks that will grade the implementation are in
place and running.

The next piece of work is issue #2, Phase 0.

## What exists

| Area | State |
| --- | --- |
| Product, architecture, palette and script-action specifications | Written and reviewed |
| Decision records 0001–0003 | Accepted for MVP+ |
| Decision record 0004 (palette presentation surface) | Proposed, blocked on a spike |
| Verification harness (`scripts/verify.sh`) | Working; most checks report SKIP until their subject exists |
| CI (core tier on Ubuntu, desktop tier in an Arch container) | Working |
| Boundary guards (Qt-free layers, no shell execution, no hardcoded paths) | Working, with self-tests against synthetic sources |
| XDG isolation for tests | Working, autouse, self-tested |
| Agent session bootstrap (`.claude/hooks/session-start.sh`) | Working |
| `src/blazelauncher` | Does not exist |
| Any user-visible feature | None |

## Things that will surprise you

- **Kirigami 6 cannot be installed from PyPI.** PySide6 can. Any machine
  without the distribution packages — including the default agent session
  container and the `core` CI job — cannot lint or run QML that imports
  `org.kde.kirigami`. Those checks report SKIP there and are covered by the
  Arch container job. Do not "fix" a SKIP by deleting the check.
- **PySide6 needs system libraries at import time**, even for offscreen
  rendering: `libegl1`, `libgl1`, `libxkbcommon0`, `libdbus-1-3`,
  `libfontconfig1` on Debian family. Without them `pytest-qt` fails while
  pytest is still configuring, which takes the whole suite down rather than
  one test. `scripts/verify.sh` detects this and disables the plugin so the
  core tier still runs.
- **`qmllint` is not on `PATH`** on Arch or Debian; it lives in
  `/usr/lib/qt6/bin`. PySide6 also ships `pyside6-qmllint`. The verify script
  looks in all three places.
- **A check that reports SKIP is not a check that passed.** The summary counts
  them separately on purpose. CI runs with `--strict`, where missing tooling is
  a failure; a SKIP because the subject does not exist yet stays benign.
- **Tool configuration lives in standalone files** (`ruff.toml`, `mypy.ini`,
  `pytest.ini`, `.importlinter`) rather than `pyproject.toml`. Each of those
  files takes precedence over `pyproject.toml`, so duplicating settings there
  produces two sources of truth and one of them will be silently ignored.
- **`mypy.ini` does not list `src` yet**, because a bare `mypy` would fail on
  the missing directory. Phase 0 adds it.

## Open questions carried forward

- How the palette window presents itself on Wayland. See decision record 0004:
  an ordinary `xdg-toplevel` cannot position or focus itself, and the usual
  answer — layer-shell — has no Python bindings. This gates Phase 3.
- Whether PySide6 with Kirigami 6 is comfortable enough to build the whole
  interface on. Same spike.
- Safe static AppImage metadata extraction (issue #6), which gates Phase 5.
- The three product questions at the end of `docs/PRODUCT.md`: cabinet layout,
  retention count, and adopting launchers in place or by copy.

## Exact next action

Issue #2, Phase 0: create the Python package, make `scripts/verify.sh` light up
the checks that currently report SKIP, and add `src` to `mypy.ini`. Read
`AGENTS.md` first.
