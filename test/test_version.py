"""
Module to make sure that the version number is tested.
"""

import os
import platform
import runpy
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.utils import ARGPARSE_X, USAGE_X

from pymarkdown.version_helper import VersionHelper


def test_version_composition() -> None:
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


def test_version_command_line_help(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure the command line interface to versions
    only shows the version help related information.
    """

    # Arrange
    supplied_arguments = ["version", "-h"]

    expected_results = ExpectedResults(
        return_code=0,
        expected_output="""usage: {USAGE_X} version [-h] [--extended]

{ARGPARSE_X}
  -h, --help  show this help message and exit
  --extended  show extended version information
""".replace("{ARGPARSE_X}", ARGPARSE_X).replace("{USAGE_X}", USAGE_X),
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_version_command_line_reflects_files(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure we get help if 'version' is supplied.

    This function is shadowed by
    test_markdown_return_code_default_success.
    """

    # Arrange
    supplied_arguments = ["version"]

    version_path = os.path.join(".", "pymarkdown", "version.py")
    version_meta = runpy.run_path(version_path)
    semantic_version = version_meta["__version__"]

    expected_results = ExpectedResults(expected_output="""{version}
""".replace("{version}", semantic_version))

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_version_command_line_with_extended(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure we get help if 'version' is supplied.

    This function is shadowed by
    test_markdown_return_code_default_success.
    """

    # Arrange
    supplied_arguments = ["version", "--extended"]

    version_path = os.path.join(".", "pymarkdown", "version.py")
    version_meta = runpy.run_path(version_path)
    semantic_version = version_meta["__version__"]
    python_version = f"{platform.python_version()} ({platform.python_implementation()}, {platform.python_compiler()})"

    expected_results = ExpectedResults(
        expected_output=f"""PyMarkdown:         {semantic_version}
Python:             {python_version}
Operating System:   {VersionHelper.get_operating_system()}
"""
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)
