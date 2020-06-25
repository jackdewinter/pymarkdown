# Project To-Do List

## Bugs - Command Line

- determine which errors to print and which to log

## Bugs - General

- need to add line/column for
  - text
  - inlines
- make better use of `index_indent`
- for all of the tokens that used position_marker, do we need =None any more?
- rewrite position_marker to not allow outside modification
  - requires clean up of how list and block quotes handle it
- add ex_ws into tokens for block quote, list starts, indented code block, html, and thematic break

## Bugs - Character Entities

- test_markdown_entity* various extra tests

## Bugs - SetExt

- MD041 requires metadata
  - implemented MD043 at the same time
  - implement MD025 at the same time
- MD023 with inline that includes leading spaces?
- MD024 with whitespace, and inline differences
- MD024 level 2 (me), level 3 (my), level 2 (me) -  should fire? is considered siblings?

## Bugs - Tabs

- check is_length_less_than_or_equal_to to see if any issues with tabs
  - most likely in conjunction with starting another type of block
- 004
  - tab is consumed as part of list prefix, not recorded anywhere, assumed to be spaces
- variations on 005, mostly wired up for scenario
  - what about tabs with plain icode? different depths?
- effect of lists and blocks with 1 tab and differing amounts of whitespace on followed text i.e. `- \tfoo' should produced a list item with foo, no icb as it would equate to 2 spaces

## Bugs - AutoLinks

- 620 - more bad cases, like <
- 603 - href? doesn't look right

## Bugs - Links

- test_link_reference_definitions_183 is a partial lrd followed by bq, add cont+leaf blocks
- Link_helper.py#86 - if link already registered, should warn?
- 296 and 297 - added in case for LRD, but need to test:
  - other types of blocks
  - block, blank, then multiple blocks

- inline link ( without any extra info
- why does GFM not specify that between [ and ] for a LRD, no blanks are allowed?
  - maybe expound on 166 a bit?
- what if bad link followed by good link?
- specific types of links for the 3 types?
- more testing to determine what in-lines are stripped within image links i.e. code spans?
- link ref def with empty link label, like 560?
- full reference link with empty link label, like 560?
- 553 with other in-lines?
- what if bad link definition discovered multiple lines down, how to back track?
- split up link definition within a block quote or list?

## Bugs - Rounding Out Rules

- MD018 - lists and block quotes
- MD020 - lists and block quotes
- MD022 - lists and block quotes and LRDs
- MD022 - should line 96-104 with all of the leaf node names be added to Markdown token?
- MD022 - what if the document had a paragraph before the first heading?

## Bugs - Block Quote

- block quotes that start and stop i.e. > then >> then > then >>>, etc.
- "# TODO add case with >" for tests
- 228 and 229 - what is the proper line/col for ">>>"?

## Bugs - List

- 257,260 - blank lines and lists, should put leading space in token

- blank line ending a list is parsed wrong into tokens
  - >>stack_count>>0>>#9:[end-ulist]
  - should be end and then blank, as the blank is outside of the list
- CommonMark and how handles non-initial cases for list starts

## Bugs - Tokenization

- 235, 236, 252, 255, etc - missing whitespace?
- setext rename .remaining_line to .extracted_whitespace & fix consistency check
- all leaf  in all container

- 262 - tokenization incorrect
  - 217, 219 same with block quotes
- 559, 560 - LRDs, huh?
- extra001, 002? correct ?
- blank lines, if starts with 2 ws, is it (x,1) or (x,3)?

## Bugs - Block Quote/List Interaction

- 300 with different list following
- 300 with extra indent on following item
- 301, but with extra levels of block quotes
- 301, with indented code blocks
- 270 and check for indent levels after

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

- can we generate Markdown from tokens? do we have enough info?
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
- currently do not pass one test with a link inside of an image link
- multi-line link reference definitions within a list of block quote not adequately tested
- no install/setup support currently
