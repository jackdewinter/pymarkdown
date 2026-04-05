"""
Module to provide tests related to the PMl102 rule.
"""

from test.rules.utils import pluginRuleTest
from typing import List

scanTests_olist_olist_bq: List[pluginRuleTest] = [
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
        scan_expected_output="""{temp_source_path}:8:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:8:2: PML102: Disallows lazy list indentation [Expected: 6; Actual: 1] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:8:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:14:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:14:3: PML102: Disallows lazy list indentation [Expected: 6; Actual: 2] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:14:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:14:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:14:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:14:1: PML102: Disallows lazy list indentation [Expected: 7; Actual: 0] (disallow-lazy-list-indentation)""",
    ),
]
