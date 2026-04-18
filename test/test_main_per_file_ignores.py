"""
Module to provide tests related the "plugins.per-file-ignores" configuration item.
"""

import os
import tempfile
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults

from .utils import temporary_change_to_directory, write_temporary_configuration

# pylint: disable=too-many-lines


def test_markdown_per_file_ignores_baseline(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure we have a baseline for per-file-ignores that is working as expected when no rule is ignored.
    """

    # Arrange
    configuration_content = {"plugins": {"per-file-ignores": {"test_value": "md041"}}}
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_file_path}:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
{source_file_path}:3:1: MD013: Line length [Expected: 80, Actual: 94] (line-length)
""",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_non_matching(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry that has no hope of matching the file does not cause any rules to be ignored.
    """

    # Arrange
    configuration_content = {"plugins": {"per-file-ignores": {"a*.json": "Md041"}}}
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_prefix="a",
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_file_path}:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
{source_file_path}:3:1: MD013: Line length [Expected: 80, Actual: 94] (line-length)
""",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_matching_single_path_single_rule(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry that matches a given file causes a single rule to be ignored for that file.
    """

    # Arrange
    configuration_content = {"plugins": {"per-file-ignores": {"a*.md": "Md041"}}}
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_prefix="a",
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_file_path}:3:1: MD013: Line length [Expected: 80, Actual: 94] (line-length)
""",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_matching_single_path_single_rule_upper_case(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry that matches a given file causes a single rule (specified in upper case) to be ignored for that file.
    """

    # Arrange
    configuration_content = {"plugins": {"per-file-ignores": {"a*.md": "MD041"}}}
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_prefix="a",
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_file_path}:3:1: MD013: Line length [Expected: 80, Actual: 94] (line-length)
""",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_matching_single_path_multiple_rules(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry that matches a given file causes multiple rules to be ignored for that file.
    """

    # Arrange
    configuration_content = {
        "plugins": {"per-file-ignores": {"a*.md": "Md041,Md013,md047"}}
    }
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_prefix="a",
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults()

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_value_not_string(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry that is not a string.
    """

    # Arrange
    configuration_content = {"plugins": {"per-file-ignores": {"a*.md": 1}}}
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_error="Configuration Error: The value for property 'plugins.per-file-ignores.'a*.md'' must be of type 'str'.",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_value_empty_string(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry that is an empty string.
    """

    # Arrange
    configuration_content = {"plugins": {"per-file-ignores": {"a*.md": ""}}}
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_error="Configuration Error: Property value for `plugins.per-file-ignores.'a*.md'` must be a non-empty, comma-separated list of rule identifiers.",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_value_only_comma(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry that is a string with only a comma.
    """

    # Arrange
    configuration_content = {"plugins": {"per-file-ignores": {"a*.md": ","}}}
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_error="Configuration Error: Property value for 'plugins.per-file-ignores.'a*.md'' contains a rule identifier '' that is not a valid rule identifier.",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_value_unrecognized_identifier(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry that is an identifier that is not recognized as a valid rule identifier.
    """

    # Arrange
    configuration_content = {
        "plugins": {"per-file-ignores": {"a*.md": "not-an-indentifier"}}
    }
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_error="Configuration Error: Property value for 'plugins.per-file-ignores.'a*.md'' contains a rule identifier 'not-an-indentifier' that is not a valid rule identifier.",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_value_is_json_list_of_elements(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry that includes a JSON list of elements instead of a string is properly rejected.
    """

    # Arrange
    configuration_content = {"plugins": {"per-file-ignores": {"a*.md": ["md041"]}}}
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_error="Configuration Error: The value for property 'plugins.per-file-ignores.'a*.md'' must be of type 'str'.",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_property_name_with_single_apostrophe(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry with a name that has an odd number of apostrophes is properly rejected.
    """

    # Arrange
    configuration_content = {"plugins": {"per-file-ignores": {"ab'cd": "md041"}}}
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_error="Configuration Error: Property name `plugins.per-file-ignores.ab'cd` has an odd number of apostrophes, which is not allowed.",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_property_name_has_extra_level(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry name does not include an extra level.
    """

    # Arrange
    configuration_content = {
        "plugins": {"per-file-ignores": {"tmp/": {"Fred": "md041"}}}
    }
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_error="Configuration Error: Property name `plugins.per-file-ignores.tmp/` cannot have an inner element with name 'fred'.",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_quoted_property_name_has_extra_level(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry that includes an extra level in the property name is properly rejected even if the property name is quoted (which would allow for an extra level if it were not rejected).
    """

    # Arrange
    configuration_content = {
        "plugins": {"per-file-ignores": {"a*.md": {"Fred": "md041"}}}
    }
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_error="Configuration Error: Property name `plugins.per-file-ignores.'a*.md'` cannot have an inner element with name 'fred'.",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_quoted_property_name_has_extra_level_local(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry that includes an extra level in the property name
    at the local level (e.g. "Fred.Flintstone").
    """

    # Arrange
    configuration_content = {
        "plugins": {"per-file-ignores": {"a*.md": {"Fred.Flintstone": "md041"}}}
    }
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_error="Configuration Error: Property name `plugins.per-file-ignores.'a*.md'` cannot have an inner element with name ''fred.flintstone''.",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_json_format_single_pattern_single_identifier(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry in a JSON format with a single pattern and single identifier is properly applied.
    """

    # Arrange
    configuration_content = '{"plugins": {"per-file-ignores": {"a*.md": "md041"}}}'
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_prefix="a",
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"{source_file_path}:3:1: MD013: Line length [Expected: 80, Actual: 94] (line-length)",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_json_format_double_pattern_single_identifier(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry in a JSON format with two patterns and single identifier is properly applied.
    """

    # Arrange
    configuration_content = (
        '{"plugins": {"per-file-ignores": {"a*.md": "md041", "aa*.md": "md013"}}}'
    )
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_prefix="aa",
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults()

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_json_format_single_pattern_double_identifier(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry in a JSON format with a single pattern and two identifiers is properly applied.
    """

    # Arrange
    configuration_content = (
        '{"plugins": {"per-file-ignores": {"a*.md": "md013,md041"}}}'
    )
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".json",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_prefix="a",
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults()

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_yaml_format_single_pattern_single_identifier(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry in a YAML format with a single pattern and single identifier is properly applied.
    """

    # Arrange
    configuration_content = """
plugins:
  per-file-ignores:
    a*.md: md041
"""
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".yml",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_prefix="a",
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"{source_file_path}:3:1: MD013: Line length [Expected: 80, Actual: 94] (line-length)",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_yaml_format_double_pattern_single_identifier(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry in a YAML format with two patterns and single identifier is properly applied.
    """

    # Arrange
    configuration_content = """plugins:
  per-file-ignores:
    a*.md: md041
    aa*.md: md013
"""
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".yaml",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_prefix="aa",
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults()

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_yaml_format_single_pattern_double_identifier(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry in a YAML format with a single pattern and two identifiers is properly applied.
    """

    # Arrange
    configuration_content = """
plugins:
  per-file-ignores:
    a*.md: md013,md041
"""
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".yaml",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_prefix="a",
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults()

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_toml_format_single_pattern_single_identifier(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry in a TOML format with a single pattern and single identifier is properly applied.
    """

    # Arrange
    configuration_content = """[tool.pymarkdown]
plugins.per-file-ignores."a*.md" = "md041"
"""
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".toml",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_prefix="a",
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"{source_file_path}:3:1: MD013: Line length [Expected: 80, Actual: 94] (line-length)",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_toml_format_double_pattern_single_identifier(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry in a TOML format with two patterns and single identifier is properly applied.
    """

    # Arrange
    configuration_content = """[tool.pymarkdown]
plugins.per-file-ignores."a*.md" = "md041"
plugins.per-file-ignores."aa*.md" = "md013"
"""
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".toml",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_prefix="aa",
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults()

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_per_file_ignores_toml_format_single_pattern_double_identifier(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure a per-file-ignores entry in a TOML format with a single pattern and two identifiers is properly applied.
    """

    # Arrange
    configuration_content = """[tool.pymarkdown]
plugins.per-file-ignores."a*.md" = "md013,md041"
"""
    scan_content = """## This is a doc

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        configuration_file_path = write_temporary_configuration(
            configuration_content,
            directory=tmp_dir_path,
            file_name_suffix=".toml",
        )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_prefix="a",
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "-c",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults()

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner_default.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)
