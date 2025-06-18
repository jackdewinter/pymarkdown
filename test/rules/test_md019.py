"""
Module to provide tests related to the MD019 rule.
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

# pylint: disable=too-many-lines

source_path = os.path.join("test", "resources", "rules", "md019") + os.sep

__plugin_disable_md010 = "md010"
__plugin_disable_md013_md033 = "md013,md033"
__plugin_disable_md023 = "md023"
__plugin_disable_md026 = "md026"
__plugin_disable_md033 = "md033"
__plugin_disable_md037 = "md037"

scanTests = [
    pluginRuleTest(
        "good_single_spacing",
        source_file_name=f"{source_path}single_spacing.md",
        source_file_contents="""# Heading 1

## Heading 2
""",
    ),
    pluginRuleTest(
        "bad_multiple_spacing",
        source_file_name=f"{source_path}multiple_spacing.md",
        source_file_contents="""#  Heading 1

##  Heading 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:3:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)""",
        fix_expected_file_contents="""# Heading 1

## Heading 2
""",
    ),
    pluginRuleTest(
        "good_multiple_spacing_with_inline",
        source_file_contents="""# Heading *number*  1

## Heading *number*  2
""",
    ),
    pluginRuleTest(
        "bad_multiple_spacing_with_inline",
        source_file_name=f"{source_path}multiple_spacing_with_inline.md",
        source_file_contents="""#  Heading *number* 1

##  Heading *number* 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:3:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)""",
        fix_expected_file_contents="""# Heading *number* 1

## Heading *number* 2
""",
    ),
    pluginRuleTest(
        "bad_multiple_spacing_with_inline_only",
        source_file_contents="""#  *number  1*

##  *number  2*
""",
        disable_rules=__plugin_disable_md037,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:3:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)""",
        fix_expected_file_contents="""# *number  1*

## *number  2*
""",
    ),
    pluginRuleTest(
        "bad_multiple_spacing_with_indent",
        source_file_name=f"{source_path}multiple_spacing_with_indent.md",
        disable_rules=__plugin_disable_md023,
        source_file_contents=""" #  Heading 1

  ##  Heading 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:3:3: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)""",
        fix_expected_file_contents=""" # Heading 1

  ## Heading 2
""",
    ),
    pluginRuleTest(
        "bad_single_space_single_tab",
        source_file_name=f"{source_path}single_space_single_tab.md",
        disable_rules=__plugin_disable_md010,
        source_file_contents="""# \tHeading 1

## \tHeading 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:3:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)""",
        fix_expected_file_contents="""# Heading 1

## Heading 2
""",
    ),
    pluginRuleTest(
        "issue-977",
        disable_rules=__plugin_disable_md013_md033,
        source_file_contents="""## Run optimization

<pre>
bazel run //tools/pymarkdown -- --help
usage: pymarkdown.py [-h] [--commit COMMIT] [--steps STEPS]

                     [--overwrite OVERWRITE] [--root_path ROOT_PATH]

options:
""",
    ),
    pluginRuleTest(
        "good_proper_heading_followed_by_paragraph_indented_lines",
        source_file_contents="""# Heading 1

  Text
  more text
""",
    ),
    pluginRuleTest(
        "good_proper_heading_followed_by_fenced_indented_lines",
        source_file_contents="""# Heading 1

```text
  Text
  more text
```
""",
    ),
    pluginRuleTest(
        "bad_empty_heading_with_spaces_followed_by_fenced_indented_lines",
        source_file_contents="""#\a\a

```text
  Text
  more text
```
""".replace(
            "\a", " "
        ),
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)",
        fix_expected_file_contents="""#\a

```text
  Text
  more text
```
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "good_empty_heading_with_empty_text",
        source_file_contents="""#

empty
""",
    ),
    pluginRuleTest(
        "good_empty_heading_with_empty_text",
        source_file_contents="""#

empty
""",
    ),
    pluginRuleTest(
        "bad_extra_space_only_raw_html",
        source_file_contents="""##  <foo></foo><foo/>

