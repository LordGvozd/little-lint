import pytest

from src.rules import scanner

from src.models import CommentsMustStartWithSpace


CORRECT_1 = """
# Some comment
print("Hello World!")
"""

CORRECT_2 = """
print("Hello World!")  # Some comment
"""

NOT_A_COMMENT = """
var = "# Not a comment"
"""

INCORRECT_1 = """
#Some comment
print("Hello World!")
"""

INCORRECT_2 = """
#Some comment
print("Hello World!")  #Some comment
"""


@pytest.mark.parametrize(
    "code, v_count",
    (
        (CORRECT_1, 0),
        (CORRECT_2, 0),
        (NOT_A_COMMENT, 0),
        (INCORRECT_1, 1),
        (INCORRECT_2, 1)
    )
)
def test_comments_must_start_with_space(code: str, v_count: int) -> None:
    violations = scanner.scan(code, CommentsMustStartWithSpace)
    assert len(violations) == v_count
    