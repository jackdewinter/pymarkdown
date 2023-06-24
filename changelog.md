# Change Log

## Unversioned - In Main, Not Released

### Added

- [Issue 655](https://github.com/jackdewinter/pymarkdown/issues/655)
  - Added support for `tool.pymarkdown` section in `pyproject.toml` for current directory

### Changed

- None

### Fixed

- None

## Version 0.9.10 - Date: 2023-04-16

### Added

- [Issue 627](https://github.com/jackdewinter/pymarkdown/issues/627)
  - Added support for default `.pymarkdown` configuration file
  - Updated documentation for configuration

### Changed

- None

### Fixed

- None

## Version 0.9.11 - Date: 2023-04-17

### Fixed

- Emergency fix.

## Version 0.9.10 - Date: 2023-04-16

### Added

- [Issue 627](https://github.com/jackdewinter/pymarkdown/issues/627)
  - Added support for default `.pymarkdown` configuration file
  - Updated documentation for configuration

### Changed

- [Issue 582](https://github.com/jackdewinter/pymarkdown/issues/582)
  - broke up leaf block processor into more distinct pieces
- [Issue 589](https://github.com/jackdewinter/pymarkdown/issues/589)
  - broke up token to GFM module into more distinct pieces
- [Issue 594](https://github.com/jackdewinter/pymarkdown/issues/594)
  - broke up token to link helper into more distinct pieces
- [Issue 596](https://github.com/jackdewinter/pymarkdown/issues/596)
  - broke up token to inline processor into more distinct pieces
- [Issue 598](https://github.com/jackdewinter/pymarkdown/issues/598)
  - broke up token to link reference definition helper into more distinct pieces
- [Issue 600](https://github.com/jackdewinter/pymarkdown/issues/600)
  - broke up html helper into more distinct pieces
- [Issue 603](https://github.com/jackdewinter/pymarkdown/issues/603)
  - broke up container block processor into more distinct pieces
- [Issue 605](https://github.com/jackdewinter/pymarkdown/issues/605)
  - broke up block quote processor
- [Issue 607](https://github.com/jackdewinter/pymarkdown/issues/607)
  - broke up list block processor
- [Issue 630](https://github.com/jackdewinter/pymarkdown/issues/630)
  - ensured that remaining whitespace tests have the standard combinations
    tested in the previous whitespace tests

### Fixed

- [Issue 613](https://github.com/jackdewinter/pymarkdown/issues/613)
  - fixed issues with tabs and thematic breaks
- [Issue 620](https://github.com/jackdewinter/pymarkdown/issues/620)
  - fixed issues with tabs and SetExt headings
- [Issue 622](https://github.com/jackdewinter/pymarkdown/issues/622)
  - fixed issues with tabs and paragraphs
- [Issue 625](https://github.com/jackdewinter/pymarkdown/issues/625)
  - fixed documentation to more clearly specifying the use of a comma-separated
    list for enabling and disabling rules
  - small change to list processing logic to strip whitespace between values,
    allowing for `md001 , md002` to equal `md001,md002`
- [Issue 626](https://github.com/jackdewinter/pymarkdown/issues/626)
  - fixed issue where parsing was not considering being in a code block before
    determining whether or not to start a list
- [Issue 634](https://github.com/jackdewinter/pymarkdown/issues/634)
  - fixed and tested various scenarios with lists that contain mostly or all
    link elements
- [Issue 637](https://github.com/jackdewinter/pymarkdown/issues/637)
  - fixed by adding extra examples and scenario tests to verify this is working
- [Issue 639](https://github.com/jackdewinter/pymarkdown/issues/639)
  - addressed inter-release issue of not specifying all code directories in
     the setup script after refactoring
  
## Version 0.9.9 - Date: 2023-02-26

This was a point release.  Issues that were addressed:

- proprly dealing with the reintegration of tabs into the HTML output
- ensuring that tabs are represented properly in the internal token format
- cleaning up code to reduce various `PyLint` errors

### Added

- [Issue 561](https://github.com/jackdewinter/pymarkdown/issues/561)
  - added Sourcery.Ai to analysis tools
    - made sure all code hits 40% Sourcery quality threshold
    - cleaned up testing scripts

### Changed

- various
  - updated build, publish, and analysis packages to latest versions
- [Issue 561](https://github.com/jackdewinter/pymarkdown/issues/561)
  - changed error output to filter through main module for more control
- [Issue 504](https://github.com/jackdewinter/pymarkdown/issues/504)
  - moved file logging code into own module
- [Issue 496](https://github.com/jackdewinter/pymarkdown/issues/496)
  - moved file scanner code into own module

### Fixed

- [Issue 561](https://github.com/jackdewinter/pymarkdown/issues/561)
  - worked to reduce the count of `too-many-locals` reported by `PyLint`
- [Issue 478](https://github.com/jackdewinter/pymarkdown/issues/478)
  - fixed false positive in reporting the start of the list
  - underlying issue was improper closing of the list, which was also fixed
- [Issue 453](https://github.com/jackdewinter/pymarkdown/issues/453)
  - still in progress
  - cleaning up reintegration of tabs into output

## Version 0.9.8 - Date: 2022-09-20

This was a point release.  Issues that were addressed:

- fixed issues with block quotes and other containers
- added support for file extensions other than .md
- added support for linting markdown from standard input
- cleared up issue with using proper path separators on Windows
- added and fixed tests for proper handling of whitespaces
- added proper support for Unicode whitespace and Unicode punctuation around emphasis elements
- updated all Python dependencies to their current versions

NOTE for Windows users:

Prior to this release, when executing PyMarkdown against a file on a Windows
machine, any paths were reported using the Posix format.  This has been
corrected as of the 0.9.8 release, with Linux and MacOs reporting paths
in Posix format and Windows reporting paths in Windows format.  If you have
scripts that invoke PyMarkdown and interprets any returned paths, please
examine those scripts to see if they need to be changed.

### Added

- [Issue 407](https://github.com/jackdewinter/pymarkdown/issues/407)
  - added support for other file extensions
- [Issue 413](https://github.com/jackdewinter/pymarkdown/issues/413)
  - added more variants for nested-three-block-block tests
- [Issue 441](https://github.com/jackdewinter/pymarkdown/issues/441)
  - added support for linting markdown from standard input
- [Issue 456](https://github.com/jackdewinter/pymarkdown/issues/456)
  - added lots of new tests for different forms of whitespace with each element
- [Issue 480](https://github.com/jackdewinter/pymarkdown/issues/480)
  - added proper support for Unicode whitespace and Unicode punctuation around emphasis elements

### Changed

- [Issue 168](https://github.com/jackdewinter/pymarkdown/issues/168)
  - moved paragraph handling code to own module
- [Issue 330](https://github.com/jackdewinter/pymarkdown/issues/330)
  - cleared up issue with using proper path separators on Windows
- [Issue 408](https://github.com/jackdewinter/pymarkdown/issues/408)
  - split tests for blocks into more discrete files
- [Issue 450](https://github.com/jackdewinter/pymarkdown/issues/450)
  - enabled proper tests for pragmas
- [Issue 454](https://github.com/jackdewinter/pymarkdown/issues/454)
  - fixed special HTML sequences that were detected by Md033

### Fixed

- [Issue 301](https://github.com/jackdewinter/pymarkdown/issues/301)
  - fixed issue where was checking indent_level instead of column_number
  - clarified documentation
- [Issue 410](https://github.com/jackdewinter/pymarkdown/issues/410)
  - not putting Markdown back together properly
- [Issue 419](https://github.com/jackdewinter/pymarkdown/issues/419)
  - fixed parsing issue with trailing spaces in empty list items
- [Issue 420](https://github.com/jackdewinter/pymarkdown/issues/420)
  - fix improper parsing with nested blocks quotes
- [Issue 421](https://github.com/jackdewinter/pymarkdown/issues/421)
  - Markdown was not put back together properly with weird Block Quote/List combinations
- [Issue 460](https://github.com/jackdewinter/pymarkdown/issues/460)
  - fixed up mismatching output with tabs
- [Issue 461](https://github.com/jackdewinter/pymarkdown/issues/461)
  - generated HTML not removing whitespace before and after paragraphs
- [Issue 465](https://github.com/jackdewinter/pymarkdown/issues/465)
  - not properly handling whitespace before fenced block info string
- [Issue 468](https://github.com/jackdewinter/pymarkdown/issues/468)
  - closing fence block allowed tabs after the fence characters
- [Issue 471](https://github.com/jackdewinter/pymarkdown/issues/471)
  - merging of end of line spaces not being handled properly
- [Issue 476](https://github.com/jackdewinter/pymarkdown/issues/476)
  - tabs within code spans were triggered stripping of whitespace
- [Issue 483](https://github.com/jackdewinter/pymarkdown/issues/483)
  - fixed RegEx within Md018 and Md021 to properly reflect spaces, not whitespaces
- [Issue 486](https://github.com/jackdewinter/pymarkdown/issues/486)
  - fixed problem with tabs causing weird parsing with a new block quote

## Version 0.9.7 - Date: 2022-07-04

### Added

- None

### Changed

- Bumping of versions of dependent packages
- [Changed - Issue 361](https://github.com/jackdewinter/pymarkdown/issues/361)
  - cleaning up badges to make them consistent
- [Changed - Issue 392](https://github.com/jackdewinter/pymarkdown/issues/392)
  - moved many of the "one-off" parameters out of arguments into a "grab-bag" with logging

### Fixed

- [Fixed - Issue 355](https://github.com/jackdewinter/pymarkdown/issues/355)
  - issues uncovered by bumping pylint version
- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/305)
  - issues with whitespace in certain situations being applied to both container and leaf tokens
- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/302)
  - issues with whitespace missing from certain scenarios
- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/253)
  - issues with lists and block quotes interacting badly, resulting in block quote being missed

## Version 0.9.6 - Date: 2022-04-02

### Added

- [Added - Issue 293](https://github.com/jackdewinter/pymarkdown/issues/293)
  - next round of nested level tests, with new list items
- [Added - Issue 319](https://github.com/jackdewinter/pymarkdown/issues/319)
  - added mypy typing to entire project and removed stubs for `application_properties`

### Changed

- [Changed - Issue 154](https://github.com/jackdewinter/pymarkdown/issues/154)
  - rule md003: added configuration `allow-setext-update`
- [Changed - Issue 283](https://github.com/jackdewinter/pymarkdown/issues/283)
  - general: moved more modules into specific directories

### Fixed

- [Fixed - Issue 95](https://github.com/jackdewinter/pymarkdown/issues/95)
  - parser: with certain cases involving a new list item, can start a container in the middle of line
- [Fixed - Issue 161](https://github.com/jackdewinter/pymarkdown/issues/161)
  - rule md005: was not returning proper values for actual and expected
- [Fixed - Issue 189](https://github.com/jackdewinter/pymarkdown/issues/189)
  - rule md027: addressed index out of bounds error keeping track of blank lines after a block quote was started in a previous section
- [Fixed - Issue 287](https://github.com/jackdewinter/pymarkdown/issues/287)
  - parser: code to handle indent was greedy with respect to HTML blocks and fenced code blocks
- [Fixed - Issue 294](https://github.com/jackdewinter/pymarkdown/issues/294)
  - markdown generator: needed to take list items into account
- [Fixed - Issue 295](https://github.com/jackdewinter/pymarkdown/issues/295)
  - markdown generator: fixed by work on 294
- [Fixed - Issue 296](https://github.com/jackdewinter/pymarkdown/issues/296)
  - parser: improper closing of previous block caused duplicate list items
- [Fixed - Issue 297](https://github.com/jackdewinter/pymarkdown/issues/297)
  - markdown generator: not indenting enough
- [Fixed - Issue 298](https://github.com/jackdewinter/pymarkdown/issues/298)
  - parser: list processing go confused between block quote and list
- [Fixed - Issue 299](https://github.com/jackdewinter/pymarkdown/issues/299)
  - parser: not recognizing inner list
- [Fixed - Issue 300](https://github.com/jackdewinter/pymarkdown/issues/300)
  - parser: various issues with lists not being properly handled in nested scenarios

## Version 0.9.5 - Date: 2022-02-07

This was a point release that highlighted improvements to the accuracy of reported tokens
in situations with nested containers.

PLEASE! If you encounter any issues with this product, please [file an issue report](https://github.com/jackdewinter/pymarkdown/issues) and tell us about it!
There are a lot of combinations of Markdown elements to cover, and we need your help to prioritize them all!

### Added

- [Added - Issue 227](https://github.com/jackdewinter/pymarkdown/issues/227)
  - scenario tests: adding 3-level nesting tests with max space, and max space plus one variations
- [Added - Issue 250](https://github.com/jackdewinter/pymarkdown/issues/250)
  - scenario tests: adding variations of removed block quotes on second line
- [Added - Issue 261](https://github.com/jackdewinter/pymarkdown/tree/issue-261)
  - scenario tests: variations of 3-level max space tests with no text after container starts on first line

### Changed

- [Changed - Issue 248](https://github.com/jackdewinter/pymarkdown/issues/248)
  - github actions: only run against `main` branch

### Fixed

- [Fixed - Issue 189](https://github.com/jackdewinter/pymarkdown/issues/189)
  - rule md027: weird case where total for series of block quotes that ended with a blank line was off by 1
- [Fixed - Issue 218](https://github.com/jackdewinter/pymarkdown/issues/218)
  - parser: lot of small things needed fixing to set the variables properly for this issue's resolution
  - parser: after that, was not properly handling shutting down a block quote that downgraded
- [Fixed - Issue 228](https://github.com/jackdewinter/pymarkdown/issues/228)
  - parser: previous adjustment no longer needed
- [Fixed - Issue 229](https://github.com/jackdewinter/pymarkdown/issues/229)
  - parser: generated HTML did not include indented code block
- [Fixed - Issue 230](https://github.com/jackdewinter/pymarkdown/issues/230)
  - parser: dropping leading `>`
- [Fixed - Issue 231](https://github.com/jackdewinter/pymarkdown/issues/231)
  - parser: fixed by issue-229
- [Fixed - Issue 232](https://github.com/jackdewinter/pymarkdown/issues/232)
  - parser: fixed by issue-233
  - parser: fixed by issue-228
- [Fixed - Issue 233](https://github.com/jackdewinter/pymarkdown/issues/233)
  - parser: limiting container checking to limited set, expanded
  - parser: extra indent was not accounted for in space calculations
  - parser: double block quotes not being handled properly
  - parser: indent being processed twice
- [Fixed - Issue 252](https://github.com/jackdewinter/pymarkdown/issues/252)
  - parser: in rare cases, was adding leading spaces to both list and paragraph within
- [Fixed - Issue 262](https://github.com/jackdewinter/pymarkdown/issues/262)
  - parser: when checking for block quote decrease, did not have empty scenarios checked for
- [Fixed - Issue 263](https://github.com/jackdewinter/pymarkdown/issues/263)
  - parser: with empty list items, was creating 2 blank line tokens, plus extra list indent
- [Fixed - Issue 264](https://github.com/jackdewinter/pymarkdown/issues/264)
  - parser: fixed issue with blending current text and original text to parse
  - parser: cleaned up remaining issues about closing off containers too early
- [Fixed - Issue 265](https://github.com/jackdewinter/pymarkdown/issues/265)
  - parser: fixed with work on [Issue 262](https://github.com/jackdewinter/pymarkdown/issues/262)
- [Fixed - Issue 268](https://github.com/jackdewinter/pymarkdown/issues/268)
  - parser: previous work took too many newlnes out, this put the right ones back in

## Version 0.9.4 - Date: 2022-01-04

This was a point release that highlighted improvements to the accuracy of reported tokens
in situations with nested containers.

- Removed "call home support" similar to VSCode and other products.
  - One of our contributors pointed out a number of falacies, and we agreed.
- Enhanced testing of the whitespace calculations recently completed.

### Changed

- [Changed - Issue 184](https://github.com/jackdewinter/pymarkdown/issues/184)
  - scenario tests: instead of mixup in different areas, added initial combinations to test in one place
- [Changed - Issue 207](https://github.com/jackdewinter/pymarkdown/issues/207)
  - adding more upfront analysis, upgrading Columnar to new version
- [Changed - Issue 214](https://github.com/jackdewinter/pymarkdown/issues/214)
  - removing call home support

### Fixed

- [Fixed - Issue 159](https://github.com/jackdewinter/pymarkdown/issues/159)
  - parser: was using wrong values to determine nesting level
- [Fixed - Issue 185](https://github.com/jackdewinter/pymarkdown/issues/185)
  - parser: nesting of block quote, list, block quote raised an assert
- [Fixed - Issue 186](https://github.com/jackdewinter/pymarkdown/issues/186)
  - parser: due to work on Issue 187, these now passed after assert examine and disabled
- [Fixed - Issue 187](https://github.com/jackdewinter/pymarkdown/issues/187)
  - parser: three separate adjustments needed to be made to ensure the whitespace is consistent
- [Fixed - Issue 188](https://github.com/jackdewinter/pymarkdown/issues/188)
  - parser: not dealing with a block occurring after 2 nested lists
- [Fixed - Issue 192](https://github.com/jackdewinter/pymarkdown/issues/192)
  - parser: needed to adjust `__calculate_current_indent_level` function to accomodate nesting
- [Fixed - Issue 196](https://github.com/jackdewinter/pymarkdown/issues/196)
  - markdown: transformer was not calculating indent properly
- [Fixed - Issue 197](https://github.com/jackdewinter/pymarkdown/issues/197)
  - parser: block quote processor was not closing blocks properly, resulting in bad HTML
- [Fixed - Issue 198](https://github.com/jackdewinter/pymarkdown/issues/198)
  - markdown: algorithm was not taking into effect newer change to calculate container indices later
- [Fixed - Issue 199](https://github.com/jackdewinter/pymarkdown/issues/199)
  - parser: fixed by work done on [Issue 202](https://github.com/jackdewinter/pymarkdown/issues/202)
- [Fixed - Issue 200](https://github.com/jackdewinter/pymarkdown/issues/200)
  - markdown: calculation for previous indent and whitespace to add after was off
- [Fixed - Issue 201](https://github.com/jackdewinter/pymarkdown/issues/201)
  - parser: fixed by work done on [Issue 202](https://github.com/jackdewinter/pymarkdown/issues/202)
- [Fixed - Issue 202](https://github.com/jackdewinter/pymarkdown/issues/202)
  - parser: block quote processor needed a lot of work to handle whitespace properly
  - parser: container block processor not handling 4 spaces at start of line properly
- [Fixed - Issue 203](https://github.com/jackdewinter/pymarkdown/issues/203)
  - markdown: adjustments to properly calculate indent
  - parser: list block processor not transferring extracted text to a nested block
  - various cleanup
- [Fixed - Issue 219](https://github.com/jackdewinter/pymarkdown/issues/219)
  - parser: indents of 4 within a single and double level list were not cleanly differentiating

## Version 0.9.3 - Date: 2021-12-14

This was a point release to allow fixed issues to be released.  While
the full descriptions are below, here are some highlights:

- Added "call home support" similar to VSCode and other products, to allow notification of new versions
  - This is currently experimental.  Feedback welcome.
- Lots of refactoring to reduce complexity and adhere to guidelines
- Rewrite of the whitespace calculations to drastically reduce their complexity

### Added

- [Added - Issue 104](https://github.com/jackdewinter/pymarkdown/issues/104)
  - core: added support for calling home every week to see if there is a new version at PyPi.org

### Changed

- [Changed - Issue 85](https://github.com/jackdewinter/pymarkdown/issues/85)
  - scenario tests: verified and documented inlines with newline tests
- [Changed - Issue 96](https://github.com/jackdewinter/pymarkdown/issues/96)
  - parser: was misunderstanding.  extra blank line was verified as per spec
- [Changed - Issue 103](https://github.com/jackdewinter/pymarkdown/issues/103)
  - refactoring: look for better way to use .items()
- [Changed - Issue 107](https://github.com/jackdewinter/pymarkdown/issues/107)
  - refactoring: identified and removed unused pylint suppressions
- [Changed - Issue 112](https://github.com/jackdewinter/pymarkdown/issues/112)
  - refactoring: finding and applying all Sourcery recommended issues
- Changed - Module Refactoring to reduce complexity
  - [plugin_manager.py](https://github.com/jackdewinter/pymarkdown/issues/115)
  - [list_block_processor.py](https://github.com/jackdewinter/pymarkdown/issues/117)
  - [coalesce_processor.py + emphasis_helper.py](https://github.com/jackdewinter/pymarkdown/issues/119)
  - [container_block_processor.py](https://github.com/jackdewinter/pymarkdown/issues/121)
  - [leaf_block_processor.py](https://github.com/jackdewinter/pymarkdown/issues/123)
  - [link_reference_definition_helper.py](https://github.com/jackdewinter/pymarkdown/issues/126)
  - [link_helper.py](https://github.com/jackdewinter/pymarkdown/issues/128)
  - [inline_processor.py](https://github.com/jackdewinter/pymarkdown/issues/130)
  - [block_quote_processor.py](https://github.com/jackdewinter/pymarkdown/issues/134)
  - [tokenized_markdown.py](https://github.com/jackdewinter/pymarkdown/issues/136)
  - [main.py + inline_helper.py + rule md027](https://github.com/jackdewinter/pymarkdown/issues/138)
  - [rest of main directory](https://github.com/jackdewinter/pymarkdown/issues/140)
  - [extensions and rules](https://github.com/jackdewinter/pymarkdown/issues/143)
- [Changed - Issue 145](https://github.com/jackdewinter/pymarkdown/issues/145)
  - refactoring: Either implemented todo or filed new issue to do it later
- [Changed - Issue 151](https://github.com/jackdewinter/pymarkdown/issues/151)
  - refactoring: tightening up code after refactoring
- [Changed - Issue 155](https://github.com/jackdewinter/pymarkdown/issues/155)
  - refactoring: moving this_bq_count and stack_bq_quote into new BlockQuoteData class
- [Changed - Issue 166](https://github.com/jackdewinter/pymarkdown/issues/166)
  - refactoring: large refactoring to standardize the whitespace in tokens

### Fixed

- [Fixed - Issue 87](https://github.com/jackdewinter/pymarkdown/issues/87)
  - scenario tests: removing `disable_consistency_checks` from tests and getting clean
    - parser: found and resolved two issues
    - consistency checks: found and resolved ~7 issues
  - general: pass through code to clean up string usage
  - consistency check: verified rehydrate usage through project
  - consistency check: tightening leading space index for block quotes
    - parser: found and resolved issue with extra newline added to leading spaces for block quote
- [Fixed - Issue 90](https://github.com/jackdewinter/pymarkdown/issues/90)
  - scenario tests: verified noted tests have been fixed
  - rule md027: rewrote bq index logic to work properly
- [Fixed(partial) - Issue 92](https://github.com/jackdewinter/pymarkdown/issues/92)
  - rule md027: nested containers were not thoroughly tested
  - parser: added new bugs linked to Issue 92 as part of discovery
- [Fixed - Issue 93](https://github.com/jackdewinter/pymarkdown/issues/93)
  - parser: was not handling extracted spaces properly, causing issues with calculating values for thematic breaks
  - parser: spent time rewriting whitespace calculation and storage to address the issue
- [Fixed - Issue 94](https://github.com/jackdewinter/pymarkdown/issues/94)
  - parser: after work on 153, this was resolved
- [Fixed - Issue 97](https://github.com/jackdewinter/pymarkdown/issues/97)
  - parser: after work on 153, this was resolved
- [Fixed - Issue 98](https://github.com/jackdewinter/pymarkdown/issues/98)
  - parser: after work on 153, this was resolved
- [Fixed - Issue 99](https://github.com/jackdewinter/pymarkdown/issues/99)
  - parser: after work on 153, this was resolved
- [Fixed - Issue 100](https://github.com/jackdewinter/pymarkdown/issues/100)
  - parser: after work on 153, this was resolved
- [Fixed - Issue 153](https://github.com/jackdewinter/pymarkdown/issues/153)
  - parser: hit missed scenario test with list indents

## Version 0.9.2 - Date: 2021-10-24

This was a point release to allow fixed issues to be released.  While
the full descriptions are below, here are some highlights:

- Fixed issue with PyMarkdown scripts not having correct permissions
- Added more scenario tests and verified that those worked
- Fixed small issues with parser and rules, mostly boundary cases

### Added

- None

### Changed

- [Changed - Issue 44](https://github.com/jackdewinter/pymarkdown/issues/44)
  - scenario tests: went through every scenario test and validated comment string
- [Changed - Issue 62](https://github.com/jackdewinter/pymarkdown/issues/62)
  - parser: not reproducible, but added extra scenario tests to make sure
- [Changed - Issue 64](https://github.com/jackdewinter/pymarkdown/issues/64)
  - rule md030: was not implemented according to specification for "double, changed to do so
- [Changed - Issue 66](https://github.com/jackdewinter/pymarkdown/issues/66)
  - rule md023: rule fine, scenario tests running with bad data
- [Changed - Issue 68](https://github.com/jackdewinter/pymarkdown/issues/68)
  - documentation: added more clear description of sibling
- [Changed - Issue 70](https://github.com/jackdewinter/pymarkdown/issues/70)
  - scenario tests: gave better names, added one for configuration

### Fixed

- [Fixed - Issue 43](https://github.com/jackdewinter/pymarkdown/issues/43)
  - parser: on start of nested list, was not allowing indent to be based on parent indent
- [Fixed - Issue 47](https://github.com/jackdewinter/pymarkdown/issues/47)
  - parser: wasn't treating "partial" LRDs as valid, rewinding past their start
- [Fixed - Issue 49](https://github.com/jackdewinter/pymarkdown/issues/49)
  - parser: aborting a LRD within a list was not generating correct reset state
  - scenario tests: addressed same issue in fenced code block and LRD tests
  - issue: added [Issue 50](https://github.com/jackdewinter/pymarkdown/issues/50) to test with extra levels
- [Fixed - Issue 51](https://github.com/jackdewinter/pymarkdown/issues/51)
  - parser: not handling list starts properly where the list indent was less than the line before it
- [Fixed - Issued 53](https://github.com/jackdewinter/pymarkdown/issues/53)
  - parser: when dealing with lines within a list item within a block quote, not removing leading spaces properly
- [Fixed - Issue 56](https://github.com/jackdewinter/pymarkdown/issues/56)
  - scenario tests: resolved outstanding rules tests that were skipped
  - parser: when parsing `- > `, did not properly retain new block quote level on return
- [Fixed - Issue 59](https://github.com/jackdewinter/pymarkdown/issues/59)
  - parser: on line after list item, if started with `===`, would think it was SetExt instead of continuation text.
- [Fixed - Issue 72](https://github.com/jackdewinter/pymarkdown/issues/72)
  - rule md006: was not properly handling block quotes and nested lists
- [Fixed - Issue 74](https://github.com/jackdewinter/pymarkdown/issues/74)
  - parser: not handling cases with list then block quote, with only block quote on next line
  - scenario tests: added extra tests to cover variations on more complex nesting cases
- [Fixed - Issue 76](https://github.com/jackdewinter/pymarkdown/issues/76)
  - scenario tests: added extra test to cover missing variations
  - parser: was not handle the unwinding of lists properly in one case due to off-by-one error
- [Fixed - Issue 77](https://github.com/jackdewinter/pymarkdown/issues/77)
  - command line: scripts not interfacing properly on linux systems
- [Fixed - Issue 79](https://github.com/jackdewinter/pymarkdown/issues/79)
  - scenario tests: added extra test to cover missing variations
  - rule Md005: rewritten to respond to ordered lists better

## Version 0.9.1 - Date: 2021-10-06

This was a point release to make several new features and fixed
issues to be released.  While the full descriptions are below,
here are some highlights:

- Added documentation on how to use Git Pre-Commit hooks with PyMarkdown
- Added support to allow PyMarkdown to be executed as a module with `-m`
- Various scenario test tasks including verifying disabled rules were required

### Added

- [Added](https://github.com/jackdewinter/pymarkdown/issues/28)
  - documentation: documentation on how to use pre-commit hooks
- [Added](https://github.com/jackdewinter/pymarkdown/issues/31)
  - core: support for executing pymarkdown as a module (`python -m pymarkdown`)
- [Added](https://github.com/jackdewinter/pymarkdown/issues/37)
  - rules test: verified existing case, added missing related case
- [Added](https://github.com/jackdewinter/pymarkdown/issues/38)
  - rules test: added new test case with provided data
  - documentation: addressed documentation issue with description for rule_md044.md
- [Added](https://github.com/jackdewinter/pymarkdown/issues/40)
  - rule md033: new configuration value `allow_first_image_element`
    - if True, allows ONLY `<h1><img></h1>` sequence (with any parameters needed) if is first token in document
- [Added](https://github.com/jackdewinter/pymarkdown/issues/41)
  - documentation: added description of how HTML comments are different
- [Added](https://github.com/jackdewinter/pymarkdown/issues/42)
  - core: added sorting of triggered rules before they are displayed

### Changed

- [Changed](https://github.com/jackdewinter/pymarkdown/issues/36)
  - rules tests:verified need for `--disable-rules` through tests, removing any that were not needed
  - documentation: addressed some documentation issues with docs/rules.md and doc/rules/rule_md032.md

### Fixed

- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/22)
  - rule Md033: no longer triggers on end tags, adjusted default allowed tags
- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/23)
  - rule Md023: whitespace at end of lines in SetExt Heading no longer being recognized as starting whitespace.
- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/27)
  - rule Md032: was not recognizing 2 end list tokens in a row
- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/32)
  - rule Md037: was not properly looking for spaces inside of possible emphasis characters
- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/33)
  - parser: found parsing error with lists in block quotes
  - rule md031,md032: fixed that and fixed issues in rules md031 and md032
- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/34)
  - parser: multiline inline elements with a Block Quote were not getting their starting positions calculated properly
    - any element directly after those elements were also likely to have a bad position
- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/39)
  - parser: fixed instance of multi-level list within block quotes not firing properly
  - issues: added item to issues list to do more looking on nested lists
  - rule md007: may show up here with nested lists

## Version 0.9.0 - Date: 2021-09-21

The main focus of this release was to fill out the features that the
project supports to the beta release level.  Big ticket items addressed
were:

- Better support from the command line for extensions and plugins
- Implementing all the rules for launch

### Added

- [Added](https://github.com/jackdewinter/pymarkdown/issues/8) - ability to have configuration values for adding pluings and enabling stack trace.
- [Added](https://github.com/jackdewinter/pymarkdown/issues/9) - better access for plugin information from the command line.
- [Added](https://github.com/jackdewinter/pymarkdown/issues/12) - extension manager to start to bring extensions up to the same level as plugins.
- [Added](https://github.com/jackdewinter/pymarkdown/issues/14) - support for missing rules in the initial set of rules.

### Changed

- [Changed](https://github.com/jackdewinter/pymarkdown/issues/7) - to move the code for `application_properties` class from this project into a new Python package, and to make this project dependant on that package.
- [Changed](https://github.com/jackdewinter/pymarkdown/issues/10) - `markdown_token.py` to included better high level `is_*_token` functions
- [Updated](https://github.com/jackdewinter/pymarkdown/issues/11) - documentation on front-matter and pragma extensions.

### Fixed

- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/13) - issues with nested Block Quotes and Lists not interacting properly with each other

## Version 0.8.0 - Date: 2021-05-31

### Added

- added `-r` flag to control whether the scan is recursive
- added support for linting and testing through GitHub Actions

### Changed

- None

### Fixed

- improved documentation
- cleaned up error handling
- issues with tests not running properly on [Linux](https://github.com/jackdewinter/pymarkdown/issues/4) and [MacOs](https://github.com/jackdewinter/pymarkdown/issues/5)

## Version 0.5.0 - Date: 2021-05-16

### Added

- Initial release

### Changed

- None

### Fixed

- None
