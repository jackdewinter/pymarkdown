"""
Module to provide tests related to the MD007 rule.
"""

import os
from test.rules.utils import (
    calculate_fix_tests,
    execute_configuration_test,
    execute_fix_test,
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginConfigErrorTest,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

# pylint: disable=too-many-lines

source_path = os.path.join("test", "resources", "rules", "md007") + os.sep

__plugin_disable_md005 = "md005"
__plugin_disable_md027 = "md027"
__plugin_disable_md030 = "md030"


configTests = [
    pluginConfigErrorTest(
        "invalid_indent",
        use_strict_config=True,
        set_args=["plugins.md007.indent=bad"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md007.indent' must be of type 'int'.""",
    ),
    pluginConfigErrorTest(
        "invalid_start_indented",
        use_strict_config=True,
        set_args=["plugins.md007.start_indented=bad"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md007.start_indented' must be of type 'bool'.""",
    ),
    pluginConfigErrorTest(
        "invalid_indent_range",
        use_strict_config=True,
        set_args=["plugins.md007.indent=$#5"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md007.indent' is not valid: Allowable values are between 2 and 4.""",
    ),
]


scanTests = [
    pluginRuleTest(
        "good_list_indentation_x",
        source_file_name=f"{source_path}good_list_indentation.md",
    ),
    pluginRuleTest(
        "bad_list_indentation_level_0",
        source_file_name=f"{source_path}bad_list_indentation_level_0.md",
        source_file_contents="""This is a test

 * this is level 1
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)",
        fix_expected_file_contents="""This is a test

* this is level 1
""",
    ),
    pluginRuleTest(
        "bad_list_indentation_level_1",
        source_file_name=f"{source_path}bad_list_indentation_level_1.md",
        source_file_contents="""This is a test

* this is level 1
   * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:4:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""This is a test

* this is level 1
  * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_indentation_level_2",
        source_file_name=f"{source_path}bad_list_indentation_level_2.md",
        source_file_contents="""This is a test

* this is level 1
  * this is level 2
     * this is level 3
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:5:6: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)",
        fix_expected_file_contents="""This is a test

* this is level 1
  * this is level 2
    * this is level 3
""",
    ),
    pluginRuleTest(
        "good_list_indentation_in_block_quote",
        source_file_name=f"{source_path}good_list_indentation_in_block_quote.md",
    ),
    pluginRuleTest(
        "good_list_indentation_in_double_block_quote",
        source_file_name=f"{source_path}good_list_indentation_in_double_block_quote.md",
    ),
    pluginRuleTest(
        "good_unordered_list_in_ordered_list",
        source_file_name=f"{source_path}good_unordered_list_in_ordered_list.md",
        disable_rules=__plugin_disable_md030,
    ),
    pluginRuleTest(
        "bad_unordered_list_in_ordered_list",
        source_file_name=f"{source_path}bad_unordered_list_in_ordered_list.md",
        disable_rules=__plugin_disable_md030,
        source_file_contents="""1.  ordered list
     + sublist
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:6: MD007: Unordered list indentation [Expected: 5, Actual=6] (ul-indent)",
        fix_expected_file_contents="""1.  ordered list
    + sublist
""",
    ),
    pluginRuleTest(
        "bad_level_1_unordered_list_in_ordered_list",
        source_file_name=f"{source_path}bad_level_1_unordered_list_in_ordered_list.md",
        disable_rules=__plugin_disable_md030,
        source_file_contents="""1.  ordered list
    + sublist
       + sublist
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:8: MD007: Unordered list indentation [Expected: 7, Actual=8] (ul-indent)",
        fix_expected_file_contents="""1.  ordered list
    + sublist
      + sublist
""",
    ),
    pluginRuleTest(
        "good_unordered_list_in_double_ordered_list",
        source_file_name=f"{source_path}good_unordered_list_in_double_ordered_list.md",
    ),
    pluginRuleTest(
        "bad_unordered_list_in_double_ordered_list",
        source_file_name=f"{source_path}bad_unordered_list_in_double_ordered_list.md",
        source_file_contents="""1. ordered list
   1. inner ordered list
       + sublist
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:8: MD007: Unordered list indentation [Expected: 7, Actual=8] (ul-indent)",
        fix_expected_file_contents="""1. ordered list
   1. inner ordered list
      + sublist
""",
    ),
    pluginRuleTest(
        "good_unordered_ordered_unordere_ordered_unordered",
        source_file_name=f"{source_path}good_unordered_ordered_unordere_ordered_unordered.md",
    ),
    pluginRuleTest(
        "bad_unordered_bad_ordered_unordered_ordered_unordered",
        source_file_name=f"{source_path}bad_unordered_bad_ordered_unordered_ordered_unordered.md",
        source_file_contents=""" + level 1
   1. level 2
      + level 3
        1. level 4
           + level 5
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)",
        fix_expected_file_contents="""+ level 1
   1. level 2
      + level 3
        1. level 4
           + level 5
""",
    ),
    pluginRuleTest(
        "bad_unordered_ordered_unordered_bad_ordered_unordered",
        source_file_name=f"{source_path}bad_unordered_ordered_unordered_bad_ordered_unordered.md",
        source_file_contents="""+ level 1
  1. level 2
      + level 3
        1. level 4
           + level 5
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:7: MD007: Unordered list indentation [Expected: 6, Actual=7] (ul-indent)",
        fix_expected_file_contents="""+ level 1
  1. level 2
     + level 3
        1. level 4
           + level 5
""",
    ),
    pluginRuleTest(
        "bad_unordered_ordered_unordered_ordered_unordered_bad",
        source_file_name=f"{source_path}bad_unordered_ordered_unordered_ordered_unordered_bad.md",
        source_file_contents="""+ level 1
  1. level 2
     + level 3
       1. level 4
           + level 5
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:5:12: MD007: Unordered list indentation [Expected: 11, Actual=12] (ul-indent)",
        fix_expected_file_contents="""+ level 1
  1. level 2
     + level 3
       1. level 4
          + level 5
""",
    ),
    pluginRuleTest(
        "bad_list_indentation_in_block_quote_level_0",
        source_file_name=f"{source_path}bad_list_indentation_in_block_quote_level_0.md",
        disable_rules=__plugin_disable_md027,
        source_file_contents="""This is a test

>  * this is level 1
>    * this is level 2
>      * this is level 3
""",
        scan_expected_return_code=1,
        scan_expected_output=(
            "{temp_source_path}:3:4: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)\n"
            + "{temp_source_path}:4:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)\n"
            + "{temp_source_path}:5:8: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)"
        ),
        fix_expected_file_contents="""This is a test

> * this is level 1
>   * this is level 2
>     * this is level 3
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_text",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_text.md",
        source_file_contents="""> This is some text
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        use_debug=True,
        scan_expected_output=(
            "{temp_source_path}:4:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)"
        ),
        fix_expected_file_contents="""> This is some text
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_atx_heading",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_atx_heading.md",
        source_file_contents="""> # This is some text
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:4:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""> # This is some text
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_thematic_break",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_thematic_break.md",
        source_file_contents="""> This is some text
>
> --------
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:6:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""> This is some text
>
> --------
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_setext_heading",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_setext_heading.md",
        source_file_contents="""> This is some text
> ---------
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)""",
        fix_expected_file_contents="""> This is some text
> ---------
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_html_block",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_html_block.md",
        source_file_contents="""> <!--
> This is a comment
> -->
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:6:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""> <!--
> This is a comment
> -->
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_fenced_block",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_fenced_block.md",
        source_file_contents="""> ```fenced
> This is a comment
> ```
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:6:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""> ```fenced
> This is a comment
> ```
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_indented_block",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_indented_block.md",
        source_file_contents=""">     This is a comment
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:4:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents=""">     This is a comment
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_link_reference_definition",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_link_reference_definition.md",
        source_file_contents="""> [link]: /url
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:4:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""> [link]: /url
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_list_in_block_quote_after_other_list",
        source_file_name=f"{source_path}bad_list_in_block_quote_after_other_list.md",
        source_file_contents="""> 1. This is another list.
>
> * this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:4:6: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)",
        fix_expected_file_contents="""> 1. This is another list.
>
> * this is level 1
>   * this is level 2
""",
    ),
    pluginRuleTest(
        "good_unordered_list_elements",
        source_file_name=f"{source_path}good_unordered_list_elements.md",
    ),
    pluginRuleTest(
        "bad_unordered_list_elements",
        source_file_name=f"{source_path}bad_unordered_list_elements.md",
        disable_rules=__plugin_disable_md005,
        source_file_contents="""This is a test

 * this is level 1
 * this is also level 1
   * this is level 2
   * this is also level 2
      * this is level 3
   * this is also level 2
    * this is also level 2
    * this is also level 2
* this is also level 1
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:4:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:5:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:6:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:7:7: MD007: Unordered list indentation [Expected: 4, Actual=6] (ul-indent)
{temp_source_path}:8:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:9:5: MD007: Unordered list indentation [Expected: 2, Actual=4] (ul-indent)
{temp_source_path}:10:5: MD007: Unordered list indentation [Expected: 2, Actual=4] (ul-indent)
""",
        fix_expected_file_contents="""This is a test

* this is level 1
* this is also level 1
  * this is level 2
  * this is also level 2
    * this is level 3
  * this is also level 2
  * this is also level 2
  * this is also level 2
* this is also level 1
""",
    ),
    pluginRuleTest(
        "good_list_indentation_by_four_ul_only",
        source_file_name=f"{source_path}good_list_indentation_by_four.md",
        source_file_contents="""This is a test

* this is level 1
    * this is level 2
        * this is level 3
""",
        set_args=["plugins.md007.indent=$#4"],
    ),
    pluginRuleTest(
        "good_list_indentation_by_four_ul_in_ol",
        source_file_contents="""This is a test

1. this is level 1
   * this is level 2
       * this is level 3
""",
        set_args=["plugins.md007.indent=$#4"],
    ),
    pluginRuleTest(
        "good_list_indentation_with_start",
        source_file_name=f"{source_path}good_list_indentation_with_start.md",
        set_args=["plugins.md007.start_indented=$!True"],
    ),
    pluginRuleTest(
        "issue_301",
        source_file_name=f"{source_path}issue-301.md",
        set_args=["plugins.md007.indent=$#4"],
        source_file_contents="""# Demo markdown

- Item
    - Sub item

1. Ordered item
    - Sub unordered item
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:7:5: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)",
        fix_expected_file_contents="""# Demo markdown

- Item
    - Sub item

1. Ordered item
   - Sub unordered item
""",
    ),
    pluginRuleTest(
        "example",
        source_file_contents="""* indented properly
  1. indented properly
     * indented properly
""",
    ),
    pluginRuleTest(
        "bad_all_indents",
        source_file_contents=""" * bad indent 1
    + bad indent 2
       - bad indent 3
""",
        disable_rules="md004",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:2:5: MD007: Unordered list indentation [Expected: 2, Actual=4] (ul-indent)
{temp_source_path}:3:8: MD007: Unordered list indentation [Expected: 4, Actual=7] (ul-indent)""",
        fix_expected_file_contents="""* bad indent 1
  + bad indent 2
    - bad indent 3
""",
    ),
    pluginRuleTest(
        "bad_all_indents_a",
        source_file_contents=""" * bad indent 1
   + bad indent 2
      - bad indent 3
""",
        disable_rules="md004",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:2:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:3:7: MD007: Unordered list indentation [Expected: 4, Actual=6] (ul-indent)""",
        fix_expected_file_contents="""* bad indent 1
  + bad indent 2
    - bad indent 3
""",
    ),
    pluginRuleTest(
        "bad_first_indent_with_extra_lines",
        source_file_contents="""* good indent 1
  next line 1
  + good indent 2
    next line 2
    - good indent 3
      next line 3
""",
        disable_rules="md004",
        scan_expected_return_code=0,
    ),
    pluginRuleTest(
        "bad_all_indent_with_extra_lines",
        source_file_contents=""" * bad indent 1
   next line 1
   + bad indent 2
     next line 2
      - bad indent 3
        next line 3
""",
        disable_rules="md004",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:3:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:5:7: MD007: Unordered list indentation [Expected: 4, Actual=6] (ul-indent)""",
        fix_expected_file_contents="""* bad indent 1
  next line 1
  + bad indent 2
    next line 2
    - bad indent 3
      next line 3
""",
    ),
    pluginRuleTest(
        "bad_all_indent_with_extra_lines_and_blanks",
        source_file_contents=""" * bad indent 1

   next line 1
   + bad indent 2

     next line 2
      - bad indent 3

        next line 3
""",
        disable_rules="md004",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:4:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:7:7: MD007: Unordered list indentation [Expected: 4, Actual=6] (ul-indent)""",
        fix_expected_file_contents="""* bad indent 1

  next line 1
  + bad indent 2

    next line 2
    - bad indent 3

      next line 3
""",
    ),
    pluginRuleTest(
        "bad_all_indent_with_extra_lines_and_blanks_and_multiples",
        source_file_contents=""" * bad indent 1.0

   next line 1.0
 * bad indent 1.1

   next line 1.1
   + bad indent 2.0

     next line 2.0
   + bad indent 2.1

     next line 2.1
      - bad indent 3.0

        next line 3.0
      - bad indent 3.1

        next line 3.1
   + bad indent 2.2

     next line 2.2
   + bad indent 2.3

     next line 2.3
 * bad indent 1.2

   next line 1.2
""",
        disable_rules="md004",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:4:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:7:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:10:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:13:7: MD007: Unordered list indentation [Expected: 4, Actual=6] (ul-indent)
{temp_source_path}:16:7: MD007: Unordered list indentation [Expected: 4, Actual=6] (ul-indent)
{temp_source_path}:19:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:22:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:25:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
""",
        fix_expected_file_contents="""* bad indent 1.0

  next line 1.0
* bad indent 1.1

  next line 1.1
  + bad indent 2.0

    next line 2.0
  + bad indent 2.1

    next line 2.1
    - bad indent 3.0

      next line 3.0
    - bad indent 3.1

      next line 3.1
  + bad indent 2.2

    next line 2.2
  + bad indent 2.3

    next line 2.3
* bad indent 1.2

  next line 1.2
""",
    ),
    pluginRuleTest(
        "bad_xxx",
        source_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> >\a
> >  ```block
> >   A code block
> >   ```
> >\a
> >  --------
> >\a
""".replace(
            "\a", " "
        ),
        disable_rules="md004,md027,md023,md009",
        scan_expected_return_code=0,
        scan_expected_output="",
    ),
    pluginRuleTest(
        "mix_md007_md004",
        source_file_contents=""" + first
   * second
     - third
 * first
   - second
     + third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:2:4: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: asterisk] (ul-style)
{temp_source_path}:2:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:3:6: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: dash] (ul-style)
{temp_source_path}:3:6: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)
{temp_source_path}:4:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:5:4: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: dash] (ul-style)
{temp_source_path}:5:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:6:6: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)
""",
        fix_expected_file_contents="""+ first
  + second
    + third
+ first
  + second
    + third
""",
    ),
    pluginRuleTest(
        "mix_md007_md005_only_md007_1",
        disable_rules=__plugin_disable_md005,
        source_file_contents=""" + first
   + second
     + third
+ first
  + second
    + third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:2:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:3:6: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)
""",
        fix_expected_file_contents="""+ first
  + second
    + third
+ first
  + second
    + third
""",
    ),
    pluginRuleTest(
        "mix_md007_md005_only_md007_2",
        disable_rules=__plugin_disable_md005,
        source_file_contents=""" + first
   + second
     + third
 + first
   + second
     + third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:2:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:3:6: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)
{temp_source_path}:4:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:5:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:6:6: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)
""",
        fix_expected_file_contents="""+ first
  + second
    + third
+ first
  + second
    + third
""",
    ),
    pluginRuleTest(
        "mix_md007_md005",
        source_file_contents=""" + first
   + second
     + third
+ first
  + second
    + third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:2:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:3:6: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)
{temp_source_path}:4:1: MD005: Inconsistent indentation for list items at the same level [Expected: 1; Actual: 0] (list-indent)
{temp_source_path}:5:3: MD005: Inconsistent indentation for list items at the same level [Expected: 3; Actual: 2] (list-indent)
{temp_source_path}:6:5: MD005: Inconsistent indentation for list items at the same level [Expected: 5; Actual: 4] (list-indent)
""",
        fix_expected_file_contents="""+ first
  + second
    + third
+ first
  + second
    + third
""",
    ),
    pluginRuleTest(
        "mix_md007_md027",
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
        "mix_md007_md030_xx",
        disable_rules=__plugin_disable_md030,
        source_file_contents=""" *  First
    first paragraph

    *  Second

    second paragraph
 *  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:4:5: MD007: Unordered list indentation [Expected: 2, Actual=4] (ul-indent)
{temp_source_path}:7:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
""",
        fix_expected_file_contents="""* First
  first paragraph

  * Second

  second paragraph
* Third
""",
    ),
    pluginRuleTest(
        "mix_md007_md030",
        disable_rules=__plugin_disable_md005,
        source_file_contents=""" *  First
    first paragraph

    *  Second

    second paragraph
 *  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:1:2: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:4:5: MD007: Unordered list indentation [Expected: 2, Actual=4] (ul-indent)
{temp_source_path}:4:5: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:7:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:7:2: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""* First
  first paragraph

  * Second

  second paragraph
* Third
""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md007_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md007")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md007_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md007_config(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}good_list_indentation.md")


def test_md007_query_config():
    config_test = pluginQueryConfigTest(
        "md007",
        """
  ITEM               DESCRIPTION

  Id                 md007
  Name(s)            ul-indent
  Short Description  Unordered list indentation
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md007.md


  CONFIGURATION ITEM  TYPE     VALUE

  indent              integer  2
  start_indented      boolean  False  

""",
    )
    execute_query_configuration_test(config_test)
