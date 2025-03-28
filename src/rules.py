import ast
import importlib.util
import sys
from pathlib import Path

from src import constants
from src.core import Scaner
from src.models import *

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
        if len(l) > constants.MAX_LINE_LENGTH:
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
