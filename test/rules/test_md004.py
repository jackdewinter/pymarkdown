"""
Module to provide tests related to the MD004 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_fix_test, execute_scan_test, id_test_plug_rule_fn, pluginRuleTest
from test.utils import assert_file_is_as_expected, copy_to_temp_file

import pytest

source_path = os.path.join("test", "resources", "rules", "md004") + os.sep


@pytest.mark.rules
def test_md004_bad_configuration_style():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with a string that is not in the list of acceptable values.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_asterisk_single_level.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md004.style=bad",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md004.style' is not valid: Allowable values: ['consistent', 'asterisk', 'plus', 'dash', 'sublist']"
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )

scanTests = [
    pluginRuleTest(
        "good_asterisk_single_level",
        source_file_name=f"{source_path}good_list_asterisk_single_level.md",
        set_args=["plugins.md004.style=asterisk"],
    ),
    pluginRuleTest(
        "good_asterisk_single_level_consistent",
        source_file_name=f"{source_path}good_list_asterisk_single_level.md",
        set_args=[],
    ),
    pluginRuleTest(
        "bad_asterisk_dash_single_level",
        source_file_name=f"{source_path}good_list_dash_single_level.md",
        set_args=["plugins.md004.style=asterisk"],
        source_file_contents="""- first
- second
- third
""",
        scan_expected_return_code=1,
        scan_expected_output=f"{source_path}good_list_dash_single_level.md:1:1: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: dash] (ul-style)",
        fix_expected_return_code=1,
        fix_expected_file_contents="""* first
* second
* third
""",
    ),
    pluginRuleTest(
        "bad_asterisk_plus_single_level",
        source_file_name=f"{source_path}good_list_plus_single_level.md",
        set_args=["plugins.md004.style=asterisk"],
        source_file_contents="""+ first
+ second
+ third
""",
        scan_expected_return_code=1,
        scan_expected_output=f"{source_path}good_list_plus_single_level.md:1:1: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: plus] (ul-style)",
        fix_expected_return_code=1,
        fix_expected_file_contents="""* first
* second
* third
""",
    ),
    pluginRuleTest(
        "good_dash_single_level",
        source_file_name=f"{source_path}good_list_dash_single_level.md",
        set_args=["plugins.md004.style=dash"],
    ),
    pluginRuleTest(
        "good_dash_single_level_consistent",
        source_file_name=f"{source_path}good_list_dash_single_level.md",
        set_args=[],
    ),
    pluginRuleTest(
        "bad_dash_asterisk_single_level",
        source_file_name=f"{source_path}good_list_asterisk_single_level.md",
        set_args=["plugins.md004.style=dash"],
        source_file_contents="""* first
* second
* third
""",
        scan_expected_return_code=1,
        scan_expected_output=f"{source_path}good_list_asterisk_single_level.md:1:1: MD004: Inconsistent Unordered List Start style [Expected: dash; Actual: asterisk] (ul-style)",
        fix_expected_return_code=1,
        fix_expected_file_contents="""- first
- second
- third
""",
    ),
    pluginRuleTest(
        "bad_dash_plus_single_level",
        source_file_name=f"{source_path}good_list_plus_single_level.md",
        set_args=["plugins.md004.style=dash"],
        source_file_contents="""+ first
+ second
+ third
""",
        scan_expected_return_code=1,
        scan_expected_output=f"{source_path}good_list_plus_single_level.md:1:1: MD004: Inconsistent Unordered List Start style [Expected: dash; Actual: plus] (ul-style)",
        fix_expected_return_code=1,
        fix_expected_file_contents="""- first
- second
- third
""",
    ),
    pluginRuleTest(
        "good_plus_single_level",
        source_file_name=f"{source_path}good_list_plus_single_level.md",
        set_args=["plugins.md004.style=plus"],
    ),
    pluginRuleTest(
        "good_plus_single_level_consistent",
        source_file_name=f"{source_path}good_list_plus_single_level.md",
        set_args=[],
    ),
    pluginRuleTest(
        "bad_plus_asterisk_single_level",
        source_file_name=f"{source_path}good_list_asterisk_single_level.md",
        set_args=["plugins.md004.style=plus"],
        source_file_contents="""* first
* second
* third
""",
        scan_expected_return_code=1,
        scan_expected_output=f"{source_path}good_list_asterisk_single_level.md:1:1: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: asterisk] (ul-style)",
        fix_expected_return_code=1,
        fix_expected_file_contents="""+ first
+ second
+ third
""",
    ),
    pluginRuleTest(
        "bad_plus_dash_single_level",
        source_file_name=f"{source_path}good_list_dash_single_level.md",
        set_args=["plugins.md004.style=plus"],
        source_file_contents="""- first
- second
- third
""",
        scan_expected_return_code=1,
        scan_expected_output=f"{source_path}good_list_dash_single_level.md:1:1: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: dash] (ul-style)",
        fix_expected_return_code=1,
        fix_expected_file_contents="""+ first
+ second
+ third
""",
    ),
    pluginRuleTest(
        "bad_single_level_consistent",
        source_file_name=f"{source_path}bad_list_different_single_level.md",
        set_args=[],
        disable_rules="md032",
        source_file_contents="""* first
+ second
- third
""",
        scan_expected_return_code=1,
        scan_expected_output=(
        f"{source_path}bad_list_different_single_level.md:2:1: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: plus] (ul-style)\n"
        + f"{source_path}bad_list_different_single_level.md:3:1: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: dash] (ul-style)"
    ),
        fix_expected_return_code=1,
        fix_expected_file_contents="""* first
* second
* third
""",
    ),
    pluginRuleTest(
        "good_multi_level_sublevel",
        source_file_name=f"{source_path}good_multi_level_sublevel.md",
        set_args=["plugins.md004.style=sublist"],
    ),
    pluginRuleTest(
        "good_multi_level_sublevel_complex",
        source_file_name=f"{source_path}good_multi_level_complex.md",
        set_args=["plugins.md004.style=sublist"],
    ),
    pluginRuleTest(
        "bad_multi_level_sublevel_complex",
        source_file_name=f"{source_path}bad_multi_level_complex.md",
        set_args=["plugins.md004.style=sublist"],
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
        scan_expected_output=f"{source_path}bad_multi_level_complex.md:6:6: MD004: Inconsistent Unordered List Start style [Expected: dash; Actual: plus] (ul-style)",
        fix_expected_return_code=1,
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
        set_args=["plugins.md004.style=asterisk"],
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
            f"{source_path}bad_multi_level_complex.md:1:1: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: plus] (ul-style)\n"
            + f"{source_path}bad_multi_level_complex.md:3:6: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: dash] (ul-style)\n"
            + f"{source_path}bad_multi_level_complex.md:6:6: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: plus] (ul-style)"
        ),
        fix_expected_return_code=1,
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
        set_args=["plugins.md004.style=sublist"],
        source_file_contents="""+ item 1
  - item 1a

this is a separator

* item 2
  - item 2a
""",
        scan_expected_return_code=1,
        scan_expected_output=f"{source_path}bad_dual_lists_with_separator.md:6:1: MD004: Inconsistent Unordered List Start style [Expected: plus; Actual: asterisk] (ul-style)",
        fix_expected_return_code=1,
        fix_expected_file_contents="""+ item 1
  - item 1a

this is a separator

+ item 2
  - item 2a
""",
    ),
]
fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents:
        fixTests.append(i)

@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md004_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test)


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md004_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)
