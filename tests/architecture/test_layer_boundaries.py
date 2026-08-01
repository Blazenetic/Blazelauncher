"""The dependency direction is a product decision, so it is a test.

``AGENTS.md`` states that dependencies point inward and that domain code must
not import Qt. import-linter checks the same rules once the package imports
cleanly; these tests work earlier, run everywhere and give a failure message
that names the file and the line.
"""

from __future__ import annotations

from tests.architecture import rules
from tests.architecture.rules import SourceFile


def test_qt_free_layers_do_not_import_qt(python_sources: list[SourceFile]) -> None:
    violations = rules.qt_imports_in_qt_free_layers(python_sources)

    assert not violations, (
        "Qt must not reach the domain, application or provider layers — "
        "expose it through an adapter port instead:\n  " + "\n  ".join(violations)
    )


def test_domain_has_no_io_imports(python_sources: list[SourceFile]) -> None:
    violations = rules.io_imports_in_domain(python_sources)

    assert not violations, (
        "The domain must stay free of Qt, processes, databases and network "
        "access:\n  " + "\n  ".join(violations)
    )


def test_subprocess_use_is_confined_to_the_process_layers(
    python_sources: list[SourceFile],
) -> None:
    violations = rules.subprocess_outside_process_layers(python_sources)

    assert not violations, (
        "Subprocess handling belongs to the shared runner in infrastructure or "
        "adapters so that argv, timeouts, cancellation and output limits stay "
        "in one place:\n  " + "\n  ".join(violations)
    )
