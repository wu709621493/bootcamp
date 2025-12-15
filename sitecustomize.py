"""Ensure local packages are importable without installation.

This module is automatically loaded by Python's site mechanism when it is
available on ``sys.path``. We use it to prepend the repository's bundled
packages to ``sys.path`` so commands like ``python -m jb_bootcamp.prime_utils``
work from a fresh checkout without an editable install.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODULE_PATH = ROOT / "modules" / "jb_bootcamp"

if MODULE_PATH.is_dir():
    module_dir = str(MODULE_PATH)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)
