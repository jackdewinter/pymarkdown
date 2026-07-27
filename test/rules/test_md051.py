"""
Module to provide tests related to the MD048 rule.
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
        set_args=["plugins.md051.ignore_case=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md051.ignore_case' must be of type 'bool'.""",
    ),
]


scanTests = [
    pluginRuleTest(
        "good_atx_simple_found",
        source_file_contents="""# Heading Name

[Link](#heading-name)
""",
    ),
    pluginRuleTest(
        "bad_atx_simple_not_found",
        source_file_contents="""# Heading Name

[Link](#fragment)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "bad_atx_simple_with_capitals_not_found",
        source_file_contents="""# Heading Name

[Link](#Heading-Name)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "bad_atx_simple_with_capitals_and_config_found",
        source_file_contents="""# Heading Name

[Link](#Heading-Name)
""",
        set_args=["plugins.md051.ignore_case=$!False"],
    ),
    pluginRuleTest(
        "good_atx_unicode_letters",
        source_file_contents="""# Heading ȅǣݵ Name

[Link](#heading-%C8%85%C7%A3%DD%B5-name)
""",
    ),
    pluginRuleTest(
        "good_atx_backslash_escape",
        source_file_contents="""# Heading \\& Name

[Link](#heading--name)
""",
    ),
    pluginRuleTest(
        "good_atx_entity_reference",
        source_file_contents="""# Heading &copy; Name

[Link](#fragment)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "good_atx_code_span",
        source_file_contents="""# Heading `foo` Name

[Link](#heading-foo-name)
""",
    ),
    pluginRuleTest(
        "bad_atx_emphasis",
        source_file_contents="""# Heading *foo* Name

[Link](#fragment)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "bad_atx_strikethrough_emphasis",
        source_file_contents="""# Heading ~foo~ Name

[Link](#fragment)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "bad_atx_link",
        source_file_contents="""# Heading [Google](www.google.com) Name

[Link](#fragment)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "bad_atx_autolink",
        source_file_contents="""# Heading <http://foo.bar.baz> Target

[Link](#fragment)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "bad_atx_raw_html",
        disable_rules="md033",
        source_file_contents="""# Heading <del>name</del> Name

[Link](#fragment)
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD051: Link fragments should be valid. (link-fragments)
""",
    ),
    pluginRuleTest(
        "good_atx_html_anchor_tag",
        source_file_contents="""<a name="bookmark">
</a>

[Link](#bookmark)
""",
        disable_rules="md033",
    ),
    pluginRuleTest(
        "good_atx_raw_html_anchor_tag",
        source_file_contents="""This is a new <a name="bookmark">bookmark</a> anchor.

[Link](#bookmark)
""",
        disable_rules="md033",
        use_debug=True
    ),
    pluginRuleTest(
        "good_atx_raw_html_anchor_tag_still",
        source_file_contents="""<a name="bookmark"></a>

[Link](#bookmark)
""",
        disable_rules="md033",
    ),
    pluginRuleTest(
        "good_atx_raw_html_tag_with_id",
        source_file_contents="""This is a <a id="bookmark"></a> new tag.

[Link](#bookmark)
""",
        disable_rules="md033",
    ),
    pluginRuleTest(
        "good_atx_raw_html_tag_with_id_still",
        source_file_contents="""<a id="bookmark"></a>

[Link](#bookmark)
""",
        disable_rules="md033",
    ),
    pluginRuleTest(
        "good_link_fragment_top",
        source_file_contents="""[Link](#top)
""",
    ),
    pluginRuleTest(
        "good_link_fragment_specific_line",
        source_file_contents="""[Link](#L20)
""",
    ),
    pluginRuleTest(
        "good_link_fragment_specific_lines_and_columns",
        source_file_contents="""[Link](#L19C5-L21C11)
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


  CONFIGURATION ITEM  TYPE     VALUE

  ignore_case         boolean  True

""",
    )
    execute_query_configuration_test(config_test)
