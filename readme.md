# Project To-Do List

## Bugs - Command Line

- determine which errors to print and which to log

## Bugs - General

- add token for LRD
- need to add line/column for
  - setext
  - html
  - indented code block
  - fenced code block
  - blank lines
  - paragraph
  - text
  - list
    - refactor is_thematic_break
  - block quote
  - LRD
  - inlines

## Bugs - Character Entities

- test_markdown_entity* various extra tests

## Bugs - SetExt

- MD041 requires metadata

## Bugs - Tabs

- check is_length_less_than_or_equal_to to see if any issues with tabs
  - most likely in conjunction with starting another type of block

## Bugs - AutoLinks

- 620 - more bad cases, like <
- 603 - href? doesn't look right

## Bugs - Links

- Link_helper.py#86 - if link already registered, should warn?

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

## Bugs - Block Quote

- block quotes that start and stop i.e. > then >> then > then >>>, etc.
- "# TODO add case with >" for tests

## Bugs - List

- blank line ending a list is parsed wrong into tokens
  - >>stack_count>>0>>#9:[end-ulist]
  - should be end and then blank, as the blank is outside of the list
- CommonMark and how handles non-initial cases for list starts

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
