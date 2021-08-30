"""
Module to provide tests related to the "-l" option.
"""
from test.markdown_scanner import MarkdownScanner


def test_markdown_with_dash_h():
    """
    Test to make sure we get help if '-h' is supplied
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["scan", "-h"]

    expected_return_code = 0
    expected_output = """usage: main.py scan [-h] [-l] [-r] path [path ...]

positional arguments:
  path              one or more paths to scan for eligible Markdown files

optional arguments:
  -h, --help        show this help message and exit
  -l, --list-files  list the markdown files found and exit
  -r, --recurse     recursively scan directories
"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_only():
    """
    Test to make sure we get help if '-l' is supplied without any paths
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["scan", "-l"]

    expected_return_code = 2
    expected_output = ""
    expected_error = """usage: main.py scan [-h] [-l] [-r] path [path ...]
main.py scan: error: the following arguments are required: path
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
    supplied_arguments = ["scan", "-l", "my-bad-path"]

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
    supplied_arguments = ["scan", "-l", "only-text"]

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
    supplied_arguments = ["scan", "-l", "simple"]

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
    supplied_arguments = ["scan", "-l", "only-text", "simple"]

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
    supplied_arguments = ["scan", "-l", "only-text/simple_text_file.txt"]

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
    supplied_arguments = ["scan", "-l", "simple/simple.md"]

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
    supplied_arguments = [
        "scan",
        "-l",
        "only-text/simple_text_file.txt",
        "simple/simple.md",
    ]

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
    supplied_arguments = ["scan", "-l", "rules/md001/*.md"]

    expected_return_code = 0
    expected_output = """rules/md001/empty.md
rules/md001/front_matter_with_alternate_title.md
rules/md001/front_matter_with_no_title.md
rules/md001/front_matter_with_title.md
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
    supplied_arguments = ["scan", "-l", "rules/md001/z*.md"]

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


def test_markdown_with_dash_l_on_directory():
    """
    Test to make sure we get help if '-l' is supplied with a directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["scan", "-l", "../../docs"]

    expected_return_code = 0
    expected_output = """../../docs/advanced_configuration.md
../../docs/advanced_plugins.md
../../docs/advanced_scanning.md
../../docs/developer.md
../../docs/extensions.md
../../docs/faq.md
../../docs/rules.md"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_markdown_with_dash_l_and_dash_r_on_directory():
    """
    Test to make sure we get help if '-l' and '-r' is supplied with a directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = ["scan", "-l", "-r", "../../docs"]

    expected_return_code = 0
    expected_output = """../../docs/advanced_configuration.md
../../docs/advanced_plugins.md
../../docs/advanced_scanning.md
../../docs/developer.md
../../docs/extensions.md
../../docs/extensions/front-matter.md
../../docs/extensions/pragmas.md
../../docs/faq.md
../../docs/rules.md
../../docs/rules/rule_md001.md
../../docs/rules/rule_md002.md
../../docs/rules/rule_md003.md
../../docs/rules/rule_md004.md
../../docs/rules/rule_md005.md
../../docs/rules/rule_md006.md
../../docs/rules/rule_md007.md
../../docs/rules/rule_md010.md
../../docs/rules/rule_md012.md
../../docs/rules/rule_md014.md
../../docs/rules/rule_md018.md
../../docs/rules/rule_md019.md
../../docs/rules/rule_md020.md
../../docs/rules/rule_md021.md
../../docs/rules/rule_md022.md
../../docs/rules/rule_md023.md
../../docs/rules/rule_md024.md
../../docs/rules/rule_md025.md
../../docs/rules/rule_md026.md
../../docs/rules/rule_md027.md
../../docs/rules/rule_md028.md
../../docs/rules/rule_md031.md
../../docs/rules/rule_md032.md
../../docs/rules/rule_md033.md
../../docs/rules/rule_md034.md
../../docs/rules/rule_md035.md
../../docs/rules/rule_md036.md
../../docs/rules/rule_md037.md
../../docs/rules/rule_md038.md
../../docs/rules/rule_md039.md
../../docs/rules/rule_md040.md
../../docs/rules/rule_md041.md
../../docs/rules/rule_md042.md
../../docs/rules/rule_md043.md
../../docs/rules/rule_md044.md
../../docs/rules/rule_md045.md
../../docs/rules/rule_md046.md
../../docs/rules/rule_md047.md
../../docs/rules/rule_md048.md"""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, cwd=scanner.resource_directory
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
