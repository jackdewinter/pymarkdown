"""
Module to provide tests related to the MD006 rule.
"""

import os
from test.rules.utils import (
    execute_fix_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md006") + os.sep

plugin_enable_this_rule = "MD006"

__plugin_disable_md004 = "md004"
__plugin_disable_md007 = "MD007"
__plugin_disable_md005_md007 = "md005,MD007"
__plugin_disable_md007_md027 = "MD007,md027"

scanTests = [
    pluginRuleTest(
        "good_indentation",
        source_file_name=f"{source_path}good_indentation.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "good_indentation_in_block_quote",
        source_file_name=f"{source_path}good_indentation_in_block_quote.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "bad_indentation_x",
        source_file_name=f"{source_path}bad_indentation.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md007,
        source_file_contents=""" * First Item
 * Second Item
""",
        scan_expected_return_code=1,
        scan_expected_output=(
            "{temp_source_path}:1:2: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
            + "{temp_source_path}:2:2: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)"
        ),
        fix_expected_file_contents="""* First Item
* Second Item
""",
    ),
    pluginRuleTest(
        "good_indentation_unordered",
        source_file_name=f"{source_path}bad_indentation_unordered.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "bad_indentation_in_block_quote",
        source_file_name=f"{source_path}bad_indentation_in_block_quote.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md007_md027,
        source_file_contents=""">  * First Item
>  * Second Item
""",
        scan_expected_return_code=1,
        scan_expected_output=(
            "{temp_source_path}:1:4: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
            + "{temp_source_path}:2:4: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)"
        ),
        fix_expected_file_contents="""> * First Item
> * Second Item
""",
    ),
    pluginRuleTest(
        "bad_ignore_bad_second_level",
        source_file_name=f"{source_path}good_ignore_bad_second_level.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md005_md007,
        source_file_contents="""* First Item
  * First-First
   * First-Second
    * First-Third
* Second Item
""",
        scan_expected_return_code=1,
        scan_expected_output=(
            "{temp_source_path}:3:4: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
            + "{temp_source_path}:4:5: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)"
        ),
        fix_expected_file_contents="""* First Item
  * First-First
  * First-Second
  * First-Third
* Second Item
""",
    ),
    pluginRuleTest(
        "good_not_ordered",
        source_file_name=f"{source_path}good_not_ordered.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "good_items_with_multiple_lines",
        source_file_name=f"{source_path}good_items_with_multiple_lines.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "good_items_with_multiple_lines_in_block_quote",
        source_file_name=f"{source_path}good_items_with_multiple_lines_in_block_quote.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "good_indentation_ordered_in_unordered",
        source_file_name=f"{source_path}good_indentation_ordered_in_unordered.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "good_indentation_unordered_in_ordered",
        source_file_name=f"{source_path}good_indentation_unordered_in_ordered.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "bad_indentation_ordered_in_unordered",
        source_file_name=f"{source_path}bad_indentation_ordered_in_unordered.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md007,
        source_file_contents=""" * First Item
   1. Second Item
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:2: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)",
        fix_expected_file_contents="""* First Item
   1. Second Item
""",
    ),
    pluginRuleTest(
        "bad_indentation_unordered_in_ordered",
        source_file_name=f"{source_path}bad_indentation_unordered_in_ordered.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md007,
        source_file_contents=""" 1. First Item
     - Second Item
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:6: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)",
        fix_expected_file_contents=""" 1. First Item
    - Second Item
""",
    ),
    pluginRuleTest(
        "good_indentation_nested",
        source_file_name=f"{source_path}good_indentation_nested.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "bad_indentation_nested",
        source_file_name=f"{source_path}bad_indentation_nested.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md007,
        source_file_contents="""- top level 1
   - First Item
   - Second Item
- top level 2
   - First Item
   - Second Item
""",
        scan_expected_return_code=1,
        scan_expected_output=(
            "{temp_source_path}:2:4: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
            + "{temp_source_path}:3:4: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
            + "{temp_source_path}:5:4: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)\n"
            + "{temp_source_path}:6:4: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)"
        ),
        fix_expected_file_contents="""- top level 1
  - First Item
  - Second Item
- top level 2
  - First Item
  - Second Item
""",
    ),
    pluginRuleTest(
        "issue_478",
        source_file_name=f"{source_path}issue_478.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md004,
    ),
    pluginRuleTest(
        "mix_md006_md004",
        is_mix_test=True,
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md007,
        source_file_contents=""" + first
   * second
     - third
 * first
   - second
     + third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)
{temp_source_path}:2:4: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: asterisk] (ul-style)
{temp_source_path}:3:6: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: dash] (ul-style)
{temp_source_path}:4:2: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)
{temp_source_path}:5:4: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: dash] (ul-style)
""",
        fix_expected_file_contents="""+ first
   + second
     + third
+ first
   + second
     + third
""",
    ),
]

fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents:
        fixTests.append(i)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md006_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, plugin_enable_this_rule)


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md006_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)
