## Outcome

<!-- What user-visible or contributor-visible outcome does this deliver? -->

Closes #

## Scope

- Included:
- Explicitly deferred:

## Safety and compatibility

- [ ] Uses temporary XDG roots in tests
- [ ] Does not add shell interpolation or implicit executable inspection
- [ ] File mutations are previewed/atomic/recoverable as applicable
- [ ] Network behaviour remains explicit and opt-in
- [ ] KDE-specific behaviour stays behind an adapter
- [ ] Queries, clipboard, history, notes, SSH data and script output are not
      logged or exposed unexpectedly
- [ ] Action risk, inputs, outputs and side effects are declared and previewed

## Evidence

Paste the `scripts/verify.sh` summary:

```text

```

- [ ] `scripts/verify.sh` passes, and any SKIP is explained below
- [ ] `docs/STATUS.md` updated
- [ ] The verification harness was not weakened to make this pass

### Not verified here

<!--
List anything you could not check, and why. Acceptance criteria needing a KDE
Plasma 6 Wayland session — the application menu, QML rendering, compositor
behaviour, every performance target — belong here rather than ticked above.
"Not verified" is a normal outcome. A wrong claim is not.
-->

- 

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
