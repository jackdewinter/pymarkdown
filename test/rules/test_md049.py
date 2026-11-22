"""
Module to provide tests related to the MD049 rule.
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

source_path = os.path.join("test", "resources", "rules", "md049") + os.sep

configTests = [
    pluginConfigErrorTest(
        "invalid_style_type",
        use_strict_config=True,
        set_args=["plugins.md049.style=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md049.style' must be of type 'str'.""",
    ),
    pluginConfigErrorTest(
        "invalid_style",
        use_strict_config=True,
        set_args=["plugins.md049.style=not-matching"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md049.style' is not valid: Allowable values: ['consistent', 'asterisk', 'underscore']""",
    ),
]


scanTests = [
    pluginRuleTest(
        "good_default_with_consistent_asterisk_emphasis",
        source_file_contents="""This is *one* emphasis.

This is the *same* emphasis.
""",
    ),
    pluginRuleTest(
        "bad_default_with_different_asterisk_emphasis",
        source_file_contents="""This is *one* emphasis.

This is the _another_ emphasis.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:13: MD049: Emphasis style [Expected: asterisk; Actual: underscore] (emphasis-style)
""",
    ),
    pluginRuleTest(
        "good_default_with_consistent_underscore_emphasis",
        source_file_contents="""This is _one_ emphasis.

This is the _same_ emphasis.
""",
    ),
    pluginRuleTest(
        "bad_default_with_different_underscore_emphasis",
        source_file_contents="""This is _one_ emphasis.

This is the *another* emphasis.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:13: MD049: Emphasis style [Expected: underscore; Actual: asterisk] (emphasis-style)
""",
    ),
    pluginRuleTest(
        "good_consistent_with_consistent_asterisk_emphasis",
        source_file_contents="""This is *one* emphasis.

This is the *same* emphasis.
""",
        set_args=["plugins.md049.style=consistent"],
    ),
    pluginRuleTest(
        "bad_consistent_with_different_asterisk_emphasis",
        source_file_contents="""This is *one* emphasis.

This is the _another_ emphasis.
""",
        set_args=["plugins.md049.style=consistent"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:13: MD049: Emphasis style [Expected: asterisk; Actual: underscore] (emphasis-style)
""",
    ),
    pluginRuleTest(
        "bad_consistent_with_different_asterisk_emphasis_and_strikethrough",
        source_file_contents="""This is ~strikethrough~ emphasis. (should not affect consistent)

This is *one* emphasis.

This is the _another_ emphasis.
""",
        set_args=[
            "plugins.md049.style=consistent",
            "extensions.markdown-strikethrough.enabled=$!True",
        ],
        use_strict_config=True,
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:13: MD049: Emphasis style [Expected: asterisk; Actual: underscore] (emphasis-style)
""",
    ),
    pluginRuleTest(
        "good_consistent_with_consistent_underscore_emphasis",
        source_file_contents="""This is _one_ emphasis.

This is the _same_ emphasis.
""",
        set_args=["plugins.md049.style=consistent"],
    ),
    pluginRuleTest(
        "bad_consistent_with_different_underscore_emphasis",
        source_file_contents="""This is _one_ emphasis.

This is the *another* emphasis.
""",
        set_args=["plugins.md049.style=consistent"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:13: MD049: Emphasis style [Expected: underscore; Actual: asterisk] (emphasis-style)
""",
    ),
    pluginRuleTest(
        "bad_consistent_with_different_underscore_emphasis_and_strikethrough",
        source_file_contents="""This is ~strikethrough~ emphasis. (should not affect consistent)

This is _one_ emphasis.

This is the *another* emphasis.
""",
        set_args=[
            "plugins.md049.style=consistent",
            "extensions.markdown-strikethrough.enabled=$!True",
        ],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:13: MD049: Emphasis style [Expected: underscore; Actual: asterisk] (emphasis-style)
""",
    ),
    pluginRuleTest(
        "good_asterisk_with_asterisk_emphasis",
        source_file_contents="""This is *one* emphasis.
""",
        set_args=["plugins.md049.style=asterisk"],
    ),
    pluginRuleTest(
        "bad_asterisk_with_underscore_emphasis",
        source_file_contents="""This is _one_ emphasis.
""",
        set_args=["plugins.md049.style=asterisk"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:9: MD049: Emphasis style [Expected: asterisk; Actual: underscore] (emphasis-style)
""",
    ),
    pluginRuleTest(
        "bad_asterisk_with_strikethrough_emphasis",
        source_file_contents="""This is ~strikethrough~.

This is _one_ emphasis.
""",
        set_args=[
            "plugins.md049.style=asterisk",
            "extensions.markdown-strikethrough.enabled=$!True",
        ],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:9: MD049: Emphasis style [Expected: asterisk; Actual: underscore] (emphasis-style)
""",
    ),
    pluginRuleTest(
        "good_underscore_with_underscore_emphasis",
        source_file_contents="""This is _one_ emphasis.
""",
        set_args=["plugins.md049.style=underscore"],
    ),
    pluginRuleTest(
        "bad_underscore_with_asterisk_emphasis",
        source_file_contents="""This is *one* emphasis.
""",
        set_args=["plugins.md049.style=underscore"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:9: MD049: Emphasis style [Expected: underscore; Actual: asterisk] (emphasis-style)
""",
    ),
    pluginRuleTest(
        "bad_underscore_with_strikethrough_emphasis",
        source_file_contents="""This is ~strikethrough~.

This is *one* emphasis.
""",
        set_args=[
            "plugins.md049.style=underscore",
            "extensions.markdown-strikethrough.enabled=$!True",
        ],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:9: MD049: Emphasis style [Expected: underscore; Actual: asterisk] (emphasis-style)
""",
    ),
]


@pytest.mark.rules
@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md049_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md049")


@pytest.mark.rules
@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md049_config(test: pluginConfigErrorTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}bad_fenced_backticks_and_tildes.md")


@pytest.mark.rules
def test_md049_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md049",
        """
  ITEM               DESCRIPTION

  Id                 md049
  Name(s)            emphasis-style
  Short Description  Emphasis style
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md049.md


  CONFIGURATION ITEM  TYPE    VALUE

  style               string  "consistent"

""",
    )
    execute_query_configuration_test(config_test)
