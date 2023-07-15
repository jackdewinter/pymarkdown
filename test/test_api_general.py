"""
Module for directly using PyMarkdown's general api.
"""

import runpy

from pymarkdown.api import PyMarkdownApi


def get_semantic_version():
    """
    Get the semantic version from the "version.py" file.
    """
    version_meta = runpy.run_path("./pymarkdown/version.py")
    return version_meta["__version__"]


def test_api_application_version():
    """
    Test to make sure that we can retrieve the application version.
    """

    # Arrange
    scanner = PyMarkdownApi()

    # Act
    found_version = scanner.application_version

    # Assert
    assert found_version == get_semantic_version()


def test_api_interface_version():
    """
    Test to make sure that we can retrieve the interface version. As there
    is nothing to compare it to yet, right now it is set to 1.
    """

    # Arrange
    scanner = PyMarkdownApi()

    # Act
    found_version = scanner.interface_version

    # Assert
    # NOTE: If this ever changes, care must be made to publish the change
    #       widely and to think about increasing a minor version if there
    #       is a breaking change.
    assert found_version == 1
