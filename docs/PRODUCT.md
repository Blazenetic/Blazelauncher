# Product brief

## Vision

Blazelauncher makes locally managed Linux applications feel intentional. It
gives power users a polished place to create launchers and care for AppImages,
while retaining transparent files, standards and CLI control underneath.

## Primary user

The first user is a technical KDE Plasma/Wayland user on CachyOS or another
Arch-family distribution who:

- runs AppImages, scripts, browser profiles, developer tools and local web apps;
- values a polished interface but still wants CLI and inspectable files;
- customises icons, categories, flags and working directories;
- wants local ownership, backups and predictable rollback;
- does not want a universal app store or a daemon watching the system.

The architecture should welcome other Linux desktops later without weakening
the KDE-first experience.

## Jobs to be done

### Launcher Studio

When I have a command or application that belongs in my desktop environment, I
want to turn it into a correct launcher, test it safely and maintain it without
memorising desktop-entry syntax.

Useful targets include:

- AppImages and normal binaries;
- scripts and terminal tools;
- local web apps and browser profiles;
- developer servers and project-specific commands;
- Flatpak commands with explicit flags;
- Wayland/Electron compatibility presets;
- custom environment variables and working directories.

### AppImage Cabinet

When I download an AppImage, I want to place it in a managed cabinet, give it a
good identity, integrate it with Plasma and replace or roll it back deliberately
without losing older working versions.

## Experience principles

1. **Friendly first, exact underneath.** Start with name, command and icon;
   reveal advanced fields progressively. Always provide an exact command and
   desktop-file preview.
2. **Safe by construction.** No hidden shell evaluation, surprise execution,
   background downloads or silent overwrites.
3. **Reversible confidence.** Show the impact, write atomically and retain a
   recoverable previous state.
4. **Native without lock-in.** Feel at home in Plasma while keeping the engine
   grounded in freedesktop and XDG standards.
5. **Useful at every layer.** GUI actions map to stable application services;
   CLI commands expose the same capability and optionally versioned JSON.
6. **Calm density.** A compact power-user interface is welcome; avoid visual
   noise, modal chains and settings sprawl.

## Information architecture

- **Home** — recent launchers, cabinet health, update checks awaiting consent,
  quick create/import actions.
- **Launchers** — search, filter, create, edit, clone, validate, test, export,
  back up and restore.
- **AppImages** — cards/list view, versions, integration state, notes, launch
  flags, file health and deliberate update/rollback actions.
- **Activity** — local audit trail of writes, integrations, updates and
  rollbacks with paths and results.
- **Settings** — cabinet location, backup retention, update consent and
  desktop-specific adapters.

## MVP+ capabilities

### Launcher Studio

- visual launcher editor with icon picker and live preview;
- name, comment, executable/URL, arguments, environment, working directory,
  terminal toggle, categories, keywords and visibility;
- data-driven presets for common Wayland/Electron, Flatpak and browser-profile
  patterns (previewed, never silently injected);
- spec-aware validation plus `desktop-file-validate` when installed;
- explicit test launch with exact command preview and captured exit result;
- import/adopt, duplicate, export, backup and restore;
- user application-menu integration and cache refresh adapter;
- corresponding CLI commands and `--json` output.

### AppImage Cabinet

- drag/drop or file-picker import into a managed directory;
- SHA-256 identity, size, permissions and duplicate detection;
- editable name, icon, notes, categories, flags and working directory;
- safe, best-effort static metadata extraction; no import-time execution;
- create/remove a managed launcher in the user application menu;
- retain several managed versions and select the active version;
- deliberate rollback and duplicate cleanup with preview;
- opt-in update detection from embedded update information, with adapters for
  additional sources later;
- explicit update download/apply flow that keeps the previous version.

## Success measures for the first real user

- A new script launcher can be created, validated and launched in under two
  minutes without editing a file.
- An AppImage can be imported and visible in Plasma's menu in under one minute.
- Every generated launcher passes internal validation; supported fixtures also
  pass `desktop-file-validate`.
- A failed or unwanted AppImage replacement can be rolled back without hunting
  through downloads.
- The GUI never freezes during hashing, extraction, launching or network work.
- A capable user can complete the same core workflows using the CLI.

## Explicit non-goals

- universal software discovery or an app store;
- managing pacman, paru/AUR, Flatpak remotes or system packages;
- privileged/system-wide installation in MVP+;
- automatic background updates;
- arbitrary container/sandbox orchestration;
- Windows or macOS support;
- a Plasma widget in MVP+ (the stable CLI/JSON surface is designed to enable
  one later);
- cloud sync, accounts or telemetry.

## Open product questions

- Should managed AppImages default to one shared cabinet directory or one
  directory per application? The architecture currently recommends per-app
  directories beneath one cabinet root.
- How many previous versions should be retained by default? Recommendation:
  two previous versions, configurable.
- Should adopted third-party launchers be edited in place or copied into a
  Blazelauncher-owned file? Recommendation: copy/adopt by default and require a
  deliberate advanced action for in-place editing.
