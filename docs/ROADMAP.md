# MVP+ roadmap

Each phase should close through one or more focused PRs. Do not begin by
building every backend layer; deliver thin vertical slices that remain usable.

## Phase 0 — Foundation

**Outcome:** a contributor can clone, run checks and launch a minimal native
window and CLI from one documented environment.

- create the Python package, task runner and development bootstrap;
- establish domain/application/infrastructure/UI boundaries;
- add CI for lint, type checks, unit tests and metadata validation;
- add AppStream metadata and a Blazelauncher desktop entry/icon placeholder;
- implement temporary-XDG test harnesses;
- ship a minimal Kirigami window and `blazelauncher doctor`.

**Exit:** clean clone works on Arch/CachyOS from documented commands; GUI and
CLI both start; CI is green.

## Phase 1 — Launcher vertical slice

**Outcome:** create one safe launcher from either CLI or GUI and see it in the
Plasma application menu.

- typed launcher/command model;
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

## Phase 3 — AppImage Cabinet vertical slice

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

## Phase 4 — Versions, updates and rollback

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

## Phase 5 — First public release

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

- Plasma widget using the versioned CLI/JSON API;
- launcher templates and shareable recipe packs;
- GitHub Releases update adapter;
- additional desktops and distro packages;
- optional filesystem watcher;
- Flatpak build with an explicit host-access design;
- DBus service only if multiple clients create a demonstrated coordination
  problem.
