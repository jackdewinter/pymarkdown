"""
Module to provide tests related to the MD012 rule.
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

source_path = os.path.join("test", "resources", "rules", "md012") + os.sep

configTests = [
    pluginConfigErrorTest(
        "bad_configuration_maximum",
        use_strict_config=True,
        set_args=["plugins.md012.maximum=$#-2"],
        expected_error="""BadPluginError encountered while configuring plugins:
The value for property 'plugins.md012.maximum' is not valid: Allowable values are any non-negative integers.""",
    ),
]

scanTests = [
    pluginRuleTest(
        "good_simple_paragraphs_single_blanks",
        source_file_contents="""this is one line

this is another line
""",
    ),
    pluginRuleTest(
        "bad_simple_paragraphs_double_blanks",
        source_file_contents="""this is one line


this is another line
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""this is one line

this is another line
""",
    ),
    pluginRuleTest(
        "good_simple_paragraphs_double_blanks",
        source_file_contents="""this is one line


this is another line
""",
        set_args=["plugins.md012.maximum=$#2"],
    ),
    pluginRuleTest(
        "bad_simple_paragraphs_triple_blanks",
        source_file_contents="""this is one line



this is another line
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)""",
        fix_expected_file_contents="""this is one line

this is another line
""",
    ),
    pluginRuleTest(
        "bad_double_blanks_at_end",
        source_file_contents="""this is a line

""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""this is a line
""",
    ),
    pluginRuleTest(
        "good_multiple_blanks_in_fenced",
        source_file_contents="""```Markdown
this is a line


this is another line
```
""",
    ),
    pluginRuleTest(
        "good_multiple_blanks_in_indented",
        source_file_contents="""this is outside the code block

    this is a line


    this is another line

this is outside the code block
""",
    ),
    pluginRuleTest(
        "bad_multiple_blanks_in_html",
        source_file_contents="""<!--


-->
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""<!--

-->
""",
    ),
    pluginRuleTest(
        "good_blanks_around_single_pragma",
        source_file_contents="""Some markdown here

<!--pyml disable-num-lines 5 md013-->

My 10 lines
""",
    ),
    pluginRuleTest(
        "bad_blanks_double_around_single_pragma",
        source_file_contents="""Some markdown here


<!--pyml disable-num-lines 5 md013-->


My 10 lines
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)
{temp_source_path}:6:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""Some markdown here

<!--pyml disable-num-lines 5 md013-->

My 10 lines
""",
    ),
    pluginRuleTest(
        "bad_blanks_double_within_double_pragmas",
        source_file_contents="""Some markdown here

<!--pyml disable-num-lines 5 md013-->


<!--pyml disable-num-lines 5 md013-->

My 10 lines
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""Some markdown here

<!--pyml disable-num-lines 5 md013-->

<!--pyml disable-num-lines 5 md013-->

My 10 lines
""",
    ),
    pluginRuleTest(
        "bad_blanks_double_around_double_pragmas",
        source_file_contents="""Some markdown here


<!--pyml disable-num-lines 5 md013-->


<!--pyml disable-num-lines 5 md013-->


My 10 lines
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)
{temp_source_path}:6:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)
{temp_source_path}:9:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""Some markdown here

<!--pyml disable-num-lines 5 md013-->

<!--pyml disable-num-lines 5 md013-->

My 10 lines
""",
    ),
    pluginRuleTest(
        "bad_block_quote_with_double_blanks_at_middle",
        source_file_contents="""> this is a start
>
>
> this is an end
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""> this is a start
>
> this is an end
""",
    ),
    pluginRuleTest(
        "bad_block_quote_with_triple_blanks_at_middle",
        source_file_contents="""> this is a start
>
>
>
> this is an end
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:2: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)""",
        fix_expected_file_contents="""> this is a start
>
> this is an end
""",
    ),
    pluginRuleTest(
        "bad_block_quote_with_double_blanks_at_start",
        source_file_contents=""">
