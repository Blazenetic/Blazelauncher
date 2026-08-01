# ADR 0002: Local-first, user-level and reversible mutations

- Status: Accepted
- Date: 2026-08-02

## Context

The application manages executable files and application-menu entries. A
mistake can hide launchers, run an unexpected command or lose a known-good
AppImage. Root privileges, a privileged/system daemon and automatic updates
would enlarge the security and operational surface before they provide proven
value. A command palette may later justify an optional user-session resident UI
for measured responsiveness, but that is a distinct and reversible choice.

## Decision

- Operate only in user-level XDG locations during MVP+.
- Require no root, privileged helper, privileged/system daemon, cloud account
  or telemetry.
- Permit an optional user-enabled resident palette GUI only through bounded
  same-user local IPC, with cold-start mode retained. See ADR 0003.
- Treat import, inspection, update checking, downloading, testing and
  integration as separate user-visible actions.
- Use atomic writes, staging, hash verification and transaction manifests.
- Keep previous launcher/AppImage state recoverable under a documented
  retention policy.
- Make network access opt-in and source-disclosed.
- Use structured process arguments and no shell by default.

## Consequences

The product is easier to understand, test and recover. Some system-wide use
cases and background convenience are deferred. Flatpak packaging cannot be
treated as a transparent wrapper because sandbox permissions materially change
the product; it requires a later design decision.
