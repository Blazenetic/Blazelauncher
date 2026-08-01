"""Fixtures for the repository contract tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.architecture.rules import SourceFile, parse_sources


@pytest.fixture(scope="session")
def python_sources(source_root: Path) -> list[SourceFile]:
    """Every Python file in the package, parsed once for the whole session."""
    sources = parse_sources(source_root)
    if not sources:
        pytest.skip("no Python sources yet")
    return sources
