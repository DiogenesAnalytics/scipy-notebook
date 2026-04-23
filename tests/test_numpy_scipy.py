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


def test_numba_jit_execution() -> None:
    """
    Verify Numba can compile and execute a simple JIT function.

    Confirms the LLVM toolchain and runtime compilation are working.

    Raises:
        AssertionError: If compiled execution produces
            an unexpected result.
    """
    from numba import njit

    @njit
    def square(x: int) -> int:
        return x * x

    result: int = square(5)

    assert result == 25


def test_sympy_symbolic_derivative() -> None:
    """
    Verify symbolic differentiation works correctly.

    Confirms the symbolic mathematics stack is operational.

    Raises:
        AssertionError: If symbolic differentiation fails.
    """
    import sympy as sp

    x: sp.Symbol = sp.Symbol("x")
    expression: sp.Expr = x**2 + 3 * x
    derivative: sp.Expr = sp.diff(expression, x)

    assert derivative == 2 * x + 3
