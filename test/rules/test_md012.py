"""
Module to provide tests related to the MD012 rule.
"""

import os
from test.rules.utils import (
    execute_configuration_test,
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginConfigErrorTest,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md012") + os.sep

configTests = [
    pluginConfigErrorTest(
        "bad_configuration_maximum",
        use_strict_config=True,
        set_args=["plugins.md012.maximum=$#-2"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md012.maximum' is not valid: Allowable values are any non-negative integers.""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_simple_paragraphs_single_blanks",
        source_file_name=f"{source_path}good_simple_paragraphs_single_blanks.md",
    ),
    pluginRuleTest(
        "bad_simple_paragraphs_double_blanks",
        source_file_name=f"{source_path}good_simple_paragraphs_double_blanks.md",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
    ),
    pluginRuleTest(
        "good_simple_paragraphs_double_blanks",
        source_file_name=f"{source_path}good_simple_paragraphs_double_blanks.md",
        set_args=["plugins.md012.maximum=$#2"],
    ),
    pluginRuleTest(
        "good_simple_paragraphs_triple_blanks",
        source_file_name=f"{source_path}good_simple_paragraphs_triple_blanks.md",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)""",
    ),
    pluginRuleTest(
        "bad_double_blanks_at_end",
        source_file_name=f"{source_path}bad_double_blanks_at_end.md",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
    ),
    pluginRuleTest(
        "bad_multiple_blanks_in_block_quote",
        source_file_name=f"{source_path}bad_multiple_blanks_in_block_quote.md",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
    ),
    pluginRuleTest(
        "bad_multiple_blanks_in_list",
        source_file_name=f"{source_path}bad_multiple_blanks_in_list.md",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md009",
    ),
    pluginRuleTest(
        "good_multiple_blanks_in_fenced",
        source_file_name=f"{source_path}good_multiple_blanks_in_fenced.md",
        scan_expected_return_code=0,
    ),
    pluginRuleTest(
        "good_multiple_blanks_in_indented",
        source_file_name=f"{source_path}good_multiple_blanks_in_indented.md",
        scan_expected_return_code=0,
    ),
    pluginRuleTest(
        "bad_multiple_blanks_in_html",
        source_file_name=f"{source_path}bad_multiple_blanks_in_html.md",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
    ),
    pluginRuleTest(
        "good_blanks_around_single_pragma",
        source_file_contents="""Some markdown here

<!--pyml disable-num-lines 5 md013-->

My 10 lines
""",
        scan_expected_return_code=0,
    ),
    pluginRuleTest(
        "bad_blanks_double_around_single_pragma",
        source_file_contents="""Some markdown here


<!--pyml disable-num-lines 5 md013-->


My 10 lines
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)
{temp_source_path}:6:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
    ),
    pluginRuleTest(
        "bad_blanks_double_within_pragmas",
        source_file_contents="""Some markdown here

<!--pyml disable-num-lines 5 md013-->


<!--pyml disable-num-lines 5 md013-->

My 10 lines
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md012_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md007")


# Fix?


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md012_config(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(
        test, f"{source_path}good_simple_paragraphs_single_blanks.md"
    )


def test_md012_query_config():
    config_test = pluginQueryConfigTest(
        "md012",
        """
  ITEM               DESCRIPTION

  Id                 md012
  Name(s)            no-multiple-blanks
  Short Description  Multiple consecutive blank lines
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md012.md


  CONFIGURATION ITEM  TYPE     VALUE

  maximum             integer  1

""",
    )
    execute_query_configuration_test(config_test)