>
> this is an end
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:2: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents=""">
> this is an end
""",
    ),
    pluginRuleTest(
        "bad_block_quote_with_double_blanks_at_end",
        source_file_contents="""> this is a start
>
>
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""> this is a start
>
""",
    ),
    pluginRuleTest(
        "bad_block_quote_with_double_double_blanks",
        source_file_contents="""> this is a start
>
>
> this is the middle
>
>
> this is an end
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)
{temp_source_path}:6:2: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""> this is a start
>
> this is the middle
>
> this is an end
""",
    ),
    pluginRuleTest(
        "bad_in_list_with_double_blanks_at_middle",
        source_file_contents="""1. fred


   fred2
1. barney
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""1. fred

   fred2
1. barney
""",
    ),
    pluginRuleTest(
        "bad_in_list_with_triple_blanks_at_middle",
        source_file_contents="""1. fred



   fred2
1. barney
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""1. fred

   fred2
1. barney
""",
    ),
    pluginRuleTest(
        "bad_in_list_with_new_list_with_double_blanks_at_middle",
        source_file_contents="""1. betty
1. fred


   fred2
1. barney
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""1. betty
1. fred

   fred2
1. barney
""",
    ),
    pluginRuleTest(  # test_extra_051a1
        "bad_in_list_with_double_blanks_at_start",
        source_file_contents="""1.

   fred2
1. barney
""",
        scan_expected_return_code=0,
        disable_rules="md009",
    ),
    pluginRuleTest(  # test_extra_051a0
        "bad_in_list_with_double_blanks_at_end",
        source_file_contents="""1. fred


1. barney
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""1. fred

1. barney
""",
    ),
    pluginRuleTest(
        "bad_in_list_with_newlist_with_double_blanks_at_end",
        source_file_contents="""1. fred
1. barney


""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""1. fred
1. barney
""",
    ),
    pluginRuleTest(
        "bad_in_list_with_double_newlist_with_double_blanks_at_end",
        source_file_contents="""1. fred
1. barney
1. betty


""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""1. fred
1. barney
1. betty
""",
    ),
    pluginRuleTest(
        "bad_in_list_with_double_double_blanks",
        source_file_contents="""1. fred


   fred2


   fred3
1. barney
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)
{temp_source_path}:6:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""1. fred

   fred2

   fred3
1. barney
""",
    ),
    pluginRuleTest(
        "bad_block_quote_in_block_quote_with_double_blanks_at_middle",
        source_file_contents="""> > this is a start
> >
> >
> > this is an end
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""> > this is a start
> >
> > this is an end
""",
    ),
    pluginRuleTest(
        "bad_block_quote_in_block_quote_with_triple_blanks_at_middle",
        source_file_contents="""> > this is a start
> >
> >
> >
> > this is an end
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)""",
        fix_expected_file_contents="""> > this is a start
> >
> > this is an end
""",
    ),
    pluginRuleTest(
        "bad_block_quote_in_block_quote_with_double_blanks_at_start",
        source_file_contents="""> >
> >
> > this is an end
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:4: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""> >
> > this is an end
""",
    ),
    pluginRuleTest(
        "bad_block_quote_in_block_quote_with_double_blanks_at_end",
        source_file_contents="""> > this is a start
> >
> >
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""> > this is a start
> >
""",
    ),
    pluginRuleTest(
        "bad_block_quote_in_block_quote_with_double_double_blanks",
        source_file_contents="""> > this is a start
> >
> >
> > this is the middle
> >
> >
> > this is an end
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)
{temp_source_path}:6:4: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""> > this is a start
> >
> > this is the middle
> >
> > this is an end
""",
    ),
    pluginRuleTest(
        "bad_block_quote_in_list_with_double_blanks_at_middle",
        source_file_contents="""+ > this is a start
  >
  >
  > this is an end
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""+ > this is a start
  >
  > this is an end
""",
    ),
    pluginRuleTest(
        "bad_block_quote_in_list_with_triple_blanks_at_middle",
        source_file_contents="""+ > this is a start
  >
  >
  >
  > this is an end
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:4: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)""",
        fix_expected_file_contents="""+ > this is a start
  >
  > this is an end
""",
    ),
    pluginRuleTest(
        "bad_block_quote_in_list_with_double_blanks_at_start",
        source_file_contents="""+ >
  >
  > this is an end
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:2:4: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""+ >
  > this is an end
""",
    ),
    pluginRuleTest(
        "bad_block_quote_in_list_with_double_blanks_at_end",
        source_file_contents="""+ > this is a start
  >
  >
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""+ > this is a start
  >
""",
    ),
    pluginRuleTest(
        "bad_block_quote_in_list_with_double_double_blanks",
        source_file_contents="""+ > this is a start
  >
  >
  > this is the middle
  >
  >
  > this is an end
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:4: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)
{temp_source_path}:6:4: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        fix_expected_file_contents="""+ > this is a start
  >
  > this is the middle
  >
  > this is an end
""",
    ),
    pluginRuleTest(
        "bad_in_list_in_list_with_double_blanks_at_middle",
        source_file_contents="""+ 1. fred


     fred2
+ 1. barney
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""+ 1. fred

     fred2
+ 1. barney
""",
    ),
    pluginRuleTest(
        "bad_in_list_in_list_with_triple_blanks_at_middle",
        source_file_contents="""+ 1. fred



     fred2
+ 1. barney
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""+ 1. fred

     fred2
+ 1. barney
""",
    ),
    pluginRuleTest(  # test_extra_051c0
        "bad_in_list_in_list_with_double_blanks_at_start",
        source_file_contents="""+ 1.

     fred2
  1. barney
""",
        scan_expected_return_code=0,
        disable_rules="md009",
    ),
    pluginRuleTest(
        "bad_in_list_in_list_with_newlist_with_double_blanks_at_end",
        source_file_contents="""+ 1. fred
  1. barney


""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:5:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""+ 1. fred
  1. barney
""",
    ),
    pluginRuleTest(
        "bad_in_list_in_list_with_double_newlist_with_double_blanks_at_end",
        source_file_contents="""+ 1. fred
  1. barney
  1. betty


""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:6:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""+ 1. fred
  1. barney
  1. betty
""",
    ),
    pluginRuleTest(
        "bad_in_list_in_list_with_double_double_blanks",
        source_file_contents="""+ 1. fred


     fred2


     fred3
+ 1. barney
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)
{temp_source_path}:6:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""+ 1. fred

     fred2

     fred3
