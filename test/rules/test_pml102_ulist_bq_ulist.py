"""
Module to provide tests related to the PMl102 rule.
"""

from test.rules.utils import pluginRuleTest
from typing import List

scanTests_ulist_bq_ulist: List[pluginRuleTest] = [
    pluginRuleTest(
        "good_ulist_bq_ulist_new_item_indent_normal_normal_both_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
      properly indented content
  > + another list
      properly indented content
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_first_minus_one_both_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
     properly indented content
  > + another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_first_minus_all_both_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
properly indented content
  > + another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_second_minus_one_both_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
      properly indented content
  > + another list
     properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_olist_bq_olist_new_item_indent_normal_second_minus_all_both_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
      properly indented content
  > + another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_ulist_bq_ulist_new_item_indent_adjust_normal_both_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027,md032",
        source_file_contents="""
+ > first list
  > + inner list
      properly indented content
  >  + another list
       properly indented content
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_adjust_minus_one_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027,md032",
        source_file_contents="""
+ > first list
  > + inner list
      properly indented content
  >  + another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_adjust_minus_all_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027,md032",
        source_file_contents="""
+ > first list
  > + inner list
      properly indented content
  >  + another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 7; Actual: 0] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "good_ulist_bq_ulist_new_item_indent_normal_normal_first_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
  >   properly indented content
  > + another list
      properly indented content
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_first_minus_one_first_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
  >  properly indented content
  > + another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_first_minus_all_first_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
  >properly indented content
  > + another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: PML102: Disallows lazy list indentation [Expected: 6; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_second_minus_one_first_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
  >   properly indented content
  > + another list
     properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_second_minus_all_first_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
  >   properly indented content
  > + another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_ulist_bq_ulist_new_item_indent_adjust_normal_first_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027,md032",
        source_file_contents="""
+ > first list
  > + inner list
      properly indented content
  >  + another list
  >    properly indented content
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_adjust_minus_one_first_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027,md032",
        source_file_contents="""
+ > first list
  > + inner list
      properly indented content
  >  + another list
  >   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_adjust_minus_all_first_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027,md032",
        source_file_contents="""
+ > first list
  > + inner list
      properly indented content
  >  + another list
  >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_ulist_bq_ulist_new_item_indent_normal_normal_second_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
      properly indented content
  > + another list
  >   properly indented content
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_first_minus_one_second_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
     properly indented content
  > + another list
  >   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_first_minus_all_second_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
properly indented content
  > + another list
  >   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_second_minus_one_second_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
      properly indented content
  > + another list
  >  properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_second_minus_all_second_no_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
      properly indented content
  > + another list
  >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:4: PML102: Disallows lazy list indentation [Expected: 6; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_ulist_bq_ulist_new_item_indent_adjust_normal_second_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027,md032",
        source_file_contents="""
+ > first list
  > + inner list
  >   properly indented content
  >  + another list
       properly indented content
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_adjust_minus_one_second_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027,md032",
        source_file_contents="""
+ > first list
  > + inner list
  >   properly indented content
  >  + another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_adjust_minus_all_second_no_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027,md032",
        source_file_contents="""
+ > first list
  > + inner list
  >   properly indented content
  >  + another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 7; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_ulist_bq_ulist_new_item_indent_normal_normal_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
  >   properly indented content
  > + another list
  >   properly indented content
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_first_minus_one_normal_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
  >  properly indented content
  > + another list
  >   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_first_minus_all_normal_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
  >properly indented content
  > + another list
  >   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: PML102: Disallows lazy list indentation [Expected: 6; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_second_minus_one_normal_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
  >   properly indented content
  > + another list
  >  properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_ulist_bq_ulist_new_item_indent_normal_second_minus_all_normal_bq",
        enable_rules="pml102",
        disable_rules="md032",
        source_file_contents="""
+ > first list
  > + inner list
  >   properly indented content
  > + another list
  >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:4: PML102: Disallows lazy list indentation [Expected: 6; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_ulist_bq_ulist_new_item_indent_adjust_normal_normal_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027,md032",
        source_file_contents="""
+ > first list
  > + inner list
  >   properly indented content
  >  + another list
  >    properly indented content
""",
    ),
    pluginRuleTest(
        "good_ulist_bq_ulist_new_item_indent_adjust_minus_one_normal_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027,md032",
        source_file_contents="""
+ > first list
  > + inner list
  >   properly indented content
  >  + another list
  >   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "good_ulist_bq_ulist_new_item_indent_adjust_minus_all_normal_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027,md032",
        source_file_contents="""
+ > first list
  > + inner list
  >   properly indented content
  >  + another list
  >properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)""",
    ),
]
