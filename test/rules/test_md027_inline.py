"""
Module to provide tests related to the MD027 rule.
"""

import os
from test.rules.utils import (
    calculate_fix_tests,
    execute_fix_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md027") + os.sep

scanTests = [
    pluginRuleTest(
        "good_block_quote_code_span",
        source_file_name=f"{source_path}good_block_quote_code_span.md",
    ),
    pluginRuleTest(
        "bad_block_quote_code_span_multiple",
        source_file_name=f"{source_path}bad_block_quote_code_span_multiple.md",
        source_file_contents="""> this is text
> `code
>  span`
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> `code
> span`
> a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_code_span_multiple_plus_one",
        source_file_name=f"{source_path}bad_block_quote_code_span_multiple_plus_one.md",
        source_file_contents=""" > this is text
 > `code
 >  span`
 > a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 > `code
 > span`
 > a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_code_span_multiple_misaligned",
        source_file_name=f"{source_path}bad_block_quote_code_span_multiple_misaligned.md",
        source_file_contents=""" > this is text
 > `code
>  span`
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 > `code
> span`
> a real test
""",
    ),
    pluginRuleTest(
        "good_block_quote_emphasis",
        source_file_name=f"{source_path}good_block_quote_emphasis.md",
    ),
    pluginRuleTest(
        "bad_block_quote_emphasis_multiple",
        source_file_name=f"{source_path}good_block_quote_emphasis_multiple.md",
        source_file_contents="""> this is *text
>  that this is
> emphasis*
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is *text
> that this is
> emphasis*
> a real test
""",
    ),
    pluginRuleTest(
        "good_block_quote_link",
        source_file_name=f"{source_path}good_block_quote_link.md",
    ),
    pluginRuleTest(
        "bad_block_quote_link",
        source_file_name=f"{source_path}bad_block_quote_link.md",
        source_file_contents="""> this is text
>  [not so
>  simple](
>  /link
>  "this is
>  a title")
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:5:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:6:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> [not so
> simple](
> /link
> "this is
> a title")
> a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_link_multiple",
        source_file_name=f"{source_path}good_block_quote_link_multiple.md",
        source_file_contents="""> this is text
> [a not
>  so simple](/link
> "a
>  title")
>  )
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:5:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:6:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> [a not
> so simple](/link
> "a
> title")
> )
> a real test
""",
    ),
    pluginRuleTest(
        "good_block_quote_raw_html",
        source_file_name=f"{source_path}good_block_quote_raw_html.md",
    ),
    pluginRuleTest(
        "bad_block_quote_raw_html_multiple",
        source_file_name=f"{source_path}bad_block_quote_raw_html_multiple.md",
        source_file_contents="""> this is text
> a <!-- comment
>  --> huh?
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> a <!-- comment
> --> huh?
> a real test
""",
    ),
    pluginRuleTest(
        "good_block_quote_autolink",
        source_file_name=f"{source_path}good_block_quote_autolink.md",
    ),
    pluginRuleTest(
        "bad_block_quote_autolink",
        source_file_name=f"{source_path}bad_block_quote_autolink.md",
        source_file_contents="""> this is text
>  <https://example.com>
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> <https://example.com>
> a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_autolink_plus_one",
        source_file_name=f"{source_path}bad_block_quote_autolink_plus_one.md",
        source_file_contents=""" > this is text
 >  <https://example.com>
 > a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:4: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents=""" > this is text
 > <https://example.com>
 > a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_code_span",
        source_file_name=f"{source_path}bad_block_quote_code_span.md",
        source_file_contents="""> this is text
>  `code span`
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> `code span`
> a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_code_span_multiple_before",
        source_file_name=f"{source_path}bad_block_quote_code_span_multiple_before.md",
        source_file_contents="""> this is text
>  `code
> span`
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> `code
> span`
> a real test
""",
    ),
    pluginRuleTest(
        "good_block_quote_emphasis_start",
        source_file_name=f"{source_path}good_block_quote_emphasis_start.md",
    ),
    pluginRuleTest(
        "bad_block_quote_emphasis_start",
        source_file_name=f"{source_path}bad_block_quote_emphasis_start.md",
        source_file_contents="""> this is text
>  *this* is emphasis
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> *this* is emphasis
> a real test
""",
    ),
    pluginRuleTest(
        "good_block_quote_image",
        source_file_name=f"{source_path}good_block_quote_image.md",
    ),
    pluginRuleTest(
        "good_block_quote_image_multiple",
        source_file_name=f"{source_path}good_block_quote_image_multiple.md",
        source_file_contents="""> this is text
> ![a not
>  so simple](/link
> "a
>  title")
>  )
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:5:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:6:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> ![a not
> so simple](/link
> "a
> title")
> )
> a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_image",
        source_file_name=f"{source_path}bad_block_quote_image.md",
        source_file_contents="""> this is text
>  ![not so
>  simple](
>  /link
>  "this is
>  a title")
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:5:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:6:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> ![not so
> simple](
> /link
> "this is
> a title")
> a real test
""",
    ),
    pluginRuleTest(
        "bad_block_quote_image_multiple_extra",
        source_file_name=f"{source_path}bad_block_quote_image_multiple_extra.md",
        source_file_contents="""> this is text
>  ![a not
>  so
>  simple](/link
> "a
>  title"
>  )
> a real test
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:6:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:7:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> ![a not
> so
> simple](/link
> "a
> title"
> )
> a real test
""",
    ),
    pluginRuleTest(
        "good_block_quote_raw_html2",
        source_file_name=f"{source_path}bad_block_quote_raw_html.md",
    ),
    pluginRuleTest(
        "good_block_quote_full_link",
        source_file_name=f"{source_path}good_block_quote_full_link.md",
    ),
    pluginRuleTest(
        "bad_block_quote_full_link",
        source_file_name=f"{source_path}bad_block_quote_full_link.md",
        source_file_contents="""> this is text
>  [simple][simple]
> a real test

[simple]: /link
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> [simple][simple]
> a real test

[simple]: /link
""",
    ),
    pluginRuleTest(
        "good_block_quote_collapsed_link",
        source_file_name=f"{source_path}good_block_quote_collapsed_link.md",
    ),
    pluginRuleTest(
        "bad_block_quote_collapsed_link",
        source_file_name=f"{source_path}bad_block_quote_collapsed_link.md",
        source_file_contents="""> this is text
>  [simple][]
> a real test

[simple]: /link
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> [simple][]
> a real test

[simple]: /link
""",
    ),
    pluginRuleTest(
        "good_block_quote_shortcut_link",
        source_file_name=f"{source_path}good_block_quote_shortcut_link.md",
    ),
    pluginRuleTest(
        "bad_block_quote_shortcut_link",
        source_file_name=f"{source_path}bad_block_quote_shortcut_link.md",
        source_file_contents="""> this is text
>  [simple]
> a real test

[simple]: /link
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
""",
        fix_expected_file_contents="""> this is text
> [simple]
> a real test

[simple]: /link
""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md027_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md027")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md027_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)
