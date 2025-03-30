import re

from src import constants
from src.models import *
from src.rules.rules_container import RulesContainer

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


# @file_rules.rule
def use_4_spaces_for_level(code: str) -> Violation | None:
    """Checks, is every line if file use 4 spaces
    per indentation level
    """
    code = code.replace("\t", "    ")

    previous_tabs_count = 0
    for number, line in enumerate(code.split("\n")):
        leading_spaces_count = get_leading_spaces_count(line)
        if leading_spaces_count % 4 != 0:
            return Not4SpaceForIndentationLevel(number)

        if leading_spaces_count - previous_tabs_count > 4:
            return Not4SpaceForIndentationLevel(number)
