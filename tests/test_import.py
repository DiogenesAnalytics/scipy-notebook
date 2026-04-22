"""
Sanity checks for core scientific dependencies.

This test ensures that the base environment is correctly installed and that
critical packages can be imported without ABI or linkage errors.
"""


def test_core_imports() -> None:
    """
    Verify that core scientific libraries import correctly.

    Raises:
        AssertionError: If any required package fails to import
        or lacks version info.
    """
    import sys

    import matplotlib
    import numpy as np
    import pandas as pd
    import scipy
    import sklearn

    assert np.__version__ is not None
    assert scipy.__version__ is not None
    assert pd.__version__ is not None
    assert matplotlib.__version__ is not None
    assert sklearn.__version__ is not None

    assert sys.version_info.major == 3
