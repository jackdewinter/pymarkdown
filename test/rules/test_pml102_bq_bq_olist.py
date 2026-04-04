"""
Module to provide tests related to the PMl102 rule.
"""

from test.rules.utils import pluginRuleTest
from typing import List

scanTests_bq_bq_olist: List[pluginRuleTest] = [
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
        scan_expected_output="""{temp_source_path}:7:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:7:8: PML102: Disallows lazy list indentation [Expected: 8; Actual: 7] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:7:4: PML102: Disallows lazy list indentation [Expected: 8; Actual: 3] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:7:1: PML102: Disallows lazy list indentation [Expected: 8; Actual: 0] (disallow-lazy-list-indentation)""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
    ),
    pluginRuleTest(
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
    ),
]
