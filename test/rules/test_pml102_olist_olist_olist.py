"""
Module to provide tests related to the PMl102 rule.
"""

from typing import List

from test.rules.utils import (
    pluginRuleTest,
)

scanTests_olist_olist_olist: List[pluginRuleTest] = [
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
        scan_expected_output="""{temp_source_path}:5:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:5:5: PML102: Disallows lazy list indentation [Expected: 9; Actual: 4] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 9; Actual: 0] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:7:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:7:5: PML102: Disallows lazy list indentation [Expected: 9; Actual: 4] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:7:1: PML102: Disallows lazy list indentation [Expected: 9; Actual: 0] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:7:10: PML102: Disallows lazy list indentation [Expected: 10; Actual: 9] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:7:7: PML102: Disallows lazy list indentation [Expected: 10; Actual: 6] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:7:1: PML102: Disallows lazy list indentation [Expected: 10; Actual: 0] (disallow-lazy-list-indentation)""",
    ),
]
