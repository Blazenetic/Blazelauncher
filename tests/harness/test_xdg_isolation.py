"""Prove the XDG isolation fixture does what the safety rules assume.

Every other test in this repository trusts that it cannot reach the
contributor's real home directory. That assumption is worth checking directly:
the failure mode is a rewritten application menu, not a red test.
"""

from __future__ import annotations

import os
from pathlib import Path

from tests.conftest import XdgRoots

XDG_VARIABLES = (
    "XDG_CONFIG_HOME",
    "XDG_DATA_HOME",
    "XDG_STATE_HOME",
    "XDG_CACHE_HOME",
)


def test_every_xdg_variable_points_inside_the_temporary_tree(
    xdg: XdgRoots, tmp_path: Path
) -> None:
    for name in XDG_VARIABLES:
        value = os.environ.get(name)
        assert value is not None, f"{name} is not set"
        assert Path(value).is_relative_to(tmp_path), f"{name} escaped to {value}"


def test_home_is_redirected(xdg: XdgRoots, tmp_path: Path) -> None:
    assert Path(os.environ["HOME"]).is_relative_to(tmp_path)
    assert xdg.home.is_dir()


def test_expanduser_follows_the_redirected_home(xdg: XdgRoots) -> None:
    # Anything resolving ~ must land in the temporary tree, including code that
    # bypasses the XDG resolver by accident.
    assert Path("~").expanduser() == xdg.home


def test_the_directories_exist_and_are_writable(xdg: XdgRoots) -> None:
    for path in (xdg.config, xdg.data, xdg.state, xdg.cache):
        assert path.is_dir()
        probe = path / "probe"
        probe.write_text("ok", encoding="utf-8")
        assert probe.read_text(encoding="utf-8") == "ok"


def test_the_application_menu_starts_empty(xdg: XdgRoots) -> None:
    # A test that expects to find launchers must create them first; discovering
    # the contributor's own entries here would mean isolation had failed.
    assert not xdg.applications.exists() or not list(xdg.applications.iterdir())


def test_isolation_is_fresh_for_each_test(xdg: XdgRoots) -> None:
    marker = xdg.config / "left-behind"
    assert not marker.exists()
    marker.write_text("", encoding="utf-8")
