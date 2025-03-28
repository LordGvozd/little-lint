import ast
import functools
import sys
import importlib.util
from collections import defaultdict
from collections.abc import Callable, Sequence
from enum import unique, Enum
import inspect
from pathlib import Path
from pprint import pprint
from typing import TypeAlias, ClassVar, Final, Type, Iterable

import astunparse

MAX_LINE_LENGTH: Final[int] = 79

def iter_node_children(node: ast.AST):
    for name, field in ast.iter_fields(node):
        if isinstance(field, ast.AST):
            yield field
        if isinstance(field, list):
            for item in field:
                if isinstance(item, ast.AST):
                    yield item


@unique
class ViolationType(Enum):
    ERROR = 1
    WARNING = 2
    NOT_RECOMMENDER = 3

class Violation:
    text: str = ""
    line: int
    type: ViolationType

    def __init__(self, line: int) -> None:
        self.line = line

    def __repr__(self):
        return f"{self.__class__.__name__} violation in line {self.line}"


class MaxLineLength(Violation):
    text = f"Max length should be {MAX_LINE_LENGTH}"
    type = ViolationType.WARNING

class UsingTabsToTabulation(Violation):
    type = ViolationType.WARNING

class InvalidImportsOrder(Violation):
    type = ViolationType.WARNING

class ManyImportOnOneLine(Violation):
    type = ViolationType.ERROR
    text = "Imports should usually be on separate lines"

class ImportsNotAtTop(Violation):
    type = ViolationType.WARNING
    text = (f"Imports are always put at the top of the file,"
            f" just after any module comments and docstrings,"
            f" and before module globals and constants")

class RelativeImports(Violation):
    type = ViolationType.NOT_RECOMMENDER
    text = ("Absolute imports are recommended,"
            " as they are usually more readable and tend to be better behaved (or at least give better error messages)"
            " if the import system is incorrectly configured (such as when a directory inside a package ends up on sys.path)")



class ModuleNotFound(Violation):
    type = ViolationType.ERROR
    text = "Module not found!"

FileRule: TypeAlias = Callable[[str], list[Violation] | None]
AstRule: TypeAlias = Callable[[ast.AST], list[Violation] | None]
AnyAstType: TypeAlias = type[ast.AST] | type[ast.mod] | type[ast.Module] | type[ast.Interactive] | type[ast.Expression] | type[ast.FunctionType] | type[ast.Suite] | type[ast.stmt] | type[ast.FunctionDef] | type[ast.AsyncFunctionDef] | type[ast.ClassDef] | type[ast.Return] | type[ast.Delete] | type[ast.Assign] | type[ast.TypeAlias] | type[ast.AugAssign] | type[ast.AnnAssign] | type[ast.For] | type[ast.AsyncFor] | type[ast.While] | type[ast.If] | type[ast.With] | type[ast.AsyncWith] | type[ast.Match] | type[ast.Raise] | type[ast.Try] | type[ast.TryStar] | type[ast.Assert] | type[ast.Import] | type[ast.ImportFrom] | type[ast.Global] | type[ast.Nonlocal] | type[ast.Expr] | type[ast.Pass] | type[ast.Break] | type[ast.Continue] | type[ast.expr] | type[ast.BoolOp] | type[ast.NamedExpr] | type[ast.BinOp] | type[ast.UnaryOp] | type[ast.Lambda] | type[ast.IfExp] | type[ast.Dict] | type[ast.Set] | type[ast.ListComp] | type[ast.SetComp] | type[ast.DictComp] | type[ast.GeneratorExp] | type[ast.Await] | type[ast.Yield] | type[ast.YieldFrom] | type[ast.Compare] | type[ast.Call] | type[ast.FormattedValue] | type[ast.JoinedStr] | type[ast.Constant] | type[ast.Attribute] | type[ast.Subscript] | type[ast.Starred] | type[ast.Name] | type[ast.List] | type[ast.Tuple] | type[ast.Slice] | type[ast.expr_context] | type[ast.Load] | type[ast.Store] | type[ast.Del] | type[ast.AugLoad] | type[ast.AugStore] | type[ast.Param] | type[ast.boolop] | type[ast.And] | type[ast.Or] | type[ast.operator] | type[ast.Add] | type[ast.Sub] | type[ast.Mult] | type[ast.MatMult] | type[ast.Div] | type[ast.Mod] | type[ast.Pow] | type[ast.LShift] | type[ast.RShift] | type[ast.BitOr] | type[ast.BitXor] | type[ast.BitAnd] | type[ast.FloorDiv] | type[ast.unaryop] | type[ast.Invert] | type[ast.Not] | type[ast.UAdd] | type[ast.USub] | type[ast.cmpop] | type[ast.Eq] | type[ast.NotEq] | type[ast.Lt] | type[ast.LtE] | type[ast.Gt] | type[ast.GtE] | type[ast.Is] | type[ast.IsNot] | type[ast.In] | type[ast.NotIn] | type[ast.comprehension] | type[ast.excepthandler] | type[ast.ExceptHandler] | type[ast.arguments] | type[ast.arg] | type[ast.keyword] | type[ast.alias] | type[ast.withitem] | type[ast.match_case] | type[ast.pattern] | type[ast.MatchValue] | type[ast.MatchSingleton] | type[ast.MatchSequence] | type[ast.MatchMapping] | type[ast.MatchClass] | type[ast.MatchStar] | type[ast.MatchAs] | type[ast.MatchOr] | type[ast.type_ignore] | type[ast.TypeIgnore] | type[ast.type_param] | type[ast.TypeVar] | type[ast.ParamSpec] | type[ast.TypeVarTuple] | type[ast.slice] | type[ast.Index] | type[ast.ExtSlice]



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

