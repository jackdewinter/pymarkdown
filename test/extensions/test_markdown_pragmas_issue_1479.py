"""
Tests for the optional pragma processing related to issue #1479.

Note that these tests are not present to test the validity of any scenario against a
    specific rule.  They are present to ensure that when a rule reports an error for
    a given token, it is being reported with the correct line number.  Given that,
    the `disable-next-line` pragma can be used on the line before or two lines before
    with a blank line between (due to some formatters) to suppress the triggering
    of the rule.
"""

from test.markdown_scanner import MarkdownScanner
from test.utils import create_temporary_configuration_file

import pytest

# Rule Md001 -- Token - Atx, SetExt                             - Covered & Verified
# Rule Md002 -- Token - Atx, SetExt                             - Covered & Verified
# Rule Md003 -- Token - Atx, SetExt                             - Covered & Verified
# Rule Md004 -- Token - Ul                                      - Covered & Verified
# Rule Md005 -- Token - Ul, Ol, Li                              - Covered & Verified
# Rule Md006 -- Token - Ul, Li                                  - Covered & Verified
# Rule Md007 -- Token - Ul, Li                                  - Covered & Verified
# Rule Md009 -- Line                                            - Covered & Verified
# Rule Md010 -- Line                                            - Covered & Verified
# Rule Md011 -- Line                                            - Covered & Verified
# Rule Md012 -- Token - Bl                                      - Covered & Verified
# Rule Md013 -- Line                                            - Covered & Verified
# Rule Md014 -- Token - Fcb                                     - Covered & Verified
# Rule Md018 -- Token - Atx                                     - Covered & Verified
# Rule Md019 -- Token - Atx                                     - Covered & Verified
# Rule Md020 -- Token - Atx                                     - Covered & Verified
# Rule Md021 -- Token - Atx                                     - Covered & Verified
# Rule Md022 -- Token - Atx, SetExt                             - Covered & Verified
# Rule Md023 -- Token - Atx, SetExt                             - Covered & Verified
# Rule Md024 -- Token - Atx, SetExt                             - Covered & Verified
# Rule Md025 -- Token - Atx, SetExt                             - Covered & Verified
# Rule Md026 -- Token - Atx, SetExt                             - Covered & Verified
# Rule Md027 -- Token - All Container and Leaf                  - Covered
# Rule Md028 -- Token - Bl                                      - Covered & Verified
# Rule Md029 -- Token - Ol                                      - Covered & Verified
# Rule Md030 -- Token - Ul, Ol, Li                              - Covered & Verified
# Rule Md031 -- Token - All Container and Leaf                  - Covered & Verified
# Rule Md032 -- Token - Ul, Ol, Li                              - Covered & Verified
# Rule Md033 -- Token - Html, Inline-Html                       - Covered & Verified
# Rule Md034 -- Token - Para/Text                               - Covered & Verified
# Rule Md035 -- Token - Tb                                      - Covered & Verified
# Rule Md036 -- Token - Para/text                               - Covered & Verified
# Rule Md037 -- Token - Para/Text                               - Covered & Verified
# Rule Md038 -- Token - Codespan                                - Covered & Verified
# Rule Md039 -- Token - Link                                    - Covered & Verified
# Rule Md040 -- Token - Fcb                                     - Covered & Verified
# Rule Md041 -- Token - Atx, SetExt, Html, Fcb (not previous)   - Covered & Verified
# Rule Md042 -- Token - Link                                    - Covered & Verified
# Rule Md043 -- Token - Atx, SetExt                             - Covered & Verified
# Rule Md044 -- Token - Text, link, image, lrd, codespan        - Covered               - (rewind logic with pragma)
# Rule Md045 -- Token - Link                                    - Covered & Verified
# Rule Md046 -- Token - Fcb, Icb                                - Covered & Verified
# Rule Md047 -- Line                                            - Covered & Verified
# Rule Md048 -- Token - Fcb                                     - Covered & Verified
# Rule Pml100 -- Token - Html, Inline-Html                      - Covered & Verified
# Rule Pml101 -- Token - Ul, Ol, Li                             - Covered & Verified


@pytest.mark.gfm
def test_pragmas_issue_1479_xx_0() -> None:
    """
    Test the case where we have a single blank line between the pragma and a rule that triggers
    on an inline element.  Because of the tokenization of links, the first instance of the
    word "paragraph" occurs within a text element within the link, which is handled by
    the normal processing of the add_triggered_rule function in the PluginScanContext instance.
    The second one occurs on the link element itself, and makes sure that the algorithm
    can handle an inline element that occurs with no text element between it and the
    paragraph that holds it.

    Modified from: test_md044_scan[bad_inline_link]
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->

[a paragraph inspired link](/paragraph "paragraph")
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_xx_1() -> None:
    """
    Test the case where we have a single blank line between the pragma and a rule that triggers
    on an inline element.  This should trigger the first two sections of the add_triggered_rule function
    in the PluginScanContext instance, for inline elements and text blocks.

    Copy of: test_pragmas_issue_1479_Md039_pragma_with_space_then_text_with_link_first_line
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-space-in-links -->

this is not [ a proper ](https://www.example.com) link
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_xx_2() -> None:
    """
    Test the case where we have a single blank line between the pragma and a rule that triggers
    on a list start element.  This should trigger the last section of the add_triggered_rule function
    in the PluginScanContext instance, checking for list ends before a list start.

    Copy of: test_pragmas_issue_1479_Pml101_pragma_with_space_then_ol_li
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line list-anchored-indent -->

 1. this is level 1
<!-- pyml disable-next-line list-anchored-indent -->

 1. this is also level 1
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml101",
            "--disable-rules",
            "Md007",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_xx3() -> None:
    """
    Test the case where we have a single blank line between the pragma and a rule that triggers
    on a list start element that follows another list start element.  This should trigger the
    last section of the add_triggered_rule function in the PluginScanContext instance, checking
    for list ends before a list start and after another list.

    Copy of: test_pragmas_issue_1479_Md004_pragma_with_space_then_ul_ul_ul
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """* first
<!-- pyml disable-next-line ul-style -->

+ second
<!-- pyml disable-next-line ul-style -->

- third
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md026_no_pragma_then_atx() -> None:
    """
    Test the case where we have a Md026 violation and no pragma, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Hi there! :wave:
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:16: MD026: Trailing punctuation present in heading text. (no-trailing-punctuation)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md026_pragma_without_space_then_atx() -> None:
    """
    Test the case where we have a Md026 violation and a disable-next-line pragma on the line before it,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-trailing-punctuation -->
# Hi there! :wave:
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md026_pragma_with_space_then_atx() -> None:
    """
    Test the case where we have a Md026 violation and a disable-next-line pragma two lines before it with a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-trailing-punctuation -->

# Hi there! :wave:
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md026_no_pragma_then_setext() -> None:
    """
    Test the case where we have a Md026 violation and a disable-next-line pragma on the line before it,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Hi there! :wave:
----------------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"{markdown_file_path}:1:16: MD026: Trailing punctuation present in heading text. (no-trailing-punctuation)"
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md026_pragma_without_space_then_setext() -> None:
    """
    Test the case where we have a Md026 violation and a disable-next-line pragma on the line before it,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-trailing-punctuation -->
Hi there! :wave:
----------------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md026_pragma_with_space_then_setext() -> None:
    """
    Test the case where we have a Md026 violation and a disable-next-line pragma on the line before it,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-trailing-punctuation -->

Hi there! :wave:
----------------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md001_no_pragma_then_atx() -> None:
    """
    Test the case where we have a Md001 violation and no pragma, and we expect the rule to fire.

    Note,
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Heading 1

### Heading 3

We skipped out a 2nd level heading in this document
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD001: Heading levels should only increment by one level at a time. [Expected: h2; Actual: h3] (heading-increment,header-increment)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md001_pragma_without_space_then_atx() -> None:
    """
    Test the case where we have a Md001 violation and a disable-next-line pragma on the line before it,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Heading 1

<!-- pyml disable-next-line heading-increment -->
### Heading 3

We skipped out a 2nd level heading in this document
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md001_pragma_with_space_then_atx() -> None:
    """
    Test the case where we have a Md001 violation and a disable-next-line pragma two lines before it with a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Heading 1

<!-- pyml disable-next-line heading-increment -->

### Heading 3

We skipped out a 2nd level heading in this document
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md001_no_pragma_then_setext_1_and_setext_2() -> None:
    """
    Test the case where we have a Md001 violation and no pragma, and we expect the rule to fire.

    Because setext headings are limited to level 1 and level 2 headings, this is the only
    of the combinations (1/1, 2/2, 2/1, 1/2) where there is an increment between the two
    headings.  Even if we replace the first heading with an Atx Heading, it would still
    be a level 1 heading (this test), a level 2 heading (equal, so no increment), or
    a heading decrement.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Foo *bar*
=========

Foo
---------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md002_no_pragma_then_atx() -> None:
    """
    Test the case where we have a Md002 violation and no pragma, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """## This isn't an H1 heading

### Another heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-e",
            "md002",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD002: First heading of the document should be a top level heading. [Expected: h1; Actual: h2] (first-heading-h1,first-header-h1)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md002_pragma_without_space_then_atx() -> None:
    """
    Test the case where we have a Md002 violation and a disable-next-line pragma on the line before it,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line first-heading-h1 -->
## This isn't an H1 heading

### Another heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-e",
            "md002",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md002_pragma_with_space_then_atx() -> None:
    """
    Test the case where we have a Md001 violation and a disable-next-line pragma two lines before it with a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line first-heading-h1 -->

## This isn't an H1 heading

### Another heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-e",
            "md002",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md002_no_pragma_then_setext() -> None:
    """
    Test the case where we have a Md002 violation and no pragma, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This isn't an H1 heading
------------------------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-e",
            "md002",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD002: First heading of the document should be a top level heading. [Expected: h1; Actual: h2] (first-heading-h1,first-header-h1)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md002_pragma_without_space_then_setext() -> None:
    """
    Test the case where we have a Md002 violation and a disable-next-line pragma on the line before it,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line first-heading-h1 -->
This isn't an H1 heading
------------------------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-e",
            "md002",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md002_pragma_with_space_then_setext() -> None:
    """
    Test the case where we have a Md001 violation and a disable-next-line pragma two lines before it with a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line first-heading-h1 -->

This isn't an H1 heading
------------------------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-e",
            "md002",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md003_no_pragma_then_setext_setext_atx() -> None:
    """
    Test the case where we have a Md003 violation and no pragma, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Heading 1
=========

Heading 2
---------

### Heading 3
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:7:1: MD003: Heading style should be consistent throughout the document. [Expected: setext; Actual: atx] (heading-style,header-style)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md003_pragma_without_space_then_setext_setext_atx() -> None:
    """
    Test the case where we have a Md003 violation and a disable-next-line pragma on the line before it,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Heading 1
=========

Heading 2
---------

<!-- pyml disable-next-line heading-style -->
### Heading 3
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md003_pragma_with_space_then_setext_setext_atx() -> None:
    """
    Test the case where we have a Md003 violation and a disable-next-line pragma two lines before it with a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Heading 1

<!-- pyml disable-next-line heading-increment -->

### Heading 3

We skipped out a 2nd level heading in this document
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md003_no_pragma_then_atx_setext() -> None:
    """
    Test the case where we have a Md003 violation and no pragma, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Heading 1

Heading 2
---------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD003: Heading style should be consistent throughout the document. [Expected: atx; Actual: setext] (heading-style,header-style)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md003_pragma_without_space_then_atx_setext() -> None:
    """
    Test the case where we have a Md003 violation and a disable-next-line pragma on the line before it,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Heading 1

<!-- pyml disable-next-line heading-style -->
Heading 2
---------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md003_pragma_with_space_then_atx_setext() -> None:
    """
    Test the case where we have a Md003 violation and a disable-next-line pragma two lines before it with a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Heading 1

<!-- pyml disable-next-line heading-style -->

Heading 2
---------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md004_no_pragma_then_ul_ul_ul() -> None:
    """
    Test the case where we have Md004 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """* first
+ second
- third
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md032,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: plus] (ul-style)
{markdown_file_path}:3:1: MD004: Inconsistent Unordered List Start style [Expected: asterisk; Actual: dash] (ul-style)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md004_pragma_without_space_then_ul_ul_ul() -> None:
    """
    Test the case where we have Md004 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """* first
