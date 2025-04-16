from src.rules.rules_container import RulesContainer, Rule


def test_add_rule_without_args() -> None:
    container = RulesContainer()

    @container.rule
    def func():
        return "test_value"

    assert len(container.get_all_rules()) == 1  # Is one rule in container
    assert (
        container.get_all_rules()[0].checker() == "test_value"
    )  # Is func added correctly

    assert container.get_all_rules()[0].args is None
    assert container.get_all_rules()[0].kwargs is None


def test_add_rule_with_args() -> None:
    container = RulesContainer()

    @container.rule(1, foo="bar")
    def func():
        return 52

    rules = container.get_all_rules()
    assert len(rules) == 1
    assert rules[0].checker() == 52
    assert rules[0].args == (1,)
    assert rules[0].kwargs == {"foo": "bar"}


def test_add_many_rules() -> None:
    container = RulesContainer()

    # Without any args or kwargs
    @container.rule
    def boo():
        return "baz"

    # Only args
    @container.rule(1, 2, "hello")
    def hello():
        return 1

    # Only kwargs
    @container.rule(batman="bruce wayne", spiderman="piter parker")
    def create_superhero():
        return "giga man"

    # Mixed args and kwargs
    @container.rule("print", hello="world")
    def print_hello_world():
        return "hello world"

    rules = container.get_all_rules()

    assert len(rules) == 4
