"""
Module to provide tests related to the MD021 rule.
"""
import os
from test.rules.utils import (
    execute_fix_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginRuleTest,
)

import pytest

# pylint: disable=too-many-lines

source_path = os.path.join("test", "resources", "rules", "md021") + os.sep

plugin_disable_md010 = "md010"
plugin_disable_md023 = "md023"

scanTests = [
    pluginRuleTest(
        "good_single_spacing",
        source_file_name=f"{source_path}single_spacing.md",
    ),
    pluginRuleTest(
        "bad_multiple_spacing_both",
        source_file_name=f"{source_path}multiple_spacing.md",
        source_file_contents="""#  Heading 1  #

##  Heading 2  ##
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)
{temp_source_path}:3:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)""",
        fix_expected_file_contents="""# Heading 1 #

## Heading 2 ##
""",
    ),
    pluginRuleTest(
        "bad_multiple_spacing_left",
        source_file_name=f"{source_path}multiple_spacing_left.md",
        source_file_contents="""#  Heading 1 #

##  Heading 2 ##
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)
{temp_source_path}:3:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)
""",
        fix_expected_file_contents="""# Heading 1 #

## Heading 2 ##
""",
    ),
    pluginRuleTest(
        "bad_multiple_spacing_right",
        source_file_name=f"{source_path}multiple_spacing_right.md",
        source_file_contents="""# Heading 1  #

## Heading 2  ##
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)
{temp_source_path}:3:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)""",
        fix_expected_file_contents="""# Heading 1 #

## Heading 2 ##
""",
    ),
    pluginRuleTest(
        "good_multiple_spacing_with_inline",
        source_file_name=f"{source_path}multiple_spacing_with_inline.md",
    ),
    pluginRuleTest(
        "bad_multiple_spacing_with_indent",
        source_file_name=f"{source_path}multiple_spacing_left.md",
        disable_rules=plugin_disable_md023,
        source_file_contents="""#  Heading 1 #

##  Heading 2 ##
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)
{temp_source_path}:3:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)
""",
        fix_expected_file_contents="""# Heading 1 #

## Heading 2 ##
""",
    ),
    pluginRuleTest(
        "bad_single_space_single_tab_before",
        source_file_name=f"{source_path}single_space_single_tab_before.md",
        disable_rules=plugin_disable_md010,
        source_file_contents="""# \tHeading 1 #

## \tHeading 2 ##
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)
{temp_source_path}:3:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)
""",
        fix_expected_file_contents="""# Heading 1 #

## Heading 2 ##
""",
    ),
    pluginRuleTest(
        "bad_single_space_single_tab_after",
        source_file_name=f"{source_path}single_space_single_tab_after.md",
        disable_rules=plugin_disable_md010,
        source_file_contents="""# Heading 1\t #

## Heading 2\t ##
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)
{temp_source_path}:3:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)
""",
        fix_expected_file_contents="""# Heading 1 #

## Heading 2 ##
""",
    ),
]

fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents:
        fixTests.append(i)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md021_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test)


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md021_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)
