"""Static checks for the boundaries described in AGENTS.md.

The rules live in importable functions rather than inside the tests so that
they can be exercised against synthetic sources. A guard that has never seen a
violation is not a guard, and while ``src/blazelauncher`` is still being built
out the real tree would give these functions nothing to say.

The analysis is deliberately syntactic: it parses files and never imports them,
so running the checks cannot execute application code.
"""

from __future__ import annotations

import ast
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

#: Layers that must stay usable without a Qt runtime.
QT_FREE_LAYERS = frozenset({"domain", "application", "providers"})

#: Qt bindings in any spelling.
QT_PACKAGES = frozenset({"PySide6", "PySide2", "PyQt5", "PyQt6", "shiboken6"})

#: The domain models behaviour. Anything reaching the outside world belongs in
#: infrastructure or adapters, behind a port.
DOMAIN_FORBIDDEN_IMPORTS = QT_PACKAGES | {
    "subprocess",
    "sqlite3",
    "socket",
    "http",
    "urllib",
    "requests",
    "httpx",
}

#: Processes are launched in one place so that structured argv, timeouts,
#: cancellation and output limits hold everywhere.
PROCESS_LAYERS = frozenset({"infrastructure", "adapters"})

#: Functions that hand a string to a shell.
SHELL_FUNCTIONS = frozenset({"system", "popen", "getoutput", "getstatusoutput"})

#: Literal user paths bypass the XDG resolver, ignore XDG_* overrides and
#: escape the temporary roots the test suite depends on.
HARDCODED_PATH_FRAGMENTS = ("~/.local", "~/.config", "~/.cache", "/home/")

#: Modules allowed to name user directories, because resolving them is their
#: entire job.
PATH_RESOLVER_MODULES = ("infrastructure.xdg", "infrastructure.paths")


@dataclass(frozen=True)
class SourceFile:
    """One parsed Python file inside a package tree."""

    path: Path
    tree: ast.Module
    #: Dotted path relative to the package root, e.g. ``domain.action``.
    module: str

    @property
    def layer(self) -> str:
        """The top-level layer, e.g. ``domain``."""
        return self.module.split(".")[0]

    def imported_roots(self) -> Iterator[tuple[str, int]]:
        """Yield ``(top-level imported package, line number)`` pairs."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    yield alias.name.split(".")[0], node.lineno
            # A relative import stays inside the package by definition.
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                yield node.module.split(".")[0], node.lineno


def parse_sources(root: Path) -> list[SourceFile]:
    """Parse every Python file beneath ``root``."""
    sources: list[SourceFile] = []

    for path in sorted(root.rglob("*.py")):
        relative = path.relative_to(root)
        module = ".".join(relative.with_suffix("").parts).removesuffix(".__init__")
        sources.append(
            SourceFile(
                path=path,
                tree=ast.parse(path.read_text(encoding="utf-8"), filename=str(path)),
                module=module or "__init__",
            )
        )

    return sources


def _imports_in(
    sources: list[SourceFile], layers: frozenset[str], forbidden: frozenset[str]
) -> list[str]:
    return [
        f"{source.path}:{line} imports {imported}"
        for source in sources
        if source.layer in layers
        for imported, line in source.imported_roots()
        if imported in forbidden
    ]


def qt_imports_in_qt_free_layers(sources: list[SourceFile]) -> list[str]:
    """Qt reaching a layer that has to work without it."""
    return _imports_in(sources, QT_FREE_LAYERS, QT_PACKAGES)


def io_imports_in_domain(sources: list[SourceFile]) -> list[str]:
    """Processes, databases or network access inside the domain."""
    return _imports_in(sources, frozenset({"domain"}), DOMAIN_FORBIDDEN_IMPORTS)


def subprocess_outside_process_layers(sources: list[SourceFile]) -> list[str]:
    """Process launching outside infrastructure and adapters."""
    return [
        f"{source.path}:{line} imports subprocess"
        for source in sources
        if source.layer not in PROCESS_LAYERS
        for imported, line in source.imported_roots()
        if imported == "subprocess"
    ]


def shell_execution(sources: list[SourceFile]) -> list[str]:
    """``shell=`` anything but ``False``, or a call that shells out implicitly."""
    violations: list[str] = []

    for source in sources:
        for node in ast.walk(source.tree):
            if not isinstance(node, ast.Call):
                continue

            for keyword in node.keywords:
                if keyword.arg != "shell":
                    continue
                literal_false = (
                    isinstance(keyword.value, ast.Constant)
                    and keyword.value.value is False
                )
                if not literal_false:
                    violations.append(
                        f"{source.path}:{node.lineno} passes shell= other than False"
                    )

            func = node.func
            if isinstance(func, ast.Attribute) and func.attr in SHELL_FUNCTIONS:
                violations.append(f"{source.path}:{node.lineno} calls {func.attr}()")

    return violations


def hardcoded_user_paths(sources: list[SourceFile]) -> list[str]:
    """String literals naming a user directory outside the XDG resolver."""
    violations: list[str] = []

    for source in sources:
        if source.module.startswith(PATH_RESOLVER_MODULES):
            continue
        for node in ast.walk(source.tree):
            if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                continue
            for fragment in HARDCODED_PATH_FRAGMENTS:
                if fragment in node.value:
                    violations.append(
                        f"{source.path}:{node.lineno} hardcodes {fragment!r}"
                    )

    return violations
