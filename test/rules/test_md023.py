"""
Module to provide tests related to the MD023 rule.
"""

import os
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
        scan_expected_output="""{temp_source_path}:3:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:8:1: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:13:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:18:1: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
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
        scan_expected_output="""{temp_source_path}:3:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:8:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:13:4: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:18:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
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
        scan_expected_output="""{temp_source_path}:8:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:18:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
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
    pluginRuleTest(
        "bad_atx_block_quote_with_tab",
        source_file_contents=""">\t# heading 1
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""> # heading 1
""",
    ),
    pluginRuleTest(
        "bad_setext_both_block_quote_with_tab",
        source_file_contents=""">\theading 1
>\t----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""> heading 1
> ----
""",
    ),
    pluginRuleTest(
        "bad_setext_one_block_quote_with_tab",
        source_file_contents=""">\theading 1
> ----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""> heading 1
> ----
""",
    ),
    pluginRuleTest(
        "bad_setext_two_block_quote_with_tab",
        source_file_contents="""> heading 1
>\t----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""> heading 1
> ----
""",
    ),
    pluginRuleTest(
        "bad_setext_four_block_quote_with_tab",
        source_file_contents=""">\theading 1
>\tpart 2
>\tpart 3
>\t----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""> heading 1
> part 2
> part 3
> ----
""",
    ),
    pluginRuleTest(
        "bad_atx_unordered_list_with_tab",
        source_file_contents="""+\t# heading 1
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md030",
    ),
    pluginRuleTest(
        "bad_atx_unordered_list_with_tab_second",
        source_file_contents="""+ # heading 1
\t# heading 2
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md022,md025,md027,md030",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""+ # heading 1
  # heading 2
""",
    ),
    pluginRuleTest(
        "bad_atx_unordered_list_with_tab_third",
        source_file_contents="""+ # heading 1
  just some text
\t# heading 2
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md022,md025,md027,md030",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""+ # heading 1
  just some text
  # heading 2
""",
    ),
    pluginRuleTest(
        "bad_atx_unordered_list_new_list_item_with_tab_second",
        source_file_contents="""+ # heading 1
  # heading 2
+ # heading 1
\t# heading 2
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md022,md024,md025,md027,md030",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""+ # heading 1
  # heading 2
+ # heading 1
  # heading 2
""",
    ),
    pluginRuleTest(
        "bad_atx_unordered_list_new_list_item_with_tab_third",
        source_file_contents="""+ # heading 1
  # heading 2
+ # heading 1
  # heading 2
\t# heading 3
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md022,md024,md025,md027,md030",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""+ # heading 1
  # heading 2
+ # heading 1
  # heading 2
  # heading 3
""",
    ),
    pluginRuleTest(
        "bad_setext_both_unordered_list_with_tab",
        source_file_contents="""+\theading 1
\t----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md030",
    ),
    pluginRuleTest(
        "bad_setext_one_unordered_list_with_tab",
        source_file_contents="""+\theading 1
  ----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md030,md032",
    ),
    pluginRuleTest(
        "bad_setext_two_unordered_list_with_tab",
        source_file_contents="""+ heading 1
\t----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""+ heading 1
  ----
""",
    ),
    pluginRuleTest(
        "bad_setext_four_unordered_list_with_tab",
        source_file_contents="""+ heading 1
  part 2
\tpart 3
  ----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""+ heading 1
  part 2
  part 3
  ----
""",
    ),
    pluginRuleTest(
        "bad_setext_four_unordered_list_with_tab_13",
        source_file_contents="""
+ heading 1\a\a
\tpart 2
\tpart 3
\t----
+ heading 1
  part 2
  part 3
  ---
+ heading 1
  part 2
  part 3
  ---
""".replace(
            "\a", " "
        ),
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md022,md024",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""
+ heading 1\a\a
  part 2
  part 3
  ----
+ heading 1
  part 2
  part 3
  ---
+ heading 1
  part 2
  part 3
  ---
""".replace(
            "\a", " "
        ),
    ),
    # dependent on test_extra_040b
    #     pluginRuleTest(
    #         "bad_setext_four_unordered_list_with_tab_codespan_13",
    #         source_file_contents="""
    # + heading `1` abc
    # \tpart 2
    # \tpart 3
    # \t----
    # + heading 1
    #   part 2
    #   part 3
    #   ---
    # + heading 1
    #   part 2
    #   part 3
    #   ---
    # """.replace("\a", " "),
    #         enable_rules=plugin_enable_this_rule,
    #         disable_rules="md010,md027,md022,md024",
    #         scan_expected_return_code=1,
    #         scan_expected_output="""{temp_source_path}:5:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
    # """,
    #         fix_expected_file_contents="""
    # + heading 1 abc
    #   part 2
    #   part 3
    #   ----
    # + heading 1
    #   part 2
    #   part 3
    #   ---
    # + heading 1
    #   part 2
    #   part 3
    #   ---
    # """.replace("\a", " "),
    #     ),
    pluginRuleTest(
        "bad_setext_four_unordered_list_with_tab_23",
        source_file_contents="""
+ heading 1
  part 2
  part 3
  ----
+ heading 2\a\a
\tpart 2
\tpart 3
\t---
+ heading 1
  part 2
  part 3
  ---""".replace(
            "\a", " "
        ),
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md022,md024,md047",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""
+ heading 1
  part 2
  part 3
  ----
+ heading 2\a\a
  part 2
  part 3
  ---
+ heading 1
  part 2
  part 3
  ---""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_setext_four_unordered_list_with_tab_33",
        source_file_contents="""
+ heading 1
  part 2
  part 3
  ---
+ heading 1
  part 2
  part 3
  ---
+ heading 2\a\a
\tpart 2
\tpart 3
\t----
""".replace(
            "\a", " "
        ),
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md022,md024",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:10:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""
+ heading 1
  part 2
  part 3
  ---
+ heading 1
  part 2
  part 3
  ---
+ heading 2\a\a
  part 2
  part 3
  ----
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_setext_four_unordered_unordered_list_with_tab",
        source_file_contents="""+ heading 0
  + heading 1
\tpart 2
\tpart 3
\t----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md022",
    ),
    pluginRuleTest(
        "bad_setext_four_unordered_ordered_list_with_tab",
        source_file_contents="""+ heading 0
  1. heading 1
\t\tpart 2
\t\tpart 3
\t\t----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md022",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:6: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""+ heading 0
  1. heading 1
     part 2
     part 3
     ----
""",
    ),
    pluginRuleTest(
        "bad_setext_four_ordered_ordered_list_with_tab",
        source_file_contents="""1. heading 0
   1. heading 1
\t\tpart 2
\t\tpart 3
\t\t----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md022",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. heading 0
   1. heading 1
      part 2
      part 3
      ----
""",
    ),
    pluginRuleTest(
        "bad_setext_four_ordered_unordered_list_with_tab",
        source_file_contents="""1. heading 0
   + heading 1
\t\tpart 2
\t\tpart 3
\t\t----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md022",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:6: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. heading 0
   + heading 1
     part 2
     part 3
     ----
""",
    ),
    pluginRuleTest(
        "bad_atx_ordered_list_with_tab",
        source_file_contents="""1.\t# heading 1
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md030",
    ),
    pluginRuleTest(
        "bad_atx_ordered_list_with_tab_second",
        source_file_contents="""1. # heading 1
\t# heading 2
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md022,md025,md027,md030",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. # heading 1
   # heading 2
""",
    ),
    pluginRuleTest(
        "bad_atx_ordered_list_with_tab_third",
        source_file_contents="""1. # heading 1
   just some text
\t# heading 2
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md022,md025,md027,md030",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. # heading 1
   just some text
   # heading 2
""",
    ),
    pluginRuleTest(
        "bad_atx_ordered_list_new_list_item_with_tab_second",
        source_file_contents="""1. # heading 1
   # heading 2
1. # heading 1
\t# heading 2
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md022,md024,md025,md027,md030",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. # heading 1
   # heading 2
1. # heading 1
   # heading 2
""",
    ),
    pluginRuleTest(
        "bad_atx_ordered_list_new_list_item_with_tab_third",
        source_file_contents="""1. # heading 1
   # heading 2
1. # heading 1
   # heading 2
\t# heading 3
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md022,md024,md025,md027,md030",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. # heading 1
   # heading 2
1. # heading 1
   # heading 2
   # heading 3
""",
    ),
    pluginRuleTest(
        "bad_setext_both_ordered_list_with_tab",
        source_file_contents="""1.\theading 1
\t----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md030",
    ),
    pluginRuleTest(
        "bad_setext_one_ordered_list_with_tab",
        source_file_contents="""1.\theading 1
    ----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md030,md032",
    ),
    pluginRuleTest(
        "bad_setext_two_ordered_list_with_tab",
        source_file_contents="""1. heading 1
\t----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. heading 1
   ----
""",
    ),
    pluginRuleTest(
        "bad_setext_four_ordered_list_with_tab",
        source_file_contents="""1. heading 1
\tpart 2
\tpart 3
\t----
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. heading 1
   part 2
   part 3
   ----
""",
    ),
    pluginRuleTest(
        "bad_setext_four_ordered_list_with_tab_and_hard_break",
        source_file_contents="""1. heading 1
\tpart 2
   part 3\a\a
\tpart 4
   part 5\a\a
\tpart 6
   ----
""".replace(
            "\a", " "
        ),
        enable_rules=plugin_enable_this_rule,
        disable_rules="md009,md010,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. heading 1
   part 2
   part 3\a\a
   part 4
   part 5\a\a
   part 6
   ----
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_setext_four_ordered_list_with_tab_and_emphasis",
        source_file_contents="""1. heading 1
\tpart 2
   part *3*\a
\tpart 4
   ----
""".replace(
            "\a", " "
        ),
        enable_rules=plugin_enable_this_rule,
        disable_rules="md009,md010,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. heading 1
   part 2
   part *3*\a
   part 4
   ----
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_setext_four_ordered_list_with_tab_and_double_emphasis_1",
        source_file_contents="""1. heading 1
\tpart 2
   part *3*\a
   part *4*\a
\tpart 6
   ----
""".replace(
            "\a", " "
        ),
        enable_rules=plugin_enable_this_rule,
        disable_rules="md009,md010,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. heading 1
   part 2
   part *3*\a
   part *4*\a
   part 6
   ----
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_setext_four_ordered_list_with_tab_and_double_emphasis_2",
        source_file_contents="""1. heading 1
\tpart 2
   part *3*\a
\tpart 4
   part *5*\a
\tpart 6
   ----
""".replace(
            "\a", " "
        ),
        enable_rules=plugin_enable_this_rule,
        disable_rules="md009,md010,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. heading 1
   part 2
   part *3*\a
   part 4
   part *5*\a
   part 6
   ----
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_setext_four_ordered_list_with_tab_13",
        source_file_contents="""
1. heading 2\a\a
\tpart 2
\tpart 3
\t----
1. heading 1
   part 2
   part 3
   ---
1. heading 1
   part 2
   part 3
   ---
""".replace(
            "\a", " "
        ),
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md022,md024",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:4: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""
1. heading 2\a\a
   part 2
   part 3
   ----
1. heading 1
   part 2
   part 3
   ---
1. heading 1
   part 2
   part 3
   ---
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_setext_four_ordered_list_with_tab_23",
        source_file_contents="""
1. heading 1
   part 2
   part 3
   ---
1. heading 2\a\a
\tpart 2
\tpart 3
\t----
1. heading 1
   part 2
   part 3
   ---""".replace(
            "\a", " "
        ),
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md022,md024,md047",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:4: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""
1. heading 1
   part 2
   part 3
   ---
1. heading 2\a\a
   part 2
   part 3
   ----
1. heading 1
   part 2
   part 3
   ---""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_setext_four_ordered_list_with_tab_33",
        source_file_contents="""
1. heading 1
   part 2
   part 3
   ---
1. heading 1
   part 2
   part 3
   ---
1. heading 2\a\a
\tpart 2
\tpart 3
\t----
""".replace(
            "\a", " "
        ),
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md027,md022,md024",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:10:4: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""
1. heading 1
   part 2
   part 3
   ---
1. heading 1
   part 2
   part 3
   ---
1. heading 2\a\a
   part 2
   part 3
   ----
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_atx_unordered_unordered_with_tab",
        source_file_contents="""+ # heading 1
   + # heading 2
\t\t# heading 3
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md007,md010,md022,md024,md025,md027,md030",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:9: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""+ # heading 1
   + # heading 2
     # heading 3
""",
    ),
    pluginRuleTest(
        "bad_atx_unordered_ordered_with_tab",
        source_file_contents="""+ # heading 1
  1. # heading 2
\t\t# heading 3
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md022,md024,md025,md027,md030",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:9: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""+ # heading 1
  1. # heading 2
     # heading 3
""",
    ),
    pluginRuleTest(
        "bad_atx_ordered_ordered_with_tab",
        source_file_contents="""1. # heading 1
   1. # heading 2
\t\t# heading 3
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md022,md024,md025,md027,md030",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:9: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. # heading 1
   1. # heading 2
      # heading 3
""",
    ),
    pluginRuleTest(
        "bad_atx_ordered_unordered_with_tab",
        source_file_contents="""1. # heading 1
   + # heading 2
\t\t# heading 3
""",
        enable_rules=plugin_enable_this_rule,
        disable_rules="md010,md022,md024,md025,md027,md030",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:9: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""1. # heading 1
   + # heading 2
     # heading 3
""",
    ),
    #     pluginRuleTest(
    #         "bad_atx_blockquote_unordered_unordered_with_tab",
    #         source_file_contents="""> + # heading 1
    # >    + # heading 2
    # > \t\t# heading 3
    # """,
    #         enable_rules=plugin_enable_this_rule,
    #         disable_rules="md007,md010,md022,md024,md025,md027,md030",
    #         scan_expected_return_code=1,
    #         scan_expected_output="""{temp_source_path}:3:9: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
    # """,
    #         fix_expected_file_contents="""+ # heading 1
    #   # heading 2
    # + # heading 1
    #   # heading 2
    #   # heading 3
    # """,
    #     ),
    #     pluginRuleTest(
    #         "bad_atx_blockquote_unordered_ordered_with_tab",
    #         source_file_contents="""> + # heading 1
    # >   1. # heading 2
    # > \t\t# heading 3
    # """,
    #         enable_rules=plugin_enable_this_rule,
    #         disable_rules="md010,md022,md024,md025,md027,md030",
    #         scan_expected_return_code=1,
    #         scan_expected_output="""{temp_source_path}:3:9: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
    # """,
    #         fix_expected_file_contents="""+ # heading 1
    #   # heading 2
    # + # heading 1
    #   # heading 2
    #   # heading 3
    # """,
    #     ),
    #     pluginRuleTest(
    #         "bad_atx_blockquote_ordered_ordered_with_tab",
    #         source_file_contents="""> 1. # heading 1
    # >    1. # heading 2
    # > \t\t# heading 3
    # """,
    #         enable_rules=plugin_enable_this_rule,
    #         disable_rules="md010,md022,md024,md025,md027,md030",
    #         scan_expected_return_code=1,
    #         scan_expected_output="""{temp_source_path}:3:9: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
    # """,
    #         fix_expected_file_contents="""+ # heading 1
    #   # heading 2
    # + # heading 1
    #   # heading 2
    #   # heading 3
    # """,
    #     ),
    #     pluginRuleTest(
    #         "bad_atx_blockquote_ordered_unordered_with_tab",
    #         source_file_contents="""> 1. # heading 1
    # >    + # heading 2
    # > \t\t# heading 3
    # """,
    #         enable_rules=plugin_enable_this_rule,
    #         disable_rules="md010,md022,md024,md025,md027,md030",
    #         scan_expected_return_code=1,
    #         scan_expected_output="""{temp_source_path}:3:9: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
    # """,
    #         fix_expected_file_contents="""+ # heading 1
    #   # heading 2
    # + # heading 1
    #   # heading 2
    #   # heading 3
    # """,
    #     ),
    pluginRuleTest(
        "mix_md023_md009",
        source_file_contents="""  ## Heading 2\a\a\a

Some more text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:1:15: MD009: Trailing spaces [Expected: 0 or 2; Actual: 3] (no-trailing-spaces)
""",
        fix_expected_file_contents="""## Heading 2

Some more text
""",
    ),
    pluginRuleTest(
        "mix_md023_md019",
        source_file_contents="""  #  Heading 1
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:1:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""# Heading 1
""",
    ),
    pluginRuleTest(
        "mix_md023_md030",
        source_file_contents=""" *  # Heading 1

    *  ## Heading 2

       *  ### Heading 3
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:1:2: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:3:5: MD007: Unordered list indentation [Expected: 2, Actual=4] (ul-indent)
{temp_source_path}:3:5: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:5:8: MD007: Unordered list indentation [Expected: 4, Actual=7] (ul-indent)
{temp_source_path}:5:8: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""* # Heading 1

  * ## Heading 2

    * ### Heading 3
""",
    ),
    pluginRuleTest(
        "mix_md023_md027",
        source_file_contents=""">  # Heading 1
>
>  ## Heading 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:1:4: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:3:4: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""> # Heading 1
>
> ## Heading 2
""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md023_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md023")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md023_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


def test_md023_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md023",
        """
  ITEM               DESCRIPTION

  Id                 md023
  Name(s)            heading-start-left,header-start-left
  Short Description  Headings must start at the beginning of the line.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md023.md

""",
    )
    execute_query_configuration_test(config_test)
