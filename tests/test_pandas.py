"""
Pandas dataframe and grouping behavior tests.

Ensures that groupby, aggregation, and dtype handling behave consistently
across environment builds.
"""

from pathlib import Path
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


def test_excel_roundtrip(tmp_path: Path) -> None:
    """
    Verify DataFrame can be written to and read from Excel.

    Args:
        tmp_path: Temporary pytest directory.

    Raises:
        AssertionError: If round-trip data changes.
    """
    import pandas as pd

    file_path: Path = tmp_path / "roundtrip.xlsx"

    original: pd.DataFrame = pd.DataFrame({"x": [1, 2, 3]})
    original.to_excel(file_path, index=False)

    loaded: pd.DataFrame = pd.read_excel(file_path)

    assert loaded.equals(original)


def test_hdf_roundtrip(tmp_path: Path) -> None:
    """
    Verify DataFrame can be written to and read from HDF5.

    Args:
        tmp_path: Temporary pytest directory.

    Raises:
        AssertionError: If round-trip data changes.
    """
    import pandas as pd

    file_path: Path = tmp_path / "roundtrip.h5"

    original: pd.DataFrame = pd.DataFrame({"x": [1, 2, 3]})
    original.to_hdf(file_path, key="df")

    loaded: pd.DataFrame = pd.read_hdf(file_path, key="df")

    assert loaded.equals(original)
