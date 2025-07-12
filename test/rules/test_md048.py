"""
Module to provide tests related to the MD048 rule.
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

source_path = os.path.join("test", "resources", "rules", "md048") + os.sep

configTests = [
    pluginConfigErrorTest(
        "invalid_style_type",
        use_strict_config=True,
        set_args=["plugins.md048.style=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md048.style' must be of type 'str'.""",
    ),
    pluginConfigErrorTest(
        "invalid_style",
        use_strict_config=True,
        set_args=["plugins.md048.style=not-matching"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md048.style' is not valid: Allowable values: ['consistent', 'tilde', 'backtick']""",
    ),
]


scanTests = [
    pluginRuleTest(
        "good_fenced_tildes_with_consistent",
        source_file_name=f"{source_path}good_fenced_tildes.md",
        set_args=["plugins.md048.style=consistent"],
    ),
    pluginRuleTest(
        "good_fenced_backticks_with_consistent",
        source_file_name=f"{source_path}good_fenced_backticks.md",
        set_args=["plugins.md048.style=consistent"],
    ),
    pluginRuleTest(
        "bad_fenced_backticks_and_tildes_with_consistent",
        source_file_name=f"{source_path}bad_fenced_backticks_and_tildes.md",
        set_args=["plugins.md048.style=consistent"],
        source_file_contents="""```Python
def test():
    print("test")
```

~~~Python
def test():
    print("test")
~~~
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: MD048: Code fence style [Expected: backtick; Actual: tilde] (code-fence-style)
""",
        fix_expected_file_contents="""```Python
def test():
    print("test")
```

```Python
def test():
    print("test")
```
""",
    ),
    pluginRuleTest(
        "good_fenced_backticks_with_backticks",
        source_file_name=f"{source_path}good_fenced_backticks.md",
        set_args=["plugins.md048.style=backtick"],
    ),
    pluginRuleTest(
        "bad_fenced_tildes_with_backticks",
        source_file_name=f"{source_path}good_fenced_tildes.md",
        set_args=["plugins.md048.style=backtick"],
        source_file_contents="""~~~Python
def test():
    print("test")
~~~

~~~Python
def test():
    print("test")
~~~
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD048: Code fence style [Expected: backtick; Actual: tilde] (code-fence-style)
{temp_source_path}:6:1: MD048: Code fence style [Expected: backtick; Actual: tilde] (code-fence-style)
""",
        fix_expected_file_contents="""```Python
def test():
    print("test")
```

```Python
def test():
    print("test")
```
""",
    ),
    pluginRuleTest(
        "bad_fenced_backticks_and_tildes_with_backticks",
        source_file_name=f"{source_path}bad_fenced_backticks_and_tildes.md",
        set_args=["plugins.md048.style=backtick"],
        source_file_contents="""```Python
def test():
    print("test")
```

~~~Python
def test():
    print("test")
~~~
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: MD048: Code fence style [Expected: backtick; Actual: tilde] (code-fence-style)
""",
        fix_expected_file_contents="""```Python
def test():
    print("test")
```

```Python
def test():
    print("test")
```
""",
    ),
    pluginRuleTest(
        "good_fenced_tildes_with_tilde",
        source_file_name=f"{source_path}good_fenced_tildes.md",
        set_args=["plugins.md048.style=tilde"],
    ),
    pluginRuleTest(
        "bad_fenced_backticks_with_tilde",
        source_file_name=f"{source_path}good_fenced_backticks.md",
        set_args=["plugins.md048.style=tilde"],
        source_file_contents="""```Python
def test():
    print("test")
```

```Python
def test():
    print("test")
```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD048: Code fence style [Expected: tilde; Actual: backtick] (code-fence-style)
{temp_source_path}:6:1: MD048: Code fence style [Expected: tilde; Actual: backtick] (code-fence-style)
""",
        fix_expected_file_contents="""~~~Python
def test():
    print("test")
~~~

~~~Python
def test():
    print("test")
~~~
""",
    ),
    pluginRuleTest(
        "bad_fenced_backticks_and_tildes_with_indented",
        source_file_name=f"{source_path}bad_fenced_backticks_and_tildes.md",
        set_args=["plugins.md048.style=tilde"],
        source_file_contents="""```Python
def test():
    print("test")
```

~~~Python
def test():
    print("test")
~~~
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD048: Code fence style [Expected: tilde; Actual: backtick] (code-fence-style)
""",
        fix_expected_file_contents="""~~~Python
def test():
    print("test")
~~~

~~~Python
def test():
    print("test")
~~~
""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md048_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md048")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md048_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md048_config(test: pluginConfigErrorTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(test, f"{source_path}bad_fenced_backticks_and_tildes.md")


def test_md048_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md048",
        """
  ITEM               DESCRIPTION

  Id                 md048
  Name(s)            code-fence-style
  Short Description  Code fence style
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md048.md


  CONFIGURATION ITEM  TYPE    VALUE

  style               string  "consistent"

""",
    )
    execute_query_configuration_test(config_test)
