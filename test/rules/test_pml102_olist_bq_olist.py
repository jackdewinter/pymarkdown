"""
Module to provide tests related to the PMl102 rule.
"""

from typing import List

from test.rules.utils import (
    pluginRuleTest,
)

scanTests_olist_bq_olist: List[pluginRuleTest] = [
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
""",
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
""",
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
""",
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
""",
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
        scan_expected_output="""{temp_source_path}:6:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:6:1: PML102: Disallows lazy list indentation [Expected: 9; Actual: 0] (disallow-lazy-list-indentation)""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
""",
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
        scan_expected_output="""{temp_source_path}:6:9: PML102: Disallows lazy list indentation [Expected: 9; Actual: 8] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:6:5: PML102: Disallows lazy list indentation [Expected: 9; Actual: 4] (disallow-lazy-list-indentation)""",
    ),
]
