"""Prove the boundary checks actually detect the things they claim to.

The guards in ``rules.py`` run against ``src/blazelauncher``, which is mostly
empty while the project is being built out — so on their own they would pass
without ever having been exercised. These tests feed them known-good and
known-bad synthetic packages instead, and they keep working as real code
lands.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.architecture import rules


def write_package(root: Path, files: dict[str, str]) -> list[rules.SourceFile]:
    """Materialise a synthetic package tree and parse it."""
    for relative, body in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    return rules.parse_sources(root)


def test_layer_is_derived_from_the_path(tmp_path: Path) -> None:
    sources = write_package(
        tmp_path,
        {
            "domain/action.py": "VALUE = 1\n",
            "infrastructure/xdg/__init__.py": "",
        },
    )

    layers = {source.module: source.layer for source in sources}
    assert layers == {
        "domain.action": "domain",
        "infrastructure.xdg": "infrastructure",
    }


@pytest.mark.parametrize(
    ("relative", "body"),
    [
        ("domain/action.py", "from PySide6.QtCore import QObject\n"),
        ("application/search.py", "import PySide6\n"),
        ("providers/files.py", "import PyQt6\n"),
    ],
)
def test_qt_in_a_qt_free_layer_is_caught(
    tmp_path: Path, relative: str, body: str
) -> None:
    sources = write_package(tmp_path, {relative: body})
    assert rules.qt_imports_in_qt_free_layers(sources)


def test_qt_in_the_gui_layer_is_allowed(tmp_path: Path) -> None:
    sources = write_package(tmp_path, {"gui/bridge.py": "import PySide6\n"})
    assert not rules.qt_imports_in_qt_free_layers(sources)


def test_io_imports_in_the_domain_are_caught(tmp_path: Path) -> None:
    sources = write_package(
        tmp_path,
        {"domain/launcher.py": "import sqlite3\nimport subprocess\n"},
    )
    assert len(rules.io_imports_in_domain(sources)) == 2


def test_pure_domain_passes(tmp_path: Path) -> None:
    sources = write_package(
        tmp_path,
        {
            "domain/launcher.py": (
                "from dataclasses import dataclass\n"
                "from pathlib import Path\n\n\n"
                "@dataclass(frozen=True)\n"
                "class Launcher:\n"
                "    path: Path\n"
            )
        },
    )
    assert not rules.io_imports_in_domain(sources)
    assert not rules.qt_imports_in_qt_free_layers(sources)
    assert not rules.subprocess_outside_process_layers(sources)


def test_subprocess_is_allowed_in_infrastructure_only(tmp_path: Path) -> None:
    sources = write_package(
        tmp_path,
        {
            "infrastructure/processes.py": "import subprocess\n",
            "adapters/media.py": "import subprocess\n",
            "cli/main.py": "import subprocess\n",
        },
    )

    violations = rules.subprocess_outside_process_layers(sources)
    assert len(violations) == 1
    assert "cli/main.py" in violations[0]


@pytest.mark.parametrize(
    "body",
    [
        "import subprocess\nsubprocess.run(cmd, shell=True)\n",
        "import subprocess\nsubprocess.run(cmd, shell=use_shell)\n",
        "import os\nos.system(cmd)\n",
        "import subprocess\nsubprocess.getoutput(cmd)\n",
    ],
)
def test_shell_execution_is_caught(tmp_path: Path, body: str) -> None:
    sources = write_package(tmp_path, {"infrastructure/processes.py": body})
    assert rules.shell_execution(sources)


def test_explicit_shell_false_passes(tmp_path: Path) -> None:
    sources = write_package(
        tmp_path,
        {
            "infrastructure/processes.py": (
                "import subprocess\n"
                "subprocess.run(argv, shell=False, timeout=5, check=False)\n"
            )
        },
    )
    assert not rules.shell_execution(sources)


@pytest.mark.parametrize(
    "body",
    [
        'CONFIG = "~/.config/blazelauncher"\n',
        'DATA = "~/.local/share/blazelauncher"\n',
        'CABINET = "/home/example/Applications"\n',
    ],
)
def test_hardcoded_user_paths_are_caught(tmp_path: Path, body: str) -> None:
    sources = write_package(tmp_path, {"application/cabinet.py": body})
    assert rules.hardcoded_user_paths(sources)


def test_the_xdg_resolver_may_name_user_directories(tmp_path: Path) -> None:
    sources = write_package(
        tmp_path,
        {"infrastructure/xdg/resolver.py": 'FALLBACK_CONFIG = "~/.config"\n'},
    )
    assert not rules.hardcoded_user_paths(sources)


def test_environment_lookups_pass(tmp_path: Path) -> None:
    sources = write_package(
        tmp_path,
        {
            "infrastructure/xdg/resolver.py": (
                "import os\n\n\n"
                "def config_home() -> str:\n"
                '    return os.environ["XDG_CONFIG_HOME"]\n'
            )
        },
    )
    assert not rules.hardcoded_user_paths(sources)
