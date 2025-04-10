import re
import tokenize
from io import BytesIO
from re import fullmatch

from src import constants
from src.models import *
from src.rules.rules_container import RulesContainer
from src.types import FileRule

file_rules = RulesContainer()


@file_rules.rule
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


@file_rules.rule
def check_tabs(code: str) -> list[Violation]:
    result: list[Violation] = []

    lines = code.split("\n")

    for number, l in enumerate(lines):
        if l.startswith("\t"):
            result.append(UsingTabsToTabulation(number + 1))
    return result


@file_rules.rule
def blank_line_at_end(code: str) -> Violation | None:
    last_line = code.split("\n")[-1]
    if re.findall(r"\S", last_line):
        return NoBlankLineAtEnd(len(code.split("\n")))


@file_rules.rule
def get_leading_spaces_count(source: str) -> int:
    count = 0
    for char in source:
        if char == " ":
            count += 1
        else:
            break
    return count


@file_rules.rule
def use_4_spaces_for_level(code: str) -> list[Violation] | None | Violation:
    """Checks, is every line if file use 4 spaces
    per indentation level
    """
    violations = []
    # ToDo: exclude docstrings and comments
    code = code.replace("\t", "    ")

    previous_tabs_count = 0
    open_bracket_count = 0
    open_bracket_level = []
    open_docstring = False

    for number, line in enumerate(code.split("\n")):
        number += 1

        leading_spaces_count = get_leading_spaces_count(line)
        if open_bracket_count > 0:
            if not line:
                pass
            elif re.findall(r"^\s*\).*", line):
                pass
            elif open_bracket_level[-1] + 4 == leading_spaces_count:
                pass
            else:
                violations.append(Not4SpaceForIndentationLevel(number))

        count_before = open_bracket_count

        open_string = False

        if line.count("'''") == 1 or line.count('"""') == 1:
            open_docstring = not open_string

        for cn, c in enumerate(line):
            if c in ("'", '"'):
                open_string = not open_string

            if open_string or open_docstring:
                continue
            if c == "(":
                open_bracket_count += 1
                open_bracket_level.append(leading_spaces_count)
            if c == ")":
                open_bracket_count -= 1
                del open_bracket_level[-1]
        if count_before < open_bracket_count:
            if not re.findall(r"\(\s*$", line):
                violations.append(Not4SpaceForIndentationLevel(number))
        if count_before > open_bracket_count:
            if not re.fullmatch(r"^\s*\).*", line):
                violations.append(Not4SpaceForIndentationLevel(number))

    return violations


# @file_rules.rule
def top_level_must_be_surrounded(code: str) -> list[Violation] | None:
    code_buffer = BytesIO(code.encode())

    must_be_surrounded = []

    indent_level = 0

    for token in tokenize.tokenize(code_buffer.readline):
        if token.type == tokenize.INDENT:
            indent_level += 1
        if token.type == tokenize.DEDENT:
            indent_level -= 1

        if token.type == tokenize.NAME:
            if token.string in ("class", "def"):
                pass
