import ast
import functools
import inspect
from collections import defaultdict
from typing import Type, Iterable

from models import Violation
from src.types import FileRule, AstRule, AnyAstType


class Scaner:

    def __init__(self):
        self._file_rules: list[FileRule] = []
        self._ast_rules: defaultdict[Type[ast.AST], list[AstRule]] = defaultdict(list)


    def scan(self, code: str) -> list[Violation]:
        violations: list[Violation] = []

        file_violations = self._scan_raw_file(code)
        ast_violations = self._scan_ast(code)

        if file_violations:
            violations.extend(file_violations)

        if ast_violations:
            violations.extend(ast_violations)

        return violations

    def _scan_raw_file(self, code: str) -> list[Violation]:
        violations: list[Violation] = []

        for file_rule in self._file_rules:
            rule_violations = file_rule(code)
            if rule_violations:
                violations.extend(rule_violations)

        return violations

    def _scan_ast(self, code: str) -> list[Violation]:
        violations: list[Violation] = []

        tree = ast.parse(code)

        violations = self._scan_node(tree, code)

        return violations

    def _scan_node(self, node: ast.AST, code: str) -> list[Violation]:
        node_violations = []

        node_type = node.__class__
        rule_list = self._ast_rules[node_type]

        # Add parent classes
        for p in node.__class__.__bases__:

            rule_list.extend(self._ast_rules[p])



        # Get current node violations
        if rule_list:
            if rule_list:
                for rule in rule_list:
                    args = inspect.getfullargspec(rule).args
                    # print(args)
                    if "code" in args:

                        violations = rule(node, code)
                    else:
                        violations = rule(node)

                    if not isinstance(violations, Iterable) and violations is not None:
                        violations = [violations]

                    if violations:
                        node_violations.extend(violations)

        # Get children node violations
        for children in ast.iter_child_nodes(node):
            children.parent = node
            node_violations.extend(self._scan_node(children, code))

        return node_violations


    def add_file_rule(self, rule: FileRule) -> None:
        self._file_rules.append(rule)

    def add_ast_rule(self, ast_type: Type[ast.AST], rule: AstRule) -> None:
        self._ast_rules[ast_type].append(rule)


    def file_rule(self, func: FileRule):
        self.add_file_rule(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    def ast_rule(self, *ast_types: AnyAstType):
        def actual_decorator(func: AstRule):
            for ast_type in ast_types:
                self.add_ast_rule(ast_type, func)
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return actual_decorator

