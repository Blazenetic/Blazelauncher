# Blazelauncher

Build launchers. Keep AppImages. Stay in control.

Blazelauncher is a focused, local-first Linux desktop utility combining:

- **Launcher Studio** — create, validate, test, back up and manage freedesktop
  `.desktop` launchers without hand-editing them.
- **AppImage Cabinet** — import, organise, integrate, version and roll back
  AppImages without becoming a universal software centre.

The primary experience targets CachyOS and Arch-family systems running KDE
Plasma 6 on Wayland. The underlying engine follows XDG and freedesktop
standards so other Linux desktops can be supported without contaminating the
core model with Plasma-specific assumptions.

## Project status

**Planning / bootstrap.** The product contract, architecture and MVP+ build
brief are ready for the first implementation agent. No working application has
been released yet.

Start here:

1. [Product brief](docs/PRODUCT.md)
2. [Architecture](docs/ARCHITECTURE.md)
3. [MVP+ roadmap](docs/ROADMAP.md)
4. [AI agent build prompt](docs/AGENT-MVP-BUILD-PROMPT.md)
5. [Contributor and agent contract](AGENTS.md)

## Product shape

```text
Native KDE GUI (PySide6 + QML/Kirigami)
                 |
Versioned application services
                 |
Desktop-entry | AppImage | backup | update adapters
                 |
       XDG user directories and local files
                 |
     blazelauncher CLI (--json available)
```

The GUI and CLI are peers over the same application services. Business rules
must not live in QML or CLI handlers.

## MVP+ boundary

Blazelauncher will manage user-owned launchers and a managed AppImage cabinet.
It may generate launchers for scripts, local web apps, developer servers,
terminal tools, Flatpaks, browser profiles and system commands. It will **not**
manage pacman, paru, Flatpak repositories or system packages.

No root daemon, privileged helper, background telemetry or mandatory account is
part of the design. Network update checks are explicit and opt-in.

## Intended installation targets

The first supported development and packaging target is Arch/CachyOS. A
Flatpak package is useful later, but its sandbox makes arbitrary local command
and AppImage management a separate design problem; it is not the first release
target.

## Licence

[MIT](LICENSE)
