"""
Module to make sure that the version number is tested.
"""

import runpy


def test_version() -> None:
    """
    Make sure that the version is a valid semantic version.
    """

    # Arrange
    version_meta = runpy.run_path("./pymarkdown/version.py")

    # Act
    actual_value = version_meta["__version__"]

    # Assert
    parts = actual_value.split(".")
    assert len(parts) == 3
    assert int(parts[0]) >= 0
    assert int(parts[1]) >= 0
    assert int(parts[2]) >= 0
