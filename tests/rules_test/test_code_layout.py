import ast

import pytest

from src.models import TopLevelFuncAndClassDefNotSurrounded
from src.rules import scanner
from src.rules.ast_rules import top_level_must_be_surrounded
from src.rules.file_rules import use_4_spaces_for_level


# Correct
using_4_spaces_for_level = """
def long_function_name(
    var_one, var_two, var_three,
    var_four
):
    print(var_one)

foo = long_function_name(
    var_one, var_two,
    var_three, var_four
)

foo = short(a, b, c, d, e)
short((a, v, sd), (as))

complex(
    a, 
    b, 
    c, 
    (
        d, 
        e,
        (
            f, 
            g
        )
        h,
    )
)

foo = long_function_name(
    var_one, var_two,
    var_three, var_four
)
"""


using_not_4_spaces_for_level = """
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)

def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)

foo(one,
    two
    three
)

foo(
    one,
    two
    three) 
"""

correct_toplevel_surrounding1 = """

# Comment, explaining that i cant write normal code
def foo():
    return "baz"
# Some

# f
print("Something")
# TEst


# com
@test
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


correct_toplevel_surrounding2 = """

def foo():
    return "baz"
    

def test(arg):
    print(arg)


test(foo())
test("Hello test")

print(foo())


class Cool:
    a = 1
    b = "VAZ BUHANKA"
    

class NotCool:
    a = -1
    c = "CAR"


print("Space")
nc = NotCool()


def last():
    pass
"""

function_not_surrounded = """
print("Hi")


# dsaf
def another():
    print("s")
    
print()
"""


class_not_surrounded = """
class One():
    pass
class Two():
    pass
"""


def test_4_spaces_per_level():
    assert len(use_4_spaces_for_level(using_4_spaces_for_level)) == 0
    assert len(use_4_spaces_for_level(using_not_4_spaces_for_level)) == 4


@pytest.mark.parametrize(
    "code", (correct_toplevel_surrounding1, correct_toplevel_surrounding2)
)
def test_top_level_correct_surrounded(code):
    violations = scanner.scan(code, TopLevelFuncAndClassDefNotSurrounded)

    assert len(violations) == 0


@pytest.mark.parametrize("code", (function_not_surrounded,))
def test_top_level_wrong_surrounded(code):
    violations = scanner.scan(code, TopLevelFuncAndClassDefNotSurrounded)

    assert len(violations) >= 1
