"""
Module for directly using PyMarkdown's general api.
"""

import os
import runpy
from test.patches.patch_base import PatchBase
from test.patches.patch_builtin_open import path_builtin_open_with_exception
from test.utils import assert_that_exception_is_raised
from typing import Any

from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException


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


def test_api_tokenizer_init_exception():
    """
    Test to make sure that if we have any problems initializing the
    core, that we can handle it.

    This function shadows
    test_markdown_with_dash_x_init
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    exception_path = os.path.join("pymarkdown", "resources", "entities.json")

    # Act
    with path_builtin_open_with_exception(
        os.path.abspath(exception_path), "rt", OSError("blah")
    ):
        expected_output = """BadTokenizationError encountered while initializing tokenizer:
Named character entity map file '{path}' was not loaded (blah).""".replace(
            "{path}", os.path.abspath(exception_path)
        )

        # Act & Assert
        assert_that_exception_is_raised(
            PyMarkdownApiException,
            expected_output,
            PyMarkdownApi().scan_path,
            source_path,
        )


class PatchFileSourceProvider(PatchBase):
    """
    Class to provide for a path to the FileSourceProvider to allow it to return
    `None`, causing an exception.
    """

    def __init__(self) -> None:
        super().__init__(
            "pymarkdown.general.source_providers.FileSourceProvider.get_next_line"
        )

    def start(self, log_action: bool = True) -> None:
        """
        Start the patching of the "open" function.
        """
        super().start(log_action=log_action)

        self._add_side_effect(self.__my_get_next_line)
        if log_action:
            self._add_action_comment("started")

    def stop(
        self, log_action: bool = True, print_action_comments: bool = False
    ) -> None:
        """
        Stop the patching of the "open" function.
        """
        super().stop(log_action=log_action, print_action_comments=print_action_comments)

    def __my_get_next_line(self, *args: Any, **kwargs: Any) -> Any:
        assert not args
        assert not kwargs


def test_api_tokenizer_failure_during_file_scan():
    """
    Test to make sure that we can handle an unexpected error that gets raised
    in the middle of the parsing of one or more files.

    This function shadows
    test_markdown_with_failure_during_file_scan
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md047", "end_with_blank_line.md"
    )
    exception_path = os.path.abspath(
        os.path.join("pymarkdown", "resources", "entities.json")
    )

    # Act
    with path_builtin_open_with_exception(exception_path, "rt", IOError("bob"), True):
        expected_output = """BadTokenizationError encountered while initializing tokenizer:
Named character entity map file '{path}' was not loaded (bob).""".replace(
            "{path}", exception_path
        )

        # Act & Assert
        assert_that_exception_is_raised(
            PyMarkdownApiException,
            expected_output,
            PyMarkdownApi().scan_path,
            source_path,
        )
