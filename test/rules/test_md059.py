"""
Module to provide tests related to the MD059 rule.
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

source_path = os.path.join("test", "resources", "rules", "md059") + os.sep

configTests = [
    pluginConfigErrorTest(
        "invalid_prohibited_phrases_type",
        use_strict_config=True,
        set_args=["plugins.md059.prohibited-phrases=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md059.prohibited-phrases' must be of type 'str'.""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_inline_good_text",
        source_file_contents="""[This is a link](#top)
""",
    ),
    pluginRuleTest(
        "bad_inline_bad_click_here_text",
        source_file_contents="""[click here](#top)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD059: Link text should be descriptive. (descriptive-link-text)
""",
    ),
    pluginRuleTest(
        "bad_inline_bad_click_here_text_space_before",
        source_file_contents="""[ click here](#top)
""",
        disable_rules="MD039",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD059: Link text should be descriptive. (descriptive-link-text)
""",
    ),
    pluginRuleTest(
        "bad_inline_bad_click_here_text_space_after",
        source_file_contents="""[click here ](#top)
""",
        disable_rules="MD039",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD059: Link text should be descriptive. (descriptive-link-text)
""",
    ),
    pluginRuleTest(
        "bad_inline_bad_click_here_text_mixed",
        source_file_contents="""[Click Here](#top)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD059: Link text should be descriptive. (descriptive-link-text)
""",
    ),
    pluginRuleTest(
        "bad_inline_bad_click_here_text_double_space",
        source_file_contents="""[Click  Here](#top)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD059: Link text should be descriptive. (descriptive-link-text)
""",
    ),
    pluginRuleTest(
        "bad_inline_bad_here_text",
        source_file_contents="""[here](#top)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD059: Link text should be descriptive. (descriptive-link-text)
""",
    ),
    pluginRuleTest(
        "bad_inline_bad_link_text",
        source_file_contents="""[link](#top)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD059: Link text should be descriptive. (descriptive-link-text)
""",
    ),
    pluginRuleTest(
        "bad_inline_bad_more_text",
        source_file_contents="""[more](#top)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD059: Link text should be descriptive. (descriptive-link-text)
""",
    ),
    pluginRuleTest(
        "good_full_good_text",
        source_file_contents="""[This is a link][bar]

[bar]: /url "title"
""",
    ),
    pluginRuleTest(
        "bad_full_bad_click_here_text",
        source_file_contents="""[click here][bar]

[bar]: /url "title"
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD059: Link text should be descriptive. (descriptive-link-text)
""",
    ),
    pluginRuleTest(
        "good_collapsed_good_text",
        source_file_contents="""[This is a link][]

[This is a link]: /url "title"
""",
    ),
    pluginRuleTest(
        "bad_collapsed_bad_click_here_text",
        source_file_contents="""[click here][]

[click here]: /url "title"
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD059: Link text should be descriptive. (descriptive-link-text)
""",
    ),
    pluginRuleTest(
        "good_shortcut_good_text",
        source_file_contents="""[This is a link]

[This is a link]: /url "title"
""",
    ),
    pluginRuleTest(
        "bad_shortcut_bad_click_here_text",
        source_file_contents="""[click here]

[click here]: /url "title"
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD059: Link text should be descriptive. (descriptive-link-text)
""",
    ),
    pluginRuleTest(
        "good_inline_good_click_here_text_after_config",
        source_file_contents="""[click here](#top)
""",
        use_strict_config=True,
        set_args=["plugins.md059.prohibited-phrases=here,link,more"],
    ),
    pluginRuleTest(
        "good_inline_image_good_text",
        source_file_contents="""![This is a link](#top)
""",
    ),
    pluginRuleTest(
        "bad_inline_image_bad_click_here_text",
        source_file_contents="""![click here](#top)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD059: Link text should be descriptive. (descriptive-link-text)
""",
    ),
    pluginRuleTest(
        "good_inline_good_click_here_text_after_config_with_empty_element",
        source_file_contents="""[click here](#top)
""",
        use_strict_config=True,
        set_args=["plugins.md059.prohibited-phrases=here,link,,more"],
    ),
]


@pytest.mark.rules
@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md059_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md051")


@pytest.mark.rules
@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md059_config(test: pluginConfigErrorTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}bad_fenced_backticks_and_tildes.md")


@pytest.mark.rules
def test_md059_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md059",
        """
  ITEM               DESCRIPTION

  Id                 md059
  Name(s)            descriptive-link-text
  Short Description  Link text should be descriptive.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md059.md


  CONFIGURATION ITEM  TYPE    VALUE

  prohibited-phrases  string  "['click here', 'here', 'link', 'more']"
""",
    )
    execute_query_configuration_test(config_test)
