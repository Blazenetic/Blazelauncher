# Blazelauncher

Build launchers. Run actions. Keep AppImages. Stay in control.

Blazelauncher is a local-first Linux command surface for people who want to see
what their desktop is about to do. Before it runs anything it shows the exact
executable, the arguments, the working directory, the environment differences
and how risky the action is. Before it changes a file it shows the file, writes
it atomically and keeps a way back.

That is the actual idea. The three surfaces below are how it reaches you:

- **Command Palette** — search, preview, execute and compose high-value local
  actions for developer and workstation workflows.
- **Launcher Studio** — create, validate, test, back up and manage freedesktop
  `.desktop` launchers without hand-editing them.
- **AppImage Cabinet** — import, organise, integrate, version and roll back
  AppImages without becoming a universal software centre.

They are peers over one action engine, so a command means the same thing and is
executed the same way wherever you found it.

The primary experience targets CachyOS and Arch-family systems running KDE
Plasma 6 on Wayland. The underlying engine follows XDG and freedesktop
standards so other Linux desktops can be supported without contaminating the
core model with Plasma-specific assumptions.

## Where it fits

Good tools already exist for parts of this. KRunner ships with Plasma and is
excellent at launching installed applications and answering system queries.
Albert, ULauncher and Kando cover the keyboard-launcher niche. MenuLibre edits
desktop entries. Gear Lever and AppImageLauncher manage AppImages.

Blazelauncher is not trying to win any of those on their own ground — the
palette explicitly leaves ordinary application launching to KRunner. What none
of them offer is a single surface where a developer action, a launcher and a
managed binary share one execution model, one preview and one risk marker, and
where every file change is reversible. That gap is the reason this exists.

If you want a launcher that opens Firefox quickly, use KRunner. If you want to
see the exact `just` recipe, its directory and its argv before it runs, and to
know that the launcher you generated last week can be restored from a backup,
that is this.

## Project status

**Planning and harness.** The product contract, architecture, palette
specification and roadmap are written. The verification harness that will grade
the implementation is in place and running: lint, types, import contracts,
boundary guards, XDG-isolated tests and a two-tier CI. There is no application
code yet.

`docs/STATUS.md` is the current state of the repository. Read it first.

Start here:

1. [Status](docs/STATUS.md)
2. [Product brief](docs/PRODUCT.md)
3. [Architecture](docs/ARCHITECTURE.md)
4. [Command Palette specification](docs/PALETTE.md)
5. [Script action manifest](docs/SCRIPT-ACTIONS.md)
6. [MVP+ roadmap](docs/ROADMAP.md)
7. [Contributor and agent contract](AGENTS.md)

## Getting set up

```bash
scripts/bootstrap-dev.sh   # system packages, then a virtual environment
scripts/verify.sh          # the checks that CI runs
```

Arch and CachyOS get everything, including Kirigami, `qmllint` and the
freedesktop validators. Other distributions get the checks that run anywhere;
the rest report SKIP and are covered by the Arch container job in CI.

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

MVP+ ships 15 built-in palette actions and a constrained local script
manifest — no extension marketplace.

No privileged/system daemon, background telemetry or mandatory account is part
of the design. Network activity is explicit and opt-in. A user may optionally
keep the palette UI resident for fast toggling through local-only IPC.

## How this repository is built

Most of the work here is done by AI coding agents, one bounded issue at a time,
with human review before anything merges. That shapes the repository:
boundaries are written down in `AGENTS.md`, the ones that can be checked
mechanically are enforced by tests rather than by review, and every change
updates `docs/STATUS.md` so the next contributor — human or not — starts from
what is actually true.

If you are picking up an issue, `AGENTS.md` is the contract and
`docs/AGENT-PROMPT.md` is the prompt template.

## Intended installation targets

The first supported development and packaging target is Arch/CachyOS. A
Flatpak package is useful later, but its sandbox makes arbitrary local command
and AppImage management a separate design problem; it is not the first release
target.

## Licence

[MIT](LICENSE)
