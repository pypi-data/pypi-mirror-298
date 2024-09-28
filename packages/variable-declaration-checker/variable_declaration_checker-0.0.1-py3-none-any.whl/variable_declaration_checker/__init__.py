import astroid

import pylint.checkers
import pylint.lint


class VariableDeclarationChecker(pylint.checkers.BaseChecker):
    name = "variable-declaration-checker"
    msgs = {
        "W0001": ("Declare the variable.",
                  "un-declared-variable",
                  "Add a type annotation for the variable at the first time it appears."),
        "W0002": ("Rename the variable.",
                  "re-declared-variable",
                  "The variable has been used before. Remove the type annotation here or rename it.")
    }

    def check_locals(self, locals_dictionary: dict[str, list[astroid.nodes.NodeNG]]):
        for locals_ in locals_dictionary.values():
            locals_iterator = iter(locals_)

            current = next(locals_iterator)
            if (
                    isinstance(current, astroid.nodes.AssignName) and
                    (not isinstance(current.parent, astroid.nodes.AnnAssign)) and
                    (not isinstance(current.parent, astroid.nodes.Arguments)) and
                    (not isinstance(current.parent, astroid.nodes.TypeAlias))
            ):
                self.add_message("un-declared-variable", node=current)

            for current in locals_iterator:
                if (
                        isinstance(current, astroid.nodes.AssignName) and
                        isinstance(current.parent, astroid.nodes.AnnAssign)
                ):
                    self.add_message("re-declared-variable", node=current)

    def visit_functiondef(self, node: astroid.nodes.FunctionDef):
        self.check_locals(node.locals)

    def visit_module(self, node: astroid.nodes.Module):
        self.check_locals(node.locals)

    def visit_classdef(self, node: astroid.nodes.ClassDef):
        self.check_locals(node.locals)

def register(linter: pylint.lint.PyLinter) -> None:
    linter.register_checker(VariableDeclarationChecker(linter))
