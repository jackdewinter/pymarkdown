"""
Module to provide
"""

import os
import tempfile
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults

from .utils import temporary_change_to_directory, write_temporary_configuration


def test_markdown_scan_with_failure_no_url_flag() -> None:
    """
    Test to ...
    """

    # Arrange
    scanner = MarkdownScanner()
    # configuration_content = {"plugins": {"per-file-ignores": {"test_value": "md041"}}}
    scan_content = """# Sample

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    # dir=os.getcwd() is needed here to avoid /private/var vs /var issues on MacOS when using the temporary directory context manager.
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        # configuration_file_path = write_temporary_configuration(
        #     configuration_content,
        #     directory=tmp_dir_path,
        #     file_name_suffix=".json",
        # )
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            # "-c",
            # configuration_file_path,
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
            execute_results = scanner.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_scan_with_failure_and_show_url_flag() -> None:
    """
    Test to ...
    """

    # Arrange
    scanner = MarkdownScanner()
    scan_content = """# Sample

this is a very, very, very, very, very, very, (yes, this is on purpose), very, very, long line
"""

    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp_dir_path:
        source_file_path = write_temporary_configuration(
            scan_content,
            directory=tmp_dir_path,
            file_name_suffix=".md",
        )

        supplied_arguments = [
            "scan",
            "--url",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_file_path}:3:1: MD013: Line length [Expected: 80, Actual: 94] (line-length) https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md013.md
""",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)


def test_markdown_scan_with_failure_and_show_url_config() -> None:
    """
    Test to ...
    """

    # Arrange
    scanner = MarkdownScanner()
    configuration_content = {"scan": {"show-urls": True}}
    scan_content = """# Sample

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
            "--config",
            configuration_file_path,
            "scan",
            source_file_path,
        ]

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{source_file_path}:3:1: MD013: Line length [Expected: 80, Actual: 94] (line-length) https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md013.md
""",
        )

        # Act
        with temporary_change_to_directory(tmp_dir_path):
            execute_results = scanner.invoke_main(
                arguments=supplied_arguments, suppress_first_line_heading_rule=False
            )

        # Assert
        execute_results.assert_results(expected_results=expected_results)
