from __future__ import annotations

import ast
from dataclasses import dataclass

from .base import Rule

MESSAGE = "EC35: Avoid the use of try-except with a file open() in the try block."


@dataclass(frozen=True)
class EC35(Rule):
    """
    Flake8 rule to check for try-except blocks that contain open() calls.
    """

    def visit_Try(self, node):
        """
        Visit try-except blocks and check if open() is called inside.
        """
        for stmt in node.body:
            self.check_for_open_call(stmt)

        # Continue visiting nested nodes
        self.generic_visit(node)

    def check_for_open_call(self, node):
        """
        Check if the given node or its children contains a call to open().
        """
        match node:
            case ast.Call(func=ast.Name(id="open")):
                self.report(node, MESSAGE)
            case _:
                for child in ast.iter_child_nodes(node):
                    self.check_for_open_call(child)
