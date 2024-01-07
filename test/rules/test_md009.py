"""
Module to provide tests related to the MD009 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import (
    execute_fix_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md009") + os.sep

plugin_disable_md012 = "md012"
plugin_disable_md033 = "md033"


@pytest.mark.rules
def test_md009_bad_configuration_br_spaces():
    """
    Test to verify that a configuration error is thrown when supplying the
    br_spaces value with a string that is not an integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_paragraph_no_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.br_spaces=not-integer",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md009.br_spaces' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_configuration_br_spaces_invalid():
    """
    Test to verify that a configuration error is thrown when supplying the
    br_spaces value is not an integer in the proper range.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_paragraph_no_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.br_spaces=$#-1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md009.br_spaces' is not valid: Allowable values are greater than or equal to 0."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_configuration_strict():
    """
    Test to verify that a configuration error is thrown when supplying the
    strict value with a string that is not a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_paragraph_no_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.strict=not-boolean",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md009.strict' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md009_bad_configuration_list_item_empty_lines():
    """
    Test to verify that a configuration error is thrown when supplying the
    list_item_empty_lines value with a string that is not a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md009", "good_paragraph_no_extra.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md009.list_item_empty_lines=not-boolean",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md009.list_item_empty_lines' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


scanTests = [
    pluginRuleTest(
        "good_paragraph_no_extra",
        source_file_name=f"{source_path}good_paragraph_no_extra.md",
    ),
    pluginRuleTest(
        "good_indented_code_block_with_extra",
        source_file_name=f"{source_path}good_indented_code_block_with_extra.md",
    ),
    pluginRuleTest(
        "good_fenced_code_block_with_extra",
        source_file_name=f"{source_path}good_fenced_code_block_with_extra.md",
    ),
    pluginRuleTest(
        "unordered_list_item_empty_lines",
        source_file_name=f"{source_path}good_unordered_list_item_empty_lines.md",
    ),
    pluginRuleTest(
        "unordered_list_item_empty_lines_with_config_strict",
        source_file_name=f"{source_path}good_unordered_list_item_empty_lines.md",
        set_args=["plugins.md009.strict=$!True"],
        use_strict_config=True,
        source_file_contents="""- list item text
\a\a
  list item text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:1: MD009: Trailing spaces [Expected: 0; Actual: 2] (no-trailing-spaces)",
        fix_expected_file_contents="""- list item text
\a\a
  list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "good_unordered_list_item_empty_lines_with_config_strict_and_list_empty",
        source_file_name=f"{source_path}good_unordered_list_item_empty_lines.md",
        set_args=[
            "plugins.md009.strict=$!True",
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
    ),
    pluginRuleTest(
        "good_ordered_list_item_empty_lines_with_list_empty",
        source_file_name=f"{source_path}good_unordered_list_item_empty_lines.md",
        set_args=["plugins.md009.list_item_empty_lines=$!True"],
        use_strict_config=True,
    ),
    pluginRuleTest(
        "bad_paragraph_increasing_extra",
        source_file_name=f"{source_path}bad_paragraph_increasing_extra.md",
        source_file_contents="""this is some text\a
each line has some\a\a
extra spaces at the\a\a\a
end of the line.\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:18: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:3:20: MD009: Trailing spaces [Expected: 0 or 2; Actual: 3] (no-trailing-spaces)""",
        fix_expected_file_contents="""this is some text
each line has some\a\a
extra spaces at the\a\a
end of the line.\a\a
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_paragraph_increasing_extra_with_config_br_spaces_3",
        source_file_name=f"{source_path}bad_paragraph_increasing_extra.md",
        use_strict_config=True,
        set_args=["plugins.md009.br_spaces=$#3"],
        source_file_contents="""this is some text\a
each line has some\a\a
extra spaces at the\a\a\a
end of the line.\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:18: MD009: Trailing spaces [Expected: 0 or 3; Actual: 1] (no-trailing-spaces)
{temp_source_path}:2:19: MD009: Trailing spaces [Expected: 0 or 3; Actual: 2] (no-trailing-spaces)
{temp_source_path}:4:17: MD009: Trailing spaces [Expected: 0 or 3; Actual: 2] (no-trailing-spaces)
""",
        fix_expected_file_contents="""this is some text
each line has some
extra spaces at the\a\a\a
end of the line.
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_paragraph_increasing_extra_with_config_br_spaces_0",
        source_file_name=f"{source_path}bad_paragraph_increasing_extra.md",
        use_strict_config=True,
        set_args=["plugins.md009.br_spaces=$#0"],
        source_file_contents="""this is some text\a
