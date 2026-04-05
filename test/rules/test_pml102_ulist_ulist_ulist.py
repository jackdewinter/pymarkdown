"""
Module to provide tests related to the PMl102 rule.
"""

from test.rules.utils import pluginRuleTest
from typing import List

scanTests_ulist_ulist_ulist: List[pluginRuleTest] = [
    pluginRuleTest(
        "good_ulist_ulist_ulist_new_item_indent_normal_normal",
        enable_rules="pml102",
        source_file_contents="""
+ first list
  + second list
    + inner list
      properly indented content
    + another list
      properly indented content
""",
    ),
    pluginRuleTest(
        "bad_ulist_ulist_ulist_new_item_indent_normal_first_minus_one",
        enable_rules="pml102",
        source_file_contents="""
+ first list
  + second list
    + inner list
     properly indented content
    + another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "bad_ulist_ulist_ulist_new_item_indent_normal_first_minus_four",
        enable_rules="pml102",
        source_file_contents="""
+ first list
  + second list
    + inner list
 properly indented content
    + another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:2: PML102: Disallows lazy list indentation [Expected: 6; Actual: 1] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "bad_ulist_ulist_ulist_new_item_indent_normal_first_minus_all",
        enable_rules="pml102",
        source_file_contents="""
+ first list
  + second list
    + inner list
properly indented content
    + another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "bad_ulist_ulist_ulist_new_item_indent_normal_second_minus_one",
        enable_rules="pml102",
        source_file_contents="""
+ first list
  + second list
    + inner list
      properly indented content
    + another list
     properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "bad_ulist_ulist_ulist_new_item_indent_normal_second_minus_four",
        enable_rules="pml102",
        source_file_contents="""
+ first list
  + second list
    + inner list
      properly indented content
    + another list
 properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:2: PML102: Disallows lazy list indentation [Expected: 6; Actual: 1] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "bad_ulist_ulist_ulist_new_item_indent_normal_second_minus_all",
        enable_rules="pml102",
        source_file_contents="""
+ first list
  + second list
    + inner list
      properly indented content
    + another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "good_ulist_ulist_ulist_new_item_indent_adjust_normal",
        enable_rules="pml102",
        disable_rules="md005,md007",
        source_file_contents="""
+ first list
  + second list
    + inner list
      properly indented content
     + another list
       properly indented content
""",
    ),
    pluginRuleTest(
        "bad_ulist_ulist_ulist_new_item_indent_adjust_minus_one",
        disable_rules="md005,md007",
        enable_rules="pml102",
        source_file_contents="""
+ first list
  + second list
    + inner list
      properly indented content
     + another list
      properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: PML102: Disallows lazy list indentation [Expected: 7; Actual: 6] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "bad_ulist_ulist_ulist_new_item_indent_adjust_minus_four",
        enable_rules="pml102",
        disable_rules="md005,md007",
        source_file_contents="""
+ first list
  + second list
    + inner list
      properly indented content
     + another list
   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:4: PML102: Disallows lazy list indentation [Expected: 7; Actual: 3] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "bad_ulist_ulist_ulist_new_item_indent_adjust_minus_all",
        enable_rules="pml102",
        disable_rules="md005,md007",
        source_file_contents="""
+ first list
  + second list
    + inner list
      properly indented content
     + another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:1: PML102: Disallows lazy list indentation [Expected: 7; Actual: 0] (disallow-lazy-list-indentation)""",
    ),
]
