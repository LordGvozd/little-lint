import ast
import inspect
from collections import defaultdict
from typing import Type, Iterable, Final

from src.models import Violation
from src.rules.rules_container import Rule
from src.types import FileRule, AstRule, AnyAstType, LineRule, AstChecker
from src.utils import ast_utils


def reparse_ast(source: str, tree: ast.AST) -> ast.AST:
    pass


class Scaner:

    AST_ALLOW_KWARGS: Final[list[str]] = ["ignore_comments_and_decorators"]

    def __init__(self):
        self._file_rules: list[Rule] = []
        self._ast_rules: defaultdict[Type[ast.AST], list[Rule]] = defaultdict(
            list
        )
        self._line_rules: list[Rule] = []

    def scan(
        self,
        code: str,
        include_only: (
            type[Violation] | tuple[type[Violation], ...] | None
        ) = None,
        *,
        exclude: type[Violation] | tuple[type[Violation], ...] | None = None,
    ) -> list[Violation]:
        violations: list[Violation] = []

        file_violations = self._scan_raw_file(code)
        line_violations = self._scan_lines(code)
        ast_violations = self._scan_ast(code)

        if file_violations:
            violations.extend(file_violations)

        if ast_violations:
            violations.extend(ast_violations)

        if line_violations:
            violations.extend(line_violations)

        if include_only:
            if not isinstance(include_only, tuple):  # Convert to tuple
                include_only = (include_only,)
            violations = [v for v in violations if type(v) in include_only]

        if exclude:
            if not isinstance(exclude, tuple):
                exclude = (exclude,)
            violations = [v for v in violations if type(v) not in exclude]

        return violations

    def _scan_raw_file(self, code: str) -> list[Violation]:
        violations: list[Violation] = []

        for file_rule in self._file_rules:
            rule_violations = file_rule.checker(code)
            if rule_violations:
                if not isinstance(rule_violations, Iterable):
                    violations.append(rule_violations)
                    continue

                violations.extend(rule_violations)

        return violations

    def _scan_lines(self, code: str) -> list[Violation]:
        violations: list[Violation] = []

        lines = code.split("\n")

        for number, line in enumerate(lines):
            line_violations = []
            for rule in self._line_rules:
                v = rule.checker(line, number + 1)
                if v:
                    line_violations.append(v)
            if line_violations:
                violations.extend(line_violations)
        return violations

    def _scan_ast(self, code: str) -> list[Violation]:
        violations: list[Violation] = []

        tree = ast.parse(code)

        violations = self._scan_node(tree, code)

        return violations

    def _scan_node(self, node: ast.AST, source: str) -> list[Violation]:
        node_violations = []

        node_type = node.__class__
        rule_list = self._ast_rules[node_type]

        # Add parent classes
        for p in node.__class__.__bases__:

            rule_list.extend(self._ast_rules[p])

        # Get current node violations
        if rule_list:
            node_to_scan = node
            for rule in rule_list:
                args = inspect.getfullargspec(rule.checker).args

                # If rule has some options (kwargs)
                for option_name, option_value in rule.kwargs.items():
                    if option_name not in self.AST_ALLOW_KWARGS:
                        raise ValueError(
                            f"Option (kwarg) {option_name} not exist!"
                        )
                    if (
                        option_name == "ignore_comments_and_decorators"
                        and option_value == True
                    ):
                        node_to_scan = ast_utils.remove_comments_from_ast(
                            source
                        )

                if len(args) == 2:
                    violations = rule.checker(node_to_scan, source)
                else:
                    violations = rule.checker(node_to_scan)

                if (
                    not isinstance(violations, Iterable)
                    and violations is not None
                ):
                    violations = [violations]

                if violations:
                    node_violations.extend(violations)

        # Get children node violations
        for children in ast.iter_child_nodes(node):
            children.parent = node
            node_violations.extend(self._scan_node(children, source))

        return node_violations

    def add_file_rule(self, rule: Rule) -> None:
        self._file_rules.append(rule)

    def add_ast_rule(self, ast_type: Type[ast.AST], rule: Rule) -> None:
        self._ast_rules[ast_type].append(rule)

    def add_line_rule(self, rule: Rule) -> None:
        self._line_rules.append(rule)
