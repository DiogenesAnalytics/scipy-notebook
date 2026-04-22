"""
Numerical linear algebra correctness tests.

These tests validate that NumPy and SciPy are correctly linked against
a working BLAS/LAPACK backend and produce stable numerical results.
"""

from typing import Final

import numpy as np
from scipy.linalg import inv

TOL: Final[float] = 1e-10


def test_matrix_inverse_stability() -> None:
    """
    Verify that matrix inversion behaves consistently.

    Uses a random matrix and checks that A @ A^-1 ≈ I.

    Raises:
        AssertionError: If numerical error exceeds tolerance.
    """
    x: np.ndarray = np.random.randn(10, 10)
    x_inv: np.ndarray = inv(x)

    identity: np.ndarray = x @ x_inv
    error: float = float(np.linalg.norm(identity - np.eye(10)))

    assert error < TOL
