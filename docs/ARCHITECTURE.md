# Architecture

## Recommendation

Build Blazelauncher as a modular Python application with a shared action engine,
a PySide6/QML/Kirigami GUI and a standard-library CLI. Keep domain and
application services free of Qt. Command Palette executes actions, Launcher
Studio persists suitable actions as desktop entries, and AppImage Cabinet
publishes managed executables into the same action model. Use SQLite for local
state and an explicit filesystem transaction layer for user-visible mutations.

This is an MVP+ optimisation: it provides a native Plasma experience, fast
iteration and an approachable codebase while preserving seams where a more
performance-sensitive component could later move to Rust or C++ without a UI
rewrite.

## System context

```text
User
  |-- Command Palette --|
  |-- Launcher Studio --|-- Action and application services
  |-- AppImage Cabinet -|     |-- provider search / preview / execute
  |-- CLI / scripts ----|     |-- launcher / cabinet / update / backup
                               |
                        Ports and adapters
                          |-- local data providers
                          |-- XDG / desktop entries / SQLite
                          |-- safe processes / optional local IPC
                          |-- Plasma / AppImage integrations
```

## Technology decisions

See the decision records in `docs/decisions/`.

- Python 3.12+ for the core and application layer.
- PySide6 (official Qt for Python bindings) with QML and Kirigami 6.
- `argparse` for a dependency-light CLI.
- SQLite for transactional metadata, notes, activity and version relationships.
- Ordinary XDG files remain the source of truth for installed launchers and
  managed binaries; SQLite is an index/control record, not a proprietary vault.
- No root helper, privileged/system daemon or required message bus service in
  MVP+. An optional user-enabled resident palette process may accept toggle
  requests over a local socket; cold-start mode remains supported.

## Modules and dependency rules

### Domain

Typed value objects and invariants:

- `ActionDefinition`, `ActionQuery`, `ActionResult`, `ActionPayload`,
  `ActionPreview`, `ExecutionPolicy`, `ProviderCapability`;
- `Launcher`, `CommandSpec`, `EnvironmentVariable`, `DesktopCategory`;
- `CabinetApp`, `AppImageVersion`, `IntegrationState`, `UpdateCandidate`;
- paths, hashes, IDs and safe validation results;
- typed errors that can be rendered differently by GUI and CLI.

The domain has no Qt, filesystem, network or process imports.

### Application

Use cases coordinating ports and transactions:

- discover providers and capabilities;
- search, rank, preview, cancel, compose and execute actions;
- register/validate local script action manifests;
- create/adopt/edit/clone/remove/restore launcher;
- preview, validate and explicitly test launch;
- import, activate, integrate, roll back and remove AppImage;
- inspect duplicates and permissions;
- check/apply an update after consent;
- export/restore backup and query activity.

### Infrastructure

- XDG directory resolver;
- atomic file writer and backup store;
- spec-aware desktop-entry codec;
- SQLite repositories and migrations;
- SHA-256 hasher and safe filesystem inspection;
- subprocess runner using argument arrays, timeouts and captured output;
- structured local activity log.

Query text, clipboard values and provider result content are excluded from the
activity log by default.

### Adapters

- local action sources: files, projects, repositories, notes, browser history,
  SSH configuration, task runners, media and clipboard;
- Plasma menu/cache refresh (`kbuildsycoca6` when available);
- icon theme and file picker integration;
- AppImage static metadata reader;
- embedded update-information adapter;
- optional external `appimageupdatetool` adapter, capability-detected;
- future GitHub Releases or zsync adapters behind the same update port.

### Interfaces

- CLI maps arguments to application commands and serialises results.
- GUI bridge exposes application view-models/signals to QML, including the
  palette query/results/preview lifecycle.
- QML owns layout, transitions and presentation state only.

## Action engine

The action engine is the product's common seam, not a generic plugin framework.

### Core contracts

An `ActionProvider` declares a stable ID, user-facing metadata, accepted query
scope, capabilities and risk class. It implements bounded operations equivalent
to:

```text
prepare(context) -> provider status
search(query, cancellation) -> stream/list of ActionResult
preview(result, cancellation) -> ActionPreview
execute(result, input, policy) -> ActionExecution
```

Providers may omit operations they do not support. Search and preview must be
side-effect free. Execution must state whether it is pure, read-only,
side-effecting or networked.

`ActionResult` has a stable provider-scoped ID, title, subtitle, icon, typed
payload, relevance components, available operations, risk marker and optional
preview handle. A result never smuggles an arbitrary callable through the
domain boundary.

