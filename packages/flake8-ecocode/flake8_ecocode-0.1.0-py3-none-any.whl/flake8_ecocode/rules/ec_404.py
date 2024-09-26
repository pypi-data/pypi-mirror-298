import ast

MESSAGE = "EC404: Use generator comprehension instead of list comprehension in for loop declaration."


class EC404(ast.NodeVisitor):
    """Flake8 plugin to check for list comprehensions inside for loops."""

    def __init__(self, tree):
        self.tree = tree
        self.errors = []

    def visit_For(self, node: ast.For):
        """Check for list comprehensions in the 'for' loop declaration."""
        # Check if the iterable (node.iter) of the for loop is a list comprehension
        if isinstance(node.iter, ast.ListComp):
            self.errors.append((node.lineno, node.col_offset, MESSAGE, type(self)))

        # Check for function calls like zip, filter, and enumerate in the iterable
        elif isinstance(node.iter, ast.Call):
            self.visit_Call(node.iter)

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        """Check function call arguments for list comprehensions."""
        function_name = self.get_function_name(node)

        # Check if the function is one of the problematic functions (e.g., zip, filter, enumerate)
        if function_name in {"zip", "filter", "enumerate"}:
            for arg in node.args:
                if isinstance(arg, ast.ListComp):
                    self.errors.append((arg.lineno, arg.col_offset, MESSAGE))
                elif isinstance(arg, ast.Call):
                    self.visit_Call(arg)
                # Alternative using match statement (Python 3.10+)
                # match arg:
                #     case ast.ListComp():
                #         self.errors.append((arg.lineno, arg.col_offset, MESSAGE))
                #     case ast.Call():
                #         self.visit_Call(arg)

    def get_function_name(self, node: ast.Call) -> str:
        """Helper method to extract the function name from a Call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return ""
