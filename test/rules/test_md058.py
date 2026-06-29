"""
Module to provide tests related to the MD058 rule.
"""

from test.rules.utils import (
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

# A heading adjacent to a table (no blank line) is the clean way to trigger
# MD058; that same adjacency triggers MD022, which is unrelated here.
__plugin_disable_md022 = "md022"
__plugin_disable_md022_md041 = "md022,md041"

scanTests = [
    pluginRuleTest(
        "good_surrounded",
        enable_extensions="markdown-tables",
        source_file_contents="""# Top

| abc | def |
| --- | --- |
| ghi | jkl |

after
""",
    ),
    pluginRuleTest(
        "good_table_at_start_of_file",
        enable_extensions="markdown-tables",
        disable_rules="md041",
        source_file_contents="""| abc | def |
| --- | --- |
| ghi | jkl |

after
""",
    ),
    pluginRuleTest(
        "good_table_at_end_of_file",
        enable_extensions="markdown-tables",
        source_file_contents="""# Top

| abc | def |
| --- | --- |
| ghi | jkl |
""",
    ),
    pluginRuleTest(
        "bad_no_blank_above",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md022,
        source_file_contents="""# Heading
| abc | def |
| --- | --- |
| ghi | jkl |
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)",
    ),
    pluginRuleTest(
        "bad_no_blank_below",
        enable_extensions="markdown-tables",
        disable_rules="md022,md025",
        source_file_contents="""# Top

| abc | def |
| --- | --- |
| ghi | jkl |
# Sub
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:5:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)",
    ),
    pluginRuleTest(
        "bad_no_blank_above_and_below",
        enable_extensions="markdown-tables",
        disable_rules="md022,md025",
        source_file_contents="""# A
| abc | def |
| --- | --- |
| ghi | jkl |
# B
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)
{temp_source_path}:4:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)""",
    ),
    pluginRuleTest(
        "good_in_block_quote_surrounded",
        enable_extensions="markdown-tables",
        source_file_contents="""> # Top
>
> | abc | def |
> | --- | --- |
> | ghi | jkl |
>
> after
""",
    ),
    pluginRuleTest(
        "good_in_block_quote_sole_content",
        enable_extensions="markdown-tables",
        disable_rules="md041",
        source_file_contents="""> | abc | def |
> | --- | --- |
> | ghi | jkl |
""",
    ),
    pluginRuleTest(
        "good_in_list_item_sole_content",
        enable_extensions="markdown-tables",
        disable_rules="md041",
        source_file_contents="""- | abc | def |
  | --- | --- |
  | ghi | jkl |
""",
    ),
]


@pytest.mark.rules
@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md058_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md058.
    """
    execute_scan_test(test, "md058")


@pytest.mark.rules
def test_md058_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md058",
        """
  ITEM               DESCRIPTION

  Id                 md058
  Name(s)            blanks-around-tables
  Short Description  Tables should be surrounded by blank lines
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md058.md
  """,
    )
    execute_query_configuration_test(config_test)
