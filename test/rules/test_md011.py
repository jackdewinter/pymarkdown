"""
Module to provide tests related to the MD011 rule.
"""

import os
from test.rules.utils import (
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md011") + os.sep

scanTests = [
    pluginRuleTest(
        "good_no_reversed",
        source_file_name=f"{source_path}good_no_reversed.md",
        source_file_contents="""This is a normal paragraph
with no reversed link syntax
found within it.
""",
    ),
    pluginRuleTest(
        "bad_with_reversed",
        source_file_name=f"{source_path}bad_with_reversed.md",
        source_file_contents="""This is a normal paragraph
with a (reversed)[link] syntax
found within it.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:8: MD011: Reversed link syntax [(reversed)[link]] (no-reversed-links)
""",
    ),
    pluginRuleTest(
        "good_markdown_footnote",
        source_file_name=f"{source_path}good_markdown_extra.md",
        source_file_contents="""This is a normal paragraph
with a Markdown Extra (example)[^footnote]
text found within it.
""",
    ),
    pluginRuleTest(
        "good_with_reversed_in_code_block",
        source_file_name=f"{source_path}good_with_reversed_in_code_block.md",
        source_file_contents="""```text
This is a normal paragraph
with a (reversed)[link] syntax
found within it.
```
""",
    ),
    pluginRuleTest(
        "good_with_reversed_in_html_block",
        source_file_name=f"{source_path}good_with_reversed_in_html_block.md",
        source_file_contents="""<!--
This is a normal paragraph
with a (reversed)[link] syntax
found within it.
-->
""",
    ),
    pluginRuleTest(
        "issue_1686_bad_two_candidates_on_same_line",
        source_file_contents="""These sequences (text)[url] and (text)[url] are both possible links.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:17: MD011: Reversed link syntax [(text)[url]] (no-reversed-links)
{temp_source_path}:1:33: MD011: Reversed link syntax [(text)[url]] (no-reversed-links)
""",
    ),
    pluginRuleTest(
        "issue_1686_bad_three_candidates_on_same_line",
        source_file_contents="""These sequences (text)[url] and (text)[url] and (text)[url] are all possible links.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:17: MD011: Reversed link syntax [(text)[url]] (no-reversed-links)
{temp_source_path}:1:33: MD011: Reversed link syntax [(text)[url]] (no-reversed-links)
{temp_source_path}:1:49: MD011: Reversed link syntax [(text)[url]] (no-reversed-links)
""",
    ),
    pluginRuleTest(
        "issue_1685_bad_one_candidates_one_real_on_same_line",
        source_file_contents="""These sequences (text)[url] and [text](url) where one is possible and one is real.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:17: MD011: Reversed link syntax [(text)[url]] (no-reversed-links)
""",
    ),
    pluginRuleTest(
        "issue_1684_bad_single_single_after_inactive_table",
        source_file_contents="""| Property | Value |
| --- | --- |
| Aliases | `md011`, `no-reversed-links` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

This rule triggers when inline link syntax has the brackets and parentheses transposed,
such as `(text)[url]` instead of `[text](url)`.

<!-- pyml disable-num-lines 3 no-reversed-links -->
```Markdown
This link (is)[/transposed].
```

> **Explanation**: The `[]` brackets and `()` parentheses are transposed, creating
> an invalid inline link syntax. The rule requires that link text be enclosed in
> `[]` followed by the URL in `()`.

Unlike the previous examples, this case embeds reversed link syntax inside an HTML
comment block, which is also excluded from rule evaluation.

```Markdown
<!--
This (reversed)[link] is in an HTML comment.
-->
```

> **Explanation**: HTML blocks and comments are excluded from inline Markdown parsing,
> so reversed link patterns within them do not trigger the rule.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:10: MD011: Reversed link syntax [(text)[url]] (no-reversed-links)
""",
    ),
    pluginRuleTest(
        "issue_1684_bad_single_single_after_active_table",
        enable_extensions="markdown-tables",
        source_file_contents="""| Property | Value |
| --- | --- |
| Aliases | `md011`, `no-reversed-links` |
| Autofix Available | Pending |
| Enabled By Default | Yes |

This rule triggers when inline link syntax has the brackets and parentheses transposed,
such as `(text)[url]` instead of `[text](url)`.

<!-- pyml disable-num-lines 3 no-reversed-links -->
```Markdown
This link (is)[/transposed].
```

> **Explanation**: The `[]` brackets and `()` parentheses are transposed, creating
> an invalid inline link syntax. The rule requires that link text be enclosed in
> `[]` followed by the URL in `()`.

Unlike the previous examples, this case embeds reversed link syntax inside an HTML
comment block, which is also excluded from rule evaluation.

```Markdown
<!--
This (reversed)[link] is in an HTML comment.
-->
```

> **Explanation**: HTML blocks and comments are excluded from inline Markdown parsing,
> so reversed link patterns within them do not trigger the rule.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:10: MD011: Reversed link syntax [(text)[url]] (no-reversed-links)
""",
    ),
]


@pytest.mark.rules
@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md011_scan(test: pluginRuleTest, request: pytest.FixtureRequest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md011", request=request)


def test_md011_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md011",
        """
  ITEM               DESCRIPTION

  Id                 md011
  Name(s)            no-reversed-links
  Short Description  Reversed link syntax
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md011.md
""",
    )
    execute_query_configuration_test(config_test)
