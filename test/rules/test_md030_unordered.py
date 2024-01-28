"""
Module to provide tests related to the MD030 rule.
"""
import os
from test.rules.utils import (
    build_fix_and_clash_lists,
    execute_configuration_test,
    execute_fix_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginConfigErrorTest,
    pluginRuleTest,
)

import pytest

# pylint: disable=too-many-lines

source_path = os.path.join("test", "resources", "rules", "md030") + os.sep

__plugin_disable_md005 = "md005"
__plugin_disable_md005_md007 = "md005,md007"
__plugin_disable_md007 = "md007"
__plugin_disable_md022 = "md022"

configTests = [
    pluginConfigErrorTest(
        "ul_single_type",
        use_strict_config=True,
        set_args=["plugins.md030.ul_single=not-integer"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md030.ul_single' must be of type 'int'.""",
    ),
    pluginConfigErrorTest(
        "ul_single_range",
        use_strict_config=True,
        set_args=["plugins.md030.ul_single=$#0"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md030.ul_single' is not valid: Allowable values are any integer greater than 0.""",
    ),
    pluginConfigErrorTest(
        "ul_multi_type",
        use_strict_config=True,
        set_args=["plugins.md030.ul_multi=not-integer"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md030.ul_multi' must be of type 'int'.""",
    ),
    pluginConfigErrorTest(
        "ul_multi_range",
        use_strict_config=True,
        set_args=["plugins.md030.ul_multi=$#0"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md030.ul_multi' is not valid: Allowable values are any integer greater than 0.""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_spacing_ul_single",
        source_file_name=f"{source_path}good_spacing_ul_single.md",
    ),
    pluginRuleTest(
        "good_spacing_ul_single_with_config_1_2",
        source_file_name=f"{source_path}good_spacing_ul_single.md",
        use_strict_config=True,
        set_args=["plugins.md030.ul_single=$#1", "plugins.md030.ul_multi=$#2"],
    ),
    pluginRuleTest(
        "bad_spacing_ul_single_with_config_2_1",
        source_file_name=f"{source_path}good_spacing_ul_single.md",
        use_strict_config=True,
        set_args=["plugins.md030.ul_single=$#2", "plugins.md030.ul_multi=$#1"],
        source_file_contents="""* First
* Second
* Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
{temp_source_path}:3:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
""",
        fix_expected_file_contents="""*  First
*  Second
*  Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ul_single",
        source_file_name=f"{source_path}bad_spacing_ul_single.md",
        source_file_contents="""*  First
*  Second
*  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:3:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""* First
* Second
* Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ul_single_config_1_2",
        source_file_name=f"{source_path}bad_spacing_ul_single.md",
        use_strict_config=True,
        set_args=["plugins.md030.ul_single=$#1", "plugins.md030.ul_multi=$#2"],
        source_file_contents="""*  First
*  Second
*  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:3:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""* First
* Second
* Third
""",
    ),
    pluginRuleTest(
        "good_spacing_ul_single_config_2_1",
        source_file_name=f"{source_path}bad_spacing_ul_single.md",
        use_strict_config=True,
        set_args=["plugins.md030.ul_single=$#2", "plugins.md030.ul_multi=$#1"],
    ),
    pluginRuleTest(
        "good_spacing_ul_double",
        source_file_name=f"{source_path}good_spacing_ul_double.md",
    ),
    pluginRuleTest(
        "good_spacing_ul_double_config_1_2",
        source_file_name=f"{source_path}good_spacing_ul_double.md",
        disable_rules=__plugin_disable_md005,
        use_strict_config=True,
        set_args=["plugins.md030.ul_single=$#1", "plugins.md030.ul_multi=$#2"],
        source_file_contents="""* First
* Second - 1

  Second - 2
* Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
""",
        fix_expected_file_contents="""* First
*  Second - 1

   Second - 2
* Third
""",
    ),
    pluginRuleTest(
        "good_spacing_ul_double_config_2_1",
        disable_rules=__plugin_disable_md005,
        source_file_name=f"{source_path}good_spacing_ul_double.md",
        use_strict_config=True,
        set_args=["plugins.md030.ul_single=$#2", "plugins.md030.ul_multi=$#1"],
        source_file_contents="""* First
* Second - 1

  Second - 2
* Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
{temp_source_path}:5:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
""",
        fix_expected_file_contents="""*  First
* Second - 1

  Second - 2
*  Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ul_double",
        source_file_name=f"{source_path}bad_spacing_ul_double.md",
        source_file_contents="""*  First
*  Second - 1

   Second - 2
*  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:5:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""* First
* Second - 1

  Second - 2
* Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ul_double_config_1_2",
        source_file_name=f"{source_path}bad_spacing_ul_double.md",
        disable_rules=__plugin_disable_md005_md007,
        use_strict_config=True,
        set_args=["plugins.md030.ul_single=$#1", "plugins.md030.ul_multi=$#2"],
        source_file_contents="""*  First
*  Second - 1

   Second - 2
*  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:5:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""* First
*  Second - 1

   Second - 2
* Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ul_double_config_2_1",
        source_file_name=f"{source_path}bad_spacing_ul_double.md",
        disable_rules=__plugin_disable_md005,
        use_strict_config=True,
        set_args=["plugins.md030.ul_single=$#2", "plugins.md030.ul_multi=$#1"],
        source_file_contents="""*  First
*  Second - 1

   Second - 2
*  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""*  First
* Second - 1

  Second - 2
*  Third
""",
    ),
    pluginRuleTest(
        "good_spacing_ul_single_nested",
        source_file_name=f"{source_path}good_spacing_ul_single_nested.md",
    ),
    pluginRuleTest(
        "bad_spacing_ul_single_nested",
        source_file_name=f"{source_path}bad_spacing_ul_single_nested.md",
        disable_rules=__plugin_disable_md007,
        source_file_contents="""*  First
   *  Second
*  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:4: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:3:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""* First
   * Second
* Third
""",
    ),
    pluginRuleTest(
        "good_spacing_ul_single_nested_double",
        source_file_name=f"{source_path}good_spacing_ul_single_nested_double.md",
    ),
    pluginRuleTest(
        "good_spacing_ul_single_nested_double_2_1",
        source_file_name=f"{source_path}good_spacing_ul_single_nested_double.md",
        disable_rules=__plugin_disable_md005,
        use_strict_config=True,
        set_args=["plugins.md030.ul_single=$#2", "plugins.md030.ul_multi=$#1"],
        source_file_contents="""* First
  first paragraph

  * Second

  second paragraph
* Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
{temp_source_path}:7:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
""",
        fix_expected_file_contents="""* First
  first paragraph

  *  Second

  second paragraph
*  Third
""",
    ),
    pluginRuleTest(
        "good_spacing_ul_single_nested_double_2_1_xx",
        disable_rules=__plugin_disable_md005,
        use_strict_config=True,
        set_args=["plugins.md030.ul_single=$#2", "plugins.md030.ul_multi=$#1"],
        source_file_contents="""* First
  first paragraph

  * Second

  second paragraph
* Third

another paragraph
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
{temp_source_path}:7:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
""",
        fix_expected_file_contents="""* First
  first paragraph

  *  Second

  second paragraph
*  Third

another paragraph
""",
    ),
    pluginRuleTest(
        "bad_spacing_ul_single_nested_double",
        source_file_name=f"{source_path}bad_spacing_ul_single_nested_double.md",
        disable_rules=__plugin_disable_md007,
        source_file_contents="""*  First
   *  Second

   second paragraph
*  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:4: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:5:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""* First
   * Second

  second paragraph
* Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ul_single_nested_double_2_1",
        source_file_name=f"{source_path}bad_spacing_ul_single_nested_double.md",
        use_strict_config=True,
        set_args=["plugins.md030.ul_single=$#2", "plugins.md030.ul_multi=$#1"],
        disable_rules=__plugin_disable_md005_md007,
        source_file_contents="""*  First
   *  Second

   second paragraph
*  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""* First
   *  Second

  second paragraph
*  Third
""",
    ),
    pluginRuleTest(
        "mix_md030_md005",
        source_file_contents="""+  Heading 1
 +  Heading 2
    +  Heading 3
     +  Heading 4
""",
        disable_rules=__plugin_disable_md007,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:2: MD005: Inconsistent indentation for list items at the same level [Expected: 1; Actual: 1] (list-indent)
{temp_source_path}:2:2: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:3:5: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:4:6: MD005: Inconsistent indentation for list items at the same level [Expected: 5; Actual: 5] (list-indent)
{temp_source_path}:4:6: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""+ Heading 1
+ Heading 2
    + Heading 3
    + Heading 4
""",
    ),
    pluginRuleTest(
        "mix_md030_md007",
        source_file_contents=""" *  First
    first paragraph

    *  Second

    second paragraph
 *  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:1:2: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:4:5: MD007: Unordered list indentation [Expected: 2, Actual=4] (ul-indent)
{temp_source_path}:4:5: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:7:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:7:2: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""* First
  first paragraph

  * Second

  second paragraph
* Third
""",
    ),
    pluginRuleTest(
        "mix_md030_md010",
        source_file_contents="""*  # list item\t1
*  ## list\titem 2

   paragraph
*  ## list\titem 3
""",
        disable_rules=__plugin_disable_md022,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:1:15: MD010: Hard tabs [Column: 15] (no-hard-tabs)
{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
{temp_source_path}:5:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:5:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
""",
        fix_expected_file_contents="""* # list item  1
* ## list  item 2

  paragraph
* ## list  item 3
""",
    ),
    pluginRuleTest(
        "mix_md030_md023",
        source_file_contents=""" *  # Heading 1

    *  ## Heading 2

       *  ### Heading 3
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:1:2: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:3:5: MD007: Unordered list indentation [Expected: 2, Actual=4] (ul-indent)
{temp_source_path}:3:5: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:5:8: MD007: Unordered list indentation [Expected: 4, Actual=7] (ul-indent)
{temp_source_path}:5:8: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""* # Heading 1

  * ## Heading 2

    * ### Heading 3
""",
    ),
    pluginRuleTest(
        "mix_md030_md027",
        source_file_contents=""">  *  Heading 1
>  *  Heading 2
""",
        disable_rules=__plugin_disable_md007,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:1:4: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:2:4: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""> * Heading 1
> * Heading 2
""",
    ),
]

fixTests, _ = build_fix_and_clash_lists(scanTests)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md030_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md030")


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md030_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md030_config(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}good_spacing_ul_single.md")