just some text
""",
        disable_rules=__plugin_disable_md033,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
""",
        fix_expected_file_contents="""## <foo></foo><foo/>

just some text
""",
    ),
    pluginRuleTest(
        "good_extra_space_only_raw_html",
        disable_rules=__plugin_disable_md033,
        source_file_contents="""## <foo></foo><foo/>

just some text
""",
    ),
    pluginRuleTest(
        "bad_extra_space_only_emphasis",
        source_file_contents="""#  *Heading 1#*

##  *Heading 2#*
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:3:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)""",
        fix_expected_file_contents="""# *Heading 1#*

## *Heading 2#*
""",
    ),
    pluginRuleTest(
        "good_extra_space_only_emphasis",
        source_file_contents="""# *Heading 1#*

## *Heading 2#*
""",
    ),
    pluginRuleTest(
        "bad_extra_space_only_autolink",
        source_file_contents="""#  <https://google.com>

just some text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
""",
        fix_expected_file_contents="""# <https://google.com>

just some text
""",
    ),
    pluginRuleTest(
        "good_extra_space_only_autolink",
        source_file_contents="""# <https://google.com>

just some text
""",
    ),
    pluginRuleTest(
        "bad_extra_space_only_link",
        source_file_contents="""#  [google](https://google.com)

just some text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
""",
        fix_expected_file_contents="""# [google](https://google.com)

just some text
""",
    ),
    pluginRuleTest(
        "good_extra_space_only_link",
        source_file_contents="""# [google](https://google.com)

just some text
""",
    ),
    pluginRuleTest(
        "bad_extra_space_only_codespan",
        source_file_contents="""#  `codespan`

just some text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
""",
        fix_expected_file_contents="""# `codespan`

just some text
""",
    ),
    pluginRuleTest(
        "good_extra_space_only_codepsan",
        source_file_contents="""# `codespan`

just some text
""",
    ),
    pluginRuleTest(
        "bad_extra_space_only_reference",
        source_file_contents="""#  &amp;

just some text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
""",
        fix_expected_file_contents="""# &amp;

just some text
""",
    ),
    pluginRuleTest(
        "good_extra_space_only_reference",
        source_file_contents="""# &amp;

just some text
""",
    ),
    pluginRuleTest(
        "bad_extra_space_only_backslash",
        disable_rules=__plugin_disable_md026,
        source_file_contents="""#  \\!

just some text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
""",
        fix_expected_file_contents="""# \\!

just some text
""",
    ),
    pluginRuleTest(
        "good_extra_space_only_backslash",
        source_file_contents="""# \\!

just some text
""",
        disable_rules=__plugin_disable_md026,
    ),
    pluginRuleTest(
        "bad_extra_space_tab_backslash_reference",
        source_file_contents="""#\t\\! &#20;

just some text
""",
        disable_rules="md010",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
""",
    ),
    pluginRuleTest(
        "mix_md019_md010",
        source_file_contents="""#\tHeading 1

a line of text\twith\ttabs
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)
{temp_source_path}:3:15: MD010: Hard tabs [Column: 15] (no-hard-tabs)
{temp_source_path}:3:21: MD010: Hard tabs [Column: 21] (no-hard-tabs)
""",
        fix_expected_file_contents="""# Heading 1

a line of text  with    tabs
""",
    ),
    pluginRuleTest(
        "mix_md019_md023",
        source_file_contents="""  #  Heading 1
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:1:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)
""",
        fix_expected_file_contents="""# Heading 1
""",
    ),
    pluginRuleTest(
        "mix_md019_md047",
        source_file_contents="""#  Heading 1

a line of text""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{temp_source_path}:3:14: MD047: Each file should end with a single newline character. (single-trailing-newline)""",
        fix_expected_file_contents="""# Heading 1

a line of text
""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md019_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md019")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md019_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


def test_md019_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md019",
        """
  ITEM               DESCRIPTION

  Id                 md019
  Name(s)            no-multiple-space-atx
  Short Description  Multiple spaces are present after hash character on Atx H
                     eading.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md019.md
  """,
    )
    execute_query_configuration_test(config_test)