<!-- pyml disable-next-line ul-style -->
+ second
<!-- pyml disable-next-line ul-style -->
- third
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md032,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md004_pragma_with_space_then_ul_ul_ul() -> None:
    """
    Test the case where we have Md004 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """* first
<!-- pyml disable-next-line ul-style -->

+ second
<!-- pyml disable-next-line ul-style -->

- third
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md005_no_pragma_then_ol_li() -> None:
    """
    Test the case where we have Md005 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. Item 1
 1. Item 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md032,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:2: MD005: Inconsistent indentation for list items at the same level [Expected: 0; Actual: 1] (list-indent)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md005_pragma_without_space_then_ol_li() -> None:
    """
    Test the case where we have Md005 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. Item 1
<!-- pyml disable-next-line list-indent -->
 1. Item 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md032,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md005_pragma_with_space_then_ol_li() -> None:
    """
    Test the case where we have Md005 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. Item 1
<!-- pyml disable-next-line list-indent -->

 1. Item 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md032,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md005_no_pragma_then_ul_li() -> None:
    """
    Test the case where we have Md005 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """+ Item 1
 + Item 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md007,Md032,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:2: MD005: Inconsistent indentation for list items at the same level [Expected: 0; Actual: 1] (list-indent)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md005_pragma_without_space_then_ul_li() -> None:
    """
    Test the case where we have Md005 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """+ Item 1
<!-- pyml disable-next-line list-indent -->
 + Item 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md007,Md032,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md005_pragma_with_space_then_ul_li() -> None:
    """
    Test the case where we have Md005 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """+ Item 1
<!-- pyml disable-next-line list-indent -->

 + Item 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md007,Md032,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md006_no_pragma_then_ol() -> None:
    """
    Test the case where we have Md006 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """ * First Item
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-e",
            "Md006",
            "-d",
            "Md007,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:2: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md006_pragma_without_space_then_ol() -> None:
    """
    Test the case where we have Md006 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line ul-start-left -->
 * First Item
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-e",
            "Md006",
            "-d",
            "Md007,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md006_pragma_with_space_then_ol() -> None:
    """
    Test the case where we have Md006 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line ul-start-left -->

 * First Item
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-e",
            "Md006",
            "-d",
            "Md007,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md006_no_pragma_then_ol_li() -> None:
    """
    Test the case where we have Md006 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """* First Item
 * Second Item
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-e",
            "Md006",
            "-d",
            "Md005,Md007,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:2: MD006: Consider starting bulleted lists at the beginning of the line (ul-start-left)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md006_pragma_without_space_then_ol_li() -> None:
    """
    Test the case where we have Md006 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """* First Item
<!-- pyml disable-next-line ul-start-left -->
 * Second Item
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-e",
            "Md006",
            "-d",
            "Md005,Md007,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md006_pragma_with_space_then_ol_li() -> None:
    """
    Test the case where we have Md006 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line ul-start-left -->

 * First Item
"""
    source_markdown = """* First Item
<!-- pyml disable-next-line ul-start-left -->

 * Second Item
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-e",
            "Md006",
            "-d",
            "Md005,Md007,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md007_no_pragma_then_ul() -> None:
    """
    Test the case where we have Md007 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """ * this is level 1
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md007_pragma_without_space_then_ul() -> None:
    """
    Test the case where we have Md007 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line ul-indent -->
 * this is level 1
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md007_pragma_with_space_then_ul_ul() -> None:
    """
    Test the case where we have Md007 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line ul-indent -->

 * this is level 1
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md007_no_pragma_then_ul_li() -> None:
    """
    Test the case where we have Md007 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """ * this is level 1
 * this is level 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)
{markdown_file_path}:2:2: MD007: Unordered list indentation [Expected: 0, Actual=1] (ul-indent)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md007_pragma_without_space_then_ul_li() -> None:
    """
    Test the case where we have Md007 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line ul-indent -->
 * this is level 1
<!-- pyml disable-next-line ul-indent -->
 * this is level 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md007_pragma_with_space_then_ul_li() -> None:
    """
    Test the case where we have Md007 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line ul-indent -->

 * this is level 1
<!-- pyml disable-next-line ul-indent -->

 * this is level 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md009_no_pragma_then_para_with_trailing() -> None:
    """
    Test the case where we have Md007 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is some text\a
each line has extra spaces\a\a
but not all are invalid\a\a\a
""".replace(
        "\a", " "
    )
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:18: MD009: Trailing spaces [Expected: 0 or 2; Actual: 1] (no-trailing-spaces)
{markdown_file_path}:3:24: MD009: Trailing spaces [Expected: 0 or 2; Actual: 3] (no-trailing-spaces)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md009_pragma_without_space_then_para_with_trailing() -> (
    None
):
    """
    Test the case where we have Md009 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-trailing-spaces -->
this is some text\a
each line has extra spaces\a\a
<!-- pyml disable-next-line no-trailing-spaces -->
but not all are invalid\a\a\a
""".replace(
        "\a", " "
    )
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md009_pragma_with_space_then_para_with_trailing() -> None:
    """
    Test the case where we have Md009 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-trailing-spaces -->

this is some text\a
each line has extra spaces\a\a
<!-- pyml disable-next-line no-trailing-spaces -->

but not all are invalid\a\a\a
""".replace(
        "\a", " "
    )
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md010_no_pragma_then_para_with_tab() -> None:
    """
    Test the case where we have Md010 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """before-tab\tafter-tab\tafter-tab
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:11: MD010: Hard tabs [Column: 11] (no-hard-tabs)
{markdown_file_path}:1:22: MD010: Hard tabs [Column: 22] (no-hard-tabs)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md010_pragma_without_space_then_para_with_tab() -> None:
    """
    Test the case where we have Md010 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-hard-tabs -->
before-tab\tafter-tab\tafter-tab
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md010_pragma_with_space_then_para_with_tab() -> None:
    """
    Test the case where we have Md010 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-hard-tabs -->

before-tab\tafter-tab\tafter-tab
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md011_no_pragma_then_para_including_found() -> None:
    """
    Test the case where we have Md011 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is a normal paragraph
with a (reversed)[link] syntax
found within it.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:8: MD011: Reversed link syntax [(reversed)[link]] (no-reversed-links)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md011_pragma_without_space_then_para_including_found() -> (
    None
):
    """
    Test the case where we have Md011 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is a normal paragraph
<!-- pyml disable-next-line no-reversed-links -->
with a (reversed)[link] syntax
found within it.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md011_pragma_with_space_then_para_including_found() -> None:
    """
    Test the case where we have Md011 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is a normal paragraph
<!-- pyml disable-next-line no-reversed-links -->

with a (reversed)[link] syntax
found within it.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md012_no_pragma_then_para_blank_lines_para() -> None:
    """
    Test the case where we have Md012 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is one line


this is another line
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD012: Multiple consecutive blank lines [Expected: 1, Actual: 2] (no-multiple-blanks)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md012_pragma_without_space_then_para_blank_lines_para() -> (
    None
):
    """
    Test the case where we have Md012 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.

    Note: This rule does not fire because this rule has special rules for deal with pragmas
        that preserve the blank lines.  In this case, the pragma visually breaks the document
        up with only one blank line between the first paragraph and itself, and then again
        with itsel and the second paragraph. While the `line-length` rule is disabled, it
        could be any pragma line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is one line

<!-- pyml disable-next-line line-length -->

this is another line
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md012_pragma_with_space_then_para_blank_lines_para() -> (
    None
):
    """
    Test the case where we have Md012 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: See test test_pragmas_issue_1479_Md012_pragma_without_space_then_para_blank_lines_para for
      more description.  However, this scenario includes 2 blank lines between the pragma and the
      second paragraph.  Therefore the pragma here is dealing with the trigger on line 5.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is one line

<!-- pyml disable-next-line no-multiple-blanks -->


this is another line
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md013_no_pragma_then_para_with_long_atx() -> None:
    """
    Test the case where we have Md013 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# This is a heading that is way way way way way way way way way way way way way too long
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD013: Line length [Expected: 80, Actual: 88] (line-length)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md013_pragma_without_space_then_long_atx() -> None:
    """
    Test the case where we have Md013 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line line-length -->
# This is a heading that is way way way way way way way way way way way way way too long
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md013_pragma_with_space_then_long_atx() -> None:
    """
    Test the case where we have Md013 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line line-length -->

# This is a heading that is way way way way way way way way way way way way way too long
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md014_no_pragma_then_para_with_shell_fcb() -> None:
    """
    Test the case where we have Md014 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```shell
$ ls /my/dir
$ cat /my/dir/file
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD014: Dollar signs used before commands without showing output (commands-show-output)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md014_pragma_without_space_then_shell_fcb() -> None:
    """
    Test the case where we have Md014 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```shell
<!-- pyml disable-next-line commands-show-output -->
$ ls /my/dir
$ cat /my/dir/file
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md014_pragma_with_space_then_shell_fcb() -> None:
    """
    Test the case where we have Md014 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: This rule is triggered if all lines in the fenced code block begin with a $ character.
       This is typically used to show linux commands.  However, the presence of ANY line that does
       not start with a `$` character, including the one after any pragma, is enough to not trigger
       this rule.  Hence, this variation on the rule is tested using `line-length` for the pragma
       to show that it does not fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```shell
<!-- pyml disable-next-line line-length -->

$ ls /my/dir
$ cat /my/dir/file
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md018_no_pragma_then_para_with_possible_atx_in_para() -> (
    None
):
    """
    Test the case where we have Md018 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """#Heading 1
more text here
##Heading 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{markdown_file_path}:3:1: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md018_pragma_without_space_then_possible_atx_in_para() -> (
    None
):
    """
    Test the case where we have Md018 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-missing-space-atx -->
#Heading 1
more text here
<!-- pyml disable-next-line no-missing-space-atx -->
##Heading 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md018_pragma_with_space_then_possible_atx_in_para() -> None:
    """
    Test the case where we have Md018 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-missing-space-atx -->

#Heading 1
more text here
<!-- pyml disable-next-line no-missing-space-atx -->

##Heading 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md018_no_pragma_then_para_with_possible_atx_in_list_in_para() -> (
    None
):
    """
    Test the case where we have Md018 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. #Heading 1
   more text here
   ##Heading 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)
{markdown_file_path}:3:4: MD018: No space present after the hash character on a possible Atx Heading. (no-missing-space-atx)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md018_pragma_without_space_then_possible_atx_in_list_in_para() -> (
    None
):
    """
    Test the case where we have Md018 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-missing-space-atx -->
1. #Heading 1
   more text here
<!-- pyml disable-next-line no-missing-space-atx -->
   ##Heading 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md018_pragma_with_space_then_possible_atx_in_list_in_para() -> (
    None
):
    """
    Test the case where we have Md018 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-missing-space-atx -->

1. #Heading 1
   more text here
