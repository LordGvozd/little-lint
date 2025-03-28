import pytest

from src.rules import scaner

# Correct
correct_imports = (
"""
import os
import sys
"""

,
"""
from __future__ import smth

import tkinter as tk
from sys import smth
import os

import pytest

import main
    
""",
"""
from subprocess import Popen, PIPE
""",
"""
import mypkg.sibling
from mypkg import sibling
from mypkg.sibling import example
""",

)

# Wrong
wrong_imports = ( """
import sys, os
""",
"""
from . import sibling
from .sibling import example

""",
"""
import myclass
import foo.bar.yourclass

"""
)


@pytest.mark.parametrize(
    "code",
    correct_imports
)
def test_correct_imports(code: str):
    violations = scaner.scan(code)

    assert len(violations) == 0


@pytest.mark.parametrize(
    "code",
    wrong_imports
)
def test_incorrect_imports(code: str):
    scaner.scan(code)

    assert True
