import ast
import importlib.util
import sys
from enum import Enum, unique
from pathlib import Path

from src import constants
from src.models import *
from src.rules.rules_container import RulesContainer
from src.utils import ast_utils

ast_rules = RulesContainer()
# @ast_rules.rule
# def whitespaces_in_expr_in_stmt(code: str) -> list[Violation]:
#     pass


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

    try:
        spec = importlib.util.find_spec(import_name)
    except:
        spec = None

    if spec:
        module_path = Path(spec.origin).resolve()

        if "site-packages" in str(module_path) or "dist-packages" in str(
            module_path
        ):
            return ImportType.THIRD_PARTY

        else:
            return ImportType.PROJECT

    else:
        return ImportType.NOT_FOUND


@ast_rules.rule(ast.Module)
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
            continue

        if last_import_type.value > import_type.value:
            imports_violation.append(InvalidImportsOrder(imp.lineno))

        last_import_type = import_type
    return imports_violation


@ast_rules.rule(ast.Import)
def import_on_one_line(node: ast.Import) -> Violation | None:
    if len(node.names) > 1:
        return ManyImportOnOneLine(node.lineno)


@ast_rules.rule(ast.Import, ast.ImportFrom)
def import_not_at_top_of_file(
    node: ast.Import | ast.ImportFrom,
) -> Violation | None:
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


@ast_rules.rule(ast.ImportFrom)
def relative_import_from(node: ast.ImportFrom) -> Violation | None:
    if node.level > 0:
        return RelativeImports(node.lineno)


@ast_rules.rule(ast.Module, ignore_comments_and_decorators=True)
def top_level_must_be_surrounded(
    module: ast.FunctionDef, source: str
) -> list[Violation] | None:

    violations = []

    nodes_must_be_surrounded: list[int] = []
    for index, child in enumerate(ast.iter_child_nodes(module)):
        if isinstance(child, (ast.FunctionDef, ast.ClassDef)):
            nodes_must_be_surrounded.append(index)

    for node_index in nodes_must_be_surrounded:
        node = module.body[node_index]
        # If node at top
        if node_index == 0:

            continue

        # If node at middle
        if (
            node.lineno
            - ast_utils.get_block_end_lineno(module.body[node_index - 1])
            != constants.TOP_LEVEL_DEFS_TAB + 1
        ):
            violations.append(
                TopLevelFuncAndClassDefNotSurrounded(node.lineno)
            )
            continue

        # If node at end
        if node_index == len(module.body) - 1:
            continue

        node_end_lineno = ast_utils.get_block_end_lineno(node)
        next_node_lineno = module.body[node_index + 1].lineno

        if (
            module.body[node_index + 1] not in nodes_must_be_surrounded
            and next_node_lineno - node_end_lineno
            != constants.TOP_LEVEL_DEFS_TAB + 1
        ):
            violations.append(
                TopLevelFuncAndClassDefNotSurrounded(next_node_lineno)
            )

    return violations
