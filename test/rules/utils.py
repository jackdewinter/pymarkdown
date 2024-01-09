import os
from contextlib import contextmanager
from dataclasses import dataclass
from test.markdown_scanner import MarkdownScanner
from test.utils import (
    assert_file_is_as_expected,
    assert_if_lists_different,
    copy_to_temporary_file,
    write_temporary_configuration,
)
from typing import Any, List, Optional


@dataclass
class pluginConfigErrorTest:
    """
    Class to represent the testing needs of a plugin rule.
    """

    name: str
    use_strict_config: bool
    set_args: List[str]
    expected_error: str


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
    use_fix_debug: bool = False
    disable_rules: str = ""
    enable_rules: str = ""
    scan_expected_return_code: int = 0
    scan_expected_output: str = ""
    scan_expected_error: str = ""
    fix_expected_return_code: int = 3
    fix_expected_file_contents: str = ""
    fix_expected_output: Optional[str] = None
    fix_expected_error: str = ""
    add_plugin_path: str = ""


def id_test_plug_rule_fn(val: Any) -> str:
    """
    Id functions to allow for parameterization to be used more meaningfully.
    """
    if isinstance(val, (pluginRuleTest, pluginConfigErrorTest)):
        return val.name
    raise AssertionError()


def build_fix_and_clash_lists(scanTests: List[pluginRuleTest]):
    fixTests: List[pluginRuleTest] = []
    clashTests: List[pluginRuleTest] = []
    for i in scanTests:
        if i.fix_expected_file_contents:
            fixTests.append(i)
    for i in fixTests:
        if i.disable_rules:
            clashTests.append(i)
    return fixTests, clashTests


@contextmanager
def build_arguments(
    test: pluginRuleTest, is_fix: bool, skip_disabled_rules: bool = False
):
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
        if test.add_plugin_path:
            supplied_arguments.extend(("--add-plugin", test.add_plugin_path))
        if test.use_strict_config:
            supplied_arguments.append("--strict-config")
        if test.set_args:
            for next_set_arg in test.set_args:
                supplied_arguments.extend(("--set", next_set_arg))
        if test.enable_rules:
            supplied_arguments.extend(("--enable-rules", test.enable_rules))
        if test.disable_rules and not skip_disabled_rules:
            supplied_arguments.extend(("--disable-rules", test.disable_rules))

        if is_fix:
            if test.use_fix_debug:
                supplied_arguments.append("-x-fix-debug"),
            supplied_arguments.extend(("-x-fix", "scan", temp_source_path))
        else:
            supplied_arguments.extend(("scan", temp_source_path))

        yield temp_source_path, supplied_arguments
    finally:
        if temp_source_path:
            os.remove(temp_source_path)


def execute_scan_test(test: pluginRuleTest, host_rule_id: str):
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
    if test.disable_rules:
        with build_arguments(test, False, skip_disabled_rules=True) as (
            temp_source_path,
            supplied_arguments,
        ):
            execute_results = scanner.invoke_main(arguments=supplied_arguments)
            assert execute_results.return_code == 1 or execute_results.return_code == 0
            assert execute_results.std_err.getvalue() == ""
            disabled_rules = test.disable_rules.lower().split(",")

            found_rules = []
            for next_line in execute_results.std_out.getvalue().split("\n"):
                if not next_line:
                    continue
                assert next_line.startswith(temp_source_path)
                split_line = next_line[len(temp_source_path) + 1 :].split(":")
                assert len(split_line) > 3
                oo = split_line[2].strip().lower()
                if oo != host_rule_id and oo not in found_rules:
                    found_rules.append(oo)

            disabled_rules.sort()
            found_rules.sort()
            assert_if_lists_different(disabled_rules, found_rules)


def execute_fix_test(test: pluginRuleTest):
    scanner = MarkdownScanner()
    with build_arguments(test, True) as (temp_source_path, supplied_arguments):
        expected_return_code = test.fix_expected_return_code
        if test.fix_expected_output is not None:
            expected_output = test.fix_expected_output.replace(
                "{temp_source_path}", temp_source_path
            )
        else:
            expected_output = f"Fixed: {temp_source_path}"
        if test.fix_expected_error:
            expected_error = test.fix_expected_error.replace(
                "{temp_source_path}", temp_source_path
            )
        else:
            expected_error = ""
        expected_file_contents = test.fix_expected_file_contents

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


def execute_clash_test(test: pluginRuleTest):
    pass


def execute_configuration_test(test: pluginConfigErrorTest, file_to_use: str):
    scanner = MarkdownScanner()

    temp_source_path = copy_to_temporary_file(file_to_use)
    supplied_arguments = []
    if test.use_strict_config:
        supplied_arguments.append("--strict-config")
    if test.set_args:
        for next_set_arg in test.set_args:
            supplied_arguments.extend(("--set", next_set_arg))

    supplied_arguments.extend(("scan", temp_source_path))

    expected_return_code = 1
    expected_output = ""
    expected_error = test.expected_error

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