<!-- pyml disable-next-line no-missing-space-atx -->

   ##Heading 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md019_no_pragma_then_atx_with_extra_spaces() -> None:
    """
    Test the case where we have Md019 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """#  Heading 1

##  Heading 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{markdown_file_path}:3:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md019_pragma_without_space_then_atx_with_extra_spaces() -> (
    None
):
    """
    Test the case where we have Md019 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-multiple-space-atx -->
#  Heading 1

<!-- pyml disable-next-line no-multiple-space-atx -->
##  Heading 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md019_pragma_with_space_then_atx_with_extra_spaces() -> (
    None
):
    """
    Test the case where we have Md019 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-multiple-space-atx -->

#  Heading 1

<!-- pyml disable-next-line no-multiple-space-atx -->

##  Heading 2
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md020_no_pragma_then_para_with_possible_atx_closed_in_para() -> (
    None
):
    """
    Test the case where we have Md020 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. #Heading 1#
   more text here
   ##Heading 2##
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:4: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)
{markdown_file_path}:3:4: MD020: No space present inside of the hashes on a possible Atx Closed Heading. (no-missing-space-closed-atx)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md020_pragma_without_space_then_para_with_possible_atx_closed_in_para() -> (
    None
):
    """
    Test the case where we have Md020 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-missing-space-closed-atx -->
1. #Heading 1#
   more text here
<!-- pyml disable-next-line no-missing-space-closed-atx -->
   ##Heading 2##
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md020_pragma_with_space_then_para_with_possible_atx_closed_in_para() -> (
    None
):
    """
    Test the case where we have Md020 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-missing-space-closed-atx -->

1. #Heading 1#
   more text here
<!-- pyml disable-next-line no-missing-space-closed-atx -->

   ##Heading 2##
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md021_no_pragma_then_atx_closed_with_extra_spaces() -> None:
    """
    Test the case where we have Md021 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Heading 1  #

## Heading 2  ##
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)
{markdown_file_path}:3:1: MD021: Multiple spaces are present inside hash characters on Atx Closed Heading. (no-multiple-space-closed-atx)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md021_pragma_without_space_then_atx_closed_with_extra_spaces() -> (
    None
):
    """
    Test the case where we have Md021 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-multiple-space-closed-atx -->
# Heading 1  #

<!-- pyml disable-next-line no-multiple-space-closed-atx -->
## Heading 2  ##
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md021_pragma_with_space_then_atx_closed_with_extra_spaces() -> (
    None
):
    """
    Test the case where we have Md021 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-multiple-space-closed-atx -->

# Heading 1  #

<!-- pyml disable-next-line no-multiple-space-closed-atx -->

##  Heading 2  ##
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md022_no_pragma_then_atx_with_no_space_around() -> None:
    """
    Test the case where we have Md022 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is a paragraph
# Heading 1
Some text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
{markdown_file_path}:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md022_pragma_without_space_then_atx_with_no_space_around() -> (
    None
):
    """
    Test the case where we have Md022 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is a paragraph
<!-- pyml disable-next-line blanks-around-headings -->
# Heading 1
Some text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md022_pragma_with_space_then_atx_with_no_space_around() -> (
    None
):
    """
    Test the case where we have Md022 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: As this is the "pragma with space" scenario, it only tests the below case as, by default,
        the above must have a single blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is a paragraph
<!-- pyml disable-next-line blanks-around-headings -->

# Heading 1
Some text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md022_no_pragma_then_setext_with_no_space_around() -> None:
    """
    Test the case where we have Md022 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """--------
SetExt
------
Some text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)
{markdown_file_path}:2:1: MD022: Headings should be surrounded by blank lines. [Expected: 1; Actual: 0; Below] (blanks-around-headings,blanks-around-headers)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md022_pragma_without_space_then_setext_with_no_space_around() -> (
    None
):
    """
    Test the case where we have Md022 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """--------
<!-- pyml disable-next-line blanks-around-headings -->
SetExt
------
Some text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md022_pragma_with_space_then_setext_with_no_space_around() -> (
    None
):
    """
    Test the case where we have Md022 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: The extra line between the pragma and the SetExt causes the "before" part of the rule
    not to trigger, leaving only the one trigger after the SetExt.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """--------
<!-- pyml disable-next-line blanks-around-headings -->

SetExt
------
Some text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md023_no_pragma_then_leading_spaces_before_atx() -> None:
    """
    Test the case where we have Md023 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Some text

  ## Heading 2

Some more text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md023_pragma_without_space_then_leading_spaces_before_atx() -> (
    None
):
    """
    Test the case where we have Md023 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Some text

<!-- pyml disable-next-line heading-start-left -->
  ## Heading 2

Some more text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md023_pragma_with_space_then_leading_spaces_before_atx() -> (
    None
):
    """
    Test the case where we have Md023 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Some text

<!-- pyml disable-next-line heading-start-left -->

  ## Heading 2

Some more text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md023_no_pragma_then_leading_spaces_before_setext() -> None:
    """
    Test the case where we have Md023 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Some text

  Heading 2
  ---------

Some more text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:3: MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md023_pragma_without_space_then_leading_spaces_before_setext() -> (
    None
):
    """
    Test the case where we have Md023 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Some text

<!-- pyml disable-next-line heading-start-left -->
  Heading 2
  ---------

Some more text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md023_pragma_with_space_then_leading_spaces_before_setext() -> (
    None
):
    """
    Test the case where we have Md023 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Some text

<!-- pyml disable-next-line heading-start-left -->

  Heading 2
  ---------

Some more text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md024_no_pragma_then_atx_with_same_title() -> None:
    """
    Test the case where we have Md024 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Some text

## Some text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md024_pragma_without_space_then_atx_with_same_title() -> (
    None
):
    """
    Test the case where we have Md024 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Some text

<!-- pyml disable-next-line no-duplicate-heading -->
## Some text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md024_pragma_with_space_then_atx_with_same_title() -> None:
    """
    Test the case where we have Md024 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Some text

<!-- pyml disable-next-line no-duplicate-heading -->

## Some text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md024_no_pragma_then_setext_with_same_title() -> None:
    """
    Test the case where we have Md024 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Some text

Some text
--------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md003",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md024_pragma_without_space_then_setext_with_same_title() -> (
    None
):
    """
    Test the case where we have Md024 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Some text

<!-- pyml disable-next-line no-duplicate-heading -->
Some text
--------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md003",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md024_pragma_with_space_then_setext_with_same_title() -> (
    None
):
    """
    Test the case where we have Md024 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Some text

<!-- pyml disable-next-line no-duplicate-heading -->

## Some text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md003",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md025_no_pragma_then_atx_atx() -> None:
    """
    Test the case where we have Md025 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# This is a top level heading

No other headings.

# This is another top level heading

No other headings.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:5:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md025_pragma_without_space_then_atx_atx() -> None:
    """
    Test the case where we have Md025 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# This is a top level heading

No other headings.

<!-- pyml disable-next-line single-title -->
# This is another top level heading

No other headings.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md025_pragma_with_space_then_atx_atx() -> None:
    """
    Test the case where we have Md025 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# This is a top level heading

No other headings.

<!-- pyml disable-next-line single-title -->

# This is another top level heading

No other headings.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md025_no_pragma_then_atx_setext() -> None:
    """
    Test the case where we have Md025 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# This is a top level heading

No other headings.

This is another top level heading
=========

No other headings.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md003",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:5:1: MD025: Multiple top-level headings in the same document (single-title,single-h1)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md025_pragma_without_space_then_atx_setext() -> None:
    """
    Test the case where we have Md025 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# This is a top level heading

No other headings.

<!-- pyml disable-next-line single-title -->
This is another top level heading
=========

No other headings.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md003",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md025_pragma_with_space_then_atx_setext() -> None:
    """
    Test the case where we have Md025 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# This is a top level heading

No other headings.

<!-- pyml disable-next-line single-title -->

This is another top level heading
=========

No other headings.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md003",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_trivial() -> None:
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.

    Note: Bqs within bqs is a special case.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """>  this is text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"{markdown_file_path}:1:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_trivial() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  this is text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md007,md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_trivial() -> None:
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  this is text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md007,md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_block_quote() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.

    Note: Bqs within bqs is a special case.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  > just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_ordered_list_start() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.

    Note: Bqs within bqs is a special case.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  1. just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md007,md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"{markdown_file_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_ordered_list_start() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  1. just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md007,md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_ordered_list_start() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  1. just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md007,md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_double_block_quote_with_space_before_ordered_list_start() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.

    Note: Bqs within bqs is a special case.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> > this is text
> >  1. just normal text
> > a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md007,md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"{markdown_file_path}:2:5: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_double_block_quote_with_space_before_ordered_list_start() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> > this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
> >  1. just normal text
> > a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md007,md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_double_block_quote_with_space_before_ordered_list_start() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> > this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

> >  1. just normal text
> > a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md007,md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_ordered_list_li() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.

    Note: Bqs within bqs is a special case.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> 1. start of list
>  1. just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md005,md007,md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"{markdown_file_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_ordered_list_li() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> 1. start of list
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  1. just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md005,md007,md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_ordered_list_li() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> 1. start of list
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  1. just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md007,md028,md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_unordered_list_start() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.

    Note: Bqs within bqs is a special case.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  + just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md007,md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"{markdown_file_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_unordered_list_start() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  + just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md007,md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_unordered_list_start() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  + just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md007,md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_unordered_list_li() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.

    Note: Bqs within bqs is a special case.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> + start of list
