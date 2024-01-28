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


__plugin_disable_md022_md023 = "md022,md023"
__plugin_disable_md023 = "md023"
__plugin_disable_md031 = "md031"

scanTests = [
    pluginRuleTest(
        "bad_block_quote_atx_heading_plus_one",
        source_file_name=f"{source_path}bad_block_quote_atx_heading_plus_one.md",
        disable_rules=__plugin_disable_md022_md023,
        source_file_contents=""" > this is text
 >  # New Heading
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 > # New Heading
""",
    ),
    pluginRuleTest(
        "bad_block_quote_atx_heading_misaligned",
        source_file_name=f"{source_path}bad_block_quote_atx_heading_misaligned.md",
        disable_rules=__plugin_disable_md022_md023,
        source_file_contents=""" > this is text
>  # New Heading
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
> # New Heading
""",
    ),
    pluginRuleTest(
        "bad_block_quote_fenced_first_plus_one",
        source_file_name=f"{source_path}bad_block_quote_fenced_first_plus_one.md",
        disable_rules=__plugin_disable_md031,
        source_file_contents=""" > this is text
 >  ```code
 > this is a fenced block
 > ```
 > a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 > ```code
 > this is a fenced block
 > ```
 > a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_fenced_last_plus_one",
        source_file_name=f"{source_path}bad_block_quote_fenced_last_plus_one.md",
        disable_rules=__plugin_disable_md031,
        source_file_contents=""" > this is text
 > ```code
 > this is a fenced block
 >   ```
 > a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 > ```code
 > this is a fenced block
 > ```
 > a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_fenced_last_misaligned",
        source_file_name=f"{source_path}bad_block_quote_fenced_last_misaligned.md",
        disable_rules=__plugin_disable_md031,
        source_file_contents=""" > this is text
 > ```code
 > this is a fenced block
>   ```
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 > ```code
 > this is a fenced block
> ```
> a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_lrd_multiple_one_plus_one",
        source_file_name=f"{source_path}bad_block_quote_lrd_multiple_one_plus_one.md",
        source_file_contents=""" > this is text
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
        scan_expected_output="""{temp_source_path}:3:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
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
        "bad_block_quote_lrd_multiple_three_plus_one",
        source_file_name=f"{source_path}bad_block_quote_lrd_multiple_three_plus_one.md",
        source_file_contents=""" > this is text
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
        scan_expected_output="""{temp_source_path}:5:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
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
        "bad_block_quote_lrd_multiple_three_misaligned",
        source_file_name=f"{source_path}bad_block_quote_lrd_multiple_three_misaligned.md",
        source_file_contents=""" > this is text
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
        fix_expected_file_contents=""" > this is text
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
        "bad_block_quote_lrd_multiple_four_plus_one",
        source_file_name=f"{source_path}bad_block_quote_lrd_multiple_four_plus_one.md",
        source_file_contents=""" > this is text
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
        scan_expected_output="""{temp_source_path}:6:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
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
        "bad_block_quote_lrd_multiple_four_misaligned",
        source_file_name=f"{source_path}bad_block_quote_lrd_multiple_four_plus_one.md",
        source_file_contents=""" > this is text
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
        scan_expected_output="""{temp_source_path}:6:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
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
        "bad_block_quote_thematic_plus_one",
        source_file_name=f"{source_path}bad_block_quote_thematic_plus_one.md",
        source_file_contents=""" > this is text
 >
 >  ------
 >
 > a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 >
 > ------
 >
 > a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_first_line_plus_one",
        source_file_name=f"{source_path}bad_block_quote_setext_heading_first_line_plus_one.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents=""" > this is text
 >
 >  a setext heading
 > ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 >
 > a setext heading
 > ---
""",
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_multiples_first_plus_one",
        source_file_name=f"{source_path}bad_block_quote_setext_heading_multiples_first_plus_one.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents=""" > this is text
 >
 >  a setext heading
 > that is not properly
 > indented
 > ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 >
 > a setext heading
 > that is not properly
 > indented
 > ---
""",
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_multiples_middle_plus_one",
        source_file_name=f"{source_path}bad_block_quote_setext_heading_multiples_middle_plus_one.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents=""" > this is text
 >
 > a setext heading
 >  that is not properly
 > indented
 > ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 >
 > a setext heading
 > that is not properly
 > indented
 > ---
""",
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_multiples_middle_misaligned",
        source_file_name=f"{source_path}bad_block_quote_setext_heading_multiples_middle_misaligned.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents=""" > this is text
 >
 > a setext heading
>  that is not properly
> indented
> ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 >
 > a setext heading
> that is not properly
> indented
> ---
""",
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_multiples_last_plus_one",
        source_file_name=f"{source_path}bad_block_quote_setext_heading_multiples_last_plus_one.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents=""" > this is text
 >
 > a setext heading
 > that is not properly
 >  indented
 > ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 >
 > a setext heading
 > that is not properly
 > indented
 > ---
""",
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_multiples_last_misaligned",
        source_file_name=f"{source_path}bad_block_quote_setext_heading_multiples_last_misaligned.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents=""" > this is text
 >
 > a setext heading
 > that is not properly
>  indented
> ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 >
 > a setext heading
 > that is not properly
> indented
> ---
""",
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_second_line_plus_one",
        source_file_name=f"{source_path}bad_block_quote_setext_heading_second_line_plus_one.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents=""" > this is text
 >
 > a setext heading
 >  ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 >
 > a setext heading
 > ---
""",
    ),
    pluginRuleTest(
        "bad_block_quote_setext_heading_second_line_misaligned",
        source_file_name=f"{source_path}bad_block_quote_setext_heading_second_line_misaligned.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents=""" > this is text
 >
 > a setext heading
>  ---
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 >
 > a setext heading
> ---
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
