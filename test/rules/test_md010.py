"""
Module to provide tests related to the MD010 rule.
"""

import os
from test.rules.utils import (
    execute_configuration_test,
    execute_fix_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginConfigErrorTest,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md010") + os.sep

__plugin_disable_md022 = "md022"
__plugin_disable_md030 = "md030"
__plugin_disable_md031_md040 = "md031,md040"
__plugin_disable_md047 = "MD047"

configTests = [
    pluginConfigErrorTest(
        "invalid_code_blocks",
        use_strict_config=True,
        set_args=["plugins.md010.code_blocks=bad"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md010.code_blocks' must be of type 'bool'.""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_simple_text_no_tab",
        source_file_name=f"{source_path}good_simple_text_no_tab.md",
    ),
    pluginRuleTest(
        "bad_simple_text_with_tab",
        source_file_name=f"{source_path}bad_simple_text_with_tab.md",
        source_file_contents="""before-tab\tafter-tab
before-tab\tafter-tab
before-tab\tafter-tab\tafter-another
a\tbb\tccc\tddd
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
{temp_source_path}:2:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
{temp_source_path}:3:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
{temp_source_path}:3:22: MD010: Hard tabs [Column: 22] (no-hard-tabs)
{temp_source_path}:4:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{temp_source_path}:4:7: MD010: Hard tabs [Column: 7] (no-hard-tabs)
{temp_source_path}:4:12: MD010: Hard tabs [Column: 12] (no-hard-tabs)
""",
        fix_expected_file_contents="""before-tab  after-tab
before-tab  after-tab
before-tab  after-tab   after-another
a   bb  ccc ddd
""",
    ),
    pluginRuleTest(
        "bad_simple_text_with_tab_fix_and_debug",
        source_file_name=f"{source_path}bad_simple_text_with_tab.md",
        use_fix_debug=True,
        source_file_contents="""before-tab\tafter-tab
before-tab\tafter-tab
before-tab\tafter-tab\tafter-another
a\tbb\tccc\tddd
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
{temp_source_path}:2:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
{temp_source_path}:3:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
{temp_source_path}:3:22: MD010: Hard tabs [Column: 22] (no-hard-tabs)
{temp_source_path}:4:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{temp_source_path}:4:7: MD010: Hard tabs [Column: 7] (no-hard-tabs)
{temp_source_path}:4:12: MD010: Hard tabs [Column: 12] (no-hard-tabs)""",
        fix_expected_file_contents="""before-tab  after-tab
before-tab  after-tab
before-tab  after-tab   after-another
a   bb  ccc ddd
""",
        fix_expected_output="""md009-before:before-tab\\tafter-tab:
md010-before:before-tab\\tafter-tab:
md010-after :before-tab  after-tab:
md047-before:before-tab  after-tab:
nl-ltw:before-tab  after-tab\\n:
md009-before:before-tab\\tafter-tab:
md010-before:before-tab\\tafter-tab:
md010-after :before-tab  after-tab:
md047-before:before-tab  after-tab:
nl-ltw:before-tab  after-tab\\n:
md009-before:before-tab\\tafter-tab\\tafter-another:
md010-before:before-tab\\tafter-tab\\tafter-another:
md010-after :before-tab  after-tab   after-another:
md047-before:before-tab  after-tab   after-another:
nl-ltw:before-tab  after-tab   after-another\\n:
md009-before:a\\tbb\\tccc\\tddd:
md010-before:a\\tbb\\tccc\\tddd:
md010-after :a   bb  ccc ddd:
md047-before:a   bb  ccc ddd:
nl-ltw:a   bb  ccc ddd\\n:
md009-before::
md010-before::
md047-before::
was_newline_added_at_end_of_file=True
fixed:a   bb  ccc ddd\\n:
is_line_empty=True
was_modified=True
nl-ltw::
FixLineRecord(source='next_line', line_number=1, plugin_id='md010')
FixLineRecord(source='next_line', line_number=2, plugin_id='md010')
FixLineRecord(source='next_line', line_number=3, plugin_id='md010')
FixLineRecord(source='next_line', line_number=4, plugin_id='md010')
Fixed: {temp_source_path}""",
    ),
    pluginRuleTest(
        "bad_simple_text_with_tabs_in_code_block_with_end_line",
        source_file_name=f"{source_path}bad_simple_text_with_tabs_in_code_block.md",
        source_file_contents="""This is a code block

```text
code	block
```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD010: Hard tabs [Column: 5] (no-hard-tabs)
""",
        fix_expected_file_contents="""This is a code block

```text
code    block
```
""",
    ),
    pluginRuleTest(
        "bad_simple_text_with_tabs_in_code_block_no_end_line",
        source_file_name=f"{source_path}bad_simple_text_with_tabs_in_code_block_no_end_line.md",
        disable_rules=__plugin_disable_md047,
        source_file_contents="""This is a code block

```text
code	block
```""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD010: Hard tabs [Column: 5] (no-hard-tabs)
""",
        fix_expected_file_contents="""This is a code block

```text
code    block
```""",
    ),
    pluginRuleTest(
        "good_simple_text_with_tabs_in_code_block_turned_off",
        source_file_name=f"{source_path}bad_simple_text_with_tabs_in_code_block.md",
        use_strict_config=True,
        set_args=["plugins.md010.code_blocks=$!false"],
        source_file_contents="""This is a code block

```text
code	block
```
""",
    ),
    pluginRuleTest(
        "bad_in_block_quotes_fall_off_after_fenced_open",
        source_file_name=f"{source_path}bad_block_quote_fall_off_after_fenced_open.md",
        disable_rules=__plugin_disable_md031_md040,
        source_file_contents="""> this is text
>
> ```text	abc
  this is not a tab in a code	block
  ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)
{temp_source_path}:4:30: MD010: Hard tabs [Column: 30] (no-hard-tabs)
""",
        fix_expected_file_contents="""> this is text
>
> ```text   abc
  this is not a tab in a code   block
  ```
""",
    ),
    pluginRuleTest(
        "bad_in_bad_block_quote_fall_off_after_fenced_open_and_text",
        source_file_name=f"{source_path}bad_block_quote_fall_off_after_fenced_open_and_text.md",
        disable_rules=__plugin_disable_md031_md040,
        source_file_contents="""> this is text
>
> ```text	abc
> this is a tab in a code	block
  ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)
{temp_source_path}:4:26: MD010: Hard tabs [Column: 26] (no-hard-tabs)
""",
        fix_expected_file_contents="""> this is text
>
> ```text   abc
> this is a tab in a code   block
  ```
""",
    ),
    pluginRuleTest(
        "bad_in_bad_block_quote_fall_off_after_fenced_open_and_text_and_close",
        source_file_name=f"{source_path}bad_block_quote_fall_off_after_fenced_open_and_text_and_close.md",
        source_file_contents="""> this is text
>
> ```text	abc
> this is a tab in a code	block
> ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)
{temp_source_path}:4:26: MD010: Hard tabs [Column: 26] (no-hard-tabs)
""",
        fix_expected_file_contents="""> this is text
>
> ```text   abc
> this is a tab in a code   block
> ```
""",
    ),
    pluginRuleTest(
        "bad_unordered_list_fall_off_after_fenced_open",
        source_file_name=f"{source_path}bad_unordered_list_fall_off_after_fenced_open.md",
        disable_rules=__plugin_disable_md031_md040,
        source_file_contents="""+ this is text

  ```text	def
+ this contains	a tab
  ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)
{temp_source_path}:4:16: MD010: Hard tabs [Column: 16] (no-hard-tabs)
""",
        fix_expected_file_contents="""+ this is text

  ```text   def
+ this contains a tab
  ```
""",
    ),
    pluginRuleTest(
        "bad_unordered_list_fall_off_after_fenced_open_and_text",
        source_file_name=f"{source_path}bad_unordered_list_fall_off_after_fenced_open_and_text.md",
        disable_rules=__plugin_disable_md031_md040,
        source_file_contents="""+ this is text

  ```text	def
  this contains	a tab
+ ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)
{temp_source_path}:4:16: MD010: Hard tabs [Column: 16] (no-hard-tabs)
""",
        fix_expected_file_contents="""+ this is text

  ```text   def
  this contains a tab
+ ```
""",
    ),
    pluginRuleTest(
        "bad_unordered_list_fall_off_after_fenced_open_and_text_and_close",
        source_file_name=f"{source_path}bad_unordered_list_fall_off_after_fenced_open_and_text_and_close.md",
        source_file_contents="""- this is text

  ```text	def
  this contains	a tab
  ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)
{temp_source_path}:4:16: MD010: Hard tabs [Column: 16] (no-hard-tabs)
""",
        fix_expected_file_contents="""- this is text

  ```text   def
  this contains a tab
  ```
""",
    ),
    pluginRuleTest(
        "bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_code_blocks_off",
        source_file_name=f"{source_path}bad_unordered_list_fall_off_after_fenced_open_and_text_and_close.md",
        set_args=["plugins.md010.code_blocks=$!false"],
        use_strict_config=True,
        source_file_contents="""- this is text

  ```text	def
  this contains	a tab
  ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:10: MD010: Hard tabs [Column: 10] (no-hard-tabs)
""",
        fix_expected_file_contents="""- this is text

  ```text   def
  this contains\ta tab
  ```
""",
    ),
    pluginRuleTest(
        "bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_space_indent",
        source_file_name=f"{source_path}bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_space_indent.md",
        disable_rules=__plugin_disable_md030,
        source_file_contents="""-   this is text

    ```text	def
    this contains	a tab
    ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:12: MD010: Hard tabs [Column: 12] (no-hard-tabs)
{temp_source_path}:4:18: MD010: Hard tabs [Column: 18] (no-hard-tabs)
""",
        fix_expected_file_contents="""-   this is text

    ```text def
    this contains   a tab
    ```
""",
    ),
    pluginRuleTest(
        "bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_tab_indent",
        source_file_name=f"{source_path}bad_unordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_tab_indent.md",
        disable_rules=__plugin_disable_md030,
        source_file_contents="""-\tthis is text

\t```text\tdef
\tthis contains\ta tab
\t```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{temp_source_path}:3:1: MD010: Hard tabs [Column: 1] (no-hard-tabs)
{temp_source_path}:3:12: MD010: Hard tabs [Column: 12] (no-hard-tabs)
{temp_source_path}:4:1: MD010: Hard tabs [Column: 1] (no-hard-tabs)
{temp_source_path}:4:18: MD010: Hard tabs [Column: 18] (no-hard-tabs)
{temp_source_path}:5:1: MD010: Hard tabs [Column: 1] (no-hard-tabs)
""",
        fix_expected_file_contents="""-   this is text

    ```text def
    this contains   a tab
    ```
""",
    ),
    pluginRuleTest(
        "bad_ordered_list_fall_off_after_fenced_open",
        source_file_name=f"{source_path}bad_ordered_list_fall_off_after_fenced_open.md",
        disable_rules=__plugin_disable_md031_md040,
        source_file_contents="""1. this is text

   ```text	def
1. this contains	a tab
   ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
{temp_source_path}:4:17: MD010: Hard tabs [Column: 17] (no-hard-tabs)
""",
        fix_expected_file_contents="""1. this is text

   ```text  def
1. this contains    a tab
   ```
""",
    ),
    pluginRuleTest(
        "bad_ordered_list_fall_off_after_fenced_open_and_text",
        source_file_name=f"{source_path}bad_ordered_list_fall_off_after_fenced_open_and_text.md",
        disable_rules=__plugin_disable_md031_md040,
        source_file_contents="""1. this is text

   ```text	def
   this contains	a tab
1. ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
{temp_source_path}:4:17: MD010: Hard tabs [Column: 17] (no-hard-tabs)
""",
        fix_expected_file_contents="""1. this is text

   ```text  def
   this contains    a tab
1. ```
""",
    ),
    pluginRuleTest(
        "bad_ordered_list_fall_off_after_fenced_open_and_text_and_close",
        source_file_name=f"{source_path}bad_ordered_list_fall_off_after_fenced_open_and_text_and_close.md",
        source_file_contents="""1. this is text

   ```text	def
   this contains	a tab
   ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
{temp_source_path}:4:17: MD010: Hard tabs [Column: 17] (no-hard-tabs)
""",
        fix_expected_file_contents="""1. this is text

   ```text  def
   this contains    a tab
   ```
""",
    ),
    pluginRuleTest(
        "bad_ordered_list_fall_off_after_fenced_open_and_text_and_close_with_code_blocks_off",
        source_file_name=f"{source_path}bad_ordered_list_fall_off_after_fenced_open_and_text_and_close.md",
        use_strict_config=True,
        set_args=["plugins.md010.code_blocks=$!false"],
        source_file_contents="""1. this is text

   ```text	def
   this contains	a tab
   ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
""",
        fix_expected_file_contents="""1. this is text

   ```text  def
   this contains	a tab
   ```
""",
    ),
    pluginRuleTest(
        "bad_ordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_space_indent",
        source_file_name=f"{source_path}bad_ordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_space_indent.md",
        disable_rules=__plugin_disable_md030,
        source_file_contents="""1.  this is text

    ```text	def
    this contains	a tab
    ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:12: MD010: Hard tabs [Column: 12] (no-hard-tabs)
{temp_source_path}:4:18: MD010: Hard tabs [Column: 18] (no-hard-tabs)
""",
        fix_expected_file_contents="""1.  this is text

    ```text def
    this contains   a tab
    ```
""",
    ),
    pluginRuleTest(
        "bad_ordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_tab_indent",
        source_file_name=f"{source_path}bad_ordered_list_fall_off_after_fenced_open_and_text_and_close_with_extra_tab_indent.md",
        disable_rules=__plugin_disable_md030,
        source_file_contents="""1.\tthis is text

\t```text\tdef
\tthis contains\ta tab
\t```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD010: Hard tabs [Column: 3] (no-hard-tabs)
{temp_source_path}:3:1: MD010: Hard tabs [Column: 1] (no-hard-tabs)
{temp_source_path}:3:12: MD010: Hard tabs [Column: 12] (no-hard-tabs)
{temp_source_path}:4:1: MD010: Hard tabs [Column: 1] (no-hard-tabs)
{temp_source_path}:4:18: MD010: Hard tabs [Column: 18] (no-hard-tabs)
{temp_source_path}:5:1: MD010: Hard tabs [Column: 1] (no-hard-tabs)
""",
        fix_expected_file_contents="""1.  this is text

    ```text def
    this contains   a tab
    ```
""",
    ),
    pluginRuleTest(
        "mix_md010_md019",
        source_file_contents="""#\tHeading 1

a line of text\twith\ttabs
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{temp_source_path}:3:15: MD010: Hard tabs [Column: 15] (no-hard-tabs)
{temp_source_path}:3:21: MD010: Hard tabs [Column: 21] (no-hard-tabs)
""",
        fix_expected_file_contents="""# Heading 1

a line of text  with    tabs
""",
    ),
    pluginRuleTest(
        "mix_md010_md021",
        source_file_contents="""#  Heading\t1  #
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)
{temp_source_path}:1:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
""",
        fix_expected_file_contents="""# Heading  1 #
""",
    ),
    pluginRuleTest(
        "mix_md010_md030",
        source_file_contents="""*  # list item\t1
*  ## list\titem 2

   paragraph
*  ## list\titem 3
""",
        disable_rules=__plugin_disable_md022,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:1:15: MD010: Hard tabs [Column: 15] (no-hard-tabs)
{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
{temp_source_path}:5:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:5:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
""",
        fix_expected_file_contents="""* # list item  1
* ## list  item 2

  paragraph
* ## list  item 3
""",
    ),
    pluginRuleTest(
        "mix_md010_md030_with_tabs",
        source_file_contents="""*\t#\tlist\titem\t1
\tlist\t1\ttext
*  ## list\titem 2

   paragraph
*  ## list\titem 3
""",
        disable_rules=__plugin_disable_md022,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 3] (list-marker-space)
{temp_source_path}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{temp_source_path}:1:5: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:1:6: MD010: Hard tabs [Column: 6] (no-hard-tabs)
{temp_source_path}:1:13: MD010: Hard tabs [Column: 13] (no-hard-tabs)
{temp_source_path}:1:21: MD010: Hard tabs [Column: 21] (no-hard-tabs)
{temp_source_path}:2:1: MD010: Hard tabs [Column: 1] (no-hard-tabs)
{temp_source_path}:2:9: MD010: Hard tabs [Column: 9] (no-hard-tabs)
{temp_source_path}:2:14: MD010: Hard tabs [Column: 14] (no-hard-tabs)
{temp_source_path}:3:1: MD005: Inconsistent indentation for list items at the same level [Expected: 2; Actual: 0] (list-indent)
{temp_source_path}:3:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:3:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
{temp_source_path}:6:1: MD005: Inconsistent indentation for list items at the same level [Expected: 2; Actual: 0] (list-indent)
{temp_source_path}:6:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:6:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
""",
        fix_expected_file_contents="""* # list    item    1
   list    1   text
* ## list  item 2

  paragraph
* ## list  item 3
""",
    ),
    pluginRuleTest(
        "mix_md010_md047",
        source_file_contents="""item\t1""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD010: Hard tabs [Column: 5] (no-hard-tabs)
{temp_source_path}:1:6: MD047: Each file should end with a single newline character. (single-trailing-newline)
""",
        fix_expected_file_contents="""item    1
""",
    ),
    pluginRuleTest(
        "issue-1015-positive",
        source_file_name=f"{source_path}issue-1015.md",
        source_file_contents="""Consider this code:
    code block here

- Consider this code:
	code block here""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD010: Hard tabs [Column: 1] (no-hard-tabs)
{temp_source_path}:5:16: MD047: Each file should end with a single newline character. (single-trailing-newline)
""",
    ),
    pluginRuleTest(
        "issue-1015-negative",
        source_file_name=f"{source_path}issue-1015.md",
        source_file_contents="""Consider this code:
    code block here

- Consider this code:
	code block here""",
        disable_rules="md010",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:16: MD047: Each file should end with a single newline character. (single-trailing-newline)
""",
    ),
]
fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents:
        fixTests.append(i)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md010_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md010")


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md010_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md010_config(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(
        test, f"{source_path}bad_simple_text_with_tabs_in_code_block.md"
    )
