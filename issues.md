# Bugs - General

## Priority 1 - Must Solve Before Initial

## Priority 2 - Like To Solve Before Initial

- make sure to generated ordered/unordered tests to make sure both covered
  - every unordered tests should have an ordered counterpart
  - every ordered tests should have an unordered counterpart

### nested lists

- 4+ levels of nesting
  - `test_list_blocks_271fx` and `test_list_blocks_271fa`

### Like To Have - Issues

- better solution than `no-space-in-code` for scenario-cases.md
- take `__consume_text_for_image_alt_text` and other functions like it and move as much as possible into token classes
  - TransformToGfmListLooseness.__handle_block_quote_start

### Like To Have - Features

- documentation for developers

- yaml support for front-matter
  - if front matter is found to be disqualified, send error?

- better globbing for 043

## Priority 3 - Like To Solve in next 3 m

### Rule ???

- is there a rule that can detect a possible front-matter header and trigger?
  i.e. something looks like front-matter and should be interpretted as front-matter
- within a given list or block quote, should only have one pattern of container tokens

### Other

- md023 - can line 61 search be done more efficiently by looking for `{space}\x02` ?
- in inline, does `if coalesced_stack and coalesced_stack[-1].is_block_quote_start:` really need
  to look for any bq on the stack?
- show url for failed rules as option
- combine traversal for 027 and 007?

- determine which errors to print and which to log
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

- (maintenance) look for cases where = True or = False, and see if can do an assignment
  easlier i.e. if x: d_a_d = False else: d_a_d = True

- (maintenance) clean up pylint warning suppressions where possible
  - too-many-locals
  - too-many-statements
  - too-many-branches
  - too-many-nested-blocks
  - too-many-lines
  - too-many-instance?

- more tests that include tab characters
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

## Priority 4 - Like To Solve in next 6 m

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

## Features - Extensions

- front matter
- tables
- task list items
- strikethrough
- disallowed raw html
- autolinks extension

## Features - Correctness - Whitespace and Punctuation

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
