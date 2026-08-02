"""
Module to provide tests related to the MD053 rule.
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

source_path = os.path.join("test", "resources", "rules", "md053") + os.sep

configTests = [
    pluginConfigErrorTest(
        "invalid_prohibited_phrases_type",
        use_strict_config=True,
        set_args=["plugins.md053.ignored-definitions=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md053.ignored-definitions' must be of type 'str'.""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_full_link_and_matching_lrd",
        source_file_contents="""[This is a link][test label]

[test label]: /url
""",
    ),
    pluginRuleTest(
        "bad_full_link_and_no_matching_lrd",
        source_file_contents="""[This is a link][another test label]

[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "bad_full_link_and_matching_lrd_with_duplicate",
        source_file_contents="""[This is a link][test label]

[test label]: /url
[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "bad_full_link_and_no_matching_lrd_with_duplicate",
        source_file_contents="""[This is a link][another test label]

[test label]: /url
[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
{temp_source_path}:4:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "good_collapsed_link_and_matching_lrd",
        source_file_contents="""[test label][]

[test label]: /url
""",
    ),
    pluginRuleTest(
        "bad_collapsed_link_and_no_matching_lrd",
        source_file_contents="""[another test label][]

[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "bad_collapsed_link_and_matching_lrd_with_duplicate",
        source_file_contents="""[test label][]

[test label]: /url
[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "bad_collapsed_link_and_no_matching_lrd_with_duplicate",
        source_file_contents="""[another test label][]

[test label]: /url
[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
{temp_source_path}:4:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "good_shortcut_link_and_matching_lrd",
        source_file_contents="""[test label]

[test label]: /url
""",
    ),
    pluginRuleTest(
        "bad_shortcut_link_and_no_matching_lrd",
        source_file_contents="""[another test label]

[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "bad_shortcut_link_and_matching_lrd_with_duplicate",
        source_file_contents="""[test label]

[test label]: /url
[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "bad_shortcut_link_and_no_matching_lrd_with_duplicate",
        source_file_contents="""[another test label]

[test label]: /url
[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
{temp_source_path}:4:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "good_full_image_and_matching_lrd",
        source_file_contents="""![This is a link][test label]

[test label]: /url
""",
    ),
    pluginRuleTest(
        "bad_full_image_and_no_matching_lrd",
        source_file_contents="""![This is a link][another test label]

[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "bad_full_image_and_matching_lrd_with_duplicate",
        source_file_contents="""![This is a link][test label]

[test label]: /url
[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "bad_full_image_and_no_matching_lrd_with_duplicate",
        source_file_contents="""![This is a link][another test label]

[test label]: /url
[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
{temp_source_path}:4:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "good_collapsed_image_and_matching_lrd",
        source_file_contents="""![test label][]

[test label]: /url
""",
    ),
    pluginRuleTest(
        "bad_collapsed_image_and_no_matching_lrd",
        source_file_contents="""![another test label][]

[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "bad_collapsed_image_and_matching_lrd_with_duplicate",
        source_file_contents="""![test label][]

[test label]: /url
[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "bad_collapsed_image_and_no_matching_lrd_with_duplicate",
        source_file_contents="""![another test label][]

[test label]: /url
[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
{temp_source_path}:4:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "good_shortcut_image_and_matching_lrd",
        source_file_contents="""![test label]

[test label]: /url
""",
    ),
    pluginRuleTest(
        "bad_shortcut_image_and_no_matching_lrd",
        source_file_contents="""![another test label]

[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "bad_shortcut_image_and_matching_lrd_with_duplicate",
        source_file_contents="""![test label]

[test label]: /url
[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "bad_shortcut_image_and_no_matching_lrd_with_duplicate",
        source_file_contents="""![another test label]

[test label]: /url
[test label]: /url
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
{temp_source_path}:4:1: MD053: Link and image reference definitions should be needed. (link-image-reference-definitions)
""",
    ),
    pluginRuleTest(
        "good_lrd_acts_like_comment",
        source_file_contents="""[//]: /url (This behaves like a comment)
""",
    ),
    pluginRuleTest(
        "good_lrd_acts_like_comment_with_config",
        source_file_contents="""[///]: /url (This behaves like a comment)
""",
        set_args=["plugins.md053.ignored-definitions=//,///"],
    ),
    pluginRuleTest(
        "good_lrd_acts_like_comment_with_config_include_blank",
        source_file_contents="""[///]: /url (This behaves like a comment)
""",
        set_args=["plugins.md053.ignored-definitions=//,,///"],
    ),
]


@pytest.mark.rules
@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md053_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md051")


@pytest.mark.rules
@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md053_config(test: pluginConfigErrorTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}bad_fenced_backticks_and_tildes.md")


@pytest.mark.rules
def test_md053_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md053",
        """
  ITEM               DESCRIPTION

  Id                 md053
  Name(s)            link-image-reference-definitions
  Short Description  Link and image reference definitions should be needed.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md053.md


  CONFIGURATION ITEM   TYPE    VALUE

  ignored-definitions  string  "['//']"
""",
    )
    execute_query_configuration_test(config_test)
