import re

from src.models import Violation, LineBreakAfterBinOp
from src.rules.rules_container import RulesContainer

line_rules = RulesContainer()


@line_rules.rule
def break_line_after_bin_op(line: str, number: int) -> Violation | None:
    if re.match(r"\w+\s*\+\s*$", line):
        return LineBreakAfterBinOp(number)
