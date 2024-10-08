"""
Module to provide tests related to the MD035 rule.
"""

import os
from test.rules.utils import (
    calculate_fix_tests,
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

source_path = os.path.join("test", "resources", "rules", "md035") + os.sep

configTests = [
    pluginConfigErrorTest(
        "invalid_style_type",
        use_strict_config=True,
        set_args=["plugins.md035.style=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md035.style' must be of type 'str'.""",
    ),
    pluginConfigErrorTest(
        "invalid_style_both_spaces",
        use_strict_config=True,
        set_args=["plugins.md035.style= ---"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md035.style' is not valid: Allowable values cannot including leading or trailing spaces.""",
    ),
    pluginConfigErrorTest(
        "invalid_style_empty",
        use_strict_config=True,
        set_args=["plugins.md035.style="],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md035.style' is not valid: Allowable values are: consistent, '---', '***', `___`, or any other horizontal rule text.""",
    ),
    pluginConfigErrorTest(
        "invalid_style_trailing_spaces",
        use_strict_config=True,
        set_args=["plugins.md035.style=--- "],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md035.style' is not valid: Allowable values cannot including leading or trailing spaces.""",
    ),
    pluginConfigErrorTest(
        "invalid_style_bad_character",
        use_strict_config=True,
        set_args=["plugins.md035.style=-=-=-"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md035.style' is not valid: Allowable values are: consistent, '---', '***', `___`, or any other horizontal rule text.""",
    ),
    pluginConfigErrorTest(
        "invalid_style_mixed_valid_character",
        use_strict_config=True,
        set_args=["plugins.md035.style=*-*-*-*"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md035.style' is not valid: Allowable values are: consistent, '---', '***', `___`, or any other horizontal rule text.""",
    ),
    pluginConfigErrorTest(
        "invalid_style_mixed_valid_character",
        use_strict_config=True,
        set_args=["plugins.md035.style=*-*-*-*"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md035.style' is not valid: Allowable values are: consistent, '---', '***', `___`, or any other horizontal rule text.""",
    ),
]


scanTests = [
    pluginRuleTest(
        "good_consistent_dash",
        source_file_name=f"{source_path}good_consistent_dash.md",
    ),
    pluginRuleTest(
        "good_consistent_dash_with_configuration",
        source_file_name=f"{source_path}good_consistent_dash.md",
        use_strict_config=True,
        set_args=["plugins.md035.style=consistent"],
    ),
    pluginRuleTest(
        "bad_consistent_dash",
        source_file_name=f"{source_path}bad_consistent_dash.md",
        source_file_contents="""---

this is one section

- - -
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD035: Horizontal rule style [Expected: ---, Actual: - - -] (hr-style)
""",
        fix_expected_file_contents="""---

this is one section

---
""",
    ),
    pluginRuleTest(
        "bad_consistent_dash_with_leading_spaces",
        source_file_name=f"{source_path}bad_consistent_dash_with_leading_spaces.md",
        source_file_contents="""---

this is one section

 - - -
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:2: MD035: Horizontal rule style [Expected: ---, Actual: - - -] (hr-style)
""",
        fix_expected_file_contents="""---

this is one section

 ---
""",
    ),
    pluginRuleTest(
        "good_dash_marker",
        source_file_name=f"{source_path}good_consistent_dash.md",
        set_args=["plugins.md035.style=---"],
        use_strict_config=True,
    ),
    pluginRuleTest(
        "bad_dash_marker",
        source_file_name=f"{source_path}bad_consistent_dash.md",
        set_args=["plugins.md035.style=---"],
        use_strict_config=True,
        source_file_contents="""---

this is one section

- - -
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD035: Horizontal rule style [Expected: ---, Actual: - - -] (hr-style)
""",
        fix_expected_file_contents="""---

this is one section

---
""",
    ),
    pluginRuleTest(
        "good_consistent_asterisk",
        source_file_name=f"{source_path}good_consistent_asterisk.md",
    ),
    pluginRuleTest(
        "bad_consistent_asterisk",
        source_file_name=f"{source_path}bad_consistent_asterisk.md",
        source_file_contents="""***

this is one section

* * *
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD035: Horizontal rule style [Expected: ***, Actual: * * *] (hr-style)
""",
        fix_expected_file_contents="""***

this is one section

***
""",
    ),
    pluginRuleTest(
        "good_asterisk_marker",
        source_file_name=f"{source_path}good_consistent_asterisk.md",
        use_strict_config=True,
        set_args=["plugins.md035.style=* * *"],
    ),
    pluginRuleTest(
        "bad_asterisk_marker",
        source_file_name=f"{source_path}bad_consistent_asterisk.md",
        source_file_contents="""***

this is one section

* * *
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD035: Horizontal rule style [Expected: ***, Actual: * * *] (hr-style)
""",
        fix_expected_file_contents="""***

this is one section

***
""",
    ),
    pluginRuleTest(
        "good_consistent_underscore",
        source_file_name=f"{source_path}good_consistent_underscore.md",
    ),
    pluginRuleTest(
        "bad_consistent_underscore",
        source_file_name=f"{source_path}bad_consistent_underscore.md",
        source_file_contents="""___

this is one section

______
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD035: Horizontal rule style [Expected: ___, Actual: ______] (hr-style)
""",
        fix_expected_file_contents="""___

this is one section

___
""",
    ),
    pluginRuleTest(
        "good_underscore_marker",
        source_file_name=f"{source_path}good_consistent_underscore.md",
        use_strict_config=True,
        set_args=["plugins.md035.style=______"],
    ),
    pluginRuleTest(
        "bad_underscore_marker",
        source_file_name=f"{source_path}bad_consistent_underscore.md",
        source_file_contents="""___

this is one section

______
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD035: Horizontal rule style [Expected: ___, Actual: ______] (hr-style)
""",
        fix_expected_file_contents="""___

this is one section

___
""",
    ),
    pluginRuleTest(  # bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list from md031
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list",
        source_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >   ______
> >   ```block
> >   A code block
> >   ```
> >   ______
""",
        disable_rules="md031,md032",
        scan_expected_return_code=0,
        scan_expected_output="",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md035_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md035")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md035_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md035_config(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}good_consistent_dash.md")


def test_md035_query_config():
    config_test = pluginQueryConfigTest(
        "md035",
        """
  ITEM               DESCRIPTION

  Id                 md035
  Name(s)            hr-style
  Short Description  Horizontal rule style
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md035.md


  CONFIGURATION ITEM  TYPE    VALUE

  style               string  "consistent"

""",
    )
    execute_query_configuration_test(config_test)
