"""
Module to provide tests related to the MD027 rule.
"""

import os
from test.rules.utils import (
    execute_fix_test,
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

# pylint: disable=too-many-lines

source_path = os.path.join("test", "resources", "rules", "md027") + os.sep


__plugin_disable_md003_md013_md022 = "md003,md013,md022"
__plugin_disable_md005 = "md005"
__plugin_disable_md005_md007 = "md005,md007"
__plugin_disable_md005_md030 = "md005,md030"
__plugin_disable_md007 = "md007"
__plugin_disable_md009 = "md009"
__plugin_disable_md009_md028 = "md009,md028"
__plugin_disable_md012 = "md012"
__plugin_disable_md022 = "MD022"
__plugin_disable_md022_md023 = "md022,md023"
__plugin_disable_md023 = "md023"
__plugin_disable_md028 = "md028"
__plugin_disable_md031 = "md031"
__plugin_disable_md031_md032 = "md031,md032"
__plugin_disable_md032 = "md032"


scanTests = [
    pluginRuleTest(
        "good_block_quote_empty",
        source_file_name=f"{source_path}good_block_quote_empty.md",
    ),
    pluginRuleTest(
        "good_block_quote_empty_just_blank",
        source_file_name=f"{source_path}good_block_quote_empty_just_blank.md",
        source_file_contents=""">
""",
    ),
    pluginRuleTest(
        "bad_block_quote_empty_too_many_spaces",
        source_file_name=f"{source_path}bad_block_quote_empty_too_many_spaces.md",
        source_file_contents=""">\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""">
""",
    ),
    pluginRuleTest(
        "bad_block_quote_empty_one_too_many_spaces",
        source_file_contents=""">\a
""".replace(
            "\a", " "
        ),
        disable_rules=__plugin_disable_md009,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""">
""",
    ),
    pluginRuleTest(
        "bad_block_quote_multiple_empty_one_too_many_spaces",
        source_file_contents=""">\a
> abc
>\a
> def
""".replace(
            "\a", " "
        ),
        disable_rules=__plugin_disable_md009,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:3:2: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""">
> abc
>
> def
""",
    ),
    pluginRuleTest(
        "bad_block_quote_multiple_empty_one_too_many_spaces_xx",
        source_file_contents=""">\a
> abc
>\a
> def
>\a
""".replace(
            "\a", " "
        ),
        disable_rules=__plugin_disable_md009,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:3:2: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:5:2: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""">
> abc
>
> def
>
""",
    ),
    pluginRuleTest(
        "good_block_quote_simple_text",
        source_file_name=f"{source_path}good_block_quote_simple_text.md",
    ),
    pluginRuleTest(
        "good_block_quote_followed_by_heading",
        source_file_name=f"{source_path}good_block_quote_followed_by_heading.md",
        disable_rules=__plugin_disable_md022,
    ),
    pluginRuleTest(
        "good_block_quote_indent",
        source_file_name=f"{source_path}good_block_quote_indent.md",
    ),
    pluginRuleTest(
        "bad_block_quote_indent",
        source_file_name=f"{source_path}bad_block_quote_indent.md",
        source_file_contents=""">  this is text
>  within a block quote
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> within a block quote
""",
    ),
    pluginRuleTest(
        "bad_block_quote_indent_plus_one",
        source_file_name=f"{source_path}bad_block_quote_indent_plus_one.md",
        source_file_contents=""" >  this is text
 >  within a block quote
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:2:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 > within a block quote
""",
    ),
    pluginRuleTest(
        "bad_block_quote_only_one_properly_indented",
        source_file_name=f"{source_path}bad_block_quote_only_one_properly_indented.md",
        source_file_contents="""> this is text
>  within a block quote
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> within a block quote
""",
    ),
    pluginRuleTest(
        "bad_block_quote_only_one_properly_indented_plus_one",
        source_file_name=f"{source_path}bad_block_quote_only_one_properly_indented_plus_one.md",
        source_file_contents=""" > this is text
 >  within a block quote
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 > within a block quote
""",
    ),
    pluginRuleTest(
        "good_block_quote_indent_with_blank",
        source_file_name=f"{source_path}good_block_quote_indent_with_blank.md",
    ),
    pluginRuleTest(
        "good_block_quote_indent_with_blank_space",
        source_file_name=f"{source_path}good_block_quote_indent_with_blank_space.md",
    ),
    pluginRuleTest(
        "bad_block_quote_indent_with_blank_two_spaces",
        source_file_name=f"{source_path}bad_block_quote_indent_with_blank_two_spaces.md",
        source_file_contents="""> this is text
>\a\a
> within a block quote
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
>
> within a block quote
""",
    ),
    pluginRuleTest(
        "bad_block_quote_indent_with_blank_two_spaces_plus_one",
        source_file_name=f"{source_path}bad_block_quote_indent_with_blank_two_spaces_plus_one.md",
        source_file_contents=""" > this is text
 >\a\a
 > within a block quote
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 >
 > within a block quote
""",
    ),
    pluginRuleTest(
        "bad_block_quote_indent_with_blank_two_spaces_misaligned",
        source_file_name=f"{source_path}bad_block_quote_indent_with_blank_two_spaces_misaligned.md",
        source_file_contents=""" > this is text
 >\a\a
> within a block quote
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 >
> within a block quote
""",
    ),
    pluginRuleTest(
        "good_block_quote_indent_with_blank_space_no_start",
        source_file_name=f"{source_path}good_block_quote_indent_with_blank_space_no_start.md",
        disable_rules=__plugin_disable_md009_md028,
    ),
    pluginRuleTest(
        "bad_two_block_quotes_space_top",
        source_file_name=f"{source_path}bad_two_block_quotes_space_top.md",
        disable_rules=__plugin_disable_md028,
        source_file_contents=""">  this is text

> within a block quote
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text

> within a block quote
""",
    ),
    pluginRuleTest(
        "bad_two_block_quotes_space_bottom",
        source_file_name=f"{source_path}bad_two_block_quotes_space_bottom.md",
        disable_rules=__plugin_disable_md028,
        source_file_contents="""> this is text

>  within a block quote
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text

> within a block quote
""",
    ),
    pluginRuleTest(
        "bad_misalligned_double_quote",
        source_file_name=f"{source_path}bad_misalligned_double_quote.md",
        source_file_contents="""> > this is text
>>  within a block quote
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> > this is text
>> within a block quote
""",
    ),
    pluginRuleTest(
        "good_aligned_double_quote",
        source_file_name=f"{source_path}good_alligned_double_quote.md",
    ),
    pluginRuleTest(
        "bad_misindented_quote_within_list",
        source_file_name=f"{source_path}bad_misindented_quote_within_list.md",
        disable_rules=__plugin_disable_md032,
        source_file_contents="""- > this is a quote
>   this is the second line
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""- > this is a quote
> this is the second line
""",
    ),
    pluginRuleTest(
        "bad_misalligned_quote_within_list",
        source_file_name=f"{source_path}bad_misalligned_quote_within_list.md",
        source_file_contents="""- > this is a quote
  >  this is the second line
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""- > this is a quote
  > this is the second line
""",
    ),
    pluginRuleTest(
        "good_aligned_quote_within_list",
        source_file_name=f"{source_path}good_alligned_quote_within_list.md",
    ),
    pluginRuleTest(
        "good_fenced_block_in_list_in_block_quote",
        source_file_name=f"{source_path}good_fenced_block_in_list_in_block_quote.md",
        disable_rules=__plugin_disable_md031_md032,
    ),
    pluginRuleTest(
        "good_list_within_block_quote_surrounded",
        source_file_name=f"{source_path}good_list_within_block_quote_surrounded.md",
        disable_rules=__plugin_disable_md032,
    ),
    pluginRuleTest(
        "good_block_quote_list_block_quote",
        source_file_name=f"{source_path}good_block_quote_list_block_quote.md",
        disable_rules=__plugin_disable_md032,
    ),
    pluginRuleTest(
        "good_multiple_blanks_in_block_quote",
        source_file_name=f"{source_path}bad_multiple_blanks_in_block_quote.md",
        disable_rules=__plugin_disable_md012,
    ),
    pluginRuleTest(
        "good_indentation_in_block_quote",
        source_file_name=f"{source_path}good_indentation_in_block_quote.md",
    ),
    pluginRuleTest(
        "good_items_with_multiple_lines_in_block_quote",
        source_file_name=f"{source_path}good_items_with_multiple_lines_in_block_quote.md",
    ),
    pluginRuleTest(
        "good_thematic_break_in_block_quote",
        source_file_name=f"{source_path}good_thematic_break_in_block_quote.md",
        disable_rules=__plugin_disable_md022,
    ),
    pluginRuleTest(
        "good_indented_code_block_in_block_quote",
        source_file_name=f"{source_path}good_indented_code_block_in_block_quote.md",
    ),
    pluginRuleTest(
        "bad_block_quote_misindented_unordered_list_first",
        source_file_name=f"{source_path}bad_block_quote_misindented_unordered_list_first.md",
        disable_rules=__plugin_disable_md005_md007,
        source_file_contents=""">  + list
>    this
> + that
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> + list
>   this
> + that
""",
    ),
    pluginRuleTest(
        "bad_block_quote_misindented_ordered_list_first",
        source_file_name=f"{source_path}bad_block_quote_misindented_ordered_list_first.md",
        disable_rules=__plugin_disable_md005,
        source_file_contents=""">  1. list
>     this
> 1. that
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> 1. list
>    this
> 1. that
""",
    ),
    pluginRuleTest(
        "bad_block_quote_misindented_unordered_list_last",
        source_file_name=f"{source_path}bad_block_quote_misindented_unordered_list_last.md",
        disable_rules=__plugin_disable_md005_md007,
        source_file_contents="""> + list
>   this
>  + that
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> + list
>   this
> + that
""",
    ),
    pluginRuleTest(
        "bad_block_quote_misindented_ordered_list_last",
        source_file_name=f"{source_path}bad_block_quote_misindented_ordered_list_last.md",
        disable_rules=__plugin_disable_md005,
        source_file_contents="""> 1. list
>    this
>  1. that
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> 1. list
>    this
> 1. that
""",
    ),
    pluginRuleTest(
        "good_block_quote_unordered_list",
        source_file_name=f"{source_path}good_block_quote_unordered_list.md",
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list",
        source_file_name=f"{source_path}good_block_quote_ordered_list.md",
    ),
    pluginRuleTest(
        "good_block_quote_unordered_list_unordered_list",
        source_file_name=f"{source_path}good_block_quote_unordered_list_unordered_list.md",
    ),
    pluginRuleTest(
        "good_block_quote_unordered_list_ordered_list",
        source_file_name=f"{source_path}good_block_quote_unordered_list_ordered_list.md",
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_ordered_list",
        source_file_name=f"{source_path}good_block_quote_ordered_list_ordered_list.md",
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_unordered_list",
        source_file_name=f"{source_path}good_block_quote_ordered_list_unordered_list.md",
    ),
    pluginRuleTest(
        "good_block_quote_unordered_list_block_quote_text",
        source_file_name=f"{source_path}good_block_quote_ordered_list_unordered_list.md",
    ),
    pluginRuleTest(
        "bad_block_quote_unordered_list_block_quote_text_first",
        source_file_name=f"{source_path}bad_block_quote_unordered_list_block_quote_text_first.md",
        source_file_contents="""> + list
>   this
>   >  good
>   > item
> + that
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> + list
>   this
>   > good
>   > item
> + that
""",
    ),
    pluginRuleTest(
        "bad_block_quote_unordered_list_block_quote_text_last",
        source_file_name=f"{source_path}bad_block_quote_unordered_list_block_quote_text_last.md",
        source_file_contents="""> + list
>   this
>   > good
>   >  item
> + that
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:7: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> + list
>   this
>   > good
>   > item
> + that
""",
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_thematic_break",
        source_file_name=f"{source_path}good_block_quote_ordered_list_thematic_break.md",
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_thematic_break_misaligned",
        source_file_name=f"{source_path}good_block_quote_ordered_list_thematic_break_misaligned.md",
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_atx_heading",
        source_file_name=f"{source_path}good_block_quote_ordered_list_atx_heading.md",
        disable_rules=__plugin_disable_md022,
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_setext_heading",
        source_file_name=f"{source_path}good_block_quote_ordered_list_setext_heading.md",
        disable_rules=__plugin_disable_md022,
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_setext_heading_first",
        source_file_name=f"{source_path}bad_block_quote_ordered_list_setext_heading_first.md",
        disable_rules=__plugin_disable_md022_md023,
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_setext_heading_last",
        source_file_name=f"{source_path}bad_block_quote_ordered_list_setext_heading_last.md",
        disable_rules=__plugin_disable_md022_md023,
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_indented_code_block",
        source_file_name=f"{source_path}good_block_quote_ordered_list_indented_code_block.md",
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_indented_code_block_first",
        source_file_name=f"{source_path}bad_block_quote_ordered_list_indented_code_block_first.md",
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_indented_code_block_last",
        source_file_name=f"{source_path}bad_block_quote_ordered_list_indented_code_block_last.md",
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_fenced_code_block",
        source_file_name=f"{source_path}good_block_quote_ordered_list_fenced_code_block.md",
        disable_rules=__plugin_disable_md031,
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_fenced_code_block_indent_first",
        source_file_name=f"{source_path}good_block_quote_ordered_list_fenced_code_block_indent_first.md",
        disable_rules=__plugin_disable_md031,
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_fenced_code_block_indent_second",
        source_file_name=f"{source_path}good_block_quote_ordered_list_fenced_code_block_indent_second.md",
        disable_rules=__plugin_disable_md031,
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_fenced_code_block_indent_third",
        source_file_name=f"{source_path}good_block_quote_ordered_list_fenced_code_block_indent_third.md",
        disable_rules=__plugin_disable_md031,
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_html_block",
        source_file_name=f"{source_path}good_block_quote_ordered_list_html_block.md",
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_html_block_with_indent",
        source_file_name=f"{source_path}good_block_quote_ordered_list_html_block_with_indent.md",
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_html_block_with_multiline",
        source_file_name=f"{source_path}good_block_quote_ordered_list_html_block_with_multiline.md",
    ),
    pluginRuleTest(
        "good_block_quote_ordered_list_lrd",
        source_file_name=f"{source_path}good_block_quote_ordered_list_lrd.md",
        use_debug=True,
    ),
    pluginRuleTest(
        "good_list_in_block_quote_after_other_list",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_other_list.md",
        disable_rules=__plugin_disable_md007,
    ),
    pluginRuleTest(
        "bad_list_indentation_in_block_quote_level_0",
        source_file_name=f"{source_path}test_md007_bad_list_indentation_in_block_quote_level_0.md",
        disable_rules=__plugin_disable_md007,
        source_file_contents="""This is a test

>  * this is level 1
>    * this is level 2
>      * this is level 3
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""This is a test

> * this is level 1
>    * this is level 2
>      * this is level 3
""",
    ),
    pluginRuleTest(
        "good_block_quote_unordered_list_text_first",
        source_file_name=f"{source_path}bad_block_quote_unordered_list_text_first.md",
        disable_rules=__plugin_disable_md005_md030,
    ),
    pluginRuleTest(
        "good_block_quote_unordered_list_text_last",
        source_file_name=f"{source_path}bad_block_quote_unordered_list_text_last.md",
    ),
    pluginRuleTest(
        "good_block_quote_with_trailing_empty_line",
        source_file_name=f"{source_path}good_block_quote_with_trailing_empty_line.md",
    ),
    pluginRuleTest(
        "issue_189",
        source_file_name=f"{source_path}issue-189.md",
        disable_rules=__plugin_disable_md003_md013_md022,
    ),
    pluginRuleTest(
        "issue_189_mini",
        source_file_name=f"{source_path}issue-189-mini.md",
    ),
    pluginRuleTest(
        "xxxx",
        source_file_contents=""">  *  Heading 1
>\a
>  *  Heading 2
>\a
""".replace(
            "\a", " "
        ),
        disable_rules="md007,md009,md012,md030",
        scan_expected_return_code=1,
        # use_debug=True,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> *  Heading 1
>\a
> *  Heading 2
>\a
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "xxxx1",
        source_file_contents=""">  *  Heading 1
>     fff
>  *  Heading 2
>     fff
""",
        disable_rules="md007,md009,md012,md030",
        scan_expected_return_code=1,
        # use_debug=True,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> *  Heading 1
>    fff
> *  Heading 2
>    fff
""",
    ),
    pluginRuleTest(
        "mix_md027_md007",
        source_file_contents=""">  + first
>     + second
>       + third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:1:4: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:2:7: MD007: Unordered list indentation [Expected: 2, Actual=4] (ul-indent)
{temp_source_path}:3:9: MD007: Unordered list indentation [Expected: 4, Actual=6] (ul-indent)
""",
        fix_expected_file_contents="""> + first
>   + second
>     + third
""",
    ),
    pluginRuleTest(
        "mix_md027_md009",
        disable_rules=__plugin_disable_md023,
        source_file_contents=""">  # Header 1\a
>
>  ## Header 2\a\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:1:14: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:3:15: MD009: Trailing spaces [Expected: 0 or 2; Actual: 3] (no-trailing-spaces)
""",
        fix_expected_file_contents="""> # Header 1
>
> ## Header 2
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "mix_md027_md023",
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
    pluginRuleTest(
        "mix_md027_md030",
        source_file_contents=""">  *  Heading 1
>  *  Heading 2
""",
        disable_rules=__plugin_disable_md007,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:1:4: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:2:4: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""> * Heading 1
> * Heading 2
""",
    ),
    pluginRuleTest(
        "mix_md027_md005",
        source_file_contents=""">  * Heading 1
>   * Heading 2
""",
        disable_rules=__plugin_disable_md007,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:2:5: MD005: Inconsistent indentation for list items at the same level [Expected: 3; Actual: 4] (list-indent)
""",
        fix_expected_file_contents="""> * Heading 1
> * Heading 2
""",
    ),
]
fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents:
        fixTests.append(i)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md027_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md027")


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md027_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


def test_md027_query_config():
    config_test = pluginQueryConfigTest(
        "md027",
        """
  ITEM               DESCRIPTION

  Id                 md027
  Name(s)            no-multiple-space-blockquote
  Short Description  Multiple spaces after blockquote symbol
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md027.md


""",
    )
    execute_query_configuration_test(config_test)
