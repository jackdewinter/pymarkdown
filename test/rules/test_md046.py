"""
Module to provide tests related to the MD046 rule.
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

source_path = os.path.join("test", "resources", "rules", "md046") + os.sep

configTests = [
    pluginConfigErrorTest(
        "invalid_configuration_style",
        use_strict_config=True,
        set_args=["plugins.md046.style=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md046.style' must be of type 'str'.""",
    ),
    pluginConfigErrorTest(
        "bad_configuration_style",
        use_strict_config=True,
        set_args=["plugins.md046.style=not-matching"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md046.style' is not valid: Allowable values: ['consistent', 'fenced', 'indented']""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_both_fenced_with_consistent",
        source_file_contents="""```Markdown
# fred
```

```Markdown
# barney
```
""",
        set_args=["plugins.md046.style=consistent"],
    ),
    pluginRuleTest(
        "good_both_indented_with_consistent",
        source_file_contents="""    # fred

wilma

    # barney
""",
        set_args=["plugins.md046.style=consistent"],
    ),
    pluginRuleTest(
        "bad_fenced_and_indented_with_consistent",
        source_file_contents="""```Markdown
# fred
```

    # barney
""",
        set_args=["plugins.md046.style=consistent"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD046: Code block style [Expected: fenced; Actual: indented] (code-block-style)
""",
        fix_expected_file_contents="""```Markdown
# fred
```

```
# barney
```
""",
    ),
    pluginRuleTest(
        "good_both_fenced_with_fenced",
        source_file_contents="""```Markdown
# fred
```

```Markdown
# barney
```
""",
        set_args=["plugins.md046.style=fenced"],
    ),
    pluginRuleTest(
        "bad_both_indented_with_fenced",
        source_file_contents="""    # fred

wilma

    # barney
""",
        set_args=["plugins.md046.style=fenced"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD046: Code block style [Expected: fenced; Actual: indented] (code-block-style)
{temp_source_path}:5:5: MD046: Code block style [Expected: fenced; Actual: indented] (code-block-style)
""",
        fix_expected_file_contents="""```
# fred
```

wilma

```
# barney
```
""",
    ),
    pluginRuleTest(
        "bad_fenced_and_indented_with_fenced",
        source_file_contents="""```Markdown
# fred
```

    # barney
""",
        set_args=["plugins.md046.style=fenced"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD046: Code block style [Expected: fenced; Actual: indented] (code-block-style)
""",
        fix_expected_file_contents="""```Markdown
# fred
```

```
# barney
```
""",
    ),
    pluginRuleTest(
        "bad_both_fenced_with_indented",
        source_file_contents="""```Markdown
# fred
```

```Markdown
# barney
```
""",
        set_args=["plugins.md046.style=indented"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD046: Code block style [Expected: indented; Actual: fenced] (code-block-style)
{temp_source_path}:5:1: MD046: Code block style [Expected: indented; Actual: fenced] (code-block-style)
""",
        fix_expected_file_contents="""    # fred

    # barney
""",
    ),
    pluginRuleTest(
        "good_both_indented_with_indented",
        source_file_contents="""    # fred

wilma

    # barney
""",
        set_args=["plugins.md046.style=indented"],
    ),
    pluginRuleTest(
        "bad_fenced_and_indented_with_indented",
        source_file_contents="""```Markdown
# fred
```

    # barney
""",
        set_args=["plugins.md046.style=indented"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD046: Code block style [Expected: indented; Actual: fenced] (code-block-style)
""",
        fix_expected_file_contents="""    # fred

    # barney
""",
    ),
    pluginRuleTest(
        "bad_paragraph_and_fenced_with_indented",
        source_file_contents="""this is a paragraph
```Markdown
# fred
```
""",
        set_args=["plugins.md046.style=indented"],
        disable_rules="md031",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD046: Code block style [Expected: indented; Actual: fenced] (code-block-style)
""",
        fix_expected_file_contents="""this is a paragraph

    # fred
""",
    ),
    pluginRuleTest(
        "bad_fenced_code_block_starts_with_space_with_indented",
        source_file_contents="""```Markdown
abc
 def
```
""",
        set_args=["plugins.md046.style=indented"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD046: Code block style [Expected: indented; Actual: fenced] (code-block-style)
""",
        fix_expected_file_contents="""    abc
     def
""",
    ),
    pluginRuleTest(
        "bad_indented_code_block_starts_with_space_with_fenced",
        source_file_contents="""    abc
     def
""",
        set_args=["plugins.md046.style=fenced"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD046: Code block style [Expected: fenced; Actual: indented] (code-block-style)
""",
        fix_expected_file_contents="""```
abc
 def
```
""",
    ),
    # An empty fenced code block gets translated into 4 spaces, which is not a proper indented code block.
    pluginRuleTest(
        "bad_fenced_code_empty_with_indented",
        source_file_contents="""```Markdown
```
""",
        set_args=["plugins.md046.style=indented"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD046: Code block style [Expected: indented; Actual: fenced] (code-block-style)
""",
        fix_expected_file_contents="",
    ),
    # An empty indented code block is not a code block, hence it is not treated as one.
    pluginRuleTest(
        "bad_indented_code_empty_with_fecned",
        source_file_contents="""\a\a\a\a
""".replace(
            "\a", " "
        ),
        set_args=["plugins.md046.style=fenced"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD009: Trailing spaces [Expected: 0 or 2; Actual: 4] (no-trailing-spaces)
{temp_source_path}:2:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)
""",
    ),
    pluginRuleTest(
        "bad_fenced_code_inconsistent_indent_with_indented",
        source_file_contents="""   ```lang
aaa
  ```
""",
        set_args=["plugins.md046.style=indented"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD046: Code block style [Expected: indented; Actual: fenced] (code-block-style)
""",
        fix_expected_file_contents="""    aaa
""",
    ),
    pluginRuleTest(
        "bad_fenced_code_spaces_and_blank_lines_with_indented",
        source_file_contents="""```lang
\a\a
abc

def
```
""".replace(
            "\a", " "
        ),
        set_args=["plugins.md046.style=indented"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD046: Code block style [Expected: indented; Actual: fenced] (code-block-style)
""",
        fix_expected_file_contents="""\a\a\a\a\a\a
    abc
\a\a\a\a
    def
""".replace(
            "\a", " "
        ),
    ),
    pluginRuleTest(
        "bad_fenced_code_paragraph_before_and_after_with_indented",
        source_file_contents="""abc
```lang
def
```
ghi
""".replace(
            "\a", " "
        ),
        set_args=["plugins.md046.style=indented"],
        disable_rules="md031",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD046: Code block style [Expected: indented; Actual: fenced] (code-block-style)
""",
        fix_expected_file_contents="""abc

    def
ghi
""",
    ),
    pluginRuleTest(
        "mix_md046_md048",
        source_file_contents="""```Markdown
# fred
```

~~~Markdown
# fred
~~~
""",
        set_args=["plugins.md046.style=indented"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:1: MD046: Code block style [Expected: indented; Actual: fenced] (code-block-style)
{temp_source_path}:5:1: MD046: Code block style [Expected: indented; Actual: fenced] (code-block-style)
{temp_source_path}:5:1: MD048: Code fence style [Expected: backtick; Actual: tilde] (code-fence-style)
""",
        fix_expected_file_contents="""    # fred

    # fred
""",
    ),
    pluginRuleTest(
        "mix_md048_md046",
        source_file_contents="""~~~Markdown
# fred
~~~

    # fred
""",
        set_args=["plugins.md046.style=fenced"],
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD046: Code block style [Expected: fenced; Actual: indented] (code-block-style)
""",
        fix_expected_file_contents="""~~~Markdown
# fred
~~~

~~~
# fred
~~~
""",
    ),
]

fixTests = []
for i in scanTests:
    if i.fix_expected_file_contents is not None:
        fixTests.append(i)


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md046_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md046")


@pytest.mark.parametrize("test", fixTests, ids=id_test_plug_rule_fn)
def test_md046_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md046_config(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(
        test,
        file_contents="""this is a paragraph without any capitalization errors
""",
    )


def test_md046_query_config():
    config_test = pluginQueryConfigTest(
        "md046",
        """
  ITEM               DESCRIPTION

  Id                 md046
  Name(s)            code-block-style
  Short Description  Code block style
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md046.md


  CONFIGURATION ITEM  TYPE    VALUE

  style               string  "consistent"

""",
    )
    execute_query_configuration_test(config_test)
