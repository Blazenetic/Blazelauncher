# Security policy

## Reporting

Please do not open a public issue for a vulnerability that could lead to
unexpected code execution, path traversal, arbitrary file overwrite, update
substitution or loss of managed versions. Use GitHub's private vulnerability
reporting for this repository when enabled. If it is unavailable, contact the
maintainer privately through the contact method on the owner's GitHub profile.

## Security posture

Blazelauncher manages executable content. Its safety contract includes:

- no AppImage execution during import or metadata inspection;
- no shell interpolation by default;
- user-level XDG mutations only;
- explicit test launches and network/update consent;
- staged, verified and reversible file changes;
- redaction of environment values from logs and diagnostics.

Only the latest tagged release is expected to receive security fixes before a
stable maintenance policy is announced.
