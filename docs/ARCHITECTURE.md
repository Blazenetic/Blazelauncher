# Architecture

## Recommendation

Build Blazelauncher as a modular Python application with a PySide6/QML/Kirigami
GUI and a standard-library CLI. Keep domain and application services free of
Qt. Use SQLite for cabinet state and an explicit filesystem transaction layer
for all user-visible mutations.

This is an MVP+ optimisation: it provides a native Plasma experience, fast
iteration and an approachable codebase while preserving seams where a more
performance-sensitive component could later move to Rust or C++ without a UI
rewrite.

## System context

```text
User
  |-- KDE GUI ----------------------|
  |-- CLI / scripts -- versioned ---|-- Application services
                                      |-- Launcher service
                                      |-- Cabinet service
                                      |-- Update service
                                      |-- Backup/activity service
                                             |
                              Ports / infrastructure adapters
                                |-- XDG filesystem
                                |-- desktop-entry parser/renderer
                                |-- SQLite repository
                                |-- Plasma cache refresh
                                |-- safe subprocess runner
                                |-- AppImage inspector/updaters
```

## Technology decisions

See the decision records in `docs/decisions/`.

- Python 3.12+ for the core and application layer.
- PySide6 (official Qt for Python bindings) with QML and Kirigami 6.
- `argparse` for a dependency-light CLI.
- SQLite for transactional metadata, notes, activity and version relationships.
- Ordinary XDG files remain the source of truth for installed launchers and
  managed binaries; SQLite is an index/control record, not a proprietary vault.
- No daemon, root helper or message bus service in MVP+.

## Modules and dependency rules

### Domain

Typed value objects and invariants:

- `Launcher`, `CommandSpec`, `EnvironmentVariable`, `DesktopCategory`;
- `CabinetApp`, `AppImageVersion`, `IntegrationState`, `UpdateCandidate`;
- paths, hashes, IDs and safe validation results;
- typed errors that can be rendered differently by GUI and CLI.

The domain has no Qt, filesystem, network or process imports.

### Application

Use cases coordinating ports and transactions:

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

### Adapters

- Plasma menu/cache refresh (`kbuildsycoca6` when available);
- icon theme and file picker integration;
- AppImage static metadata reader;
- embedded update-information adapter;
- optional external `appimageupdatetool` adapter, capability-detected;
- future GitHub Releases or zsync adapters behind the same update port.

### Interfaces

- CLI maps arguments to application commands and serialises results.
- GUI bridge exposes application view-models/signals to QML.
- QML owns layout, transitions and presentation state only.

## Data locations

Resolve paths from the environment; never assume `~/.local` directly.

```text
$XDG_CONFIG_HOME/blazelauncher/config.toml
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
- Environment keys and paths are validated; secrets are not written into
  activity logs or exported diagnostics.
- Network work has consent, timeouts, size limits, TLS verification and clear
  cancellation.
- File operations defend against path traversal, symlink swaps, partial copies
  and cross-device rename behaviour.
- No root or system-wide mutations are needed for MVP+.

## Concurrency and responsiveness

Hashing, copies, static extraction, subprocesses and network operations run in
bounded workers. UI state receives progress and cancellation events. Mutations
for the same launcher/cabinet app are serialised; read-only list/detail work may
run concurrently.

## CLI contract

Proposed command families:

```text
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
