import sys
from calendar import month

import pytest

from src.models import (
    ImportsNotAtTop,
    InvalidImportsOrder,
    ManyImportOnOneLine,
    ModuleNotFound,
)
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
many_import_on_one_line = """
import sys, os
"""

invalid_imports_order = """
import astunparse
import sys
"""

not_exist_module_import = """
import zibyubibyaka
"""


@pytest.mark.parametrize("code", correct_imports)
def test_correct_imports(code: str):
    violations = scanner.scan(code, include_only=InvalidImportsOrder)
    print(violations)

    assert len(violations) == 0


@pytest.mark.parametrize(
    "code",
    (many_import_on_one_line, invalid_imports_order, not_exist_module_import),
)
def test_incorrect_imports(code: str):
    sys.path.append("./test_project/")

    import_on_one_line = scanner.scan(
        code,
        include_only=(
            ManyImportOnOneLine,
            InvalidImportsOrder,
            ModuleNotFound,
        ),
    )

    assert len(import_on_one_line) == 1