### Search broker

- Normal queries fan out only to enabled providers whose trigger/scope matches.
- Each provider receives a time/result budget and cancellation token.
- A new keystroke cancels stale searches and prevents late results replacing
  the current generation.
- Ranking combines explicit scope, exact/prefix/fuzzy match, recency and
  provider confidence using documented deterministic weights.
- Provider failures degrade independently and remain inspectable through
  `doctor`; one slow provider cannot block the palette.
- Search history is off by default. Optional local recency stores stable result
  IDs/timestamps, not raw query, clipboard, note or browser-history text.

### Typed composition

MVP+ composition is intentionally small. Payloads use a controlled type set
such as `text/plain`, `text/path`, `text/url`, `internal/project`,
`internal/repository` and `internal/note`. A provider declares accepted and
produced types.

One result may be sent to a compatible pure/read-only transform. A
side-effecting execution is terminal. There is no saved graph, loop,
background trigger or multi-step workflow editor in MVP+.

## Palette runtime and KDE integration

The first palette is a standalone borderless Kirigami window/overlay. It is not
a KRunner plugin: KDE's documented runner extension path is C++-centred, while
Blazelauncher's Python action engine and richer preview/composition model should
first be proven without a second implementation stack.

Invocation modes:

1. `blazelauncher palette --toggle` cold-starts the application when it is not
   running.
2. Optional resident mode keeps the user-session GUI process alive and accepts
   authenticated same-user toggle/query messages through
   `QLocalServer`/`QLocalSocket` or an equivalently constrained local transport.
3. KDE's shortcut settings can bind the toggle command. MVP+ does not install
   low-level keyboard hooks or require a global-shortcut daemon.

The local IPC protocol is versioned, length-bounded and limited to control
messages; it does not expose a network listener. Stale socket cleanup and
same-user permissions require tests. Residency is a measured performance
choice, user-visible and reversible—not a hidden service.

## Built-in providers

The first complete palette milestone ships exactly 15 product actions, grouped
behind focused providers rather than one class per button:

| Group | Actions | Primary adapters |
| --- | --- | --- |
| Navigation | files, recent projects, Git repositories, Obsidian notes, browser history | bounded filesystem/index search; read-only snapshots |
| Execution | saved commands, workstation sessions, media, SSH destinations, `just`, `mise` | structured processes; capability detection |
| Transformation | unit conversion, UUID generation, text encode/decode, clipboard transformations | pure functions and Qt clipboard adapter |

Detailed behaviour and privacy rules live in `docs/PALETTE.md`.

## Script actions

Script manifest v1 is a local declarative adapter, not an extension system.
One TOML file defines one visible action with metadata, structured argv, input
mode, timeout, risk declaration and output type. The engine resolves and shows
the exact invocation before running it with `shell=False`.

Scripts cannot contribute dynamic search results, load Python into the process,
declare background triggers, install dependencies or download further
manifests. Standard output is bounded and becomes a typed text payload; it is
not interpreted as instructions. See `docs/SCRIPT-ACTIONS.md`.

## Data locations

Resolve paths from the environment; never assume `~/.local` directly.

```text
$XDG_CONFIG_HOME/blazelauncher/config.toml
$XDG_CONFIG_HOME/blazelauncher/actions/*.toml
$XDG_DATA_HOME/blazelauncher/cabinet/<app-id>/<version>/<file>.AppImage
$XDG_DATA_HOME/blazelauncher/icons/<managed icons>
$XDG_DATA_HOME/blazelauncher/backups/<transaction-id>/...
$XDG_DATA_HOME/applications/org.blazenetic.Blazelauncher.<id>.desktop
$XDG_STATE_HOME/blazelauncher/state.sqlite3
$XDG_CACHE_HOME/blazelauncher/<derived metadata>
```

Database migrations must be monotonic and covered by upgrade tests. Backups
should include a small manifest containing original path, hash, operation and
timestamp.

## Desktop-entry model

Implement against the freedesktop Desktop Entry Specification 1.5 unless a
newer adopted version is confirmed.

- Generate only `Type=Application` entries in MVP+.
- Treat `Exec` as structured executable plus arguments and field codes, not a
  shell string.
- Validate quoting and allowed field codes explicitly.
- Preserve case, locale keys and unknown `X-*` keys when adopting entries.
- Maintain a Blazelauncher ownership marker such as
  `X-Blazelauncher-Managed=true` and stable internal ID.
