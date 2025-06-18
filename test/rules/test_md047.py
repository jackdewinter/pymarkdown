"""
Module to provide tests related to the MD047 rule.
"""

import os
from test.rules.utils import (
    calculate_fix_tests,
    execute_fix_test,
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md047") + os.sep

scanTests = [
    pluginRuleTest(
        "good_end_with_blank_line",
        source_file_name=f"{source_path}end_with_blank_line.md",
    ),
    pluginRuleTest(
        "bad_end_with_no_blank_line",
        source_file_name=f"{source_path}end_with_no_blank_line.md",
        source_file_contents="""# This is a test

The line after this line should be blank.""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:41: MD047: Each file should end with a single newline character. (single-trailing-newline)
""",
        fix_expected_file_contents="""# This is a test

The line after this line should be blank.
""",
    ),
    pluginRuleTest(
        "bad_end_with_blank_line_containing_spaces",
        source_file_name=f"{source_path}end_with_no_blank_line_and_spaces.md",
        source_file_contents="""# This is a test

The line after this line is blank, but contains two spaces.
\a\a""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:2: MD047: Each file should end with a single newline character. (single-trailing-newline)
""",
        fix_expected_file_contents="""# This is a test

The line after this line is blank, but contains two spaces.
\a\a
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_end_with_no_blank_line_fix_and_debug",
        source_file_name=f"{source_path}end_with_no_blank_line.md",
        source_file_contents="""# This is a test

The line after this line should be blank.""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:41: MD047: Each file should end with a single newline character. (single-trailing-newline)
""",
        fix_expected_file_contents="""# This is a test

The line after this line should be blank.
""",
        use_fix_debug=True,
        fix_expected_output="""md009-before:# This is a test:
md010-before:# This is a test:
md047-before:# This is a test:
nl-ltw:# This is a test\\n:
md009-before::
md010-before::
md047-before::
nl-ltw:\\n:
md009-before:The line after this line should be blank.:
md010-before:The line after this line should be blank.:
md047-before:The line after this line should be blank.:
was_newline_added_at_end_of_file=False
fixed:\\n:
is_line_empty=False
was_modified=True
nl-ltw:The line after this line should be blank.:
cf-ltw:\\n:
FixLineRecord(source='completed_file', line_number=4, plugin_id='md047')
Fixed: {temp_source_path}""",
    ),
    pluginRuleTest(
        "bad_conflicting_changes_at_end_of_file",
        add_plugin_path=os.path.join(
            "test", "resources", "plugins", "bad", "bad_update_last_line.py"
        ),
        source_file_name=f"{source_path}end_with_no_blank_line_and_spaces.md",
        source_file_contents="""# This is a test

The line after this line is blank, but contains two spaces.
\a\a""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:4:2: MD047: Each file should end with a single newline character. (single-trailing-newline)",
        fix_expected_file_contents="""# This is a test

The line after this line is blank, but contains two spaces.
\a\a""".replace(
            "\a", " "
        ),
        fix_expected_return_code=1,
        fix_expected_output="",
        fix_expected_error="""BadPluginError encountered while scanning '{temp_source_path}':
Plugin id 'MDE003' had a critical failure during the 'completed_file' action.""",
    ),
    pluginRuleTest(
        "mix_md047_md010",
        source_file_contents="""item\t1""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD010: Hard tabs [Column: 5] (no-hard-tabs)
{temp_source_path}:1:6: MD047: Each file should end with a single newline character. (single-trailing-newline)
""",
        fix_expected_file_contents="""item    1
""",
    ),
    pluginRuleTest(
        "mix_md047_md019",
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


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md047_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md047")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md047_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


def test_md047_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md047",
        """
  ITEM               DESCRIPTION

  Id                 md047
  Name(s)            single-trailing-newline
  Short Description  Each file should end with a single newline character.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md047.md
""",
    )
    execute_query_configuration_test(config_test)
