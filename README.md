# Blazelauncher

Build launchers. Run actions. Keep AppImages. Stay in control.

Blazelauncher is a focused, local-first Linux command surface combining:

- **Command Palette** — search, preview, execute and compose high-value local
  actions for developer and workstation workflows.

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
3. [Command Palette specification](docs/PALETTE.md)
4. [Script action manifest](docs/SCRIPT-ACTIONS.md)
5. [MVP+ roadmap](docs/ROADMAP.md)
6. [AI agent build prompt](docs/AGENT-MVP-BUILD-PROMPT.md)
7. [Contributor and agent contract](AGENTS.md)

## Product shape

```text
Command Palette | Launcher Studio | AppImage Cabinet | CLI
                             |
                  Shared action services
                             |
 Provider search | desktop-entry | AppImage | safety adapters
                             |
           XDG user directories and local sources
```

Every surface is a peer over the same action and application services. Business
rules must not live in QML or CLI handlers.

## MVP+ boundary

Blazelauncher will run local actions, manage user-owned launchers and maintain a
managed AppImage cabinet. It may generate launchers for scripts, local web apps,
developer servers, terminal tools, Flatpaks, browser profiles and system
commands. It will **not** manage pacman, paru, Flatpak repositories or system
packages.

The palette does not try to replace KRunner's ordinary application launching.
Its differentiation is developer workflows, composable typed actions and rich
previews. MVP+ ships 15 built-in actions and a constrained local script
manifest—no extension marketplace.

No privileged/system daemon, background telemetry or mandatory account is part
of the design. Network activity is explicit and opt-in. A user may optionally
keep the palette UI resident for fast toggling through local-only IPC.

## Intended installation targets

The first supported development and packaging target is Arch/CachyOS. A
Flatpak package is useful later, but its sandbox makes arbitrary local command
and AppImage management a separate design problem; it is not the first release
target.

## Licence

[MIT](LICENSE)
