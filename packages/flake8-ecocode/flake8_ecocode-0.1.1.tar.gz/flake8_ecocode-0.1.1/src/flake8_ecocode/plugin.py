from __future__ import annotations

from collections.abc import Iterator

from .rules.ec_35 import EC35
from .rules.ec_404 import EC404
from .types import FlakeError

CHECKERS = [
    EC404,
    EC35,
]


class EcocodePlugin:
    """
    Plugin class for Flake8.
    """

    name = "flake8-ecocode"
    version = "0.1.0"

    def __init__(self, tree):
        self.tree = tree

    def run(self) -> Iterator[FlakeError]:
        for checker_class in CHECKERS:
            checker = checker_class(self.tree)
            checker.visit(self.tree)
            yield from checker.errors