scaner = Scaner()

@scaner.file_rule
def check_max_line_length(code: str) -> list[Violation]:
    result: list[Violation] = []

    code = code.replace("\t", "    ")
    lines = code.split("\n")

    for number, l in enumerate(lines):
        if l.startswith("#"):
           if len(l) <= 72:
               continue
        if len(l) > MAX_LINE_LENGTH:
            result.append(MaxLineLength(number + 1))

    return result

@scaner.file_rule
def check_tabs(code: str) -> list[Violation]:
    result: list[Violation] = []

    lines = code.split("\n")

    for number, l in enumerate(lines):
        if l.startswith("\t"):
            result.append(UsingTabsToTabulation(number + 1))
    return result


@scaner.ast_rule
def whitespaces_in_expr_in_stmt(code: str) -> list[Violation]:
    pass


@unique
class ImportType(Enum):
    # DO NOT CHANGE THIS ORDER
    NOT_FOUND = 0
    FUTURE = 1
    STDLIB = 2
    THIRD_PARTY = 3
    PROJECT = 4

def get_import_type(imp: ast.Import | ast.ImportFrom) -> ImportType:
    if isinstance(imp, ast.Import):
        import_name = imp.names[0].name
    else:
        import_name = imp.module

        if import_name == "__future__":
            return ImportType.FUTURE

    if import_name is None:
        return ImportType.PROJECT

    stdlib_names = sys.stdlib_module_names
    if import_name in stdlib_names:
        return ImportType.STDLIB

    spec = importlib.util.find_spec(import_name)

    if spec:
        module_path = Path(spec.origin).resolve()

        if "site-packages" in str(module_path) or "dist-packages" in str(module_path):
            return ImportType.THIRD_PARTY

        else:
            if str(module_path.parent) in sys.path:
                return ImportType.PROJECT
    else:
        return ImportType.NOT_FOUND

@scaner.ast_rule(ast.Module)
def right_order(node: ast.Module) -> list[Violation]:
    imports_violation = []

    all_imports = []

    for n in node.body:
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            all_imports.append(n)


    all_imports = sorted(all_imports, key=lambda i: i.lineno)

    # Sort imports
    last_import_type: ImportType = ImportType.NOT_FOUND
    for imp in all_imports:
        import_type = get_import_type(imp)

        if import_type == ImportType.NOT_FOUND:
            imports_violation.append(ModuleNotFound(imp.lineno))

        if last_import_type.value > import_type.value:
            imports_violation.append(InvalidImportsOrder(imp.lineno))

        last_import_type = import_type
    return imports_violation




@scaner.ast_rule(ast.Import)
def import_on_one_line(node: ast.Import) -> Violation:
    if len(node.names) > 1:
        return ManyImportOnOneLine(node.lineno)

@scaner.ast_rule(ast.Import, ast.ImportFrom)
def import_not_at_top_of_file(node: ast.Import | ast.ImportFrom) -> Violation | None:
    # Get root
    root = node
    while hasattr(root, "parent"):
        root = root.parent

    # ToDo: support docstrings

    import_lineno = node.lineno
    for n in root.body:
        if not isinstance(n, (ast.Import, ast.ImportFrom)):
            if n.lineno < import_lineno:
                return ImportsNotAtTop(import_lineno)

@scaner.ast_rule(ast.ImportFrom)
def relative_import_from(node: ast.ImportFrom) -> Violation | None:
    if node.level > 0:
        return RelativeImports(node.lineno)

@scaner.ast_rule(ast.stmt)
def whitespace_in_stmt(node: ast.stmt, code) -> Violation | None:
    source = ast.get_source_segment(code, node)

    # print(source)


    # for line in source.split("\n"):
    #     print(line)
    #     if "( " in line:
    #         print('Kuk')


test_code = """

from sys import write

import sys


import time
import abc

import astunparse


def foo():
    print( "bar")

test =        1        


if test ==   2:
    pass
    
# very_long_string = "12345678910111213141516171819022122232425262728293031323334353637383940414243444546474849505152535455565758596061626364656667686970717273747576777879"

"""

pprint(scaner.scan(test_code))



