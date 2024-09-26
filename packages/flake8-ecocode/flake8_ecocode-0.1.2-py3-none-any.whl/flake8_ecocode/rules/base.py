from __future__ import annotations

import ast
from dataclasses import dataclass, field

from flake8_ecocode.types import FlakeError


@dataclass(frozen=True)
class Rule(ast.NodeVisitor):
    """Base class for visitors."""

    tree: ast.AST
    errors: list[FlakeError] = field(default_factory=list)

    def report(self, node: ast.AST, message: str):
        self.errors.append((node.lineno, node.col_offset, message, type(self)))  # type: ignore[attr-defined]
