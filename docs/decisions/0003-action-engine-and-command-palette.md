# ADR 0003: Shared action engine and standalone Command Palette

- Status: Accepted for MVP+
- Date: 2026-08-02

## Context

Launcher Studio and AppImage Cabinet already share command, executable and
desktop-integration concepts. Adding developer workflows as a separate palette
would duplicate models, execution safety and UI state. Treating every idea as a
generic extension would instead create an immature plugin platform before the
core workflows are proven.

KRunner already provides strong application and system search. KDE's documented
runner extension tutorial is C++-centred, whereas Blazelauncher uses Python,
PySide6 and Kirigami. The product also needs richer previews, typed composition
and explicit risk details beyond a basic application result.

Qt for Python provides local server/socket APIs suitable for same-machine
single-instance control, allowing an optional warm palette without adding a
privileged or network daemon.

References:

- [KDE KRunner plugin documentation](https://develop.kde.org/docs/plasma/krunner/)
- [PySide6 QLocalServer](https://doc.qt.io/qtforpython-6/PySide6/QtNetwork/QLocalServer.html)
- [PySide6 QLocalSocket](https://doc.qt.io/qtforpython-6/PySide6/QtNetwork/QLocalSocket.html)

## Decision

1. Introduce a Qt-free action domain and provider contract shared by Command
   Palette, Launcher Studio, AppImage Cabinet and CLI.
2. Build a standalone Kirigami palette rather than a KRunner plugin in MVP+.
3. Compete on developer workflows, local knowledge, rich previews, typed
   composition and execution transparency—not basic application launching.
4. Ship exactly 15 built-in actions before expanding the catalogue.
5. Support one constrained local TOML manifest per script action; do not ship a
   marketplace, remote registry or dynamic provider protocol.
6. Limit initial composition to one typed value passed to compatible pure/read-
   only transforms. Side-effecting actions terminate the chain.
7. Support cold-start invocation and an optional user-enabled resident GUI
   process controlled through versioned, bounded, local-only IPC. Do not add a
   root helper, privileged/system daemon or network listener.

## Consequences

- All product surfaces share validation, risk, preview and execution policy.
- The launcher and cabinet remain coherent rather than becoming legacy modules
  beside a new palette.
- A standalone overlay can optimise its interaction model without KRunner API
  or C++ constraints.
- Basic installed-app search may feel less comprehensive than KRunner; this is
  intentional and should be explained in the UI/docs.
- Provider cancellation, ranking, privacy and latency become first-class
  engineering requirements.
- Optional residency slightly expands lifecycle/IPC complexity and therefore
  requires measurement, same-user socket controls and a visible preference.
- The constrained script model covers personal commands but deliberately cannot
  provide dynamic search results or background automation.

## Revisit triggers

- The action API is stable and users consistently request KRunner exposure.
- Measured cold/warm performance shows local sockets or residency are the wrong
  trade-off.
- At least several real script actions cannot be expressed safely by manifest
  v1 and a dynamic protocol has a credible security design.
- Typed one-step composition proves insufficient for common real workflows;
  any expansion requires a separate workflow-engine decision, not silent scope
  creep.
