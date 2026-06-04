"""
Module to provide tests related to the PMl102 rule.
"""

from test.rules.test_pml102_bq_bq_olist import scanTests_bq_bq_olist
from test.rules.test_pml102_bq_bq_ulist import scanTests_bq_bq_ulist
from test.rules.test_pml102_bq_olist import scanTests_bq_olist
from test.rules.test_pml102_bq_olist_bq import scanTests_bq_olist_bq
from test.rules.test_pml102_bq_olist_olist import scanTests_bq_olist_olist
from test.rules.test_pml102_bq_ulist import scanTests_bq_ulist
from test.rules.test_pml102_bq_ulist_bq import scanTests_bq_ulist_bq
from test.rules.test_pml102_bq_ulist_ulist import scanTests_bq_ulist_ulist
from test.rules.test_pml102_olist_bq_bq import scanTests_olist_bq_bq
from test.rules.test_pml102_olist_bq_olist import scanTests_olist_bq_olist
from test.rules.test_pml102_olist_olist import scanTests_olist_olist
from test.rules.test_pml102_olist_olist_bq import scanTests_olist_olist_bq
from test.rules.test_pml102_olist_olist_olist import scanTests_olist_olist_olist
from test.rules.test_pml102_ulist_bq_bq import scanTests_ulist_bq_bq
from test.rules.test_pml102_ulist_bq_ulist import scanTests_ulist_bq_ulist
from test.rules.test_pml102_ulist_ulist import scanTests_ulist_ulist
from test.rules.test_pml102_ulist_ulist_bq import scanTests_ulist_ulist_bq
from test.rules.test_pml102_ulist_ulist_ulist import scanTests_ulist_ulist_ulist
from test.rules.utils import (
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginQueryConfigTest,
    pluginRuleTest,
)
from typing import List

import pytest

