"""
Module to provide tests related to the MD020 rule.
"""

import os
from test.rules.utils import (
    calculate_scan_tests,
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md020") + os.sep

# pylint: disable=too-many-lines


scanTests = [
    pluginRuleTest(
        "good_start_spacing",
        source_file_name=f"{source_path}good_start_spacing.md",
        source_file_contents="""# Heading 1 #

## Heading 2 ##
""",
    ),
    pluginRuleTest(
        "good_start_spacing_in_list",
        source_file_name=f"{source_path}good_start_spacing_in_list.md",
        source_file_contents="1. # Heading 1 #\n\n2. ## Heading 2 ##\n",
    ),
    pluginRuleTest(
        "good_start_spacing_in_block_quote",
        source_file_name=f"{source_path}good_start_spacing_in_block_quote.md",
        source_file_contents="> # Heading 1 #\n>\n> ## Heading 2 ##\n",
    ),
    pluginRuleTest(
        "bad_ignore_bad_atx_spacing",
        source_file_name=f"{source_path}ignore_bad_atx_spacing.md",
        source_file_contents="#Heading 1\n\n##Heading 2\n",
        disable_rules="md018",
    ),
    pluginRuleTest(
        "bad_missing_start_spacing",
        source_file_name=f"{source_path}missing_start_spacing.md",
        source_file_contents="#Heading 1 #\n\n##Heading 2 #\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:3:1: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_missing_start_spacing_in_list",
        source_file_name=f"{source_path}missing_start_spacing_in_list.md",
        source_file_contents="1. #Heading 1 #\n\n2. ##Heading 2 #\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:3:4: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_missing_start_spacing_in_block_quotes",
        source_file_name=f"{source_path}missing_start_spacing_in_block_quotes.md",
        source_file_contents="> #Heading 1 #\n> \n> ##Heading 2 #\n",
        disable_rules="md009,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:3:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_missing_end_spacingx",
        source_file_name=f"{source_path}missing_end_spacing.md",
        source_file_contents="# Heading 1#\n\n## Heading 2#\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:12: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:3:13: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_missing_end_spacing_in_list",
        source_file_name=f"{source_path}missing_end_spacing_in_list.md",
        source_file_contents="1. # Heading 1#\n\n1. ## Heading 2##\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:15: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:3:16: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_missing_end_spacing_in_block_quotes",
        source_file_name=f"{source_path}missing_end_spacing_in_block_quotes.md",
        source_file_contents="> # Heading 1#\n>\n> ## Heading 2#\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:14: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:3:15: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "good_almost_missing_end_spacing",
        source_file_name=f"{source_path}almost_missing_end_spacing.md",
        source_file_contents="# *Heading 1#*\n\n## *Heading 2#*\n",
    ),
    pluginRuleTest(
        "bad_missing_both_spacing",
        source_file_name=f"{source_path}missing_both_spacing.md",
        source_file_contents="#Heading 1#\n\n##Heading 2#\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:3:1: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_missing_both_spacing_in_list",
        source_file_name=f"{source_path}missing_both_spacing_in_list.md",
        source_file_contents="1. #Heading 1#\n\n2. ##Heading 2#\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:3:4: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_missing_both_spacing_in_block_quotes",
        source_file_name=f"{source_path}missing_both_spacing_in_block_quotes.md",
        source_file_contents="> #Heading 1#\n> \n> ##Heading 2#\n",
        disable_rules="md009,md027",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:3:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "good_with_setext_headings",
        source_file_name=f"{source_path}with_setext_headings.md",
        source_file_contents="#Heading 1#\n---------\n\n##Heading 2##\n=========\n",
    ),
    pluginRuleTest(
        "good_with_code_blocks",
        source_file_name=f"{source_path}with_code_blocks.md",
        source_file_contents="```text\n#Heading 1#\n```\n\n    ##Heading 2##\n",
        disable_rules="md046",
    ),
    pluginRuleTest(
        "good_with_html_blocks",
        source_file_name=f"{source_path}with_html_blocks.md",
        source_file_contents="<!--\n#Heading 1#\n-->\n\n<script>\n    ##Heading 2##\n</script>\n",
        disable_rules="md033,PML100",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph",
        source_file_name=f"{source_path}multiple_within_paragraph.md",
        source_file_contents="#Heading 1 with no blank lines#\n##Heading 2 with no blank lines##\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:2:1: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph_separated_codespan",
        source_file_name=f"{source_path}multiple_within_paragraph_separated_codespan.md",
        source_file_contents="#Heading 1 with no blank lines#\n`code span`\n##Heading 2 with no blank lines##\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:3:1: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph_separated_codespan_multi",
        source_file_name=f"{source_path}multiple_within_paragraph_separated_codespan_multi.md",
        source_file_contents="#Heading 1 with no blank lines#\n`code\nspan`\n##Heading 2 with no blank lines##\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:4:1: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph_separated_inline_codespan_multi",
        source_file_name=f"{source_path}multiple_within_paragraph_separated_inline_codespan_multi.md",
        source_file_contents="#Heading 1 with no blank lines#`code\n span`##Heading 2 with no blank lines##\n  `code span`\n  ###Heading 3 with no blank lines###\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph_separated_inline_rawhtml_multi",
        source_file_name=f"{source_path}multiple_within_paragraph_separated_inline_rawhtml_multi.md",
        source_file_contents="#Heading 1 with no blank lines#<raw\n html=0>##Heading 2 with no blank lines##\n  <raw html=0>\n  ###Heading 3 with no blank lines###\n",
        disable_rules="md033",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph_separated_inline_image_multi",
        source_file_name=f"{source_path}multiple_within_paragraph_separated_inline_image_multi.md",
        source_file_contents="#Heading 1 with no blank lines#![my\nimage](\n    https://google.com\n'tit\nle'\n)##Heading 2 with no blank lines##\n ![my image](https://google.com 'title')\n  ###Heading 3 with no blank lines##\n",
        disable_rules="md033",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph_separated_full_image_multi",
        source_file_name=f"{source_path}multiple_within_paragraph_separated_full_image_multi.md",
        source_file_contents='#Heading 1 with no blank lines#![my\nimage][foo\nbar]##Heading 2 with no blank lines##\n #![my image][foo bar]\n  ###Heading 3 with no blank lines##\n\n[FOO\nBAR]: train.jpg "train & tracks"\n[FOO BAR]: train.jpg "train & tracks"\n',
        disable_rules="md033",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph_separated_shortcut_image_multi",
        source_file_name=f"{source_path}multiple_within_paragraph_separated_shortcut_image_multi.md",
        source_file_contents='#Heading 1 with no blank lines#![foo\nbar]##Heading 2 with no blank lines##\n #![foo bar]\n  ###Heading 3 with no blank lines###\n\n[FOO\nBAR]: train.jpg "train & tracks"\n[FOO BAR]: train.jpg "train & tracks"\n',
        disable_rules="md033",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph_separated_collapsed_image_multi",
        source_file_name=f"{source_path}multiple_within_paragraph_separated_collapsed_image_multi.md",
        source_file_contents='#Heading 1 with no blank lines#![foo\nbar][]##Heading 2 with no blank lines##\n #![foo bar][]\n  ###Heading 3 with no blank lines###\n\n[FOO\nBAR]: train.jpg "train & tracks"\n[FOO BAR]: train.jpg "train & tracks"\n',
        disable_rules="md033",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph_separated_inline_link_multi",
        source_file_name=f"{source_path}multiple_within_paragraph_separated_inline_link_multi.md",
        source_file_contents="#Heading 1 with no blank lines##[my\nimage](\n    https://google.com\n'tit\nle'\n)##Heading 2 with no blank lines##\n [my image](https://google.com 'title')\n  ###Heading 3 with no blank lines##\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph_separated_full_link_multi",
        source_file_name=f"{source_path}multiple_within_paragraph_separated_full_link_multi.md",
        source_file_contents='#Heading 1 with no blank lines#[my\nimage][foo\nbar]##Heading 2 with no blank lines##\n [my image][foo bar]\n  ###Heading 3 with no blank lines##\n\n[FOO\nBAR]: train.jpg "train & tracks"\n[FOO BAR]: train.jpg "train & tracks"\n',
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph_separated_separated_shortcut_link_multi",
        source_file_name=f"{source_path}multiple_within_paragraph_separated_shortcut_link_multi.md",
        source_file_contents='#Heading 1 with no blank lines#[foo\nbar]##Heading 2 with no blank lines##\n [foo bar]\n  ###Heading 3 with no blank lines###\n\n[FOO\nBAR]: train.jpg "train & tracks"\n[FOO BAR]: train.jpg "train & tracks"\n',
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph_separated_collapsed_link_multi",
        source_file_name=f"{source_path}multiple_within_paragraph_separated_collapsed_link_multi.md",
        source_file_contents='#Heading 1 with no blank lines#[foo\nbar][]##Heading 2 with no blank lines##\n [foo bar][]\n  ###Heading 3 with no blank lines###\n\n[FOO\nBAR]: train.jpg "train & tracks"\n[FOO BAR]: train.jpg "train & tracks"\n',
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_multiple_within_paragraph_separated_inline_hardbreak_multi",
        source_file_name=f"{source_path}multiple_within_paragraph_separated_inline_hardbreak_multi.md",
        source_file_contents="#Heading 1 with no blank lines#\\\n ##Heading 2 with no blank lines##  \n  ###Heading 3 with no blank lines###\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_paragraphs_with_starting_whitespace",
        source_file_name=f"{source_path}paragraphs_with_starting_whitespace.md",
        source_file_contents="#Heading 1#\n\n ##Heading 2##\n\n  ###Heading 3###\n\n   ####Heading 4####\n\n    #####Heading 5#####\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:3:2: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:5:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:7:4: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_single_paragraph_with_starting_whitespace",
        source_file_name=f"{source_path}single_paragraph_with_starting_whitespace.md",
        source_file_contents="#Heading 1#\n ##Heading 2##\n  ###Heading 3###\n   ####Heading 4####\n    #####Heading 5#####\n",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:2:2: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:3:3: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{temp_source_path}:4:4: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
""",
    ),
    pluginRuleTest(
        "bad_single_paragraph_with_whitespace_at_start",
        source_file_name=f"{source_path}single_paragraph_with_whitespace_at_start.md",
        source_file_contents="#\tHeading 1 #\n ##\tHeading 2 ##\n",
        disable_rules="md010,md021,md022,md023",
    ),
    pluginRuleTest(
        "bad_single_paragraph_with_whitespace_at_end",
        source_file_name=f"{source_path}single_paragraph_with_whitespace_at_end.md",
        source_file_contents="# Heading 1\t#\n ## Heading 2\t##\n",
        disable_rules="md010,md021,md022,md023",
    ),
    pluginRuleTest(
        "issue-1302-primary",
        source_file_contents="""# MD020

<!-- Escaped hash at end of line -->

## Intro to C\\#

Emits MD020 warning.

<!-- Escaped hash followed by punctuation -->

### Intro to C\\#, continued

Emits nothing.

<!--  Escaped hash followed by a space -->

## Intro to C\\# programming

Emits nothing.
""",
    ),
    pluginRuleTest(
        "issue-1302-secondary",
        source_file_contents="""## Intro to C&#35;

Emits MD020 warning.
""",
    ),
    pluginRuleTest(
        "issue-1302-tertiary-1",
        source_file_contents="""\\# Intro to C++

Emits MD020 warning.
""",
    ),
    pluginRuleTest(
        "issue-1302-tertiary-2",
        source_file_contents="""&#35; Intro to C++

Emits MD020 warning.
""",
    ),
]


@pytest.mark.parametrize(
    "test", calculate_scan_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md020_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md020.
    """
    execute_scan_test(test, "md020")


def test_md020_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md020",
        """
  ITEM               DESCRIPTION

  Id                 md020
  Name(s)            no-missing-space-closed-atx
  Short Description  No space present inside of the hashes on a possible Atx C
                     losed Heading.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md020.md
  """,
    )
    execute_query_configuration_test(config_test)
