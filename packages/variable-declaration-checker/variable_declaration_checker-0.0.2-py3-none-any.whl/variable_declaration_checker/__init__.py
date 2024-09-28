import astroid

import pylint.checkers
import pylint.lint


class VariableDeclarationChecker(pylint.checkers.BaseChecker):
    name = "variable-declaration-checker"
    msgs = {
        "W5901": ("Declare the variable with type annotation.",
                  "un-declared-variable",
                  "It's the first time the variable appears, so here should be a type annotation."),
        "W5902": ("Rename the variable or remove the type annotation.",
                  "re-declared-variable",
                  "The variable has been used before, so here shouldn't be a type annotation."),
    }

    def check_locals(self, locals_dictionary: dict[str, list[astroid.nodes.NodeNG]]):
        for name, occurrences in locals_dictionary.items():
            if name == "_":
                return

            occurrence_iterator = iter(occurrences)
            occurrence = next(occurrence_iterator)

            if (
                    isinstance(occurrence, astroid.nodes.AssignName) and
                    (not isinstance(occurrence.parent, astroid.nodes.AnnAssign)) and
                    (not isinstance(occurrence.parent, astroid.nodes.Arguments)) and
                    (not isinstance(occurrence.parent, astroid.nodes.TypeAlias))
            ):
                self.add_message("un-declared-variable", node=occurrence)

            for occurrence in occurrence_iterator:
                if (
                        isinstance(occurrence.parent, astroid.nodes.AnnAssign)
                ):
                    self.add_message("re-declared-variable", node=occurrence)

    def visit_functiondef(self, node: astroid.nodes.FunctionDef):
        self.check_locals(node.locals)

    def visit_module(self, node: astroid.nodes.Module):
        self.check_locals(node.locals)

    def visit_classdef(self, node: astroid.nodes.ClassDef):
        self.check_locals(node.locals)

def register(linter: pylint.lint.PyLinter) -> None:
    linter.register_checker(VariableDeclarationChecker(linter))
