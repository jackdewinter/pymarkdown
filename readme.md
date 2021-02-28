# Project To-Do List

## Bugs - Command Line

- determine which errors to print and which to log

## Bugs - General

### Priority 1 - Must Solve Before Initial

- why does hard break not have \n? (fix before release)
- track down uses of rehydrate_index in consistency checks and make to have cases to verify that each is updating properly, including multi
  - leading_text_index
- link and emphasis (inline) tokens cannot be forced close, rewrite end to not expose :::False?
- (performance) plugin set_context: fold in to normal calls to avoid 2nd call

### Priority 2 - Like To Solve Before Initial

- why does fcb with only newlines and newlines with ws not fold down to text?
  - coalesce with blank lines in fenced code block?
- make sure to generated ordered/unordered tests to make sure both covered
  - every unordered tests should have an ordered counterpart
  - every ordered tests should have an unordered counterpart

- take `__consume_text_for_image_alt_text` and other functions like it and move as much as possible into token classes
  - TransformToGfmListLooseness.__handle_block_quote_start
- switch from bq to list and back again
  - switch from list to bq and back again
  - 270 and check for indent levels after

- LRD + FCB in list/block
  - test_fenced_code_blocks_extra_02a
  - test_fenced_code_blocks_extra_03a
  - test_fenced_code_blocks_extra_06a
- LRD + HTML in list/block
  - test_html_blocks_extra_02x
  - test_html_blocks_extra_02a
  - test_html_blocks_extra_03a
  - test_html_blocks_extra_04a
  - test_html_blocks_extra_05a
  - test_html_blocks_extra_06a
- same as these, but with an extra level of list or block

- implement missing rules

### Priority 3 - Like To Solve in next 3 m

- (performance) debug: search for any cases where adding a call to `is_debug_enabled` would be helpful
- (performance) assert: do as little as possible to ensure better performance
- (performance) else: ??
- (performance) replace MarkdownToken properties like is_block_quote_end with more performant?
- (performance) count_characters_in_text
- (performance) can further eliminate len() calls by looking for places can calculate once and pass to child functions
- (performance) order of "if" conditions in critical areas
- (performance) are all "x and x.blah" requiring the "x" check first? can factor out?
- (performance) ParserHelper functions can be further optimized? i.e. __remove_backspaces_from_text and how combines
- (performance) handle_inline_backslash
- (performance) handle_character_reference

- (maintenance) clean up pylint warning suppressions where possible
  - too-many-locals
  - too-many-statements
  - too-many-branches
  - too-many-nested-blocks
  - too-many-lines
  - too-many-instance?

- look for places where common access patterns can be used i.e. link_title
  - `= len(parser_state.token_stack`
- HTML and Fenced Blocks and better handling of capturing newlines to avoid counting token height
- cases like 183 where first non-ws character is an inline specifier
  - can this be fixed in a way that does not require the other fix to add
   starting_whitespace after the fact?
- make better use of `index_indent`
- why does `__revert_token_to_normal_text_token` require TextMarkdown.copy instead of `replacement_token = text_token_to_replace.create_copy()`?
- image token handling confusing and non-standard
- fenced code block handling of line/col could be better
- LRD and block quote interaction - process_link_reference_definition - search for XXXXX
- `LOGGER.debug("handle_block_quote_section>>fenced")` and collapse?

### Priority 4 - Like To Solve in next 6 m

- verifying vs validating?
- bqp:check_for_lazy_handling, why exclude tb?
- unify 2 separate calculations in `__pre_list` function
- raise requeue_line_info instead of returning it?  worried about recursion points
- replace calculate_last_line with calculate_deltas with some work?
- is_complete_html_end_tag can be more concise, but worth it?
- modify_end_string. inline?
- is_valid_tag_name refactor using ParserHelper?
  - extract_html_attribute_name and others to use "in" where possible instead of "or"
- __calculate_full_deltas - calc_deltas from ParserHelper?
- __process_inline_text_block - calc_deltas from ParserHelper?
- is_length_less_than_or_equal_to(extracted_whitespace, 3) - calc once at start of leaf block proc?
- is_character_at_index_one_of inside of where? collect function?
- __parse_line_for_leaf_blocks - why calling count_of_block_quotes_on_stack so often?

## Bugs - General - Uncategorized

- None

## Ask talk.commonmark.org

- test_link_reference_definitions_extra_02b vs test_link_reference_definitions_extra_02c

## Bugs - Tabs

- should be able to have tabs and not trigger bad tokens, should be excluded?
- check is_length_less_than_or_equal_to to see if any issues with tabs
  - most likely in conjunction with starting another type of block
- 004
  - tab is consumed as part of list prefix, not recorded anywhere, assumed to be spaces
- variations on 005, mostly wired up for scenario
  - what about tabs with plain icode? different depths?
- effect of lists and blocks with 1 tab and differing amounts of whitespace on followed text i.e. `- \tfoo' should produced a list item with foo, no icb as it would equate to 2 spaces
- 235, 236, 252, 255
  - need to account for the fact that indent may not be all spaces all the time
  - for indented code blocks, starts at the start of the icb, else at the first non-ws

## Bugs - Rules - Rounding Out Rules

- MD018
  - for multiple occurrences inside of a single paragraph, reporting line/col of starting token
  - whitespace starts, etc.
  - lists and block quotes
- MD020
  - for multiple occurrences inside of a single paragraph, reporting line/col of starting token
  - whitespace starts, etc.
  - lists and block quotes
- MD022 - lists and block quotes and LRDs
- MD022 - should line 96-104 with all of the leaf node names be added to Markdown token?
- MD022 - what if the document had a paragraph before the first heading?

## Bugs - Rules - SetExt

- MD041 requires metadata
  - implemented MD043 at the same time
  - implement MD025 at the same time
- MD023 with inline that includes leading spaces?
- MD024 with whitespace, and inline differences
- MD024 level 2 (me), level 3 (my), level 2 (me) -  should fire? is considered siblings?

## Features - Extensions

- front matter
- tables
- task list items
- strikethrough
- disallowed raw html
- autolinks extension

## Features - Correctness - Whitespace and Punctuation

- go through each use of extract_whitespace and validate whether it should be e_space or e_whitespace
- scan GFM and ensure Unicode whitespace uses actual Unicode whitespace, not just whitespace
- complete list of Unicode punctuation characters
- Atx headings only consider space, not whitespace?
  - impact to MD018 to MD021?

## Features - Correctness

- go back and see if can replace some of the end token fiddling with start_markdown_token
- go through any case that uses lazy and do un-lazy example
- samples that end without a blank line, and add a blank line?

## Features - Performance

- reduce html_helper functions?
  - i.e. html_helper contains 2 for various elements?
- collect_until_one_of_characters with backslashes?
- rewrite transform to allow it to consume a Markdown file as it goes
- modify parse_blocks_pass to consume lines as it goes, instead of requiring entire string in memory

## document current restrictions

- nested block quotes and nested lists are okay, but not together
- no install/setup support currently

## Python performance

https://towardsdatascience.com/how-to-assess-your-code-performance-in-python-346a17880c9f

## xx

https://github.com/executablebooks/mdit-py-plugins/blob/master/mdit_py_plugins/front_matter/index.py
https://github.com/micromark/micromark
https://github.com/commonmark/commonmark-spec-web/blob/gh-pages/0.29/spec.txt
