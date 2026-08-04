"""
Module to provide tests related to the MD054 rule.
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

source_path = os.path.join("test", "resources", "rules", "md054") + os.sep

configTests = [
    pluginConfigErrorTest(
        "invalid_autolinks_type",
        use_strict_config=True,
        set_args=["plugins.md054.autolinks=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md054.autolinks' must be of type 'bool'.""",
    ),
    pluginConfigErrorTest(
        "invalid_inline_links_type",
        use_strict_config=True,
        set_args=["plugins.md054.inline-links=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md054.inline-links' must be of type 'bool'.""",
    ),
    pluginConfigErrorTest(
        "invalid_full_links_type",
        use_strict_config=True,
        set_args=["plugins.md054.full-links=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md054.full-links' must be of type 'bool'.""",
    ),
    pluginConfigErrorTest(
        "invalid_collapsed_links_type",
        use_strict_config=True,
        set_args=["plugins.md054.collapsed-links=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md054.collapsed-links' must be of type 'bool'.""",
    ),
    pluginConfigErrorTest(
        "invalid_shortcut_links_type",
        use_strict_config=True,
        set_args=["plugins.md054.shortcut-links=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md054.shortcut-links' must be of type 'bool'.""",
    ),
    pluginConfigErrorTest(
        "invalid_inline_urls_type",
        use_strict_config=True,
        set_args=["plugins.md054.inline-urls=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md054.inline-urls' must be of type 'bool'.""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_allow_uri_autolink",
        source_file_contents="""<http://foo.bar.baz>
""",
    ),
    pluginRuleTest(
        "bad_disallow_uri_autolink_by_configuration",
        source_file_contents="""<http://foo.bar.baz>
""",
        set_args=["plugins.md054.autolinks=$!False"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD054: Link and image style. [Disallowed Type: Autolink] (link-image-style)
""",
    ),
    pluginRuleTest(
        "good_allow_email_autolink",
        source_file_contents="""<someone@somewhere.com>
""",
    ),
    pluginRuleTest(
        "bad_disallow_email_autolink_by_configuration",
        source_file_contents="""<someone@somewhere.com>
""",
        set_args=["plugins.md054.autolinks=$!False"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD054: Link and image style. [Disallowed Type: Autolink] (link-image-style)
""",
    ),
    pluginRuleTest(
        "good_allow_inline_url_link",
        source_file_contents="""[/inline](/inline)
""",
    ),
    pluginRuleTest(
        "bad_disallow_inline_url_link_by_configuration",
        source_file_contents="""[/inline](/inline)
""",
        set_args=["plugins.md054.inline-urls=$!False"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD054: Link and image style. [Disallowed Type: Inline Url] (link-image-style)
""",
    ),
    pluginRuleTest(
        "good_allow_inline_link",
        source_file_contents="""[label](/inline)
""",
    ),
    pluginRuleTest(
        "bad_disallow_inline_link_by_configuration",
        source_file_contents="""[label](/inline)
""",
        set_args=["plugins.md054.inline-links=$!False"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD054: Link and image style. [Disallowed Type: Inline] (link-image-style)
""",
    ),
    pluginRuleTest(
        "good_allow_full_link",
        source_file_contents="""[text][label]

[label]: /url
""",
    ),
    pluginRuleTest(
        "bad_disallow_full_link_by_configuration",
        source_file_contents="""[text][label]

[label]: /url
""",
        set_args=["plugins.md054.full-links=$!False"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD054: Link and image style. [Disallowed Type: Full] (link-image-style)
""",
    ),
    pluginRuleTest(
        "good_allow_collapsed_link",
        source_file_contents="""[label][]

[label]: /url
""",
    ),
    pluginRuleTest(
        "bad_disallow_collapsed_link_by_configuration",
        source_file_contents="""[label][]

[label]: /url
""",
        set_args=["plugins.md054.collapsed-links=$!False"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD054: Link and image style. [Disallowed Type: Collapsed] (link-image-style)
""",
    ),
    pluginRuleTest(
        "good_allow_shortcut_link",
        source_file_contents="""[label]

[label]: /url
""",
    ),
    pluginRuleTest(
        "bad_disallow_shortcut_link_by_configuration",
        source_file_contents="""[label]

[label]: /url
""",
        set_args=["plugins.md054.shortcut-links=$!False"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD054: Link and image style. [Disallowed Type: Shortcut] (link-image-style)
""",
    ),
    pluginRuleTest(
        "good_allow_inline_url_image",
        source_file_contents="""![/inline](/inline)
""",
    ),
    pluginRuleTest(
        "bad_disallow_inline_url_image_by_configuration",
        source_file_contents="""![/inline](/inline)
""",
        set_args=["plugins.md054.inline-urls=$!False"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD054: Link and image style. [Disallowed Type: Inline Url] (link-image-style)
""",
    ),
    pluginRuleTest(
        "good_allow_inline_url_image_by_configuration_with_title",
        source_file_contents="""![/inline](/inline "title")
""",
        set_args=["plugins.md054.inline-urls=$!False"],
    ),
    pluginRuleTest(
        "good_allow_inline_image",
        source_file_contents="""![label](/inline)
""",
    ),
    pluginRuleTest(
        "bad_disallow_inline_image_by_configuration",
        source_file_contents="""![label](/inline)
""",
        set_args=["plugins.md054.inline-links=$!False"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD054: Link and image style. [Disallowed Type: Inline] (link-image-style)
""",
    ),
    pluginRuleTest(
        "good_allow_full_image",
        source_file_contents="""![text][label]

[label]: /url
""",
    ),
    pluginRuleTest(
        "bad_disallow_full_image_by_configuration",
        source_file_contents="""![text][label]

[label]: /url
""",
        set_args=["plugins.md054.full-links=$!False"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD054: Link and image style. [Disallowed Type: Full] (link-image-style)
""",
    ),
    pluginRuleTest(
        "good_allow_collapsed_image",
        source_file_contents="""![label][]

[label]: /url
""",
    ),
    pluginRuleTest(
        "bad_disallow_collapsed_image_by_configuration",
        source_file_contents="""![label][]

[label]: /url
""",
        set_args=["plugins.md054.collapsed-links=$!False"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD054: Link and image style. [Disallowed Type: Collapsed] (link-image-style)
""",
    ),
    pluginRuleTest(
        "good_allow_shortcut_image",
        source_file_contents="""![label]

[label]: /url
""",
    ),
    pluginRuleTest(
        "bad_disallow_shortcut_image_by_configuration",
        source_file_contents="""![label]

[label]: /url
""",
        set_args=["plugins.md054.shortcut-links=$!False"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD054: Link and image style. [Disallowed Type: Shortcut] (link-image-style)
""",
    ),
]


@pytest.mark.rules
@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md054_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md054")


@pytest.mark.rules
@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md054_config(test: pluginConfigErrorTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}bad_fenced_backticks_and_tildes.md")


@pytest.mark.rules
def test_md054_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md054",
        """
  ITEM               DESCRIPTION

  Id                 md054
  Name(s)            link-image-style
  Short Description  Link and image style.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md054.md


  CONFIGURATION ITEM  TYPE     VALUE

  autolinks           boolean  True
  inline-links        boolean  True
  full-links          boolean  True
  collapsed-links     boolean  True
  shortcut-links      boolean  True
  inline-urls         boolean  True

""",
    )
    execute_query_configuration_test(config_test)
