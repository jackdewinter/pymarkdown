# Project To-Do List

## Bugs - Command Line

- determine which errors to print and which to log

## Bugs - General

### Priority 1 - Must Solve Before Initial

- test_paragraph_series_m_ul_t_nl_ulb_nl_tb - with abc/def/*

- possible to merge link token and image token more closely?

- Link_helper.py#86 - if link already registered, should warn?
- where is `elif starting_whitespace:` used? why? better way to do it?
- merge leading_spaces code from both container tokens
- why does hard break not have \n? (fix before release)
  - hard break followed by 3 spaces, then emphasis
  - variations of 52e with extra spaces after, etc.
    - variation with start of 52e, then hard break, then something like start of 52e again i.e. make /x02 splitter come into affect
  - hard break followed by each inline type
  - hard break at start of text?
- all types of end-inlines and inlines at end i.e. 50
- track down uses of rehydrate_index in consistency checks and make to have cases to verify that each is updating properly, including multi
  - rehydrate_index
  - leading_text_index
  - leading_spaces_index + is_loose

### Priority 2 - Like To Solve Before Initial

- look for `valid_raw_html = "\n".join(split_raw)` and see if can combine
- refactor `for stack_index in range(len(parser_state.token_stack) - 1, -1, -1):`
  from different areas into one helper function
  - leaf parse_paragraph
  - len(parser_state
- why does fcb with only newlines and newlines with ws not fold down to text?
  - coalesce with blank lines in fenced code block?
- check for common code in consistency checks, i.e. link and image handling
- make sure to generated ordered/unordered tests to make sure both covered
  - every unordered tests should have an ordered counterpart
  - every ordered tests should have an unordered counterpart
- link and emphasis (inline) tokens cannot be forced close, rewrite end to not expost :::False?

- unify 2 separate calculations in `__pre_list` function

### Priority 3 - Like To Solve in next 3 m

- look for places where common access patterns can be used i.e. link_title
- HTML and Fenced Blocks and better handling of capturing newlines to avoid counting token height
- cases like 183 where first non-ws character is an inline specifier
  - can this be fixed in a way that does not require the other fix to add
   starting_whitespace after the fact?
- make better use of `index_indent`
- why does `__revert_token_to_normal_text_token` require TextMarkdown.copy instead of `replacement_token = text_token_to_replace.create_copy()`?
- image token handling confusing and non-standard
- fenced code block handling of line/col could be better

### Priority 4 - Like To Solve in next 6 m

- verifying vs validating?
- bqp:check_for_lazy_handling, why exclude tb?

## Bugs - General - Uncategorized

- links, 518b
  - 518b inside of list and/or block quote
  - links with & and \ with inner link to mine
    - see __collect_text_from_blocks
- 634, but forcing an html block

## Bugs - Block Quote/List Interaction

- 270 and check for indent levels after
- verify that leading_text_index and list's version match up with expected at end of verify
- verify that leading_text_index and list's version match up with expected at end of markdown gen
- verify multi-line raw-html in different blocks, not only paragraph
  - inside of link - test_paragraph_series_j_l_rh_s_t
- verify multi-line code-spans in different blocks, not only paragraph
- check resolve/remove helpers for groupings per file type i.e. html, markdown, proc, verify
- check `__verify_next_inline_raw_html` for refactor

## Bugs - Tokenization

- should be able to have tabs and not trigger bad tokens, should be excluded?

## Bugs - Tabs

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
- look for cases where " " is used, and convert to whitespace helper
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
