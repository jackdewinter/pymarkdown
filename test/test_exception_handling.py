"""
Module to provide tests for altering how the command line handles exceptions.
"""

from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.utils import create_temporary_markdown_file, generate_path_to_bad_plugin


def test_exception_handling_no_exception(scanner_default: MarkdownScanner) -> None:
    """
    Test to validate normal operations of scanning files without any plugin exception being thrown.
    """

    contents_file_1_and_3 = """#\tPerfectly healthy file
This triggers several rules:
1. Guess which ones
1. Bla
"""

    with create_temporary_markdown_file(
        contents_file_1_and_3, file_name_prefix="tmp1"
    ) as file_name_1:
        with create_temporary_markdown_file(
            contents_file_1_and_3, file_name_prefix="tmp3"
        ) as file_name_3:
            # Arrange
            supplied_arguments = ["scan", file_name_1, file_name_3]

            expected_results = ExpectedResults(
                return_code=1,
                expected_output=f"""{file_name_1}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{file_name_1}:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
{file_name_1}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{file_name_1}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{file_name_3}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{file_name_3}:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
{file_name_3}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{file_name_3}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
""",
            )

            # Act
            execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

            # Assert
            execute_results.assert_results(expected_results=expected_results)


def test_exception_handling_scan_with_plugin_exception_and_no_flag(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to validate normal operations of scanning files with a simple plugin exception being thrown.
    """

    contents_file_1_and_3 = """#\tPerfectly healthy file
This triggers several rules:
1. Guess which ones
1. Bla
"""
    contents_file_2 = """# File the causes exception

throw_exception
"""
    plugin_path = generate_path_to_bad_plugin("bad_next_line_with_scan_trigger.py")

    with create_temporary_markdown_file(
        contents_file_1_and_3, file_name_prefix="tmp1"
    ) as file_name_1:
        with create_temporary_markdown_file(
            contents_file_2, file_name_prefix="tmp2"
        ) as file_name_2:
            with create_temporary_markdown_file(
                contents_file_1_and_3, file_name_prefix="tmp3"
            ) as file_name_3:
                # Arrange
                supplied_arguments = [
                    "--add-plugin",
                    plugin_path,
                    "scan",
                    file_name_1,
                    file_name_2,
                    file_name_3,
                ]

                expected_results = ExpectedResults(
                    return_code=1,
                    expected_output=f"""{file_name_1}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{file_name_1}:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
{file_name_1}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{file_name_1}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
""",
                    expected_error=f"""
                
BadPluginError encountered while scanning '{file_name_2}':
(Line 3): Plugin id 'MDE008' had a critical failure during the 'next_line' action.
""",
                )

                # Act
                execute_results = scanner_default.invoke_main(
                    arguments=supplied_arguments
                )

                # Assert
                execute_results.assert_results(expected_results=expected_results)


def test_exception_handling_scan_with_plugin_exception_and_flag(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to validate normal operations of scanning files with a simple plugin exception being thrown.
    """

    contents_file_1_and_3 = """#\tPerfectly healthy file
This triggers several rules:
1. Guess which ones
1. Bla
"""
    contents_file_2 = """# File the causes exception

throw_exception
"""
    plugin_path = generate_path_to_bad_plugin("bad_next_line_with_scan_trigger.py")

    with create_temporary_markdown_file(
        contents_file_1_and_3, file_name_prefix="tmp1"
    ) as file_name_1:
        with create_temporary_markdown_file(
            contents_file_2, file_name_prefix="tmp2"
        ) as file_name_2:
            with create_temporary_markdown_file(
                contents_file_1_and_3, file_name_prefix="tmp3"
            ) as file_name_3:
                # Arrange
                supplied_arguments = [
                    "--add-plugin",
                    plugin_path,
                    "--continue-on-error",
                    "scan",
                    file_name_1,
                    file_name_2,
                    file_name_3,
                ]

                expected_results = ExpectedResults(
                    return_code=1,
                    expected_output=f"""{file_name_1}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{file_name_1}:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
{file_name_1}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{file_name_1}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{file_name_3}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{file_name_3}:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
{file_name_3}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{file_name_3}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
""",
                    expected_error=f"""{file_name_2}:0:0: (Line 3): Plugin id 'MDE008' had a critical failure during the 'next_line' action.
""",
                )
                # Act
                execute_results = scanner_default.invoke_main(
                    arguments=supplied_arguments
                )

                # Assert
                execute_results.assert_results(expected_results=expected_results)


def test_exception_handling_scan_with_tokenization_exception_and_no_flag(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to validate normal operations of scanning files with a simple tokenization exception being thrown.
    """

    contents_file_1_and_3 = """#\tPerfectly healthy file
This triggers several rules:
1. Guess which ones
1. Bla
"""
    extension_enable_front_matter = "extensions.front-matter.enabled=$!True"
    contents_file_2 = """---
test: assert
---
"""
    with create_temporary_markdown_file(
        contents_file_1_and_3, file_name_prefix="tmp1"
    ) as file_name_1:
        with create_temporary_markdown_file(
            contents_file_2, file_name_prefix="tmp2"
        ) as file_name_2:
            with create_temporary_markdown_file(
                contents_file_1_and_3, file_name_prefix="tmp3"
            ) as file_name_3:
                # Arrange
                supplied_arguments = [
                    "--set",
                    extension_enable_front_matter,
                    "scan",
                    file_name_1,
                    file_name_2,
                    file_name_3,
                ]

                expected_results = ExpectedResults(
                    return_code=1,
                    expected_output=f"""{file_name_1}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{file_name_1}:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
{file_name_1}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{file_name_1}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
""",
                    expected_error="""
                
Unexpected Error(BadTokenizationError): An unhandled error occurred processing the document.
""",
                )

                # Act
                execute_results = scanner_default.invoke_main(
                    arguments=supplied_arguments
                )

                # Assert
                execute_results.assert_results(expected_results=expected_results)


def test_exception_handling_scan_with_tokenization_exception_and_flag(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to validate normal operations of scanning files with a simple tokenization exception being thrown.
    """

    contents_file_1_and_3 = """#\tPerfectly healthy file
This triggers several rules:
1. Guess which ones
1. Bla
"""
    extension_enable_front_matter = "extensions.front-matter.enabled=$!True"
    contents_file_2 = """---
test: assert
---
"""
    with create_temporary_markdown_file(
        contents_file_1_and_3, file_name_prefix="tmp1"
    ) as file_name_1:
        with create_temporary_markdown_file(
            contents_file_2, file_name_prefix="tmp2"
        ) as file_name_2:
            with create_temporary_markdown_file(
                contents_file_1_and_3, file_name_prefix="tmp3"
            ) as file_name_3:
                # Arrange
                supplied_arguments = [
                    "--continue-on-error",
                    "--set",
                    extension_enable_front_matter,
                    "scan",
                    file_name_1,
                    file_name_2,
                    file_name_3,
                ]

                expected_results = ExpectedResults(
                    return_code=1,
                    expected_output=f"""{file_name_1}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{file_name_1}:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
{file_name_1}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{file_name_1}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{file_name_3}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{file_name_3}:1:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)
{file_name_3}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{file_name_3}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
""",
                    expected_error=f"""{file_name_2}:0:0: An unhandled error occurred processing the document.""",
                )

                # Act
                execute_results = scanner_default.invoke_main(
                    arguments=supplied_arguments
                )

                # Assert
                execute_results.assert_results(expected_results=expected_results)


def test_exception_handling_fix_with_plugin_exception_and_no_flag(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to validate normal operations of scanning files with a simple plugin exception being thrown.
    """

    contents_file_1_and_3 = """#\tPerfectly healthy file
This triggers several rules:
1. Guess which ones
1. Bla
"""
    contents_file_2 = """# File the causes exception

throw_exception
"""
    plugin_path = generate_path_to_bad_plugin("bad_next_line_with_fix_trigger.py")

    with create_temporary_markdown_file(
        contents_file_1_and_3, file_name_prefix="tmp1"
    ) as file_name_1:
        with create_temporary_markdown_file(
            contents_file_2, file_name_prefix="tmp2"
        ) as file_name_2:
            with create_temporary_markdown_file(
                contents_file_1_and_3, file_name_prefix="tmp3"
            ) as file_name_3:
                # Arrange
                supplied_arguments = [
                    "--add-plugin",
                    plugin_path,
                    "fix",
                    file_name_1,
                    file_name_2,
                    file_name_3,
                ]

                expected_results = ExpectedResults(
                    return_code=1,
                    expected_output=f"""Fixed: {file_name_1}""",
                    expected_error=f"""

                
BadPluginError encountered while scanning '{file_name_2}':
(Line 3): Plugin id 'MDE008' had a critical failure during the 'next_line' action.""",
                )

                # Act
                execute_results = scanner_default.invoke_main(
                    arguments=supplied_arguments
                )

                # Assert
                execute_results.assert_results(expected_results=expected_results)


def test_exception_handling_fix_with_plugin_exception_and_flag(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to validate normal operations of scanning files with a simple plugin exception being thrown.
    """

    contents_file_1_and_3 = """#\tPerfectly healthy file
This triggers several rules:
1. Guess which ones
1. Bla
"""
    contents_file_2 = """# File the causes exception

throw_exception
"""
    plugin_path = generate_path_to_bad_plugin("bad_next_line_with_fix_trigger.py")

    with create_temporary_markdown_file(
        contents_file_1_and_3, file_name_prefix="tmp1"
    ) as file_name_1:
        with create_temporary_markdown_file(
            contents_file_2, file_name_prefix="tmp2"
        ) as file_name_2:
            with create_temporary_markdown_file(
                contents_file_1_and_3, file_name_prefix="tmp3"
            ) as file_name_3:
                # Arrange
                supplied_arguments = [
                    "--continue-on-error",
                    "--add-plugin",
                    plugin_path,
                    "fix",
                    file_name_1,
                    file_name_2,
                    file_name_3,
                ]

                expected_results = ExpectedResults(
                    return_code=1,
                    expected_output=f"""Fixed: {file_name_1}
Fixed: {file_name_3}""",
                    expected_error=f"""{file_name_2}:0:0: (Line 3): Plugin id 'MDE008' had a critical failure during the 'next_line' action.""",
                )
                # Act
                execute_results = scanner_default.invoke_main(
                    arguments=supplied_arguments
                )

                # Assert
                execute_results.assert_results(expected_results=expected_results)


def test_exception_handling_fix_with_tokenization_exception_and_no_flag(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to validate normal operations of scanning files with a simple tokenization exception being thrown.
    """

    contents_file_1_and_3 = """#\tPerfectly healthy file
This triggers several rules:
1. Guess which ones
1. Bla
"""
    extension_enable_front_matter = "extensions.front-matter.enabled=$!True"
    contents_file_2 = """---
test: assert
---
"""
    with create_temporary_markdown_file(
        contents_file_1_and_3, file_name_prefix="tmp1"
    ) as file_name_1:
        with create_temporary_markdown_file(
            contents_file_2, file_name_prefix="tmp2"
        ) as file_name_2:
            with create_temporary_markdown_file(
                contents_file_1_and_3, file_name_prefix="tmp3"
            ) as file_name_3:
                # Arrange
                supplied_arguments = [
                    "--set",
                    extension_enable_front_matter,
                    "fix",
                    file_name_1,
                    file_name_2,
                    file_name_3,
                ]

                expected_results = ExpectedResults(
                    return_code=1,
                    expected_output=f"""Fixed: {file_name_1}""",
                    expected_error="""
                
Unexpected Error(BadTokenizationError): An unhandled error occurred processing the document.
""",
                )

                # Act
                execute_results = scanner_default.invoke_main(
                    arguments=supplied_arguments
                )

                # Assert
                execute_results.assert_results(expected_results=expected_results)


def test_exception_handling_fix_with_tokenization_exception_and_flag(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to validate normal operations of scanning files with a simple tokenization exception being thrown.
    """

    contents_file_1_and_3 = """#\tPerfectly healthy file
This triggers several rules:
1. Guess which ones
1. Bla
"""
    extension_enable_front_matter = "extensions.front-matter.enabled=$!True"
    contents_file_2 = """---
test: assert
---
"""
    with create_temporary_markdown_file(
        contents_file_1_and_3, file_name_prefix="tmp1"
    ) as file_name_1:
        with create_temporary_markdown_file(
            contents_file_2, file_name_prefix="tmp2"
        ) as file_name_2:
            with create_temporary_markdown_file(
                contents_file_1_and_3, file_name_prefix="tmp3"
            ) as file_name_3:
                # Arrange
                supplied_arguments = [
                    "--continue-on-error",
                    "--set",
                    extension_enable_front_matter,
                    "fix",
                    file_name_1,
                    file_name_2,
                    file_name_3,
                ]

                expected_results = ExpectedResults(
                    return_code=1,
                    expected_output=f"""Fixed: {file_name_1}
Fixed: {file_name_3}""",
                    expected_error=f"""{file_name_2}:0:0: An unhandled error occurred processing the document.""",
                )
                # Act
                execute_results = scanner_default.invoke_main(
                    arguments=supplied_arguments
                )

                # Assert
                execute_results.assert_results(expected_results=expected_results)
