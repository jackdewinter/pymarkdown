"""
Module to provide tests related to the MD037 rule.
"""

import os
from test.rules.utils import (
    execute_fix_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md037") + os.sep

scanTests = [
    pluginRuleTest(
        "good_valid_emphasis",
        source_file_name=f"{source_path}good_valid_emphasis.md",
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
        scan_expected_output="""{temp_source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""this text *is* in italics

this text _is_ in italics

this text **is** in bold

this text __is__ in bold
""",
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
        scan_expected_output="""{temp_source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
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
        scan_expected_output="""{temp_source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
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
        scan_expected_output="""{temp_source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:4:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:10:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
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
        scan_expected_output="""{temp_source_path}:1:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:4:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:10:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
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
        scan_expected_output="""{temp_source_path}:1:13: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:14: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:14: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:7:14: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
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
        scan_expected_output="""{temp_source_path}:1:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:3:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:5:11: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
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
        scan_expected_output="""{temp_source_path}:1:5: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *[link](/url)* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_link_before_fix",
        source_file_contents="""abc * [link](/url)* ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *[link](/url)* ghi
""",
    ),
    pluginRuleTest(
        "bad_surrounding_emphasis_link_after_fix",
        source_file_contents="""abc *[link](/url) * ghi
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""abc *[link](/url)* ghi
""",
    ),
]
fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents:
        fixTests.append(i)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md037_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md037")


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md037_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)
