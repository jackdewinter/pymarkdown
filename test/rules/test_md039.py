"""
Module to provide tests related to the MD039 rule.
"""
import os
from test.rules.utils import (
    execute_fix_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md039") + os.sep


scanTests = [
    pluginRuleTest(
        "good_inline_link",
        source_file_name=f"{source_path}good_inline_link.md",
    ),
    pluginRuleTest(
        "bad_inline_link_trailing_space",
        source_file_name=f"{source_path}bad_inline_link_trailing_space.md",
        source_file_contents="""this is not
[a proper ](https://www.example.com)
link
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)
""",
        fix_expected_file_contents="""this is not
[a proper](https://www.example.com)
link
""",
    ),
    pluginRuleTest(
        "bad_inline_link_leading_space",
        source_file_name=f"{source_path}bad_inline_link_leading_space.md",
        source_file_contents="""this is not
[ a proper](https://www.example.com)
link
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)
""",
        fix_expected_file_contents="""this is not
[a proper](https://www.example.com)
link
""",
    ),
    pluginRuleTest(
        "bad_inline_link_both_space",
        source_file_name=f"{source_path}bad_inline_link_both_space.md",
        source_file_contents="""this is not
[ a proper ](https://www.example.com)
link
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)
""",
        fix_expected_file_contents="""this is not
[a proper](https://www.example.com)
link
""",
    ),
    pluginRuleTest(
        "good_full_link",
        source_file_name=f"{source_path}good_full_link.md",
    ),
    pluginRuleTest(
        "bad_full_link_both_space",
        source_file_name=f"{source_path}bad_full_link_both_space.md",
        source_file_contents="""this is
[ a proper ][bar]
link

[bar]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)
""",
        fix_expected_file_contents="""this is
[a proper][bar]
link

[bar]: /url
""",
    ),
    pluginRuleTest(
        "good_collapsed_link",
        source_file_name=f"{source_path}good_collapsed_link.md",
    ),
    pluginRuleTest(
        "bad_collapsed_link_both_space",
        source_file_name=f"{source_path}bad_collapsed_link_both_space.md",
        source_file_contents="""this is not
[ a proper ][]
link

[ a proper ]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)
""",
        fix_expected_file_contents="""this is not
[a proper][]
link

[ a proper ]: /url
""",
    ),
    pluginRuleTest(
        "good_shortcut_link",
        source_file_name=f"{source_path}good_shortcut_link.md",
    ),
    pluginRuleTest(
        "bad_shortcut_link_both_space",
        source_file_name=f"{source_path}bad_shortcut_link_both_space.md",
        source_file_contents="""this is not
[ a proper ]
link

[ a proper ]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)
""",
        fix_expected_file_contents="""this is not
[a proper]
link

[ a proper ]: /url
""",
    ),
    pluginRuleTest(
        "good_inline_image",
        source_file_name=f"{source_path}good_inline_image.md",
    ),
    pluginRuleTest(
        "bad_inline_image_trailing_space",
        source_file_name=f"{source_path}bad_inline_image_trailing_space.md",
        source_file_contents="""this is not
![a proper ](https://www.example.com)
link
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)
""",
        fix_expected_file_contents="""this is not
![a proper](https://www.example.com)
link
""",
    ),
    pluginRuleTest(
        "bad_inline_image_leading_space",
        source_file_name=f"{source_path}bad_inline_image_leading_space.md",
        source_file_contents="""this is not
![ a proper](https://www.example.com)
link
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)
""",
        fix_expected_file_contents="""this is not
![a proper](https://www.example.com)
link
""",
    ),
    pluginRuleTest(
        "bad_inline_image_both_space",
        source_file_name=f"{source_path}bad_inline_image_both_space.md",
        source_file_contents="""this is not
![ a proper ](https://www.example.com)
link
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)
""",
        fix_expected_file_contents="""this is not
![a proper](https://www.example.com)
link
""",
    ),
    pluginRuleTest(
        "good_full_image",
        source_file_name=f"{source_path}good_full_image.md",
    ),
    pluginRuleTest(
        "bad_full_image_both_space",
        source_file_name=f"{source_path}bad_full_image_both_space.md",
        source_file_contents="""this is
![ a proper ][bar]
link

[bar]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)
""",
        fix_expected_file_contents="""this is
![a proper][bar]
link

[bar]: /url
""",
    ),
    pluginRuleTest(
        "good_collapsed_image",
        source_file_name=f"{source_path}good_collapsed_image.md",
    ),
    pluginRuleTest(
        "bad_collapsed_image_both_space",
        source_file_name=f"{source_path}bad_collapsed_image_both_space.md",
        source_file_contents="""this is not
![ a proper ][]
link

[ a proper ]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)
""",
        fix_expected_file_contents="""this is not
![a proper][]
link

[ a proper ]: /url
""",
    ),
    pluginRuleTest(
        "good_shortcut_image",
        source_file_name=f"{source_path}good_shortcut_image.md",
    ),
    pluginRuleTest(
        "bad_shortcut_image_both_space",
        source_file_name=f"{source_path}bad_shortcut_image_both_space.md",
        source_file_contents="""this is not
![ a proper ]
link

[ a proper ]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)
""",
        fix_expected_file_contents="""this is not
![a proper]
link

[ a proper ]: /url
""",
    ),
]
fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents:
        fixTests.append(i)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md039_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md039")


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md039_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)
