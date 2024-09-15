"""
Module to provide tests related to the MD007 rule.
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

# pylint: disable=too-many-lines

__plugin_enable_this_rule = "pml101"
__plugin_disable_this_rule = "md007"
__plugin_disable_this_rule_and_md005 = "md007,md005"
__plugin_disable_this_rule_and_md027 = "md007,md027"
__plugin_disable_this_rule_and_md027_and_md032 = "md007,md027,md032"
__plugin_disable_this_rule_and_md032 = "md007,md032"

configTests = [
    pluginConfigErrorTest(
        "invalid_indent",
        use_strict_config=True,
        set_args=["plugins.pml101.enabled=$!True", "plugins.pml101.indent=bad"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.pml101.indent' must be of type 'int'.""",
    ),
    pluginConfigErrorTest(
        "invalid_indent_range",
        use_strict_config=True,
        set_args=["plugins.pml101.enabled=$!True", "plugins.pml101.indent=$#9"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.pml101.indent' is not valid: Allowable values are between 3 and 5.""",
    ),
]


scanTests = [
    pluginRuleTest(
        "good_simple_indent_default_ul_ul_ul",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""* text
    * this is level 1
        * this is level 2
""",
    ),
    pluginRuleTest(
        "good_simple_indent_default_level_0_ul",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""* this is level 1
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_0_ul",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents=""" * this is level 1
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_level_0_ul_enhanced",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""* this is level 1
  part of level 1
* this is now level 2
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_0_ul_enhanced_0",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md005,
        source_file_contents=""" * this is level 1
  part of level 1
* this is now level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_0_ul_enhanced_1",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents=""" * this is level 1
   part of level 1
 * this is now level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)
{temp_source_path}:3:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)""",
    ),
    pluginRuleTest(
        "good_simple_indent_default_level_0_ol",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""1. this is level 1
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_0_ol",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents=""" 1. this is level 1
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_level_0_ol_enhanced",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""1. this is level 1
   part of level 1
