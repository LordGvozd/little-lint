import functools
from collections.abc import FunctionType
from dataclasses import dataclass
from typing import Any, Mapping, overload

from black.trans import Callable

from src.types import AstRule, FileRule, LineRule


@dataclass
class Rule:
    checker: Callable[[Any], Any]

    args: tuple[Any, ...] | None = None
    kwargs: Mapping[Any, Any] | None = None


class RulesContainer:
    def __init__(self):
        self._rules = []

    def get_all_rules(self):
        return self._rules

    def _add_rule(
        self,
        checker: Callable[[Any], Any],
        args: tuple[Any, ...] | None = None,
        kwargs: Mapping[Any, Any] | None = None,
    ) -> None:
        self._rules.append(Rule(checker, args, kwargs))

    @overload
    def rule(self, func: Callable) -> Any:
        pass

    @overload
    def rule(self, *rule_args, **rule_kwargs) -> Any:
        pass

    def rule(self, *rule_args, **rule_kwargs):
        # If decorator without args or kwargs
        if isinstance(rule_args[0], FunctionType):

            self._add_rule(rule_args[0], None, None)

            def wrapper(*args, **kwargs):
                return rule_args[0](*args, **kwargs)

            return wrapper
        else:
            # If decorator takes some args or kwargs
            def actual_decorator(func: AstRule | FileRule | LineRule):
                self._add_rule(func, rule_args, rule_kwargs)

                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    return func(*args, **kwargs)

                return wrapper

            return actual_decorator
