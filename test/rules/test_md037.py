"""
Module to provide tests related to the MD037 rule.
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

source_path = os.path.join("test", "resources", "rules", "md037") + os.sep

scanTests = [
    pluginRuleTest(
        "good_valid_emphasis",
        source_file_name=f"{source_path}good_valid_emphasis.md",
        use_debug=True,
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis",
        source_file_name=f"{source_path}bad_surrounding_emphasis.md",
        source_file_contents="""this text * is * in italics

this text _ is _ in italics

this text ** is ** in bold

this text __ is __ in bold
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:1:15: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:15: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:16: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:16: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""this text *is* in italics

this text _is_ in italics

this text **is** in bold

this text __is__ in bold
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_extra",
        source_file_contents="""this text *  is  * in italics

this text _  is  _ in italics

this text **  is  ** in bold

this text __  is  __ in bold
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:1:17: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:17: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:18: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:18: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""this text *is* in italics

this text _is_ in italics

this text **is** in bold

this text __is__ in bold
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_short_non_first",
        source_file_contents="""this is the first line
this text * is * in italics
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:2:15: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""this is the first line
this text *is* in italics
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_short_with_backslash_before",
        source_file_contents="""this \\* text * is * in italics
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:15: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:1:18: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""this \\* text *is* in italics
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_short_with_reference_before",
        source_file_contents="""this &#x2a; text * is * in italics
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:19: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:1:22: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""this &#x2a; text *is* in italics
""",
    ),
    pluginRuleTest(
        "good_surrounding_emphasis_short_with_mixed",
        source_file_contents="""this * text _ is * in _ italics
""",
        scan_expected_return_code=0,
        scan_expected_output="",
    ),
    pluginRuleTest(
        "good_surrounding_emphasis_short_with_other_mixed",
        source_file_contents="""this _ text * is _ in * italics
""",
        scan_expected_return_code=0,
        scan_expected_output="",
    ),
    pluginRuleTest(
        "bad_leading_emphasis",
        source_file_name=f"{source_path}bad_leading_emphasis.md",
        source_file_contents="""this text * is* in italics

this text _ is_ in italics

this text ** is** in bold

this text __ is__ in bold
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""this text *is* in italics

this text _is_ in italics

this text **is** in bold

this text __is__ in bold
""",
    ),
    pluginRuleTest(
        "bad_trailing_emphasis",
        source_file_name=f"{source_path}bad_trailing_emphasis.md",
        source_file_contents="""this text *is * in italics

this text _is _ in italics

this text **is ** in bold

this text __is __ in bold
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:14: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:14: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:15: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:15: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""this text *is* in italics

this text _is_ in italics

this text **is** in bold

this text __is__ in bold
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_multiline",
        source_file_name=f"{source_path}bad_surrounding_emphasis_multiline.md",
        source_file_contents="""this text * is
not * in italics

this text _ is
not _ in italics

this text ** is
not ** in bold

this text __ is
not __ in bold
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:2:4: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:4:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:4: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:8:4: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:10:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:11:4: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""this text *is
not* in italics

this text _is
not_ in italics

this text **is
not** in bold

this text __is
not__ in bold
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_multiline_extra",
        source_file_contents="""this text *  is
not  * in italics

this text _  is
not  _ in italics

this text **  is
not  ** in bold

this text __  is
not  __ in bold
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:2:5: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:4:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:5: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:8:5: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:10:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:11:5: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""this text *is
not* in italics

this text _is
not_ in italics

this text **is
not** in bold

this text __is
not__ in bold
""",
    ),
    pluginRuleTest(
        "bad_surrounding_empahsis_setext",
        source_file_name=f"{source_path}bad_surrounding_empahsis_setext.md",
        source_file_contents="""this text * is * in italics
===

this text _ is _ in italics
---

this text ** is ** in bold
---

this text __ is __ in bold
---
""",
        scan_expected_return_code=1,
        use_debug=True,
        scan_expected_output="""{temp_source_path}:1:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:1:15: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:4:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:4:15: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:16: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:10:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:10:16: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""this text *is* in italics
===

this text _is_ in italics
---

this text **is** in bold
---

this text __is__ in bold
---
""",
    ),
    pluginRuleTest(
        "bad_surrounding_empahsis_atx",
        source_file_name=f"{source_path}bad_surrounding_empahsis_atx.md",
        source_file_contents="""# this text * is * in italics

## this text _ is _ in italics

## this text ** is ** in bold

## this text __ is __ in bold
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:14: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:1:17: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:15: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:18: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:16: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:19: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:16: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:19: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""# this text *is* in italics

## this text _is_ in italics

## this text **is** in bold

## this text __is__ in bold
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_containers",
        source_file_name=f"{source_path}bad_surrounding_emphasis_containers.md",
        source_file_contents="""1. this is * not in * italics

+ this is * not in * italics

> this is * not in * italics
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:1:20: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:19: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:19: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""1. this is *not in* italics

+ this is *not in* italics

> this is *not in* italics
""",
    ),
    pluginRuleTest(
        "good_emphasis_with_code_span",
        source_file_name=f"{source_path}good_emphasis_with_code_span.md",
    ),
    pluginRuleTest(
        "good_no_emphasis_but_stars",
        source_file_name=f"{source_path}good_no_emphasis_but_stars.md",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_link_surround",
        source_file_contents="""abc * [link](/url) * ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:6: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:1:19: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *[link](/url)* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_link_surround_extra",
        source_file_contents="""abc *  [link](/url)  * ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:6: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:1:21: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *[link](/url)* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_link_before_fix",
        source_file_contents="""abc * [link](/url)* ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:6: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *[link](/url)* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_link_after_fix",
        source_file_contents="""abc *[link](/url) * ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:18: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *[link](/url)* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_backslash_surround",
        source_file_contents="""abc * \\! * ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:6: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:1:9: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *\\!* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_backslash_before_fix",
        source_file_contents="""abc * \\!* ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:6: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *\\!* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_backslash_after_fix",
        source_file_contents="""abc *\\! * ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:8: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *\\!* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_reference_surround",
        source_file_contents="""abc * &amp; * ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:6: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:1:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *&amp;* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_reference_before_fix",
        source_file_contents="""abc * &amp;* ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:6: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *&amp;* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_reference_after_fix",
        source_file_contents="""abc *&amp; * ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *&amp;* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_autolink_surround",
        source_file_contents="""abc * <http://google.com> * ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:6: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:1:26: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *<http://google.com>* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_autolink_before_fix",
        source_file_contents="""abc * <http://google.com>* ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:6: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *<http://google.com>* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_autolink_after_fix",
        source_file_contents="""abc *<http://google.com> * ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:25: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *<http://google.com>* ghi
""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md037_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md037")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md037_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


def test_md037_query_config():
    config_test = pluginQueryConfigTest(
        "md037",
        """
  ITEM               DESCRIPTION

  Id                 md037
  Name(s)            no-space-in-emphasis
  Short Description  Spaces inside emphasis markers
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md037.md

""",
    )
    execute_query_configuration_test(config_test)
