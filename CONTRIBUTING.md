# Contributing

Thanks for helping make Linux application launchers calmer and safer.

Read `docs/STATUS.md` for where the project actually is, then `AGENTS.md`,
which applies to human and AI contributors alike. Then choose an open issue with
a bounded outcome, or propose one before beginning a substantial change.

## Setting up

```bash
scripts/bootstrap-dev.sh   # system packages, then a virtual environment
scripts/verify.sh          # the checks CI runs
```

Arch and CachyOS get the full toolchain. Elsewhere the Qt, QML and freedesktop
checks report SKIP — Kirigami 6 is not installable from PyPI — and are covered
by the Arch container job in CI.

## Principles

- Keep Blazelauncher focused on local actions, launchers and AppImage lifecycle
  management—not package management or a general automation platform.
- Prefer a small vertical slice that users can exercise.
- Add tests around file/process behaviour and use temporary XDG directories.
- Explain new production dependencies and security-relevant choices.
- Preserve freedesktop/XDG compatibility even when polishing KDE integration.

## Pull requests

Use a focused branch and complete the repository PR template. A material UI
change should include a screenshot or recording where practical. Never include
personal paths, environment values, tokens or imported executable samples.

Paste the real output of `scripts/verify.sh`, and be explicit about what you
could not verify — several acceptance criteria here need a live KDE Plasma 6
Wayland session and simply cannot be checked anywhere else. Update
`docs/STATUS.md` in the same pull request.

By contributing, you agree that your contribution is licensed under the MIT
licence.
