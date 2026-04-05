"""
Module to provide tests related to the PMl102 rule.
"""

from test.rules.utils import pluginRuleTest
from typing import List

scanTests_olist_olist: List[pluginRuleTest] = [
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
]
