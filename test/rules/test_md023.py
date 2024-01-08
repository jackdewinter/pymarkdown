"""
Module to provide tests related to the MD023 rule.
"""
import os
from test.rules.utils import (
    execute_fix_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md023") + os.sep

plugin_enable_this_rule = "MD023"

__plugin_disable_md005_md030_md032 = "MD005,md030,md032"
__plugin_disable_md009 = "md009"
__plugin_disable_md009_md022_md027 = "md009,md022,MD027"
__plugin_disable_md022_md030 = "MD022,md030"
__plugin_disable_md027 = "MD027"

scanTests = [
    pluginRuleTest(
        "good_proper_indent_atx",
        source_file_name=f"{source_path}proper_indent_atx.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "good_proper_indent_setext",
        source_file_name=f"{source_path}proper_indent_setext.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "bad_improper_indent_atx",
        source_file_name=f"{source_path}improper_indent_atx.md",
        enable_rules=plugin_enable_this_rule,
        source_file_contents="""Some text

  ## Heading 2

Some more text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)""",
        fix_expected_file_contents="""Some text

## Heading 2

Some more text
""",
    ),
    pluginRuleTest(
        "good_proper_indent_atx_in_list_item",
        source_file_name=f"{source_path}proper_indent_atx_in_list_item.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "bad_improper_indent_atx_in_list_item",
        source_file_name=f"{source_path}improper_indent_atx_in_list_item.md",
        disable_rules=__plugin_disable_md022_md030,
        enable_rules=plugin_enable_this_rule,
        source_file_contents="""1. Some text

1.  ## Heading 2
     ## Heading 2.1

1. Some more text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. Some text

1.  ## Heading 2
    ## Heading 2.1

1. Some more text
""",
    ),
    pluginRuleTest(
        "good_proper_indent_atx_in_block_quote",
        source_file_name=f"{source_path}proper_indent_atx_in_block_quote.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "bad_improper_indent_atx_in_block_quote",
        source_file_name=f"{source_path}improper_indent_atx_in_block_quote.md",
        disable_rules=__plugin_disable_md027,
        enable_rules=plugin_enable_this_rule,
        source_file_contents="""> Some text
>
>  ## Heading 2
>
> Some more text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""> Some text
>
> ## Heading 2
>
> Some more text
""",
    ),
    pluginRuleTest(
        "bad_improper_indent_setext_x",
        source_file_name=f"{source_path}improper_indent_setext.md",
        enable_rules=plugin_enable_this_rule,
        source_file_contents="""Some text

  Heading 2
  ---------

Some more text

Another Heading 2
  -----------------

more text

  Yet Another Heading 2
-----------------

more text

A Very
  Very
Very
  Long Heading
-----------------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:9:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:14:1: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:22:1: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""Some text

Heading 2
---------

Some more text

Another Heading 2
-----------------

more text

Yet Another Heading 2
-----------------

more text

A Very
Very
Very
Long Heading
-----------------
""",
    ),
    pluginRuleTest(
        "bad_improper_indent_setext_in_block_quote",
        source_file_name=f"{source_path}improper_indent_setext_in_block_quote.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md009_md022_md027,
        source_file_contents="""> Some text
>
>   Heading 2
>   ---------
>
> Some more text
>
> Another Heading 2
>   -----------------
>
> more text
>
>  Yet Another Heading 2
> -----------------
>
> more text
>
>   A Very 
>   Very1 
> Very2 
>   Long Heading
> -----------------
>
> Normal Heading
> ---------
>
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:9:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:14:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:22:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""> Some text
>
> Heading 2
> ---------
>
> Some more text
>
> Another Heading 2
> -----------------
>
> more text
>
> Yet Another Heading 2
> -----------------
>
> more text
>
> A Very 
> Very1 
> Very2 
> Long Heading
> -----------------
>
> Normal Heading
> ---------
>
""",
    ),
    pluginRuleTest(
        "good_proper_indent_setext_in_block_quote",
        source_file_contents="""> A Very\a
> Long Heading
> -----------------
""".replace(
            "\a", " "
        ),
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md009,
    ),
    pluginRuleTest(
        "bad_improper_indent_setext_in_list_item",
        source_file_name=f"{source_path}improper_indent_setext_in_list_item.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md005_md030_md032,
        source_file_contents="""- Some text

-   Heading 2 - md030 warns of too many spaces, md023 does not trigger
    ---------

- Some more text

- Another Heading 2 - md023 triggers
     -----------------

- more text

-  Yet Another Heading 2 - md030 warns of too many spaces, md023 does not trigger
  -----------------

- more text

- A Very1
   Very2
  Very3
   Long Heading  - md023 does trigger due to second and fourth lines
  -----------------

- Normal Heading
  ---------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:9:6: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:22:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""- Some text

-   Heading 2 - md030 warns of too many spaces, md023 does not trigger
    ---------

- Some more text

- Another Heading 2 - md023 triggers
  -----------------

- more text

-  Yet Another Heading 2 - md030 warns of too many spaces, md023 does not trigger
  -----------------

- more text

- A Very1
  Very2
  Very3
  Long Heading  - md023 does trigger due to second and fourth lines
  -----------------

- Normal Heading
  ---------
""",
    ),
    pluginRuleTest(
        "good_proper_indented_atx_after_emphasis",
        source_file_name=f"{source_path}improper_indented_atx_after_emphasis.md",
        enable_rules=plugin_enable_this_rule,
    ),
    pluginRuleTest(
        "good_proper_indent_setext_trailing_x",
        source_file_name=f"{source_path}proper_indent_setext_trailing.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md009,
    ),
    pluginRuleTest(
        "proper_indent_setext_trailing_first",
        source_file_name=f"{source_path}proper_indent_setext_trailing_first.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md009,
    ),
    pluginRuleTest(
        "proper_indent_setext_trailing_second",
        source_file_name=f"{source_path}proper_indent_setext_trailing_second.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md009,
    ),
    pluginRuleTest(
        "proper_indent_setext_trailing_third",
        source_file_name=f"{source_path}proper_indent_setext_trailing_third.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md009,
    ),
    pluginRuleTest(
        "proper_indent_setext_larger_trailing_middle",
        source_file_name=f"{source_path}proper_indent_setext_larger_trailing_middle.md",
        enable_rules=plugin_enable_this_rule,
        disable_rules=__plugin_disable_md009,
    ),
]

fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents:
        fixTests.append(i)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md023_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md023")


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md023_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)
