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

source_path = os.path.join("test", "resources", "rules", "md060") + os.sep

configTests = [
    pluginConfigErrorTest(
        "invalid_style_type",
        use_strict_config=True,
        set_args=["plugins.md060.style=$#1"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md060.style' must be of type 'str'.""",
    ),
    pluginConfigErrorTest(
        "invalid_style",
        use_strict_config=True,
        set_args=["plugins.md060.style=bob"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md060.style' is not valid: Allowable values: ['any', 'tight', 'compact', 'aligned'].""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_implicit_tight_column_style",
        source_file_contents="""|Character|Meaning|
|---|---|
|Y|Yes|
|N|No|
""",
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_implicit_tight_column_style_with_compact_first_column_content",
        source_file_contents="""| Character |Meaning|
|---|---|
| Y |Yes|
| N |No|
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_implicit_tight_column_style_with_too_many_and_too_few_separators",
        source_file_contents="""|Character|Meaning|
|------|--|
|Y|Yes|
|N|No|
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:2: MD060: Table column style. [Style: tight Expected-Delimeters: 3 Actual-Delimeters: 6] (table-column-style)
{temp_source_path}:2:9: MD060: Table column style. [Style: tight Expected-Delimeters: 3 Actual-Delimeters: 2] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_implicit_tight_column_style_with_compact_second_column",
        source_file_contents="""|Character|Meaning|
|---|---|
|Y| Yes |
|N| No |
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:7: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_explicit_tight_column_style",
        source_file_contents="""|Character|Meaning|
|---|---|
|Y|Yes|
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "good_explicit_tight_column_style_within_text",
        source_file_contents="""This is a table.

|Character|Meaning|
|---|---|
|Y|Yes|
|N|No|

That was a table.
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "good_explicit_tight_column_style_with_empty_columns",
        source_file_contents="""|Character|Meaning|
|---|---|
|Y||
|N||
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_second_column",
        source_file_contents="""|Character|Meaning|
|---|---|
|Y| Yes |
|N| No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:7: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table",
        source_file_contents="""| Character | Meaning |
| --- | --- |
| Y | Yes |
| N | No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table_leading_increasing_whitespace",
        source_file_contents=""" | Character | Meaning |
  | --- | --- |
   | Y | Yes |
 | N | No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:3: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:13: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:15: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:23: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:5: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:7: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:13: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:5: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:7: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table_leading_increasing_whitespace_no_leading_and_trailing",
        source_file_contents=""" Character | Meaning
  --- | ---
   Y | Yes
 N | No
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:11: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:13: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:5: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:7: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:5: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table_align_left",
        source_file_contents="""| Character | Meaning |
| :-- | :-- |
| Y | Yes |
| N | No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table_align_center",
        source_file_contents="""| Character | Meaning |
| :-: | :-: |
| Y | Yes |
| N | No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table_align_right",
        source_file_contents="""| Character | Meaning |
| --: | --: |
| Y | Yes |
| N | No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table_no_starting_bar",
        source_file_contents="""Character | Meaning |
--- | --- |
Y | Yes |
N | No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:20: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:7: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table_title_no_starting_bar",
        source_file_contents="""Character | Meaning |
| --- | --- |
| Y | Yes |
| N | No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:20: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table_separator_no_starting_bar",
        source_file_contents="""| Character | Meaning |
--- | --- |
| Y | Yes |
| N | No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table_row_no_starting_bar",
        source_file_contents="""| Character | Meaning |
| --- | --- |
Y | Yes |
| N | No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table_no_ending_bar",
        source_file_contents="""| Character | Meaning
| --- | ---
| Y | Yes
| N | No
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table_title_no_ending_bar",
        source_file_contents="""| Character | Meaning
| --- | --- |
| Y | Yes |
| N | No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table_separator_no_ending_bar",
        source_file_contents="""| Character | Meaning |
| --- | ---
| Y | Yes |
| N | No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_compact_styled_table_row_no_ending_bar",
        source_file_contents="""| Character | Meaning |
| --- | --- |
| Y | Yes
| N | No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_backslashes_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| \\$Y | \\$Yes |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_entities_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| &amp;Y | &amp;Yes |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:11: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:20: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_code_spans_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| Y `Y` | Yes `Y` |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:18: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_emphasis_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| *Y* | *Yes* |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_strikethrough_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ~Y~ | ~Yes~ |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables,markdown-strikethrough",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:8: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google](www.google.com) | [Google](www.google.com) |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:27: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:29: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:54: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_with_title_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google](www.google.com "title") | [Google](www.google.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:35: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:37: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:70: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_with_title_in_first_row_with_link_text_special",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo&gle](www.google.com "title") | [Goo&gle](www.google.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:36: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:38: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:72: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_with_title_in_first_row_with_link_text_backslash",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo\\$gle](www.google.com "title") | [Goo\\$gle](www.google.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:37: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:39: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:74: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_with_title_in_first_row_with_link_text_entity",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo&copy;gle](www.google.com "title") | [Goo&copy;gle](www.google.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        disable_rules="md013",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:41: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:43: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:82: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_with_title_in_first_row_with_link_text_code_span",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo `copy` gle](www.google.com "title") | [Goo `copy` gle](www.google.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        disable_rules="md013",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:43: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:45: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:86: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_with_title_in_first_row_with_link_dest_special",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google](www.goo&gle.com "title") | [Google](www.goo&gle.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:36: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:38: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:72: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_with_title_in_first_row_with_link_dest_backslash",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google](www.goo\\$gle.com "title") | [Google](www.goo\\$gle.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:37: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:39: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:74: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_with_title_in_first_row_with_link_dest_entity",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google](www.goo&copy;gle.com "title") | [Google](www.goo&copy;gle.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        disable_rules="md013",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:41: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:43: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:82: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_with_title_in_first_row_with_link_dest_code_span",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google](www.goo`copy`gle.com "title") | [Google](www.goo`copy`gle.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        disable_rules="md013",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:41: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:43: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:82: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_with_title_in_first_row_with_link_title_special",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google](www.google.com "ti&tle") | [Google](www.google.com "ti&tle") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:36: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:38: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:72: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_with_title_in_first_row_with_link_title_backslash",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google](www.google.com "ti\\$tle") | [Google](www.google.com "ti\\$tle") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:37: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:39: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:74: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_with_title_in_first_row_with_link_title_entity",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google](www.google.com "tit&copy;le") | [Google](www.google.com "ti&copy;tle") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        disable_rules="md013",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:41: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:43: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:82: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_links_with_title_in_first_row_with_link_title_code_span",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google](www.google.com "ti`copy`tle") | [Google](www.google.com "ti`copy`tle") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        disable_rules="md013",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:41: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:43: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:82: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_links_without_lrd_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [MyGoogle][Google] | [MyGoogle][Google] |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:21: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:23: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:42: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_links_with_lrd_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [MyGoogle][Google] | [MyGoogle][Google] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:21: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:23: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:42: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_links_with_lrd_and_first_special_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [My&Google][Google] | [My&Google][Google] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:24: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:44: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_links_with_lrd_and_second_special_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [MyGoogle][Goo&gle] | [MyGoogle][Goo&gle] |
|N|No|

[Goo&gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:24: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:44: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_links_with_lrd_and_first_backslash_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [My\\$Google][Google] | [My\\$Google][Google] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:23: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:25: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:46: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_links_with_lrd_and_second_backslash_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [MyGoogle][Goo\\$gle] | [MyGoogle][Goo\\$gle] |
|N|No|

[Goo\\$gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:23: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:25: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:46: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_links_with_lrd_and_first_entity_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [My&copy;Google][Google] | [My&copy;Google][Google] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:27: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:29: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:54: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_links_with_lrd_and_second_entity_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [MyGoogle][Goo&copy;gle] | [MyGoogle][Goo&copy;gle] |
|N|No|

[Goo&copy;gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:27: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:29: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:54: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_links_with_lrd_and_first_code_span_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [My `copy` Google][Google] | [My `copy` Google][Google] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:29: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:31: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:58: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_links_with_lrd_and_second_code_span_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [MyGoogle][Goo `copy` gle] | [MyGoogle][Goo `copy` gle] |
|N|No|

[Goo `copy` gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:29: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:31: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:58: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_links_without_lrd_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google][] | [Google][] |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:13: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:15: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:26: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_links_with_lrd_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google][] | [Google][] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:13: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:15: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:26: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_links_with_lrd_and_special_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo&gle][] | [Goo&gle][] |
|N|No|

[Goo&gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:16: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:28: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_links_with_lrd_and_backslash_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo\\$gle][] | [Goo\\$gle][] |
|N|No|

[Goo\\$gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:15: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:17: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:30: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_links_with_lrd_and_entity_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo&copy;gle][] | [Goo&copy;gle][] |
|N|No|

[Goo&copy;gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:19: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:21: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:38: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_links_with_lrd_and_code_span_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo`copy`gle][] | [Goo`copy`gle][] |
|N|No|

[Goo`copy`gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:19: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:21: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:38: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_links_with_lrd_and_emphasis_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo *copy* gle][] | [Goo *copy* gle][] |
|N|No|

[Goo *copy* gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:21: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:23: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:42: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_links_without_lrd_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google] | [Google] |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:11: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:13: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_links_with_lrd_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Google] | [Google] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:11: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:13: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_links_with_lrd_and_special_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo&gle] | [Goo&gle] |
|N|No|

[Goo&gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:24: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_links_with_lrd_and_backslash_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo\\$gle] | [Goo\\$gle] |
|N|No|

[Goo\\$gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:13: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:15: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:26: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_links_with_lrd_and_entity_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo&copy;gle] | [Goo&copy;gle] |
|N|No|

[Goo&copy;gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:17: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:19: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:34: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_links_with_lrd_and_code_span_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo`copy`gle] | [Goo`copy`gle] |
|N|No|

[Goo`copy`gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:17: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:19: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:34: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_links_with_lrd_and_emphasis_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| [Goo *copy* gle] | [Goo *copy* gle] |
|N|No|

[Goo *copy* gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:19: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:21: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:38: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_image_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Google](www.google.com) | ![Google](www.google.com) |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:28: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:30: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:56: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_image_with_title_in_first_row_with_link_text_special",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo&gle](www.google.com "title") | ![Goo&gle](www.google.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:37: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:39: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:74: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_image_with_title_in_first_row_with_link_text_backslash",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo\\$gle](www.google.com "title") | ![Goo\\$gle](www.google.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:38: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:40: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:76: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_image_with_title_in_first_row_with_link_text_entity",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo&copy;gle](www.google.com "title") | ![Goo&copy;gle](www.google.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        disable_rules="md013",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:42: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:44: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:84: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_image_with_title_in_first_row_with_link_text_code_span",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo `copy` gle](www.google.com "title") | ![Goo `copy` gle](www.google.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        disable_rules="md013",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:44: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:46: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:88: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_image_with_title_in_first_row_with_link_dest_special",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Google](www.goo&gle.com "title") | ![Google](www.goo&gle.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:37: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:39: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:74: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_image_with_title_in_first_row_with_link_dest_backslash",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Google](www.goo\\$gle.com "title") | ![Google](www.goo\\$gle.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:38: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:40: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:76: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_image_with_title_in_first_row_with_link_dest_entity",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Google](www.goo&copy;gle.com "title") | ![Google](www.goo&copy;gle.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        disable_rules="md013",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:42: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:44: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:84: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_image_with_title_in_first_row_with_link_dest_code_span",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Google](www.goo`copy`gle.com "title") | ![Google](www.goo`copy`gle.com "title") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        disable_rules="md013",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:42: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:44: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:84: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_image_with_title_in_first_row_with_link_title_special",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Google](www.google.com "ti&tle") | ![Google](www.google.com "ti&tle") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:37: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:39: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:74: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_image_with_title_in_first_row_with_link_title_backslash",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Google](www.google.com "ti\\$tle") | ![Google](www.google.com "ti\\$tle") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:38: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:40: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:76: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_image_with_title_in_first_row_with_link_title_entity",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Google](www.google.com "tit&copy;le") | ![Google](www.google.com "ti&copy;tle") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        disable_rules="md013",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:42: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:44: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:84: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_inline_image_with_title_in_first_row_with_link_title_code_span",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Google](www.google.com "ti`copy`tle") | ![Google](www.google.com "ti`copy`tle") |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        disable_rules="md013",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:42: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:44: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:84: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_image_without_lrd_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![MyGoogle][Google] | ![MyGoogle][Google] |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:24: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:44: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_image_with_lrd_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![MyGoogle][Google] | ![MyGoogle][Google] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:24: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:44: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_image_with_lrd_and_first_special_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![My&Google][Google] | ![My&Google][Google] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:23: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:25: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:46: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_image_with_lrd_and_second_special_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![MyGoogle][Goo&gle] | ![MyGoogle][Goo&gle] |
|N|No|

[Goo&gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:23: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:25: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:46: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_image_with_lrd_and_first_backslash_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![My\\$Google][Google] | ![My\\$Google][Google] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:24: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:26: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:48: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_image_with_lrd_and_second_backslash_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![MyGoogle][Goo\\$gle] | ![MyGoogle][Goo\\$gle] |
|N|No|

[Goo\\$gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:24: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:26: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:48: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_image_with_lrd_and_first_entity_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![My&copy;Google][Google] | ![My&copy;Google][Google] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:28: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:30: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:56: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_image_with_lrd_and_second_entity_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![MyGoogle][Goo&copy;gle] | ![MyGoogle][Goo&copy;gle] |
|N|No|

[Goo&copy;gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:28: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:30: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:56: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_image_with_lrd_and_first_code_span_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![My `copy` Google][Google] | ![My `copy` Google][Google] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:30: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:32: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:60: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_full_image_with_lrd_and_second_code_span_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![MyGoogle][Goo `copy` gle] | ![MyGoogle][Goo `copy` gle] |
|N|No|

[Goo `copy` gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:30: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:32: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:60: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_image_without_lrd_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Google][] | ![Google][] |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:16: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:28: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_image_with_lrd_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Google][] | ![Google][] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:16: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:28: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_image_with_lrd_and_special_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo&gle][] | ![Goo&gle][] |
|N|No|

[Goo&gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:15: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:17: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:30: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_image_with_lrd_and_backslash_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo\\$gle][] | ![Goo\\$gle][] |
|N|No|

[Goo\\$gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:16: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:18: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:32: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_image_with_lrd_and_entity_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo&copy;gle][] | ![Goo&copy;gle][] |
|N|No|

[Goo&copy;gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:20: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:40: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_image_with_lrd_and_code_span_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo `copy` gle][] | ![Goo `copy` gle][] |
|N|No|

[Goo `copy` gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:24: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:44: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_collapsed_image_with_lrd_and_emphasis_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo **copy** gle][] | ![Goo **copy** gle][] |
|N|No|

[Goo **copy** gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:24: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:26: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:48: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_image_without_lrd_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Google] | ![Google] |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:24: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_image_with_lrd_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Google] | ![Google] |
|N|No|

[Google]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:24: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_image_with_lrd_and_special_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo&gle] | ![Goo&gle] |
|N|No|

[Goo&gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:13: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:15: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:26: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_image_with_lrd_and_backslash_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo\\$gle] | ![Goo\\$gle] |
|N|No|

[Goo\\$gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:16: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:28: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_image_with_lrd_and_entity_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo&copy;gle] | ![Goo&copy;gle] |
|N|No|

[Goo&copy;gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:18: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:20: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:36: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_image_with_lrd_and_code_span_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo `copy` gle] | ![Goo `copy` gle] |
|N|No|

[Goo `copy` gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:20: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:40: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_shortcut_image_with_lrd_and_emphasis_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| ![Goo **copy** gle] | ![Goo **copy** gle] |
|N|No|

[Goo **copy** gle]: http://google.com
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:24: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:44: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_autolinks_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| <http://www.google.com> | <someone@somewhere.com> |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:26: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:28: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:52: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_html_in_first_row",
        source_file_contents="""|Character|Meaning|
|---|---|
| A<br/>B | A<br>B |
|N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        disable_rules="md033",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:19: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_tight_column_style_with_aligned_delimiter",
        source_file_contents="""|Character|Meaning|
|---|---|
| A<br/>B | A<br>B |
|N|No|
""",
        set_args=[
            "plugins.md060.style=tight",
            "plugins.md060.aligned_delimiter=$!True",
        ],
        enable_extensions="markdown-tables",
        disable_rules="md033",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:5: MD060: Table column style. [Style: aligned-delimiter Expected-Column: 11 Actual-Column: 5] (table-column-style)
{temp_source_path}:2:9: MD060: Table column style. [Style: aligned-delimiter Expected-Column: 19 Actual-Column: 9] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:19: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_implicit_compact_column_style",
        source_file_contents="""| Character | Meaning |
| --- | --- |
| Y | Yes |
| N | No |
""",
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_implicit_compact_column_style_with_tight_second_column",
        source_file_contents="""| Character | Meaning |
| --- | --- |
| Y |Yes|
| N |No|
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:9: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:8: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_explicit_compact_column_style",
        source_file_contents="""| Character | Meaning |
| --- | --- |
| Y | Yes |
| N | No |
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_explicit_compact_column_style_with_tight_second_column",
        source_file_contents="""| Character | Meaning |
| --- | --- |
| Y |Yes|
| N |No|
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:9: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:8: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)

""",
    ),
    pluginRuleTest(
        "bad_explicit_compact_column_style_with_empty_column",
        source_file_contents="""| Character | Meaning |
| --- | --- |
| Y ||
| N ||
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)

""",
    ),
    pluginRuleTest(
        "bad_explicit_compact_column_style_with_tight_styled_table",
        source_file_contents="""|Character|Meaning|
|---|---|
|Y|Yes|
|N|No|
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:19: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:5: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:9: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:7: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_compact_column_style_with_tight_styled_table_no_starting_bar",
        source_file_contents="""Character|Meaning|
---|---|
Y|Yes|
N|No|
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:10: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:18: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:5: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:5: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_compact_column_style_with_tight_styled_table_title_no_starting_bar",
        source_file_contents="""Character|Meaning|
|---|---|
|Y|Yes|
|N|No|
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:10: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:18: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:5: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:9: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:7: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_compact_column_style_with_tight_styled_table_separator_no_starting_bar",
        source_file_contents="""|Character|Meaning|
---|---|
|Y|Yes|
|N|No|
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:19: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:5: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:8: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:7: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_compact_column_style_with_tight_styled_table_row_no_starting_bar",
        source_file_contents="""|Character|Meaning|
|---|---|
Y|Yes|
|N|No|
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:19: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:5: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:9: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_compact_column_style_with_tight_styled_table_no_ending_bar",
        source_file_contents="""|Character|Meaning
|---|---
|Y|Yes
|N|No
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:5: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_compact_column_style_with_tight_styled_table_title_no_ending_bar",
        source_file_contents="""|Character|Meaning
|---|---|
|Y|Yes|
|N|No|
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:5: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:9: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:7: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_compact_column_style_with_tight_styled_table_separator_no_ending_bar",
        source_file_contents="""|Character|Meaning|
|---|---
|Y|Yes|
|N|No|
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:19: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:5: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:7: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_compact_column_style_with_tight_styled_table_row_no_ending_bar",
        source_file_contents="""|Character|Meaning|
|---|---|
|Y|Yes
|N|No|
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:12: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:1:19: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:5: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:2:9: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_compact_column_style_with_aligned_delimiter",
        source_file_contents="""| Character | Meaning |
| --- | --- |
|A<br/>B|A<br>B|
|N|No|
""",
        set_args=[
            "plugins.md060.style=compact",
            "plugins.md060.aligned_delimiter=$!True",
        ],
        enable_extensions="markdown-tables",
        disable_rules="md033",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:7: MD060: Table column style. [Style: aligned-delimiter Expected-Column: 13 Actual-Column: 7] (table-column-style)
{temp_source_path}:2:13: MD060: Table column style. [Style: aligned-delimiter Expected-Column: 23 Actual-Column: 13] (table-column-style)
{temp_source_path}:3:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:9: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:16: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:2: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_implicit_aligned_column_style",
        source_file_contents="""
| Character | Meaning |
|-----------|---------|
| Y         |      Yes|
| N         |       No|
""",
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_implicit_aligned_column_style_with_compact_second_column",
        source_file_contents="""
| Character | Meaning |
| --------- | ------- |
| Y         | Yes |
| N         | No |
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:19: MD060: Table column style. [Style: aligned Expected-Column: 23 Actual-Column: 19] (table-column-style)
{temp_source_path}:5:18: MD060: Table column style. [Style: aligned Expected-Column: 23 Actual-Column: 18] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_implicit_aligned_column_style_with_tight_second_column",
        source_file_contents="""
| Character | Meaning |
| --------- |---      |
|          Y|Yes|
|          N|No|
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:17: MD060: Table column style. [Style: aligned Expected-Column: 23 Actual-Column: 17] (table-column-style)
{temp_source_path}:5:16: MD060: Table column style. [Style: aligned Expected-Column: 23 Actual-Column: 16] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_explicit_aligned_column_style",
        source_file_contents="""
| Character | Meaning |
| --------- | ------- |
| Y         | Yes     |
| N         | No      |
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_explicit_aligned_column_style_missing_leading",
        source_file_contents="""
| Character | Meaning |
  --------- | ------- |
Y           | Yes     |
N           | No      |
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
{temp_source_path}:4:1: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
{temp_source_path}:5:1: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_aligned_column_style_empty_column",
        source_file_contents="""
| Character | Meaning |
| --------- | ------- |
| Y         ||
| N         ||
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:14: MD060: Table column style. [Style: aligned Expected-Column: 23 Actual-Column: 14] (table-column-style)
{temp_source_path}:5:14: MD060: Table column style. [Style: aligned Expected-Column: 23 Actual-Column: 14] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_aligned_column_style_missing_leading_with_ws",
        source_file_contents="""
| Character | Meaning |
  --------- | ------- |
  Y         | Yes     |
  N         | No      |
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
{temp_source_path}:5:3: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_aligned_column_style_extra_leading",
        source_file_contents="""
Character | Meaning |
| ------- | ------- |
| Y       | Yes     |
| N       | No      |
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD060: Table column style. [Style: aligned Expected-Leading: False Actual-Leading: True] (table-column-style)
{temp_source_path}:4:1: MD060: Table column style. [Style: aligned Expected-Leading: False Actual-Leading: True] (table-column-style)
{temp_source_path}:5:1: MD060: Table column style. [Style: aligned Expected-Leading: False Actual-Leading: True] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_aligned_column_style_varied_leading_ws",
        source_file_contents="""
 | Character | Meaning |
  | ---------| ------- |
   | Y       | Yes     |
| N          | No      |
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD060: Table column style. [Style: aligned Expected-Column: 2 Actual-Column: 3] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: aligned Expected-Column: 2 Actual-Column: 4] (table-column-style)
{temp_source_path}:5:1: MD060: Table column style. [Style: aligned Expected-Column: 2 Actual-Column: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_aligned_column_style_missing_ending",
        source_file_contents="""
| Character | Meaning |
| --------- | -------
| Y         | Yes
| N         | No
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:22: MD060: Table column style. [Style: aligned Expected-Trailing: True Actual-Trailing: False] (table-column-style)
{temp_source_path}:4:18: MD060: Table column style. [Style: aligned Expected-Trailing: True Actual-Trailing: False] (table-column-style)
{temp_source_path}:5:17: MD060: Table column style. [Style: aligned Expected-Trailing: True Actual-Trailing: False] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_explicit_aligned_column_style_extra_ending",
        source_file_contents="""
| Character | Meaning
| --------- | ------- |
| Y         | Yes     |
| N         | No      |
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:24: MD060: Table column style. [Style: aligned Expected-Trailing: False Actual-Trailing: True] (table-column-style)
{temp_source_path}:4:24: MD060: Table column style. [Style: aligned Expected-Trailing: False Actual-Trailing: True] (table-column-style)
{temp_source_path}:5:24: MD060: Table column style. [Style: aligned Expected-Trailing: False Actual-Trailing: True] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_bq_implicit_tight_column_style",
        source_file_contents="""> |Character|Meaning|
> |---|---|
> |Y|Yes|
> |N|No|
""",
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_bq_implicit_tight_column_style_with_compact_first_column_content",
        source_file_contents="""> | Character |Meaning|
> |---|---|
> | Y |Yes|
> | N |No|
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_bq_explicit_tight_column_style",
        source_file_contents="""> |Character|Meaning|
> |---|---|
> |Y|Yes|
> |N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_bq_explicit_tight_column_style_with_compact_second_column",
        source_file_contents="""> |Character|Meaning|
> |---|---|
> |Y| Yes |
> |N| No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_bq_implicit_compact_column_style",
        source_file_contents="""> | Character | Meaning |
> | --- | --- |
> | Y | Yes |
> | N | No |
""",
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_bq_implicit_compact_column_style_with_tight_second_column",
        source_file_contents="""> | Character | Meaning |
> | --- | --- |
> | Y |Yes|
> | N |No|
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:8: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:8: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:10: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_bq_explicit_compact_column_style",
        source_file_contents="""> | Character | Meaning |
> | --- | --- |
> | Y | Yes |
> | N | No |
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_bq_explicit_compact_column_style_with_tight_second_column",
        source_file_contents="""> | Character | Meaning |
> | --- | --- |
> | Y |Yes|
> | N |No|
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:8: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:8: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:10: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)

""",
    ),
    pluginRuleTest(
        "good_bq_implicit_aligned_column_style",
        source_file_contents="""
> | Character | Meaning |
> |-----------|---------|
> | Y         |      Yes|
> | N         |       No|
""",
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_bq_implicit_aligned_column_style_with_compact_second_column",
        source_file_contents="""
> | Character | Meaning |
> | --------- | ------- |
> | Y         | Yes |
> | N         | No |
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:21: MD060: Table column style. [Style: aligned Expected-Column: 25 Actual-Column: 21] (table-column-style)
{temp_source_path}:5:20: MD060: Table column style. [Style: aligned Expected-Column: 25 Actual-Column: 20] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_bq_implicit_aligned_column_style_with_tight_second_column",
        source_file_contents="""
> | Character | Meaning |
> | --------- |---      |
> |          Y|Yes|
> |          N|No|
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:19: MD060: Table column style. [Style: aligned Expected-Column: 25 Actual-Column: 19] (table-column-style)
{temp_source_path}:5:18: MD060: Table column style. [Style: aligned Expected-Column: 25 Actual-Column: 18] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_bq_explicit_aligned_column_style",
        source_file_contents="""
> | Character | Meaning |
> | --------- | ------- |
> | Y         | Yes     |
> | N         | No      |
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_bq_explicit_aligned_column_style_missing_leading",
        source_file_contents="""
> | Character | Meaning |
> ----------- | ------- |
> Y           | Yes     |
> N           | No      |
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
{temp_source_path}:5:3: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_ul_implicit_tight_column_style",
        source_file_contents="""+ |Character|Meaning|
  |---|---|
  |Y|Yes|
  |N|No|
""",
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_ul_implicit_tight_column_style_with_compact_first_column_content",
        source_file_contents="""+ | Character |Meaning|
  |---|---|
  | Y |Yes|
  | N |No|
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_ul_explicit_tight_column_style",
        source_file_contents="""+ |Character|Meaning|
  |---|---|
  |Y|Yes|
  |N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_ul_explicit_tight_column_style_with_compact_second_column",
        source_file_contents="""+ |Character|Meaning|
  |---|---|
  |Y| Yes |
  |N| No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:6: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_ul_implicit_compact_column_style",
        source_file_contents="""+ | Character | Meaning |
  | --- | --- |
  | Y | Yes |
  | N | No |
""",
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_ul_implicit_compact_column_style_with_tight_second_column",
        source_file_contents="""+ | Character | Meaning |
  | --- | --- |
  | Y |Yes|
  | N |No|
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:8: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:8: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:10: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_ul_explicit_compact_column_style",
        source_file_contents="""+ | Character | Meaning |
  | --- | --- |
  | Y | Yes |
  | N | No |
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_ul_explicit_compact_column_style_with_tight_second_column",
        source_file_contents="""+ | Character | Meaning |
  | --- | --- |
  | Y |Yes|
  | N |No|
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:8: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:8: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:10: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)

""",
    ),
    pluginRuleTest(
        "good_ul_implicit_aligned_column_style",
        source_file_contents="""
+ | Character | Meaning |
  |-----------|---------|
  | Y         |      Yes|
  | N         |       No|
""",
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_ul_implicit_aligned_column_style_with_compact_second_column",
        source_file_contents="""
+ | Character | Meaning |
  | --------- | ------- |
  | Y         | Yes |
  | N         | No |
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:21: MD060: Table column style. [Style: aligned Expected-Column: 25 Actual-Column: 21] (table-column-style)
{temp_source_path}:5:20: MD060: Table column style. [Style: aligned Expected-Column: 25 Actual-Column: 20] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_ul_implicit_aligned_column_style_with_tight_second_column",
        source_file_contents="""
+ | Character | Meaning |
  | --------- |---      |
  |          Y|Yes|
  |          N|No|
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:19: MD060: Table column style. [Style: aligned Expected-Column: 25 Actual-Column: 19] (table-column-style)
{temp_source_path}:5:18: MD060: Table column style. [Style: aligned Expected-Column: 25 Actual-Column: 18] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_ul_explicit_aligned_column_style",
        source_file_contents="""
+ | Character | Meaning |
  | --------- | ------- |
  | Y         | Yes     |
  | N         | No      |
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_ul_explicit_aligned_column_style_missing_leading",
        source_file_contents="""
+ | Character | Meaning |
  ----------- | ------- |
  Y           | Yes     |
  N           | No      |
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:3: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
{temp_source_path}:4:3: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
{temp_source_path}:5:3: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_ol_implicit_tight_column_style",
        source_file_contents="""1. |Character|Meaning|
   |---|---|
   |Y|Yes|
   |N|No|
""",
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_ol_implicit_tight_column_style_with_compact_first_column_content",
        source_file_contents="""1. | Character |Meaning|
   |---|---|
   | Y |Yes|
   | N |No|
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:1:5: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:1:15: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:5: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:7: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:5: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:7: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_ol_explicit_tight_column_style",
        source_file_contents="""1. |Character|Meaning|
   |---|---|
   |Y|Yes|
   |N|No|
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_ol_explicit_tight_column_style_with_compact_second_column",
        source_file_contents="""1. |Character|Meaning|
   |---|---|
   |Y| Yes |
   |N| No |
""",
        set_args=["plugins.md060.style=tight"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:7: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:3:11: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:7: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:4:10: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_ol_implicit_compact_column_style",
        source_file_contents="""1. | Character | Meaning |
   | --- | --- |
   | Y | Yes |
   | N | No |
""",
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_ol_implicit_compact_column_style_with_tight_second_column",
        source_file_contents="""1. | Character | Meaning |
   | --- | --- |
   | Y |Yes|
   | N |No|
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:9: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:12: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_ol_explicit_compact_column_style",
        source_file_contents="""1. | Character | Meaning |
   | --- | --- |
   | Y | Yes |
   | N | No |
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_ol_explicit_compact_column_style_with_tight_second_column",
        source_file_contents="""1. | Character | Meaning |
   | --- | --- |
   | Y |Yes|
   | N |No|
""",
        set_args=["plugins.md060.style=compact"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:9: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:3:12: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:9: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)
{temp_source_path}:4:11: MD060: Table column style. [Style: compact Expected-Whitespace: 1 Actual-Whitespace: 0] (table-column-style)

""",
    ),
    pluginRuleTest(
        "good_ol_implicit_aligned_column_style",
        source_file_contents="""
1. | Character | Meaning |
   |-----------|---------|
   | Y         |      Yes|
   | N         |       No|
""",
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_ol_implicit_aligned_column_style_with_compact_second_column",
        source_file_contents="""
1. | Character | Meaning |
   | --------- | ------- |
   | Y         | Yes |
   | N         | No |
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:22: MD060: Table column style. [Style: aligned Expected-Column: 26 Actual-Column: 22] (table-column-style)
{temp_source_path}:5:21: MD060: Table column style. [Style: aligned Expected-Column: 26 Actual-Column: 21] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_ol_implicit_aligned_column_style_with_tight_second_column",
        source_file_contents="""
1. | Character | Meaning |
   | --------- |---      |
   |          Y|Yes|
   |          N|No|
""",
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:20: MD060: Table column style. [Style: aligned Expected-Column: 26 Actual-Column: 20] (table-column-style)
{temp_source_path}:5:19: MD060: Table column style. [Style: aligned Expected-Column: 26 Actual-Column: 19] (table-column-style)
""",
    ),
    pluginRuleTest(
        "good_ol_explicit_aligned_column_style",
        source_file_contents="""
1. | Character | Meaning |
   | --------- | ------- |
   | Y         | Yes     |
   | N         | No      |
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
    ),
    pluginRuleTest(
        "bad_ol_explicit_aligned_column_style_missing_leading",
        source_file_contents="""
1. | Character | Meaning |
   ----------- | ------- |
   Y           | Yes     |
   N           | No      |
""",
        set_args=["plugins.md060.style=aligned"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
{temp_source_path}:4:4: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
{temp_source_path}:5:4: MD060: Table column style. [Style: aligned Expected-Leading: True Actual-Leading: False] (table-column-style)
""",
    ),
    pluginRuleTest(
        "bad_tight_with_aligned",
        source_file_contents="""
| Character | Meaning | French | Spanish |
| --------- | :------ | -----: | :-----: |
|Y|Yes|Oui|Si|
|N|No|Non|No|
""",
        set_args=["plugins.md060.style=tight","plugins.md060.aligned_delimiter=$!True"],
        enable_extensions="markdown-tables",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:2: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:12: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:14: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:22: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:24: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:31: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:33: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
{temp_source_path}:2:41: MD060: Table column style. [Style: tight Expected-Whitespace: 0 Actual-Whitespace: 1] (table-column-style)
""",
    ),
]


@pytest.mark.rules
@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md060_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md054.
    """
    execute_scan_test(test, "md060")


@pytest.mark.rules
@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md060_config(test: pluginConfigErrorTest) -> None:
    """
    Execute a parameterized fix test for plugin md054.
    """
    execute_configuration_test(test, f"{source_path}bad_fenced_backticks_and_tildes.md")


@pytest.mark.rules
def test_md060_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md060",
        """
  ITEM               DESCRIPTION

  Id                 md060
  Name(s)            table-column-style
  Short Description  Table column style.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md060.md


  CONFIGURATION ITEM  TYPE     VALUE

  style               string   "any"
  aligned_delimiter   boolean  False
""",
    )
    execute_query_configuration_test(config_test)
