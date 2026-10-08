"""
Module to provide tests related to the MD058 rule.
"""

from test.rules.utils import (
    calculate_fix_tests,
    execute_fix_test,
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
        fix_expected_file_contents="""# Heading

| abc | def |
| --- | --- |
| ghi | jkl |
""",
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
        fix_expected_file_contents="""# Top

| abc | def |
| --- | --- |
| ghi | jkl |

# Sub
""",
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
        fix_expected_file_contents="""# A

| abc | def |
| --- | --- |
| ghi | jkl |

# B
""",
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
        "good_table_after_list",
        enable_extensions="markdown-tables",
        source_file_contents="""# Top

- first
- second

| abc | def |
| --- | --- |
| ghi | jkl |

after
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
    pluginRuleTest(
        "bad_two_tables",
        enable_extensions="markdown-tables",
        disable_rules="md022,md025",
        source_file_contents="""# A
| abc | def |
| --- | --- |
| ghi | jkl |
# B
| mno | pqr |
| --- | --- |
| stu | vwx |
# C
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)
{temp_source_path}:4:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)
{temp_source_path}:6:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)
{temp_source_path}:8:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)""",
        fix_expected_file_contents="""# A

| abc | def |
| --- | --- |
| ghi | jkl |

# B

| mno | pqr |
| --- | --- |
| stu | vwx |

# C
""",
    ),
    pluginRuleTest(
        "bad_below_thematic_break",
        enable_extensions="markdown-tables",
        source_file_contents="""# Top

| abc | def |
| --- | --- |
---
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)",
        fix_expected_file_contents="""# Top

| abc | def |
| --- | --- |

---
""",
    ),
    pluginRuleTest(
        "bad_below_fenced_md031_enabled",
        enable_extensions="markdown-tables",
        source_file_contents="""# Top

| abc | def |
| --- | --- |
```text
x
```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)
{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)""",
        fix_expected_file_contents="""# Top

| abc | def |
| --- | --- |

```text
x
```
""",
    ),
    pluginRuleTest(
        "bad_below_block_quote",
        enable_extensions="markdown-tables",
        source_file_contents="""# Top

| abc | def |
| --- | --- |
> quote
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)",
        fix_expected_file_contents="""# Top

| abc | def |
| --- | --- |

> quote
""",
    ),
    pluginRuleTest(
        "bad_below_list",
        enable_extensions="markdown-tables",
        disable_rules="md032",
        source_file_contents="""# Top

| abc | def |
| --- | --- |
- item
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)",
        fix_expected_file_contents="""# Top

| abc | def |
| --- | --- |

- item
""",
    ),
    pluginRuleTest(
        "good_pragma_suppressed",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md022,
        source_file_contents="""# A
<!-- pyml disable-next-line md058 -->
| abc | def |
| --- | --- |
""",
        fix_expected_return_code=0,
        fix_expected_output="",
        fix_expected_file_contents="""# A
<!-- pyml disable-next-line md058 -->
| abc | def |
| --- | --- |
""",
    ),
    pluginRuleTest(
        "bad_in_block_quote_not_fixed",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md022_md041,
        source_file_contents="""> # A
> | abc | def |
> | --- | --- |
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:3: MD058: Tables should be surrounded by blank lines (blanks-around-tables)",
        fix_expected_return_code=0,
        fix_expected_output="",
        fix_expected_file_contents="""> # A
> | abc | def |
> | --- | --- |
""",
    ),
    pluginRuleTest(
        "bad_in_list_item_not_fixed",
        enable_extensions="markdown-tables",
        disable_rules=__plugin_disable_md022_md041,
        source_file_contents="""- # A
  | abc | def |
  | --- | --- |
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:3: MD058: Tables should be surrounded by blank lines (blanks-around-tables)",
        fix_expected_return_code=0,
        fix_expected_output="",
        fix_expected_file_contents="""- # A
  | abc | def |
  | --- | --- |
""",
    ),
    pluginRuleTest(
        "bad_table_in_html_block_parse",
        enable_extensions="markdown-tables",
        disable_rules="md033,md041",
        notes="The parser places this table inside the HTML block, so the "
        + "token after the table is the HTML block's end token. Inserting a "
        + "blank line before an end token crashed MD012 in fix mode.",
        source_file_contents="""<div>
</div>
| a | b |
| - | - |
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)
{temp_source_path}:3:1: MD058: Tables should be surrounded by blank lines (blanks-around-tables)""",
        fix_expected_file_contents="""<div>
</div>

| a | b |
| - | - |
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
@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md058_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md058.
    """
    execute_fix_test(test)


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
