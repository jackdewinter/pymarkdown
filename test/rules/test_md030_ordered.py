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


configTests = [
    pluginConfigErrorTest(
        "ol_single_type",
        use_strict_config=True,
        set_args=["plugins.md030.ol_single=not-integer"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md030.ol_single' must be of type 'int'.""",
    ),
    pluginConfigErrorTest(
        "ol_single_range",
        use_strict_config=True,
        set_args=["plugins.md030.ol_single=$#0"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md030.ol_single' is not valid: Allowable values are any integer greater than 0.""",
    ),
    pluginConfigErrorTest(
        "ol_multi_type",
        use_strict_config=True,
        set_args=["plugins.md030.ol_multi=not-integer"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md030.ol_multi' must be of type 'int'.""",
    ),
    pluginConfigErrorTest(
        "ol_multi_range",
        use_strict_config=True,
        set_args=["plugins.md030.ol_multi=$#0"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md030.ol_multi' is not valid: Allowable values are any integer greater than 0.""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_spacing_ol_single_x",
        source_file_name=f"{source_path}good_spacing_ol_single.md",
    ),
    pluginRuleTest(
        "test_md030_good_spacing_ol_single_with_config_1_2",
        source_file_name=f"{source_path}good_spacing_ol_single.md",
        use_strict_config=True,
        set_args=["plugins.md030.ol_single=$#1", "plugins.md030.ol_multi=$#2"],
    ),
    pluginRuleTest(
        "bad_spacing_ol_single_with_config_2_1",
        source_file_name=f"{source_path}good_spacing_ol_single.md",
        use_strict_config=True,
        set_args=["plugins.md030.ol_single=$#2", "plugins.md030.ol_multi=$#1"],
        source_file_contents="""1. First
1. Second
1. Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
{temp_source_path}:3:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
""",
        fix_expected_file_contents="""1.  First
1.  Second
1.  Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ol_single",
        source_file_name=f"{source_path}bad_spacing_ol_single.md",
        source_file_contents="""1.  First
1.  Second
1.  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:3:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""1. First
1. Second
1. Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ol_single_config_1_2",
        source_file_name=f"{source_path}bad_spacing_ol_single.md",
        use_strict_config=True,
        set_args=["plugins.md030.ol_single=$#1", "plugins.md030.ol_multi=$#2"],
        source_file_contents="""1.  First
1.  Second
1.  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:3:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""1. First
1. Second
1. Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ol_single_config_2_1",
        source_file_name=f"{source_path}bad_spacing_ol_single.md",
        use_strict_config=True,
        set_args=["plugins.md030.ol_single=$#2", "plugins.md030.ol_multi=$#1"],
    ),
    pluginRuleTest(
        "good_spacing_ol_double",
        source_file_name=f"{source_path}good_spacing_ol_double.md",
    ),
    pluginRuleTest(
        "bad_spacing_ol_double_config_1_2",
        source_file_name=f"{source_path}good_spacing_ol_double.md",
        use_strict_config=True,
        set_args=["plugins.md030.ol_single=$#1", "plugins.md030.ol_multi=$#2"],
        source_file_contents="""1. First
1. Second - 1

   Second - 2
1. Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
""",
        fix_expected_file_contents="""1. First
1.  Second - 1

    Second - 2
1. Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ol_double_config_2_1",
        source_file_name=f"{source_path}good_spacing_ol_double.md",
        use_strict_config=True,
        set_args=["plugins.md030.ol_single=$#2", "plugins.md030.ol_multi=$#1"],
        source_file_contents="""1. First
1. Second - 1

   Second - 2
1. Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
{temp_source_path}:5:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
""",
        fix_expected_file_contents="""1.  First
1. Second - 1

   Second - 2
1.  Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ol_double",
        source_file_name=f"{source_path}bad_spacing_ol_double.md",
        source_file_contents="""1.  First
1.  Second - 1

    Second - 2
1.  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:5:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""1. First
1. Second - 1

   Second - 2
1. Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ol_double_config_1_2",
        source_file_name=f"{source_path}bad_spacing_ol_double.md",
        use_strict_config=True,
        set_args=["plugins.md030.ol_single=$#1", "plugins.md030.ol_multi=$#2"],
        source_file_contents="""1.  First
1.  Second - 1

    Second - 2
1.  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:5:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""1. First
1.  Second - 1

    Second - 2
1. Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ol_double_config_2_1",
        source_file_name=f"{source_path}bad_spacing_ol_double.md",
        use_strict_config=True,
        set_args=["plugins.md030.ol_single=$#2", "plugins.md030.ol_multi=$#1"],
        source_file_contents="""1.  First
1.  Second - 1

    Second - 2
1.  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)\n
""",
        fix_expected_file_contents="""1.  First
1. Second - 1

   Second - 2
1.  Third
""",
    ),
    pluginRuleTest(
        "good_spacing_ol_single_nested",
        source_file_name=f"{source_path}good_spacing_ol_single_nested.md",
    ),
    pluginRuleTest(
        "bad_spacing_ol_single_nested",
        source_file_name=f"{source_path}bad_spacing_ol_single_nested.md",
        source_file_contents="""1.  First
    1.  Second
1.  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:5: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:3:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""1. First
    1. Second
1. Third
""",
    ),
    pluginRuleTest(
        "good_spacing_ol_single_nested_double",
        source_file_name=f"{source_path}good_spacing_ol_single_nested_double.md",
    ),
    pluginRuleTest(
        "good_spacing_ol_single_nested_double_2_1",
        source_file_name=f"{source_path}good_spacing_ol_single_nested_double.md",
        use_strict_config=True,
        set_args=["plugins.md030.ol_single=$#2", "plugins.md030.ol_multi=$#1"],
        source_file_contents="""1. First
   first paragraph

   1. Second

   second paragraph
1. Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
{temp_source_path}:7:1: MD030: Spaces after list markers [Expected: 2; Actual: 1] (list-marker-space)
""",
        fix_expected_file_contents="""1. First
   first paragraph

   1.  Second

   second paragraph
1.  Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ol_single_nested_double",
        source_file_name=f"{source_path}bad_spacing_ol_single_nested_double.md",
        source_file_contents="""1.  First
    1.  Second

    second paragraph
1.  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:2:5: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{temp_source_path}:5:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""1. First
    1. Second

   second paragraph
1. Third
""",
    ),
    pluginRuleTest(
        "bad_spacing_ol_single_nested_double_2_1",
        source_file_name=f"{source_path}bad_spacing_ol_single_nested_double.md",
        use_strict_config=True,
        set_args=["plugins.md030.ol_single=$#2", "plugins.md030.ol_multi=$#1"],
        source_file_contents="""1.  First
    1.  Second

    second paragraph
1.  Third
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
""",
        fix_expected_file_contents="""1. First
    1.  Second

   second paragraph
1.  Third
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
def test_md001_config(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}good_spacing_ol_single.md")