each line has some\a\a
extra spaces at the\a\a\a
end of the line.\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:18: MD009: Trailing spaces [Expected: 0; Actual: 1] (no-trailing-spaces)
{temp_source_path}:2:19: MD009: Trailing spaces [Expected: 0; Actual: 2] (no-trailing-spaces)
{temp_source_path}:3:20: MD009: Trailing spaces [Expected: 0; Actual: 3] (no-trailing-spaces)
{temp_source_path}:4:17: MD009: Trailing spaces [Expected: 0; Actual: 2] (no-trailing-spaces)
""",
        fix_expected_file_contents="""this is some text
each line has some
extra spaces at the
end of the line.
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_paragraph_increasing_extra_with_config_strict",
        source_file_name=f"{source_path}bad_paragraph_increasing_extra.md",
        use_strict_config=True,
        set_args=["plugins.md009.strict=$!True"],
        source_file_contents="""this is some text\a
each line has some\a\a
extra spaces at the\a\a\a
end of the line.\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:18: MD009: Trailing spaces [Expected: 0; Actual: 1] (no-trailing-spaces)
{temp_source_path}:2:19: MD009: Trailing spaces [Expected: 0; Actual: 2] (no-trailing-spaces)
{temp_source_path}:3:20: MD009: Trailing spaces [Expected: 0; Actual: 3] (no-trailing-spaces)
{temp_source_path}:4:17: MD009: Trailing spaces [Expected: 0; Actual: 2] (no-trailing-spaces)
""",
        fix_expected_file_contents="""this is some text
each line has some\a\a
extra spaces at the\a\a
end of the line.\a\a
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_atx_heading_with_extra",
        source_file_name=f"{source_path}bad_atx_heading_with_extra.md",
        source_file_contents="""# A Heading with trailing space\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:32: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)",
        fix_expected_file_contents="""# A Heading with trailing space
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_setext_heading_with_extra",
        source_file_name=f"{source_path}bad_setext_heading_with_extra.md",
        source_file_contents="""A Heading with trailing space\a
on more than one line\a
---------------------\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:30: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:2:22: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:3:22: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
""",
        fix_expected_file_contents="""A Heading with trailing space
on more than one line
---------------------
""",
    ),
    pluginRuleTest(
        "bad_theamtic_break_with_extra",
        source_file_name=f"{source_path}bad_theamtic_break_with_extra.md",
        source_file_contents="""----------\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:11: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)",
        fix_expected_file_contents="""----------
""",
    ),
    pluginRuleTest(
        "bad_html_block_with_extra",
        source_file_name=f"{source_path}bad_html_block_with_extra.md",
        disable_rules=plugin_disable_md033,
        source_file_contents="""<!--
this\a
is\a
a\a
HTML\a
block\a
-->

<abc>\a\a
</abc>\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:3:3: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:4:2: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:5:5: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:6:6: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
""",
        fix_expected_file_contents="""<!--
this
is
a
HTML
block
-->

<abc>\a\a
</abc>\a\a
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_link_reference_definition_with_extra",
        source_file_name=f"{source_path}bad_link_reference_definition_with_extra.md",
        source_file_contents="""[abc](\a
    /url\a
    "title"\a
    )
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:7: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:2:9: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:3:12: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
""",
        fix_expected_file_contents="""[abc](
    /url
    "title"
    )
""",
    ),
    pluginRuleTest(
        "bad_blank_lines_with_extra",
        source_file_name=f"{source_path}bad_blank_lines_with_extra.md",
        disable_rules=plugin_disable_md012,
        source_file_contents="""\a
\a\a
\a\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:3:1: MD009: Trailing spaces [Expected: 0 or 2; Actual: 3] (no-trailing-spaces)
""",
        fix_expected_file_contents="""
\a\a
\a\a
""".replace(
            "\a", " "
        ),
    ),
]
fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents:
        fixTests.append(i)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md009_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test)


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md009_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)
