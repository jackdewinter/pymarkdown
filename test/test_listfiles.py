"""
Module to provide tests related to the "-l" option.
"""
from test.markdown_scanner import MarkdownScanner


def test_markdown_with_dash_l_only():
    """
    Test to make sure we get help if '-l' is supplied without any paths
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["-l"]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py [-h] [--version] [-l] [-e ENABLE_RULES] [-d DISABLE_RULES]
               [--add-plugin ADD_PLUGIN] [--config CONFIGURATION_FILE]
               [--stack-trace]
               [--log-level {CRITICAL,ERROR,WARNING,INFO,DEBUG}]
               [--log-file LOG_FILE]
               path [path ...]
main.py: error: the following arguments are required: path
"""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_bad_path():
    """
    Test to make sure we get help if '-l' is supplied with a bad path.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["-l", "my-bad-path"]

    expected_return_code = 1
    expected_output = ""
    expected_error = """Provided path 'my-bad-path' does not exist.
"""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_non_md_directory():
    """
    Test to make sure we get help if '-l' is supplied with a path containing no md files.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["-l", "only-text"]

    expected_return_code = 1
    expected_output = ""
    expected_error = """No matching files found.
"""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_md_directory():
    """
    Test to make sure we get help if '-l' is supplied with a path containing a simple md file.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["-l", "simple"]

    expected_return_code = 0
    expected_output = """simple/simple.md
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_mixed_directories():
    """
    Test to make sure we get help if '-l' is supplied with a path containing the md directory and the non-md directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["-l", "only-text", "simple"]

    expected_return_code = 0
    expected_output = """simple/simple.md
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_non_md_file():
    """
    Test to make sure we get help if '-l' is supplied with a file path that isn't a md file.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["-l", "only-text/simple_text_file.txt"]

    expected_return_code = 1
    expected_output = ""
    expected_error = """Provided file path 'only-text/simple_text_file.txt' is not a valid file. Skipping.
"""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_md_file():
    """
    Test to make sure we get help if '-l' is supplied with a file path that is a simple md file.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["-l", "simple/simple.md"]

    expected_return_code = 0
    expected_output = """simple/simple.md
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_mixed_files():
    """
    Test to make sure we get help if '-l' is supplied with a file path that is a simple md file and one that isn't.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["-l", "only-text/simple_text_file.txt", "simple/simple.md"]

    expected_return_code = 1
    expected_output = """"""
    expected_error = """Provided file path 'only-text/simple_text_file.txt' is not a valid file. Skipping.
"""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_globbed_files():
    """
    Test to make sure we get help if '-l' is supplied with a globbed file path that works.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["-l", "rules/md001/*.md"]

    expected_return_code = 0
    expected_output = """rules/md001/empty.md
rules/md001/improper_atx_heading_incrementing.md
rules/md001/improper_setext_heading_incrementing.md
rules/md001/proper_atx_heading_incrementing.md
rules/md001/proper_setext_heading_incrementing.md"""
    expected_error = """"""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_on_non_matching_globbed_files():
    """
    Test to make sure we get help if '-l' is supplied with a globbed file path that works.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["-l", "rules/md001/z*.md"]

    expected_return_code = 1
    expected_output = """"""
    expected_error = (
        """Provided glob path 'rules/md001/z*.md' did not match any files."""
    )

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
