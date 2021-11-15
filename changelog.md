# Change Log

## Unversioned - In Main, Not Released

### Added

- [Added - Issue 104](https://github.com/jackdewinter/pymarkdown/issues/104)
  - core: added support for calling home every week to see if there is a new version at PyPi.org

### Changed

- [Changed - Issue 85](https://github.com/jackdewinter/pymarkdown/issues/85)
  - scenario tests: verified and documented inlines with newline tests
- [Changed - Issue 103](https://github.com/jackdewinter/pymarkdown/issues/103)
  - refactoring: look for better way to use .items()
- [Changed - Issue 107](https://github.com/jackdewinter/pymarkdown/issues/107)
  - refactoring: identified and removed unused pylint suppressions
- [Changed - Issue 112](https://github.com/jackdewinter/pymarkdown/issues/112)
  - refactoring: finding and applying all Sourcery recommended issues
- Module Refactoring:
  - [plugin_manager.py](https://github.com/jackdewinter/pymarkdown/issues/115)
  - [list_block_processor.py](https://github.com/jackdewinter/pymarkdown/issues/117)
  - [coalesce_processor.py + emphasis_helper.py](https://github.com/jackdewinter/pymarkdown/issues/119)
  - [container_block_processor.py](https://github.com/jackdewinter/pymarkdown/issues/121)
  - [leaf_block_processor.py](https://github.com/jackdewinter/pymarkdown/issues/123)

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
