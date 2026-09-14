"""
Module to provide tests related to the MD055 rule.
"""

import os
from test.rules.utils import (
    execute_configuration_test,
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginConfigErrorTest,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md055") + os.sep

# MD041 (first-line-heading) fires on tables that start a file; unrelated here.
__plugin_disable_md041 = "md041"

configTests = [
    pluginConfigErrorTest(
        "invalid_style_type",
        use_strict_config=True,
        set_args=["plugins.md055.style=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md055.style' must be of type 'str'.""",
    ),
    pluginConfigErrorTest(
        "invalid_style",
        use_strict_config=True,
        set_args=["plugins.md055.style=not-matching"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md055.style' is not valid: Allowable values: ['consistent', 'leading_and_trailing', 'leading_only', 'no_leading_or_trailing', 'trailing_only']""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_consistent_leading_and_trailing",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc | def |
| --- | --- |
| ghi | jkl |
""",
    ),
    pluginRuleTest(
        "good_consistent_no_leading_or_trailing",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""abc | def
--- | ---
ghi | jkl
""",
    ),
    pluginRuleTest(
        "bad_consistent_missing_trailing",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc | def |
| --- | --- |
| ghi | jkl
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:1: MD055: Table pipe style [Expected: leading_and_trailing; Actual: leading_only; Missing trailing pipe] (table-pipe-style)",
    ),
    pluginRuleTest(
        "bad_consistent_missing_leading",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc | def |
| --- | --- |
ghi | jkl |
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:1: MD055: Table pipe style [Expected: leading_and_trailing; Actual: trailing_only; Missing leading pipe] (table-pipe-style)",
    ),
    pluginRuleTest(
        "bad_delimiter_row_mismatch",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc | def |
--- | ---
| ghi | jkl |
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD055: Table pipe style [Expected: leading_and_trailing; Actual: no_leading_or_trailing; Missing leading pipe] (table-pipe-style)
{temp_source_path}:2:1: MD055: Table pipe style [Expected: leading_and_trailing; Actual: no_leading_or_trailing; Missing trailing pipe] (table-pipe-style)""",
    ),
    pluginRuleTest(
        "bad_explicit_no_leading_or_trailing",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        set_args=["plugins.md055.style=no_leading_or_trailing"],
        use_strict_config=True,
        source_file_contents="""| abc | def |
| --- | --- |
| ghi | jkl |
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD055: Table pipe style [Expected: no_leading_or_trailing; Actual: leading_and_trailing; Unexpected leading pipe] (table-pipe-style)
{temp_source_path}:1:1: MD055: Table pipe style [Expected: no_leading_or_trailing; Actual: leading_and_trailing; Unexpected trailing pipe] (table-pipe-style)
{temp_source_path}:2:1: MD055: Table pipe style [Expected: no_leading_or_trailing; Actual: leading_and_trailing; Unexpected leading pipe] (table-pipe-style)
{temp_source_path}:2:1: MD055: Table pipe style [Expected: no_leading_or_trailing; Actual: leading_and_trailing; Unexpected trailing pipe] (table-pipe-style)
{temp_source_path}:3:1: MD055: Table pipe style [Expected: no_leading_or_trailing; Actual: leading_and_trailing; Unexpected leading pipe] (table-pipe-style)
{temp_source_path}:3:1: MD055: Table pipe style [Expected: no_leading_or_trailing; Actual: leading_and_trailing; Unexpected trailing pipe] (table-pipe-style)""",
    ),
    pluginRuleTest(
        "good_explicit_leading_only",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        set_args=["plugins.md055.style=leading_only"],
        use_strict_config=True,
        source_file_contents="""| abc | def
| --- | ---
| ghi | jkl
""",
    ),
    pluginRuleTest(
        "good_single_column",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| abc |
| --- |
| ghi |
""",
    ),
    pluginRuleTest(
        "good_trailing_whitespace_after_pipe",
        enable_extensions="markdown-tables",
        disable_rules="md041,md009",
        source_file_contents="""| abc | def |\a
| --- | --- |\a
| ghi | jkl |\a
""".replace("\a", " "),
    ),
    pluginRuleTest(
        "good_escaped_pipe_in_cell",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""| a \\| b | def |
| --- | --- |
| ghi | jkl |
""",
    ),
    pluginRuleTest(
        "bad_overfull_row_missing_trailing",
        enable_extensions="markdown-tables",
        disable_rules="md041,md056,md058",
        source_file_contents="""| a | b |
| --- | --- |
| 1 | 2 | 3 | 4
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:1: MD055: Table pipe style [Expected: leading_and_trailing; Actual: leading_only; Missing trailing pipe] (table-pipe-style)",
    ),
    pluginRuleTest(
        "good_overfull_row_with_trailing",
        enable_extensions="markdown-tables",
        disable_rules="md041,md056,md058",
        source_file_contents="""| a | b |
| --- | --- |
| 1 | 2 | 3 | 4 |
""",
    ),
    pluginRuleTest(
        "bad_in_block_quote",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md041,
        source_file_contents="""> | abc | def |
> | --- | --- |
> | ghi | jkl
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:3: MD055: Table pipe style [Expected: leading_and_trailing; Actual: leading_only; Missing trailing pipe] (table-pipe-style)",
    ),
]


@pytest.mark.rules
@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md055_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md055.
    """
    execute_scan_test(test, "md055")


@pytest.mark.rules
@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md055_config(test: pluginConfigErrorTest) -> None:
    """
    Execute a parameterized configuration error test for plugin md055.
    """
    execute_configuration_test(test, f"{source_path}good_table.md")


@pytest.mark.rules
def test_md055_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md055",
        """
  ITEM               DESCRIPTION

  Id                 md055
  Name(s)            table-pipe-style
  Short Description  Table pipe style
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md055.md


  CONFIGURATION ITEM  TYPE    VALUE

  style               string  "consistent"

""",
    )
    execute_query_configuration_test(config_test)
