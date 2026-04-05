"""
Module to provide tests related to the PMl102 rule.
"""

from test.rules.utils import pluginRuleTest
from typing import List

scanTests_ulist_ulist: List[pluginRuleTest] = [
    pluginRuleTest(
        "good_double_ulist_indent_normal",
        enable_rules="pml102",
        source_file_contents="""
+ a list
  + another list
    properly indented content
""",
    ),
    pluginRuleTest(
        "bad_double_ulist_indent_minus_one",
        enable_rules="pml102",
        source_file_contents="""
+ a list
  + another list
   almost properly indented content (-1 indent)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: PML102: Disallows lazy list indentation [Expected: 4; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_double_ulist_indent_minus_three",
        enable_rules="pml102",
        source_file_contents="""+ a list
  + another list
 almost properly indented content (-3 indent)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: PML102: Disallows lazy list indentation [Expected: 4; Actual: 1] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_double_ulist_indent_minus_all",
        enable_rules="pml102",
        source_file_contents="""
+ a list
  + another list
almost properly indented content (-4 indent)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: PML102: Disallows lazy list indentation [Expected: 4; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_double_ulist_indent_plus_one",
        enable_rules="pml102",
        source_file_contents="""+ a list
  + another list
     almost properly indented content (+1 indent)
""",
    ),
    pluginRuleTest(
        "good_double_ulist_new_item_indent_normal",
        enable_rules="pml102",
        source_file_contents="""
+ a list
  + another list
    properly indented content
  + another list
    properly indented content
""",
    ),
    pluginRuleTest(
        "bad_double_ulist_new_item_indent_normal_first_minus_one",
        enable_rules="pml102",
        source_file_contents="""
+ a list
  + another list
   properly indented content
  + another list
    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: PML102: Disallows lazy list indentation [Expected: 4; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_double_ulist_new_item_indent_normal_first_minus_all",
        enable_rules="pml102",
        source_file_contents="""
+ a list
  + another list
properly indented content
  + another list
    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: PML102: Disallows lazy list indentation [Expected: 4; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_double_ulist_new_item_indent_normal_second_minus_one",
        enable_rules="pml102",
        source_file_contents="""
+ a list
  + another list
    properly indented content
  + another list
   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:4: PML102: Disallows lazy list indentation [Expected: 4; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_double_ulist_new_item_indent_normal_second_minus_all",
        enable_rules="pml102",
        source_file_contents="""
+ a list
  + another list
    properly indented content
  + another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 4; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_double_ulist_new_item_adjust_indent_normal",
        enable_rules="pml102",
        disable_rules="md005,md007",
        source_file_contents="""
+ a list
  + another list
    properly indented content
   + another list
     properly indented content
""",
    ),
    pluginRuleTest(
        "bad_double_ulist_new_item_adjust_indent_minus_one",
        enable_rules="pml102",
        disable_rules="md005,md007",
        source_file_contents="""
+ a list
  + another list
    properly indented content
   + another list
    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_double_ulist_new_item_adjust_indent_minus_all",
        enable_rules="pml102",
        disable_rules="md005,md007",
        source_file_contents="""
+ a list
  + another list
    properly indented content
   + another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 5; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
]
