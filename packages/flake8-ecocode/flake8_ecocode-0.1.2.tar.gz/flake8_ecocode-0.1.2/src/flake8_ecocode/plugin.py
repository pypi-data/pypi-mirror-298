from __future__ import annotations

import ast
from collections.abc import Iterator
from dataclasses import dataclass

from .rules.base import Rule
from .rules.ec_35 import EC35
from .rules.ec_404 import EC404
from .types import FlakeError

CHECKERS: list[type[Rule]] = [
    EC404,
    EC35,
]


@dataclass(frozen=True)
class EcocodePlugin:
    """
    Plugin class for Flake8.
    """
    tree: ast.AST

    name = "flake8-ecocode"
    version = "0.1.0"

    def run(self) -> Iterator[FlakeError]:
        for checker_class in CHECKERS:
            checker = checker_class(self.tree)
            checker.visit(self.tree)
            yield from checker.errors
