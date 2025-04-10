import ast
import re
from fileinput import lineno


def get_block_end_lineno(block_root: ast.AST) -> int:
    max_line_end = 0

    for node in ast.walk(block_root):
        if hasattr(node, "end_lineno"):
            node_end = node.end_lineno
        elif hasattr(node, "lineno"):
            node_end = node.lineno
        else:
            continue

        max_line_end = max(
            (
                max_line_end,
                node_end,
            )
        )

    return max_line_end


def remove_comments_from_ast(source: str) -> ast.AST:
    """Return ast without taking into account comments"""
    new_text = ""

    for line in source.split("\n"):
        line_starts_from_comment = False
        for c in line:
            if c in (" ", "\t"):
                continue

            elif c in ("#", "@"):
                line_starts_from_comment = True
                break
            else:
                break
        if line_starts_from_comment:
            continue
        new_text += f"{line}\n"

    tree = ast.parse(new_text)

    return tree


if __name__ == "__main__":

    source = r"""

# Comment, explaining that i cant write normal code
def foo():
    return "baz"
# Some

# f
print("Something")
# TEst

# com
class Point:
    ''' Class, contained point coordinates
        Really cool
        Used it


        blalbalba
    '''
    x = 1
    y = 2


point = Point()


    """

    print(source.count("\n"), end="|")
    source = re.sub(r"^\s*#.*$", "", source, flags=re.MULTILINE)

    print(source, "|", source.count("\n"), sep="")
