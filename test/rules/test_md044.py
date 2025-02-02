"""
Module to provide tests related to the MD044 rule.
"""

import os
from test.rules.utils import (
    calculate_fix_tests,
    execute_configuration_test,
    execute_fix_test,
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginConfigErrorTest,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md044") + os.sep


configTests = [
    pluginConfigErrorTest(
        "names_bad_type",
        use_strict_config=True,
        set_args=["plugins.md044.names=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md044.names' must be of type 'str'.""",
    ),
    pluginConfigErrorTest(
        "names_empty_elements",
        use_strict_config=True,
        set_args=["plugins.md044.names=,,"],
        expected_error="""BadPluginError encountered while configuring plugins:
Elements in the comma-separated list cannot be empty.""",
    ),
    pluginConfigErrorTest(
        "names_repeated_elements",
        use_strict_config=True,
        set_args=["plugins.md044.names=one,two,One"],
        expected_error="""BadPluginError encountered while configuring plugins:
Element `One` is already present in the list as `one`.""",
    ),
    pluginConfigErrorTest(
        "code_blocks",
        use_strict_config=True,
        set_args=["plugins.md044.code_blocks=one"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md044.code_blocks' must be of type 'bool'.""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_paragraph_text",
        source_file_contents="""this is a paragraph without any capitalization errors
""",
        set_args=["plugins.md044.names=paragraph"],
    ),
    pluginRuleTest(
        "bad_paragraph_text",
        source_file_contents="""this is a paragraph without any capitalization errors
""",
        set_args=["plugins.md044.names=ParaGraph"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:11: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a ParaGraph without any capitalization errors
""",
    ),
    pluginRuleTest(
        "good_paragraph_text_prefix",
        source_file_contents="""nothing like a good reparagraph to go
""",
        set_args=["plugins.md044.names=ParaGraph"],
    ),
    pluginRuleTest(
        "good_paragraph_text_suffix",
        source_file_contents="""this is paragraphing at its best
""",
        set_args=["plugins.md044.names=ParaGraph"],
    ),
    pluginRuleTest(
        "bad_paragraph_text_start",
        source_file_contents="""paragraph is how this starts
""",
        set_args=["plugins.md044.names=ParaGraph"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""ParaGraph is how this starts
""",
    ),
    pluginRuleTest(
        "bad_paragraph_text_end",
        source_file_contents="""ends with the word paragraph
""",
        set_args=["plugins.md044.names=ParaGraph"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:20: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""ends with the word ParaGraph
""",
    ),
    pluginRuleTest(
        "bad_paragraph_text_followed_non_alpha",
        source_file_contents="""this is a paragraph.
""",
        set_args=["plugins.md044.names=ParaGraph"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:11: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a ParaGraph.
""",
    ),
    pluginRuleTest(
        "bad_paragraph_text_multiples",
        source_file_contents="""this is a paragraph with paragraph capitalization errors
""",
        set_args=["plugins.md044.names=ParaGraph"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:11: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:1:26: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a ParaGraph with ParaGraph capitalization errors
""",
    ),
    pluginRuleTest(
        "bad_paragraph_text_multiples_on_multiple_lines",
        source_file_contents="""this is a sample where the word paragraph should
appear on multiple lines so we can make sure that
advancing the line and column for the paragraph
error reporting works.
""",
        set_args=["plugins.md044.names=ParaGraph"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:33: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:3:39: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a sample where the word ParaGraph should
appear on multiple lines so we can make sure that
advancing the line and column for the ParaGraph
error reporting works.
""",
    ),
    pluginRuleTest(
        "bad_paragraph_text_backslash",
        source_file_contents="""paragraph \\! paragraph
""",
        set_args=["plugins.md044.names=ParaGraph"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:1:14: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""ParaGraph \\! ParaGraph
""",
    ),
    pluginRuleTest(
        "bad_paragraph_text_reference",
        source_file_contents="""paragraph &amp; paragraph
""",
        set_args=["plugins.md044.names=ParaGraph"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:1:17: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""ParaGraph &amp; ParaGraph
""",
    ),
    pluginRuleTest(
        "bad_atx_heading_text",
        source_file_contents="""# This section contains a paragraph

yes, a paragraph is contained.
""",
        set_args=["plugins.md044.names=ParaGraph"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:27: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:3:8: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""# This section contains a ParaGraph

yes, a ParaGraph is contained.
""",
    ),
    pluginRuleTest(
        "bad_setext_heading_text",
        source_file_contents="""This section contains a paragraph
===

yes, a paragraph is contained.
""",
        set_args=["plugins.md044.names=ParaGraph"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:25: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:4:8: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""This section contains a ParaGraph
===

yes, a ParaGraph is contained.
""",
    ),
    pluginRuleTest(
        "bad_indented_code_block_text",
        source_file_contents="""# This section contains a paragraph

    yes, a paragraph is contained.
""",
        set_args=["plugins.md044.names=ParaGraph"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:27: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:3:12: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""# This section contains a ParaGraph

    yes, a ParaGraph is contained.
""",
    ),
    pluginRuleTest(
        "bad_indented_code_block_text_no_code_blocks",
        source_file_contents="""# This section contains a paragraph

    yes, a paragraph is contained.
""",
        set_args=["plugins.md044.names=ParaGraph", "plugins.md044.code_blocks=$!False"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:27: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""# This section contains a ParaGraph

    yes, a paragraph is contained.
""",
    ),
    pluginRuleTest(
        "bad_fenced_code_block_text",
        source_file_contents="""# This section contains a paragraph

```text
yes, a paragraph is contained.
```
""",
        set_args=["plugins.md044.names=ParaGraph"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:27: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:4:8: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""# This section contains a ParaGraph

```text
yes, a ParaGraph is contained.
```
""",
    ),
    pluginRuleTest(
        "bad_fenced_code_block_text_no_code_blocks",
        source_file_contents="""# This section contains a paragraph

```text
yes, a paragraph is contained.
```
""",
        set_args=["plugins.md044.names=ParaGraph", "plugins.md044.code_blocks=$!False"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:27: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""# This section contains a ParaGraph

```text
yes, a paragraph is contained.
```
""",
    ),
    pluginRuleTest(
        "bad_html_block_text",
        source_file_contents="""# This section contains a paragraph

<!--
yes, a paragraph is contained.
-->
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:27: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:4:8: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""# This section contains a ParaGraph

<!--
yes, a ParaGraph is contained.
-->
""",
    ),
    pluginRuleTest(
        "bad_block_quote_text",
        source_file_contents="""# This section contains a paragraph

> yes, a paragraph is contained.
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:27: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:3:10: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""# This section contains a ParaGraph

> yes, a ParaGraph is contained.
""",
    ),
    pluginRuleTest(
        "bad_code_span_text",
        source_file_contents="""# This section contains a paragraph

yes, `a paragraph is` contained.
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:27: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:3:9: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""# This section contains a ParaGraph

yes, `a ParaGraph is` contained.
""",
    ),
    pluginRuleTest(
        "bad_code_span_text_with_code_blocks_disabled",
        source_file_contents="""# This section contains a paragraph

yes, `a paragraph is` contained.
""",
        set_args=["plugins.md044.names=ParaGraph", "plugins.md044.code_spans=$!False"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:27: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""# This section contains a ParaGraph

yes, `a paragraph is` contained.
""",
    ),
    pluginRuleTest(
        "bad_code_span_text_multiple_lines",
        source_file_contents="""# This section contains a paragraph

yes, `a paragraph a
is a paragraph` contained.
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:27: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:3:9: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:4:6: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""# This section contains a ParaGraph

yes, `a ParaGraph a
is a ParaGraph` contained.
""",
    ),
    pluginRuleTest(
        "bad_inline_link",
        source_file_contents="""[a paragraph inspired link](/paragraph "paragraph")
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:1:41: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""[a ParaGraph inspired link](/paragraph "ParaGraph")
""",
    ),
    pluginRuleTest(
        "bad_inline_link_backslash",
        source_file_contents="""[a paragraph inspired \\! paragraph link](/paragraph "paragraph \\! paragraph")
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:1:26: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:1:54: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:1:67: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""[a ParaGraph inspired \\! ParaGraph link](/paragraph "ParaGraph \\! ParaGraph")
""",
    ),
    pluginRuleTest(
        "bad_inline_link_reference",
        source_file_contents="""[a paragraph inspired &amp; paragraph link](/paragraph "paragraph &amp; paragraph")
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:1:29: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:1:57: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:1:73: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""[a ParaGraph inspired &amp; ParaGraph link](/paragraph "ParaGraph &amp; ParaGraph")
""",
    ),
    pluginRuleTest(
        "bad_inline_link_multiple_lines_one",
        source_file_contents="""[a paragraph inspired link](
/paragraph
"paragraph")
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:3:2: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""[a ParaGraph inspired link](
/paragraph
"ParaGraph")
""",
    ),
    pluginRuleTest(
        "bad_inline_link_multiple_lines_two",
        source_file_contents="""[a paragraph inspired link](
/paragraph
"this is
a very long paragraph")
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:4:13: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""[a ParaGraph inspired link](
/paragraph
"this is
a very long ParaGraph")
""",
    ),
    pluginRuleTest(
        "bad_inline_link_multiple_lines_three",
        source_file_contents="""[a
paragraph inspired link](
/paragraph
"paragraph")
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:4:2: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""[a
ParaGraph inspired link](
/paragraph
"ParaGraph")
""",
    ),
    pluginRuleTest(
        "bad_inline_image",
        source_file_contents="""![a paragraph inspired link](/paragraph "paragraph")
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:1:42: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""![a ParaGraph inspired link](/paragraph "ParaGraph")
""",
    ),
    pluginRuleTest(
        "bad_inline_image_multiple_lines_one",
        source_file_contents="""![a paragraph inspired link](
/paragraph
"paragraph")
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:3:2: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""![a ParaGraph inspired link](
/paragraph
"ParaGraph")
""",
    ),
    pluginRuleTest(
        "bad_inline_image_multiple_lines_two",
        source_file_contents="""![a paragraph inspired link](
/paragraph
"this is
a very long paragraph")
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:4:13: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""![a ParaGraph inspired link](
/paragraph
"this is
a very long ParaGraph")
""",
    ),
    pluginRuleTest(
        "bad_full_link",
        source_file_contents="""this is
[a paragraph inspired link][bar]
link

[bar]: /url "a paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:4: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:5:16: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is
[a ParaGraph inspired link][bar]
link

[bar]: /url "a ParaGraph title"
""",
    ),
    pluginRuleTest(
        "bad_full_link_multiple",
        source_file_contents="""this is
[a
paragraph inspired link][ba
r]
link

[ba
r]: /url "a
paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:9:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is
[a
ParaGraph inspired link][ba
r]
link

[ba
r]: /url "a
ParaGraph title"
""",
    ),
    pluginRuleTest(
        "bad_full_image",
        source_file_contents="""this is
![a paragraph inspired link][bar]
link

[bar]: /url "a paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:5:16: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is
![a ParaGraph inspired link][bar]
link

[bar]: /url "a ParaGraph title"
""",
    ),
    pluginRuleTest(
        "bad_full_image_multiple",
        source_file_contents="""this is
![a
paragraph inspired link][ba
r]
link

[ba
r]: /url "a
paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:9:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is
![a
ParaGraph inspired link][ba
r]
link

[ba
r]: /url "a
ParaGraph title"
""",
    ),
    pluginRuleTest(
        "bad_collapsed_link",
        source_file_contents="""this is a
[collapsed
paragraph][]
link

[collapsed
paragraph]: /url "a paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:7:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:7:21: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a
[collapsed
ParaGraph][]
link

[collapsed
ParaGraph]: /url "a ParaGraph title"
""",
    ),
    pluginRuleTest(
        "bad_collapsed_link_multiple",
        source_file_contents="""this is a
[collapsed
link paragraph][]
link

[collapsed
link paragraph]: /url "a
big paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:6: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:7:6: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:8:5: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a
[collapsed
link ParaGraph][]
link

[collapsed
link ParaGraph]: /url "a
big ParaGraph title"
""",
    ),
    pluginRuleTest(
        "bad_collapsed_image",
        source_file_contents="""this is a
![collapsed
paragraph][]
link

[collapsed
paragraph]: /url "a paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:7:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:7:21: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a
![collapsed
ParaGraph][]
link

[collapsed
ParaGraph]: /url "a ParaGraph title"
""",
    ),
    pluginRuleTest(
        "bad_collapsed_image_multiple",
        source_file_contents="""this is a
![collapsed
paragraph][]
link

[collapsed
paragraph]: /url "a
big paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:7:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:8:5: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a
![collapsed
ParaGraph][]
link

[collapsed
ParaGraph]: /url "a
big ParaGraph title"
""",
    ),
    pluginRuleTest(
        "bad_shortcut_link",
        source_file_contents="""this is a
[another
paragraph]
link

[another
paragraph]: /url "a paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:7:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:7:21: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a
[another
ParaGraph]
link

[another
ParaGraph]: /url "a ParaGraph title"
""",
    ),
    pluginRuleTest(
        "bad_shortcut_link_no_title",
        source_file_contents="""this is a
[another
paragraph]
link

[another
paragraph]: /url
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:7:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a
[another
ParaGraph]
link

[another
ParaGraph]: /url
""",
    ),
    pluginRuleTest(
        "bad_shortcut_link_backslash",
        source_file_contents="""this is a
[paragraph \\! paragraph]
link

[paragraph \\! paragraph]: /paragraph "a paragraph \\! paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:2: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:2:15: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:5:2: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:5:15: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:5:41: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:5:54: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a
[ParaGraph \\! ParaGraph]
link

[ParaGraph \\! ParaGraph]: /paragraph "a ParaGraph \\! ParaGraph title"
""",
    ),
    pluginRuleTest(
        "bad_shortcut_link_reference",
        source_file_contents="""this is a
[paragraph &amp; paragraph]
link

[paragraph &amp; paragraph]: /paragraph "a paragraph &amp; paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:2: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:2:18: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:5:2: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:5:18: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:5:44: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:5:60: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a
[ParaGraph &amp; ParaGraph]
link

[ParaGraph &amp; ParaGraph]: /paragraph "a ParaGraph &amp; ParaGraph title"
""",
    ),
    pluginRuleTest(
        "bad_shortcut_link_multiple",
        source_file_contents="""this is a
[collapsed
link paragraph]
link

[collapsed
link paragraph]: /url "a
big paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:6: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:7:6: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:8:5: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a
[collapsed
link ParaGraph]
link

[collapsed
link ParaGraph]: /url "a
big ParaGraph title"
""",
    ),
    pluginRuleTest(
        "bad_shortcut_image",
        source_file_contents="""this is a
![collapsed
paragraph]
link

[collapsed
paragraph]: /url "a paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:7:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:7:21: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a
![collapsed
ParaGraph]
link

[collapsed
ParaGraph]: /url "a ParaGraph title"
""",
    ),
    pluginRuleTest(
        "bad_shortcut_image_multiple",
        source_file_contents="""this is a
![collapsed
paragraph]
link

[collapsed
paragraph]: /url "a
big paragraph title"
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:7:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:8:5: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this is a
![collapsed
ParaGraph]
link

[collapsed
ParaGraph]: /url "a
big ParaGraph title"
""",
    ),
    pluginRuleTest(
        "mix_md044_md037",
        source_file_contents="""this * paragraph * is the best!
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        # disable_rules=__plugin_disable_md007,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:7: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
{temp_source_path}:1:8: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{temp_source_path}:1:17: MD037: Spaces inside emphasis markers (no-space-in-emphasis)
""",
        fix_expected_file_contents="""this *ParaGraph* is the best!
""",
    ),
    pluginRuleTest(
        "mix_md044_md038",
        source_file_contents="""this this is ` paragraph` is the best!
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        # disable_rules=__plugin_disable_md007,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:14: MD038: Spaces inside code span elements (no-space-in-code)
{temp_source_path}:1:16: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this this is `ParaGraph` is the best!
""",
    ),
    pluginRuleTest(
        "mix_md044_md039",
        source_file_contents="""this link
[ paragraph ](https://www.example.com)
is bad
""",
        set_args=["plugins.md044.names=ParaGraph"],
        use_strict_config=True,
        # disable_rules=__plugin_disable_md007,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD039: Spaces inside link text (no-space-in-links)
{temp_source_path}:2:3: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
""",
        fix_expected_file_contents="""this link
[ParaGraph](https://www.example.com)
is bad
""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md044_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md044")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md044_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md044_config(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(
        test,
        file_contents="""this is a paragraph without any capitalization errors
""",
    )


def test_md044_query_config():
    config_test = pluginQueryConfigTest(
        "md044",
        """
  ITEM               DESCRIPTION

  Id                 md044
  Name(s)            proper-names
  Short Description  Proper names should have the correct capitalization
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md044.md


  CONFIGURATION ITEM  TYPE     VALUE

  code_blocks         boolean  True
  code_spans          boolean  True
  names               string   ""

""",
    )
    execute_query_configuration_test(config_test)
