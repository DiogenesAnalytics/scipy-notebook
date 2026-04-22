"""
Pytest configuration module for deterministic numerical testing.

This module is automatically discovered by pytest and is used to configure
global test behavior across the entire test suite.

Primary purpose:
    - Ensure reproducible random number generation across all tests
    - Eliminate nondeterminism in numerical and statistical assertions

Note:
    This affects NumPy's legacy RNG (`np.random`) and Python's `random` module.
"""

import random

import numpy as np


def pytest_configure() -> None:
    """
    Pytest hook executed once per test session during initialization.

    This function seeds all global random number generators to ensure that
    all tests involving randomness are deterministic and reproducible.

    Side Effects:
        - Sets NumPy global RNG seed to 42
        - Sets Python standard library RNG seed to 42

    Returns:
        None
    """
    np.random.seed(42)
    random.seed(42)
