# AGENTS.md

This file is the durable entry point for human and AI contributors.

## Mission

Build a calm, polished local command surface for Linux power users, starting
with KDE Plasma 6 on Wayland. Command Palette, Launcher Studio and AppImage
Cabinet must feel like one product over one action engine. Keep it local-first,
modular and pleasant to extend after MVP+.

## Required reading order

Before changing code or plans, read:

1. `docs/STATUS.md` — what is actually true in the repository right now
2. `README.md`
3. `docs/PRODUCT.md`
4. `docs/ARCHITECTURE.md`
5. `docs/PALETTE.md` for palette/provider work
6. `docs/SCRIPT-ACTIONS.md` for script action work
7. `docs/ROADMAP.md`
8. every decision record relevant to the task
9. the linked GitHub issue and current branch/PR context

`docs/AGENT-PROMPT.md` holds the prompt templates used to start this work.

Documents describe intent. `docs/STATUS.md` describes reality, and where they
disagree, reality wins — say so in the pull request rather than implementing
around it.

## Non-negotiable product boundaries

- The action model is the foundation: Command Palette executes actions,
  Launcher Studio persists suitable actions into Plasma, and AppImage Cabinet
  publishes managed executables as actions/launchers.
- Remain a personal command surface, not a package manager, software centre,
  general workflow engine or KRunner clone.
- Support user-level XDG locations. Do not require root, a privileged/system
  daemon or a system service.
- GUI and CLI must use the same application services and domain model.
- Keep Plasma/KDE integration behind adapters; keep the core freedesktop/XDG.
- Treat imported AppImages, launcher commands and script actions as untrusted
  executable input.
- Never execute an imported AppImage merely to inspect it.
- Never interpolate user commands through a shell by default.
- Never log palette queries, clipboard contents, browser-history values, note
  contents, SSH details or script output by default.
- Script actions are explicit local manifests, not dynamically downloaded
  extensions. MVP+ has no marketplace or arbitrary provider protocol.
- Side-effecting actions are terminal steps; initial composition is limited to
  typed values and pure/read-only transforms.
- Make file changes atomic, previewable and reversible where practical.
- Never perform network checks or downloads without explicit user action or a
  clearly enabled preference.
- Preserve unknown `X-*` desktop-entry keys when adopting existing launchers.
- Do not overwrite non-Blazelauncher files without a visible backup and user
  confirmation.

Some of these are enforced mechanically. `tests/architecture/` fails the build
when Qt reaches a Qt-free layer, when a command would go through a shell, when
a subprocess is launched outside the process layers, or when a user directory
is hardcoded past the XDG resolver. Those guards are self-tested against
synthetic sources, so they work before the package exists.

The rest — side-effect-free search and preview, not logging sensitive data,
staged and reversible writes — are reviewed by a human. A green suite is not
evidence that they hold.

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
  providers/       # built-in action providers and provider contracts
  adapters/        # Plasma, local sources, AppImage metadata/update sources
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
- Keep implementation status in issues/PRs and in `docs/STATUS.md`, not copied
  into this file. `docs/STATUS.md` is the one place that carries context
  between contributors who share no memory, so update it in the same change.
- Record an ADR when changing a boundary, data model, security posture or
  primary technology.
- Write British English in documentation and user-facing strings, matching the
  existing docs ("licence", "behaviour", "organise").

## Verification contract

```bash
scripts/bootstrap-dev.sh   # once: system packages, then .venv
scripts/verify.sh          # the contract
```

`scripts/verify.sh` is the definition of "the checks pass". CI runs it, the
`justfile` wraps it, and pull requests are reviewed against its output. Do not
invent a parallel set of commands, and do not add a check that only exists in
CI — put it in the script.

It runs `ruff format --check`, `ruff check`, `shellcheck`, `mypy`,
import-linter contracts, pytest, offscreen Qt tests, `qmllint`,
`desktop-file-validate` and `appstreamcli validate`.

### Verification tiers

- **core** — Python only. Runs on any Linux with Python 3.12 and
  `requirements-dev.txt`, including agent containers and the main CI job.
- **desktop** — Qt, QML, Kirigami, desktop-entry and AppStream validation.
  Needs distribution packages. Kirigami 6 is not installable from PyPI, so QML
  importing `org.kde.kirigami` can only be checked on Arch/CachyOS or in the
  Arch container job in CI.

A check whose subject does not exist yet reports SKIP; so does a check whose
tooling is missing. CI passes `--strict`, where missing tooling is a failure.
**A SKIP is not a pass** — if an acceptance criterion depends on a check that
skipped in your environment, say so rather than implying it passed.

Qt tests are marked `gui` and run under `QT_QPA_PLATFORM=offscreen`. Tests
needing Kirigami are marked `kirigami` and are desktop tier only. Never run the
suite against a live session; a stray window on someone's desktop is a bug in
the test.

### Tool configuration

`ruff.toml`, `mypy.ini`, `pytest.ini` and `.importlinter` live at the
repository root. Each takes precedence over `pyproject.toml`, so do not
duplicate these settings there — the copy in `pyproject.toml` would be ignored
without any warning.

The harness is owned by the maintainer. Relaxing a rule, a guard test or a CI
job in the same change that the rule would have caught is a review failure.
Raise it in the pull request and leave the check failing.

### Test data

Tests that touch XDG data must point `XDG_CONFIG_HOME`, `XDG_DATA_HOME`,
`XDG_STATE_HOME` and `XDG_CACHE_HOME` at temporary directories. The autouse
`xdg` fixture in `tests/conftest.py` does this for every test, including `HOME`,
and fails a test that points any of them back at the real user. Never test
against a contributor's real application menu or AppImage directory.

Provider tests must use fixtures or disposable copies, never real browser
profiles, Obsidian vaults, SSH configuration, clipboard content, repositories
or task files. Performance claims require measurements with stated conditions.

## Definition of done

A change is done when behaviour, tests, documentation and error handling agree;
the relevant checks pass; unsafe operations are gated; `docs/STATUS.md` matches
reality; and the PR contains a compact handover with evidence, decisions,
remaining risks and the exact next action.

## Evidence

Separate three things in every pull request, and never blur them:

- **checked** — you ran a command and its output is in the PR;
- **not checked** — nothing verified this, and you say so;
- **cannot be checked here** — it needs the real desktop.

Several acceptance criteria in this project genuinely cannot be verified
outside a KDE Plasma 6 Wayland session: whether a launcher appears in the
application menu, how QML renders, anything involving the compositor, and every
performance target. Name those plainly and leave them for the maintainer.

Performance claims need measurements with stated hardware, data size, sample
count and cold or warm state. A number without conditions is not evidence, and
a number produced by a harness you wrote in the same change is weak evidence —
say which it is.
