import sys
from calendar import month

import pytest

from src.models import ImportsNotAtTop, InvalidImportsOrder
from src.rules import scanner

# Correct
correct_imports = (
    """
import os
import sys
""",
    """
from __future__ import smth

import tkinter as tk
from sys import smth
import os

import pytest

import gogogog
    
""",
    """
from subprocess import Popen, PIPE
""",
)

# Wrong
wrong_imports = (
    """
import sys, os
""",
)


@pytest.mark.parametrize("code", correct_imports)
def test_correct_imports(code: str):
    violations = scanner.scan(code, include_only=InvalidImportsOrder)
    print(violations)

    assert len(violations) == 0


@pytest.mark.parametrize("code", wrong_imports)
def test_incorrect_imports(code: str):
    sys.path.append("./test_project/")
    scanner.scan(code, include_only=InvalidImportsOrder)

    assert True
