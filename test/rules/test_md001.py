"""
Module to provide tests related to the MD001 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import (
    execute_fix_test,
    execute_scan_test,
    id_test_plug_rule_fn,
    pluginRuleTest,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md001") + os.sep

extension_enable_front_matter = "extensions.front-matter.enabled=$!True"

plugin_disable_md003 = "md003"


@pytest.mark.rules
def test_md001_all_samples():
    """
    Test to make sure we get the expected behavior after scanning all the files in the
    test/resources/rules/md001 directory.  Note that with three front-matter files in
    this directory and no config to enable that extension, Md022 will report bad
    heading formats.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        plugin_disable_md003,
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}front_matter_with_alternate_title.md:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{source_path}front_matter_with_no_title.md:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{source_path}front_matter_with_title.md:2:1: "
        + "MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{source_path}improper_atx_heading_incrementing.md:3:1: "
        + "MD001: Heading levels should only increment by one level at a time. "
        + "[Expected: h2; Actual: h3] (heading-increment,header-increment)\n"
        + f"{source_path}improper_setext_heading_incrementing.md:4:1: "
        + "MD001: Heading levels should only increment by one level at a time. "
        + "[Expected: h3; Actual: h4] (heading-increment,header-increment)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md001_bad_configuration_enabled():
    """
    Test to verify that enabling front matter with text "True" fails.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--strict-config",
        "--set",
        "extensions.front-matter.enabled=True",
        "scan",
        f"{source_path}front_matter_with_title.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """Configuration error ValueError encountered while initializing extensions:
The value for property 'extensions.front-matter.enabled' must be of type 'bool'."""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md001_bad_configuration_front_matter_title():
    """
    Test to verify that enabling front matter title with number "1" fails.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--strict-config",
        "--set",
        extension_enable_front_matter,
        "--set",
        "plugins.md001.front_matter_title=$#1",
        "scan",
        f"{source_path}proper_atx_heading_incrementing.md",
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md001.front_matter_title' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


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
        disable_rules=plugin_disable_md003,
    ),
    pluginRuleTest(
        "bad_improper_atx_heading_incrementing",
        source_file_name=f"{source_path}improper_atx_heading_incrementing.md",
        source_file_contents="""# Heading 1

### Heading 3

We skipped out a 2nd level heading in this document
""",
        scan_expected_return_code=1,
        scan_expected_output=(
            f"{source_path}improper_atx_heading_incrementing.md:3:1: "
            + "MD001: Heading levels should only increment by one level at a time. "
            + "[Expected: h2; Actual: h3] (heading-increment,header-increment)\n"
        ),
        fix_expected_return_code=1,
        fix_expected_file_contents="""# Heading 1

## Heading 3

We skipped out a 2nd level heading in this document
""",
    ),
    pluginRuleTest(
        "bad_improper_setext_heading_incrementing",
        source_file_name=f"{source_path}improper_setext_heading_incrementing.md",
        disable_rules=plugin_disable_md003,
        source_file_contents="""Heading 2
---------

#### Heading 4

We skipped out a heading level in this document
""",
        scan_expected_return_code=1,
        scan_expected_output=(
            f"{source_path}improper_setext_heading_incrementing.md:4:1: "
            + "MD001: Heading levels should only increment by one level at a time. "
            + "[Expected: h3; Actual: h4] (heading-increment,header-increment)\n"
        ),
        fix_expected_return_code=1,
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
        scan_expected_output=f"{source_path}front_matter_with_title.md:5:1: MD001: Heading levels should only increment by one level at a time. [Expected: h2; Actual: h3] (heading-increment,header-increment)\n",
        fix_expected_return_code=1,
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
            "plugins.md001.front_matter_title=Subject",
        ],
        source_file_contents="""---
Subject: field
---

### Heading 3

We skipped out a 2nd level heading in this document, which should only
kick in if there is a title field in the front matter.
""",
        scan_expected_return_code=1,
        scan_expected_output=f"{source_path}front_matter_with_alternate_title.md:5:1: MD001: Heading levels should only increment by one level at a time. [Expected: h2; Actual: h3] (heading-increment,header-increment)\n",
        fix_expected_return_code=1,
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
    execute_scan_test(test)


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md001_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)
