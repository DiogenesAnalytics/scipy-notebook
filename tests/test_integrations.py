"""
Integration tests for optional scientific environment components.

This module validates interoperability between higher-level ecosystem
packages that commonly fail at environment build time despite importing
successfully, including database connectivity and geospatial libraries.
"""


def test_sqlalchemy_in_memory() -> None:
    """
    Verify SQLAlchemy can execute a simple in-memory query.

    Confirms the database abstraction layer is functional.

    Raises:
        AssertionError: If query execution fails.
    """
    from sqlalchemy import create_engine, text

    engine = create_engine("sqlite:///:memory:")

    with engine.connect() as connection:
        result: int = connection.execute(text("SELECT 1")).scalar_one()

    assert result == 1


def test_geopandas_geometry() -> None:
    """
    Verify GeoPandas and Shapely integrate correctly.

    Confirms geospatial geometry objects operate as expected.

    Raises:
        AssertionError: If geometry area calculation is incorrect.
    """
    import geopandas as gpd
    from shapely.geometry import Polygon

    polygon: Polygon = Polygon(
        [
            (0.0, 0.0),
            (1.0, 0.0),
            (1.0, 1.0),
            (0.0, 1.0),
        ]
    )

    frame: gpd.GeoDataFrame = gpd.GeoDataFrame(geometry=[polygon])

    area: float = float(frame.geometry.area.iloc[0])

    assert area == 1.0
