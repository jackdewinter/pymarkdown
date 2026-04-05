"""
Module to provide tests related to the PMl102 rule.
"""

from test.rules.utils import pluginRuleTest
from typing import List

scanTests_bq_olist_bq: List[pluginRuleTest] = [
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
        scan_expected_output="""{temp_source_path}:8:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:8:2: PML102: Disallows lazy list indentation [Expected: 5; Actual: 1] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:13:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:13:2: PML102: Disallows lazy list indentation [Expected: 5; Actual: 1] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:18:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:18:2: PML102: Disallows lazy list indentation [Expected: 5; Actual: 1] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:13:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:13:3: PML102: Disallows lazy list indentation [Expected: 6; Actual: 2] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:13:2: PML102: Disallows lazy list indentation [Expected: 6; Actual: 1] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:8:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:8:1: PML102: Disallows lazy list indentation [Expected: 5; Actual: 0] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:13:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:13:1: PML102: Disallows lazy list indentation [Expected: 5; Actual: 0] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:18:5: PML102: Disallows lazy list indentation [Expected: 5; Actual: 4] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:18:1: PML102: Disallows lazy list indentation [Expected: 5; Actual: 0] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:13:6: PML102: Disallows lazy list indentation [Expected: 6; Actual: 5] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:13:3: PML102: Disallows lazy list indentation [Expected: 6; Actual: 2] (disallow-lazy-list-indentation)""",
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
        scan_expected_output="""{temp_source_path}:13:1: PML102: Disallows lazy list indentation [Expected: 6; Actual: 0] (disallow-lazy-list-indentation)""",
    ),
]
