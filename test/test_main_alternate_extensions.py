"""
Module to provide tests related to alternate extensions.
"""
import os
from test.markdown_scanner import MarkdownScanner


def test_markdown_with_dash_ae_with_invalid_file_extension():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "scan",
        "-ae",
        ".abc",
        file_to_scan,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        f"Provided file path '{file_to_scan}' is not a valid file. Skipping."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_ae_with_valid_file_extension():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        ".txt",
        file_to_scan,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_ae_with_valid_file_extension_multiple():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = "test/resources/double-line-with-blank-and-trailing.txt"
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        ".txt,.md",
        file_to_scan,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_ae_with_invalid_file_extension_no_period():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        "md",
        file_to_scan,
    ]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension 'md' must start with a period."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_ae_with_invalid_file_extension_no_alphanum():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        ".*",
        file_to_scan,
    ]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension '.*' must only contain alphanumeric characters after the period."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_ae_with_invalid_file_extension_only_period():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        ".",
        file_to_scan,
    ]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension '.' must have at least one character after the period."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_ae_with_invalid_file_extension_semicolon_as_sep():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        ".md;.txt",
        file_to_scan,
    ]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension '.md;.txt' must only contain alphanumeric characters after the period."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_ae_with_invalid_file_extension_empty():
    """
    Test to make sure
    """

    # Arrange
    scanner = MarkdownScanner()
    file_to_scan = os.path.join(
        "test", "resources", "double-line-with-blank-and-trailing.txt"
    )
    supplied_arguments = [
        "--stack-trace",
        "scan",
        "-ae",
        "",
        file_to_scan,
    ]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] [-ae ALTERNATE_EXTENSIONS] path [path ...]
main.py scan: error: argument -ae/--alternate-extensions: Extension '' must start with a period."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
