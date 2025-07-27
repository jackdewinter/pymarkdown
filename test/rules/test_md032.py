"""
Module to provide tests related to the MD032 rule.
"""

import os
from test.rules.utils import (
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md032") + os.sep

scanTests = [
    pluginRuleTest(
        "good_list_surrounded",
        source_file_name=f"{source_path}good_list_surrounded.md",
        source_file_contents="""This is text and a blank line.

+ a list

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "good_list_at_start",
        source_file_name=f"{source_path}good_list_at_start.md",
        source_file_contents="""+ a list

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "good_list_at_end",
        source_file_name=f"{source_path}good_list_at_end.md",
        source_file_contents="""This is text and a blank line.

+ a list""",
        disable_rules="md047",
    ),
    pluginRuleTest(
        "bad_list_before",
        source_file_name=f"{source_path}bad_list_before.md",
        source_file_contents="""This is text.
+ a list

This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
""",
    ),
    pluginRuleTest(
        "bad_list_after",
        source_file_name=f"{source_path}bad_list_after.md",
        source_file_contents="""This is text and a blank line.

+ a list
# This is any non-text block
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
""",
        disable_rules="md022",
    ),
    pluginRuleTest(
        "bad_block_quote_list_block_quote",
        source_file_name=f"{source_path}bad_block_quote_list_block_quote.md",
        source_file_contents="""> this is a block quote
+ a list
+ still a list
> this is a block quote
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{temp_source_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
""",
    ),
    pluginRuleTest(
        "bad_other_list_list_other_list",
        source_file_name=f"{source_path}bad_other_list_list_other_list.md",
        source_file_contents="""1. this is a block quote
+ a list
+ still a list
1. this is a block quote
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{temp_source_path}:2:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{temp_source_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{temp_source_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
""",
    ),
    pluginRuleTest(
        "good_list_within_list_surrounded",
        source_file_name=f"{source_path}good_list_within_list_surrounded.md",
        source_file_contents="""This is text and a blank line.

+ a list
  + a sublist

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "good_list_within_block_quote_surrounded",
        source_file_name=f"{source_path}good_list_within_block_quote_surrounded.md",
        source_file_contents="""This is text and a blank line.

> + a list

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_list_within_block_quote_surrounded",
        source_file_name=f"{source_path}bad_list_within_block_quote_surrounded.md",
        source_file_contents="""This is text and a blank line.

> a block quote
> + a list

This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
""",
    ),
    pluginRuleTest(
        "good_nested_lists",
        source_file_name=f"{source_path}good_nested_lists.md",
        source_file_contents="""These are nested lists.

- some text at level 1
- some more text at level 1
  - some text at level 2
- yet more text at level 1
  - some text at level 2
""",
    ),
    pluginRuleTest(
        "good_list_levels_1_2_3_2_1",
        source_file_name=f"{source_path}good_list_levels_1_2_3_2_1.md",
        source_file_contents="""# title

- 1
  - 1.1
    - 1.1.1
  - 1.2
- 2
""",
    ),
    pluginRuleTest(
        "good_list_levels_1_2_3_space_1",
        source_file_name=f"{source_path}good_list_levels_1_2_3_space_1.md",
        source_file_contents="""# title

- 1
  - 1.1
    - 1.1.1

- 2
""",
    ),
    pluginRuleTest(
        "good_list_levels_1_2_3_1",
        source_file_name=f"{source_path}good_list_levels_1_2_3_1.md",
        source_file_contents="""# title

- 1
  - 1.1
    - 1.1.1
- 2
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote",
        source_file_name=f"{source_path}bad_fenced_block_in_list_in_block_quote.md",
        source_file_contents="""> + list
> ```block
> A code block
> ```
> 1. another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{temp_source_path}:5:3: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
""",
        disable_rules="md031",
    ),
    pluginRuleTest(  # https://github.github.com/gfm/#example-268
        "issue-1426-a-a",
        source_file_contents="""This is text and a blank line.

+ a list
This is any non-text block
""",
    ),
    pluginRuleTest(
        "issue-1426-a-b",
        source_file_contents="""This is text and a blank line.

This is any non-text block
+ a list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)""",
    ),
    pluginRuleTest(
        "issue-1426-b-a",
        source_file_contents="""This is text and a blank line.

+ a list
## This is any non-text block
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)""",
        disable_rules="md022",
    ),
    pluginRuleTest(
        "issue-1426-b-b",
        source_file_contents="""This is text and a blank line.

## This is any non-text block
+ a list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)""",
        disable_rules="md022",
    ),
    pluginRuleTest(
        "issue-1426-c-a",
        source_file_contents="""This is text and a blank line.

+ a list
------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)""",
        disable_rules="md022",
    ),
    pluginRuleTest(
        "issue-1426-c-b",
        source_file_contents="""This is text and a blank line.

------
+ a list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)""",
        disable_rules="md022",
    ),
    pluginRuleTest(
        "issue-1426-d-a",
        source_file_contents="""This is text and a blank line.

+ a list
```Markdown
# blah
```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)""",
        disable_rules="md022,md031",
    ),
    pluginRuleTest(
        "issue-1426-d-b",
        source_file_contents="""This is text and a blank line.

```Markdown
# blah
```
+ a list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)""",
        disable_rules="md022,md031",
    ),
    pluginRuleTest(  # https://github.github.com/gfm/#example-268 - just more spaces instead of less
        "issue-1426-e-a",
        source_file_contents="""This is text and a blank line.

+ a list
    blah
""",
        disable_rules="md022",
    ),
    pluginRuleTest(
        "issue-1426-e-b",
        source_file_contents="""This is text and a blank line.

    blah
+ a list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)""",
        disable_rules="md022",
    ),
    pluginRuleTest(  # https://github.github.com/gfm/#example-268 - variation
        "issue-1426-f-a",
        source_file_contents="""This is text and a blank line.

+ a list
[blah]: /url
""",
        disable_rules="md022",
    ),
    pluginRuleTest(
        "issue-1426-f-b",
        source_file_contents="""This is text and a blank line.

[blah]: /url
+ a list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)""",
        disable_rules="md022",
    ),
    pluginRuleTest(
        "issue-1426-g-a",
        source_file_contents="""This is text and a blank line.

+ a list
<!-- blah -->
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)""",
        disable_rules="md022",
    ),
    pluginRuleTest(
        "issue-1426-g-b",
        source_file_contents="""This is text and a blank line.

<!-- blah -->
+ a list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)""",
        disable_rules="md022",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md032_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md032")


def test_md032_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md032",
        """
  ITEM               DESCRIPTION

  Id                 md032
  Name(s)            blanks-around-lists
  Short Description  Lists should be surrounded by blank lines
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md032.md

""",
    )
    execute_query_configuration_test(config_test)
