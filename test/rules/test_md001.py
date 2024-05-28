"""
Module to provide tests related to the MD001 rule.
"""

import os
from test.rules.utils import (
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

source_path = os.path.join("test", "resources", "rules", "md001") + os.sep

extension_enable_front_matter = "extensions.front-matter.enabled=$!True"
plug_set_front_matter_title_to_subject = "plugins.md001.front_matter_title=Subject"

extension_set_invalid_enable_front_matter_as_string = (
    "extensions.front-matter.enabled=True"
)
plugin_set_invalid_front_matter_title = "plugins.md001.front_matter_title=$#1"

__plugin_disable_md003 = "md003"

configTests = [
    pluginConfigErrorTest(
        "enable_front_matter_with_string",
        use_strict_config=True,
        set_args=[extension_set_invalid_enable_front_matter_as_string],
        expected_error="""Configuration error ValueError encountered while initializing extensions:
The value for property 'extensions.front-matter.enabled' must be of type 'bool'.""",
    ),
    pluginConfigErrorTest(
        "plugin_set_invalid_front_matter_title",
        use_strict_config=True,
        set_args=[extension_enable_front_matter, plugin_set_invalid_front_matter_title],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md001.front_matter_title' must be of type 'str'.""",
    ),
]


scanTests = [
    pluginRuleTest(
        "empty_configuration_front_matter_title",
        source_file_name=f"{source_path}front_matter_with_title.md",
        set_args=[extension_enable_front_matter, "plugins.md001.front_matter_title="],
    ),
    pluginRuleTest(
        "good_proper_atx_heading_incrementing",
        source_file_name=f"{source_path}proper_atx_heading_incrementing.md",
    ),
    pluginRuleTest(
        "good_proper_setext_heading_incrementing",
        source_file_name=f"{source_path}proper_setext_heading_incrementing.md",
        disable_rules=__plugin_disable_md003,
    ),
    pluginRuleTest(
        "bad_improper_atx_heading_incrementing",
        source_file_name=f"{source_path}improper_atx_heading_incrementing.md",
        source_file_contents="""# Heading 1

### Heading 3

We skipped out a 2nd level heading in this document
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:3:1: MD001: Heading levels should only increment by one level at a time. [Expected: h2; Actual: h3] (heading-increment,header-increment)\n",
        fix_expected_file_contents="""# Heading 1

## Heading 3

We skipped out a 2nd level heading in this document
""",
    ),
    pluginRuleTest(
        "bad_improper_setext_heading_incrementing",
        source_file_name=f"{source_path}improper_setext_heading_incrementing.md",
        disable_rules=__plugin_disable_md003,
        source_file_contents="""Heading 2
---------

#### Heading 4

We skipped out a heading level in this document
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:4:1: MD001: Heading levels should only increment by one level at a time. [Expected: h3; Actual: h4] (heading-increment,header-increment)\n",
        fix_expected_file_contents="""Heading 2
---------

### Heading 4

We skipped out a heading level in this document
""",
    ),
    pluginRuleTest(
        "front_matter_with_no_title",
        source_file_name=f"{source_path}front_matter_with_no_title.md",
        set_args=[extension_enable_front_matter],
    ),
    pluginRuleTest(
        "front_matter_with_title",
        source_file_name=f"{source_path}front_matter_with_title.md",
        set_args=[extension_enable_front_matter],
        source_file_contents="""---
title: field
---

### Heading 3

We skipped out a 2nd level heading in this document, which should only
kick in if there is a title field in the front matter.
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:5:1: MD001: Heading levels should only increment by one level at a time. [Expected: h2; Actual: h3] (heading-increment,header-increment)\n",
        fix_expected_file_contents="""---
title: field
---

## Heading 3

We skipped out a 2nd level heading in this document, which should only
kick in if there is a title field in the front matter.
""",
    ),
    pluginRuleTest(
        "front_matter_with_alternate_title",
        source_file_name=f"{source_path}front_matter_with_alternate_title.md",
        set_args=[
            extension_enable_front_matter,
            plug_set_front_matter_title_to_subject,
        ],
        source_file_contents="""---
Subject: field
---

### Heading 3

We skipped out a 2nd level heading in this document, which should only
kick in if there is a title field in the front matter.
""",
        scan_expected_return_code=1,
        scan_expected_output="{temp_source_path}:5:1: MD001: Heading levels should only increment by one level at a time. [Expected: h2; Actual: h3] (heading-increment,header-increment)\n",
        fix_expected_file_contents="""---
Subject: field
---

## Heading 3

We skipped out a 2nd level heading in this document, which should only
kick in if there is a title field in the front matter.
""",
    ),
]
fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents:
        fixTests.append(i)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md001_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md001")


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md001_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md001_config(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}front_matter_with_title.md")


def test_md001_query_config():
    config_test = pluginQueryConfigTest(
        "md001",
        """
  ITEM               DESCRIPTION

  Id                 md001
  Name(s)            heading-increment,header-increment
  Short Description  Heading levels should only increment by one level at a ti
                     me.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md001.md


  CONFIGURATION ITEM  TYPE    VALUE

  front_matter_title  string  "title"

""",
    )
    execute_query_configuration_test(config_test)