scanTests: List[pluginRuleTest] = [
    pluginRuleTest(
        "good_single_olist_indent_normal_single_line",
        enable_rules="pml102",
        source_file_contents="""1. a list
""",
    ),
    pluginRuleTest(
        "good_single_olist_indent_normal_double_line",
        enable_rules="pml102",
        source_file_contents="""1. a list
   properly indented content
""",
    ),
    pluginRuleTest(
        "good_single_olist_indent_normal_atx_para",
        enable_rules="pml102",
        source_file_contents="""1. ## bob

   a list
   properly indented content
""",
    ),
    pluginRuleTest(
        "good_single_olist_indent_normal_para_atx_para",
        enable_rules="pml102",
        source_file_contents="""1. first lines
   of list

   ## bob

   a list
   properly indented content
""",
    ),
    pluginRuleTest(
        "bad_single_olist_indent_minus_one",
        enable_rules="pml102",
        source_file_contents="""
1. a list
  almost properly indented content (-1 indent)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: PML102: Disallows lazy list indentation [Expected: 3; Actual: 2] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_olist_indent_minus_all",
        enable_rules="pml102",
        source_file_contents="""
1. a list
almost properly indented content (-1 indent)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_single_olist_indent_plus_one",
        enable_rules="pml102",
        source_file_contents="""
1. a list
    almost properly indented content (+1 indent)
""",
    ),
    pluginRuleTest(
        "good_single_olist_new_item_indent_normal",
        enable_rules="pml102",
        source_file_contents="""
1. a list
   properly indented content
2. a list
   properly indented content
""",
    ),
    pluginRuleTest(
        "bad_single_olist_new_item_indent_minus_one_minus_two",
        enable_rules="pml102",
        source_file_contents="""
1. a list
  properly indented content
2. a list
 properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: PML102: Disallows lazy list indentation [Expected: 3; Actual: 2] (disallow-lazy-list-indentation)
{temp_source_path}:5:2: PML102: Disallows lazy list indentation [Expected: 3; Actual: 1] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_olist_new_item_indent_minus_all",
        enable_rules="pml102",
        source_file_contents="""
1. a list
properly indented content
2. a list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)
{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_single_olist_new_item_adjust_indent_normal",
        enable_rules="pml102",
        disable_rules="md005,md030",
        source_file_contents="""
1. a list
   properly indented content
 2. a list
    properly indented content
""",
    ),
    pluginRuleTest(
        "bad_single_olist_new_item_adjust_indent_first_minus_two",
        enable_rules="pml102",
        disable_rules="md005,md030",
        source_file_contents="""
1. a list
 properly indented content
 2. a list
    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: PML102: Disallows lazy list indentation [Expected: 3; Actual: 1] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_olist_new_item_adjust_indent_first_minus_all",
        enable_rules="pml102",
        disable_rules="md005,md030",
        source_file_contents="""
1. a list
properly indented content
 2. a list
    properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_olist_new_item_adjust_indent_second_minus_one",
        enable_rules="pml102",
        disable_rules="md005,md030",
        source_file_contents="""
1. a list
   properly indented content
 2. a list
   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: PML102: Disallows lazy list indentation [Expected: 4; Actual: 3] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_olist_new_item_adjust_indent_second_minus_all",
        enable_rules="pml102",
        disable_rules="md005,md030",
        source_file_contents="""
1. a list
   properly indented content
 2. a list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 4; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_single_ulist_indent_normal_single_line",
        enable_rules="pml102",
        source_file_contents="""+ a list
""",
    ),
    pluginRuleTest(
        "good_single_ulist_indent_normal_double_line",
        enable_rules="pml102",
        source_file_contents="""+ a list
  properly indented content
""",
    ),
    pluginRuleTest(
        "good_single_ulist_indent_normal_atx_para",
        enable_rules="pml102",
        source_file_contents="""+ ## bob

  a list
  properly indented content
""",
    ),
    pluginRuleTest(
        "good_single_ulist_indent_normal_para_atx_para",
        enable_rules="pml102",
        source_file_contents="""+ first lines
  of list

  ## bob

  a list
  properly indented content
""",
    ),
    pluginRuleTest(
        "bad_single_ulist_indent_minus_one",
        enable_rules="pml102",
        source_file_contents="""
+ a list
 almost properly indented content (-1 indent)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: PML102: Disallows lazy list indentation [Expected: 2; Actual: 1] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_ulist_indent_minus_all",
        enable_rules="pml102",
        source_file_contents="""
+ a list
almost properly indented content (-1 indent)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: PML102: Disallows lazy list indentation [Expected: 2; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_single_ulist_indent_plus_one",
        enable_rules="pml102",
        source_file_contents="""
+ a list
   almost properly indented content (+1 indent)
""",
    ),
    pluginRuleTest(
        "good_single_ulist_new_item_indent_normal",
        enable_rules="pml102",
        source_file_contents="""
+ a list
  properly indented content
+ a list
  properly indented content
""",
    ),
    pluginRuleTest(
        "bad_single_ulist_new_item_indent_minus_one_minus_two",
        enable_rules="pml102",
        source_file_contents="""
+ a list
 properly indented content
+ a list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: PML102: Disallows lazy list indentation [Expected: 2; Actual: 1] (disallow-lazy-list-indentation)
{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 2; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_ulist_new_item_indent_minus_all",
        enable_rules="pml102",
        source_file_contents="""
+ a list
properly indented content
+ a list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: PML102: Disallows lazy list indentation [Expected: 2; Actual: 0] (disallow-lazy-list-indentation)
{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 2; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_single_ulist_new_item_adjust_indent_normal",
        enable_rules="pml102",
        disable_rules="md005,md007,md030",
        source_file_contents="""
+ a list
  properly indented content
 + a list
   properly indented content
""",
    ),
    pluginRuleTest(
        "bad_single_ulist_new_item_adjust_indent_first_minus_two",
        enable_rules="pml102",
        disable_rules="md005,md007,md030",
        source_file_contents="""
+ a list
properly indented content
 + a list
   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: PML102: Disallows lazy list indentation [Expected: 2; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_ulist_new_item_adjust_indent_first_minus_all",
        enable_rules="pml102",
        disable_rules="md005,md007,md030",
        source_file_contents="""
+ a list
properly indented content
 + a list
   properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: PML102: Disallows lazy list indentation [Expected: 2; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_ulist_new_item_adjust_indent_second_minus_one",
        enable_rules="pml102",
        disable_rules="md005,md007,md030",
        source_file_contents="""
+ a list
  properly indented content
 + a list
  properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: PML102: Disallows lazy list indentation [Expected: 3; Actual: 2] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "bad_single_ulist_new_item_adjust_indent_second_minus_all",
        enable_rules="pml102",
        disable_rules="md005,md007,md030",
        source_file_contents="""
+ a list
  properly indented content
 + a list
properly indented content
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)
""",
    ),
    pluginRuleTest(
        "good_single_ulist_new_item_indent_normal_test",
        enable_rules="pml102",
        disable_rules="md012",
        source_file_contents="""
- taking a second pass at the outputs from the recent `fix` addition, re-verifying
  the output and fixing any issues
- cleaning up documentation to properly note what type of whitespace is used
  in the core and well as various extensions and plugins
- for parsers like Python-Markdown, used in the MkDocs tools, added Rule Pml101
  to handle the different indentation requirements
""",
        scan_expected_return_code=0,
        # scan_expected_output="""{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "good_single_ulist_new_item_indent_normal_with_sublists",
        enable_rules="pml102",
        disable_rules="md012",
        source_file_contents="""
- taking a second pass at the outputs from the recent `fix` addition, re-verifying
  the output and fixing any issues
- cleaning up documentation to properly note what type of whitespace is used
  in the core and well as various extensions and plugins
  - at the same time, clearly followed the specification on what kind of whitespace
    to use, instead of allowing unicode whitespace by default
- for parsers like Python-Markdown, used in the MkDocs tools, added Rule Pml101
  to handle the different indentation requirements
  - note that this new rule give advice against Md007, so only one of the two
    rules should be enabled at any one time
""",
        scan_expected_return_code=0,
        # scan_expected_output="""{temp_source_path}:5:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "issue-1588-full-text",
        enable_rules="pml102",
        disable_rules="md007,md012",
        source_file_contents="""
1. **You have a concrete idea.**

    - Read our feedback carefully. We review each issue seriously and try to be clear
      about constraints and priorities.
    - If the idea is important to you, contributing is often the best way to move
      it forward while still respecting the project's direction.
    - While your idea may not fit our roadmap, we can work with you to figure out
      if your idea has merit outside of our project, and how you can realize that.

2. **You want to help but do not have a specific idea yet.**  

    You might be looking for something you can
    [sink your teeth into](https://dictionary.cambridge.org/dictionary/english/sink-teeth-into),
    want to build your open-source resume, or just want to explore the project.
""",
    ),
    pluginRuleTest(
        "issue-1588-level-2-lists",
        enable_rules="pml102",
        disable_rules="md012",
        source_file_contents="""
1. list 1
   - list 1.1 - line 1
     list 1.1 - line 2
   - list 1.2 - line 1
     list 1.2 - line 2
   - list 1.3 - line 1
     list 1.3 - line 2
2. list 2
   - list 2.2 - line 1
   - list 2.2 - line 2
""",
    ),
    pluginRuleTest(
        "issue-1588-level-2-paragraph-good",
        enable_rules="pml102",
        disable_rules="md012",
        source_file_contents="""
1. list 1 - line 1
   - list 1.1 - line 1
     list 1.1 - line 2
   - list 1.2 - line 1
     list 1.2 - line 2
   - list 1.3 - line 1
     list 1.3 - line 2
2. list 2 - line 1
   list 2 - line 2
   list 2 - line 3
""",
    ),
    pluginRuleTest(
        "issue-1588-level-2-paragraph-bad",
        enable_rules="pml102",
        disable_rules="md012",
        source_file_contents="""
1. list 1 - line 1
   - list 1.1 - line 1
     list 1.1 - line 2
   - list 1.2 - line 1
     list 1.2 - line 2
   - list 1.3 - line 1
     list 1.3 - line 2
2. list 2 - line 1
 list 2 - line 2
 list 2 - line 3
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:10:2: PML102: Disallows lazy list indentation [Expected: 3; Actual: 1] (disallow-lazy-list-indentation)
{temp_source_path}:11:2: PML102: Disallows lazy list indentation [Expected: 3; Actual: 1] (disallow-lazy-list-indentation)        
""",
    ),
    pluginRuleTest(
        "issue-1588-level-2-paragraphs-2-good",
        enable_rules="pml102",
        disable_rules="md012",
        source_file_contents="""
1. list 1 - line 1
   - list 1.1 - line 1
     list 1.1 - line 2
   - list 1.2 - line 1
     list 1.2 - line 2
   - list 1.3 - line 1
     list 1.3 - line 2
2. list 2 - para 1 - line 1

   list 2 - para 2 - line 1
   list 2 - para 2 - line 2
""",
    ),
    pluginRuleTest(
        "issue-1588-level-2-paragraphs-2-bad",
        enable_rules="pml102",
        disable_rules="md012",
        source_file_contents="""
1. list 1 - line 1
   - list 1.1 - line 1
     list 1.1 - line 2
   - list 1.2 - line 1
     list 1.2 - line 2
   - list 1.3 - line 1
     list 1.3 - line 2
2. list 2 - para 1 - line 1

   list 2 - para 2 - line 1
  list 2 - para 2 - line 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:12:3: PML102: Disallows lazy list indentation [Expected: 3; Actual: 2] (disallow-lazy-list-indentation)""",
    ),
    pluginRuleTest(
        "issue-1588-level-2-paragraphs-3-good",
        enable_rules="pml102",
        disable_rules="md012,md009",
        source_file_contents="""
1. list 1 - line 1
   - list 1.1 - line 1
     list 1.1 - line 2
   - list 1.2 - line 1
     list 1.2 - line 2
   - list 1.3 - line 1
     list 1.3 - line 2
2. list 2 - para 1 - line 1

   list 2 - para 2 - line 1
   list 2 - para 2 - line 2

   list 2 - para 3 - line 1
   list 2 - para 3 - line 2
""",
    ),
    pluginRuleTest(
        "issue-1588-level-2-paragraphs-3-bad",
        enable_rules="pml102",
        disable_rules="md012,md009",
        source_file_contents="""
1. list 1 - line 1
   - list 1.1 - line 1
     list 1.1 - line 2
   - list 1.2 - line 1
     list 1.2 - line 2
   - list 1.3 - line 1
     list 1.3 - line 2
2. list 2 - para 1 - line 1

   list 2 - para 2 - line 1
   list 2 - para 2 - line 2

   list 2 - para 3 - line 1
list 2 - para 3 - line 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:15:1: PML102: Disallows lazy list indentation [Expected: 3; Actual: 0] (disallow-lazy-list-indentation)""",
    ),
]


all_scan_tests: List[pluginRuleTest] = []
all_scan_tests.extend(scanTests)

# No bq, bq, as no list portion.
all_scan_tests.extend(scanTests_bq_olist)
all_scan_tests.extend(scanTests_bq_ulist)
all_scan_tests.extend(scanTests_olist_olist)
all_scan_tests.extend(scanTests_ulist_ulist)

# No bq_bq_bq as no list portion.
all_scan_tests.extend(scanTests_bq_bq_olist)
all_scan_tests.extend(scanTests_bq_bq_ulist)
all_scan_tests.extend(scanTests_bq_olist_bq)
all_scan_tests.extend(scanTests_bq_ulist_bq)
all_scan_tests.extend(scanTests_bq_olist_olist)
all_scan_tests.extend(scanTests_bq_ulist_ulist)
all_scan_tests.extend(scanTests_olist_bq_bq)
all_scan_tests.extend(scanTests_ulist_bq_bq)
all_scan_tests.extend(scanTests_olist_bq_olist)
all_scan_tests.extend(scanTests_ulist_bq_ulist)
all_scan_tests.extend(scanTests_olist_olist_bq)
all_scan_tests.extend(scanTests_olist_olist_olist)
all_scan_tests.extend(scanTests_ulist_ulist_ulist)
all_scan_tests.extend(scanTests_ulist_ulist_bq)


@pytest.mark.rules
@pytest.mark.parametrize("test", all_scan_tests, ids=id_test_plug_rule_fn)
def test_pml102_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin pml102.
    """
    execute_scan_test(test, "pml102")


@pytest.mark.rules
def test_pml102_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "pml102",
        """
  ITEM               DESCRIPTION

  Id                 pml102
  Name(s)            disallow-lazy-list-indentation
  Short Description  Disallows lazy list indentation
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     pml102.md


""",
    )
    execute_query_configuration_test(config_test)
