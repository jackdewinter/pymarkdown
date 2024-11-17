"""
Module to provide tests related to the MD004 rule.
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

source_path = os.path.join("test", "resources", "rules", "md004") + os.sep

set_style_asterisk = "plugins.md004.style=asterisk"
set_style_dash = "plugins.md004.style=dash"
set_style_plus = "plugins.md004.style=plus"
set_style_sublist = "plugins.md004.style=sublist"

__plugin_enable_md006 = "MD006"

__plugin_disable_md007 = "MD007"
__plugin_disable_md032 = "md032"

configTests = [
    pluginConfigErrorTest(
        "invalid_style",
        use_strict_config=True,
        set_args=["plugins.md004.style=bad"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md004.style' is not valid: Allowable values: ['consistent', 'asterisk', 'plus', 'dash', 'sublist']""",
    ),
]


scanTests = [
    pluginRuleTest(
        "good_asterisk_single_level",
        source_file_name=f"{source_path}good_list_asterisk_single_level.md",
        set_args=[set_style_asterisk],
    ),
    pluginRuleTest(
        "good_asterisk_single_level_consistent",
        source_file_name=f"{source_path}good_list_asterisk_single_level.md",
        set_args=[],
    ),
    pluginRuleTest(
        "bad_asterisk_dash_single_level",
        source_file_name=f"{source_path}good_list_dash_single_level.md",
        set_args=[set_style_asterisk],
        source_file_contents="""- first
- second
- third
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:1: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: dash] (ul-style)",
        fix_expected_file_contents="""* first
* second
* third
""",
    ),
    pluginRuleTest(
        "bad_asterisk_plus_single_level",
        source_file_name=f"{source_path}good_list_plus_single_level.md",
        set_args=[set_style_asterisk],
        source_file_contents="""+ first
+ second
+ third
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:1: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: plus] (ul-style)",
        fix_expected_file_contents="""* first
* second
* third
""",
    ),
    pluginRuleTest(
        "good_dash_single_level",
        source_file_name=f"{source_path}good_list_dash_single_level.md",
        set_args=[set_style_dash],
    ),
    pluginRuleTest(
        "good_dash_single_level_consistent",
        source_file_name=f"{source_path}good_list_dash_single_level.md",
        set_args=[],
    ),
    pluginRuleTest(
        "bad_dash_asterisk_single_level",
        source_file_name=f"{source_path}good_list_asterisk_single_level.md",
        set_args=[set_style_dash],
        source_file_contents="""* first
* second
* third
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:1: MD004: Inconsistent Unordered List Start style [Expected: dash; Actual: asterisk] (ul-style)",
        fix_expected_file_contents="""- first
- second
- third
""",
    ),
    pluginRuleTest(
        "bad_dash_plus_single_level",
        source_file_name=f"{source_path}good_list_plus_single_level.md",
        set_args=[set_style_dash],
        source_file_contents="""+ first
+ second
+ third
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:1: MD004: Inconsistent Unordered List Start style [Expected: dash; Actual: plus] (ul-style)",
        fix_expected_file_contents="""- first
- second
- third
""",
    ),
    pluginRuleTest(
        "good_plus_single_level",
        source_file_name=f"{source_path}good_list_plus_single_level.md",
        set_args=[set_style_plus],
    ),
    pluginRuleTest(
        "good_plus_single_level_consistent",
        source_file_name=f"{source_path}good_list_plus_single_level.md",
        set_args=[],
    ),
    pluginRuleTest(
        "bad_plus_asterisk_single_level",
        source_file_name=f"{source_path}good_list_asterisk_single_level.md",
        set_args=[set_style_plus],
        source_file_contents="""* first
* second
* third
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:1: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: asterisk] (ul-style)",
        fix_expected_file_contents="""+ first
+ second
+ third
""",
    ),
    pluginRuleTest(
        "bad_plus_dash_single_level",
        source_file_name=f"{source_path}good_list_dash_single_level.md",
        set_args=[set_style_plus],
        source_file_contents="""- first
- second
- third
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:1: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: dash] (ul-style)",
        fix_expected_file_contents="""+ first
+ second
+ third
""",
    ),
    pluginRuleTest(
        "bad_single_level_consistent",
        source_file_name=f"{source_path}bad_list_different_single_level.md",
        set_args=[],
        disable_rules=__plugin_disable_md032,
        source_file_contents="""* first
+ second
- third
""",
        scan_expected_return_code=1,
        scan_expected_output=(
            "{temp_source_path}:2:1: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: plus] (ul-style)\n"
            + "{temp_source_path}:3:1: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: dash] (ul-style)"
        ),
        fix_expected_file_contents="""* first
* second
* third
""",
    ),
    pluginRuleTest(
        "good_multi_level_sublevel",
        source_file_name=f"{source_path}good_multi_level_sublevel.md",
        set_args=[set_style_sublist],
    ),
    pluginRuleTest(
        "good_multi_level_sublevel_complex",
        source_file_name=f"{source_path}good_multi_level_complex.md",
        set_args=[set_style_sublist],
    ),
    pluginRuleTest(
        "bad_multi_level_sublevel_complex",
        source_file_name=f"{source_path}bad_multi_level_complex.md",
        set_args=[set_style_sublist],
        source_file_contents="""+ first
  1. second
     - third
+ first
  1. second
     + third
       1. fourth
          * fifth
     + third
       1. fourth
          * fifth
     + third
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:6:6: MD004: Inconsistent Unordered List Start style [Expected: dash; Actual: plus] (ul-style)",
        fix_expected_file_contents="""+ first
  1. second
     - third
+ first
  1. second
     - third
       1. fourth
          * fifth
     - third
       1. fourth
          * fifth
     - third
""",
    ),
    pluginRuleTest(
        "bad_multi_level_sublevel_complex_asterisk",
        source_file_name=f"{source_path}bad_multi_level_complex.md",
        set_args=[set_style_asterisk],
        source_file_contents="""+ first
  1. second
     - third
+ first
  1. second
     + third
       1. fourth
          * fifth
     + third
       1. fourth
          * fifth
     + third
""",
        scan_expected_return_code=1,
        scan_expected_output=(
            "{temp_source_path}:1:1: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: plus] (ul-style)\n"
            + "{temp_source_path}:3:6: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: dash] (ul-style)\n"
            + "{temp_source_path}:6:6: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: plus] (ul-style)"
        ),
        fix_expected_file_contents="""* first
  1. second
     * third
* first
  1. second
     * third
       1. fourth
          * fifth
     * third
       1. fourth
          * fifth
     * third
""",
    ),
    pluginRuleTest(
        "bad_dual_lists_with_separator",
        source_file_name=f"{source_path}bad_dual_lists_with_separator.md",
        set_args=[set_style_sublist],
        source_file_contents="""+ item 1
  - item 1a

this is a separator

* item 2
  - item 2a
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:6:1: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: asterisk] (ul-style)",
        fix_expected_file_contents="""+ item 1
  - item 1a

this is a separator

+ item 2
  - item 2a
""",
    ),
    pluginRuleTest(
        "mix_md004_md006",
        is_mix_test=True,
        enable_rules=__plugin_enable_md006,
        disable_rules=__plugin_disable_md007,
        source_file_contents=""" + first
   * second
     - third
 * first
   - second
     + third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)
{temp_source_path}:2:4: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: asterisk] (ul-style)
{temp_source_path}:3:6: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: dash] (ul-style)
{temp_source_path}:4:2: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)
{temp_source_path}:5:4: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: dash] (ul-style)
""",
        fix_expected_file_contents="""+ first
   + second
     + third
+ first
   + second
     + third
""",
    ),
    pluginRuleTest(
        "mix_md004_md007",
        source_file_contents=""" + first
   * second
     - third
 * first
   - second
     + third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:2:4: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: asterisk] (ul-style)
{temp_source_path}:2:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:3:6: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: dash] (ul-style)
{temp_source_path}:3:6: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)
{temp_source_path}:4:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{temp_source_path}:5:4: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: dash] (ul-style)
{temp_source_path}:5:4: MD007: Unordered list indentation [Expected: 2, Actual=3] (ul-indent)
{temp_source_path}:6:6: MD007: Unordered list indentation [Expected: 4, Actual=5] (ul-indent)
""",
        fix_expected_file_contents="""+ first
  + second
    + third
+ first
  + second
    + third
""",
    ),
    pluginRuleTest(
        "mix_md004_md032",
        source_file_contents="""+ first
  * second
    - third
* first
  - second
    + third
-----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: asterisk] (ul-style)
{temp_source_path}:3:5: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: dash] (ul-style)
{temp_source_path}:5:3: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: dash] (ul-style)
{temp_source_path}:6:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
""",
        fix_expected_file_contents="""+ first
  + second
    + third
+ first
  + second
    + third
-----
""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md004_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md004")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md004_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md004_config(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}good_list_asterisk_single_level.md")


def test_md004_query_config():
    config_test = pluginQueryConfigTest(
        "md004",
        """
  ITEM               DESCRIPTION

  Id                 md004
  Name(s)            ul-style
  Short Description  Inconsistent Unordered List Start style
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md004.md


  CONFIGURATION ITEM  TYPE    VALUE

  style               string  "consistent"

""",
    )
    execute_query_configuration_test(config_test)
