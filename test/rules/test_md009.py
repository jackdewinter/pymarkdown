"""
Module to provide tests related to the MD009 rule.
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

source_path = os.path.join("test", "resources", "rules", "md009") + os.sep

__plugin_disable_md012 = "md012"
__plugin_disable_md023 = "md023"
__plugin_disable_md033 = "md033"

configTests = [
    pluginConfigErrorTest(
        "invalid_br_spaces",
        use_strict_config=True,
        set_args=["plugins.md009.br_spaces=not-integer"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md009.br_spaces' must be of type 'int'.""",
    ),
    pluginConfigErrorTest(
        "br_spaces_range",
        use_strict_config=True,
        set_args=["plugins.md009.br_spaces=$#-1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md009.br_spaces' is not valid: Allowable values are greater than or equal to 0.""",
    ),
    pluginConfigErrorTest(
        "strict_not_boolean",
        use_strict_config=True,
        set_args=["plugins.md009.strict=not-boolean"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md009.strict' must be of type 'bool'.""",
    ),
    pluginConfigErrorTest(
        "list_item_empty_lines_not_boolean",
        use_strict_config=True,
        set_args=["plugins.md009.list_item_empty_lines=not-boolean"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md009.list_item_empty_lines' must be of type 'bool'.""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_paragraph_no_extra",
        source_file_name=f"{source_path}good_paragraph_no_extra.md",
    ),
    pluginRuleTest(
        "two_paragraphs_list_item_empty_line_no_spaces",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        source_file_contents="""this is one paragraph
\a\a\a\a
this is another paragraph
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD009: Trailing spaces [Expected: 0 or 2; Actual: 4] (no-trailing-spaces)
""",
    ),
    pluginRuleTest(
        "good_indented_code_block_with_extra",
        source_file_name=f"{source_path}good_indented_code_block_with_extra.md",
    ),
    pluginRuleTest(
        "good_fenced_code_block_with_extra",
        source_file_name=f"{source_path}good_fenced_code_block_with_extra.md",
    ),
    pluginRuleTest(
        "unordered_list_item_empty_line_no_spaces",
        source_file_contents="""- list item text

  list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "unordered_list_item_empty_line",
        source_file_name=f"{source_path}good_unordered_list_item_empty_lines.md",
        source_file_contents="""- list item text
\a\a
  list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "unordered_list_item_empty_line_strict",
        source_file_name=f"{source_path}good_unordered_list_item_empty_lines.md",
        set_args=["plugins.md009.strict=$!True"],
        source_file_contents="""- list item text
\a\a
  list item text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD009: Trailing spaces [Expected: 0; Actual: 2] (no-trailing-spaces)
""",
        fix_expected_file_contents="""- list item text

  list item text
""",
    ),
    pluginRuleTest(
        "unordered_list_item_empty_line_extra_space",
        source_file_contents="""- list item text
\a\a\a\a
  list item text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD009: Trailing spaces [Expected: 0 or 2; Actual: 4] (no-trailing-spaces)
""",
        fix_expected_file_contents="""- list item text
\a\a
  list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "unordered_list_item_empty_line_extra_space_strict",
        source_file_contents="""- list item text
\a\a\a\a
  list item text
""".replace(
            "\a", " "
        ),
        set_args=["plugins.md009.strict=$!True"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD009: Trailing spaces [Expected: 0; Actual: 4] (no-trailing-spaces)
""",
        fix_expected_file_contents="""- list item text

  list item text
""",
    ),
    pluginRuleTest(
        "ordered_list_item_empty_line_no_spaces",
        source_file_contents="""1. list item text

   list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "ordered_list_item_empty_line",
        source_file_contents="""1. list item text
\a\a
   list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "ordered_list_item_empty_line_strict",
        source_file_contents="""1. list item text
\a\a
   list item text
""".replace(
            "\a", " "
        ),
        set_args=["plugins.md009.strict=$!True"],
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:2:1: MD009: Trailing spaces [Expected: 0; Actual: 2] (no-trailing-spaces)",
        fix_expected_file_contents="""1. list item text

   list item text
""",
    ),
    pluginRuleTest(
        "ordered_list_item_empty_line_extra_space",
        source_file_contents="""1. list item text
\a\a\a\a
   list item text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD009: Trailing spaces [Expected: 0 or 2; Actual: 4] (no-trailing-spaces)
""",
        fix_expected_file_contents="""1. list item text
\a\a
   list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "ordered_list_item_empty_line_extra_space_strict",
        source_file_contents="""1. list item text
\a\a\a\a
   list item text
""".replace(
            "\a", " "
        ),
        set_args=["plugins.md009.strict=$!True"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD009: Trailing spaces [Expected: 0; Actual: 4] (no-trailing-spaces)
""",
        fix_expected_file_contents="""1. list item text

   list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "unordered_list_item_empty_line_with_list_empty_and_exact_spaces",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""- list item text
\a\a\a\a
  list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "unordered_list_item_empty_line_with_list_empty_and_exact_spaces_minus_one",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""- list item text
\a\a\a
  list item text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD009: Trailing spaces [Expected: 4; Actual: 3] (no-trailing-spaces)
""",
        fix_expected_file_contents="""- list item text
\a\a\a\a
  list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "unordered_list_item_empty_line_with_list_empty_and_exact_spaces_plus_one",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""- list item text
\a\a\a\a\a
  list item text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD009: Trailing spaces [Expected: 4; Actual: 5] (no-trailing-spaces)
""",
        fix_expected_file_contents="""- list item text
\a\a\a\a
  list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "unordered_list_item_with_new_list_item_empty_line_with_list_empty_and_exact_spaces",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""- list item text
- list item text
\a\a\a\a
  list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "unordered_list_item_with_new_list_item_empty_line_with_list_empty_and_exact_spaces_plus_one",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""- list item text
- list item text
\a\a\a\a\a
  list item text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD009: Trailing spaces [Expected: 4; Actual: 5] (no-trailing-spaces)
""",
        fix_expected_file_contents="""- list item text
- list item text
\a\a\a\a
  list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "unordered_list_item_with_nested_list_item_empty_line_with_list_empty_and_exact_spaces",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""- list item text
  - list item text
\a\a\a\a\a\a
    list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "unordered_list_item_with_nested_list_item_empty_line_with_list_empty_and_exact_spaces_plus_one",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""- list item text
  - list item text
\a\a\a\a\a\a\a
    list item text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD009: Trailing spaces [Expected: 6; Actual: 7] (no-trailing-spaces)
""",
        fix_expected_file_contents="""- list item text
  - list item text
\a\a\a\a\a\a
    list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "ordered_list_item_empty_line_with_list_empty_and_exact_spaces",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""1. list item text
\a\a\a\a\a
   list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "ordered_list_item_empty_line_with_list_empty_and_exact_spaces_minus_one",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""1. list item text
\a\a\a\a
   list item text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD009: Trailing spaces [Expected: 5; Actual: 4] (no-trailing-spaces)
""",
        fix_expected_file_contents="""1. list item text
\a\a\a\a\a
   list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "ordered_list_item_empty_line_with_list_empty_and_exact_spaces_plus_one",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""1. list item text
\a\a\a\a\a\a
   list item text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD009: Trailing spaces [Expected: 5; Actual: 6] (no-trailing-spaces)
""",
        fix_expected_file_contents="""1. list item text
\a\a\a\a\a
   list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "ordered_list_item_with_new_list_item_empty_line_with_list_empty_and_exact_spaces",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""1. list item text
1. list item text
\a\a\a\a\a
   list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "ordered_list_item_with_new_list_item_empty_line_with_list_empty_and_exact_spaces_plus_one",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""1. list item text
1. list item text
\a\a\a\a\a\a
   list item text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD009: Trailing spaces [Expected: 5; Actual: 6] (no-trailing-spaces)
""",
        fix_expected_file_contents="""1. list item text
1. list item text
\a\a\a\a\a
   list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "ordered_list_item_with_nested_list_item_empty_line_with_list_empty_and_exact_spaces",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""1. list item text
   1. list item text
\a\a\a\a\a\a\a\a
      list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "ordered_list_item_with_nested_list_item_empty_line_with_list_empty_and_exact_spaces_plus_one",
        set_args=[
            "plugins.md009.list_item_empty_lines=$!True",
        ],
        use_strict_config=True,
        source_file_contents="""1. list item text
   1. list item text
\a\a\a\a\a\a\a\a\a
      list item text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD009: Trailing spaces [Expected: 8; Actual: 9] (no-trailing-spaces)
""",
        fix_expected_file_contents="""1. list item text
   1. list item text
\a\a\a\a\a\a\a\a
      list item text
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_paragraph_increasing_extra",
        source_file_name=f"{source_path}bad_paragraph_increasing_extra.md",
        source_file_contents="""this is some text\a
each line has some\a\a
extra spaces at the\a\a\a
end of the line.\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:18: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:3:20: MD009: Trailing spaces [Expected: 0 or 2; Actual: 3] (no-trailing-spaces)""",
        fix_expected_file_contents="""this is some text
each line has some\a\a
extra spaces at the\a\a
end of the line.\a\a
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_paragraph_increasing_extra_with_config_br_spaces_3",
        source_file_name=f"{source_path}bad_paragraph_increasing_extra.md",
        use_strict_config=True,
        set_args=["plugins.md009.br_spaces=$#3"],
        source_file_contents="""this is some text\a
each line has some\a\a
extra spaces at the\a\a\a
end of the line.\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:18: MD009: Trailing spaces [Expected: 0 or 3; Actual: 1] (no-trailing-spaces)
{temp_source_path}:2:19: MD009: Trailing spaces [Expected: 0 or 3; Actual: 2] (no-trailing-spaces)
{temp_source_path}:4:17: MD009: Trailing spaces [Expected: 0 or 3; Actual: 2] (no-trailing-spaces)
""",
        fix_expected_file_contents="""this is some text
each line has some
extra spaces at the\a\a\a
end of the line.
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_paragraph_increasing_extra_with_config_br_spaces_0",
        source_file_name=f"{source_path}bad_paragraph_increasing_extra.md",
        use_strict_config=True,
        set_args=["plugins.md009.br_spaces=$#0"],
        source_file_contents="""this is some text\a
each line has some\a\a
extra spaces at the\a\a\a
end of the line.\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:18: MD009: Trailing spaces [Expected: 0; Actual: 1] (no-trailing-spaces)
{temp_source_path}:2:19: MD009: Trailing spaces [Expected: 0; Actual: 2] (no-trailing-spaces)
{temp_source_path}:3:20: MD009: Trailing spaces [Expected: 0; Actual: 3] (no-trailing-spaces)
{temp_source_path}:4:17: MD009: Trailing spaces [Expected: 0; Actual: 2] (no-trailing-spaces)
""",
        fix_expected_file_contents="""this is some text
each line has some
extra spaces at the
end of the line.
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_paragraph_increasing_extra_with_config_strict",
        source_file_name=f"{source_path}bad_paragraph_increasing_extra.md",
        use_strict_config=True,
        set_args=["plugins.md009.strict=$!True"],
        source_file_contents="""this is some text\a
each line has some\a\a
extra spaces at the\a\a\a
end of the line.\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:18: MD009: Trailing spaces [Expected: 0; Actual: 1] (no-trailing-spaces)
{temp_source_path}:2:19: MD009: Trailing spaces [Expected: 0; Actual: 2] (no-trailing-spaces)
{temp_source_path}:3:20: MD009: Trailing spaces [Expected: 0; Actual: 3] (no-trailing-spaces)
{temp_source_path}:4:17: MD009: Trailing spaces [Expected: 0; Actual: 2] (no-trailing-spaces)
""",
        fix_expected_file_contents="""this is some text
each line has some
extra spaces at the
end of the line.
""",
    ),
    pluginRuleTest(
        "bad_atx_heading_with_extra",
        source_file_name=f"{source_path}bad_atx_heading_with_extra.md",
        source_file_contents="""# A Heading with trailing space\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:32: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)",
        fix_expected_file_contents="""# A Heading with trailing space
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_setext_heading_with_extra",
        source_file_name=f"{source_path}bad_setext_heading_with_extra.md",
        source_file_contents="""A Heading with trailing space\a
on more than one line\a
---------------------\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:30: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:2:22: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:3:22: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
""",
        fix_expected_file_contents="""A Heading with trailing space
on more than one line
---------------------
""",
    ),
    pluginRuleTest(
        "bad_theamtic_break_with_extra",
        source_file_name=f"{source_path}bad_theamtic_break_with_extra.md",
        source_file_contents="""----------\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:11: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)",
        fix_expected_file_contents="""----------
""",
    ),
    pluginRuleTest(
        "bad_html_block_with_extra",
        source_file_name=f"{source_path}bad_html_block_with_extra.md",
        disable_rules=__plugin_disable_md033,
        source_file_contents="""<!--
this\a
is\a
a\a
HTML\a
block\a
-->

<abc>\a\a
</abc>\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:3:3: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:4:2: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:5:5: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:6:6: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
""",
        fix_expected_file_contents="""<!--
this
is
a
HTML
block
-->

<abc>\a\a
</abc>\a\a
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_link_reference_definition_with_extra",
        source_file_name=f"{source_path}bad_link_reference_definition_with_extra.md",
        source_file_contents="""[abc](\a
    /url\a
    "title"\a
    )
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:7: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:2:9: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:3:12: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
""",
        fix_expected_file_contents="""[abc](
    /url
    "title"
    )
""",
    ),
    pluginRuleTest(
        "bad_blank_lines_with_extra",
        source_file_name=f"{source_path}bad_blank_lines_with_extra.md",
        disable_rules=__plugin_disable_md012,
        source_file_contents="""\a
\a\a
\a\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:3:1: MD009: Trailing spaces [Expected: 0 or 2; Actual: 3] (no-trailing-spaces)
""",
        fix_expected_file_contents="""
\a\a
\a\a
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "mix_md009_md023",
        source_file_contents="""  ## Heading 2\a\a\a

Some more text
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
{temp_source_path}:1:15: MD009: Trailing spaces [Expected: 0 or 2; Actual: 3] (no-trailing-spaces)
""",
        fix_expected_file_contents="""## Heading 2

Some more text
""",
    ),
    pluginRuleTest(
        "mix_md009_md027",
        disable_rules=__plugin_disable_md023,
        source_file_contents=""">  # Header 1\a
>
>  ## Header 2\a\a\a
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:1:14: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{temp_source_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{temp_source_path}:3:15: MD009: Trailing spaces [Expected: 0 or 2; Actual: 3] (no-trailing-spaces)
""",
        fix_expected_file_contents="""> # Header 1
>
> ## Header 2
""".replace(
            "\a", " "
        ),
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md009_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md009")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md009_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md009_config(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}good_paragraph_no_extra.md")


def test_md009_query_config():
    config_test = pluginQueryConfigTest(
        "md009",
        """
  ITEM               DESCRIPTION

  Id                 md009
  Name(s)            no-trailing-spaces
  Short Description  Trailing spaces
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md009.md


  CONFIGURATION ITEM     TYPE     VALUE

  br_spaces              integer  2
  strict                 boolean  False
  list_item_empty_lines  boolean  False
""",
    )
    execute_query_configuration_test(config_test)
