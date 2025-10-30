"""Test configuration for the :mod:`jb_bootcamp` package."""

from __future__ import annotations

import sys
from pathlib import Path


def pytest_configure() -> None:
    """Ensure the package root is importable during tests."""

    package_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(package_root))
