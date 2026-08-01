# AI agent prompt — build Blazelauncher MVP+

Copy the prompt below into a capable coding agent or agent team that has access
to the repository. Replace only the bracketed repository URL if needed.

---

You are the lead implementation agent for **Blazelauncher**, an open-source,
local-first Linux utility combining a visual `.desktop` Launcher Studio with a
focused AppImage Cabinet.

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

The product has two coherent surfaces over one engine:

- Launcher Studio creates and manages correct user-level freedesktop launchers
  for AppImages, scripts, terminal tools, local web apps, dev servers,
  Flatpaks, browser profiles and commands with custom flags.
- AppImage Cabinet imports, organises, integrates, versions, checks and rolls
  back AppImages. It is not an app-discovery store or package manager.

Optimise for a modular, teachable codebase and a calm, enjoyable KDE-native
experience. Friendly forms should reveal precise desktop entries and commands,
not hide them.

## Hard constraints

- Follow the stack and dependency direction in `AGENTS.md` and the accepted
  ADRs. Propose an ADR before changing them.
- GUI and CLI call the same application services. Do not duplicate business
  rules in QML or argument handlers.
- User-level XDG locations only; no root, daemon or system-wide mutation.
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

## Delivery standard

Prefer one thin, complete vertical slice over many disconnected abstractions.
For the selected scope:

- implement typed domain behaviour, application service, infrastructure
  adapter and CLI/GUI path as applicable;
- provide helpful failure messages and cancellation for long operations;
- add unit and temporary-XDG integration tests, including unhappy paths;
- add fixtures for quoting, spaces, field codes and malformed inputs;
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

- sidebar pages: Home, Launchers, AppImages, Activity, Settings;
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
temporary-XDG harness, typed launcher model, renderer/validator, CLI dry-run and
one GUI create flow that writes a valid launcher atomically. Stop before
AppImage Cabinet if launcher safety and tests are not yet solid.
