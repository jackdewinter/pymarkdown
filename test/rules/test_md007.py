"""
Module to provide tests related to the MD007 rule.
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

# pylint: disable=too-many-lines

source_path = os.path.join("test", "resources", "rules", "md007") + os.sep

plugin_disable_md005_md027 = "md005,md027"
plugin_disable_md023 = "MD023"
plugin_disable_md027 = "md027"
plugin_disable_md030 = "md030"


@pytest.mark.rules
def test_md007_bad_configuration_indent():
    """
    Test to verify that a configuration error is thrown when supplying the
    indent value with a string that is not an integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "good_list_indentation.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md007.indent=bad",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md007.indent' must be of type 'int'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_configuration_start_indented():
    """
    Test to verify that a configuration error is thrown when supplying the
    start_indented value with a value that is not a boolean.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "good_list_indentation.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md007.start_indented=bad",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md007.start_indented' must be of type 'bool'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md007_bad_configuration_indent_bad():
    """
    Test to verify that a configuration error is thrown when supplying the
    indent value with a string that is not a valid integer.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "good_list_indentation.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md007.indent=$#5",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md007.indent' is not valid: Allowable values are between 2 and 4."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


scanTests = [
    pluginRuleTest(
        "good_list_indentation_x",
        source_file_name=f"{source_path}good_list_indentation.md",
    ),
    pluginRuleTest(
        "bad_list_indentation_level_0",
        source_file_name=f"{source_path}bad_list_indentation_level_0.md",
        source_file_contents="""This is a test

 * this is level 1
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)",
        fix_expected_file_contents="""This is a test

* this is level 1
""",
    ),
    pluginRuleTest(
        "bad_list_indentation_level_1",
        source_file_name=f"{source_path}bad_list_indentation_level_1.md",
        disable_rules=plugin_disable_md023,
        source_file_contents="""This is a test

* this is level 1
   * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:4:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""This is a test

* this is level 1
  * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_indentation_level_2",
        source_file_name=f"{source_path}bad_list_indentation_level_2.md",
        disable_rules=plugin_disable_md023,
        source_file_contents="""This is a test

* this is level 1
  * this is level 2
     * this is level 3
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:5:6: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)",
        fix_expected_file_contents="""This is a test

* this is level 1
  * this is level 2
    * this is level 3
""",
    ),
    pluginRuleTest(
        "good_list_indentation_in_block_quote",
        source_file_name=f"{source_path}good_list_indentation_in_block_quote.md",
    ),
    pluginRuleTest(
        "good_list_indentation_in_double_block_quote",
        source_file_name=f"{source_path}good_list_indentation_in_double_block_quote.md",
    ),
    pluginRuleTest(
        "good_unordered_list_in_ordered_list",
        source_file_name=f"{source_path}good_unordered_list_in_ordered_list.md",
        disable_rules=plugin_disable_md030,
    ),
    pluginRuleTest(
        "bad_unordered_list_in_ordered_list",
        source_file_name=f"{source_path}bad_unordered_list_in_ordered_list.md",
        disable_rules=plugin_disable_md030,
        source_file_contents="""1.  ordered list
     + sublist
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:6: MD007: Unordered list indentation [Expected: 5, Actual=6] (ul-indent)",
        fix_expected_file_contents="""1.  ordered list
    + sublist
""",
    ),
    pluginRuleTest(
        "bad_level_1_unordered_list_in_ordered_list",
        source_file_name=f"{source_path}bad_level_1_unordered_list_in_ordered_list.md",
        disable_rules=plugin_disable_md030,
        source_file_contents="""1.  ordered list
    + sublist
       + sublist
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:8: MD007: Unordered list indentation [Expected: 7, Actual=8] (ul-indent)",
        fix_expected_file_contents="""1.  ordered list
    + sublist
      + sublist
""",
    ),
    pluginRuleTest(
        "good_unordered_list_in_double_ordered_list",
        source_file_name=f"{source_path}good_unordered_list_in_double_ordered_list.md",
    ),
    pluginRuleTest(
        "bad_unordered_list_in_double_ordered_list",
        source_file_name=f"{source_path}bad_unordered_list_in_double_ordered_list.md",
        disable_rules=plugin_disable_md030,
        source_file_contents="""1. ordered list
   1. inner ordered list
       + sublist
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:8: MD007: Unordered list indentation [Expected: 7, Actual=8] (ul-indent)",
        fix_expected_file_contents="""1. ordered list
   1. inner ordered list
      + sublist
""",
    ),
    pluginRuleTest(
        "good_unordered_ordered_unordere_ordered_unordered",
        source_file_name=f"{source_path}good_unordered_ordered_unordere_ordered_unordered.md",
    ),
    pluginRuleTest(
        "bad_unordered_bad_ordered_unordered_ordered_unordered",
        source_file_name=f"{source_path}bad_unordered_bad_ordered_unordered_ordered_unordered.md",
        disable_rules=plugin_disable_md030,
        source_file_contents=""" + level 1
   1. level 2
      + level 3
        1. level 4
           + level 5
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)",
        fix_expected_file_contents="""+ level 1
   1. level 2
      + level 3
        1. level 4
           + level 5
""",
    ),
    pluginRuleTest(
        "bad_unordered_ordered_unordered_bad_ordered_unordered",
        source_file_name=f"{source_path}bad_unordered_ordered_unordered_bad_ordered_unordered.md",
        disable_rules=plugin_disable_md030,
        source_file_contents="""+ level 1
  1. level 2
      + level 3
        1. level 4
           + level 5
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:7: MD007: Unordered list indentation [Expected: 6, Actual=7] (ul-indent)",
        fix_expected_file_contents="""+ level 1
  1. level 2
     + level 3
        1. level 4
           + level 5
""",
    ),
    pluginRuleTest(
        "bad_unordered_ordered_unordered_ordered_unordered_bad",
        source_file_name=f"{source_path}bad_unordered_ordered_unordered_ordered_unordered_bad.md",
        disable_rules=plugin_disable_md030,
        source_file_contents="""+ level 1
  1. level 2
     + level 3
       1. level 4
           + level 5
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:5:12: MD007: Unordered list indentation [Expected: 11, Actual=12] (ul-indent)",
        fix_expected_file_contents="""+ level 1
  1. level 2
     + level 3
       1. level 4
          + level 5
""",
    ),
    pluginRuleTest(
        "bad_list_indentation_in_block_quote_level_0",
        source_file_name=f"{source_path}bad_list_indentation_in_block_quote_level_0.md",
        disable_rules=plugin_disable_md027,
        source_file_contents="""This is a test

>  * this is level 1
>    * this is level 2
>      * this is level 3
""",
        scan_expected_return_code=1,
        scan_expected_output=(
            "{temp_source_path}:3:4: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)\n"
            + "{temp_source_path}:4:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)\n"
            + "{temp_source_path}:5:8: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)"
        ),
        fix_expected_file_contents="""This is a test

>  * this is level 1
>    * this is level 2
>      * this is level 3
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_text",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_text.md",
        disable_rules=plugin_disable_md027,
        source_file_contents="""> This is some text
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output=(
            "{temp_source_path}:4:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)"
        ),
        fix_expected_file_contents="""> This is some text
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_atx_heading",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_atx_heading.md",
        disable_rules=plugin_disable_md027,
        source_file_contents="""> # This is some text
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:4:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""> # This is some text
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_thematic_break",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_thematic_break.md",
        disable_rules=plugin_disable_md027,
        source_file_contents="""> This is some text
>
> --------
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:6:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""> This is some text
>
> --------
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_setext_heading",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_setext_heading.md",
        disable_rules=plugin_disable_md027,
        source_file_contents="""> This is some text
> ---------
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:5:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""> This is some text
> ---------
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_html_block",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_html_block.md",
        disable_rules=plugin_disable_md027,
        source_file_contents="""> <!--
> This is a comment
> -->
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:6:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""> <!--
> This is a comment
> -->
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_fenced_block",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_fenced_block.md",
        disable_rules=plugin_disable_md027,
        source_file_contents="""> ```fenced
> This is a comment
> ```
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:6:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""> ```fenced
> This is a comment
> ```
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_indented_block",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_indented_block.md",
        disable_rules=plugin_disable_md027,
        source_file_contents=""">     This is a comment
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:4:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents=""">     This is a comment
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_link_reference_definition",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_link_reference_definition.md",
        disable_rules=plugin_disable_md027,
        source_file_contents="""> [link]: /url
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:4:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""> [link]: /url
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_other_list",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_other_list.md",
        disable_rules=plugin_disable_md027,
        source_file_contents="""> 1. This is another list.
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:4:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""> 1. This is another list.
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "good_unordered_list_elements",
        source_file_name=f"{source_path}good_unordered_list_elements.md",
    ),
    pluginRuleTest(
        "bad_unordered_list_elements",
        source_file_name=f"{source_path}bad_unordered_list_elements.md",
        disable_rules=plugin_disable_md005_md027,
        source_file_contents="""This is a test

 * this is level 1
 * this is also level 1
   * this is level 2
   * this is also level 2
      * this is level 3
   * this is also level 2
    * this is also level 2
    * this is also level 2
* this is also level 1
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:4:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:5:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:6:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:7:7: MD007: Unordered list indentation [Expected: 4, Actual=6] (ul-indent)
{temp_source_path}:8:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:9:5: MD007: Unordered list indentation [Expected: 2, Actual=4] (ul-indent)
{temp_source_path}:10:5: MD007: Unordered list indentation [Expected: 2, Actual=4] (ul-indent)
""",
        fix_expected_file_contents="""This is a test

* this is level 1
* this is also level 1
  * this is level 2
  * this is also level 2
    * this is level 3
  * this is also level 2
  * this is also level 2
  * this is also level 2
* this is also level 1
""",
    ),
    pluginRuleTest(
        "good_list_indentation_by_four",
        source_file_name=f"{source_path}good_list_indentation_by_four.md",
        set_args=["plugins.md007.indent=$#4"],
    ),
    pluginRuleTest(
        "good_list_indentation_with_start",
        source_file_name=f"{source_path}good_list_indentation_with_start.md",
        set_args=["plugins.md007.start_indented=$!True"],
    ),
    pluginRuleTest(
        "issue_301",
        source_file_name=f"{source_path}issue-301.md",
        disable_rules=plugin_disable_md005_md027,
        set_args=["plugins.md007.indent=$#4"],
        source_file_contents="""# Demo markdown

- Item
    - Sub item

1. Ordered item
    - Sub unordered item
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:7:5: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)",
        fix_expected_file_contents="""# Demo markdown

- Item
    - Sub item

1. Ordered item
   - Sub unordered item
""",
    ),
]
fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents:
        fixTests.append(i)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md007_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test)


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md007_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)
