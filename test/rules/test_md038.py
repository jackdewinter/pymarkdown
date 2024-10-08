"""
Module to provide tests related to the MD038 rule.
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

source_path = os.path.join("test", "resources", "rules", "md038") + os.sep

scanTests = [
    pluginRuleTest(
        "good_code_span",
        source_file_name=f"{source_path}good_code_span.md",
    ),
    pluginRuleTest(
        "bad_code_span_trailing",
        source_file_name=f"{source_path}bad_code_span_trailing.md",
        source_file_contents="""this is `bad code span ` text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:9: MD038: Spaces inside code span elements (no-space-in-code)
""",
        fix_expected_file_contents="""this is `bad code span` text
""",
    ),
    pluginRuleTest(
        "bad_code_span_leading",
        source_file_name=f"{source_path}bad_code_span_leading.md",
        source_file_contents="""this is ` bad code span` text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:9: MD038: Spaces inside code span elements (no-space-in-code)
""",
        fix_expected_file_contents="""this is `bad code span` text
""",
    ),
    pluginRuleTest(
        "good_code_span_both",
        source_file_name=f"{source_path}good_code_span_both.md",
    ),
    pluginRuleTest(
        "bad_code_span_both_extra",
        source_file_name=f"{source_path}bad_code_span_both_extra.md",
        source_file_contents="""this is `  bad code span  ` text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:9: MD038: Spaces inside code span elements (no-space-in-code)
""",
        fix_expected_file_contents="""this is ` bad code span ` text
""",
    ),
    pluginRuleTest(
        "good_code_span_embedded_leading_backtick",
        source_file_name=f"{source_path}good_code_span_embedded_leading_backtick.md",
    ),
    pluginRuleTest(
        "good_code_span_embedded_trailing_backtick",
        source_file_name=f"{source_path}good_code_span_embedded_trailing_backtick.md",
    ),
    pluginRuleTest(
        "bad_code_span_empty",
        source_file_name=f"{source_path}bad_code_span_empty.md",
        source_file_contents="""this is an almost empty ` ` codepsan

this is an only spaces `  ` codepsan
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:25: MD038: Spaces inside code span elements (no-space-in-code)
{temp_source_path}:3:24: MD038: Spaces inside code span elements (no-space-in-code)
""",
        fix_expected_file_contents="""this is an almost empty `` codepsan

this is an only spaces `` codepsan
""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md038_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md038")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md038_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


def test_md038_query_config():
    config_test = pluginQueryConfigTest(
        "md038",
        """
  ITEM               DESCRIPTION

  Id                 md038
  Name(s)            no-space-in-code
  Short Description  Spaces inside code span elements
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md038.md

""",
    )
    execute_query_configuration_test(config_test)
