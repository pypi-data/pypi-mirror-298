from __future__ import annotations

import ast
from dataclasses import dataclass

from .base import Rule

MESSAGE = "EC404: Use generator comprehension instead of list comprehension in for loop declaration."


@dataclass(frozen=True)
class EC404(Rule):
    """Flake8 rule to check for list comprehensions inside for loops."""

    def visit_For(self, node: ast.For):
        """Check for list comprehensions in the 'for' loop declaration."""
        match node.iter:
            # Check if the iterable (node.iter) of the for loop is a list comprehension
            case ast.ListComp():
                self.report(node.iter, MESSAGE)
            # Check for function calls like zip, filter, and enumerate in the iterable
            case ast.Call():
                self.visit_Call(node.iter)

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        """Check function call arguments for list comprehensions."""
        function_name = self.get_function_name(node)

        # Check if the function is one of the problematic functions (e.g., zip, filter, enumerate)
        if function_name not in {"zip", "filter", "enumerate"}:
            return

        for arg in node.args:
            match arg:
                case ast.ListComp():
                    self.report(arg, MESSAGE)
                case ast.Call():
                    self.visit_Call(arg)

    def get_function_name(self, node: ast.Call) -> str:
        """Helper method to extract the function name from a Call node."""
        match node.func:
            case ast.Name(id=name):
                return name
            case ast.Attribute(attr=name):
                return name
            case _:
                return ""
