"""Safety rules from AGENTS.md that can be checked mechanically.

Ruff catches most of this through its bandit rules. These tests exist because
the rules are product boundaries rather than style preferences: the failure
should read like a design objection, and it should survive someone relaxing a
Ruff rule.
"""

from __future__ import annotations

from tests.architecture import rules
from tests.architecture.rules import SourceFile


def test_no_shell_execution(python_sources: list[SourceFile]) -> None:
    violations = rules.shell_execution(python_sources)

    assert not violations, (
        "Commands are structured argv executed with shell=False. An expert "
        "shell mode, if it ever exists, needs its own ADR and a user-visible "
        "marker:\n  " + "\n  ".join(violations)
    )


def test_no_hardcoded_user_directories(python_sources: list[SourceFile]) -> None:
    violations = rules.hardcoded_user_paths(python_sources)

    assert not violations, (
        "Resolve user directories through the XDG resolver. Hardcoded paths "
        "ignore XDG_* overrides and escape the temporary roots the tests rely "
        "on:\n  " + "\n  ".join(violations)
    )