1. this is now level 2
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_0_ol_enhanced_0",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md005,
        source_file_contents=""" 1. this is level 1
   part of level 1
1. this is now level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_0_ol_enhanced_1",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents=""" 1. this is level 1
    part of level 1
 1. this is now level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)
{temp_source_path}:3:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)
""",
    ),
    pluginRuleTest(
        "good_simple_indent_default_level_1_ul_ul",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""* this is level 1
    * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_1_ul_ul",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""* this is level 1
  * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:3: PML101: Anchored list indentation [Expected: 4, Actual=2] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_level_1_ul_ul_enhanced",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""* this is level 1
  still level 1
    * this is level 2
      still level 2
    * this is level 2a
      still level 2a
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_1_ul_ul_enhanced_0",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents=""" * this is level 1
  still level 1
    * this is level 2
      still level 2
    * this is level 2a
      still level 2a
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_1_ul_ul_enhanced_1",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md005,
        source_file_contents="""* this is level 1
  still level 1
     * this is level 2
       still level 2
    * this is level 2a
      still level 2a
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:6: PML101: Anchored list indentation [Expected: 4, Actual=5] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_1_ul_ul_enhanced_2",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md005,
        source_file_contents="""* this is level 1
  still level 1
   * this is level 2
     still level 2
    * this is level 2a
      still level 2a
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:4: PML101: Anchored list indentation [Expected: 4, Actual=3] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_level_1_ol_ul",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""1. this is level 1
    * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_1_ol_ul",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""1. this is level 1
   * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:4: PML101: Anchored list indentation [Expected: 4, Actual=3] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_level_1_ol_ul_enhanced",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""1. this is level 1
   still level 1
    * this is level 2
      still level 2
    * this is level 2a
      still level 2a
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_1_ol_ul_enhanced_0",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents=""" 1. this is level 1
   still level 1
    * this is level 2
      still level 2
    * this is level 2a
      still level 2a
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_1_ol_ul_enhanced_1",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md005,
        source_file_contents="""1. this is level 1
   still level 1
     * this is level 2
       still level 2
    * this is level 2a
      still level 2a
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:6: PML101: Anchored list indentation [Expected: 4, Actual=5] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_1_ol_ul_enhanced_2",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md005,
        source_file_contents="""1. this is level 1
  still level 1
   * this is level 2
     still level 2
    * this is level 2a
      still level 2a
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:4: PML101: Anchored list indentation [Expected: 4, Actual=3] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_level_1_ol_ol",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""1. this is level 1
    1. this is level 2
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_1_ol_ol",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""1. this is level 1
   1. this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:4: PML101: Anchored list indentation [Expected: 4, Actual=3] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_level_1_ol_ol_enhanced",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""1. this is level 1
   still level 1
    1. this is level 2
       still level 2
    1. this is level 2a
       still level 2a
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_1_ol_ol_enhanced_0",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md005,
        source_file_contents=""" 1. this is level 1
   still level 1
    1. this is level 2
       still level 2
    1. this is level 2a
       still level 2a
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_1_ol_ol_enhanced_1",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md005,
        source_file_contents="""1. this is level 1
   still level 1
     1. this is level 2
       still level 2
    1. this is level 2a
      still level 2a
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:6: PML101: Anchored list indentation [Expected: 4, Actual=5] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_1_ol_ol_enhanced_2",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md005,
        source_file_contents="""1. this is level 1
  still level 1
   1. this is level 2
     still level 2
    1. this is level 2a
      still level 2a
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:4: PML101: Anchored list indentation [Expected: 4, Actual=3] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_level_1_ul_ol",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""* this is level 1
    1. this is level 2
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_level_1_ul_ol",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""* this is level 1
  1. this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:3: PML101: Anchored list indentation [Expected: 4, Actual=2] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_bq_level_0_ul",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""> * this is level 1
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_bq_level_0_ul",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md027,
        source_file_contents=""">  * this is level 1
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:4: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_bq_level_0_ol",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""> 1. this is level 1
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_bq_level_0_ol",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md027,
        source_file_contents=""">  1. this is level 1
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:4: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_bq_level_1_ul_ul",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""> * this is level 1
>     * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_bq_level_1_ul_ul",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""> * this is level 1
>   * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:5: PML101: Anchored list indentation [Expected: 4, Actual=2] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_bq_level_1_ol_ul",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""> 1. this is level 1
>     * this is level 2
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_bq_level_1_ol_ul",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""> 1. this is level 1
>    * this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:6: PML101: Anchored list indentation [Expected: 4, Actual=3] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_bq_level_1_ol_ol",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""> 1. this is level 1
>     1. this is level 2
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_bq_level_1_ol_ol",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""> 1. this is level 1
>    1. this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:6: PML101: Anchored list indentation [Expected: 4, Actual=3] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_simple_indent_default_bq_level_1_ul_ol",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""> * this is level 1
>     1. this is level 2
""",
    ),
    pluginRuleTest(
        "bad_simple_indent_default_bq_level_1_ul_ol",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule,
        source_file_contents="""> * this is level 1
>   1. this is level 2
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:5: PML101: Anchored list indentation [Expected: 4, Actual=2] (list-anchored-indent)",
    ),
    pluginRuleTest(
        "good_complex_1",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md032,
        source_file_contents="""* > * this is level 3?
* > * level 3, new list item
""",
    ),
    pluginRuleTest(
        "good_complex_2",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md032,
        source_file_contents="""* > * > 1. this is level 5?
* > * > 1. level 5, new list item
""",
    ),
    pluginRuleTest(
        "good_complex_3",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md032,
        source_file_contents="""* > > > 1. this is level 5?
* > > > 1. level 5, new list item
""",
    ),
    pluginRuleTest(
        "bad_complex_3",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md027_and_md032,
        source_file_contents="""* > > >  1. this is level 5?
* > > >  1. level 5, new list item
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:10: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)
{temp_source_path}:2:10: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)""",
    ),
    pluginRuleTest(
        "bad_complex_4",
        enable_rules=__plugin_enable_this_rule,
        disable_rules=__plugin_disable_this_rule_and_md027_and_md032,
        source_file_contents="""* > > >
  > > >  1. this is level 5?
  > > >     level 5, same list item
  > > >  1. level 5, new list item
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:10: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)
{temp_source_path}:4:10: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)
""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_pml101_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "pml101")


# @pytest.mark.parametrize("test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn)
# def test_pml101_fix(test: pluginRuleTest) -> None:
#     """
#     Execute a parameterized fix test for plugin md001.
#     """
#     execute_fix_test(test)


source_path = os.path.join("test", "resources", "rules", "md007") + os.sep


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_pml101_config(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}good_list_indentation.md")


def test_pml101_query_config():
    config_test = pluginQueryConfigTest(
        "pml101",
        """
  ITEM               DESCRIPTION

  Id                 pml101
  Name(s)            list-anchored-indent
  Short Description  Anchored list indentation
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     pml101.md


  CONFIGURATION ITEM  TYPE     VALUE

  indent              integer  4

""",
    )
    execute_query_configuration_test(config_test)
