"""
Module to provide tests related to the MD026 rule.
"""

import os
from test.rules.utils import (
    execute_configuration_test,
    execute_query_configuration_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginConfigErrorTest,
    pluginQueryConfigTest,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md041") + os.sep
extension_enable_front_matter = "extensions.front-matter.enabled=$!True"

configTests = [
    pluginConfigErrorTest(
        "bad_configuration_level",
        use_strict_config=True,
        set_args=["plugins.md041.level=1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md041.level' must be of type 'int'.""",
    ),
    pluginConfigErrorTest(
        "bad_configuration_level_bad",
        use_strict_config=True,
        set_args=["plugins.md041.level=$#0"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md041.level' is not valid: Allowable values are between 1 and 6.""",
    ),
    pluginConfigErrorTest(
        "bad_configuration_front_matter_title",
        use_strict_config=True,
        set_args=["plugins.md041.front_matter_title=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md041.front_matter_title' must be of type 'str'.""",
    ),
    pluginConfigErrorTest(
        "bad_configuration_front_matter_title_invalid",
        use_strict_config=True,
        set_args=["plugins.md041.front_matter_title=a:b"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md041.front_matter_title' is not valid: Colons (:) are not allowed in the value.""",
    ),
    pluginConfigErrorTest(
        "bad_configuration_invisible_tags_bad_name",
        use_strict_config=True,
        set_args=["plugins.md041.invisible_tags=bad_tag"],
        expected_error="""BadPluginError encountered while configuring plugins:
Invalid tag name 'bad_tag' found between commas.""",
    ),
    pluginConfigErrorTest(
        "bad_configuration_invisible_tags_empty",
        use_strict_config=True,
        set_args=["plugins.md041.invisible_tags=bad,,tag"],
        expected_error="""BadPluginError encountered while configuring plugins:
Empty tag name found in between commas.""",
    ),
]


scanTests = [
    pluginRuleTest(
        "good_single_top_level_atx",
        source_file_name=f"{source_path}good_heading_top_level_atx.md",
    ),
    pluginRuleTest(
        "good_blank_lines_top_level_atx_heading",
        source_file_name=f"{source_path}good_blank_lines_top_level_atx_heading.md",
    ),
    pluginRuleTest(
        "bad_single_top_level_atx",
        source_file_name=f"{source_path}bad_heading_top_level_atx.md",
        source_file_contents="""## Top Level Heading

This is not a good document.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
""",
    ),
    pluginRuleTest(
        "bad_single_top_level_atx_with_config",
        source_file_name=f"{source_path}bad_heading_top_level_atx.md",
        source_file_contents="""## Top Level Heading

This is not a good document.
""",
        set_args=["plugins.md041.level=$#2"],
    ),
    pluginRuleTest(
        "good_heading_top_level_setext",
        source_file_name=f"{source_path}good_heading_top_level_setext.md",
        source_file_contents="""Top Level Heading
====

This is a good document.
""",
    ),
    pluginRuleTest(
        "bad_single_top_level_setext",
        source_file_name=f"{source_path}bad_heading_top_level_setext.md",
        source_file_contents="""Top Level Heading
----

This is not a good document.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
""",
    ),
    pluginRuleTest(
        "bad_front_matter_top_level_and_atx_top_level",
        source_file_name=f"{source_path}good_front_matter_top_level.md",
        source_file_contents="""---
title: Top Level Heading
---

# This is a good document
""",
        set_args=[extension_enable_front_matter],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)
""",
    ),
    pluginRuleTest(
        "good_bad_front_matter_top_level",
        source_file_name=f"{source_path}good_bad_front_matter_top_level.md",
        source_file_contents="""---
subject: Top Level Heading
---

# This is a good document
""",
        set_args=[extension_enable_front_matter],
    ),
    pluginRuleTest(
        "good_bad_front_matter_top_level_repeat",
        source_file_name=f"{source_path}good_bad_front_matter_top_level.md",
        source_file_contents="""---
subject: Top Level Heading
---

# This is a good document
""",
        set_args=[
            extension_enable_front_matter,
            "plugins.md041.front_matter_title=subject",
        ],
    ),
    pluginRuleTest(
        "bad_fenced_code_block",
        source_file_name=f"{source_path}bad_fenced_code_block.md",
        source_file_contents="""```python
def bad_func():
    pass
```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
""",
    ),
    pluginRuleTest(
        "bad_thematic_break",
        source_file_name=f"{source_path}bad_thematic_break.md",
        source_file_contents="""---
reverse setext?
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
""",
    ),
    pluginRuleTest(
        "bad_indented_code_block",
        source_file_name=f"{source_path}bad_indented_code_block.md",
        source_file_contents="""    def bad_func():
        pass
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
""",
    ),
    pluginRuleTest(
        "bad_html_block",
        source_file_name=f"{source_path}bad_html_block.md",
        source_file_contents="""<html></html>
""",
        disable_rules="MD033",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
""",
    ),
    pluginRuleTest(
        "bad_html_block_heading",
        source_file_name=f"{source_path}bad_html_block_heading.md",
        source_file_contents="""<h2>some heading</h2>
""",
        disable_rules="MD033",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
""",
    ),
    pluginRuleTest(
        "good_html_block_heading",
        source_file_name=f"{source_path}good_html_block_heading.md",
        source_file_contents="""<h1><img src="fred"></h1>
""",
    ),
    pluginRuleTest(
        "issue-1505",
        source_file_contents="""
""",
        disable_rules="MD012,MD033",
        scan_expected_return_code=0,
    ),
    pluginRuleTest(
        "issue-1400-scenario-1-no-blank-line",
        source_file_contents="""<link rel="stylesheet" href="/styles.css">
# What seems like a level-1 heading is actually part of the link html block.
""",
        disable_rules="MD033",
        scan_expected_return_code=0,
    ),
    pluginRuleTest(
        "issue-1400-scenario-1-with-blank-line",
        source_file_contents="""<link rel="stylesheet" href="/styles.css">

# This file starts with a level 1 heading
""",
        disable_rules="MD033",
    ),
    pluginRuleTest(
        "issue-1400-scenario-2-comment-with-blank-line-after",
        source_file_contents="""<!--
SPDX-FileCopyrightText: REUSE Coder, Inc.

SPDX-License-Identifier: MIT
-->

# This file starts with a level 1 heading
""",
        set_args=[extension_enable_front_matter],
    ),
    pluginRuleTest(
        "issue-1400-scenario-2-comment-with-no-blank-line-after",
        source_file_contents="""<!--
SPDX-FileCopyrightText: REUSE Coder, Inc.

SPDX-License-Identifier: MIT
-->
# This file starts with a level 1 heading
""",
        disable_rules="MD022",
    ),
    pluginRuleTest(
        "issue-1400-scenario-3-comment-with-blank-line-after",
        source_file_contents="""<!-- This file doesn't start with H1,
but could be valid depending on the value of
the `plugins.md041.level` configuration -->

## This file starts with a level 2 heading
""",
        disable_rules="MD022",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
""",
    ),
    pluginRuleTest(
        "issue-1400-scenario-3-comment-with-no-blank-line-after",
        source_file_contents="""<!-- This file doesn't start with H1,
but could be valid depending on the value of
the `plugins.md041.level` configuration -->
## This file starts with a level 2 heading
""",
        disable_rules="MD022",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)
""",
    ),
    pluginRuleTest(
        "issue-1400-scenario-4-custom",
        source_file_contents="""<bob>

# This file starts with a level 2 heading
""",
        set_args=["plugins.md041.invisible_tags=bob"],
        disable_rules="MD033",
    ),
    pluginRuleTest(  # Ensure that first and last parts of comments are the same.
        "issue-1447-a",
        source_file_contents="""<!--- pyml disable-next-line first-line-heading --->
-8<- "README.md"
""",
    ),
    pluginRuleTest(  # Ensure that first and last parts of comments are the same.
        "issue-1447-b",
        source_file_contents="""<!--- pyml disable-num-lines 200 first-line-heading --->
-8<- "README.md"
""",
    ),
    pluginRuleTest(  # Ensure that first and last parts of comments are the same.
        "issue-1447-c",
        source_file_contents="""<!--- pyml disable first-line-heading --->
-8<- "README.md"
""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md041_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md041", suppress_first_line_heading_rule=False)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md041_config(test: pluginConfigErrorTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(
        test,
        f"{source_path}good_heading_top_level_atx.md",
        suppress_first_line_heading_rule=False,
    )


def test_md041_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md041",
        """
  ITEM               DESCRIPTION

  Id                 md041
  Name(s)            first-line-heading,first-line-h1
  Short Description  First line in file should be a top level heading
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md041.md


  CONFIGURATION ITEM  TYPE     VALUE

  level               integer  1
  front_matter_title  string   "title"
  invisible_tags      string   "<!--,<link"

""",
    )
    execute_query_configuration_test(config_test)