+ 1. barney
""",
    ),
    pluginRuleTest(
        "bad_in_list_in_block_quote_with_double_blanks_at_middle",
        source_file_contents="""> 1. fred
>
>
>    fred2
> 1. barney
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md009",
        # use_fix_debug=True,
        fix_expected_file_contents="""> 1. fred
>
>    fred2
> 1. barney
""",
    ),
    pluginRuleTest(  # test_extra_051b0 test_extra_051b1
        "bad_in_list_in_block_quote_with_triple_blanks_at_middle",
        source_file_contents="""> 1. fred
>
>
>
>    fred2
> 1. barney
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:4:2: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 3] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""> 1. fred
>
>    fred2
> 1. barney
""",
    ),
    pluginRuleTest(  # test_extra_051a2
        "bad_in_list_in_block_quote_with_double_blanks_at_start",
        source_file_contents="""> 1.
>
>    fred2
> 1. barney
""",
        scan_expected_return_code=0,
        disable_rules="md027",
    ),
    pluginRuleTest(
        "bad_in_list_in_block_quote_with_double_blanks_at_end",
        source_file_contents="""> 1. fred
>
>
> 1. barney
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""> 1. fred
>
> 1. barney
""",
    ),
    pluginRuleTest(
        "bad_in_list_in_block_quote_with_double_double_blanks",
        source_file_contents="""> 1. fred
>
>
>    fred2
>
>
>    fred3
> 1. barney
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:3:2: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)
{temp_source_path}:6:2: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md009",
        fix_expected_file_contents="""> 1. fred
>
>    fred2
>
>    fred3
> 1. barney
""",
    ),
    pluginRuleTest(
        "issue-1326-a",
        source_file_contents="""# z

z




<div class="grid cards" markdown>

-   z

-   z


-   z
</div>
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 4] (no-multiple-blanks)
{temp_source_path}:14:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md030,md032,md033",
        fix_expected_file_contents="""# z

z

<div class="grid cards" markdown>

-   z

-   z

-   z
</div>
""",
    ),
    pluginRuleTest(
        "issue-1326-b",
        source_file_contents="""# z

z




<div class="grid cards" markdown>

-   z


-   z

-   z
</div>
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 4] (no-multiple-blanks)
{temp_source_path}:12:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md030,md032,md033",
        fix_expected_file_contents="""# z

z

<div class="grid cards" markdown>

-   z

-   z

-   z
</div>
""",
    ),
    pluginRuleTest(
        "issue-1326-c",
        source_file_contents="""# z

z

<div class="grid cards" markdown>

-   z


-   z

-   z
</div>
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:9:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md030,md032,md033",
        fix_expected_file_contents="""# z

z

<div class="grid cards" markdown>

-   z

-   z

-   z
</div>
""",
    ),
    pluginRuleTest(
        "issue-1326-d",
        source_file_contents="""# z

z




<div class="grid cards" markdown>

-   z

-   z

-   z


</div>
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:7:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 4] (no-multiple-blanks)
{temp_source_path}:16:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md030,md032,md033",
        fix_expected_file_contents="""# z

z

<div class="grid cards" markdown>

-   z

-   z

-   z

</div>
""",
    ),
    pluginRuleTest(
        "issue-1326-e",
        source_file_contents="""# z

z

<div class="grid cards" markdown>

-   z

-   z

-   z


</div>
""",
        scan_expected_return_code=1,
        scan_expected_output="""{temp_source_path}:13:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)""",
        disable_rules="md030,md032,md033",
        fix_expected_file_contents="""# z

z

<div class="grid cards" markdown>

-   z

-   z

-   z

</div>
""",
    ),
]


@pytest.mark.parametrize("test", scanTests, ids=id_test_plug_rule_fn)
def test_md012_scan(test: pluginRuleTest) -> None:
    """
    Execute a parameterized scan test for plugin md001.
    """
    execute_scan_test(test, "md012")


@pytest.mark.parametrize(
    "test", calculate_fix_tests(scanTests), ids=id_test_plug_rule_fn
)
def test_md012_fix(test: pluginRuleTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_fix_test(test)


@pytest.mark.parametrize("test", configTests, ids=id_test_plug_rule_fn)
def test_md012_config(test: pluginConfigErrorTest) -> None:
    """
    Execute a parameterized fix test for plugin md001.
    """
    execute_configuration_test(
        test,
        file_contents="""this is one line

this is another line
""",
    )


def test_md012_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md012",
        """
  ITEM               DESCRIPTION

  Id                 md012
  Name(s)            no-multiple-blanks
  Short Description  Multiple consecutive blank lines
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md012.md


  CONFIGURATION ITEM  TYPE     VALUE

  maximum             integer  1

""",
    )
    execute_query_configuration_test(config_test)