>  + just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md005,md007,md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"{markdown_file_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_unordered_list_li() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> + start of list
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  + just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md005,md007,md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_unordered_list_li() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> + start of list
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  + just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md007,md028,md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_thematic() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  ______
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_thematic() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  ______
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_thematic() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  ______
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_atx() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  # atx heading
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_atx() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  # atx heading
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_atx() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  # atx heading
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_setext_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  setext heading
> ==============
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_setext_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  setext heading
> ==============
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_setext_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  setext heading
> ==============
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_setext_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> setext heading
>  ==============
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_setext_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> setext heading
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  ==============
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_setext_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> setext heading
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  ==============
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_setext_both_lines() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  setext heading
>  ==============
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{markdown_file_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_setext_both_lines() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  setext heading
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  ==============
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_setext_both_lines() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> setext heading
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  ==============
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_icb_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.

    Note: Indented Code Blocks cannot interrupt paragraphs, so a blank line is needed.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>
>      icb 1
>     icb 2
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_fcb_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  ```text
> some text
> ```
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_fcb_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  ```text
> some text
> ```
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_fcb_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  ```text
> some text
> ```
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md028,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_fcb_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.

    Note: as the extra indented space is within the fence start of the code block, it is not a violation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> ```text
>  some text
> ```
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_fcb_third_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> ```text
> some text
>  ```
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_fcb_third_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> ```text
> some text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  ```
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_fcb_third_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> ```text
> some text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  ```
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md031,md040,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_fcb_all_lines() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  ```text
>  some text
>  ```
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)
{markdown_file_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_fcb_all_lines() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  ```text
>  some text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  ```
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_fcb_all_lines() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  ```text
>  some text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  ```
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md040,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_html_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  <-- this
> is a
> comment -->
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_html_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  <-- this
> is a
> comment -->
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_html_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  <-- this
> is a
> comment -->
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_html_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> <-- this
>  is a
> comment -->
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_html_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> <-- this
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  is a
> comment -->
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_html_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> <-- this
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  is a
> comment -->
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_html_third_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> <-- this
> is a
>  comment -->
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_html_third_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> <-- this
> is a
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  comment -->
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_html_third_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> <-- this
> is a
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  comment -->
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_lrd_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  [abc]:
> /url
> "title"
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_lrd_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  [abc]:
> /url
> "title"
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_lrd_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  [abc]:
> /url
> "title"
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_lrd_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> [abc]:
>  /url
> "title"
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_lrd_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> [abc]:
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  /url
> "title"
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_lrd_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> [abc]:
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  /url
> "title"
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_lrd_third_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> [abc]:
> /url
>  "title"
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_lrd_third_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> [abc]:
> /url
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  "title"
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md023,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_lrd_third_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> [abc]:
> /url
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  "title"
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
@pytest.mark.skip(reason="https://github.com/jackdewinter/pymarkdown/issues/1515")
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_table_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  | abc | def |
> | --- | --- |
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-extensions",
            "markdown-tables",
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:4:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
@pytest.mark.skip(reason="https://github.com/jackdewinter/pymarkdown/issues/1515")
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_table_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  | abc | def |
> | --- | --- |
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-extensions",
            "markdown-tables",
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
@pytest.mark.skip(reason="https://github.com/jackdewinter/pymarkdown/issues/1515")
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_table_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> [abc]:
> /url
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  "title"
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-extensions",
            "markdown-tables",
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
@pytest.mark.skip(reason="https://github.com/jackdewinter/pymarkdown/issues/1515")
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_table_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> | abc | def |
>  | --- | --- |
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-extensions",
            "markdown-tables",
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
@pytest.mark.skip(reason="https://github.com/jackdewinter/pymarkdown/issues/1515")
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_table_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
> | abc | def |
>  | --- | --- |
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-extensions",
            "markdown-tables",
            "-d",
            "md022,md023,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
@pytest.mark.skip(reason="https://github.com/jackdewinter/pymarkdown/issues/1515")
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_table_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> [abc]:
> /url
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  "title"
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-extensions",
            "markdown-tables",
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_text_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_text_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_text_first_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_text_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> this is still text
>  just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_text_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> this is still text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_text_second_line() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
> this is still text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  just normal text
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_no_pragma_then_block_quote_with_space_before_codespan() -> (
    None
):
    """
    Test the case where we have Md027 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
>  `code span`
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:3: MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_without_space_then_block_quote_with_space_before_codespan() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->
>  `code span`
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md027_pragma_with_space_then_block_quote_with_space_before_codespan() -> (
    None
):
    """
    Test the case where we have Md027 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is text
<!-- pyml disable-next-line no-multiple-space-blockquote -->

>  `code span`
> a real test
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md028,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md028_no_pragma_then_block_quote_with_blank() -> None:
    """
    Test the case where we have Md028 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> This is one section of a block quote

> This is the other section.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD028: Blank line inside blockquote (no-blanks-blockquote)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md028_pragma_without_space_then_block_quote_with_blank() -> (
    None
):
    """
    Test the case where we have Md028 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> This is one section of a block quote
<!-- pyml disable-next-line no-blanks-blockquote -->

> This is the other section.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md028_pragma_with_space_then_block_quote_with_blank() -> (
    None
):
    """
    Test the case where we have Md028 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: This is a weird scenario.  Both blanks on lines 3 and 4 are disabled due to the pragma.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> This is one section of a block quote
<!-- pyml disable-next-line no-blanks-blockquote -->


> This is the other section.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md012,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md029_no_pragma_then_ol_ol_ol_out_of_order() -> None:
    """
    Test the case where we have Md029 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. Simple
2. One
1. List
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD029: Ordered list item prefix [Expected: 3; Actual: 1; Style: 1/2/3] (ol-prefix)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md029_pragma_without_space_then_ol_ol_ol_out_of_order() -> (
    None
):
    """
    Test the case where we have Md029 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. Simple
2. One
<!-- pyml disable-next-line ol-prefix -->
1. List
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md029_pragma_with_space_then_ol_ol_ol_out_of_order() -> (
    None
):
    """
    Test the case where we have Md029 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. Simple
2. One
<!-- pyml disable-next-line ol-prefix -->

1. List
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md029_no_pragma_then_ol_ol_ol_bad_start() -> None:
    """
    Test the case where we have Md029 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """3. Simple
2. One
1. List
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD029: Ordered list item prefix [Expected: 1; Actual: 3; Style: 1/2/3] (ol-prefix)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md029_pragma_without_space_then_ol_ol_ol_bad_start() -> (
    None
):
    """
    Test the case where we have Md029 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line ol-prefix -->
3. Simple
2. One
1. List
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md029_pragma_with_space_then_ol_ol_ol_bad_start() -> None:
    """
    Test the case where we have Md029 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line ol-prefix -->

3. Simple
2. One
1. List
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md030_no_pragma_then_ul_extra_indent_ul_extra_indent() -> (
    None
):
    """
    Test the case where we have Md030 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """*  First
*  Second
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{markdown_file_path}:2:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md030_pragma_without_space_then_ul_extra_indent_ul_extra_indent() -> (
    None
):
    """
    Test the case where we have Md030 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line list-marker-space -->
*  First
<!-- pyml disable-next-line list-marker-space -->
*  Second
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md030_pragma_with_space_then_ul_extra_indent_ul_extra_indent() -> (
    None
):
    """
    Test the case where we have Md030 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line list-marker-space -->

*  First
<!-- pyml disable-next-line list-marker-space -->

*  Second
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md030_no_pragma_then_ol_extra_indent_ol_extra_indent() -> (
    None
):
    """
    Test the case where we have Md030 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1.  First
1.  Second
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)
{markdown_file_path}:2:1: MD030: Spaces after list markers [Expected: 1; Actual: 2] (list-marker-space)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md030_pragma_without_space_then_ol_extra_indent_ol_extra_indent() -> (
    None
):
    """
    Test the case where we have Md030 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line list-marker-space -->
1.  First
<!-- pyml disable-next-line list-marker-space -->
1.  Second
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md030_pragma_with_space_then_ol_extra_indent_ol_extra_indent() -> (
    None
):
    """
    Test the case where we have Md030 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line list-marker-space -->

1.  First
<!-- pyml disable-next-line list-marker-space -->

1.  Second
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_no_pragma_then_thematic_fenced_block_thematic() -> (
    None
):
    """
    Test the case where we have Md031 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """---
```block
A code block
```
---
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{markdown_file_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_without_space_then_thematic_fenced_block_thematic() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """---
<!-- pyml disable-next-line blanks-around-fences -->
```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->
```
---
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_with_space_then_thematic_fenced_block_thematic() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: The adding of the blank lines after the pragmas affected the rule. For the first
        pragmas, the blank line after it means that the code block is now properly preceded
        by a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """---
<!-- pyml disable-next-line line-length -->

```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->

```
---
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_no_pragma_then_atx_fenced_block_atx() -> None:
    """
    Test the case where we have Md031 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Atx Heading
```block
A code block
```
## Another Atx Heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{markdown_file_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_without_space_then_atx_fenced_block_atx() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Atx Heading
<!-- pyml disable-next-line blanks-around-fences -->
```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->
```
## Another Atx Heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_with_space_then_atx_fenced_block_atx() -> None:
    """
    Test the case where we have Md031 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: The adding of the blank lines after the pragmas affected the rule. For the first
        pragmas, the blank line after it means that the code block is now properly preceded
        by a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Atx Heading
<!-- pyml disable-next-line line-length -->

```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->

```
## Another Atx Heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_no_pragma_then_setext_fenced_block_setext() -> None:
    """
    Test the case where we have Md031 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """SetExt Heading
---
```block
A code block
```
Another SetExt Heading
===
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{markdown_file_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_without_space_then_setext_fenced_block_setext() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """SetExt Heading
---
<!-- pyml disable-next-line blanks-around-fences -->
```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->
```
Another SetExt Heading
===
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_with_space_then_setext_fenced_block_setext() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: The adding of the blank lines after the pragmas affected the rule. For the first
        pragmas, the blank line after it means that the code block is now properly preceded
        by a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """SetExt Heading
---
<!-- pyml disable-next-line line-length -->

```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->

```
Another SetExt Heading
===
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_no_pragma_then_icb_fenced_block_icb() -> None:
    """
    Test the case where we have Md031 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """    Indented Code Block
```block
A code block
```
    Another Indented Code Block
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md041,md046",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{markdown_file_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_without_space_then_icb_fenced_block_icb() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """    Indented Code Block
<!-- pyml disable-next-line blanks-around-fences -->
```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->
```
    Another Indented Code Block
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md041,md046",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_with_space_then_icb_fenced_block_icb() -> None:
    """
    Test the case where we have Md031 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: The adding of the blank lines after the pragmas affected the rule. For the first
        pragmas, the blank line after it means that the code block is now properly preceded
        by a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """    Indented Code Block
<!-- pyml disable-next-line line-length -->

```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->

```
    Another Indented Code Block
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md041,md046",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_no_pragma_then_fenced_block_fenced_block() -> None:
    """
    Test the case where we have Md031 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```block
A code block
```
```block
A code block
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md041,md046",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{markdown_file_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_without_space_then_fenced_block_fenced_block() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->
```
<!-- pyml disable-next-line blanks-around-fences -->
```block
A code block
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md041,md046",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_with_space_then_fenced_block_fenced_block() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: The adding of the blank lines after the pragmas affected the rule. For both
        pragmas, the blank lines mean that both code blocks are now properly surrounded
        by the proper blank lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```block
A code block
<!-- pyml disable-next-line line-length -->

```
<!-- pyml disable-next-line line-length -->

```block
A code block
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_no_pragma_then_html_block_fenced_block_html_block() -> (
    None
):
    """
    Test the case where we have Md031 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<script>
</script>
```block
A code block
```
<script>
</script>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{markdown_file_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_without_space_then_html_block_fenced_block_html_block() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<script>
</script>
<!-- pyml disable-next-line blanks-around-fences -->
```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->
```
<script>
</script>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_with_space_then_html_block_fenced_block_html_block() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: The adding of the blank lines after the pragmas affected the rule. For the first
        pragmas, the blank line after it means that the code block is now properly preceded
        by a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<script>
</script>
<!-- pyml disable-next-line line-length -->

```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->

```
<script>
</script>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_no_pragma_then_lrd_fenced_block_lrd() -> None:
    """
    Test the case where we have Md031 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """[lrd]: /url
```block
A code block
```
[lrd]: /url
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{markdown_file_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_without_space_then_lrd_fenced_block_lrd() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """[lrd]: /url
<!-- pyml disable-next-line blanks-around-fences -->
```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->
```
[lrd]: /url
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_with_space_then_lrd_fenced_block_lrd() -> None:
    """
    Test the case where we have Md031 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: The adding of the blank lines after the pragmas affected the rule. For the first
        pragmas, the blank line after it means that the code block is now properly preceded
        by a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """[lrd]: /url
<!-- pyml disable-next-line line-length -->

```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->

```
[lrd]: /url
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_no_pragma_then_para_fenced_block_para() -> None:
    """
    Test the case where we have Md031 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """first paragraph
```block
A code block
```
second paragraph
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{markdown_file_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_without_space_then_para_fenced_block_para() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """first paragraph
<!-- pyml disable-next-line blanks-around-fences -->
```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->
```
second paragraph
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_with_space_then_para_fenced_block_para() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: The adding of the blank lines after the pragmas affected the rule. For the first
        pragmas, the blank line after it means that the code block is now properly preceded
        by a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """first paragraph
<!-- pyml disable-next-line line-length -->

```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->

```
second paragraph
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_no_pragma_then_table_fenced_block_table() -> None:
    """
    Test the case where we have Md031 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """| abc | def |
| --- | --- |
```block
A code block
```
| abc | def |
| --- | --- |
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-extensions",
            "markdown-tables",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{markdown_file_path}:5:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_without_space_then_table_fenced_block_table() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """| abc | def |
| --- | --- |
<!-- pyml disable-next-line blanks-around-fences -->
```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->
```
| abc | def |
| --- | --- |
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-extensions",
            "markdown-tables",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_with_space_then_table_fenced_block_table() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: The adding of the blank lines after the pragmas affected the rule. For the first
        pragmas, the blank line after it means that the code block is now properly preceded
        by a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """| abc | def |
| --- | --- |
<!-- pyml disable-next-line line-length -->

```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->

```
| abc | def |
| --- | --- |
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_no_pragma_then_ul_fenced_block_ul() -> None:
    """
    Test the case where we have Md031 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """+ first list
```block
A code block
```
+ second list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{markdown_file_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_without_space_then_ul_fenced_block_ul() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """+ first list
<!-- pyml disable-next-line blanks-around-fences -->
```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->
```
+ second list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_with_space_then_ul_fenced_block_ul() -> None:
    """
    Test the case where we have Md031 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: The adding of the blank lines after the pragmas affected the rule. For the first
        pragmas, the blank line after it means that the code block is now properly preceded
        by a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """+ first list
<!-- pyml disable-next-line line-length -->

```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->

```
+ second list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_no_pragma_then_ol_fenced_block_ol() -> None:
    """
    Test the case where we have Md031 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. first list
```block
A code block
```
1. second list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{markdown_file_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_without_space_then_ol_fenced_block_ol() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. first list
<!-- pyml disable-next-line blanks-around-fences -->
```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->
```
1. second list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_with_space_then_ol_fenced_block_ol() -> None:
    """
    Test the case where we have Md031 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: The adding of the blank lines after the pragmas affected the rule. For the first
        pragmas, the blank line after it means that the code block is now properly preceded
        by a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. first list
<!-- pyml disable-next-line line-length -->

```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->

```
1. second list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_no_pragma_then_bq_fenced_block_bq() -> None:
    """
    Test the case where we have Md031 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> first quote
```block
A code block
```
> second quote
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)
{markdown_file_path}:4:1: MD031: Fenced code blocks should be surrounded by blank lines (blanks-around-fences)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_without_space_then_bq_fenced_block_bq() -> (
    None
):
    """
    Test the case where we have Md031 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> first quote
<!-- pyml disable-next-line blanks-around-fences -->
```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->
```
> second quote
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md032,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md031_pragma_with_space_then_bq_fenced_block_bq() -> None:
    """
    Test the case where we have Md031 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: The adding of the blank lines after the pragmas affected the rule. For the first
        pragmas, the blank line after it means that the code block is now properly preceded
        by a blank line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> first quote
<!-- pyml disable-next-line line-length -->

```block
A code block
<!-- pyml disable-next-line blanks-around-fences -->

```
> second quote
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_bq_ul_ul_bq() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is a block quote
+ a list
+ still a list
+ still still a list
> this is a block quote
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{markdown_file_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_bq_ul_ul_bq() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is a block quote
<!-- pyml disable-next-line blanks-around-lists -->
+ a list
+ still a list
<!-- pyml disable-next-line blanks-around-lists -->
+ still still a list
> this is a block quote
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_bq_ul_ul_bq() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: This "pragma with space" scenario creates a blank line before the start of the list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is a block quote
<!-- pyml disable-next-line line-length -->

+ a list
+ still a list
<!-- pyml disable-next-line blanks-around-lists -->

+ still still a list
> this is a block quote
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_bq_ul_ul_2_lines_bq() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is a block quote
+ a list
+ still a list
+ still still a list
  just a longer item
> this is a block quote
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{markdown_file_path}:5:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_bq_ul_ul_2_lines_bq() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is a block quote
<!-- pyml disable-next-line blanks-around-lists -->
+ a list
+ still a list
+ still still a list
<!-- pyml disable-next-line blanks-around-lists -->
  just a longer item
> this is a block quote
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_bq_ul_ul_2_lines_bq() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: This "pragma with space" scenario creates a blank line before the start of the list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is a block quote
<!-- pyml disable-next-line line-length -->

+ a list
+ still a list
+ still still a list
<!-- pyml disable-next-line blanks-around-lists -->

  just a longer item
> this is a block quote
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_bq_ol_ol_ol_bq() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is a block quote
1. a list
1. still a list
1. still still a list
> this is a block quote
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{markdown_file_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_bq_ol_ol_ol_bq() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is a block quote
<!-- pyml disable-next-line blanks-around-lists -->
1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->
1. still still a list
> this is a block quote
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_bq_ol_ol_bq() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: This "pragma with space" scenario creates a blank line before the start of the list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """> this is a block quote
<!-- pyml disable-next-line line-length -->

1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->

1. still still a list
> this is a block quote
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_ul_ol_ol_ol_ul() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """+ this is a list
1. a list
1. still a list
+ this is a list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{markdown_file_path}:2:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{markdown_file_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{markdown_file_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_ul_ol_ol_ol_ul() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line blanks-around-lists -->
+ this is a list
<!-- pyml disable-next-line blanks-around-lists -->
1. a list
<!-- pyml disable-next-line blanks-around-lists -->
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->
+ this is a list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_ul_ol_ol_ol_ul() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: This "pragma with space" scenario creates a blank line before the start of the list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line blanks-around-lists -->

+ this is a list
<!-- pyml disable-next-line blanks-around-lists -->

1. a list
<!-- pyml disable-next-line blanks-around-lists -->

1. still a list
<!-- pyml disable-next-line blanks-around-lists -->

+ this is a list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_thematic_ol_ol_thematic() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """___
1. a list
1. still a list
1. still still a list
___
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md024,md025,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{markdown_file_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_thematic_ol_ol_thematic() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """___
<!-- pyml disable-next-line blanks-around-lists -->
1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->
1. still still a list
___
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md024,md025,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_thematic_ol_ol_thematic() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: This "pragma with space" scenario creates a blank line before the start of the list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """___
<!-- pyml disable-next-line blanks-around-lists -->

1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->

1. still still a list
___
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md024,md025,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_atx_ol_ol_atx() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# this is an atx heading
1. a list
1. still a list
1. still still a list
# this is an atx heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md024,md025,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{markdown_file_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_atx_ol_ol_atx() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# this is an atx heading
<!-- pyml disable-next-line blanks-around-lists -->
1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->
1. still still a list
# this is an atx heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md024,md025,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_atx_ol_ol_atx() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: This "pragma with space" scenario creates a blank line before the start of the list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# this is an atx heading
<!-- pyml disable-next-line line-length -->

1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->

1. still still a list
# this is an atx heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md024,md025,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_setext_ol_ol_setext() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.

    Note: Since setext headings cannot interrupt paragraphs and a paragraph was starting
          in the last list item, the `---` line becomes a thematic break, and the violation
          is reported there.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is a setext heading
=====
1. a list
1. still a list
1. still still a list
this is a setext heading
-----
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md024,md025,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{markdown_file_path}:6:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_setext_ol_ol_setext() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.

    Note: Since setext headings cannot interrupt paragraphs and a paragraph was starting
          in the last list item, the `---` line becomes a thematic break, and the violation
          is reported there.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is a setext heading
=====
<!-- pyml disable-next-line blanks-around-lists -->
1. a list
1. still a list
1. still still a list
<!-- pyml disable-next-line blanks-around-lists -->
this is a setext heading
-----
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md024,md025,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_setext_ol_ol_setext() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: This "pragma with space" scenario creates a blank line before the start of the list.
    Note: Since setext headings cannot interrupt paragraphs and a paragraph was starting
          in the last list item, the `---` line becomes a thematic break, and the violation
          is reported there.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is a setext heading
=====
<!-- pyml disable-next-line line-length -->

1. a list
1. still a list
1. still still a list
<!-- pyml disable-next-line line-length -->

this is a setext heading
-----
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md024,md025,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_fenced_ol_ol_fenced() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```text
```
1. a list
1. still a list
1. still still a list
```text
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md024,md025,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{markdown_file_path}:5:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_fenced_ol_ol_fenced() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```text
```
<!-- pyml disable-next-line blanks-around-lists -->
1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->
1. still still a list
```text
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md024,md025,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_fenced_ol_ol_fenced() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: This "pragma with space" scenario creates a blank line before the start of the list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```text
```
<!-- pyml disable-next-line line-length -->

1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->

1. still still a list
```text
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md024,md025,md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_html_ol_ol_html() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<script>
</script>
1. a list
1. still a list
1. still still a list
<script>
</script>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{markdown_file_path}:5:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_html_ol_ol_html() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<script>
</script>
<!-- pyml disable-next-line blanks-around-lists -->
1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->
1. still still a list
<script>
</script>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_html_ol_ol_html() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: This "pragma with space" scenario creates a blank line before the start of the list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<script>
</script>
<!-- pyml disable-next-line line-length -->

1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->

1. still still a list
<script>
</script>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_lrd_ol_ol_lrd() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.

    Note: Since lrds cannot interrupt paragraphs and a paragraph was starting
          in the last list item, the lrd gets broken up to an inline link and the test `: /url
          is reported there.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """[lrd]: /url
1. a list
1. still a list
1. still still a list
[lrd]: /url
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_lrd_ol_ol_lrd() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.

    Note: Since lrds cannot interrupt paragraphs and a paragraph was starting
          in the last list item, the lrd gets broken up to an inline link and the test `: /url
          is reported there.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """[lrd]: /url
<!-- pyml disable-next-line blanks-around-lists -->
1. a list
1. still a list
1. still still a list
[lrd]: /url
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_lrd_ol_ol_lrd() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: This "pragma with space" scenario creates a blank line before the start of the list.
    Note: Since lrds cannot interrupt paragraphs and a paragraph was starting
          in the last list item, the lrd gets broken up to an inline link and the test `: /url
          is reported there.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """[lrd]: /url
<!-- pyml disable-next-line line-length -->

1. a list
1. still a list
1. still still a list
[lrd]: /url
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_table_ol_ol_table() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.

    Note: Since tables cannot interrupt paragraphs and a paragraph was starting
          in the last list item, the lrd gets broken up to an inline link and the test `: /url
          is reported there.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """| abc | def |
| --- | --- |
1. a list
1. still a list
1. still still a list
| abc | def |
| --- | --- |
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-extensions",
            "markdown-tables",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_table_ol_ol_table() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """| abc | def |
| --- | --- |
<!-- pyml disable-next-line blanks-around-lists -->
1. a list
1. still a list
1. still still a list
| abc | def |
| --- | --- |
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_table_ol_ol_table() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    Note: This "pragma with space" scenario creates a blank line before the start of the list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """| abc | def |
| --- | --- |
<!-- pyml disable-next-line line-length -->

1. a list
1. still a list
1. still still a list
| abc | def |
| --- | --- |
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_ol_ol_with_bq_and_bq() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   > inner bq
> outer bq
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_ol_ol_with_bq_and_bq() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->
   > inner bq
> outer bq
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_ol_ol_with_bq_and_bq() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->

   > inner bq
> outer bq
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_ol_ol_with_ul_and_ul() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   + inner list
+ outer list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)
{markdown_file_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_ol_ol_with_ul_and_ul() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->
   + inner list
<!-- pyml disable-next-line blanks-around-lists -->
+ outer list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_ol_ol_with_ul_and_ul() -> None:
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->

   _______
_______
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_ol_ol_with_thematic_and_thematic() -> (
    None
):
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   _______
_______
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_ol_ol_with_thematic_and_thematic() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->
   _______
_______
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_ol_ol_with_thematic_and_thematic() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->

   _______
_______
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_ol_ol_with_atx_and_atx() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   # atx within a list
# not a list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-extensions",
            "markdown-tables",
            "-d",
            "md022,md025,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_ol_ol_with_atx_and_atx() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->
   # atx within a list
# not a list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md025,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_ol_ol_with_atx_and_atx() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
<!-- pyml disable-next-line blanks-around-lists -->

   # atx within a list
# not a list
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md022,md025,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_ol_ol_with_fcb_and_fcb() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   ```text
   ```
```text
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_ol_ol_with_fcb_and_fcb() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   ```text
<!-- pyml disable-next-line blanks-around-lists -->
   ```
```text
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_ol_ol_with_fcb_and_fcb() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   ```text
<!-- pyml disable-next-line blanks-around-lists -->

   ```
```text
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_ol_ol_with_fcb_text_and_fcb() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   ```text
   some text
   ```
```text
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:5:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_ol_ol_with_fcb_text_and_fcb() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   ```text
   some text
<!-- pyml disable-next-line blanks-around-lists -->
   ```
```text
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_ol_ol_with_fcb_text_and_fcb() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   ```text
   some text
<!-- pyml disable-next-line blanks-around-lists -->

   ```
```text
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_ol_ol_with_fcb_text_nl_and_fcb() -> (
    None
):
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   ```text
   some text

   ```
```text
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:6:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_ol_ol_with_fcb_text_nl_and_fcb() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   ```text
   some text

<!-- pyml disable-next-line blanks-around-lists -->
   ```
```text
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_ol_ol_with_fcb_text_nl_and_fcb() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   ```text
   some text

<!-- pyml disable-next-line blanks-around-lists -->

   ```
```text
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md031,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_no_pragma_then_ol_ol_with_html_and_html() -> None:
    """
    Test the case where we have Md032 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   <script>
   </script>
<script>
</script>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:4:1: MD032: Lists should be surrounded by blank lines (blanks-around-lists)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_without_space_then_ol_ol_with_html_and_html() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   <script>
<!-- pyml disable-next-line blanks-around-lists -->
   </script>
<script>
</script>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md032_pragma_with_space_then_ol_ol_with_html_and_html() -> (
    None
):
    """
    Test the case where we have Md032 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """1. a list
1. still a list
   <script>
<!-- pyml disable-next-line blanks-around-lists -->

   </script>
<script>
</script>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "md033,md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md033_no_pragma_then_html_block() -> None:
    """
    Test the case where we have Md033 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<img src="fred">
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD033: Inline HTML [Element: img] (no-inline-html)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md033_pragma_without_space_then_html_block() -> None:
    """
    Test the case where we have Md033 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-inline-html -->
<img src="fred">
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md033_pragma_with_space_then_html_block() -> None:
    """
    Test the case where we have Md033 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-inline-html -->

<img src="fred">
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md033_no_pragma_then_text_with_inline_html_first_line() -> (
    None
):
    """
    Test the case where we have Md033 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is paragraph <img src="fred"> with in image embedded.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:19: MD033: Inline HTML [Element: img] (no-inline-html)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md033_pragma_without_space_then_text_with_inline_html_first_line() -> (
    None
):
    """
    Test the case where we have Md033 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-inline-html -->
This is paragraph <img src="fred"> with in image embedded.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md033_pragma_with_space_then_text_with_inline_html_first_line() -> (
    None
):
    """
    Test the case where we have Md033 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-inline-html -->

This is paragraph <img src="fred"> with in image embedded.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md033_no_pragma_then_text_with_non_first_line_inline_html() -> (
    None
):
    """
    Test the case where we have Md033 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is a paragraph with an image embedded
in something other <img src="fred"> than the first line.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:20: MD033: Inline HTML [Element: img] (no-inline-html)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md033_pragma_without_space_then_text_with_non_first_line_inline_html() -> (
    None
):
    """
    Test the case where we have Md033 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is a paragraph with an image embedded
<!-- pyml disable-next-line no-inline-html -->
in something other <img src="fred"> than the first line.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md033_pragma_with_space_then_text_with_non_first_line_inline_html() -> (
    None
):
    """
    Test the case where we have Md033 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is a paragraph with an image embedded
<!-- pyml disable-next-line no-inline-html -->

in something other <img src="fred"> than the first line.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md034_no_pragma_then_para_with_url_first_line() -> None:
    """
    Test the case where we have Md034 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This text has a bare http URL http://www.google.com in it.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"""{markdown_file_path}:1:31: MD034: Bare URL used (no-bare-urls)"""
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md034_pragma_without_space_then_para_with_url_first_line() -> (
    None
):
    """
    Test the case where we have Md034 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-bare-urls -->
This text has a bare http URL http://www.google.com in it.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md034_pragma_with_space_then_para_with_url_first_line() -> (
    None
):
    """
    Test the case where we have Md034 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-bare-urls -->

This text has a bare http URL http://www.google.com in it.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md034_no_pragma_then_para_with_url_second_line() -> None:
    """
    Test the case where we have Md034 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This text has a bare
http URL http://www.google.com in it.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"""{markdown_file_path}:2:10: MD034: Bare URL used (no-bare-urls)"""
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md034_pragma_without_space_then_para_with_url_second_line() -> (
    None
):
    """
    Test the case where we have Md034 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This text has a bare
<!-- pyml disable-next-line no-bare-urls -->
http URL http://www.google.com in it.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md034_pragma_with_space_then_para_with_url_second_line() -> (
    None
):
    """
    Test the case where we have Md034 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This text has a bare
<!-- pyml disable-next-line no-bare-urls -->

http URL http://www.google.com in it.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md035_no_pragma_then_tb_text_tb() -> None:
    """
    Test the case where we have Md035 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """---
this is one section
- - -
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD035: Horizontal rule style [Expected: ---, Actual: - - -] (hr-style)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md035_pragma_without_space_then_tb_text_tb() -> None:
    """
    Test the case where we have Md035 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """---
this is one section
<!-- pyml disable-next-line hr-style -->
- - -
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md035_pragma_with_space_then_tb_text_tb() -> None:
    """
    Test the case where we have Md035 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """---
this is one section
<!-- pyml disable-next-line hr-style -->

- - -
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md036_no_pragma_then_text_in_emphasis_with_para_following() -> (
    None
):
    """
    Test the case where we have Md036 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """**text**

Lorem ipsum dolor sit amet...
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md036_pragma_without_space_then_text_in_emphasis_with_para_following() -> (
    None
):
    """
    Test the case where we have Md036 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-emphasis-as-heading -->
**text**

Lorem ipsum dolor sit amet...
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md036_pragma_with_space_then_text_in_emphasis_with_para_following() -> (
    None
):
    """
    Test the case where we have Md036 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-emphasis-as-heading -->

**text**

Lorem ipsum dolor sit amet...
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md037_no_pragma_then_text_with_space_within_emphasis_first_line() -> (
    None
):
    """
    Test the case where we have Md037 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this text * is* in italics
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md037_pragma_without_space_then_text_with_space_within_emphasis_first_line() -> (
    None
):
    """
    Test the case where we have Md037 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-space-in-emphasis -->
this text * is* in italics
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md037_pragma_with_space_then_text_with_space_within_emphasis_first_line() -> (
    None
):
    """
    Test the case where we have Md037 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-space-in-emphasis -->

this text * is* in italics
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md037_no_pragma_then_text_with_space_within_emphasis_second_line() -> (
    None
):
    """
    Test the case where we have Md037 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is the first line
this text * is* in italics
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:12: MD037: Spaces inside emphasis markers (no-space-in-emphasis)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md037_pragma_without_space_then_text_with_space_within_emphasis_second_line() -> (
    None
):
    """
    Test the case where we have Md037 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is the first line
<!-- pyml disable-next-line no-space-in-emphasis -->
this text * is* in italics
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md037_pragma_with_space_then_text_with_space_within_emphasis_second_line() -> (
    None
):
    """
    Test the case where we have Md037 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is the first line
<!-- pyml disable-next-line no-space-in-emphasis -->

this text * is* in italics
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md038_no_pragma_then_text_with_code_span_first_line() -> (
    None
):
    """
    Test the case where we have Md038 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is ` bad code span` text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:9: MD038: Spaces inside code span elements (no-space-in-code)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md038_pragma_without_space_then_text_with_code_span_first_line() -> (
    None
):
    """
    Test the case where we have Md038 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-space-in-code -->
this is ` bad code span` text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md038_pragma_with_space_then_text_with_code_span_first_line() -> (
    None
):
    """
    Test the case where we have Md038 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-space-in-code -->

this is ` bad code span` text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md038_no_pragma_then_text_with_code_span_second_line() -> (
    None
):
    """
    Test the case where we have Md038 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is the first line
this is ` bad code span` text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:9: MD038: Spaces inside code span elements (no-space-in-code)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md038_pragma_without_space_then_text_with_code_span_second_line() -> (
    None
):
    """
    Test the case where we have Md038 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is the first line
<!-- pyml disable-next-line no-space-in-code -->
this is ` bad code span` text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md038_pragma_with_space_then_text_with_code_span_second_line() -> (
    None
):
    """
    Test the case where we have Md038 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is the first line
<!-- pyml disable-next-line no-space-in-code -->

this is ` bad code span` text
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md039_no_pragma_then_text_with_link_first_line() -> None:
    """
    Test the case where we have Md039 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is not [ a proper ](https://www.example.com) link
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:13: MD039: Spaces inside link text (no-space-in-links)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md039_pragma_without_space_then_text_with_link_first_line() -> (
    None
):
    """
    Test the case where we have Md039 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-space-in-links -->
this is not [ a proper ](https://www.example.com) link
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md039_pragma_with_space_then_text_with_link_first_line() -> (
    None
):
    """
    Test the case where we have Md039 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-space-in-links -->

this is not [ a proper ](https://www.example.com) link
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md039_no_pragma_then_text_with_link_second_line() -> None:
    """
    Test the case where we have Md039 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is the first line
this is not [ a proper ](https://www.example.com) link
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:13: MD039: Spaces inside link text (no-space-in-links)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md039_pragma_without_space_then_text_with_link_second_line() -> (
    None
):
    """
    Test the case where we have Md039 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is the first line
<!-- pyml disable-next-line no-space-in-links -->
this is not [ a proper ](https://www.example.com) link
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md039_pragma_with_space_then_text_with_link_second_line() -> (
    None
):
    """
    Test the case where we have Md039 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is the first line
<!-- pyml disable-next-line no-space-in-links -->

this is not [ a proper ](https://www.example.com) link
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md040_no_pragma_then_fenced_code_block() -> None:
    """
    Test the case where we have Md040 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```
def func(arg1, arg2):
    return arg1 + arg2
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD040: Fenced code blocks should have a language specified (fenced-code-language)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md040_pragma_without_space_then_fenced_code_block() -> None:
    """
    Test the case where we have Md040 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line fenced-code-language -->
```
def func(arg1, arg2):
    return arg1 + arg2
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md040_pragma_with_space_then_fenced_code_block() -> None:
    """
    Test the case where we have Md040 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line fenced-code-language -->

```
def func(arg1, arg2):
    return arg1 + arg2
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md041_no_pragma_then_atx_level_2() -> None:
    """
    Test the case where we have Md041 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """## Not Top Level
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md041_pragma_without_space_then_atx_level_2() -> None:
    """
    Test the case where we have Md041 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line first-line-heading -->
## Not Top Level
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md041_pragma_with_space_then_atx_level_2() -> None:
    """
    Test the case where we have Md041 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line first-line-heading -->

## Not Top Level
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md041_no_pragma_then_setext_level_2() -> None:
    """
    Test the case where we have Md041 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Not Top Level
---------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md041_pragma_without_space_then_setext_level_2() -> None:
    """
    Test the case where we have Md041 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line first-line-heading -->
Not Top Level
---------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md041_pragma_with_space_then_setext_level_2() -> None:
    """
    Test the case where we have Md041 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line first-line-heading -->

Not Top Level
---------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md041_no_pragma_then_html_h2() -> None:
    """
    Test the case where we have Md041 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<h2>Not Top Level</h2>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md033",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md041_pragma_without_space_then_html_h2() -> None:
    """
    Test the case where we have Md041 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line first-line-heading -->
<h2>Not Top Level</h2>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md033",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md041_pragma_with_space_then_html_h2() -> None:
    """
    Test the case where we have Md041 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line first-line-heading -->

<h2>Not Top Level</h2>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md033",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md041_no_pragma_then_fenced_code_block() -> None:
    """
    Test the case where we have Md041 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```python
def bad_func():
    pass
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD041: First line in file should be a top level heading (first-line-heading,first-line-h1)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md041_pragma_without_space_then_fenced_code_block() -> None:
    """
    Test the case where we have Md041 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line first-line-heading -->
```python
def bad_func():
    pass
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md041_pragma_with_space_then_fenced_code_block() -> None:
    """
    Test the case where we have Md041 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line first-line-heading -->

```python
def bad_func():
    pass
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, suppress_first_line_heading_rule=False
        )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md042_no_pragma_then_text_with_link_first_line() -> None:
    """
    Test the case where we have Md042 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is not a [valid](#) link
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"""{markdown_file_path}:1:15: MD042: No empty links (no-empty-links)"""
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md042_pragma_without_space_then_text_with_link_first_line() -> (
    None
):
    """
    Test the case where we have Md042 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-empty-links -->
this is not a [valid](#) link
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md042_pragma_with_space_then_text_with_link_first_line() -> (
    None
):
    """
    Test the case where we have Md042 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-empty-links -->

this is not a [valid](#) link
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md042_no_pragma_then_text_with_link_second_line() -> None:
    """
    Test the case where we have Md042 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is the first line
this is not a [valid](#) link
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"""{markdown_file_path}:2:15: MD042: No empty links (no-empty-links)"""
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md042_pragma_without_space_then_text_with_link_second_line() -> (
    None
):
    """
    Test the case where we have Md042 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is the first line
<!-- pyml disable-next-line no-empty-links -->
this is not a [valid](#) link
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md042_pragma_with_space_then_text_with_link_second_line() -> (
    None
):
    """
    Test the case where we have Md042 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is the first line
<!-- pyml disable-next-line no-empty-links -->

this is not a [valid](#) link
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_no_pragma_then_atx_bad_match() -> None:
    """
    Test the case where we have Md043 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# This is a single heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md043.headings=# This is the first heading",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD043: Required heading structure [Bad heading text: Expected: This is the first heading, Actual: This is a single heading] (required-headings,required-headers)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_without_space_then_atx_bad_match() -> None:
    """
    Test the case where we have Md043 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line required-headings -->
# This is a single heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md043.headings=# This is the first heading",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_with_space_then_atx_bad_match() -> None:
    """
    Test the case where we have Md043 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line required-headings -->

# This is a single heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md043.headings=# This is the first heading",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_no_pragma_then_setext_bad_match() -> None:
    """
    Test the case where we have Md043 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is a single heading
=========
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md043.headings=# This is the first heading",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD043: Required heading structure [Bad heading text: Expected: This is the first heading, Actual: This is a single heading] (required-headings,required-headers)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_without_space_then_setext_bad_match() -> None:
    """
    Test the case where we have Md043 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line required-headings -->
This is a single heading
=========
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md043.headings=# This is the first heading",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_with_space_then_setext_bad_match() -> None:
    """
    Test the case where we have Md043 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line required-headings -->

This is a single heading
=========
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md043.headings=# This is the first heading",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_no_pragma_then_atx_extra() -> None:
    """
    Test the case where we have Md043 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# This is the first heading
# This is a single heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022,Md025",
            "--set",
            "plugins.md043.headings=# This is the first heading",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD043: Required heading structure [Extra heading] (required-headings,required-headers)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_without_space_then_atx_extra() -> None:
    """
    Test the case where we have Md043 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# This is the first heading
<!-- pyml disable-next-line required-headings -->
# This is a single heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022,Md025",
            "--set",
            "plugins.md043.headings=# This is the first heading",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_with_space_then_atx_extra() -> None:
    """
    Test the case where we have Md043 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# This is the first heading
<!-- pyml disable-next-line required-headings -->

# This is a single heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022,Md025",
            "--set",
            "plugins.md043.headings=# This is the first heading",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_no_pragma_then_setext_extra() -> None:
    """
    Test the case where we have Md043 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is the first heading
=================
This is a single heading
------------------------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022",
            "--set",
            "plugins.md043.headings=# This is the first heading",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD043: Required heading structure [Extra heading] (required-headings,required-headers)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_without_space_then_setext_extra() -> None:
    """
    Test the case where we have Md043 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is the first heading
=================
<!-- pyml disable-next-line required-headings -->
This is a single heading
------------------------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022,Md025",
            "--set",
            "plugins.md043.headings=# This is the first heading",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_with_space_then_setext_extra() -> None:
    """
    Test the case where we have Md043 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is the first heading
=================
<!-- pyml disable-next-line required-headings -->

This is a single heading
------------------------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022,Md025",
            "--set",
            "plugins.md043.headings=# This is the first heading",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_no_pragma_then_atx_wildcard() -> None:
    """
    Test the case where we have Md043 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# This is a single heading
## Another heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022",
            "--set",
            "plugins.md043.headings=# A single heading,*",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD043: Required heading structure [Wildcard heading match failed.] (required-headings,required-headers)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_without_space_then_atx_wildcard() -> None:
    """
    Test the case where we have Md043 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line required-headings -->
# This is a single heading
## Another heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022,Md025",
            "--set",
            "plugins.md043.headings=# A single heading,*",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_with_space_then_atx_wildcard() -> None:
    """
    Test the case where we have Md043 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line required-headings -->

# This is a single heading
## Another heading
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022,Md025",
            "--set",
            "plugins.md043.headings=# A single heading,*",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_no_pragma_then_setext_wildcard() -> None:
    """
    Test the case where we have Md043 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is a single heading
===========
Another heading
-----------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022",
            "--set",
            "plugins.md043.headings=# A single heading,*",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: MD043: Required heading structure [Wildcard heading match failed.] (required-headings,required-headers)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_without_space_then_setext_wildcard() -> None:
    """
    Test the case where we have Md043 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line required-headings -->
This is a single heading
===========
Another heading
-----------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022,Md025",
            "--set",
            "plugins.md043.headings=# A single heading,*",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_with_space_then_setext_wildcard() -> None:
    """
    Test the case where we have Md043 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line required-headings -->

This is a single heading
===========
Another heading
-----------
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022,Md025",
            "--set",
            "plugins.md043.headings=# A single heading,*",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_no_pragma_then_atx_multiple_wildcard() -> None:
    """
    Test the case where we have Md043 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Heading 1

## Heading 2

## Heading 2

## Heading 2

### Heading 3
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022,Md024",
            "--set",
            "plugins.md043.headings=# Heading 1,*,### Heading 3,*,### Heading 3",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD043: Required heading structure [Multiple wildcard matching failed.] (required-headings,required-headers)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_without_space_then_atx_multiple_wildcard() -> (
    None
):
    """
    Test the case where we have Md043 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Heading 1

<!-- pyml disable-next-line required-headings -->
## Heading 2

## Heading 2

## Heading 2

### Heading 3
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022,Md024",
            "--set",
            "plugins.md043.headings=# Heading 1,*,### Heading 3,*,### Heading 3",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md043_pragma_with_space_then_atx_multiple_wildcard() -> (
    None
):
    """
    Test the case where we have Md043 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """# Heading 1

<!-- pyml disable-next-line required-headings -->

## Heading 2

## Heading 2

## Heading 2

### Heading 3
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md022,Md024",
            "--set",
            "plugins.md043.headings=# Heading 1,*,### Heading 3,*,### Heading 3",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_text_in_para_first_line() -> None:
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is a simple paragraph with text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:18: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_text_in_para_first_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->
This is a simple paragraph with text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_text_in_para_first_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->

This is a simple paragraph with text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_text_in_para_first_and_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is a line in a paragraph with text.
This is another line in a paragraph with text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:21: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{markdown_file_path}:2:27: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_text_in_para_first_and_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->
This is a line in a paragraph with text.
<!-- pyml disable-next-line proper-names -->
This is another line in a paragraph with text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_text_in_para_first_and_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->

This is a line in a paragraph with text.
<!-- pyml disable-next-line proper-names -->

This is another line in a paragraph with text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_link_in_first_line() -> None:
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is an [inline link in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:30: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_link_in_first_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->
This is an [inline link in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_link_in_first_line() -> None:
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->

This is an [inline link in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_link_in_first_and_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is an [inline link in a paragraph](http://www.google.com) in the text.
This is another [inline link in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:30: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{markdown_file_path}:2:35: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_link_in_first_and_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->
This is an [inline link in a paragraph](http://www.google.com) in the text.
<!-- pyml disable-next-line proper-names -->
This is another [inline link in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_link_in_first_and_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->

This is an [inline link in a paragraph](http://www.google.com) in the text.
<!-- pyml disable-next-line proper-names -->

This is another [inline link in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_image_in_first_line() -> None:
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is an ![inline image in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:32: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_image_in_first_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->
This is an ![inline image in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_image_in_first_line() -> None:
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->

This is an ![inline image in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_image_in_first_linexx() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->

This is an ![inline image in a paragraph](http://www.google.com) in the text.
<!-- pyml disable-next-line proper-names -->

This is another [inline link in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_image_in_first_and_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is an ![inline image in a paragraph](http://www.google.com) in the text.
This is another [inline link in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:32: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{markdown_file_path}:2:35: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_image_in_first_and_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->
This is an ![inline image in a paragraph](http://www.google.com) in the text.
<!-- pyml disable-next-line proper-names -->
This is another [inline link in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_image_in_first_and_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->

This is an ![inline image in a paragraph](http://www.google.com) in the text.
<!-- pyml disable-next-line proper-names -->

This is another [inline link in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_image_split_over_two_lines() -> None:
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is an ![inline image
in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:6: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_image_split_over_two_lines() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is an ![inline image
<!-- pyml disable-next-line proper-names -->
in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_image_split_over_two_lines() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is an ![inline image
<!-- pyml disable-next-line proper-names -->

in a paragraph](http://www.google.com) in the text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_lrd_in_first_line() -> None:
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """[lrd with a paragraph]: http://www.google.com
LRD.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:13: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_lrd_in_first_line() -> None:
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->
[lrd with a paragraph]: http://www.google.com
LRD.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_lrd_in_first_line() -> None:
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->

[lrd with a paragraph]: http://www.google.com
LRD.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_lrd_in_second_line() -> None:
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """[lrd with a
paragraph]: http://www.google.com
LRD.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_lrd_in_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """[lrd with a
<!-- pyml disable-next-line proper-names -->
paragraph]: http://www.google.com
LRD.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_lrd_in_second_line() -> None:
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """[lrd with a
<!-- pyml disable-next-line proper-names -->

paragraph]: http://www.google.com
LRD.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md034,md041",
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_lrd_in_first_line_and_in_first_line_title() -> (
    None
):
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """[lrd with a paragraph]: http://www.google.com "a paragraph"
LRD.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:13: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{markdown_file_path}:1:50: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_lrd_in_first_line_and_in_first_line_title() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->
[lrd with a paragraph]: http://www.google.com "a paragraph"
LRD.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_lrd_in_first_line_and_in_first_line_title() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->

[lrd with a paragraph]: http://www.google.com "a paragraph"
LRD.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md034,md041",
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_lrd_in_first_line_and_in_second_line_title() -> (
    None
):
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """[lrd with a paragraph]: http://www.google.com "a
paragraph"
LRD.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:13: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{markdown_file_path}:2:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_lrd_in_first_line_and_in_second_line_title() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->
[lrd with a paragraph]: http://www.google.com "a
<!-- pyml disable-next-line proper-names -->
paragraph"
LRD.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
@pytest.mark.skip(reason="https://github.com/jackdewinter/pymarkdown/issues/1516")
def test_pragmas_issue_1479_Md044_pragma_with_space_then_lrd_in_first_line_and_in_second_line_title() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.

    NOTE: This is failing because the LRD rewind logic needs fixing.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->

[lrd with a paragraph]: http://www.google.com "a
<!-- pyml disable-next-line proper-names -->

paragraph"
LRD.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md034,md041",
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_code_span_in_first_line() -> None:
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """My paragraph with `a paragraph in a` code span.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:4: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{markdown_file_path}:1:22: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_code_span_in_first_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->
My paragraph with `a paragraph in a` code span.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_code_span_in_first_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->

My paragraph with `a paragraph in a` code span.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md034,md041",
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_code_span_in_second_line() -> None:
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """My paragraph
with `a paragraph in a` code span.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:4: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)
{markdown_file_path}:2:9: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_code_span_in_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->
My paragraph
<!-- pyml disable-next-line proper-names -->
with `a paragraph in a` code span.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_code_span_in_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line proper-names -->

My paragraph
<!-- pyml disable-next-line proper-names -->

with `a paragraph in a` code span.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md034,md041",
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_no_pragma_then_multilinecode_span_in_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """My para with `a
paragraph in a` code span.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:1: MD044: Proper names should have the correct capitalization [Expected: ParaGraph; Actual: paragraph] (proper-names)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_without_space_then_multilinecode_span_in_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """My para with `a
<!-- pyml disable-next-line proper-names -->
paragraph in a` code span.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md044_pragma_with_space_then_multilinecode_span_in_second_line() -> (
    None
):
    """
    Test the case where we have Md044 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """My para with `a
<!-- pyml disable-next-line proper-names -->

paragraph in a` code span.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "-d",
            "Md034,md041",
            "--set",
            "plugins.md044.names=ParaGraph",
            "--strict-config",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md045_no_pragma_then_para_with_image_first_line() -> None:
    """
    Test the case where we have Md045 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Every image link like this ![ ](image.png) should have alternate text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--disable",
            "Md039,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:28: MD045: Images should have alternate text (alt text) (no-alt-text)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md045_pragma_without_space_then_para_with_image_first_line() -> (
    None
):
    """
    Test the case where we have Md045 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-alt-text -->
Every image link like this ![ ](image.png) should have alternate text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--disable",
            "Md039,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md045_pragma_with_space_then_para_with_image_first_line() -> (
    None
):
    """
    Test the case where we have Md045 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line no-alt-text -->

Every image link like this ![ ](image.png) should have alternate text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--disable",
            "Md039,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md045_no_pragma_then_para_with_image_second_line() -> None:
    """
    Test the case where we have Md045 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Every image link like
this ![ ](image.png) should have alternate text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--disable",
            "Md039,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:6: MD045: Images should have alternate text (alt text) (no-alt-text)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md045_pragma_without_space_then_para_with_image_second_line() -> (
    None
):
    """
    Test the case where we have Md045 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Every image link like
<!-- pyml disable-next-line no-alt-text -->
this ![ ](image.png) should have alternate text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--disable",
            "Md039,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md045_pragma_with_space_then_para_with_image_second_line() -> (
    None
):
    """
    Test the case where we have Md045 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """Every image link like
<!-- pyml disable-next-line no-alt-text -->

this ![ ](image.png) should have alternate text.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--disable",
            "Md039,Md041",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md046_no_pragma_then_fenced_and_indented_code_blocks() -> (
    None
):
    """
    Test the case where we have Md046 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```Markdown
# fred
```

    # barney
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:5:5: MD046: Code block style [Expected: fenced; Actual: indented] (code-block-style)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md046_pragma_without_space_then_fenced_and_indented_code_blocks() -> (
    None
):
    """
    Test the case where we have Md046 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```Markdown
# fred
```

<!-- pyml disable-next-line code-block-style -->
    # barney
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md046_pragma_with_space_then_fenced_and_indented_code_blocks() -> (
    None
):
    """
    Test the case where we have Md046 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```Markdown
# fred
```

<!-- pyml disable-next-line code-block-style -->

    # barney
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md046_no_pragma_then_indented_and_fenced_code_blocks() -> (
    None
):
    """
    Test the case where we have Md046 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """    # barney

```Markdown
# fred
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:3:1: MD046: Code block style [Expected: indented; Actual: fenced] (code-block-style)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md046_pragma_without_space_then_indented_and_fenced_code_blocks() -> (
    None
):
    """
    Test the case where we have Md046 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """    # barney

<!-- pyml disable-next-line code-block-style -->
```Markdown
# fred
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md046_pragma_with_space_then_indented_and_fenced_code_blocks() -> (
    None
):
    """
    Test the case where we have Md046 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """    # barney

<!-- pyml disable-next-line code-block-style -->

```Markdown
# fred
```
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md047_no_pragma_then_text_with_no_ending_line() -> None:
    """
    Test the case where we have Md047 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """this is the text"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:16: MD047: Each file should end with a single newline character. (single-trailing-newline)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md047_pragma_without_space_then_text_with_no_ending_line() -> (
    None
):
    """
    Test the case where we have Md047 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line single-trailing-newline -->
this is the text"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md047_pragma_with_space_then_text_with_no_ending_line() -> (
    None
):
    """
    Test the case where we have Md047 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line single-trailing-newline -->

this is the text"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md048_no_pragma_then_two_fenced_blocks() -> None:
    """
    Test the case where we have Md048 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```Python
def test():
    print("test")
```

~~~Python
def test():
    print("test")
~~~
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:6:1: MD048: Code fence style [Expected: backtick; Actual: tilde] (code-fence-style)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md048_pragma_without_space_then_two_fenced_blocks() -> None:
    """
    Test the case where we have Md048 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```Python
def test():
    print("test")
```

<!-- pyml disable-next-line code-fence-style -->
~~~Python
def test():
    print("test")
~~~
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Md048_pragma_with_space_then_two_fenced_blocks() -> None:
    """
    Test the case where we have Md048 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """```Python
def test():
    print("test")
```

<!-- pyml disable-next-line code-fence-style -->

~~~Python
def test():
    print("test")
~~~
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml100_no_pragma_then_html_block() -> None:
    """
    Test the case where we have Pml100 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<noframes>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml100",
            "--disable-rules",
            "Md033",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:1: PML100: Disallowed HTML [Tag Name: noframes] (disallowed-html)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml100_pragma_without_space_then_html_block() -> None:
    """
    Test the case where we have Pml100 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line disallowed-html -->
<noframes>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml100",
            "--disable-rules",
            "Md033",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml100_pragma_with_space_then_html_block() -> None:
    """
    Test the case where we have Pml100 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line disallowed-html -->

<noframes>
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml100",
            "--disable-rules",
            "Md033",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml100_no_pragma_then_inline_html_first_line() -> None:
    """
    Test the case where we have Pml100 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This html <noframes> is in a text block.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml100",
            "--disable-rules",
            "Md033",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:11: PML100: Disallowed HTML [Tag Name: noframes] (disallowed-html)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml100_pragma_without_space_then_inline_html_first_line() -> (
    None
):
    """
    Test the case where we have Pml100 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line disallowed-html -->
This html <noframes> is in a text block.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml100",
            "--disable-rules",
            "Md033",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml100_pragma_with_space_then_inline_html_first_line() -> (
    None
):
    """
    Test the case where we have Pml100 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line disallowed-html -->

This html <noframes> is in a text block.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml100",
            "--disable-rules",
            "Md033",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml100_no_pragma_then_inline_html_second_line() -> None:
    """
    Test the case where we have Pml100 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is the first line.
This html <noframes> is in a text block.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml100",
            "--disable-rules",
            "Md033",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:2:11: PML100: Disallowed HTML [Tag Name: noframes] (disallowed-html)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml100_pragma_without_space_then_inline_html_second_line() -> (
    None
):
    """
    Test the case where we have Pml100 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is the first line.
<!-- pyml disable-next-line disallowed-html -->
This html <noframes> is in a text block.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml100",
            "--disable-rules",
            "Md033",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml100_pragma_with_space_then_inline_html_second_line() -> (
    None
):
    """
    Test the case where we have Pml100 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """This is the first line.
<!-- pyml disable-next-line disallowed-html -->

This html <noframes> is in a text block.
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml100",
            "--disable-rules",
            "Md033",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml101_no_pragma_then_ul_li() -> None:
    """
    Test the case where we have Pml101 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """ * this is level 1
 * this is also level 1
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml101",
            "--disable-rules",
            "Md007",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)
{markdown_file_path}:2:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml101_pragma_without_space_then_ul_li() -> None:
    """
    Test the case where we have Pml101 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line list-anchored-indent -->
 * this is level 1
<!-- pyml disable-next-line list-anchored-indent -->
 * this is also level 1
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml101",
            "--disable-rules",
            "Md007",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml101_pragma_with_space_then_ul_li() -> None:
    """
    Test the case where we have Pml101 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line list-anchored-indent -->

 * this is level 1
<!-- pyml disable-next-line list-anchored-indent -->

 * this is also level 1
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml101",
            "--disable-rules",
            "Md007",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml101_no_pragma_then_ol_li() -> None:
    """
    Test the case where we have Pml101 violations and no pragmas, and we expect the rule to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """ 1. this is level 1
 1. this is also level 1
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml101",
            "--disable-rules",
            "Md007",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 1
        expected_output = f"""{markdown_file_path}:1:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)
{markdown_file_path}:2:2: PML101: Anchored list indentation [Expected: 0, Actual=1] (list-anchored-indent)"""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml101_pragma_without_space_then_ol_li() -> None:
    """
    Test the case where we have Pml101 violations and a disable-next-line pragma on the line before each one,
    and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line list-anchored-indent -->
 1. this is level 1
<!-- pyml disable-next-line list-anchored-indent -->
 1. this is also level 1
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml101",
            "--disable-rules",
            "Md007",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_pragmas_issue_1479_Pml101_pragma_with_space_then_ol_li() -> None:
    """
    Test the case where we have Pml101 violations and a disable-next-line pragma two lines before each one a single blank line between them, and we expect the rule not to fire.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_markdown = """<!-- pyml disable-next-line list-anchored-indent -->

 1. this is level 1
<!-- pyml disable-next-line list-anchored-indent -->

 1. this is also level 1
"""
    with create_temporary_configuration_file(
        supplied_configuration=source_markdown, file_name_suffix=".md"
    ) as markdown_file_path:
        supplied_arguments = [
            "--enable-rules",
            "Pml101",
            "--disable-rules",
            "Md007",
            "scan",
            markdown_file_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
