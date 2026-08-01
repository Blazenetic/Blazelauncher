# AGENTS.md

This file is the durable entry point for human and AI contributors.

## Mission

Build a calm, polished launcher and AppImage manager for Linux power users,
starting with KDE Plasma 6 on Wayland. Keep the project narrow, local-first,
modular and pleasant to extend after MVP+.

## Required reading order

Before changing code or plans, read:

1. `README.md`
2. `docs/PRODUCT.md`
3. `docs/ARCHITECTURE.md`
4. `docs/ROADMAP.md`
5. every decision record relevant to the task
6. the linked GitHub issue and current branch/PR context

For the initial autonomous build, also read
`docs/AGENT-MVP-BUILD-PROMPT.md` in full.

## Non-negotiable product boundaries

- Launcher management is the foundation; AppImage Cabinet is a specialised
  module that consumes it.
- Remain a launcher/AppImage utility, not a package manager or software centre.
- Support user-level XDG locations. Do not require root, a daemon or a system
  service.
- GUI and CLI must use the same application services and domain model.
- Keep Plasma/KDE integration behind adapters; keep the core freedesktop/XDG.
- Treat imported AppImages and launcher commands as untrusted input.
- Never execute an imported AppImage merely to inspect it.
- Never interpolate user commands through a shell by default.
- Make file changes atomic, previewable and reversible where practical.
- Never perform network checks or downloads without explicit user action or a
  clearly enabled preference.
- Preserve unknown `X-*` desktop-entry keys when adopting existing launchers.
- Do not overwrite non-Blazelauncher files without a visible backup and user
  confirmation.

## Chosen stack

- Python 3.12+
- PySide6 with QML and KDE Kirigami 6 for the GUI
- Python standard library for the CLI (`argparse`), SQLite and core file work
- `platformdirs` only if direct XDG handling proves insufficient
- `pytest`, `pytest-qt`, `ruff` and `mypy` for quality
- `desktop-file-validate`, `appstreamcli` and `qmllint` in integration/CI checks

Minimise dependencies. A new production dependency needs a short rationale in
the PR and should replace meaningful complexity rather than convenience alone.

## Target source layout

```text
src/blazelauncher/
  domain/          # immutable models, invariants, typed errors
  application/     # use cases shared by GUI and CLI
  infrastructure/  # XDG, desktop files, SQLite, filesystem, subprocesses
  adapters/        # Plasma, AppImage metadata/update sources
  cli/             # argument parsing and presentation only
  gui/             # PySide bridge/view-models
  qml/             # declarative interface only
tests/
  unit/
  integration/
  fixtures/
```

Dependency direction is inward: UI and infrastructure depend on application
and domain contracts. Domain code must not import Qt.

## Delivery workflow

- One GitHub issue should describe one reviewable outcome.
- Use a focused branch named `feat/...`, `fix/...`, `docs/...` or `chore/...`.
- Link the PR to its issue and use `Closes #N` only when acceptance criteria are
  actually met.
- Prefer small vertical slices over broad layer-first rewrites.
- Keep implementation status in issues/PRs, not copied into this file.
- Record an ADR when changing a boundary, data model, security posture or
  primary technology.

## Verification contract

Until the task runner exists, use the equivalent direct commands. The project
should converge on these stable checks:

```bash
python -m pytest
ruff check .
ruff format --check .
mypy src
desktop-file-validate <generated-fixture.desktop>
qmllint src/blazelauncher/qml
appstreamcli validate org.blazenetic.Blazelauncher.metainfo.xml
```

Tests that mutate XDG data must point `XDG_CONFIG_HOME`, `XDG_DATA_HOME`,
`XDG_STATE_HOME` and `XDG_CACHE_HOME` at temporary directories. Never test
against a contributor's real application menu or AppImage directory.

## Definition of done

A change is done when behaviour, tests, documentation and error handling agree;
the relevant checks pass; unsafe operations are gated; and the PR contains a
compact handover with evidence, decisions, remaining risks and the exact next
action.
