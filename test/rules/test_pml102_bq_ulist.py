"""
Module to provide tests related to the PMl102 rule.
"""

from test.rules.utils import pluginRuleTest
from typing import List

scanTests_bq_ulist: List[pluginRuleTest] = [
    pluginRuleTest(
        "good_bq_ulist_indent_normal",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
    properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_ulist_indent_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
>   properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_ulist_indent_minus_one",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: PML102: Disallows lazy list indentation [Expected: 4; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_bq_ulist_indent_minus_all",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 4; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_bq_ulist_indent_minus_one_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
>  properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: PML102: Disallows lazy list indentation [Expected: 4; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_bq_ulist_indent_minus_all_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
>properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:2: PML102: Disallows lazy list indentation [Expected: 4; Actual: 1] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_bq_ulist_indent_plus_one",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
     properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_ulist_indent_plus_one_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
>    properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_ulist_new_item_indent_normal",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
    properly indented content
> + another list
    properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_ulist_new_item_indent_normal_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
>   properly indented content
> + another list
>   properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_ulist_new_item_indent_first_minus_one",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
   properly indented content
> + another list
    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: PML102: Disallows lazy list indentation [Expected: 4; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_bq_ulist_new_item_indent_first_minus_all",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
properly indented content
> + another list
    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 4; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_bq_ulist_new_item_indent_second_minus_one_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
>   properly indented content
> + another list
>  properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:4: PML102: Disallows lazy list indentation [Expected: 4; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_bq_ulist_new_item_indent_second_minus_all_bq",
        enable_rules="pml102",
        source_file_contents="""
> a block
>
> + another list
>   properly indented content
> + another list
>properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:2: PML102: Disallows lazy list indentation [Expected: 4; Actual: 1] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_bq_ulist_new_item_adjust_indent_normal",
        enable_rules="pml102",
        disable_rules="md005,md007,md027",
        source_file_contents="""
> a block
>
> + another list
    properly indented content
>  + another list
     properly indented content
""",
    ),
    pluginRuleTest(
        "good_bq_ulist_new_item_adjust_indent_normal_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027",
        source_file_contents="""
> a block
>
> + another list
>   properly indented content
>  + another list
>    properly indented content
""",
    ),
    pluginRuleTest(
        "bad_bq_ulist_new_item_adjust_indent_minus_one",
        enable_rules="pml102",
        disable_rules="md005,md007,md027",
        source_file_contents="""
> a block
>
> + another list
    properly indented content
>  + another list
    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_bq_ulist_new_item_adjust_indent_second_minus_one_bq",
        enable_rules="pml102",
        disable_rules="md005,md007,md027",
        source_file_contents="""
> a block
>
> + another list
>   properly indented content
>  + another list
>   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)
""",
    ),
]
