import pytest

from src import models
from src.rules import scanner

correct_file = """

def some():
    print('Hello world!')

"""

correct_file_with_spaces = """

def some():
    print('Hello world!')
             """

incorrect_file = """

def some():
    print('Hello world!')"""


@pytest.mark.parametrize("code", (correct_file, correct_file_with_spaces))
def test_correct(code: str) -> None:
    violations = scanner.scan(code, include_only=models.NoBlankLineAtEnd)

    assert len(violations) == 0


def test_no_blank_line() -> None:
    violations = scanner.scan(
        incorrect_file, include_only=models.NoBlankLineAtEnd
    )

    assert len(violations) == 1
