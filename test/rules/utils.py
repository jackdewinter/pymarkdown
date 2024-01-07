import os
from contextlib import contextmanager
from dataclasses import dataclass
from test.markdown_scanner import MarkdownScanner
from test.utils import (
    assert_file_is_as_expected,
    copy_to_temporary_file,
    write_temporary_configuration,
)
from typing import Any, List, Optional


@dataclass
class pluginRuleTest:
    """
    Class to represent the testing needs of a plugin rule.
    """

    name: str
    source_file_name: Optional[str] = None
    source_file_contents: Optional[str] = None
    set_args: Optional[List[str]] = None
    use_strict_config: bool = False
    disable_rules: str = ""
    enable_rules: str = ""
    scan_expected_return_code: int = 0
    scan_expected_output: str = ""
    scan_expected_error: str = ""
    fix_expected_file_contents: str = ""


def id_test_plug_rule_fn(val: Any) -> str:
    """
    Id functions to allow for parameterization to be used more meaningfully.
    """
    if isinstance(val, pluginRuleTest):
        return val.name
    raise AssertionError()


@contextmanager
def build_arguments(test: pluginRuleTest, is_fix: bool):
    temp_source_path = None
    try:
        if test.source_file_name:
            temp_source_path = copy_to_temporary_file(test.source_file_name)
            if test.source_file_contents:
                assert_file_is_as_expected(temp_source_path, test.source_file_contents)
        else:
            assert test.source_file_contents
            temp_source_path = write_temporary_configuration(
                test.source_file_contents, file_name_suffix=".md"
            )

        supplied_arguments = []
        if test.use_strict_config:
            supplied_arguments.append("--strict-config")
        if test.set_args:
            for next_set_arg in test.set_args:
                supplied_arguments.extend(("--set", next_set_arg))
        if test.enable_rules:
            supplied_arguments.extend(("--enable-rules", test.enable_rules))
        if test.disable_rules:
            supplied_arguments.extend(("--disable-rules", test.disable_rules))

        if is_fix:
            supplied_arguments.extend(("-x-fix", "scan", temp_source_path))
        else:
            supplied_arguments.extend(("scan", temp_source_path))

        yield temp_source_path, supplied_arguments
    finally:
        if temp_source_path:
            os.remove(temp_source_path)


def execute_scan_test(test: pluginRuleTest):
    scanner = MarkdownScanner()
    with build_arguments(test, False) as (temp_source_path, supplied_arguments):
        expected_return_code = test.scan_expected_return_code
        expected_output = test.scan_expected_output.replace(
            "{temp_source_path}", temp_source_path
        )
        expected_error = test.scan_expected_error

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


def execute_fix_test(test: pluginRuleTest):
    scanner = MarkdownScanner()
    with build_arguments(test, True) as (temp_source_path, supplied_arguments):
        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""
        expected_file_contents = test.fix_expected_file_contents

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)
