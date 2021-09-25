# Change Log

## Unversion - In Main, Not Released

### Added

- None

### Changed

- None

### Fixed

- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/22) - no longer triggers on end tags, adjusted default allowed tags
- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/23) - whitespace at end of lines in SetExt Heading no longer being recognized as starting whitespace.
- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/27) - was not recognizing 2 end list tokens in a row

## Version 0.9.0 - Date: 2021-09-21

The main focus of this release was to fill out the features that the
project supports to the beta release level.  Big ticket items addressed
were:

- Better support from the command line for extensions and plugins
- Implementing all the rules for launch

### Added

- [Added](https://github.com/jackdewinter/pymarkdown/issues/8) ability to have configuration values for adding pluings and enabling stack trace.
- [Added](https://github.com/jackdewinter/pymarkdown/issues/9) better access for plugin information from the command line.
- [Added](https://github.com/jackdewinter/pymarkdown/issues/12) extension manager to start to bring extensions up to the same level as plugins.
- [Added](https://github.com/jackdewinter/pymarkdown/issues/14) support for missing rules in the initial set of rules.

### Changed

- [Changed](https://github.com/jackdewinter/pymarkdown/issues/7) to move the code for `application_properties` class from this project into a new Python package, and to make this project dependant on that package.
- [Changed](https://github.com/jackdewinter/pymarkdown/issues/10) `markdown_token.py` to included better high level `is_*_token` functions
- [Updated](https://github.com/jackdewinter/pymarkdown/issues/11) documentation on front-matter and pragma extensions.

### Fixed

- [Fixed](https://github.com/jackdewinter/pymarkdown/issues/13) issues with nested Block Quotes and Lists not interacting properly with each other

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
