"""
Module to provide tests related to the MD031 rule.
"""

import os
from test.rules.utils import (
    calculate_fix_tests,
    calculate_scan_tests,
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

source_path = os.path.join("test", "resources", "rules", "md031") + os.sep

configTests = [
    pluginConfigErrorTest(
        "bad_configuration_list_items",
        use_strict_config=True,
        set_args=["plugins.md031.list_items=bad"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md031.list_items' must be of type 'bool'.""",
    ),
]

skip_fix_bad_markdown = True

scanTests = [
    pluginRuleTest(
        "good_both_fenced_with_consistent",
        source_file_contents="""This is text and a blank line.

```block
A code block
```

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_after",
        source_file_contents="""This is text and no blank line.
```block
A code block
```

This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""This is text and no blank line.

```block
A code block
```

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_after_with_fix_debug",
        source_file_contents="""This is text and no blank line.
```block
A code block
```

This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        use_fix_debug=True,
        fix_expected_output="""md009-before:This is text and no blank line.:
md010-before:This is text and no blank line.:
md047-before:This is text and no blank line.:
nl-ltw:This is text and no blank line.\\n:
md009-before:```block:
md010-before:```block:
md047-before:```block:
nl-ltw:```block\\n:
md009-before:A code block:
md010-before:A code block:
md047-before:A code block:
nl-ltw:A code block\\n:
md009-before:```:
md010-before:```:
md047-before:```:
nl-ltw:```\\n:
md009-before::
md010-before::
md047-before::
nl-ltw:\\n:
md009-before:This is a blank line and some text.:
md010-before:This is a blank line and some text.:
md047-before:This is a blank line and some text.:
nl-ltw:This is a blank line and some text.\\n:
md009-before::
md010-before::
md047-before::
was_newline_added_at_end_of_file=True
fixed:This is a blank line and some text.\\n:
is_line_empty=True
was_modified=True
nl-ltw::
--
--
TOKENS-----
 00:[para(1,1):]
 01:[text(1,1):This is text and no blank line.:]
 02:[end-para:::False]
 03:[fcode-block(2,1):`:3:block:::::]
 04:[text(3,1):A code block:]
 05:[end-fcode-block:::3:False]
 06:[BLANK(5,1):]
 07:[para(6,1):]
 08:[text(6,1):This is a blank line and some text.:]
 09:[end-para:::True]
 10:[BLANK(7,1):]
 11:[end-of-stream(8,0)]
TOKENS-----
 ReplaceTokensRecord(plugin_id='MD031', start_token='[fcode-block(2,1):`:3:block:::::]', end_token='[fcode-block(2,1):`:3:block:::::]', replacement_tokens=['[BLANK(2,0):]', '[fcode-block(3,1):`:3:block:::::]'])
TOKENS-----
 00:[para(1,1):]
 01:[text(1,1):This is text and no blank line.:]
 02:[end-para:::False]
 03:[BLANK(2,0):]
 04:[fcode-block(3,1):`:3:block:::::]
 05:[text(4,1):A code block:]
 06:[end-fcode-block:::3:False]
 07:[BLANK(6,1):]
 08:[para(7,1):]
 09:[text(7,1):This is a blank line and some text.:]
 10:[end-para:::True]
 11:[BLANK(8,1):]
 12:[end-of-stream(9,0)]
TOKENS-----
--
MARKDOWN:This is text and no blank line.\\n\\n```block\\nA code block\\n```\\n\\nThis is a blank line and some text.\\n
nl-ltw:This is text and no blank line.\\n:
nl-ltw:\\n:
nl-ltw:```block\\n:
nl-ltw:A code block\\n:
nl-ltw:```\\n:
nl-ltw:\\n:
nl-ltw:This is a blank line and some text.\\n:
was_newline_added_at_end_of_file=True
fixed:This is a blank line and some text.\\n:
is_line_empty=True
was_modified=True
nl-ltw::
Fixed: {temp_source_path}""",
        fix_expected_file_contents="""This is text and no blank line.

```block
A code block
```

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_after_with_thematics",
        source_file_contents="""This is text and no blank line.
----
```block
A code block
```

---
This is a blank line and some text.
""",
        scan_expected_return_code=1,
        disable_rules="md022,md026",
        scan_expected_output="""{temp_source_path}:3:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""This is text and no blank line.
----

```block
A code block
```

---
This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_before",
        source_file_contents="""This is text and a blank line.

```block
A code block
```
This is no blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""This is text and a blank line.

```block
A code block
```

This is no blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_before_with_thematics",
        source_file_contents="""This is text and a blank line.
---

```block
A code block
```
---
This is no blank line and some text.
""",
        scan_expected_return_code=1,
        disable_rules="md026",
        scan_expected_output="""{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""This is text and a blank line.
---

```block
A code block
```

---
This is no blank line and some text.
""",
    ),
    pluginRuleTest(
        "good_fenced_block_at_start",
        source_file_contents="""```block
A code block
```

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "good_fenced_block_at_end",
        source_file_contents="""This is text and a blank line.

```block
A code block
```""",
        disable_rules="md047",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_after_start_indent",
        source_file_contents="""This is text and no blank line.
 ```block
A code block
```

This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:2: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""This is text and no blank line.

 ```block
A code block
```

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_before_start_indent",
        source_file_contents="""This is text and a blank line.

 ```block
A code block
```
This is no blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""This is text and a blank line.

 ```block
A code block
```

This is no blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_before_end_indent",
        source_file_contents="""This is text and a blank line.

```block
A code block
 ```
This is no blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:2: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""This is text and a blank line.

```block
A code block
 ```

This is no blank line and some text.
""",
    ),
    pluginRuleTest(
        "good_fenced_block_surrounded_in_block_quote",
        source_file_contents="""This is text and a blank line.

>```block
>A code block
>```

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "good_fenced_block_surrounded_in_ordered_list",
        source_file_contents="""This is text and a blank line.

1. ```block
   A code block
   ```

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "good_fenced_block_surrounded_in_unordered_list",
        source_file_contents="""This is text and a blank line.

- ```block
  A code block
  ```

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_after_in_block_quote",
        source_file_contents="""> This is text and no blank line.
> ```block
> A code block
> ```
>
>This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> This is text and no blank line.
>
> ```block
> A code block
> ```
>
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_after_in_block_quote_with_thematics",
        source_file_contents="""> This is text and no blank line.
> ___
> ```block
> A code block
> ```
>
> ___
>This is a blank line and some text.
""",
        disable_rules="md022,md026",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> This is text and no blank line.
> ___
>
> ```block
> A code block
> ```
>
> ___
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_after_in_block_quote_with_setext",
        source_file_contents="""> This is text and no blank line.
> ---
> ```block
> A code block
> ```
>
> ---
>This is a blank line and some text.
""",
        disable_rules="md022,md026",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> This is text and no blank line.
> ---
>
> ```block
> A code block
> ```
>
> ---
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_before_in_block_quote",
        source_file_contents="""> This is text and no blank line.
>
> ```block
> A code block
> ```
>This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> This is text and no blank line.
>
> ```block
> A code block
> ```
>
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_before_in_block_quote_with_thematics",
        source_file_contents="""> This is text and no blank line.
> ___
>
> ```block
> A code block
> ```
> ___
>This is a blank line and some text.
""",
        disable_rules="md026",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> This is text and no blank line.
> ___
>
> ```block
> A code block
> ```
>
> ___
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_before_in_block_quote_with_setext",
        source_file_contents="""> This is text and no blank line.
> ---
>
> ```block
> A code block
> ```
> ---
>This is a blank line and some text.
""",
        disable_rules="md026",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> This is text and no blank line.
> ---
>
> ```block
> A code block
> ```
>
> ---
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote",
        source_file_contents="""> This is text and no blank line.
> ```block
> A code block
> ```
>This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> This is text and no blank line.
>
> ```block
> A code block
> ```
>
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_thematics",
        source_file_contents="""> This is text and no blank line.
> ****
> ```block
> A code block
> ```
> ****
>This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> This is text and no blank line.
> ****
>
> ```block
> A code block
> ```
>
> ****
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_setext",
        source_file_contents="""> This is text and no blank line.
> ---
> ```block
> A code block
> ```
> ---
>This is a blank line and some text.
""",
        disable_rules="md022,md026",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> This is text and no blank line.
> ---
>
> ```block
> A code block
> ```
>
> ---
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_empty",
        source_file_contents="""> This is text and no blank line.
> ****
> ```block
> ```
> ****
>This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> This is text and no blank line.
> ****
>
> ```block
> ```
>
> ****
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_bare",
        source_file_contents="""> This is text and no blank line.
> ```block
> A code block
> ```
>This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> This is text and no blank line.
>
> ```block
> A code block
> ```
>
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_block",
        source_file_contents="""> > inner block
> > inner block
> ```block
> A code block
> ```
> This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> > inner block
> > inner block
>
> ```block
> A code block
> ```
>
> This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_block_double_drop",
        source_file_contents="""> > inner block
> > inner block
```block
A code block
```
This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> > inner block
> > inner block

```block
A code block
```

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_block_with_text",
        source_file_contents="""> > inner block
> > inner block
>
> This is text and no blank line.
> ```block
> A code block
> ```
>This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> > inner block
> > inner block
>
> This is text and no blank line.
>
> ```block
> A code block
> ```
>
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_block_with_thematics",
        source_file_contents="""> > inner block
> > inner block
> ___
> ```block
> A code block
> ```
> ___
>This is a blank line and some text.
""",
        disable_rules="md022,md026",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> > inner block
> > inner block
> ___
>
> ```block
> A code block
> ```
>
> ___
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_block_double_drop_with_thematics",
        source_file_contents="""> > inner block
> > inner block
___
```block
A code block
```
___
This is a blank line and some text.
""",
        disable_rules="md022,md026",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> > inner block
> > inner block
___

```block
A code block
```

___
This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_block_with_setext",
        source_file_contents="""> > inner block
> > inner block
>
> This is text and no blank line.
> ---
> ```block
> A code block
> ```
> ---
>This is a blank line and some text.
""",
        disable_rules="md022,md026",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> > inner block
> > inner block
>
> This is text and no blank line.
> ---
>
> ```block
> A code block
> ```
>
> ---
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_list",
        source_file_contents="""> + inner list
> + inner list
> ```block
> A code block
> ```
> This is a blank line and some text.
""",
        disable_rules="md032",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> + inner list
> + inner list
>
> ```block
> A code block
> ```
>
> This is a blank line and some text.
""",
    ),
    pluginRuleTest(  # BAD FIX EXPECTED
        "bad_fenced_block_in_block_quote_with_previous_inner_list_double_drop",
        source_file_contents="""> + inner list
> + inner list
```block
A code block
```
This is a blank line and some text.
""",
        disable_rules="md032",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> + inner list
> + inner list

```block
A code block
```

This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_list_with_text",
        source_file_contents="""> + inner list
> + inner list
>
> This is text and no blank line.
> ```block
> A code block
> ```
>This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> + inner list
> + inner list
>
> This is text and no blank line.
>
> ```block
> A code block
> ```
>
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_list_with_thematics",
        source_file_contents="""> + inner list
> + inner list
> ___
> ```block
> A code block
> ```
> ___
>This is a blank line and some text.
""",
        disable_rules="md022,md026,md032",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> + inner list
> + inner list
> ___
>
> ```block
> A code block
> ```
>
> ___
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_list_double_drop_with_thematics",
        source_file_contents="""> + inner list
> + inner list
___
```block
A code block
```
___
This is a blank line and some text.
""",
        disable_rules="md022,md026,md032",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> + inner list
> + inner list
___

```block
A code block
```

___
This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_list_with_setext",
        source_file_contents="""> + inner list
> + inner list
>
> This is text and no blank line.
> ---
> ```block
> A code block
> ```
> ---
>This is a blank line and some text.
""",
        disable_rules="md022,md026",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> + inner list
> + inner list
>
> This is text and no blank line.
> ---
>
> ```block
> A code block
> ```
>
> ---
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_block_and_para_continue",
        source_file_contents="""> > inner block
> > inner block
> This is text and no blank line.
> ```block
> A code block
> ```
> This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> > inner block
> > inner block
> This is text and no blank line.
>
> ```block
> A code block
> ```
>
> This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_block_and_para_continue_and_thematics",
        source_file_contents="""> > inner block
> > inner block
> This is text and no blank line.
> ---
> ```block
> A code block
> ```
> ---
> This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> > inner block
> > inner block
> This is text and no blank line.
> ---
>
> ```block
> A code block
> ```
>
> ---
> This is a blank line and some text.
""",
    ),
    pluginRuleTest(  # test_extra_047f6 test_extra_047f6d https://github.com/jackdewinter/pymarkdown/issues/1213
        "bad_fenced_block_in_block_quote_with_previous_inner_blocks",
        source_file_contents="""> > inner block
> > > innermost block
> > > innermost block
> > _____
> > inner block
> ```block
> A code block
> ```
>This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> > inner block
> > > innermost block
> > > innermost block
> > _____
> > inner block
>
> ```block
> A code block
> ```
>
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_with_previous_inner_blocks_with_text",
        source_file_contents="""> > inner block
> > > innermost block
> > > innermost block
> > inner block
>
> This is text and no blank line.
> ```block
> A code block
> ```
>This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> > inner block
> > > innermost block
> > > innermost block
> > inner block
>
> This is text and no blank line.
>
> ```block
> A code block
> ```
>
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(  # test_extra_047f6b test_extra_047f6c
        "bad_fenced_block_in_block_quote_with_previous_inner_blocks_with_thematics",
        source_file_contents="""> > inner block
> > > innermost block
> > > innermost block
> > inner block
> ___
> ```block
> A code block
> ```
> ___
>This is a blank line and some text.
""",
        disable_rules="md022,md026",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> > inner block
> > > innermost block
> > > innermost block
> > inner block
> ___
>
> ```block
> A code block
> ```
>
> ___
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(  # test_extra_047f3
        "bad_fenced_block_in_block_quote_with_previous_inner_blocks_with_setext",
        source_file_contents="""> > inner block
> > > innermost block
> > > innermost block
> > inner block
>
> This is text and no blank line.
> ---
> ```block
> A code block
> ```
> ---
>This is a blank line and some text.
""",
        disable_rules="md022,md026",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:10:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> > inner block
> > > innermost block
> > > innermost block
> > inner block
>
> This is text and no blank line.
> ---
>
> ```block
> A code block
> ```
>
> ---
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_only_after",
        source_file_contents="""> This is text and no blank line.
>
> some paragraph
> ```block
> A good code block
> ```
>
>This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> This is text and no blank line.
>
> some paragraph
>
> ```block
> A good code block
> ```
>
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_only_after_thematics",
        source_file_contents="""> This is text and no blank line.
>
> some paragraph
> ---
> ```block
> A good code block
> ```
>
> ---
>This is a blank line and some text.
""",
        disable_rules="md022",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> This is text and no blank line.
>
> some paragraph
> ---
>
> ```block
> A good code block
> ```
>
> ---
>This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_after_in_unordered_list",
        source_file_contents="""- This is text and no blank line.
  ```block
  A code block
  ```

  This is a blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""- This is text and no blank line.

  ```block
  A code block
  ```

  This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_after_in_unordered_list_with_thematics",
        source_file_contents="""- This is text and no blank line.
  ---
  ```block
  A code block
  ```

  ---
  This is a blank line and some text.
""",
        disable_rules="md022,md026",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""- This is text and no blank line.
  ---

  ```block
  A code block
  ```

  ---
  This is a blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_before_in_unordered_list",
        source_file_contents="""- This is text and a blank line.

  ```block
  A code block
  ```
  This is no blank line and some text.
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""- This is text and a blank line.

  ```block
  A code block
  ```

  This is no blank line and some text.
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_only_before_in_unordered_list_with_thematics",
        source_file_contents="""- This is text and a blank line.
  --

  ```block
  A code block
  ```
  --
  This is no blank line and some text.
""",
        disable_rules="md026",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""- This is text and a blank line.
  --

  ```block
  A code block
  ```

  --
  This is no blank line and some text.
""",
    ),
    pluginRuleTest(
        "good_fenced_block_only_after_in_unordered_list_with_config",
        source_file_contents="""- This is text and no blank line.
  ```block
  A code block
  ```
  
  This is a blank line and some text.
""",
        set_args=["plugins.md031.list_items=$!False"],
        use_strict_config=True,
    ),
    pluginRuleTest(
        "good_fenced_block_only_before_in_unordered_list_with_config",
        source_file_contents="""- This is text and a blank line.

  ```block
  A code block
  ```
  This is no blank line and some text.
""",
        set_args=["plugins.md031.list_items=$!False"],
        use_strict_config=True,
    ),
    pluginRuleTest(
        "good_fenced_block_empty",
        source_file_contents="""This is text and a blank line.

```block
```

This is a blank line and some text.
""",
        set_args=["plugins.md031.list_items=$!False"],
        use_strict_config=True,
    ),
    pluginRuleTest(  # test_extra_046x0 # test_extra_046x1
        "bad_fenced_block_surrounded_by_block_quote",
        source_file_contents="""> block quote
```block
A code block
```
> block quote
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> block quote

```block
A code block
```

> block quote
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_surrounded_by_block_quote_with_thematics",
        source_file_contents="""> block quote
---
```block
A code block
```
---
> block quote
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> block quote
---

```block
A code block
```

---
> block quote
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_surrounded_by_block_quote_with_setext",
        source_file_contents="""> block quote

abc
---
```block
A code block
```
abc
---
> block quote
""",
        disable_rules="md022,md024",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        fix_expected_file_contents="""> block quote

abc
---

```block
A code block
```

abc
---
> block quote
""",
    ),
    pluginRuleTest(  # test_extra_046w0a test_extra_046w1
        "bad_fenced_block_surrounded_by_list",
        source_file_contents="""+ list
```block
A code block
```
1. another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list

```block
A code block
```

1. another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_surrounded_by_list_with_thematics",
        source_file_contents="""+ list
---
```block
A code block
```
---
1. another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list
---

```block
A code block
```

---
1. another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_surrounded_by_list_with_setext",
        source_file_contents="""+ list

abc
---
```block
A code block
```
abc
---
1. another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""+ list

abc
---

```block
A code block
```

abc
---
1. another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list",
        source_file_contents="""+ list
  ```block
  A code block
  ```
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list

  ```block
  A code block
  ```

+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_thematics",
        source_file_contents="""+ list
  ***
  ```block
  A code block
  ```
  ***
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list
  ***

  ```block
  A code block
  ```

  ***
+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_empty",
        source_file_contents="""+ list
  *****
  ```block
  ```
  *****
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list
  *****

  ```block
  ```

  *****
+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_bare_fenced",
        source_file_contents="""+ list
  ```block
  A code block
  ```
  list
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list

  ```block
  A code block
  ```

  list
+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_block",
        source_file_contents="""+ list
  > inner list
  > couple of lines
  ```block
  A code block
  ```
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list
  > inner list
  > couple of lines

  ```block
  A code block
  ```

+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_block_double_drop",
        source_file_contents="""+ list
  > inner list
  > couple of lines
```block
A code block
```
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list
  > inner list
  > couple of lines

```block
A code block
```

another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_block_with_thematics",
        source_file_contents="""+ list
  > inner list
  > couple of lines
  -----
  ```block
  A code block
  ```
  -----
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list
  > inner list
  > couple of lines
  -----

  ```block
  A code block
  ```

  -----
+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_block_double_drop_with_thematics",
        source_file_contents="""+ list
  > inner list
  > couple of lines
-----
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list
  > inner list
  > couple of lines
-----

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_block_with_setext",
        source_file_contents="""+ list
  > inner list
  > couple of lines
  
  abc
  -----
  ```block
  A code block
  ```
  abc
  -----
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""+ list
  > inner list
  > couple of lines
  
  abc
  -----

  ```block
  A code block
  ```

  abc
  -----
+ another list
""",
    ),
    pluginRuleTest(  # test_extra_047b0 test_extra_047b1
        "bad_fenced_block_in_list_with_previous_inner_list",
        source_file_contents="""+ list
  + inner list
    couple of lines
  ```block
  A code block
  ```
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list
  + inner list
    couple of lines

  ```block
  A code block
  ```

+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_list_double_drop",
        source_file_contents="""+ list
  + inner list
    couple of lines
```block
A code block
```
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list
  + inner list
    couple of lines

```block
A code block
```

another list
""",
    ),
    pluginRuleTest(  # test_extra_047c0 test_extra_047c1
        "bad_fenced_block_in_list_with_previous_inner_list_with_thematics",
        source_file_contents="""+ list
  + inner list
    couple of lines
  -----
  ```block
  A code block
  ```
  -----
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list
  + inner list
    couple of lines
  -----

  ```block
  A code block
  ```

  -----
+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_list_double_drop_with_thematics",
        source_file_contents="""+ list
  + inner list
    couple of lines
-----
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list
  + inner list
    couple of lines
-----

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_list_with_setext",
        source_file_contents="""+ list
  + inner list
  couple of lines
  -----
  ```block
  A code block
  ```
  couple of lines
  -----
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022",
        fix_expected_file_contents="""+ list
  + inner list
  couple of lines
  -----

  ```block
  A code block
  ```

  couple of lines
  -----
+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_list_and_para_continue",
        source_file_contents="""+ list
  + inner list
    couple of lines
  continued line
  ```block
  A code block
  ```
  -----
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list
  + inner list
    couple of lines
  continued line

  ```block
  A code block
  ```

  -----
+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_list_and_para_continue_and_thematics",
        source_file_contents="""+ list
  + inner list
    couple of lines
  continued line
  -----
  ```block
  A code block
  ```
  -----
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ list
  + inner list
    couple of lines
  continued line
  -----

  ```block
  A code block
  ```

  -----
+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_list_and_para_continue_and_setext",
        source_file_contents="""+ list
  + inner list
    couple of lines

  continued line
  -----
  ```block
  A code block
  ```
  continued line
  -----
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""+ list
  + inner list
    couple of lines

  continued line
  -----

  ```block
  A code block
  ```

  continued line
  -----
+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_lists",
        source_file_contents="""+ list
    + innermost list
    + innermost list
  + inner list
    couple of lines
  original list
  ```block
  A code block
  ```
  list
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md007,md005",
        fix_expected_file_contents="""+ list
    + innermost list
    + innermost list
  + inner list
    couple of lines
  original list

  ```block
  A code block
  ```

  list
+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_lists_and_thematics",
        source_file_contents="""+ list
    + innermost list
    + innermost list
  + inner list
    couple of lines
  original list
  ---
  ```block
  A code block
  ```
  ---
  list
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:10:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md007,md005",
        fix_expected_file_contents="""+ list
    + innermost list
    + innermost list
  + inner list
    couple of lines
  original list
  ---

  ```block
  A code block
  ```

  ---
  list
+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_with_previous_inner_lists_and_setext",
        source_file_contents="""+ list
    + innermost list
    + innermost list
  + inner list
    couple of lines

  original list
  ---
  ```block
  A code block
  ```
  original list
  ---
  list
+ another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:9:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:11:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md007,md005,md022,md024",
        fix_expected_file_contents="""+ list
    + innermost list
    + innermost list
  + inner list
    couple of lines

  original list
  ---

  ```block
  A code block
  ```

  original list
  ---
  list
+ another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote",
        source_file_contents="""> > --------
> > ```block
> > A code block
> > ```
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > --------
> >
> > ```block
> > A code block
> > ```
> >
> > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_double_drop",
        source_file_contents="""> > --------
```block
A code block
```
--------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > --------

```block
A code block
```

--------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_empty",
        source_file_contents="""> > --------
> > ```block
> > ```
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:3:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > --------
> >
> > ```block
> > ```
> >
> > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_bare_fenced",
        source_file_contents="""> > some text
> > ```block
> > A code block
> > ```
> > some other text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > some text
> >
> > ```block
> > A code block
> > ```
> >
> > some other text
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_block",
        source_file_contents="""> > > block 3
> > > block 3
> > > block 3
> > ```block
> > A code block
> > ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > > block 3
> > > block 3
> > > block 3
> >
> > ```block
> > A code block
> > ```
""",
    ),
    pluginRuleTest(  # test_extra_050g0 test_extra_050g1
        "bad_fenced_block_in_block_quote_in_block_quote_double_drop_with_previous_inner_block",
        source_file_contents="""> > > block 3
> > > block 3
> > > block 3
> ```block
> A code block
> ```
> text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md027",
        fix_expected_file_contents="""> > > block 3
> > > block 3
> > > block 3
>
> ```block
> A code block
> ```
>
> text
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_triple_drop_with_previous_inner_block",
        source_file_contents="""> > > block 3
> > > block 3
> > > block 3
```block
A code block
```
text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > > block 3
> > > block 3
> > > block 3

```block
A code block
```

text
""",
    ),
    pluginRuleTest(  # test_extra_044x test_extra_044a
        "bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_block_with_thematics",
        source_file_contents="""> > > block 3
> > > block 3
> > > block 3
> > --------
> > ```block
> > A code block
> > ```
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > > block 3
> > > block 3
> > > block 3
> > --------
> >
> > ```block
> > A code block
> > ```
> >
> > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_block_double_drop_with_thematics",
        source_file_contents="""> > > block 3
> > > block 3
> > > block 3
> --------
> ```block
> A code block
> ```
> --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > > block 3
> > > block 3
> > > block 3
> --------
>
> ```block
> A code block
> ```
>
> --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_block_triple_drop_with_thematics",
        source_file_contents="""> > > block 3
> > > block 3
> > > block 3
--------
```block
A code block
```
--------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > > block 3
> > > block 3
> > > block 3
--------

```block
A code block
```

--------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_block_with_setext",
        source_file_contents="""> > > block 3
> > > block 3
> > > block 3
> >
> > abc
> > --------
> > ```block
> > A code block
> > ```
> > abc
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""> > > block 3
> > > block 3
> > > block 3
> >
> > abc
> > --------
> >
> > ```block
> > A code block
> > ```
> >
> > abc
> > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_block_and_para_continue",
        source_file_contents="""> > > block 3
> > > block 3
> > block 3
> > ```block
> > A code block
> > ```
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > > block 3
> > > block 3
> > block 3
> >
> > ```block
> > A code block
> > ```
> >
> > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_block_and_para_continue_and_thematics",
        source_file_contents="""> > > block 3
> > > block 3
> > --------
> > ```block
> > A code block
> > ```
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > > block 3
> > > block 3
> > --------
> >
> > ```block
> > A code block
> > ```
> >
> > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_block_and_para_continue_and_setext",
        source_file_contents="""> > > block 3
> > > block 3
> >
> > abc
> > --------
> > ```block
> > A code block
> > ```
> > abc
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""> > > block 3
> > > block 3
> >
> > abc
> > --------
> >
> > ```block
> > A code block
> > ```
> >
> > abc
> > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_list",
        source_file_contents="""> > + block 3
> >   block 3
> > + block 3
> > ```block
> > A code block
> > ```
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > + block 3
> >   block 3
> > + block 3
> >
> > ```block
> > A code block
> > ```
> >
> > --------
""",
    ),
    pluginRuleTest(  # test_extra_049l0 test_extra_050h0 test_extra_050h1
        "bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_list_double_drop",
        source_file_contents="""> > + block 3
> >   block 3
> > + block 3
> ```block
> A code block
> ```
> --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > + block 3
> >   block 3
> > + block 3
>
> ```block
> A code block
> ```
>
> --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_list_triple_drop",
        source_file_contents="""> > + block 3
> >   block 3
> > + block 3
```block
A code block
```
--------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > + block 3
> >   block 3
> > + block 3

```block
A code block
```

--------
""",
    ),
    pluginRuleTest(  # test_extra_044lx test_nested_three_block_block_unordered_drop_list_after_new_list_and_text_with_thematic_and_fenced_with_blanks
        "bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_list_with_thematics",
        source_file_contents="""> > + block 3
> >   block 3
> > + block 3
> > --------
> > ```block
> > A code block
> > ```
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > + block 3
> >   block 3
> > + block 3
> > --------
> >
> > ```block
> > A code block
> > ```
> >
> > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_list_with_setext",
        source_file_contents="""> > + block 3
> >   block 3
> > + block 3
> >
> > abc
> > --------
> > ```block
> > A code block
> > ```
> > abc
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""> > + block 3
> >   block 3
> > + block 3
> >
> > abc
> > --------
> >
> > ```block
> > A code block
> > ```
> >
> > abc
> > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote",
        source_file_contents="""> > > --------
> > > ```block
> > > A code block
> > > ```
> > > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > > --------
> > >
> > > ```block
> > > A code block
> > > ```
> > >
> > > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_empty",
        source_file_contents="""> > > --------
> > > ```block
> > > ```
> > > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:3:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > > --------
> > >
> > > ```block
> > > ```
> > >
> > > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block",
        source_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
> > > ```block
> > > A code block
> > > ```
> > > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
> > >
> > > ```block
> > > A code block
> > > ```
> > >
> > > --------
""",
    ),
    pluginRuleTest(  # test_extra_052a0 test_extra_052a1
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_double_drop",
        source_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
> > ```block
> > A code block
> > ```
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md027",
        fix_expected_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
> >
> > ```block
> > A code block
> > ```
> >
> > --------
""",
    ),
    pluginRuleTest(  # test_extra_051h0 test_extra_051h1
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_triple_drop",
        source_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
> ```block
> A code block
> ```
> --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md027",
        use_debug=True,
        fix_expected_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
>
> ```block
> A code block
> ```
>
> --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_quad_drop",
        source_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
```block
A code block
```
--------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2

```block
A code block
```

--------
""",
    ),
    pluginRuleTest(  # test_extra_044ma
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_with_thematics",
        source_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
> > > --------
> > > ```block
> > > A code block
> > > ```
> > > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
> > > --------
> > >
> > > ```block
> > > A code block
> > > ```
> > >
> > > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_double_drop_with_thematics",
        source_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
> > --------
> > ```block
> > A code block
> > ```
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
> > --------
> >
> > ```block
> > A code block
> > ```
> >
> > --------
""",
    ),
    pluginRuleTest(  # test_extra_051j0
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_triple_drop_with_thematics",
        source_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
> --------
> ```block
> A code block
> ```
> --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
> --------
>
> ```block
> A code block
> ```
>
> --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_quad_drop_with_thematics",
        source_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
--------
```block
A code block
```
--------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
--------

```block
A code block
```

--------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_with_setext",
        source_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
> > >
> > > abc
> > > --------
> > > ```block
> > > A code block
> > > ```
> > > abc
> > > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""> > >
> > > > fourth block 1
> > > > fourth block 2
> > >
> > > abc
> > > --------
> > >
> > > ```block
> > > A code block
> > > ```
> > >
> > > abc
> > > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_list",
        source_file_contents="""> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> > > ```block
> > > A code block
> > > ```
> > > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> > >
> > > ```block
> > > A code block
> > > ```
> > >
> > > --------
""",
    ),
    pluginRuleTest(  # test_extra_049l1
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_list_double_drop",
        source_file_contents="""> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> > ```block
> > A code block
> > ```
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> >
> > ```block
> > A code block
> > ```
> >
> > --------
""",
    ),
    pluginRuleTest(  # test_extra_049l2a test_extra_049l2b
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_list_triple_drop",
        source_file_contents="""> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> ```block
> A code block
> ```
> --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md027",
        use_debug=True,
        fix_expected_file_contents="""> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
>
> ```block
> A code block
> ```
>
> --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_list_quad_drop",
        source_file_contents="""> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
```block
A code block
```
--------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3

```block
A code block
```

--------
""",
    ),
    pluginRuleTest(  # test_extra_044mcy0
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_list_with_thematics",
        source_file_contents="""> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> > > --------
> > > ```block
> > > A code block
> > > ```
> > > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> > > --------
> > >
> > > ```block
> > > A code block
> > > ```
> > >
> > > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_list_with_setext",
        source_file_contents="""> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> > >
> > > abc
> > > --------
> > > ```block
> > > A code block
> > > ```
> > > abc
> > > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:10:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> > >
> > > abc
> > > --------
> > >
> > > ```block
> > > A code block
> > > ```
> > >
> > > abc
> > > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_block_quote",
        source_file_contents="""> > + --------
> >   ```block
> >   A code block
> >   ```
> >   --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > + --------
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_empty",
        source_file_contents="""> > + --------
> >   ```block
> >   ```
> >   --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:3:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > + --------
> >
> >   ```block
> >   ```
> >
> >   --------
""",
    ),
    pluginRuleTest(  # test_extra_046v0 test_extra_046v1
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block",
        source_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> >   ```block
> >   A code block
> >   ```
> >   --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        use_debug=True,
        fix_expected_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_double_drop",
        source_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> > ```block
> > A code block
> > ```
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md027",
        use_debug=True,
        fix_expected_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> >
> > ```block
> > A code block
> > ```
> >
> > --------
""",
    ),
    pluginRuleTest(  # test_extra_049b0
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_triple_drop",
        source_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> ```block
> A code block
> ```
> --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > + --------
> >   > block 1
> >   > block 2
>
> ```block
> A code block
> ```
>
> --------
""",
    ),
    pluginRuleTest(  # test_extra_049c0
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_quad_drop",
        source_file_contents="""> > + --------
> >   > block 1
> >   > block 2
```block
A code block
```
--------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > + --------
> >   > block 1
> >   > block 2

```block
A code block
```

--------
""",
    ),
    pluginRuleTest(  # test_extra_047h0 test_extra_047h1
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_with_thematics",
        source_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> >   --------
> >   ```block
> >   A code block
> >   ```
> >   --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> >   --------
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_double_drop_with_thematics",
        source_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> > --------
> > ```block
> > A code block
> > ```
> > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> > --------
> >
> > ```block
> > A code block
> > ```
> >
> > --------
""",
    ),
    pluginRuleTest(  # test_extra_049b1a
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_triple_drop_with_thematics",
        source_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> --------
> ```block
> A code block
> ```
> --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> --------
>
> ```block
> A code block
> ```
>
> --------
""",
    ),
    pluginRuleTest(  # test_extra_049c1
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_quad_drop_with_thematics",
        source_file_contents="""> > + --------
> >   > block 1
> >   > block 2
--------
```block
A code block
```
--------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> > + --------
> >   > block 1
> >   > block 2
--------

```block
A code block
```

--------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_with_setext",
        source_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> >
> >   abc
> >   --------
> >   ```block
> >   A code block
> >   ```
> >   abc
> >   --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""> > + --------
> >   > block 1
> >   > block 2
> >
> >   abc
> >   --------
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   abc
> >   --------
""",
    ),
    pluginRuleTest(  # test_extra_046u0 test_extra_046u1
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list",
        source_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >   ```block
> >   A code block
> >   ```
> >   ______
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md035",
        fix_expected_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   ______
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_double_drop",
        source_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> > ```block
> > A code block
> > ```
> > ______
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md035",
        fix_expected_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >
> > ```block
> > A code block
> > ```
> >
> > ______
""",
    ),
    pluginRuleTest(  # test_extra_049l3a test_extra_049l3b
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_triple_drop",
        source_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> ```block
> A code block
> ```
> ______
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md035",
        fix_expected_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
>
> ```block
> A code block
> ```
>
> ______
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_quad_drop",
        source_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
```block
A code block
```
______
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md035",
        fix_expected_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3

```block
A code block
```

______
""",
    ),
    pluginRuleTest(  # test_extra_044lex1 test_extra_044lex1a
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_and_thematics",
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
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md035",
        fix_expected_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >   ______
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   ______
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_double_drop_and_thematics",
        source_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> > ______
> > ```block
> > A code block
> > ```
> > ______
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md035",
        fix_expected_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> > ______
> >
> > ```block
> > A code block
> > ```
> >
> > ______
""",
    ),
    pluginRuleTest(  # test_extra_052d0 test_extra_052d1 FOOBAR1
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_triple_drop_and_thematics",
        source_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> ______
> ```block
> A code block
> ```
> ______
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md035",
        use_fix_debug=True,
        mark_fix_as_skipped=skip_fix_bad_markdown,
        fix_expected_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> ______
>
> ```block
> A code block
> ```
>
> ______
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_quad_drop_and_thematics",
        source_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
______
```block
A code block
```
______
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md035",
        fix_expected_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
______

```block
A code block
```

______
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_and_setext",
        source_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >
> >   abc
> >   -----
> >   ```block
> >   A code block
> >   ```
> >   abc
> >   -----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:10:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md035,md022,md024",
        fix_expected_file_contents="""> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >
> >   abc
> >   -----
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   abc
> >   -----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list",
        source_file_contents="""1. > ----
   > ```block
   > A code block
   > ```
   > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > ----
   >
   > ```block
   > A code block
   > ```
   >
   > ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_empty",
        source_file_contents="""1. > ----
   > ```block
   > ```
   > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:3:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > ----
   >
   > ```block
   > ```
   >
   > ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_bare",
        source_file_contents="""1. > block quote
   > ```block
   > A code block
   > ```
   > block quote
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > block quote
   >
   > ```block
   > A code block
   > ```
   >
   > block quote
""",
    ),
    pluginRuleTest(  # test_extra_046t0 test_extra_046t1
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_block",
        source_file_contents="""1. > >
   > > block 3
   > > block 3
   > ```block
   > A code block
   > ```
   > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > >
   > > block 3
   > > block 3
   >
   > ```block
   > A code block
   > ```
   >
   > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_block_double_drop",
        source_file_contents="""1. > >
   > > block 3
   > > block 3
   ```block
   A code block
   ```
   --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > >
   > > block 3
   > > block 3

   ```block
   A code block
   ```

   --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_block_triple_drop",
        source_file_contents="""1. > >
   > > block 3
   > > block 3
```block
A code block
```
--------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > >
   > > block 3
   > > block 3

```block
A code block
```

--------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_block_with_thematics",
        source_file_contents="""1. > >
   > > block 3
   > > block 3
   > --------
   > ```block
   > A code block
   > ```
   > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > >
   > > block 3
   > > block 3
   > --------
   >
   > ```block
   > A code block
   > ```
   >
   > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_block_double_drop_with_thematics",
        source_file_contents="""1. > >
   > > block 3
   > > block 3
   --------
   ```block
   A code block
   ```
   --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > >
   > > block 3
   > > block 3
   --------

   ```block
   A code block
   ```

   --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_block_triple_drop_with_thematics",
        source_file_contents="""1. > >
   > > block 3
   > > block 3
--------
```block
A code block
```
--------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > >
   > > block 3
   > > block 3
--------

```block
A code block
```

--------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_block_with_setext",
        source_file_contents="""1. > >
   > > block 3
   > > block 3
   >
   > abc
   > --------
   > ```block
   > A code block
   > ```
   > abc
   > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""1. > >
   > > block 3
   > > block 3
   >
   > abc
   > --------
   >
   > ```block
   > A code block
   > ```
   >
   > abc
   > --------
""",
    ),
    pluginRuleTest(  # test_extra_046s0 test_extra_046s1
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_block_and_para_continue",
        source_file_contents="""1. > >
   > > block 3
   > block 3
   > ```block
   > A code block
   > ```
   > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > >
   > > block 3
   > block 3
   >
   > ```block
   > A code block
   > ```
   >
   > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_block_and_para_continue_with_thematics",
        source_file_contents="""1. > >
   > > block 3
   > block 3
   > --------
   > ```block
   > A code block
   > ```
   > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        use_debug=True,
        fix_expected_file_contents="""1. > >
   > > block 3
   > block 3
   > --------
   >
   > ```block
   > A code block
   > ```
   >
   > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_block_and_para_continue_with_setext",
        source_file_contents="""1. > >
   > > block 3
   >
   > block 3
   > --------
   > ```block
   > A code block
   > ```
   > block 3
   > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""1. > >
   > > block 3
   >
   > block 3
   > --------
   >
   > ```block
   > A code block
   > ```
   >
   > block 3
   > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_list",
        source_file_contents="""1. > +
   >   list 3
   > + list 3
   > ```block
   > A code block
   > ```
   > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > +
   >   list 3
   > + list 3
   >
   > ```block
   > A code block
   > ```
   >
   > --------
""",
    ),
    pluginRuleTest(  # FOOBAR14
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_list_double_drop",
        source_file_contents="""1. > +
   >   list 3
   > + list 3
   ```block
   A code block
   ```
   --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        fix_expected_file_contents="""1. > +
   >   list 3
   > + list 3

   ```block
   A code block
   ```

   --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_list_triple_drop",
        source_file_contents="""1. > +
   >   list 3
   > + list 3
```block
A code block
```
--------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > +
   >   list 3
   > + list 3

```block
A code block
```

--------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_list_with_thematics",
        source_file_contents="""1. > +
   >   list 3
   > + list 3
   > --------
   > ```block
   > A code block
   > ```
   > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > +
   >   list 3
   > + list 3
   > --------
   >
   > ```block
   > A code block
   > ```
   >
   > --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_list_double_drop_with_thematics",
        source_file_contents="""1. > +
   >   list 3
   > + list 3
   --------
   ```block
   A code block
   ```
   --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > +
   >   list 3
   > + list 3
   --------

   ```block
   A code block
   ```

   --------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_list_triple_drop_with_thematics",
        source_file_contents="""1. > +
   >   list 3
   > + list 3
--------
```block
A code block
```
--------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > +
   >   list 3
   > + list 3
--------

```block
A code block
```

--------
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_with_previous_inner_list_with_setext",
        source_file_contents="""1. > +
   >   list 3
   > + list 3
   >
   > abc
   > --------
   > ```block
   > A code block
   > ```
   > abc
   > --------
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""1. > +
   >   list 3
   > + list 3
   >
   > abc
   > --------
   >
   > ```block
   > A code block
   > ```
   >
   > abc
   > --------
""",
    ),
    pluginRuleTest(  # test_extra_046r0 test_extra_046r1
        "bad_fenced_block_in_block_quote_in_block_quote_in_list",
        source_file_contents="""1. > > ----
   > > ```block
   > > A code block
   > > ```
   > > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
""",
    ),
    pluginRuleTest(  # test_extra_046q0 test_extra_046q1
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_empty",
        source_file_contents="""1. > > ----
   > > ```block
   > > ```
   > > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:3:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > >
   > > ```block
   > > ```
   > >
   > > ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_inner_block",
        source_file_contents="""1. > > ----
   > > > block 1
   > > > block 2
   > > ```block
   > > A code block
   > > ```
   > > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > > block 1
   > > > block 2
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_inner_block_double_drop",
        source_file_contents="""1. > > ----
   > > > block 1
   > > > block 2
   > ```block
   > A code block
   > ```
   > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > > block 1
   > > > block 2
   >
   > ```block
   > A code block
   > ```
   >
   > ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_inner_block_triple_drop",
        source_file_contents="""1. > > ----
   > > > block 1
   > > > block 2
   ```block
   A code block
   ```
   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > > block 1
   > > > block 2

   ```block
   A code block
   ```

   ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_inner_block_quad_drop",
        source_file_contents="""1. > > ----
   > > > block 1
   > > > block 2
```block
A code block
```
----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > > block 1
   > > > block 2

```block
A code block
```

----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_inner_list",
        source_file_contents="""1. > > ----
   > > + block 1
   > >   block 2
   > > ```block
   > > A code block
   > > ```
   > > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > + block 1
   > >   block 2
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
""",
    ),
    pluginRuleTest(  # test_extra_049l5
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_inner_list_double_drop",
        source_file_contents="""1. > > ----
   > > + block 1
   > >   block 2
   > ```block
   > A code block
   > ```
   > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > + block 1
   > >   block 2
   >
   > ```block
   > A code block
   > ```
   >
   > ----
""",
    ),
    pluginRuleTest(  # test_extra_052f0 test_extra_052f1
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_inner_list_triple_drop",
        source_file_contents="""1. > > ----
   > > + block 1
   > >   block 2
   ```block
   A code block
   ```
   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > + block 1
   > >   block 2

   ```block
   A code block
   ```

   ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_inner_list_quad_drop",
        source_file_contents="""1. > > ----
   > > + block 1
   > >   block 2
```block
A code block
```
----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > + block 1
   > >   block 2

```block
A code block
```

----
""",
    ),
    pluginRuleTest(  # test_extra_044mx2
        "bad_fenced_block_in_list_in_block_quote_in_list",
        source_file_contents="""1. > + ----
   >   ```block
   >   A code block
   >   ```
   >   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > + ----
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   ----
""",
    ),
    pluginRuleTest(  # test_extra_044mx1 test_extra_044mcw1
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block",
        source_file_contents="""1. > + ----
   >   > block 1
   >   > block 2
   >   ```block
   >   A code block
   >   ```
   >   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        use_debug=True,
        fix_expected_file_contents="""1. > + ----
   >   > block 1
   >   > block 2
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   ----
""",
    ),
    pluginRuleTest(  # test_extra_050e0 test_extra_050e1
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block_double_drop",
        source_file_contents="""1. > + ----
   >   > block 1
   >   > block 2
   > ```block
   > A code block
   > ```
   > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md027",
        fix_expected_file_contents="""1. > + ----
   >   > block 1
   >   > block 2
   >
   > ```block
   > A code block
   > ```
   >
   > ----
""",
    ),
    pluginRuleTest(  # test_extra_052g0 test_extra_052g1
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block_triple_drop",
        source_file_contents="""1. > + ----
   >   > block 1
   >   > block 2
   ```block
   A code block
   ```
   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        use_debug=True,
        fix_expected_file_contents="""1. > + ----
   >   > block 1
   >   > block 2

   ```block
   A code block
   ```

   ----
""",
    ),
    pluginRuleTest(  # test_extra_049f0
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block_quad_drop",
        source_file_contents="""1. > + ----
   >   > block 1
   >   > block 2
```block
A code block
```
----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > + ----
   >   > block 1
   >   > block 2

```block
A code block
```

----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block_2",
        source_file_contents="""1. > + ----
   >   > block 1
   >   > block 2
   >   ----
   >   ```block
   >   A code block
   >   ```
   >   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > + ----
   >   > block 1
   >   > block 2
   >   ----
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block_3",
        source_file_contents="""1. > + ----
   >   > block 1
   >   > block 2
   >   <!-- html -->
   >   ```block
   >   A code block
   >   ```
   >   <!-- html -->
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > + ----
   >   > block 1
   >   > block 2
   >   <!-- html -->
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   <!-- html -->
""",
    ),
    pluginRuleTest(  # test_extra_044mcw2
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block_4",
        source_file_contents="""1. > + ----
   >   > block 1
   >   > block 2
   >   # header 1
   >   ```block
   >   A code block
   >   ```
   >   # header 2
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md025",
        fix_expected_file_contents="""1. > + ----
   >   > block 1
   >   > block 2
   >   # header 1
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   # header 2
""",
    ),
    pluginRuleTest(  # test_extra_046p0 test_extra_046p1
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list",
        source_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >   ```block
   >   A code block
   >   ```
   >   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_double_drop",
        source_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   > ```block
   > A code block
   > ```
   > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >
   > ```block
   > A code block
   > ```
   >
   > ----
""",
    ),
    pluginRuleTest(  # test_extra_050f0 test_extra_050f1
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_triple_drop",
        source_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   ```block
   A code block
   ```
   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3

   ```block
   A code block
   ```

   ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_quad_drop",
        source_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
```block
A code block
```
----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3

```block
A code block
```

----
""",
    ),
    pluginRuleTest(  # test_extra_046n0 test_extra_046n1
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_with_thematics",
        source_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >   ----
   >   ```block
   >   A code block
   >   ```
   >   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >   ----
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   ----
""",
    ),
    pluginRuleTest(  # test_extra_049a0
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_double_drop_with_thematics",
        source_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   > ----
   > ```block
   > A code block
   > ```
   > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        use_debug=True,
        fix_expected_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   > ----
   >
   > ```block
   > A code block
   > ```
   >
   > ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_triple_drop_with_thematics",
        source_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   ----
   ```block
   A code block
   ```
   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   ----

   ```block
   A code block
   ```

   ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_quad_drop_with_thematics",
        source_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
----
```block
A code block
```
----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
----

```block
A code block
```

----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_with_setext",
        source_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >
   >   abc
   >   ----
   >   ```block
   >   A code block
   >   ```
   >   abc
   >   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:10:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >
   >   abc
   >   ----
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   abc
   >   ----
""",
    ),
    pluginRuleTest(  # test_extra_046m0 test_extra_046m1
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block",
        source_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
   > > ```block
   > > A code block
   > > ```
   > > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block_double_drop",
        source_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
   > ```block
   > A code block
   > ```
   > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
   >
   > ```block
   > A code block
   > ```
   >
   > ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block_triple_drop",
        source_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
   ```block
   A code block
   ```
   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2

   ```block
   A code block
   ```

   ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block_quad_drop",
        source_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
```block
A code block
```
----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2

```block
A code block
```

----
""",
    ),
    pluginRuleTest(  # test_extra_046k0 test_extra_046k1
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block_with_thematics",
        source_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
   > > ----
   > > ```block
   > > A code block
   > > ```
   > > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
   > > ----
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block_double_drop_with_thematics",
        source_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
   > ----
   > ```block
   > A code block
   > ```
   > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
   > ----
   >
   > ```block
   > A code block
   > ```
   >
   > ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block_triple_drop_with_thematics",
        source_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
   ----
   ```block
   A code block
   ```
   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
   ----

   ```block
   A code block
   ```

   ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block_quad_drop_with_thematics",
        source_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
----
```block
A code block
```
----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
----

```block
A code block
```

----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block_with_setext",
        source_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
   > >
   > > abc
   > > ----
   > > ```block
   > > A code block
   > > ```
   > > abc
   > > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""1. > > ----
   > > > inner block 1
   > > > inner block 2
   > >
   > > abc
   > > ----
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > abc
   > > ----
""",
    ),
    pluginRuleTest(  # test_extra_046j0 test_extra_046j1
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list",
        source_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > > ```block
   > > A code block
   > > ```
   > > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
""",
    ),
    pluginRuleTest(  # test_extra_049l6
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_double_drop",
        source_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > ```block
   > A code block
   > ```
   > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   >
   > ```block
   > A code block
   > ```
   >
   > ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_triple_drop",
        source_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   ```block
   A code block
   ```
   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        use_debug=True,
        fix_expected_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3

   ```block
   A code block
   ```

   ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_quad_drop",
        source_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
```block
A code block
```
----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3

```block
A code block
```

----
""",
    ),
    pluginRuleTest(  # test_extra_046h0 test_extra_046h1
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_with_thematics",
        source_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > > ----
   > > ```block
   > > A code block
   > > ```
   > > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > > ----
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
""",
    ),
    pluginRuleTest(  # test_extra_052e0 test_extra_052e1 FOOBAR3
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_double_drop_with_thematics",
        source_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > ----
   > ```block
   > A code block
   > ```
   > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:6: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_fix_debug=True,
        fix_expected_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > ----
   >
   > ```block
   > A code block
   > ```
   >
   > ----
""",
    ),
    pluginRuleTest(  # test_extra_052h0 test_extra_052h1 FOOBAR4
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_triple_drop_with_thematics",
        source_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   ----
   ```block
   A code block
   ```
   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:4: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_fix_debug=True,
        fix_expected_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   ----

   ```block
   A code block
   ```

   ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_quad_drop_with_thematics",
        source_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
----
```block
A code block
```
----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
----

```block
A code block
```

----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_with_setext",
        source_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > >
   > > abc
   > > ----
   > > ```block
   > > A code block
   > > ```
   > > abc
   > > ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:10:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > >
   > > abc
   > > ----
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > abc
   > > ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_in_list_empty",
        source_file_contents="""1. > + ----
   >   ```block
   >   ```
   >   ----
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:3:8: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""1. > + ----
   >
   >   ```block
   >   ```
   >
   >   ----
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote",
        source_file_contents="""> + -----
>   ```block
>   A code block
>   ```
>   -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + -----
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_empty",
        source_file_contents="""> + -----
>   ```block
>   ```
>   -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:3:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + -----
>
>   ```block
>   ```
>
>   -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_046l0 test_extra_046l1
        "bad_fenced_block_in_list_in_block_quote_bare",
        source_file_contents="""> + list
>   ```block
>   A code block
>   ```
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list
>
>   ```block
>   A code block
>   ```
>
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_044la0 test_extra_044la1
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_0",
        source_file_contents="""> + list 1
>   > block 2
>   > block 3
>   ------
>   ```block
>   A code block
>   ```
>   ------
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   > block 2
>   > block 3
>   ------
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_double_drop",
        source_file_contents="""> + list 1
>   > block 2
>   > block 3
> ------
> ```block
> A code block
> ```
> ------
> another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   > block 2
>   > block 3
> ------
>
> ```block
> A code block
> ```
>
> ------
> another list
""",
    ),
    pluginRuleTest(  # test_extra_049k0
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_triple_drop",
        source_file_contents="""> + list 1
>   > block 2
>   > block 3
------
```block
A code block
```
------
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   > block 2
>   > block 3
------

```block
A code block
```

------
another list
""",
    ),
    pluginRuleTest(  # test_extra_046g0 test_extra_046g1
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_0_without_thematics",
        source_file_contents="""> + list 1
>   > block 2
>   > block 3
>   ```block
>   A code block
>   ```
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   > block 2
>   > block 3
>
>   ```block
>   A code block
>   ```
>
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_052b0 test_extra_052b1
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_double_drop_without_thematics",
        source_file_contents="""> + list 1
>   > block 2
>   > block 3
> ```block
> A code block
> ```
> another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md027",
        fix_expected_file_contents="""> + list 1
>   > block 2
>   > block 3
>
> ```block
> A code block
> ```
>
> another list
""",
    ),
    pluginRuleTest(  # test_extra_049k1
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_triple_drop_without_thematics",
        source_file_contents="""> + list 1
>   > block 2
>   > block 3
```block
A code block
```
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   > block 2
>   > block 3

```block
A code block
```

another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_1",
        source_file_contents="""> + list 1
>   > block 2
>   > block 3
>   > block 4
>   ------
>   ```block
>   A code block
>   ```
>   ------
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   > block 2
>   > block 3
>   > block 4
>   ------
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_2",
        source_file_contents="""> + list 1
>   > block 2
>   > block 3
>   ------
>   ```block
>   line 1
>   line 2
>   ```
>   ------
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   > block 2
>   > block 3
>   ------
>
>   ```block
>   line 1
>   line 2
>   ```
>
>   ------
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_3",
        source_file_contents="""> + list 1
>   > block 2
>   ------
>   ```block
>   line 1
>   ```
>   ------
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   > block 2
>   ------
>
>   ```block
>   line 1
>   ```
>
>   ------
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_4",
        source_file_contents="""> + list 1
>   > block 1
>   ------
>   > block 2
>   ------
>   ```block
>   line 1
>   ```
>   ------
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   > block 1
>   ------
>   > block 2
>   ------
>
>   ```block
>   line 1
>   ```
>
>   ------
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_046f0 test_extra_046f1
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_list",
        source_file_contents="""> + list 1
>   + list 2
>     list 3
>   ```block
>   A code block
>   ```
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   + list 2
>     list 3
>
>   ```block
>   A code block
>   ```
>
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_double_drop",
        source_file_contents="""> + list 1
>   + list 2
>     list 3
> ```block
> A code block
> ```
> another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   + list 2
>     list 3
>
> ```block
> A code block
> ```
>
> another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_triple_drop",
        source_file_contents="""> + list 1
>   + list 2
>     list 3
```block
A code block
```
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   + list 2
>     list 3

```block
A code block
```

another list
""",
    ),
    pluginRuleTest(  # see sub3    test_extra_044cx test_extra_044ca
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_with_thematics",
        source_file_contents="""> + list 1
>   + list 2
>     list 3
>   ------
>   ```block
>   A code block
>   ```
>   ------
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   + list 2
>     list 3
>   ------
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_double_drop_with_thematics",
        source_file_contents="""> + list 1
>   + list 2
>     list 3
> ------
> ```block
> A code block
> ```
> ------
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   + list 2
>     list 3
> ------
>
> ```block
> A code block
> ```
>
> ------
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_triple_drop_with_thematics",
        source_file_contents="""> + list 1
>   + list 2
>     list 3
------
```block
A code block
```
------
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   + list 2
>     list 3
------

```block
A code block
```

------
another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_with_setext",
        source_file_contents="""> + list 1
>   + list 2
>     list 3
>
>   abc
>   ------
>   ```block
>   A code block
>   ```
>   abc
>   ------
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""> + list 1
>   + list 2
>     list 3
>
>   abc
>   ------
>
>   ```block
>   A code block
>   ```
>
>   abc
>   ------
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_with_thematics_sub1",
        source_file_contents="""> + list 1
>     list 2
>   ------
>   ```block
>   A code block
>   ```
>   ------
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md022,md023",
        fix_expected_file_contents="""> + list 1
>     list 2
>   ------
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_with_thematics_sub2",
        source_file_contents="""> + list 1
>     list 2
>     list 3
>   _____
>   ```block
>   A code block
>   ```
>   _____
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md022,md023",
        fix_expected_file_contents="""> + list 1
>     list 2
>     list 3
>   _____
>
>   ```block
>   A code block
>   ```
>
>   _____
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_046e0 test_extra_046e1
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_with_thematics_sub3",
        source_file_contents="""> + list 1
>   + list 2
>   + list 3
>   _____
>   ```block
>   A code block
>   ```
>   _____
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   + list 2
>   + list 3
>   _____
>
>   ```block
>   A code block
>   ```
>
>   _____
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_046da test_extra_046db
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_and_para_continue",
        source_file_contents="""> + list 1
>   + list 2
>   list 3
>   ```block
>   A code block
>   ```
>   ------
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   + list 2
>   list 3
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_046x test_extra_046dx
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_and_para_continue_with_thematics",
        source_file_contents="""> + list 1
>   + list 2
>   list 3
>   ------
>   ```block
>   A code block
>   ```
>   ------
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + list 1
>   + list 2
>   list 3
>   ------
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_and_para_continue_with_setext",
        source_file_contents="""> + list 1
>   + list 2
>
>   list 3
>   ------
>   ```block
>   A code block
>   ```
>   ------
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022",
        fix_expected_file_contents="""> + list 1
>   + list 2
>
>   list 3
>   ------
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_044jax test_extra_044jaa
        "bad_fenced_block_in_block_quote_in_list_in_block_quote",
        source_file_contents="""> + > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + > -----
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_044jxx test_extra_044jxa
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_empty",
        source_file_contents="""> + > -----
>   > ```block
>   > ```
>   > -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:3:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + > -----
>   >
>   > ```block
>   > ```
>   >
>   > -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_044mcz1 test_extra_046ca
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blockx_x",
        source_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_053c0 test_extra_053c1
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blockx_double_drop",
        source_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>   ```block
>   A code block
>   ```
>   -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        use_debug=True,
        # xxx
        mark_fix_as_skipped=skip_fix_bad_markdown,
        fix_expected_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blockx_triple_drop",
        source_file_contents="""> + > -----
>   > > block 1
>   > > block 2
> ```block
> A code block
> ```
> -----
> another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md007,md023,md027",
        fix_expected_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>
> ```block
> A code block
> ```
>
> -----
> another list
""",
    ),
    pluginRuleTest(  # test_extra_049e0
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blockx_quad_drop",
        source_file_contents="""> + > -----
>   > > block 1
>   > > block 2
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + > -----
>   > > block 1
>   > > block 2

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(  # test_extra_047d0, test_extra_047d1
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blocks",
        source_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   > > block 1
>   > > block 2
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   > > block 1
>   > > block 2
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_044mcv0 test_extra_044mcv1
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_with_thematics",
        source_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_double_drop_with_thematics",
        source_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>   -----
>   ```block
>   A code block
>   ```
>   -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_debug=True,
        fix_expected_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>   -----
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_051k0
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_triple_drop_with_thematics",
        source_file_contents="""> + > -----
>   > > block 1
>   > > block 2
> -----
> ```block
> A code block
> ```
> -----
> another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + > -----
>   > > block 1
>   > > block 2
> -----
>
> ```block
> A code block
> ```
>
> -----
> another list
""",
    ),
    pluginRuleTest(  # test_extra_049h0
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_quad_drop_with_thematics",
        source_file_contents="""> + > -----
>   > > block 1
>   > > block 2
-----
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + > -----
>   > > block 1
>   > > block 2
-----

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(  # test_extra_044mcv0 test_extra_044mcv1
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_with_thematics_fixed",
        source_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
""",
        scan_expected_output="",
        disable_rules="md032",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_with_setext",
        source_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>   >
>   > abc
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > abc
>   > -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022",
        fix_expected_file_contents="""> + > -----
>   > > block 1
>   > > block 2
>   >
>   > abc
>   > -----
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > abc
>   > -----
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list",
        source_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_049l7a test_extra_049l7b
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_double_drop_x",
        source_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   ```block
>   A code block
>   ```
>   -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md027",
        use_debug=True,
        fix_expected_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_049l8a test_extra_049l8b
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_triple_dropx",
        source_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
> ```block
> A code block
> ```
> -----
> another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md027",
        use_debug=True,
        fix_expected_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>
> ```block
> A code block
> ```
>
> -----
> another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_triple_dropa",
        source_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   >   list 3
> ```block
> A code block
> ```
> -----
> another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   >   list 3
>
> ```block
> A code block
> ```
>
> -----
> another list
""",
    ),
    pluginRuleTest(  # test_extra_049j0
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_quad_drop",
        source_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(  # test_extra_044mcu0 test_extra_044mcu1
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_and_thematics",
        source_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   > -----
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_051f0 test_extra_051f1
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_double_drop_and_thematics",
        source_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   -----
>   ```block
>   A code block
>   ```
>   -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md027",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_fix_debug=True,
        use_debug=True,
        fix_expected_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   -----
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_051g0 test_extra_051g1
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_triple_drop_and_thematics",
        source_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
> -----
> ```block
> A code block
> ```
> -----
> another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
> -----
>
> ```block
> A code block
> ```
>
> -----
> another list
""",
    ),
    pluginRuleTest(  # test_extra_049j1
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_quad_drop_and_thematics",
        source_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
-----
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        use_debug=True,
        fix_expected_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
-----

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_and_setext",
        source_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   >
>   > abc
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > abc
>   > -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:10:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   >
>   > abc
>   > -----
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > abc
>   > -----
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_block_quote",
        source_file_contents="""> + + -----
>     ```block
>     A code block
>     ```
>     -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + + -----
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_block_quote_empty",
        source_file_contents="""> + + -----
>     ```block
>     ```
>     -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:3:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + + -----
>
>     ```block
>     ```
>
>     -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_044mcz0x test_extra_044mcz0a
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block",
        source_file_contents="""> + + -----
>     > block 1
>     > block 2
>     ```block
>     A code block
>     ```
>     -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        use_debug=True,
        fix_expected_file_contents="""> + + -----
>     > block 1
>     > block 2
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_050d0 test_extra_050d1
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_double_drop",
        source_file_contents="""> + + -----
>     > block 1
>     > block 2
>   ```block
>   A code block
>   ```
>   -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        use_debug=True,
        # xxx
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_fix_debug=True,
        fix_expected_file_contents="""> + + -----
>     > block 1
>     > block 2
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_052j0 test_extra_052j1
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_triple_drop",
        source_file_contents="""> + + -----
>     > block 1
>     > block 2
> ```block
> A code block
> ```
> -----
> another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md027",
        use_debug=True,
        fix_expected_file_contents="""> + + -----
>     > block 1
>     > block 2
>
> ```block
> A code block
> ```
>
> -----
> another list
""",
    ),
    pluginRuleTest(  # test_extra_049d0
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_quad_drop",
        source_file_contents="""> + + -----
>     > block 1
>     > block 2
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + + -----
>     > block 1
>     > block 2

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(  # test_extra_044mct0 test_extra_044mct1
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_with_thematics",
        source_file_contents="""> + + -----
>     > block 1
>     > block 2
>     -----
>     ```block
>     A code block
>     ```
>     -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + + -----
>     > block 1
>     > block 2
>     -----
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_052c0 test_extra_052c1
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_double_drop_with_thematics",
        source_file_contents="""> + + -----
>     > block 1
>     > block 2
>   -----
>   ```block
>   A code block
>   ```
>   -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md027",
        use_debug=True,
        use_fix_debug=True,
        mark_fix_as_skipped=skip_fix_bad_markdown,
        fix_expected_file_contents="""> + + -----
>     > block 1
>     > block 2
>   -----
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_052k0 test_extra_052k1 FOOBAR7
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_triple_drop_with_thematics",
        source_file_contents="""> + + -----
>     > block 1
>     > block 2
> -----
> ```block
> A code block
> ```
> -----
> another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_fix_debug=True,
        fix_expected_file_contents="""> + + -----
>     > block 1
>     > block 2
> -----
>
> ```block
> A code block
> ```
>
> -----
> another list
""",
    ),
    pluginRuleTest(  # test_extra_049d1
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_quad_drop_with_thematics",
        source_file_contents="""> + + -----
>     > block 1
>     > block 2
-----
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + + -----
>     > block 1
>     > block 2
-----

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_with_setext",
        source_file_contents="""> + + -----
>     > block 1
>     > block 2
>
>     abc
>     -----
>     ```block
>     A code block
>     ```
>     abc
>     -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""> + + -----
>     > block 1
>     > block 2
>
>     abc
>     -----
>
>     ```block
>     A code block
>     ```
>
>     abc
>     -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_046cc0 test_extra_046cc1
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list",
        source_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
>     ```block
>     A code block
>     ```
>     -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_052l0 test_extra_052l01 NONCOMP1
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_double_drop",
        source_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
>   ```block
>   A code block
>   ```
>   -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_debug=True,
        fix_expected_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_triple_drop",
        source_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
> ```block
> A code block
> ```
> -----
> another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
>
> ```block
> A code block
> ```
>
> -----
> another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_quad_drop",
        source_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(  # test_extra_044mcs0 test_extra_044mcs1
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_and_thematics",
        source_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
>     -----
>     ```block
>     A code block
>     ```
>     -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
>     -----
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list
""",
    ),
    pluginRuleTest(  # test_extra_052m0 test_extra_052m1 NONCOMP2
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_double_drop_and_thematics",
        source_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
>   -----
>   ```block
>   A code block
>   ```
>   -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        use_debug=True,
        mark_fix_as_skipped=skip_fix_bad_markdown,
        fix_expected_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
>   -----
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_triple_drop_and_thematics",
        source_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
> -----
> ```block
> A code block
> ```
> -----
> another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
> -----
>
> ```block
> A code block
> ```
>
> -----
> another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_quad_drop_and_thematics",
        source_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
-----
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
-----

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_and_setext",
        source_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
>
>     abc
>     -----
>     ```block
>     A code block
>     ```
>     abc
>     -----
> + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:10:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""> + + -----
>     + list 1
>       list 2
>     + list 3
>
>     abc
>     -----
>
>     ```block
>     A code block
>     ```
>
>     abc
>     -----
> + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list",
        source_file_contents="""+ + -----
    ```block
    A code block
    ```
    -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + -----

    ```block
    A code block
    ```

    -----
  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_empty",
        source_file_contents="""+ + -----
    ```block
    ```
    -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:3:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + -----

    ```block
    ```

    -----
  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_bare",
        source_file_contents="""+ + list
    ```block
    A code block
    ```
    more text
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list

    ```block
    A code block
    ```

    more text
""",
    ),
    pluginRuleTest(  # test_extra_044mcr0 test_extra_044mcr1
        "bad_fenced_block_in_list_in_list_with_previous_inner_block",
        source_file_contents="""+ + list 1
    > block 2.1
    > block 2.2
    ```block
    A code block
    ```
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list 1
    > block 2.1
    > block 2.2

    ```block
    A code block
    ```

  + another list
""",
    ),
    pluginRuleTest(  # test_extra_050a0a test_extra_050a0b
        "bad_fenced_block_in_list_in_list_with_previous_inner_block_double_drop",
        source_file_contents="""+ + list 1
    > block 2.1
    > block 2.2
  ```block
  A code block
  ```
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_fix_debug=True,
        use_debug=True,
        fix_expected_file_contents="""+ + list 1
    > block 2.1
    > block 2.2

  ```block
  A code block
  ```

  another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_with_previous_inner_block_triple_drop",
        source_file_contents="""+ + list 1
    > block 2.1
    > block 2.2
```block
A code block
```
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list 1
    > block 2.1
    > block 2.2

```block
A code block
```

another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_with_previous_inner_block_with_thematics",
        source_file_contents="""+ + list 1
    > block 2.1
    > block 2.2
    ----
    ```block
    A code block
    ```
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list 1
    > block 2.1
    > block 2.2
    ----

    ```block
    A code block
    ```

  + another list
""",
    ),
    pluginRuleTest(  # test_extra_052n0 test_extra_052n1
        "bad_fenced_block_in_list_in_list_with_previous_inner_block_double_drop_with_thematics",
        source_file_contents="""+ + list 1
    > block 2.1
    > block 2.2
  ----
  ```block
  A code block
  ```
  ----
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        fix_expected_file_contents="""+ + list 1
    > block 2.1
    > block 2.2
  ----

  ```block
  A code block
  ```

  ----
  another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_with_previous_inner_block_triple_drop_with_thematics",
        source_file_contents="""+ + list 1
    > block 2.1
    > block 2.2
----
```block
A code block
```
----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list 1
    > block 2.1
    > block 2.2
----

```block
A code block
```

----
another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_with_previous_inner_block_with_setext",
        source_file_contents="""+ + list 1
    > block 2.1
    > block 2.2

    abc
    ----
    ```block
    A code block
    ```
    abc
    ----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""+ + list 1
    > block 2.1
    > block 2.2

    abc
    ----

    ```block
    A code block
    ```

    abc
    ----
  + another list
""",
    ),
    pluginRuleTest(  # test_extra_047a0 test_extra_047a1
        "bad_fenced_block_in_list_in_list_with_previous_inner_listx",
        source_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2
    ```block
    A code block
    ```
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2

    ```block
    A code block
    ```

  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_with_previous_inner_list_double_drop",
        source_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2
  ```block
  A code block
  ```
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2

  ```block
  A code block
  ```

  another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_with_previous_inner_list_triple_drop",
        source_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2
```block
A code block
```
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2

```block
A code block
```

another list
""",
    ),
    pluginRuleTest(  # test_extra_047g0 test_extra_047g1
        "bad_fenced_block_in_list_in_list_with_previous_inner_list_with_thematics",
        source_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2
    ----
    ```block
    A code block
    ```
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2
    ----

    ```block
    A code block
    ```

  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_with_previous_inner_list_double_drop_with_thematics",
        source_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2
  ----
  ```block
  A code block
  ```
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2
  ----

  ```block
  A code block
  ```

  another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_with_previous_inner_list_triple_drop_with_thematics",
        source_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2
----
```block
A code block
```
----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2
----

```block
A code block
```

----
another list
""",
    ),
    pluginRuleTest(  # test_extra_047g2 test_extra_047g3
        "bad_fenced_block_in_list_in_list2_with_previous_inner_list_with_thematics",
        source_file_contents="""+ + list 1
    + list 2.1
      list 2.2
    ----
    ```block
    A code block
    ```
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list 1
    + list 2.1
      list 2.2
    ----

    ```block
    A code block
    ```

  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_with_previous_inner_list_with_setext",
        source_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2

    abc
    ----
    ```block
    A code block
    ```
    abc
    ----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""+ + list 1
+ + + list 2.1
      list 2.2

    abc
    ----

    ```block
    A code block
    ```

    abc
    ----
  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_with_previous_inner_list_and_para_continue",
        source_file_contents="""+ + list 1
+ + + list 2.1
    list 2.2
    ```block
    A code block
    ```
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list 1
+ + + list 2.1
    list 2.2

    ```block
    A code block
    ```

  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_with_previous_inner_list_and_para_continue_and_thematics",
        source_file_contents="""+ + list 1
+ + + list 2.1
    list 2.2
    ---
    ```block
    A code block
    ```
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + list 1
+ + + list 2.1
    list 2.2
    ---

    ```block
    A code block
    ```

  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_with_previous_inner_list_and_para_continue_and_setext",
        source_file_contents="""+ + list 1
+ + + list 2.1
    list 2.2

    abc
    ---
    ```block
    A code block
    ```
    abc
    ---
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""+ + list 1
+ + + list 2.1
    list 2.2

    abc
    ---

    ```block
    A code block
    ```

    abc
    ---
  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_list",
        source_file_contents="""+ + > -----
    > ```block
    > A code block
    > ```
    > -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + > -----
    >
    > ```block
    > A code block
    > ```
    >
    > -----
  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_list_empty",
        source_file_contents="""+ + > -----
    > ```block
    > ```
    > -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:3:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + > -----
    >
    > ```block
    > ```
    >
    > -----
  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_block",
        source_file_contents="""+ + > -----
    > > block 1
    > > block 2
    > ```block
    > A code block
    > ```
    > -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + > -----
    > > block 1
    > > block 2
    >
    > ```block
    > A code block
    > ```
    >
    > -----
  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_block_double_drop",
        source_file_contents="""+ + > -----
    > > block 1
    > > block 2
    ```block
    A code block
    ```
    -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + > -----
    > > block 1
    > > block 2

    ```block
    A code block
    ```

    -----
  + another list
""",
    ),
    pluginRuleTest(  # test_extra_052p0 NONCOMP4
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_block_triple_drop",
        source_file_contents="""+ + > -----
    > > block 1
    > > block 2
  ```block
  A code block
  ```
  -----
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_debug=True,
        fix_expected_file_contents="""+ + > -----
    > > block 1
    > > block 2

  ```block
  A code block
  ```

  -----
  another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_block_quad_drop",
        source_file_contents="""+ + > -----
    > > block 1
    > > block 2
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + > -----
    > > block 1
    > > block 2

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(  # test_extra_044lc
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_block_and_thematics",
        source_file_contents="""+ + > -----
    > > block 1
    > > block 2
    > -----
    > ```block
    > A code block
    > ```
    > -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + > -----
    > > block 1
    > > block 2
    > -----
    >
    > ```block
    > A code block
    > ```
    >
    > -----
  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_block_double_drop_and_thematics",
        source_file_contents="""+ + > -----
    > > block 1
    > > block 2
    -----
    ```block
    A code block
    ```
    -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + > -----
    > > block 1
    > > block 2
    -----

    ```block
    A code block
    ```

    -----
  + another list
""",
    ),
    pluginRuleTest(  # test_extra_052q0 NONCOMP5
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_block_triple_drop_and_thematics",
        source_file_contents="""+ + > -----
    > > block 1
    > > block 2
  -----
  ```block
  A code block
  ```
  -----
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        fix_expected_file_contents="""+ + > -----
    > > block 1
    > > block 2
  -----

  ```block
  A code block
  ```

  -----
  another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_block_quad_drop_and_thematics",
        source_file_contents="""+ + > -----
    > > block 1
    > > block 2
-----
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + > -----
    > > block 1
    > > block 2
-----

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_block_and_setext",
        source_file_contents="""+ + > -----
    > > block 1
    > > block 2
    >
    > abc
    > -----
    > ```block
    > A code block
    > ```
    > abc
    > -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""+ + > -----
    > > block 1
    > > block 2
    >
    > abc
    > -----
    >
    > ```block
    > A code block
    > ```
    >
    > abc
    > -----
  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list",
        source_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
    > ```block
    > A code block
    > ```
    > -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
    >
    > ```block
    > A code block
    > ```
    >
    > -----
  + another list
""",
    ),
    pluginRuleTest(  # test_extra_049l9a test_extra_049l9b
        "bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_double_dropy",
        source_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
    ```block
    A code block
    ```
    -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3

    ```block
    A code block
    ```

    -----
  + another list
""",
    ),
    pluginRuleTest(  # test_extra_052r0 test_extra_052r1 NONCOMP6
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list_triple_drop",
        source_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
  ```block
  A code block
  ```
  -----
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_debug=True,
        fix_expected_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3

  ```block
  A code block
  ```

  -----
  another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list_quad_drop",
        source_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list_and_thematics",
        source_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
    > -----
    > ```block
    > A code block
    > ```
    > -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
    > -----
    >
    > ```block
    > A code block
    > ```
    >
    > -----
  + another list
""",
    ),
    pluginRuleTest(  # test_extra_052s0 test_extra_052s1
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list_double_drop_and_thematics",
        source_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
    -----
    ```block
    A code block
    ```
    -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_fix_debug=True,
        fix_expected_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
    -----

    ```block
    A code block
    ```

    -----
  + another list
""",
    ),
    pluginRuleTest(  # test_extra_052t0 NONCOMP7
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list_triple_drop_and_thematics",
        source_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
  -----
  ```block
  A code block
  ```
  -----
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        fix_expected_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
  -----

  ```block
  A code block
  ```

  -----
  another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list_quad_drop_and_thematics",
        source_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
-----
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
-----

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list_and_setext",
        source_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
    >
    > abc
    > -----
    > ```block
    > A code block
    > ```
    > abc
    > -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:10:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""+ + > -----
    > + list 1
    >   list 2
    > + list 3
    >
    > abc
    > -----
    >
    > ```block
    > A code block
    > ```
    >
    > abc
    > -----
  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_list",
        source_file_contents="""+ + + -----
      ```block
      A code block
      ```
      -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:4:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + + -----

      ```block
      A code block
      ```

      -----
  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_list_with_previous_block",
        source_file_contents="""+ + + -----
      > block 1
      > block 2
      ```block
      A code block
      ```
      -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + + -----
      > block 1
      > block 2

      ```block
      A code block
      ```

      -----
  + another list
""",
    ),
    pluginRuleTest(  # test_extra_049l4xa test_extra_049l4xb FOOBAR10
        "bad_fenced_block_in_list_in_list_in_list_with_previous_block_double_drop",
        source_file_contents="""+ + + -----
      > block 1
      > block 2
    ```block
    A code block
    ```
    -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        use_debug=True,
        mark_fix_as_skipped=skip_fix_bad_markdown,
        fix_expected_file_contents="""+ + + -----
      > block 1
      > block 2

    ```block
    A code block
    ```

    -----
  + another list
""",
    ),
    pluginRuleTest(  # test_extra_052u0 test_extra_052u1 FOOBAR11
        "bad_fenced_block_in_list_in_list_in_list_with_previous_block_triple_drop",
        source_file_contents="""+ + + -----
      > block 1
      > block 2
  ```block
  A code block
  ```
  -----
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_debug=True,
        fix_expected_file_contents="""+ + + -----
      > block 1
      > block 2

  ```block
  A code block
  ```

  -----
  another list
""",
    ),
    pluginRuleTest(  # test_extra_050c2 test_extra_050c3
        "bad_fenced_block_in_list_in_list_in_list_with_previous_block_quad_drop",
        source_file_contents="""+ + + -----
      > block 1
      > block 2
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:6:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        use_debug=True,
        fix_expected_file_contents="""+ + + -----
      > block 1
      > block 2

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_list_with_previous_block_with_thematics",
        source_file_contents="""+ + + -----
      > block 1
      > block 2
      -----
      ```block
      A code block
      ```
      -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + + -----
      > block 1
      > block 2
      -----

      ```block
      A code block
      ```

      -----
  + another list
""",
    ),
    pluginRuleTest(  # test_extra_052v0 test_extra_052v1 NONCOMP8
        "bad_fenced_block_in_list_in_list_in_list_with_previous_block_double_drop_with_thematics",
        source_file_contents="""+ + + -----
      > block 1
      > block 2
    -----
    ```block
    A code block
    ```
    -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_debug=True,
        fix_expected_file_contents="""+ + + -----
      > block 1
      > block 2
    -----

    ```block
    A code block
    ```

    -----
  + another list
""",
    ),
    pluginRuleTest(  # test_extra_050c0 test_extra_050c1
        "bad_fenced_block_in_list_in_list_in_list_with_previous_block_triple_drop_with_thematics",
        source_file_contents="""+ + + -----
      > block 1
      > block 2
  -----
  ```block
  A code block
  ```
  -----
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + + -----
      > block 1
      > block 2
  -----

  ```block
  A code block
  ```

  -----
  another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_list_with_previous_block_quad_drop_with_thematics",
        source_file_contents="""+ + + -----
      > block 1
      > block 2
-----
```block
A code block
```
-----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + + -----
      > block 1
      > block 2
-----

```block
A code block
```

-----
another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_list_with_previous_block_with_setext",
        source_file_contents="""+ + + -----
      > block 1
      > block 2

      abc
      -----
      ```block
      A code block
      ```
      abc
      -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:9:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032,md022,md024",
        fix_expected_file_contents="""+ + + -----
      > block 1
      > block 2

      abc
      -----

      ```block
      A code block
      ```

      abc
      -----
  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_list_with_previous_inner_list_with_thematics",
        source_file_contents="""+ + + list 1
+ + + + list 2.1
        list 2.2
      ----
      ```block
      A code block
      ```
      ----
    + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + + list 1
+ + + + list 2.1
        list 2.2
      ----

      ```block
      A code block
      ```

      ----
    + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_list_with_previous_inner_list_double_drop_with_thematics",
        source_file_contents="""+ + + list 1
+ + + + list 2.1
        list 2.2
    ----
    ```block
    A code block
    ```
    ----
    another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + + list 1
+ + + + list 2.1
        list 2.2
    ----

    ```block
    A code block
    ```

    ----
    another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_list_with_previous_inner_list_triple_drop_with_thematics",
        source_file_contents="""+ + + list 1
+ + + + list 2.1
        list 2.2
  ----
  ```block
  A code block
  ```
  ----
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + + list 1
+ + + + list 2.1
        list 2.2
  ----

  ```block
  A code block
  ```

  ----
  another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_list_with_previous_inner_list_quad_drop_with_thematics",
        source_file_contents="""+ + + list 1
+ + + + list 2.1
        list 2.2
----
```block
A code block
```
----
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + + list 1
+ + + + list 2.1
        list 2.2
----

```block
A code block
```

----
another list
""",
    ),
    pluginRuleTest(  # test_extra_044mcq0 test_extra_044mcq1
        "bad_fenced_block_in_list_in_list_in_list_with_previous_list_0",
        source_file_contents="""+ + + -----
      + list 1
        list 2
      + list 3
      -----
      ```block
      A code block
      ```
      -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:8:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + + -----
      + list 1
        list 2
      + list 3
      -----

      ```block
      A code block
      ```

      -----
  + another list
""",
    ),
    pluginRuleTest(  # test_extra_050b0 test_extra_050b1 FOOBAR12
        "bad_fenced_block_in_list_in_list_in_list_with_previous_list_double_drop",
        source_file_contents="""+ + + -----
      + list 1
        list 2
      + list 3
    ```block
    A code block
    ```
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:5: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_fix_debug=True,
        use_debug=True,
        fix_expected_file_contents="""+ + + -----
      + list 1
        list 2
      + list 3

    ```block
    A code block
    ```

  + another list
""",
    ),
    pluginRuleTest(  # test_extra_052w0 test_extra_052w1
        "bad_fenced_block_in_list_in_list_in_list_with_previous_list_triple_drop",
        source_file_contents="""+ + + -----
      + list 1
        list 2
      + list 3
  ```block
  A code block
  ```
  another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        mark_fix_as_skipped=skip_fix_bad_markdown,
        use_debug=True,
        fix_expected_file_contents="""+ + + -----
      + list 1
        list 2
      + list 3

  ```block
  A code block
  ```

  another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_list_with_previous_list_quad_drop",
        source_file_contents="""+ + + -----
      + list 1
        list 2
      + list 3
```block
A code block
```
another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:7:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + + -----
      + list 1
        list 2
      + list 3

```block
A code block
```

another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_list_with_previous_list_1",
        source_file_contents="""+ + + -----
      + list 1
        list 2
      + list 1
        list 2
      + list 3
      -----
      ```block
      A code block
      ```
      -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:8:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:10:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + + -----
      + list 1
        list 2
      + list 1
        list 2
      + list 3
      -----

      ```block
      A code block
      ```

      -----
  + another list
""",
    ),
    pluginRuleTest(
        "bad_fenced_block_in_list_in_list_in_list_empty",
        source_file_contents="""+ + + -----
      ```block
      ```
      -----
  + another list
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{temp_source_path}:3:7: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md032",
        fix_expected_file_contents="""+ + + -----

      ```block
      ```

      -----
  + another list
""",
    ),
    pluginRuleTest(
        "issue_626",
        source_file_contents="""# Steps

1. First

    ```yaml
    ---
    apiVersion: kustomize.toolkit.fluxcd.io/v1beta2
    ```

2. Create

    ```yaml
    ---
    resources:
        - ../../base/git-common
    ```
""",
    ),
    pluginRuleTest(
        "in_block_quotes_fall_off_after_fenced_open",
        source_file_contents="""> this is text
>
> ```text
  this is not a tab in a code block
  ```
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:3: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
""",
        disable_rules="md010,md040",
        fix_expected_file_contents="""> this is text
>
> ```text
  this is not a tab in a code block

  ```
""",
    ),
]


@pytest.mark.parametrize(
    "test", calculate_scan_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md031_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md031")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md031_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md031_config(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(
        test,
        file_contents="""this is a paragraph without any capitalization errors
""",
    )


def test_md031_query_config():
    config_test = pluginQueryConfigTest(
        "md031",
        """
  ITEM               DESCRIPTION

  Id                 md031
  Name(s)            blanks-around-fences
  Short Description  Fenced code blocks should be surrounded by blank lines
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md031.md


  CONFIGURATION ITEM  TYPE     VALUE

  list_items          boolean  True

""",
    )
    execute_query_configuration_test(config_test)