- Write to a temporary sibling, fsync where appropriate, validate, then rename.
- Back up an existing target before replacement.

## AppImage lifecycle

### Import

1. Resolve and stat the selected file without following surprising symlink
   changes.
2. Verify it is a regular file and calculate SHA-256 off the GUI thread.
3. Detect duplicates before copying.
4. Inspect metadata without executing the AppImage. If safe static extraction
   is unavailable, ask for user-supplied metadata rather than running it.
5. Copy into a staging directory, verify the copied hash, set only the required
   user execute bit after confirmation, then atomically activate it.
6. Record the version and activity transaction.

### Integration

Generate a Blazelauncher-owned desktop entry and managed icon that points to the
active cabinet version. Respect AppImage metadata such as
`X-AppImage-Integrate=false` and terminal launchers; surface the reason instead
of overriding it silently.

### Update and rollback

- Update checks are opt-in and reveal the source/URL before contact.
- Prefer embedded AppImage update information when present.
- Download into staging; verify basic file integrity and hash before activation.
- Never replace the current binary in place. Add a new version, switch the
  active pointer/launcher transactionally, then retain the previous version.
- Rollback is the same activation operation pointed at an older local version.
- Automatic cleanup must never remove the active or only known-good version.

## Security model

AppImages and launcher commands are executable content, not documents.

- Import, inspection and icon extraction must not launch the target.
- Test launch is a separate, explicit user action showing the exact executable,
  arguments, environment differences and working directory.
- Default subprocess calls use `shell=False`; a future expert shell mode must
  be clearly marked and isolated.
- Script manifests are executable intent. Load errors are visible; execution
  shows resolved argv, input source, working directory, risk and timeout.
- Clipboard text, palette queries, browser history, note content, SSH details
  and script output are sensitive ephemeral data and are not logged by default.
- Browser databases are read from bounded disposable snapshots; live profiles
  are never modified.
- SSH providers expose configured destinations, not keys, passwords,
  `known_hosts` contents or arbitrary wildcard expansion.
- Environment keys and paths are validated; secrets are not written into
  activity logs or exported diagnostics.
- Network work has consent, timeouts, size limits, TLS verification and clear
  cancellation.
- File operations defend against path traversal, symlink swaps, partial copies
  and cross-device rename behaviour.
- No root or system-wide mutations are needed for MVP+.

## Concurrency and responsiveness

Provider searches, hashing, copies, static extraction, subprocesses and network
operations run in bounded workers. UI state receives progress and cancellation
events. Query generations cancel stale provider work. Mutations for the same
launcher/cabinet app are serialised; read-only work may run concurrently within
provider and global budgets.

## CLI contract

Proposed command families:

```text
blazelauncher palette show|toggle|query
blazelauncher action list|show|run|validate
blazelauncher launcher list|show|create|edit|clone|validate|test|export|remove
blazelauncher appimage list|show|import|integrate|activate|check|update|rollback|remove
blazelauncher backup list|restore|export
blazelauncher doctor
```

All read and mutation commands should support stable exit codes. Machine use
adds `--json`; JSON carries a schema version, result/error object and no
human-only decorations. Mutations gain `--dry-run` where meaningful.

## Testing strategy

- Unit tests for parsing, quoting, validation, IDs, transitions and policies.
- Contract tests for provider cancellation, result stability, deterministic
  ranking, typed composition, risk gates and script manifests.
- Fixture-backed tests for browser, note, SSH, repository and task providers;
  never inspect the test runner's real local data.
- Performance harnesses for palette visibility, first result and stale-query
  cancellation with environment/hardware recorded.
- Golden fixtures for `.desktop` files, including spaces, field codes,
  localisation and unknown keys.
- Integration tests under temporary XDG roots for every mutation and rollback.
- Fake subprocess/network/update ports for deterministic tests.
- Qt model tests plus a small number of GUI smoke tests; avoid brittle pixel
  assertions.
- Real-system exploratory checks on CachyOS/KDE Plasma/Wayland before release.
- CI on a mainstream Linux runner; an Arch container job validates the primary
  packaging path.

## Packaging

Prioritise:

1. development install from source;
2. reproducible Arch `PKGBUILD` suitable for an AUR package;
3. signed/tagged source releases;
4. optional standalone bundle after dependency and QML-plugin behaviour is
   proven;
5. Flatpak only after designing host-filesystem and launch permissions honestly.

Do not make Blazelauncher itself an AppImage until the recursive integration
and update story has been tested.
