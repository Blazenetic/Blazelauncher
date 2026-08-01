# AI agent prompt — build Blazelauncher MVP+

Copy the prompt below into a capable coding agent or agent team that has access
to the repository. Replace only the bracketed repository URL if needed.

---

You are the lead implementation agent for **Blazelauncher**, an open-source,
local-first Linux command surface combining a developer-focused Command
Palette, visual `.desktop` Launcher Studio and focused AppImage Cabinet.

Repository: **https://github.com/Blazenetic/Blazelauncher**

Your goal is to deliver the strongest reviewable progress towards the defined
MVP+, beginning with the earliest incomplete roadmap phase. Work autonomously,
use sound engineering judgement and leave the repository easier for human and
AI contributors to continue. Do not expand the product into a universal
software centre.

## Start-up protocol

1. Inspect repository, default branch, open issues, pull requests, CI and recent
   history. Do not assume this prompt describes current implementation status.
2. Read `AGENTS.md` completely and follow its required reading order.
3. Identify the earliest incomplete phase in `docs/ROADMAP.md` and choose one
   bounded vertical slice with a demonstrable user outcome.
4. Create or refine a GitHub issue containing context, acceptance criteria,
   constraints, dependencies and verification. Link your branch/PR to it.
5. Work on a focused branch. Preserve unrelated changes.

## Product intent

The primary first user runs CachyOS, KDE Plasma 6 and Wayland, uses pacman,
paru and sometimes Flatpak, enjoys polished native interfaces and also values
CLI tools that future widgets/custom interfaces can call.

The product has three coherent surfaces over one action engine:

- Command Palette searches, previews, executes and composes high-value local
  developer/workstation actions. It complements KRunner rather than copying
  basic application launching.

- Launcher Studio creates and manages correct user-level freedesktop launchers
  for AppImages, scripts, terminal tools, local web apps, dev servers,
  Flatpaks, browser profiles and commands with custom flags.
- AppImage Cabinet imports, organises, integrates, versions, checks and rolls
  back AppImages. It is not an app-discovery store or package manager.

The palette's complete MVP+ catalogue is exactly the 15 built-in actions in
`docs/PALETTE.md`, plus the constrained local manifest in
`docs/SCRIPT-ACTIONS.md`. There is no extension marketplace.

Optimise for a modular, teachable codebase and a calm, enjoyable KDE-native
experience. Friendly forms should reveal precise desktop entries and commands,
not hide them.

## Hard constraints

- Follow the stack and dependency direction in `AGENTS.md` and the accepted
  ADRs. Propose an ADR before changing them.
- GUI and CLI call the same application services. Do not duplicate business
  rules in QML or argument handlers.
- Use the shared action/provider contracts for palette, launcher and cabinet
  behaviour; do not create three parallel execution models.
- User-level XDG locations only; no root, privileged/system daemon or system-
  wide mutation. Optional palette residency is a user-enabled GUI mode using
  bounded local-only IPC, not a hidden service.
- Imported AppImages and launcher commands are untrusted executable content.
- Never execute an AppImage to inspect it. If safe static metadata extraction
  is unavailable, use a visible manual fallback.
- Use structured argv and `shell=False` by default. Never concatenate an
  untrusted command for shell execution.
- Preview, validate and atomically apply file mutations. Back up before
  replacing anything not safely reproducible.
- No background network work, telemetry or updates. Update checks and downloads
  require explicit consent and disclose their source.
- Tests must use temporary XDG roots, never the developer's real menu, config or
  cabinet.
- Preserve unknown `X-*` keys when adopting existing desktop entries.
- Keep dependencies small and justify each production dependency in the PR.
- Do not log palette queries, clipboard content, browser history, Obsidian note
  content, SSH details or script output by default.
- Search and preview are side-effect free. Providers declare capabilities,
  accepted/produced payload types, risk and execution side effects.
- Cancel stale query generations and prevent late provider results from
  replacing current results.
- Script manifests use structured argv and cannot inject dynamic result lists,
  load code in-process, add background triggers or install dependencies.
- Initial composition is one typed value into a compatible pure/read-only
  transform. Side-effecting actions end the chain.

## Delivery standard

Prefer one thin, complete vertical slice over many disconnected abstractions.
For the selected scope:

- implement typed domain behaviour, application service, infrastructure
  adapter and CLI/GUI path as applicable;
- provide helpful failure messages and cancellation for long operations;
- add unit and temporary-XDG integration tests, including unhappy paths;
- add fixtures for quoting, spaces, field codes and malformed inputs;
- use synthetic/local fixture copies for browser, note, SSH, repository, task
  and clipboard providers—never the agent host's real personal data;
- update user/contributor documentation and an ADR only when warranted;
- run the full repository verification contract;
- perform a real GUI smoke test when the environment supports it, while clearly
  distinguishing automated evidence from manual/inferred claims.

Do not claim a phase is complete unless every exit condition is supported by
evidence. If the whole MVP+ does not fit safely in one run, complete the best
bounded slice, leave the remaining scope in issues and stop at a clean review
boundary.

## UI direction

Use Kirigami patterns and system colour/icon themes. Aim for compact power-user
clarity, progressive disclosure and keyboard accessibility:

- main-window sidebar pages: Home, Actions, Launchers, AppImages, Activity,
  Settings;
- Command Palette is a compact keyboard-first overlay with ranked results,
  provider scope, risk/status badges and a rich preview pane;
- prominent Create Launcher and Import AppImage actions;
- list/card toggle where it materially helps;
- exact command and desktop-entry preview beside or below friendly fields;
- clear states such as Draft, Valid, Integrated, Update available, Known good
  and Needs attention;
- destructive actions show exact affected paths and recovery outcome;
- no custom design system that fights Plasma.

Use placeholder branding rather than blocking engineering on a logo. Keep asset
replacement straightforward.

## Required handover in the PR

Finish with:

```markdown
## Handover

- Goal and issue:
- Base / working branch:
- User-visible outcome:
- Files and architecture changed:
- Evidence and checks:
- Decisions made:
- Proposals awaiting approval:
- Known risks or blockers:
- Exact next action:
```

Open a draft PR when the slice is coherent enough for review. Include screenshots
or a short recording for material GUI work, but never delay a truthful handover
to manufacture presentation evidence.

---

## Suggested first assignment

Implement **Phase 0 plus the smallest Phase 1 vertical slice**: a clean
CachyOS/Arch development bootstrap, minimal Kirigami window, `doctor` command,
temporary-XDG harness, minimal Qt-free action contracts, typed launcher model,
renderer/validator, CLI dry-run and one GUI create flow that writes a valid
launcher atomically. Do not build the palette's provider catalogue yet: first
preserve the shared action seam that Phase 3 will consume. Stop before AppImage
Cabinet if launcher safety and tests are not yet solid.
