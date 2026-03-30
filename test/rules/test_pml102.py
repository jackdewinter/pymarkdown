"""
Module to provide tests related to the PMl102 rule.
"""

from test.rules.utils import (
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

scanTests = [
    pluginRuleTest(
        "good_single_olist_indent_normal_single_line",
        enable_rules="pml102",
        source_file_contents="""1. a list
""",
    ),
    pluginRuleTest(
        "good_single_olist_indent_normal_double_line",
        enable_rules="pml102",
        source_file_contents="""1. a list
   properly indented content
""",
    ),
    pluginRuleTest(
        "good_single_olist_indent_normal_atx_para",
        enable_rules="pml102",
        source_file_contents="""1. ## bob

   a list
   properly indented content
""",
    ),
    pluginRuleTest(
        "good_single_olist_indent_normal_para_atx_para",
        enable_rules="pml102",
        source_file_contents="""1. first lines
   of list

   ## bob

   a list
   properly indented content
""",
    ),
    pluginRuleTest(
        "bad_single_olist_indent_minus_one",
        enable_rules="pml102",
        source_file_contents="""
1. a list
  almost properly indented content (-1 indent)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: PML102: Disallows lazy list indentation [Expected: 3; Actual: 2] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_olist_indent_minus_all",
        enable_rules="pml102",
        source_file_contents="""
1. a list
almost properly indented content (-1 indent)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_single_olist_indent_plus_one",
        enable_rules="pml102",
        source_file_contents="""
1. a list
    almost properly indented content (+1 indent)
""",
    ),
    pluginRuleTest(
        "good_single_olist_new_item_indent_normal",
        enable_rules="pml102",
        source_file_contents="""
1. a list
   properly indented content
2. a list
   properly indented content
""",
    ),
    pluginRuleTest(
        "bad_single_olist_new_item_indent_minus_one_minus_two",
        enable_rules="pml102",
        source_file_contents="""
1. a list
  properly indented content
2. a list
 properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: PML102: Disallows lazy list indentation [Expected: 3; Actual: 2] (disallow-lazy-list-indentation)
{temp_source_path}:5:2: PML102: Disallows lazy list indentation [Expected: 3; Actual: 1] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_olist_new_item_indent_minus_all",
        enable_rules="pml102",
        source_file_contents="""
1. a list
properly indented content
2. a list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)
{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_single_olist_new_item_adjust_indent_normal",
        enable_rules="pml102",
        disable_rules="md030",
        source_file_contents="""
1. a list
   properly indented content
2.  a list
    properly indented content
""",
    ),
    pluginRuleTest(
        "bad_single_olist_new_item_adjust_indent_first_minus_two",
        enable_rules="pml102",
        disable_rules="md030",
        source_file_contents="""
1. a list
 properly indented content
2.  a list
    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: PML102: Disallows lazy list indentation [Expected: 3; Actual: 1] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_olist_new_item_adjust_indent_first_minus_all",
        enable_rules="pml102",
        disable_rules="md030",
        source_file_contents="""
1. a list
properly indented content
2.  a list
    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_olist_new_item_adjust_indent_second_minus_one",
        enable_rules="pml102",
        disable_rules="md030",
        source_file_contents="""
1. a list
   properly indented content
2.  a list
   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: PML102: Disallows lazy list indentation [Expected: 4; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_olist_new_item_adjust_indent_second_minus_all",
        enable_rules="pml102",
        disable_rules="md030",
        source_file_contents="""
1. a list
   properly indented content
2.  a list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 4; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_double_olist_indent_normal",
        enable_rules="pml102",
        source_file_contents="""
1. a list
   1. another list
      properly indented content
""",
    ),
    pluginRuleTest(
        "bad_double_olist_indent_minus_one",
        enable_rules="pml102",
        source_file_contents="""
1. a list
   1. another list
     almost properly indented content (-1 indent)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_double_olist_indent_minus_all",
        enable_rules="pml102",
        source_file_contents="""
1. a list
   1. another list
almost properly indented content (-1 indent)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_double_olist_indent_minus_four",
        enable_rules="pml102",
        source_file_contents="""1. a list
   1. another list
  almost properly indented content (-4 indent)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: PML102: Disallows lazy list indentation [Expected: 6; Actual: 2] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_double_olist_indent_plus_one",
        enable_rules="pml102",
        source_file_contents="""1. a list
   1. another list
       almost properly indented content (+1 indent)
""",
    ),
    pluginRuleTest(
        "good_double_olist_new_item_indent_normal",
        enable_rules="pml102",
        source_file_contents="""
1. a list
   1. another list
      properly indented content
   1. another list
      properly indented content
""",
    ),
    pluginRuleTest(
        "bad_double_olist_new_item_indent_normal_first_minus_one",
        enable_rules="pml102",
        source_file_contents="""
1. a list
   1. another list
     properly indented content
   1. another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_double_olist_new_item_indent_normal_first_minus_all",
        enable_rules="pml102",
        source_file_contents="""
1. a list
   1. another list
properly indented content
   1. another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_double_olist_new_item_indent_normal_second_minus_one",
        enable_rules="pml102",
        source_file_contents="""
1. a list
   1. another list
      properly indented content
   1. another list
     properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_double_olist_new_item_indent_normal_second_minus_all",
        enable_rules="pml102",
        source_file_contents="""
1. a list
   1. another list
      properly indented content
   1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_double_olist_new_item_adjust_indent_normal",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
1. a list
   1. another list
      properly indented content
    1. another list
       properly indented content
""",
    ),
    pluginRuleTest(
        "bad_double_olist_new_item_adjust_indent_minus_one",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
1. a list
   1. another list
      properly indented content
    1. another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_double_olist_new_item_adjust_indent_minus_all",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
1. a list
   1. another list
      properly indented content
    1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 7; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_bq_olist_indent_normal",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
     properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_olist_indent_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
>    properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_indent_minus_one",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_indent_minus_all",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 5; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_indent_minus_one_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
>   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_indent_minus_all_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
>properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:2: PML102: Disallows lazy list indentation [Expected: 5; Actual: 1] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_bq_olist_indent_plus_one",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
      properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_olist_indent_plus_one_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
>     properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_olist_new_item_indent_normal",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
     properly indented content
> 1. another list
     properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_olist_new_item_indent_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
>    properly indented content
> 1. another list
>    properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_new_item_indent_first_minus_one",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
    properly indented content
> 1. another list
     properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_new_item_indent_first_minus_all",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
properly indented content
> 1. another list
     properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 5; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_new_item_indent_second_minus_one_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
>    properly indented content
> 1. another list
>   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_new_item_indent_second_minus_all_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
>    properly indented content
> 1. another list
>properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:2: PML102: Disallows lazy list indentation [Expected: 5; Actual: 1] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_bq_olist_new_item_adjust_indent_normal",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> a block
>
> 1. another list
     properly indented content
>  1. another list
      properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_olist_new_item_adjust_indent_normal_bq",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> a block
>
> 1. another list
>    properly indented content
>  1. another list
>     properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_new_item_adjust_indent_minus_one",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> a block
>
> 1. another list
     properly indented content
>  1. another list
     properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_new_item_adjust_indent_second_minus_one_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> 1. another list
>    properly indented content
> 1. another list
>   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_indent_normal_first_no_bq_12",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
       properly indented content
> > 1. another list
> >    properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_indent_normal_second_no_bq_12",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> > 1. another list
       properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_first_minus_one_first_no_bq_12",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
      properly indented content
> > 1. another list
> >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_first_minus_one_second_no_bq_12",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >   properly indented content
> > 1. another list
       properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_first_minus_all_first_no_bq_12",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
properly indented content
> > 1. another list
> >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 7; Actual: 0] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_first_minus_all_second_no_bq_12",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >properly indented content
> > 1. another list
       properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_one_first_no_bq_12",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
       properly indented content
> > 1. another list
> >   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_one_second_no_bq_12",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> > 1. another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_all_first_no_bq_12",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
       properly indented content
> > 1. another list
> >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_all_second_no_bq_12",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
       properly indented content
> > 1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:1: PML102: Disallows lazy list indentation [Expected: 7; Actual: 0] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_indent_adjust_first_no_bq_12",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
       properly indented content
> >  1. another list
        properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_indent_adjust_second_no_bq_12",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> >  1. another list
        properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_adjust_minus_one_first_no_bq_12",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
       properly indented content
> >  1. another list
> >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_adjust_minus_one_second_no_bq_12",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> >  1. another list
       properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_adjust_minus_all_first_no_bq_12",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
       properly indented content
> >  1. another list
> >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:4: PML102: Disallows lazy list indentation [Expected: 8; Actual: 3] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_adjust_minus_all_second_no_bq_12",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> >  1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:1: PML102: Disallows lazy list indentation [Expected: 8; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_indent_normal_first_no_bq_1",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
  >    properly indented content
> > 1. another list
> >    properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_indent_normal_second_no_bq_1",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> > 1. another list
  >    properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_first_minus_one_first_no_bq_1",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
  >   properly indented content
> > 1. another list
> >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_first_minus_one_second_no_bq_1",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >   properly indented content
> > 1. another list
  >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_indent_normal_first_minus_all_first_no_bq_1",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
> > a block
> >
  > 1. another list
> >properly indented content
> > 1. another list
> >    properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_first_minus_all_second_no_bq_1",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >properly indented content
> > 1. another list
  >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_one_first_no_bq_1",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
  >    properly indented content
> > 1. another list
> >   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_one_second_no_bq_1",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> > 1. another list
  >   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_all_first_no_bq_1",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
  >    properly indented content
> > 1. another list
> >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_all_second_no_bq_1",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> > 1. another list
  >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_adjust_indent_normal_first_no_bq_1",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
  >    properly indented content
> >  1. another list
> >     properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_adjust_indent_normal_second_no_bq_1",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> >  1. another list
  >     properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_adjust_indent_minus_one_first_no_bq_1",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
  >    properly indented content
> >  1. another list
> >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_adjust_indent_minus_one_second_no_bq_1",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> >  1. another list
  >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_adjust_indent_minus_all_first_no_bq_1",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
  >    properly indented content
> >  1. another list
> >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:4: PML102: Disallows lazy list indentation [Expected: 8; Actual: 3] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_adjust_indent_minus_all_second_no_bq_1",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> >  1. another list
  >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:4: PML102: Disallows lazy list indentation [Expected: 8; Actual: 3] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_indent_normal_first_no_bq_2",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
>      properly indented content
> > 1. another list
> >    properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_indent_normal_second_no_bq_2",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> > 1. another list
>      properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_first_minus_one_first_no_bq_2",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
>     properly indented content
> > 1. another list
> >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_first_minus_one_second_no_bq_2",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >   properly indented content
> > 1. another list
>      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_first_minus_all_no_bq_2",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >properly indented content
> > 1. another list
>      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_one_no_bq_2",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> > 1. another list
>     properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_first_minus_all_first_no_bq_2",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
>properly indented content
> > 1. another list
> >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:2: PML102: Disallows lazy list indentation [Expected: 7; Actual: 1] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_one_second_no_bq_2",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> > 1. another list
>     properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_all_first_no_bq_2",
        enable_rules="pml102",
        disable_rules="md032,md027",
        source_file_contents="""
> > a block
> >
>   1. another list
> >    properly indented content
> > 1. another list
> >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_all_second_no_bq_2",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> > 1. another list
>properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:2: PML102: Disallows lazy list indentation [Expected: 7; Actual: 1] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_adjust_indent_normal_first_no_bq_2",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
>      properly indented content
> >  1. another list
> >     properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_adjust_indent_normal_second_no_bq_2",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> >  1. another list
>       properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_adjust_indent_minus_one_first_no_bq_2",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
>      properly indented content
> >  1. another list
> >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_adjust_indent_minus_one_second_no_bq_2",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> >  1. another list
>      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_adjust_indent_minus_all_first_no_bq_2",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
>      properly indented content
> >  1. another list
> >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:4: PML102: Disallows lazy list indentation [Expected: 8; Actual: 3] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_adjust_indent_minus_all_second_no_bq_2",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> >  1. another list
>properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:2: PML102: Disallows lazy list indentation [Expected: 8; Actual: 1] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_indent_normal_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> > 1. another list
> >    properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_first_minus_one_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >   properly indented content
> > 1. another list
> >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_first_minus_all_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >properly indented content
> > 1. another list
> >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_one_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> > 1. another list
> >   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_indent_normal_second_minus_all_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> > 1. another list
> >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_bq_bq_olist_new_item_adjust_indent_normal_normal_bq",
        enable_rules="pml102",
        disable_rules="md005,md027,md018,md020",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> >  1. another list
> >     properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_adjust_indent_minus_one_normal_bq",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> >  1. another list
> >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_bq_olist_new_item_adjust_indent_minus_all_normal_bq",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> > a block
> >
> > 1. another list
> >    properly indented content
> >  1. another list
> >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:4: PML102: Disallows lazy list indentation [Expected: 8; Actual: 3] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_bq_olist_olist_new_item_indent_normal_normal_both_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
        properly indented content
>    1. another list
        properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_first_minus_one_both_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
       properly indented content
>    1. another list
        properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_first_minus_all_both_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
properly indented content
>    1. another list
        properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: PML102: Disallows lazy list indentation [Expected: 8; Actual: 0] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_second_minus_one_both_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
        properly indented content
>    1. another list
       properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_second_minus_all_both_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
        properly indented content
>    1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 8; Actual: 0] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_bq_olist_olist_new_item_indent_adjust_normal_both_no_bq",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
> 1. first list
>    1. inner list
        properly indented content
>     1. another list
         properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_adjust_minus_one_no_bq",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
> 1. first list
>    1. inner list
        properly indented content
>     1. another list
        properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_adjust_minus_all_no_bq",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
> 1. first list
>    1. inner list
        properly indented content
>     1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 9; Actual: 0] (disallow-lazy-list-indentation)"""
    ),

    pluginRuleTest(
        "good_bq_olist_olist_new_item_indent_normal_normal_first_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
>       properly indented content
>    1. another list
        properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_first_minus_one_first_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
>      properly indented content
>    1. another list
        properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_first_minus_all_first_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
>properly indented content
>    1. another list
        properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:2: PML102: Disallows lazy list indentation [Expected: 8; Actual: 1] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_second_minus_one_first_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
>       properly indented content
>    1. another list
       properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_second_minus_all_first_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
>       properly indented content
>    1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 8; Actual: 0] (disallow-lazy-list-indentation)
"""
    ),


    pluginRuleTest(
        "good_bq_olist_olist_new_item_indent_adjust_normal_first_no_bq",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
> 1. first list
>    1. inner list
        properly indented content
>     1. another list
>        properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_adjust_minus_one_first_no_bq",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
> 1. first list
>    1. inner list
        properly indented content
>     1. another list
>       properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_adjust_minus_all_first_no_bq",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
> 1. first list
>    1. inner list
        properly indented content
>     1. another list
>properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:2: PML102: Disallows lazy list indentation [Expected: 9; Actual: 1] (disallow-lazy-list-indentation)
"""
    ),


    pluginRuleTest(
        "good_bq_olist_olist_new_item_indent_normal_normal_second_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
        properly indented content
>    1. another list
>       properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_first_minus_one_second_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
       properly indented content
>    1. another list
>       properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_first_minus_all_second_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
properly indented content
>    1. another list
>       properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: PML102: Disallows lazy list indentation [Expected: 8; Actual: 0] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_second_minus_one_second_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
        properly indented content
>    1. another list
>      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_second_minus_all_second_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
        properly indented content
>    1. another list
>properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:2: PML102: Disallows lazy list indentation [Expected: 8; Actual: 1] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_bq_olist_olist_new_item_indent_adjust_normal_second_no_bq",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
> 1. first list
>    1. inner list
>       properly indented content
>     1. another list
         properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_adjust_minus_one_second_no_bq",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
> 1. first list
>    1. inner list
>       properly indented content
>     1. another list
        properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_adjust_minus_all_second_no_bq",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
> 1. first list
>    1. inner list
>       properly indented content
>     1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 9; Actual: 0] (disallow-lazy-list-indentation)
"""
    ),

    pluginRuleTest(
        "good_bq_olist_olist_new_item_indent_normal_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
>       properly indented content
>    1. another list
>       properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_first_minus_one_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
>      properly indented content
>    1. another list
>       properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_first_minus_all_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
>properly indented content
>    1. another list
>       properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:2: PML102: Disallows lazy list indentation [Expected: 8; Actual: 1] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_second_minus_one_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
>       properly indented content
>    1. another list
>      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_bq_olist_olist_new_item_indent_normal_second_minus_all_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> 1. first list
>    1. inner list
>       properly indented content
>    1. another list
>properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:2: PML102: Disallows lazy list indentation [Expected: 8; Actual: 1] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_bq_olist_olist_new_item_indent_adjust_normal_normal_bq",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
> 1. first list
>    1. inner list
>       properly indented content
>     1. another list
>        properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_olist_olist_new_item_indent_adjust_minus_one_normal_bq",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
> 1. first list
>    1. inner list
>       properly indented content
>     1. another list
>       properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "good_bq_olist_olist_new_item_indent_adjust_minus_all_normal_bq",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
> 1. first list
>    1. inner list
>       properly indented content
>     1. another list
>properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:2: PML102: Disallows lazy list indentation [Expected: 9; Actual: 1] (disallow-lazy-list-indentation)"""
    ),


    pluginRuleTest(
        "good_olist_bq_olist_new_item_indent_normal_normal_both_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
        properly indented content
   > 1. another list
        properly indented content
""",
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_first_minus_one_both_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
       properly indented content
   > 1. another list
        properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_first_minus_all_both_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
properly indented content
   > 1. another list
        properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: PML102: Disallows lazy list indentation [Expected: 8; Actual: 0] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_second_minus_one_both_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
        properly indented content
   > 1. another list
       properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_second_minus_all_both_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
        properly indented content
   > 1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 8; Actual: 0] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_olist_bq_olist_new_item_indent_adjust_normal_both_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md027,md032",
        source_file_contents="""
1. > first list
   > 1. inner list
        properly indented content
   >  1. another list
         properly indented content
""",
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_adjust_minus_one_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md027,md032",
        source_file_contents="""
1. > first list
   > 1. inner list
        properly indented content
   >  1. another list
        properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_adjust_minus_all_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md027,md032",
        source_file_contents="""
1. > first list
   > 1. inner list
        properly indented content
   >  1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 9; Actual: 0] (disallow-lazy-list-indentation)"""
    ),

    pluginRuleTest(
        "good_olist_bq_olist_new_item_indent_normal_normal_first_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >    properly indented content
   > 1. another list
        properly indented content
""",
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_first_minus_one_first_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >   properly indented content
   > 1. another list
        properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_first_minus_all_first_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >properly indented content
   > 1. another list
        properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: PML102: Disallows lazy list indentation [Expected: 8; Actual: 4] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_second_minus_one_first_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >    properly indented content
   > 1. another list
       properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_second_minus_all_first_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >    properly indented content
   > 1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 8; Actual: 0] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_olist_bq_olist_new_item_indent_adjust_normal_first_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md027,md032",
        source_file_contents="""
1. > first list
   > 1. inner list
        properly indented content
   >  1. another list
   >     properly indented content
""",
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_adjust_minus_one_first_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md027,md032",
        source_file_contents="""
1. > first list
   > 1. inner list
        properly indented content
   >  1. another list
   >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_adjust_minus_all_first_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md027,md032",
        source_file_contents="""
1. > first list
   > 1. inner list
        properly indented content
   >  1. another list
   >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:5: PML102: Disallows lazy list indentation [Expected: 9; Actual: 4] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_olist_bq_olist_new_item_indent_normal_normal_second_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
        properly indented content
   > 1. another list
   >    properly indented content
""",
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_first_minus_one_second_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
       properly indented content
   > 1. another list
   >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_first_minus_all_second_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
properly indented content
   > 1. another list
   >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: PML102: Disallows lazy list indentation [Expected: 8; Actual: 0] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_second_minus_one_second_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
        properly indented content
   > 1. another list
   >   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_second_minus_all_second_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
        properly indented content
   > 1. another list
   >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:5: PML102: Disallows lazy list indentation [Expected: 8; Actual: 4] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_olist_bq_olist_new_item_indent_adjust_normal_second_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md027,md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >    properly indented content
   >  1. another list
         properly indented content
""",
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_adjust_minus_one_second_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md027,md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >    properly indented content
   >  1. another list
        properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_adjust_minus_all_second_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md027,md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >    properly indented content
   >  1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 9; Actual: 0] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_olist_bq_olist_new_item_indent_normal_normal_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >    properly indented content
   > 1. another list
   >    properly indented content
""",
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_first_minus_one_normal_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >   properly indented content
   > 1. another list
   >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_first_minus_all_normal_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >properly indented content
   > 1. another list
   >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: PML102: Disallows lazy list indentation [Expected: 8; Actual: 4] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_second_minus_one_normal_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >    properly indented content
   > 1. another list
   >   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_second_minus_all_normal_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >    properly indented content
   > 1. another list
   >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:5: PML102: Disallows lazy list indentation [Expected: 8; Actual: 4] (disallow-lazy-list-indentation)
"""
    ),
    pluginRuleTest(
        "good_olist_bq_olist_new_item_indent_adjust_normal_normal_bq",
        enable_rules="pml102",
        disable_rules="md005,md027,md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >    properly indented content
   >  1. another list
   >     properly indented content
""",
    ),
    pluginRuleTest(
        "good_olist_bq_olist_new_item_indent_adjust_minus_one_normal_bq",
        enable_rules="pml102",
        disable_rules="md005,md027,md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >    properly indented content
   >  1. another list
   >    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "good_olist_bq_olist_new_item_indent_adjust_minus_all_normal_bq",
        enable_rules="pml102",
        disable_rules="md005,md027,md032",
        source_file_contents="""
1. > first list
   > 1. inner list
   >    properly indented content
   >  1. another list
   >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:5: PML102: Disallows lazy list indentation [Expected: 9; Actual: 4] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "good_olist_olist_olist_new_item_indent_normal_normal",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   1. second list
      1. inner list
         properly indented content
      1. another list
         properly indented content
""",
    ),
    pluginRuleTest(
        "bad_olist_olist_olist_new_item_indent_normal_first_minus_one",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   1. second list
      1. inner list
        properly indented content
      1. another list
         properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_olist_new_item_indent_normal_first_minus_four",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   1. second list
      1. inner list
    properly indented content
      1. another list
         properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: PML102: Disallows lazy list indentation [Expected: 9; Actual: 4] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_olist_new_item_indent_normal_first_minus_all",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   1. second list
      1. inner list
properly indented content
      1. another list
         properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 9; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_olist_new_item_indent_normal_second_minus_one",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   1. second list
      1. inner list
         properly indented content
      1. another list
        properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_olist_new_item_indent_normal_second_minus_four",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   1. second list
      1. inner list
         properly indented content
      1. another list
    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:5: PML102: Disallows lazy list indentation [Expected: 9; Actual: 4] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_olist_new_item_indent_normal_second_minus_all",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   1. second list
      1. inner list
         properly indented content
      1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:1: PML102: Disallows lazy list indentation [Expected: 9; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "good_olist_olist_olist_new_item_indent_adjust_normal",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
1. first list
   1. second list
      1. inner list
         properly indented content
       1. another list
          properly indented content
""",
    ),
    pluginRuleTest(
        "bad_olist_olist_olist_new_item_indent_adjust_minus_one",
        disable_rules="md005",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   1. second list
      1. inner list
         properly indented content
       1. another list
         properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:10: PML102: Disallows lazy list indentation [Expected: 10; Actual: 9] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_olist_new_item_indent_adjust_minus_four",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
1. first list
   1. second list
      1. inner list
         properly indented content
       1. another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: PML102: Disallows lazy list indentation [Expected: 10; Actual: 6] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_olist_new_item_indent_adjust_minus_all",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
1. first list
   1. second list
      1. inner list
         properly indented content
       1. another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:1: PML102: Disallows lazy list indentation [Expected: 10; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "good_olist_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_normal",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
""",
    ),
    pluginRuleTest(
        "bad_olist_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_first_minus_one",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. first list
   1. second list
      > inner block
      > inner block
      ----
      first line
     another list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_first_minus_four",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   1. second list
      > inner block
      > inner block
      ----
      first line
 another list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:2: PML102: Disallows lazy list indentation [Expected: 6; Actual: 1] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_first_minus_all",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   1. second list
      > inner block
      > inner block
      ----
      first line
another list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_second_minus_one",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. first list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
   1. second list
      > inner block
      > inner block
      ----
      first line
     another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:14:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_second_minus_four",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
   1. second list
      > inner block
      > inner block
      ----
      first line
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:14:3: PML102: Disallows lazy list indentation [Expected: 6; Actual: 2] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_second_minus_all",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
   1. second list
      > inner block
      > inner block
      ----
      first line
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:14:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "good_olist_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_adjust_normal",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
1. first list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
    1. second list
       > inner block
       > inner block
       ----
       first line
       another list
""",
    ),
    pluginRuleTest(
        "bad_olist_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_adjust_bad_minus_one",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
1. first list
   1. second list
      > inner block
      > inner block
      ----
       first line
      another list
    1. second list
       > inner block
       > inner block
       ----
       first line
      another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:14:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_adjust_bad_minus_four",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
1. first list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
    1. second list
       > inner block
       > inner block
       ----
       first line
   another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:14:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_adjust_bad_minus_all",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
1. first list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
    1. second list
       > inner block
       > inner block
       ----
       first line
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:14:1: PML102: Disallows lazy list indentation [Expected: 7; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "good_olist_bq_bq_closebq_closebq_tb_text_new_item_bq_bq_closebq_closebq_tb_text_indent_normal_normal",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   > > inner block
   > > inner block
   ----
   first line
   another list
1. second list
   > > inner block
   > > inner block
   ----
   first line
   another list
""",
    ),
    pluginRuleTest(
        "bad_olist_bq_bq_closebq_closebq_tb_text_new_item_bq_bq_closebq_closebq_tb_text_indent_normal_first_minus_one",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
1. first list
   > > inner block
   > > inner block
   ----
   first line
  another list
1. second list
   > > inner block
   > > inner block
   ----
   first line
   another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:3: PML102: Disallows lazy list indentation [Expected: 3; Actual: 2] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_bq_bq_closebq_closebq_tb_text_new_item_bq_bq_closebq_closebq_tb_text_indent_normal_first_minus_all",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   > > inner block
   > > inner block
   ----
   first line
another list
1. second list
   > > inner block
   > > inner block
   ----
   first line
   another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_bq_bq_closebq_closebq_tb_text_new_item_bq_bq_closebq_closebq_tb_text_indent_normal_second_minus_one",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   > > inner block
   > > inner block
   ----
   first line
   another list
1. second list
   > > inner block
   > > inner block
   ----
   first line
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:3: PML102: Disallows lazy list indentation [Expected: 3; Actual: 2] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_bq_bq_closebq_closebq_tb_text_new_item_bq_bq_closebq_closebq_tb_text_indent_normal_second_minus_all",
        enable_rules="pml102",
        source_file_contents="""
1. first list
   > > inner block
   > > inner block
   ----
   first line
   another list
1. second list
   > > inner block
   > > inner block
   ----
   first line
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "good_olist_bq_bq_closebq_closebq_tb_text_new_item_bq_bq_closebq_closebq_tb_text_indent_adjust_normal",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
1. first list
   > > inner block
   > > inner block
   ----
   first line
   another list
 1. second list
    > > inner block
    > > inner block
    ----
    first line
    another list
""",
    ),
    pluginRuleTest(
        "bad_olist_bq_bq_closebq_closebq_tb_text_new_item_bq_bq_closebq_closebq_tb_text_indent_adjust_bad_minus_one",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
1. first list
   > > inner block
   > > inner block
   ----
   first line
   another list
 1. second list
    > > inner block
    > > inner block
    ----
    first line
   another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:4: PML102: Disallows lazy list indentation [Expected: 4; Actual: 3] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_olist_bq_bq_closebq_closebq_tb_text_new_item_bq_bq_closebq_closebq_tb_text_indent_adjust_bad_minus_all",
        enable_rules="pml102",
        disable_rules="md005",
        source_file_contents="""
1. first list
   > > inner block
   > > inner block
   ----
   first line
   another list
 1. second list
    > > inner block
    > > inner block
    ----
    first line
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:1: PML102: Disallows lazy list indentation [Expected: 4; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "good_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
>    another list
> 1. second list
>    > block within list
>    ----
>    first line
>    another list
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_first_minus_one_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
>   another list
> 1. second list
>    > block within list
>    ----
>    first line
>    another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_first_minus_all_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
>another list
> 1. second list
>    > block within list
>    ----
>    first line
>    another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:2: PML102: Disallows lazy list indentation [Expected: 5; Actual: 1] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_second_minus_one_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
>    another list
> 1. second list
>    > block within list
>    ----
>    first line
>   another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_second_minus_all_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
>    another list
> 1. second list
>    > block within list
>    ----
>    first line
>another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:2: PML102: Disallows lazy list indentation [Expected: 5; Actual: 1] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_third_minus_one_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
>    another list
> 1. second list
>    > block within list
>    ----
>    first line
>    another list
> 1. third list
>    > block within list
>    ----
>    first line
>   another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:18:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_third_minus_all_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
>    another list
> 1. second list
>    > block within list
>    ----
>    first line
>    another list
> 1. third list
>    > block within list
>    ----
>    first line
>another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:18:2: PML102: Disallows lazy list indentation [Expected: 5; Actual: 1] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "good_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_adjust_normal",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
>    another list
>  1. second list
>     > block within list
>     ----
>     first line
>     another list
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_adjust_minus_one_bq",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
>    another list
>  1. second list
>     > block within list
>     ----
>     first line
>    another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_adjust_minus_four_bq",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
>    another list
>  1. second list
>     > block within list
>     ----
>     first line
> another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:3: PML102: Disallows lazy list indentation [Expected: 6; Actual: 2] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_adjust_minus_all_bq",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
>    another list
>  1. second list
>     > block within list
>     ----
>     first line
>another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:2: PML102: Disallows lazy list indentation [Expected: 6; Actual: 1] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "good_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_normal_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
     another list
> 1. second list
>    > block within list
>    ----
>    first line
     another list
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_first_minus_one_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
    another list
> 1. second list
>    > block within list
>    ----
>    first line
     another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_first_minus_all_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
another list
> 1. second list
>    > block within list
>    ----
>    first line
>    another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:1: PML102: Disallows lazy list indentation [Expected: 5; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_second_minus_one_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
     another list
> 1. second list
>    > block within list
>    ----
>    first line
    another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_second_minus_all_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
     another list
> 1. second list
>    > block within list
>    ----
>    first line
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:1: PML102: Disallows lazy list indentation [Expected: 5; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_third_minus_one_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
     another list
> 1. second list
>    > block within list
>    ----
>    first line
     another list
> 1. third list
>    > block within list
>    ----
>    first line
    another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:18:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_normal_third_minus_all_no_bq",
        enable_rules="pml102",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
     another list
> 1. second list
>    > block within list
>    ----
>    first line
     another list
> 1. third list
>    > block within list
>    ----
>    first line
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:18:1: PML102: Disallows lazy list indentation [Expected: 5; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "good_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_adjust_normal_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
     another list
>  1. second list
>     > block within list
>     ----
>     first line
      another list
""",
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_adjust_minus_one_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
     another list
>  1. second list
>     > block within list
>     ----
>     first line
     another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_adjust_minus_four_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
     another list
>  1. second list
>     > block within list
>     ----
>     first line
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:3: PML102: Disallows lazy list indentation [Expected: 6; Actual: 2] (disallow-lazy-list-indentation)"""
    ),
    pluginRuleTest(
        "bad_bq_olist_bq_closebq_tb_text_new_item_bq_closebq_tb_text_indent_adjust_minus_all_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md027",
        source_file_contents="""
> block start
>
> 1. first list
>    > block within list
>    ----
>    first line
     another list
>  1. second list
>     > block within list
>     ----
>     first line
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)"""
    ),
]
    # TODO add sets of tests with ulist instead of olist



@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_pml102_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin pml102.
    """
    execute_scan_test(test, "pml102")


def test_pml102_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "pml102",
        """
  ITEM               DESCRIPTION

  Id                 pml102
  Name(s)            disallow-lazy-list-indentation
  Short Description  Disallows lazy list indentation
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     pml102.md


""",
    )
    execute_query_configuration_test(config_test)
