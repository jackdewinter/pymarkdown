"""
Module to provide tests related to the MD056 rule.
"""

from test.rules.utils import (
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

# MD041 (first-line-heading) fires on tables that start a file; it is unrelated
# to column counting, so it is disabled in these fixtures.
__plugin_disable_md041 = "md041"

scanTests = [
    pluginRuleTest(
        "good_equal_columns",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc | def |
| --- | --- |
| ghi | jkl |
""",
    ),
    pluginRuleTest(
        "bad_too_few",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc | def |
| --- | --- |
| bar |
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:1: MD056: Table column count [Expected: 2; Actual: 1; Too few cells, row will be missing data] (table-column-count)",
    ),
    pluginRuleTest(
        "bad_too_many",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc | def |
| --- | --- |
| bar | baz | boo |
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:1: MD056: Table column count [Expected: 2; Actual: 3; Too many cells, extra data will be missing] (table-column-count)",
    ),
    pluginRuleTest(
        "bad_mixed_too_few_and_too_many",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc | def |
| --- | --- |
| bar |
| bar | baz | boo |
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD056: Table column count [Expected: 2; Actual: 1; Too few cells, row will be missing data] (table-column-count)
{temp_source_path}:4:1: MD056: Table column count [Expected: 2; Actual: 3; Too many cells, extra data will be missing] (table-column-count)""",
    ),
    pluginRuleTest(
        "good_single_column",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc |
| --- |
| bar |
""",
    ),
    pluginRuleTest(
        "good_empty_cells",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc | def |
| --- | --- |
|  |  |
""",
    ),
    pluginRuleTest(
        "good_header_delimiter_mismatch_is_not_a_table",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc | def |
| --- |
| bar |
""",
    ),
    pluginRuleTest(
        "good_escaped_pipe_in_cell",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc | def |
| --- | --- |
| a \\| b | c |
""",
    ),
    pluginRuleTest(
        "bad_escaped_pipe_in_excess_cell",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc | def |
| --- | --- |
| c | d | e \\| f |
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:1: MD056: Table column count [Expected: 2; Actual: 3; Too many cells, extra data will be missing] (table-column-count)",
    ),
    pluginRuleTest(
        "good_in_block_quote",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""> | abc | def |
> | --- | --- |
> | bar | baz |
""",
    ),
    pluginRuleTest(
        "bad_in_block_quote",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""> | abc | def |
> | --- | --- |
> | bar |
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:3: MD056: Table column count [Expected: 2; Actual: 1; Too few cells, row will be missing data] (table-column-count)",
    ),
    pluginRuleTest(
        "good_in_list",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""- | abc | def |
  | --- | --- |
  | bar | baz |
""",
    ),
]


@pytest.mark.rules
@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md056_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md056.
    """
    execute_scan_test(test, "md056")


@pytest.mark.rules
def test_md056_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md056",
        """
  ITEM               DESCRIPTION

  Id                 md056
  Name(s)            table-column-count
  Short Description  Table column count
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md056.md
  """,
    )
    execute_query_configuration_test(config_test)
