# ADR 0004: How the Command Palette presents itself on Wayland

- Status: Proposed. Blocked on a spike; must be accepted before Phase 3 begins.
- Date: 2026-08-01

## Context

ADR 0003 decided that the palette is a standalone Kirigami overlay rather than
a KRunner plugin. It did not say how that overlay gets on screen, and on the
primary target — KDE Plasma 6 on Wayland — that is not a detail.

Under Wayland a client cannot place its own windows. There is no protocol for
an ordinary `xdg-toplevel` to position itself over the active output, and a
window generally cannot raise or focus itself on demand. A launcher overlay
wants all three. The usual answer is the `wlr-layer-shell` protocol, which KDE
exposes through the `LayerShellQt` library and uses for KRunner itself.

`LayerShellQt` is a C++ Qt library. It has no Python bindings. There appears to
be a process-wide route through the `QT_WAYLAND_SHELL_INTEGRATION=layer-shell`
environment variable, but per-window configuration — anchors, keyboard
interactivity, exclusive zones — is C++ API. None of this has been tested from
PySide6, and the fallback behaviour on a system without layer-shell support is
also untested.

The same spike should confirm the surrounding assumption in ADR 0001: PySide6
driving Kirigami 6 is a supported and comfortable combination for a whole
application, not just a window that opens.

This is the load-bearing unknown for Phase 3. Every issue from #11 onwards
assumes an overlay that appears instantly, centred, focused and dismissible.

## Options

1. **Ordinary `xdg-toplevel`.** No extra dependency; the compositor decides
   placement and focus. Simple, and possibly good enough on Plasma with a
   window rule — but placement becomes advisory and the experience varies by
   compositor.
2. **Layer-shell through the environment variable.** Correct behaviour with no
   C++ in the build, if the shell integration plugin can be activated for a
   single window and configured well enough from QML.
3. **Layer-shell through a small compiled helper.** A minimal C++ or PyBind
   shim over `LayerShellQt`. Correct and configurable, at the cost of a
   compiled component in a Python project and a harder packaging story.
4. **KWin window rules shipped with the application.** Placement handled by
   configuration the user installs. Plasma-specific, and it puts behaviour in
   a file the user can silently break.

## Decision

Deferred. The spike decides, and this record is updated with the outcome.

## Decision criteria

- Does the overlay appear centred on the active output, focused and accepting
  keyboard input, from a cold start and from a resident process?
- Does Escape dismiss it, and does it behave over a fullscreen window?
- What happens on a compositor without layer-shell, and on X11?
- What does the chosen route cost at packaging time on Arch?
- Are the toggle-to-visible measurements in `docs/PALETTE.md` achievable, and
  under which mode?

## Consequences

Until this is settled, Phase 3 estimates carry an unpriced risk. If the answer
is option 3, the project acquires a compiled component and ADR 0001's "Python
plus PySide6" framing needs revisiting. If it is option 1, the performance
targets in `docs/PALETTE.md` may need to be restated as compositor-dependent
rather than absolute.

Recording the question now means the answer arrives before five phases of work
have assumed one.
