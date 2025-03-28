import ast
import functools
import sys
import importlib.util
from collections import defaultdict
from collections.abc import Callable, Sequence
from enum import unique, Enum
import inspect
from pathlib import Path
from pprint import pprint
from typing import TypeAlias, ClassVar, Final, Type, Iterable

import astunparse

from src import constants
from src.core import Scaner
from src.models import *


def iter_node_children(node: ast.AST):
    for name, field in ast.iter_fields(node):
        if isinstance(field, ast.AST):
            yield field
        if isinstance(field, list):
            for item in field:
                if isinstance(item, ast.AST):
                    yield item






scaner = Scaner()





test_code = """

from sys import write

import sys


import time
import abc

import astunparse


def foo():
    print( "bar")

test =        1        


if test ==   2:
    pass
    
# very_long_string = "12345678910111213141516171819022122232425262728293031323334353637383940414243444546474849505152535455565758596061626364656667686970717273747576777879"

"""

pprint(scaner.scan(test_code))



