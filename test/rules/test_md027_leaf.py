"""
Module to provide tests related to the MD027 rule.
"""

import os
from test.rules.utils import (
    execute_fix_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md027") + os.sep

__plugin_disable_md009 = "md009"
__plugin_disable_md022 = "md022"
__plugin_disable_md022_md023 = "md022,md023"
__plugin_disable_md023 = "md023"
__plugin_disable_md031 = "md031"

scanTests = [
    pluginRuleTest(
        "good_block_quote_atx_heading",
        source_file_name=f"{source_path}good_block_quote_atx_heading.md",
        disable_rules=__plugin_disable_md022,
    ),
    pluginRuleTest(
        "bad_block_quote_atx_heading",
        source_file_name=f"{source_path}bad_block_quote_atx_heading.md",
        disable_rules=__plugin_disable_md022_md023,
        source_file_contents="""> this is text
>  # New Heading
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> # New Heading
""",
    ),
    pluginRuleTest(
        "good_block_quote_setext_heading",
        source_file_name=f"{source_path}good_block_quote_setext_heading.md",
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_first_line",
        source_file_name=f"{source_path}bad_block_quote_setext_heading_first_line.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents="""> this is text
>
>  a setext heading
> ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
>
> a setext heading
> ---
""",
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_second_line",
        source_file_name=f"{source_path}bad_block_quote_setext_heading_second_line.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents="""> this is text
>
> a setext heading
>  ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
>
> a setext heading
> ---
""",
    ),
    pluginRuleTest(
        "good_block_quote_setext_heading_multiples",
        source_file_name=f"{source_path}good_block_quote_setext_heading_multiples.md",
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_multiples_first",
        source_file_name=f"{source_path}bad_block_quote_setext_heading_multiples_first.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents="""> this is text
>
>  a setext heading
> that is not properly
> indented
> ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
>
> a setext heading
> that is not properly
> indented
> ---
""",
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_multiples_middle",
        source_file_name=f"{source_path}bad_block_quote_setext_heading_multiples_middle.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents="""> this is text
>
> a setext heading
>  that is not properly
> indented
> ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
>
> a setext heading
> that is not properly
> indented
> ---
""",
    ),
    pluginRuleTest(
        "good_block_quote_setext_heading_multiples_middle___X",
        disable_rules=__plugin_disable_md009,
        source_file_contents="""> this is text
>
> a setext heading\a
> that is not properly\a
> indented
> ---
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_multiples_last",
        source_file_name=f"{source_path}bad_block_quote_setext_heading_multiples_last.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents="""> this is text
>
> a setext heading
> that is not properly
>  indented
> ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
>
> a setext heading
> that is not properly
> indented
> ---
""",
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_multiples_last_x",
        disable_rules=__plugin_disable_md023,
        source_file_contents="""> this is text
>
> a setext heading
> that is not properly
> indented
>  ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
>
> a setext heading
> that is not properly
> indented
> ---
""",
    ),
    pluginRuleTest(
        "good_block_quote_thematic",
        source_file_name=f"{source_path}good_block_quote_thematic.md",
    ),
    pluginRuleTest(
        "bad_block_quote_thematic",
        source_file_contents="""> this is text
>
>  ------
>
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
>
> ------
>
> a real test
""",
    ),
    pluginRuleTest(
        "good_block_quote_html",
        source_file_name=f"{source_path}good_block_quote_html.md",
    ),
    pluginRuleTest(
        "good_block_quote_html_first",
        source_file_name=f"{source_path}good_block_quote_html_first.md",
    ),
    pluginRuleTest(
        "good_block_quote_html_middle",
        source_file_name=f"{source_path}good_block_quote_html_middle.md",
    ),
    pluginRuleTest(
        "good_block_quote_html_last",
        source_file_name=f"{source_path}good_block_quote_html_last.md",
    ),
    pluginRuleTest(
        "good_block_quote_fenced",
        source_file_name=f"{source_path}good_block_quote_fenced.md",
        disable_rules=__plugin_disable_md031,
    ),
    pluginRuleTest(
        "good_block_quote_fenced_middle",
        source_file_name=f"{source_path}good_block_quote_fenced_middle.md",
        disable_rules=__plugin_disable_md031,
    ),
    pluginRuleTest(
        "bad_block_quote_fenced_first",
        source_file_name=f"{source_path}bad_block_quote_fenced_first.md",
        disable_rules=__plugin_disable_md031,
        source_file_contents="""> this is text
>  ```code
> this is a fenced block
> ```
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> ```code
> this is a fenced block
> ```
> a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_fenced_last",
        source_file_name=f"{source_path}bad_block_quote_fenced_last.md",
        disable_rules=__plugin_disable_md031,
        source_file_contents="""> this is text
> ```code
> this is a fenced block
>   ```
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> ```code
> this is a fenced block
> ```
> a real test
""",
    ),
    pluginRuleTest(
        "good_block_quote_indented",
        source_file_name=f"{source_path}good_block_quote_indented.md",
    ),
    pluginRuleTest(
        "good_block_quote_indented_first",
        source_file_name=f"{source_path}good_block_quote_indented_first.md",
    ),
    pluginRuleTest(
        "good_block_quote_indented_middle",
        source_file_name=f"{source_path}good_block_quote_indented_middle.md",
    ),
    pluginRuleTest(
        "good_block_quote_indented_last",
        source_file_name=f"{source_path}good_block_quote_indented_last.md",
    ),
    pluginRuleTest(
        "good_block_quote_lrd",
        source_file_name=f"{source_path}good_block_quote_lrd.md",
    ),
    pluginRuleTest(
        "good_block_quote_lrd_multiple",
        source_file_name=f"{source_path}good_block_quote_lrd_multiple.md",
    ),
    pluginRuleTest(
        "bad_block_quote_lrd_multiple_one",
        source_file_name=f"{source_path}bad_block_quote_lrd_multiple_one.md",
        source_file_contents="""> this is text
>
>  [lab
> el]:
> /url
> "tit
> le"
>
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
>
> [lab
> el]:
> /url
> "tit
> le"
>
> a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_lrd_no_title",
        source_file_contents="""> this is text
>
>  [lab
> el]:
> /url
>
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
>
> [lab
> el]:
> /url
>
> a real test
""",
    ),
    pluginRuleTest(
        "good_block_quote_lrd_multiple_two",
        source_file_name=f"{source_path}good_block_quote_lrd_multiple_two.md",
    ),
    pluginRuleTest(
        "bad_block_quote_lrd_multiple_three",
        source_file_name=f"{source_path}bad_block_quote_lrd_multiple_three.md",
        source_file_contents="""> this is text
>
> [lab
> el]:
>  /url
> "tit
> le"
>
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
>
> [lab
> el]:
> /url
> "tit
> le"
>
> a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_lrd_multiple_four",
        source_file_name=f"{source_path}bad_block_quote_lrd_multiple_four.md",
        source_file_contents="""> this is text
>
> [lab
> el]:
> /url
>  "tit
> le"
>
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
>
> [lab
> el]:
> /url
> "tit
> le"
>
> a real test
""",
    ),
    pluginRuleTest(
        "good_block_quote_lrd_multiple_five",
        source_file_name=f"{source_path}good_block_quote_lrd_multiple_five.md",
    ),
    pluginRuleTest(
        "bad_block_quote_link_multiple_extra",
        source_file_name=f"{source_path}bad_block_quote_link_multiple_extra.md",
        source_file_contents="""> this is text
> [a not
>  so
>  simple](/link
> "a
>  title"
>  )
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:6:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:7:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> [a not
> so
> simple](/link
> "a
> title"
> )
> a real test
""",
    ),
]
fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents:
        fixTests.append(i)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md027_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md027")


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md027_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)
