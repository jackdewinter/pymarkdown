"""
Module to provide tests related to the MD051 rule.
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

source_path = os.path.join("test", "resources", "rules", "md051") + os.sep

configTests = [
    pluginConfigErrorTest(
        "invalid_ignore_case_type",
        use_strict_config=True,
        set_args=["plugins.md051.ignore-case=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md051.ignore-case' must be of type 'bool'.""",
    ),
    pluginConfigErrorTest(
        "invalid_ignore_pattern_regex",
        use_strict_config=True,
        set_args=["plugins.md051.ignore-pattern-regex=[open_not_closed"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md051.ignore-pattern-regex' is not a valid regular expression.""",
    ),
]


scanTests = [
    pluginRuleTest(
        "good_atx_simple_found",
        source_file_contents="""# Heading Name

[Heading Text](#heading-name)
""",
    ),
    pluginRuleTest(
        "bad_atx_simple_not_found",
        source_file_contents="""# Heading Name

[Heading Text](#fragment)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "bad_atx_simple_with_capitals_not_found",
        source_file_contents="""# Heading Name

[Heading Text](#Heading-Name)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "good_atx_simple_with_capitals_and_config_found",
        source_file_contents="""# Heading Name

[Heading Text](#Heading-Name)
""",
        set_args=["plugins.md051.ignore-case=$!False"],
    ),
    pluginRuleTest(
        "good_atx_unicode_letters",
        source_file_contents="""# Heading ȅǣݵ Name

[Heading Text](#heading-%C8%85%C7%A3%DD%B5-name)
""",
    ),
    pluginRuleTest(
        "good_atx_backslash_escape",
        source_file_contents="""# Heading \\* Name

[Heading Text](#heading--name)
""",
    ),
    pluginRuleTest(
        "good_atx_backslash_escape_special",
        source_file_contents="""# Heading \\< Name

[Heading Text](#heading--name)
""",
    ),
    pluginRuleTest(
        "good_atx_entity_reference",
        source_file_contents="""# Heading &copy; Name

[Heading Text](#heading--name)
""",
    ),
    pluginRuleTest(
        "good_atx_numeric_entity_reference",
        source_file_contents="""## Heading &#x0041; Name

[Heading Text](#heading-a-name)
""",
    ),
    pluginRuleTest(
        "good_atx_code_span",
        source_file_contents="""# Heading `foo` Name

[Heading Text](#heading-foo-name)
""",
    ),
    pluginRuleTest(
        "good_atx_emphasis",
        source_file_contents="""# Heading *foo* Name

[Heading Text](#heading-foo-name)
""",
    ),
    pluginRuleTest(
        "good_atx_strikethrough_emphasis",
        source_file_contents="""# Heading ~foo~ Name

[Heading Text](#heading-foo-name)
""",
        enable_extensions="markdown-strikethrough",
    ),
    pluginRuleTest(
        "good_atx_link",
        source_file_contents="""# Heading [Google](www.google.com) Name

[Heading Text](#heading-google-name)
""",
    ),
    pluginRuleTest(
        "good_atx_uri_autolink",
        source_file_contents="""# Heading <http://foo.bar.baz> Target

[Heading Text](#heading-httpfoobarbaz-target)
""",
    ),
    pluginRuleTest(
        "good_atx_email_autolink",
        source_file_contents="""# Heading <foo@bar.example.com> Target

[Heading Text](#heading-foobarexamplecom-target)
""",
    ),
    pluginRuleTest(
        "good_atx_raw_html",
        disable_rules="md033",
        source_file_contents="""# Heading <del>name</del> Name

[Heading Text](#heading-name-name)
""",
    ),
    pluginRuleTest(
        "good_atx_html_anchor_tag",
        source_file_contents="""<a name="bookmark">
</a>

[Heading Text](#bookmark)
""",
        disable_rules="md033",
    ),
    pluginRuleTest(
        "good_atx_raw_html_anchor_tag",
        source_file_contents="""This is a new <a name="bookmark">bookmark</a> anchor.

[Heading Text](#bookmark)
""",
        disable_rules="md033",
        use_debug=True,
    ),
    pluginRuleTest(
        "good_atx_raw_html_anchor_tag_still",
        source_file_contents="""<a name="bookmark"></a>

[Heading Text](#bookmark)
""",
        disable_rules="md033",
    ),
    pluginRuleTest(
        "good_atx_raw_html_tag_with_id",
        source_file_contents="""This is a <a id="bookmark"></a> new tag.

[Heading Text](#bookmark)
""",
        disable_rules="md033",
    ),
    pluginRuleTest(
        "good_atx_raw_html_tag_with_id_still",
        source_file_contents="""<a id="bookmark"></a>

[Heading Text](#bookmark)
""",
        disable_rules="md033",
    ),
    pluginRuleTest(
        "good_setext_simple_found",
        source_file_contents="""Heading Name
====

[Heading Text](#heading-name)
""",
    ),
    pluginRuleTest(
        "bad_setext_simple_not_found",
        source_file_contents="""Heading Name
====

[Heading Text](#fragment)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "bad_setext_simple_with_capitals_not_found",
        source_file_contents="""Heading Name
====

[Heading Text](#Heading-Name)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "good_setext_simple_with_capitals_and_config_found",
        source_file_contents="""Heading Name
====

[Heading Text](#Heading-Name)
""",
        set_args=["plugins.md051.ignore-case=$!False"],
    ),
    pluginRuleTest(
        "good_setext_unicode_letters",
        source_file_contents="""Heading ȅǣݵ Name
====

[Heading Text](#heading-%C8%85%C7%A3%DD%B5-name)
""",
    ),
    pluginRuleTest(
        "good_setext_backslash_escape",
        source_file_contents="""Heading \\* Name
====

[Heading Text](#heading--name)
""",
    ),
    pluginRuleTest(
        "good_setext_entity_reference",
        source_file_contents="""Heading &copy; Name
====

[Heading Text](#heading--name)
""",
    ),
    pluginRuleTest(
        "good_setext_numeric_entity_reference",
        source_file_contents="""Heading &#x0041; Name
====

[Heading Text](#heading-a-name)
""",
    ),
    pluginRuleTest(
        "good_setext_code_span",
        source_file_contents="""Heading `foo` Name
====

[Heading Text](#heading-foo-name)
""",
    ),
    pluginRuleTest(
        "good_setext_emphasis",
        source_file_contents="""Heading *foo* Name
====

[Heading Text](#heading-foo-name)
""",
    ),
    pluginRuleTest(
        "good_setext_strikethrough_emphasis",
        source_file_contents="""Heading ~foo~ Name
====

[Heading Text](#heading-foo-name)
""",
        enable_extensions="markdown-strikethrough",
    ),
    pluginRuleTest(
        "good_setext_link",
        source_file_contents="""Heading [Google](www.google.com) Name
====

[Heading Text](#heading-google-name)
""",
    ),
    pluginRuleTest(
        "good_setext_uri_autolink",
        source_file_contents="""Heading <http://foo.bar.baz> Target
====

[Heading Text](#heading-httpfoobarbaz-target)
""",
    ),
    pluginRuleTest(
        "good_setext_email_autolink",
        source_file_contents="""Heading <foo@bar.example.com> Target
====

[Heading Text](#heading-foobarexamplecom-target)
""",
    ),
    pluginRuleTest(
        "good_setext_raw_html",
        disable_rules="md033",
        source_file_contents="""Heading <del>name</del> Name
====

[Heading Text](#heading-name-name)
""",
    ),
    pluginRuleTest(
        "bad_lrd_reports_lrd_not_link_to_lrd",
        source_file_contents="""[blah][blah]

[blah]: #fred
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "good_link_fragment_top",
        source_file_contents="""[Heading Text](#top)
""",
    ),
    pluginRuleTest(
        "bad_figure_link_not_present",
        source_file_contents="""[Heading Text](#figure-1)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "good_figure_link_not_present_with_config",
        source_file_contents="""[Heading Text](#figure-1)
""",
        use_strict_config=True,
        set_args=["plugins.md051.ignore-pattern-regex=^figure"],
    ),
    pluginRuleTest(
        "bad_image_link_not_present_with_config",
        source_file_contents="""[Heading Text](#image-1)
""",
        use_strict_config=True,
        set_args=["plugins.md051.ignore-pattern-regex=^figure"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
]


@pytest.mark.rules
@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md051_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md051")


@pytest.mark.rules
@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md051_config(test: pluginConfigErrorTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}bad_fenced_backticks_and_tildes.md")


@pytest.mark.rules
def test_md051_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md051",
        """
  ITEM               DESCRIPTION

  Id                 md051
  Name(s)            link-fragments
  Short Description  Link fragments should be valid.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md051.md


  CONFIGURATION ITEM    TYPE     VALUE

  ignore-case           boolean  True
  ignore-pattern-regex  string   ""
""",
    )
    execute_query_configuration_test(config_test)
