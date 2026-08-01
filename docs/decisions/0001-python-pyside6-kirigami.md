# ADR 0001: Python, PySide6 and Kirigami 6

- Status: Accepted for MVP+
- Date: 2026-08-02

## Context

Blazelauncher needs a polished KDE Plasma interface, a first-class CLI, strong
filesystem/process safety and a codebase that a small human/AI team can extend
quickly. C++/Qt is maximally native but increases implementation cost. A web
shell weakens native integration. Rust/Qt bindings add maturity and packaging
risk for this bounded MVP+.

KDE documents a supported Python application path using PySide6 or PyQt with
QML/Kirigami. PySide6 is the official Qt binding and works well for keeping UI
presentation in QML while placing application behaviour in testable Python.

## Decision

Use Python 3.12+, PySide6, QML and Kirigami 6. Use the Python standard library
for CLI parsing and SQLite. Isolate Qt to GUI bridge/presentation modules.

Install PySide6 and Kirigami from the distribution during Arch/CachyOS
development so their Qt versions match. Packaging work must validate QML plugin
discovery explicitly.

## Consequences

- Fast MVP iteration and an approachable contributor path.
- Native Plasma theming, icons and Kirigami interaction patterns.
- One Python core can serve GUI and CLI.
- Packaging is more involved than a pure script because Qt/Kirigami modules
  must align.
- CPU-heavy hashing/extraction must run in bounded workers and avoid blocking
  the Qt event loop.
- Domain/application ports must remain clean enough to replace an adapter or
  performance-sensitive component later without a rewrite.

## Revisit triggers

Reconsider only with profiling or packaging evidence: sustained performance
failures in a bounded component, missing required native APIs, or an
unmaintainable distribution story. Preference alone is not sufficient.
