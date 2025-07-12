"""
Module to provide tests related to the MD029 rule.
"""

import os
from test.rules.utils import (
    calculate_fix_tests,
    execute_configuration_test,
    execute_fix_test,
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginConfigErrorTest,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

# pylint: disable=too-many-lines

source_path = os.path.join("test", "resources", "rules", "md029") + os.sep

__plugin_disable_md007 = "md007"

configTests = [
    pluginConfigErrorTest(
        "invalid_style_type",
        use_strict_config=True,
        set_args=["plugins.md029.style=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md029.style' must be of type 'str'.""",
    ),
    pluginConfigErrorTest(
        "invalid_style",
        use_strict_config=True,
        set_args=["plugins.md029.style=not-matching"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md029.style' is not valid: Allowable values: ['one', 'ordered', 'zero', 'one_or_ordered']""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_one_list",
        source_file_name=f"{source_path}good_one_list.md",
    ),
    pluginRuleTest(
        "bad_one_one_three_list",
        source_file_name=f"{source_path}bad_one_one_three_list.md",
        source_file_contents="""1. Simple
1. One
3. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD029: Ordered list item prefix [Expected: 1; Actual: 3; Style: 1/1/1] (ol-prefix)
""",
        fix_expected_file_contents="""1. Simple
1. One
1. List
""",
    ),
    pluginRuleTest(
        "bad_one_two_one_list",
        source_file_name=f"{source_path}bad_one_two_one_list.md",
        source_file_contents="""1. Simple
2. One
1. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD029: Ordered list item prefix [Expected: 3; Actual: 1; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""1. Simple
2. One
3. List
""",
    ),
    pluginRuleTest(
        "good_one_two_three_list",
        source_file_name=f"{source_path}good_one_two_three_list.md",
    ),
    pluginRuleTest(
        "bad_two_three_four_list",
        source_file_name=f"{source_path}bad_two_three_four_list.md",
        source_file_contents="""2. Simple
3. One
4. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""1. Simple
2. One
3. List
""",
    ),
    pluginRuleTest(
        "bad_two_three_four_list_with_config",
        source_file_name=f"{source_path}bad_two_three_four_list.md",
        source_file_contents="""2. Simple
3. One
4. List
""",
        set_args=["plugins.md029.allow_extended_start_values=$!True"],
    ),
    pluginRuleTest(
        "bad_nested_lists_1_with_no_config",
        source_file_contents="""2. first
   1. first-first
   1. first-second
3. second
   1. second-first
   2. second-second
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""1. first
   1. first-first
   1. first-second
2. second
   1. second-first
   2. second-second
""",
    ),
    pluginRuleTest(
        "bad_nested_lists_1_with_config",
        source_file_contents="""2. first
   1. first-first
   1. first-second
3. second
   1. second-first
   2. second-second
""",
        set_args=["plugins.md029.allow_extended_start_values=$!True"],
    ),
    pluginRuleTest(
        "bad_nested_lists_2_with_no_config",
        source_file_contents="""0. first
   1. first-first
   31. first-second
3. second
   1. second-first
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD029: Ordered list item prefix [Expected: 2; Actual: 31; Style: 1/2/3] (ol-prefix)
{temp_source_path}:4:1: MD029: Ordered list item prefix [Expected: 1; Actual: 3; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""0. first
   1. first-first
   2. first-second
1. second
   1. second-first
""",
    ),
    pluginRuleTest(
        "good_nested_lists_3_with_no_config",
        source_file_contents="""1. First Line
1. Second Line

text to break up lists

1. First Item
2. Second Item
3. Third Item
""",
    ),
    pluginRuleTest(
        "good_zero_one_two_three_list",
        source_file_name=f"{source_path}good_zero_one_two_three_list.md",
    ),
    pluginRuleTest(
        "bad_lists_1_with_no_config",
        source_file_contents="""3. first
3. second
3. third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 3; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""1. first
2. second
3. third
""",
    ),
    pluginRuleTest(
        "bad_zero_list",
        source_file_name=f"{source_path}good_zero_list.md",
        source_file_contents="""0. Simple
0. One
0. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD029: Ordered list item prefix [Expected: 1; Actual: 0; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""0. Simple
1. One
2. List
""",
    ),
    pluginRuleTest(
        "good_one_list_with_config_one",
        source_file_name=f"{source_path}good_one_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=one"],
    ),
    pluginRuleTest(
        "bad_one_one_three_list_with_config_one",
        source_file_name=f"{source_path}bad_one_one_three_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=one"],
        source_file_contents="""1. Simple
1. One
3. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD029: Ordered list item prefix [Expected: 1; Actual: 3; Style: 1/1/1] (ol-prefix)
""",
        fix_expected_file_contents="""1. Simple
1. One
1. List
""",
    ),
    pluginRuleTest(
        "bad_one_two_one_list_with_config_one",
        source_file_name=f"{source_path}bad_one_two_one_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=one"],
        source_file_contents="""1. Simple
2. One
1. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/1/1] (ol-prefix)
""",
        fix_expected_file_contents="""1. Simple
1. One
1. List
""",
    ),
    pluginRuleTest(
        "bad_one_two_three_list_with_config_one",
        source_file_name=f"{source_path}bad_one_two_one_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=one"],
        source_file_contents="""1. Simple
2. One
1. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/1/1] (ol-prefix)
""",
        fix_expected_file_contents="""1. Simple
1. One
1. List
""",
    ),
    pluginRuleTest(
        "bad_two_three_four_list_with_config_one",
        source_file_name=f"{source_path}bad_two_three_four_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=one"],
        source_file_contents="""2. Simple
3. One
4. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/1/1] (ol-prefix)
""",
        fix_expected_file_contents="""1. Simple
1. One
1. List
""",
    ),
    pluginRuleTest(
        "bad_nested_lists_with_config_one",
        use_strict_config=True,
        set_args=["plugins.md029.style=one"],
        source_file_contents="""2. first
   1. first-first
   2. first-second
3. second
   1. second-first
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/1/1] (ol-prefix)
{temp_source_path}:3:4: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/1/1] (ol-prefix)
""",
        fix_expected_file_contents="""1. first
   1. first-first
   1. first-second
1. second
   1. second-first
""",
    ),
    pluginRuleTest(
        "bad_zero_one_two_list_with_config_one",
        source_file_name=f"{source_path}good_zero_one_two_three_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=one"],
        source_file_contents="""0. Simple
1. One
2. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 0; Style: 1/1/1] (ol-prefix)
""",
        fix_expected_file_contents="""1. Simple
1. One
1. List
""",
    ),
    pluginRuleTest(
        "bad_zero_list_with_config_one",
        source_file_name=f"{source_path}good_zero_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=one"],
        source_file_contents="""0. Simple
0. One
0. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 0; Style: 1/1/1] (ol-prefix)
""",
        fix_expected_file_contents="""1. Simple
1. One
1. List
""",
    ),
    pluginRuleTest(
        "bad_one_list_with_config_ordered",
        source_file_name=f"{source_path}good_one_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=ordered"],
        source_file_contents="""1. Simple
1. One
1. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD029: Ordered list item prefix [Expected: 2; Actual: 1; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""1. Simple
2. One
3. List
""",
    ),
    pluginRuleTest(
        "bad_one_one_three_list_with_config_ordered",
        source_file_name=f"{source_path}bad_one_one_three_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=ordered"],
        source_file_contents="""1. Simple
1. One
3. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD029: Ordered list item prefix [Expected: 2; Actual: 1; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""1. Simple
2. One
3. List
""",
    ),
    pluginRuleTest(
        "bad_one_two_one_list_with_config_ordered",
        source_file_name=f"{source_path}bad_one_two_one_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=ordered"],
        source_file_contents="""1. Simple
2. One
1. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD029: Ordered list item prefix [Expected: 3; Actual: 1; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""1. Simple
2. One
3. List
""",
    ),
    pluginRuleTest(
        "good_one_two_three_list_with_config_ordered",
        source_file_name=f"{source_path}good_one_two_three_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=ordered"],
    ),
    pluginRuleTest(
        "bad_two_three_four_list_with_config_ordered",
        source_file_name=f"{source_path}bad_two_three_four_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=ordered"],
        source_file_contents="""2. Simple
3. One
4. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""1. Simple
2. One
3. List
""",
    ),
    pluginRuleTest(
        "bad_nested_lists_with_config_ordered",
        use_strict_config=True,
        set_args=["plugins.md029.style=ordered"],
        source_file_contents="""2. first
   1. first-first
   1. first-second
3. second
   1. second-first
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 2; Style: 1/2/3] (ol-prefix)
{temp_source_path}:3:4: MD029: Ordered list item prefix [Expected: 2; Actual: 1; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""1. first
   1. first-first
   2. first-second
2. second
   1. second-first
""",
    ),
    pluginRuleTest(
        "bad_nested_lists_with_config_ordered_extended",
        use_strict_config=True,
        set_args=[
            "plugins.md029.style=ordered",
            "plugins.md029.allow_extended_start_values=$!True",
        ],
        source_file_contents="""2. first
   1. first-first
   1. first-second
3. second
   1. second-first
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD029: Ordered list item prefix [Expected: 2; Actual: 1; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""2. first
   1. first-first
   2. first-second
3. second
   1. second-first
""",
    ),
    pluginRuleTest(
        "good_zero_one_two_list_with_config_ordered",
        source_file_name=f"{source_path}good_zero_one_two_three_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=ordered"],
        source_file_contents="""0. Simple
1. One
2. List
""",
    ),
    pluginRuleTest(
        "bad_zero_list_with_config_ordered",
        source_file_name=f"{source_path}good_zero_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=ordered"],
        source_file_contents="""0. Simple
0. One
0. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD029: Ordered list item prefix [Expected: 1; Actual: 0; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""0. Simple
1. One
2. List
""",
    ),
    pluginRuleTest(
        "bad_one_list_with_config_zero",
        source_file_name=f"{source_path}good_one_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=zero"],
        source_file_contents="""1. Simple
1. One
1. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)
""",
        fix_expected_file_contents="""0. Simple
0. One
0. List
""",
    ),
    pluginRuleTest(
        "bad_one_one_three_list_with_config_zero",
        source_file_name=f"{source_path}bad_one_one_three_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=zero"],
        source_file_contents="""1. Simple
1. One
3. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)
""",
        fix_expected_file_contents="""0. Simple
0. One
0. List
""",
    ),
    pluginRuleTest(
        "bad_one_two_one_list_with_config_zero",
        source_file_name=f"{source_path}bad_one_two_one_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=zero"],
        source_file_contents="""1. Simple
2. One
1. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)
""",
        fix_expected_file_contents="""0. Simple
0. One
0. List
""",
    ),
    pluginRuleTest(
        "bad_one_two_three_list_with_config_zero",
        source_file_name=f"{source_path}good_one_two_three_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=zero"],
        source_file_contents="""1. Simple
2. One
3. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)
""",
        fix_expected_file_contents="""0. Simple
0. One
0. List
""",
    ),
    pluginRuleTest(
        "bad_two_three_four_list_with_config_zero",
        source_file_name=f"{source_path}bad_two_three_four_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=zero"],
        source_file_contents="""2. Simple
3. One
4. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 0; Actual: 2; Style: 0/0/0] (ol-prefix)
""",
        fix_expected_file_contents="""0. Simple
0. One
0. List
""",
    ),
    pluginRuleTest(
        "bad_nested_lists_with_config_zero",
        use_strict_config=True,
        set_args=["plugins.md029.style=zero"],
        source_file_contents="""2. first
   1. first-first
   2. first-second
3. second
   1. second-first
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD029: Ordered list item prefix [Expected: 0; Actual: 2; Style: 0/0/0] (ol-prefix)
{temp_source_path}:2:4: MD029: Ordered list item prefix [Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)
{temp_source_path}:5:4: MD029: Ordered list item prefix [Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)
""",
        fix_expected_file_contents="""0. first
   0. first-first
   0. first-second
0. second
   0. second-first
""",
    ),
    pluginRuleTest(
        "bad_zero_one_two_list_with_config_zero",
        source_file_name=f"{source_path}good_zero_one_two_three_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=zero"],
        source_file_contents="""0. Simple
1. One
2. List
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD029: Ordered list item prefix [Expected: 0; Actual: 1; Style: 0/0/0] (ol-prefix)
""",
        fix_expected_file_contents="""0. Simple
0. One
0. List
""",
    ),
    pluginRuleTest(
        "good_zero_list_with_config_zero",
        source_file_name=f"{source_path}good_zero_list.md",
        use_strict_config=True,
        set_args=["plugins.md029.style=zero"],
    ),
    pluginRuleTest(
        "mix_md005_md029",
        source_file_contents="""1. Heading 1
 9. Heading 2
    1. Heading 2
     9. Heading 2
""",
        disable_rules=__plugin_disable_md007,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:2: MD005: Inconsistent indentation for list items at the same level [Expected: 0; Actual: 1] (list-indent)
{temp_source_path}:2:2: MD029: Ordered list item prefix [Expected: 2; Actual: 9; Style: 1/2/3] (ol-prefix)
{temp_source_path}:4:6: MD005: Inconsistent indentation for list items at the same level [Expected: 4; Actual: 5] (list-indent)
{temp_source_path}:4:6: MD029: Ordered list item prefix [Expected: 2; Actual: 9; Style: 1/2/3] (ol-prefix)
""",
        fix_expected_file_contents="""1. Heading 1
2. Heading 2
    1. Heading 2
    2. Heading 2
""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md029_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md029")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md029_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md029_config(test: pluginConfigErrorTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}good_one_list.md")


def test_md029_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md029",
        """
  ITEM               DESCRIPTION

  Id                 md029
  Name(s)            ol-prefix
  Short Description  Ordered list item prefix
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md029.md


  CONFIGURATION ITEM           TYPE     VALUE

  style                        string   "one_or_ordered"
  allow_extended_start_values  boolean  False

""",
    )
    execute_query_configuration_test(config_test)
