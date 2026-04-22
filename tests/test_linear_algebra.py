"""
Linear algebra invariants and shape correctness tests.

These ensure that the underlying BLAS implementation behaves consistently
and that matrix operations are numerically stable.
"""

import numpy as np


def test_matrix_multiplication_shape() -> None:
    """
    Validate matrix multiplication shape correctness.

    Raises:
        AssertionError: If output shape is incorrect.
    """
    a: np.ndarray = np.random.randn(100, 50)
    b: np.ndarray = np.random.randn(50, 30)

    result: np.ndarray = a @ b

    assert result.shape == (100, 30)


def test_associativity_numerical_stability() -> None:
    """
    Check approximate associativity of matrix multiplication.

    Note:
        Floating point arithmetic is not strictly associative; this test
        ensures deviations remain within tolerance.

    Raises:
        AssertionError: If deviation exceeds tolerance.
    """
    a: np.ndarray = np.random.randn(20, 20)
    b: np.ndarray = np.random.randn(20, 20)
    c: np.ndarray = np.random.randn(20, 20)

    lhs: np.ndarray = (a @ b) @ c
    rhs: np.ndarray = a @ (b @ c)

    assert np.allclose(lhs, rhs, atol=1e-8)
