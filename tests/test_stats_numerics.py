"""
Statistical correctness and distribution sanity checks.

Ensures RNG, mean/variance behavior, and basic probabilistic properties
are intact across builds.
"""

import numpy as np


def test_sample_mean_convergence() -> None:
    """
    Verify sample mean of Gaussian approaches zero.

    Raises:
        AssertionError: If mean deviates excessively.
    """
    x: np.ndarray = np.random.randn(10_000)

    assert abs(np.mean(x)) < 0.05


def test_variance_positive() -> None:
    """
    Ensure variance is positive for non-degenerate distributions.

    Raises:
        AssertionError: If variance is invalid.
    """
    x: np.ndarray = np.random.randn(1_000)

    assert np.var(x) > 0
