# MVP+ roadmap

Each phase should close through one or more focused PRs. Do not begin by
building every backend layer; deliver thin vertical slices that remain usable.

## Phase 0 — Foundation

**Outcome:** a contributor can clone, run checks and launch a minimal native
window and CLI from one documented environment.

- create the Python package, task runner and development bootstrap;
- establish domain/application/infrastructure/UI boundaries;
- establish the minimal Qt-free action/provider contracts used by every
  product surface;
- add CI for lint, type checks, unit tests and metadata validation;
- add AppStream metadata and a Blazelauncher desktop entry/icon placeholder;
- implement temporary-XDG test harnesses;
- ship a minimal Kirigami window and `blazelauncher doctor`.

**Exit:** clean clone works on Arch/CachyOS from documented commands; GUI and
CLI both start; CI is green.

## Phase 1 — Action and launcher vertical slice

**Outcome:** create one safe launcher from either CLI or GUI and see it in the
Plasma application menu.

- typed action, launcher and command model;
- desktop-entry renderer and parser fixtures;
- create, list, show, validate and remove services;
- atomic XDG integration and backup;
- CLI with text/JSON and dry-run;
- GUI list plus progressive create/edit form, icon picker and live preview;
- Plasma cache refresh adapter;
- explicit test launch with captured result.

**Exit:** the first-user success path works without hand-editing; test fixtures
pass both internal and freedesktop validation.

## Phase 2 — Launcher Studio MVP+

**Outcome:** launcher management is credible enough to replace routine manual
editing and the relevant parts of MenuLibre.

- adopt/clone existing launchers while preserving unknown keys;
- environment variables, working directory, terminal toggle, categories,
  keywords, visibility and actions;
- previewable Wayland/Electron, Flatpak, browser-profile and local-web-app
  presets;
- search/filter, validation explanations, export, backup and restore;
- local activity history and diagnostics bundle with secret redaction;
- keyboard-first polish, accessible names and responsive layouts.

**Exit:** scripts, AppImages, dev servers, browser profiles and Flatpaks can be
modelled safely; advanced fields remain understandable.

## Phase 3 — Command Palette core

**Outcome:** a keyboard shortcut opens a fast native palette that queries safe
fixture providers, ranks and previews results, and executes one shared action.

- query/result/payload/preview/execution provider contracts;
- cancellable search broker with deterministic ranking and budgets;
- compact Kirigami overlay, keyboard navigation and preview pane;
- provider scoping and quiet availability/error states;
- typed one-step composition boundary;
- cold-start toggle plus measured optional resident mode over local-only IPC;
- CLI action/palette query surfaces and versioned JSON;
- privacy, cancellation, IPC and performance harnesses.

**Exit:** stale results cannot replace the current query; a fixture/local saved
action is searchable, previewable and executable; the UI stays responsive; warm
performance is measured honestly on the reference workstation.

## Phase 4 — Fifteen built-ins and script actions

**Outcome:** the palette's full differentiating action set is useful enough for
daily developer/workstation use without an extension marketplace.

- navigation/local knowledge: files, recent projects, Git repositories,
  Obsidian notes and browser history;
- execution/workstation: saved commands, workstation sessions, media, SSH,
  `just` and `mise`;
- utilities/composition: unit conversion, UUIDs, encode/decode and clipboard
  transformations;
- provider configuration, capability detection, bounded previews and useful
  empty/error states;
- TOML script action manifest v1 with validation, exact argv/risk preview,
  timeout and bounded plain-text output;
- complete fixture, privacy, risk, keyboard and provider-contract coverage.

**Exit:** all 15 canonical actions in `docs/PALETTE.md` meet their acceptance
contract; manifest v1 runs one explicit local action safely; no marketplace,
dynamic provider protocol or general workflow engine has been introduced.

## Phase 5 — AppImage Cabinet vertical slice

**Outcome:** import and integrate an AppImage without scattering unmanaged
files through the home directory.

- cabinet data model, SQLite migrations and per-app version directories;
- drag/drop, picker and CLI import;
- hash, size, permission and duplicate inspection;
- safe static metadata strategy with manual fallback;
- name, icon, notes, categories and launch flags;
- integrate/unintegrate through Launcher Studio;
- active-version selection and remove preview.

**Exit:** an imported AppImage is catalogued, appears in Plasma and can be
cleanly unintegrated without touching unrelated files.

## Phase 6 — Versions, updates and rollback

**Outcome:** a user can deliberately check, update and return to a known-good
AppImage version.

- retain and activate multiple local versions;
- rollback and retention policy with protected known-good versions;
- embedded update-information discovery;
- opt-in update checks with source disclosure and cancellation;
- optional `appimageupdatetool` adapter, capability-detected;
- staged download/apply flow and duplicate cleanup;
- failure injection tests for interrupted copies, bad downloads and database
  transaction errors.

**Exit:** update and rollback are transactional; no update happens in the
background; the previous version remains available.

## Phase 7 — First public release

**Outcome:** a small group of Arch/KDE users can install, understand and report
problems safely.

- CachyOS/Arch real-system acceptance pass;
- reproducible Arch package/AUR-ready `PKGBUILD`;
- first-run tour and built-in safety explanations;
- screenshots, concise user guide, troubleshooting and privacy statement;
- release checklist, changelog and signed `v0.1.0` tag;
- triage labels and good-first contribution issues derived from real use.

**Exit:** no critical data-loss/security bugs; install/upgrade/uninstall paths
are documented; release artefacts are reproducible.

## Later candidates, not implied commitments

- KRunner adapter after the action API is stable;
- Plasma widget using the versioned CLI/JSON/local action API;
- launcher templates and shareable recipe packs;
- GitHub Releases update adapter;
- additional desktops and distro packages;
- optional filesystem watcher;
- Flatpak build with an explicit host-access design;
- DBus service only if multiple clients create a demonstrated coordination
  problem;
- dynamic script-provider protocol or broader composition only after real
  manifest/action limitations are demonstrated and separately designed.
