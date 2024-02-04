---
title: The PyMarkdown Linter
summary: Base information about the PyMarkdown Linter
authors:
  - Jack De Winter
---

## Note To Any Readers

As part of our effort to clean up the project in preparation for a version 1.0.0
release, we are moving our documentation from plain Markdown files hosted on
[GitHub](https://github.com/jackdewinter/pymarkdown) to this new format. Please
bear with us during this transitional period.

## And On with The Show...

PyMarkdown is primarily a Markdown Linter. To ensure that the Markdown
[linting](https://en.wikipedia.org/wiki/Lint_%28software%29) is conducted
successfully, the rules engine that powers the linter uses a Markdown parser
that is both [GitHub Flavored Markdown](https://github.github.com/gfm/)
compliant and [CommonMark](https://spec.commonmark.org/) compliant. While there
are other parsers in use today, we estimate that over 90% of the existing
parsers are either partially or fully compliant to one of these two
specifications. By adhering to these specifications for our parser, we can
therefore align with the behavior of those Markdown parsers with little effort.

The PyMarkdown project has the following advantages:

- Consistency
    - This project's interface can examine multiple files and directories with a
      single invocation, ensuring that all targeted Markdown files adhere to the
      provided set of guidelines.
- Portable
    - This project runs on any system with Python 3.8 or later, with no
      modifications. Each merge of new code to the `main` branch executes every
      scenario test against the project. These tests are repeated for Linux,
      Windows, and MacOS machines to ensure any portability issues are detected
      and fixed early.
- Standardized
    - The parser powering this project's linter is mostly
      [GitHub Flavored Markdown](https://github.github.com/gfm/) or GFM
      compliant. Due to that foundation, the parser does not guess how parsers
      may manage a given situation, it follows the same set of clearly defined
      rules that other GFM utilities use.
- Accurate
    - The project's parser passes most GFM conformance tests and CommonMark
      conformance tests without modification. For any test scenarios that were
      not present in either set of conformance tests, the CommonMark 0.29.2
      release was used to decide the correct parsing for that Markdown sequence.
- Flexible
    - Each Markdown document is parsed into PyMarkdown's own internal token
      format. Each rule can choose to take advantage of that token format or use
      simple line-by-line algorithms, whichever is clearer and most efficient.
- Thoroughly tested
    - The project currently has over 6504 scenario tests and a coverage percentage
      of 100 percent.
- Extensible
    - The core parts of the parser can be enhanced using
      [extensions](https://github.com/jackdewinter/pymarkdown/blob/main/docs/extensions.md)
      that provide other needed features. Each of the
      [rules](https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules.md)
      that the parser leverages are implemented as a plugin, with simple
      mechanisms for enabling, disabling, and adding new plugins.
- Versatile
    - The PyMarkdown linter can be executed from a script on the command line,
      from within another Python program, using our simple API, or using the
      popular Git Pre-Commit hooks.
