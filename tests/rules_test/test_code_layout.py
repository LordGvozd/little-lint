from src.rules import use_4_spaces_for_level

# Correct
using_4_spaces_for_level = """
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
"""

using_not_4_spaces_for_level = """
foo = long_function_name(var_one, var_two,
    var_three, var_four)

def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
"""


def test_4_spaces_per_level():
    assert use_4_spaces_for_level(using_4_spaces_for_level) is None
