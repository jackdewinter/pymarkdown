"""
Module to provide tests related to the MD019 rule.
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

source_path = os.path.join("test", "resources", "rules", "md019") + os.sep

__plugin_disable_md010 = "md010"
__plugin_disable_md023 = "md023"

scanTests = [
    pluginRuleTest(
        "good_single_spacing",
        source_file_name=f"{source_path}single_spacing.md",
    ),
    pluginRuleTest(
        "bad_multiple_spacing",
        source_file_name=f"{source_path}multiple_spacing.md",
        source_file_contents="""#  Heading 1

##  Heading 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:3:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)""",
        fix_expected_file_contents="""# Heading 1

## Heading 2
""",
    ),
    pluginRuleTest(
        "bad_multiple_spacing_with_inline",
        source_file_name=f"{source_path}multiple_spacing_with_inline.md",
        source_file_contents="""#  Heading *number* 1

##  Heading *number* 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:3:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)""",
        fix_expected_file_contents="""# Heading *number* 1

## Heading *number* 2
""",
    ),
    pluginRuleTest(
        "bad_multiple_spacing_with_indent",
        source_file_name=f"{source_path}multiple_spacing_with_indent.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents=""" #  Heading 1

  ##  Heading 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:3:3: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)""",
        fix_expected_file_contents=""" # Heading 1

  ## Heading 2
""",
    ),
    pluginRuleTest(
        "bad_single_space_single_tab",
        source_file_name=f"{source_path}single_space_single_tab.md",
        disable_rules=__plugin_disable_md010,
        source_file_contents="""# \tHeading 1

## \tHeading 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:3:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)""",
        fix_expected_file_contents="""# Heading 1

## Heading 2
""",
    ),
    pluginRuleTest(
        "xxx",
        source_file_contents="""#  Heading 1

a line of text""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:3:14: MD047: Each file should end with a single newline character. (single-trailing-newline)""",
        fix_expected_file_contents="""# Heading 1

a line of text
""",
    ),
]

fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents:
        fixTests.append(i)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md019_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md019")


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md019_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)
