# Project To-Do List

## Bugs - Command Line

- determine which errors to print and which to log

## Bugs - General - Nice To Have

- verifying vs validating?

- use built in `is_x` functions instead of `token_name`
- end tokens should all have start tokens that caused them?
- why does fcb with only newlines and newlines with ws not fold down to text?
  - coalesce with blank lines in fenced code block?
- HTML and Fenced Blocks and better handling of capturing newlines to avoid counting token height
- Link_helper.py#86 - if link already registered, should warn?
- check for common code in consistency checks, i.e. link and image handling
- start making token fields private with setters
  - look for places where common access patterns can be used i.e. link_title

- cases like 183 where first non-ws character is an inline specifier
  - can this be fixed in a way that does not require the other fix to add
   starting_whitespace after the fact?
- where is `elif starting_whitespace:` used? why? better way to do it?

- make better use of `index_indent`
- merge leading_spaces code from both container tokens
- refactor `for stack_index in range(len(parser_state.token_stack) - 1, -1, -1):`
  from different areas into one helper function
  - leaf parse_paragraph
  - len(parser_state

- does post processing for Markdown transformer need to be complicated
- why does hard break not have \n? (fix before release)
  - hard break followed by 3 spaces, then emphasis
  - variations of 52e with extra spaces after, etc.
    - variation with start of 52e, then hard break, then something like start of 52e again i.e. make /x02 splitter come into affect
  - hard break followed by each inline type
  - hard break at start of text?
- unify 2 separate calculations in `__pre_list` function

- image token handling confusing and non-standard
- fenced code block handling of line/col could be better
- track down uses of rehydrate_index in consistency checks and make to have cases to verify that each is updating properly, including multi
- all types of end-inlines and inlines at end i.e. 50
- possible to merge link token and image token more closely?

## Bugs - General - Uncategorized

- 634a in bq and in list
- links, 518b
  - 518b inside of list and/or block quote
  - links with & and \ with inner link to mine

## Bugs - Block Quote

- tests like cov2 with blank before, after, and both for html blocks and other blocks
- tests like cov2 with multiple lines for block items, like html

## Bugs - Block Quote/List Interaction

- 300 with different list following
- 300 with extra indent on following item
- 301, but with extra levels of block quotes
- 301, with indented code blocks
- 270 and check for indent levels after
- check to make sure indents work properly for a list containing a block quote where the
  block quote ends and there is more data for that item within the list
- same as before, just a bq with a list
- split up link definition within a block quote or list?

## Bugs - Tokenization

- should be able to have tabs and not trigger bad tokens, should be excluded?
- all leaf in all container
- blank lines as part of bquote
  - compare test_block_quotes_218 vs test_blank_lines_197a
  - already fixed test_list_blocks_260, 257

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
- multi-line link reference definitions within a list of block quote not adequately tested
- no install/setup support currently
