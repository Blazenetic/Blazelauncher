"""Shared test fixtures.

The most important thing here is XDG isolation. Blazelauncher writes desktop
entries, manages a cabinet of binaries and stores state in a database — a test
that escapes into a contributor's real home directory can rewrite their
application menu. Isolation is therefore automatic and applies to every test,
rather than being something an individual test has to remember to ask for.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pytest

#: The environment as it was before pytest touched anything. Used to prove the
#: suite never points at the real user's directories.
_REAL_ENVIRONMENT = {
    name: os.environ.get(name)
    for name in (
        "HOME",
        "XDG_CONFIG_HOME",
        "XDG_DATA_HOME",
        "XDG_STATE_HOME",
        "XDG_CACHE_HOME",
    )
}


@dataclass(frozen=True)
class XdgRoots:
    """The temporary XDG directories a test may write to."""

    home: Path
    config: Path
    data: Path
    state: Path
    cache: Path

    @property
    def applications(self) -> Path:
        """Where user-level desktop entries are installed."""
        return self.data / "applications"


@pytest.fixture(autouse=True)
def xdg(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[XdgRoots]:
    """Redirect HOME and every XDG base directory into a temporary tree.

    Autouse: opting in per test would eventually be forgotten, and the failure
    mode is damage to the contributor's desktop rather than a red test.
    """
    home = tmp_path / "home"
    roots = XdgRoots(
        home=home,
        config=home / ".config",
        data=home / ".local" / "share",
        state=home / ".local" / "state",
        cache=home / ".cache",
    )

    for path in (roots.home, roots.config, roots.data, roots.state, roots.cache):
        path.mkdir(parents=True, exist_ok=True)

    monkeypatch.setenv("HOME", str(roots.home))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(roots.config))
    monkeypatch.setenv("XDG_DATA_HOME", str(roots.data))
    monkeypatch.setenv("XDG_STATE_HOME", str(roots.state))
    monkeypatch.setenv("XDG_CACHE_HOME", str(roots.cache))

    # Runtime directories are session-scoped and must not be inherited either.
    monkeypatch.delenv("XDG_RUNTIME_DIR", raising=False)

    yield roots


@pytest.fixture(autouse=True)
def _no_real_home_leakage(xdg: XdgRoots) -> Iterator[None]:
    """Fail a test that re-points an XDG variable at the real environment."""
    yield

    for name, original in _REAL_ENVIRONMENT.items():
        if original is None:
            continue
        current = os.environ.get(name)
        if current == original:
            pytest.fail(
                f"{name} was restored to the real user value ({original!r}) "
                "during the test. Tests must stay inside the temporary XDG "
                "roots provided by the `xdg` fixture."
            )


@pytest.fixture(scope="session")
def repository_root() -> Path:
    """The checkout root, for tests that inspect the repository itself."""
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def source_root(repository_root: Path) -> Path:
    """The package source tree, skipping the test when it does not exist yet."""
    source = repository_root / "src" / "blazelauncher"
    if not source.is_dir():
        pytest.skip("src/blazelauncher does not exist yet")
    return source
