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


def test_4_spaces_per_level():
    assert len(use_4_spaces_for_level(using_4_spaces_for_level)) == 0
    assert len(use_4_spaces_for_level(using_not_4_spaces_for_level)) == 4
