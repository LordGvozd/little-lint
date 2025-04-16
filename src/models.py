from enum import unique, Enum

from src.constants import MAX_LINE_LENGTH


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
    text = "Spaces are the preferred indentation method"


class InvalidImportsOrder(Violation):
    type = ViolationType.WARNING
    text = """Imports should be grouped in the following order:
    1) Standard library imports.
    2) Related third party imports.
    3) Local application/library specific imports."""


class ManyImportOnOneLine(Violation):
    type = ViolationType.ERROR
    text = "Imports should usually be on separate lines"


class ImportsNotAtTop(Violation):
    type = ViolationType.WARNING
    text = (
        f"Imports are always put at the top of the file,"
        f" just after any module comments and docstrings,"
        f" and before module globals and constants"
    )


class RelativeImports(Violation):
    type = ViolationType.NOT_RECOMMENDER
    text = (
        "Absolute imports are recommended,"
        " as they are usually more readable and tend"
        " to be better behaved (or at least give better error messages)"
        " if the import system is"
        " incorrectly configured"
        " (such as when a directory inside a package ends up on sys.path)"
    )


class ModuleNotFound(Violation):
    type = ViolationType.ERROR
    text = "Module not found!"


class LineBreakAfterBinOp(Violation):
    type = ViolationType.WARNING
    text = (
        "In Python code, it is permissible to break before"
        " or after a binary operator,"
        " as long as the convention is consistent locally."
        " For new code Knuth’s style is suggested."
    )


class NoBlankLineAtEnd(Violation):
    type = ViolationType.ERROR
    text = "You should put blank line to end of file."


class Not4SpaceForIndentationLevel(Violation):
    type = ViolationType.ERROR
    text = "Use 4 spaces per indentation level."


class CommentsMustStartWithSpace(Violation):
    type = ViolationType.WARNING
    text = """Comments must start with space character.
    Correct:
    # Example comment
    
    Incorrect:
    #Example comment"""
   
  
class TopLevelFuncAndClassDefNotSurrounded(Violation):
    type = ViolationType.WARNING
    text = (
        "Surround top-level function"
        " and class definitions with two blank lines."
    )
