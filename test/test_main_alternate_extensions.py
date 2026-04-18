"""
Module to provide tests related to alternate extensions.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from typing import Tuple


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", source_file_name)
    return source_path, os.path.abspath(source_path)


def test_markdown_with_dash_ae_with_invalid_file_extension(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure
    """

    # Arrange
    path_to_scan, _ = __generate_source_path("double-line-with-blank-and-trailing.txt")
    supplied_arguments = [
        "scan",
        "-ae",
        ".abc",
        path_to_scan,
    ]

    expected_results = ExpectedResults(return_code=1)

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_ae_with_valid_file_extension(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure
    """

    # Arrange
    path_to_scan, _ = __generate_source_path("double-line-with-blank-and-trailing.txt")
    supplied_arguments = [
        "scan",
        "-ae",
        ".txt",
        path_to_scan,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_ae_with_valid_file_extension_multiple(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure that a file with a non-md extension but with
    alternate extensions is accepted as a valid file.

    This function is a shadow of
    test_api_list_for_non_markdown_file_with_alternate_extensions
    """

    # Arrange
    file_to_scan = "test/resources/double-line-with-blank-and-trailing.txt"
    supplied_arguments = [
        "scan",
        "-ae",
        ".txt,.md",
        file_to_scan,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_ae_with_invalid_file_extension_no_period(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure
    """

    # Arrange
    path_to_scan, _ = __generate_source_path("double-line-with-blank-and-trailing.txt")
    supplied_arguments = [
        "scan",
        "-ae",
        "md",
        path_to_scan,
    ]

    expected_results = ExpectedResults(
        return_code=2,
        expected_error="""usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS]
                    [-e PATH_EXCLUSIONS] [--respect-gitignore]
                    path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension 'md' must start with a period.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_ae_with_invalid_file_extension_no_alphanum(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure
    """

    # Arrange
    path_to_scan, _ = __generate_source_path("double-line-with-blank-and-trailing.txt")
    supplied_arguments = [
        "scan",
        "-ae",
        ".*",
        path_to_scan,
    ]

    expected_results = ExpectedResults(
        return_code=2,
        expected_error="""usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS]
                    [-e PATH_EXCLUSIONS] [--respect-gitignore]
                    path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension '.*' must only contain alphanumeric characters after the period.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_ae_with_invalid_file_extension_only_period(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure
    """

    # Arrange
    path_to_scan, _ = __generate_source_path("double-line-with-blank-and-trailing.txt")
    supplied_arguments = [
        "scan",
        "-ae",
        ".",
        path_to_scan,
    ]

    expected_results = ExpectedResults(
        return_code=2,
        expected_error="""usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS]
                    [-e PATH_EXCLUSIONS] [--respect-gitignore]
                    path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension '.' must have at least one character after the period.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_ae_with_invalid_file_extension_semicolon_as_sep(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure
    """

    # Arrange
    path_to_scan, _ = __generate_source_path("double-line-with-blank-and-trailing.txt")
    supplied_arguments = [
        "scan",
        "-ae",
        ".md;.txt",
        path_to_scan,
    ]

    expected_results = ExpectedResults(
        return_code=2,
        expected_error="""usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS]
                    [-e PATH_EXCLUSIONS] [--respect-gitignore]
                    path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension '.md;.txt' must only contain alphanumeric characters after the period.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_ae_with_invalid_file_extension_empty(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure
    """

    # Arrange
    path_to_scan, _ = __generate_source_path("double-line-with-blank-and-trailing.txt")
    supplied_arguments = [
        "scan",
        "-ae",
        "",
        path_to_scan,
    ]

    expected_results = ExpectedResults(
        return_code=2,
        expected_error="""usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS]
                    [-e PATH_EXCLUSIONS] [--respect-gitignore]
                    path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Alternate extensions cannot be an empty string.""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_ae_xxx1(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure
    """

    # Arrange
    path_to_scan, absolute_path_to_scan = __generate_source_path("test-directory-1")
    supplied_arguments = [
        "scan",
        "-l",
        "--alternate-extension=.qmd",
        f"{path_to_scan}/*",
    ]

    expected_results = ExpectedResults(
        expected_output=f"{absolute_path_to_scan}{os.sep}test.qmd"
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_markdown_with_dash_ae_xxx2(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure
    """

    # Arrange
    path_to_scan, absolute_path_to_scan = __generate_source_path("test-directory-1")
    supplied_arguments = [
        "scan",
        "-l",
        "--alternate-extension=.qmd",
        f"{path_to_scan}/",
    ]

    expected_results = ExpectedResults(
        expected_output=f"{absolute_path_to_scan}{os.sep}test.qmd"
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)
