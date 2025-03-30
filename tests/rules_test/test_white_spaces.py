from src.models import LineBreakAfterBinOp
from src.rules.line_rules import break_line_after_bin_op

# Correct
break_before_bin_op = """
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)
"""

# Wrong
break_after_bin_op = """
income = (gross_wages +
          taxable_interest +
          (dividends - qualified_dividends) -
          ira_deduction -
          student_loan_interest)

"""


def test_break_line_after_bin_op() -> None:
    assert break_line_after_bin_op("+ 5", 1) is None
    assert str(break_line_after_bin_op("5 + ", 1)) == str(
        LineBreakAfterBinOp(1)
    )
