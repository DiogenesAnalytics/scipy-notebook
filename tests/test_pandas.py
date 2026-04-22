"""
Pandas dataframe and grouping behavior tests.

Ensures that groupby, aggregation, and dtype handling behave consistently
across environment builds.
"""

from typing import Final

import numpy as np
import pandas as pd

GROUPS: Final[int] = 10


def test_groupby_mean() -> None:
    """
    Validate groupby aggregation correctness.

    Raises:
        AssertionError: If grouping or aggregation is incorrect.
    """
    df: pd.DataFrame = pd.DataFrame(
        {
            "a": np.arange(100),
            "b": np.random.randn(100),
        }
    )

    grouped: pd.DataFrame = df.groupby(df["a"] % GROUPS).mean()

    assert grouped.shape[0] == GROUPS
    assert "b" in grouped.columns
