"""
Module to provide tests related to the MD023 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import (
    assert_file_is_as_expected,
    copy_to_temp_file,
    create_temporary_configuration_file,
)

import pytest

source_path = os.path.join("test", "resources", "rules", "md023") + os.sep


@pytest.mark.rules
def test_md023_good_proper_indent_atx():
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx heading that starts at the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "proper_indent_atx.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_good_proper_indent_setext():
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that starts at the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "proper_indent_setext.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indent_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading that does not start at the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "improper_indent_atx.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:3: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indent_atx_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading that does not start at the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(source_path + "improper_indent_atx.md") as temp_source_path:
        original_file_contents = """Some text

  ## Heading 2

Some more text
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """Some text

## Heading 2

Some more text
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md023_good_proper_indent_atx_in_list_item():
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx heading that does start at the very left within a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "proper_indent_atx_in_list_item.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indent_atx_in_list_item():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading that does not start at the very left in a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "improper_indent_atx_in_list_item.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "MD022,md030",
        "--enable-rules",
        "MD023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:6: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indent_atx_in_list_item_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading that does not start at the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "improper_indent_atx_in_list_item.md"
    ) as temp_source_path:
        original_file_contents = """1. Some text

1.  ## Heading 2
     ## Heading 2.1

1. Some more text
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """1. Some text

1.  ## Heading 2
    ## Heading 2.1

1. Some more text
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md023_good_proper_indent_atx_in_block_quote():
    """
    Test to make sure this rule does not trigger with a document that
    contains an Atx heading that does start at the very left within a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "proper_indent_atx_in_block_quote.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indent_atx_in_block_quote():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading that does not start at the very left in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "improper_indent_atx_in_block_quote.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "MD027",
        "--enable-rules",
        "MD023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:4: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indent_atx_in_block_quote_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading that does not start at the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "improper_indent_atx_in_block_quote.md"
    ) as temp_source_path:
        original_file_contents = """> Some text
>
>  ## Heading 2
>
> Some more text
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "MD027",
            "--enable-rules",
            "MD023",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """> Some text
>
> ## Heading 2
>
> Some more text
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md023_bad_improper_indent_setext_x():
    """
    Test to make sure this rule does trigger with a document that
    contains a SetExt heading that any part of it does not start at
    the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "improper_indent_setext.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + f"{source_path}:9:3: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + f"{source_path}:14:1: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + f"{source_path}:22:1: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indent_setext_x_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading that does not start at the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "improper_indent_setext.md"
    ) as temp_source_path:
        original_file_contents = """Some text

  Heading 2
  ---------

Some more text

Another Heading 2
  -----------------

more text

  Yet Another Heading 2
-----------------

more text

A Very
  Very
Very
  Long Heading
-----------------
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """Some text

Heading 2
---------

Some more text

Another Heading 2
-----------------

more text

Yet Another Heading 2
-----------------

more text

A Very
Very
Very
Long Heading
-----------------
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md023_bad_improper_indent_setext_in_block_quote():
    """
    Test to make sure this rule does trigger with a document that
    contains a SetExt heading that any part of it does not start at
    the very left in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md023",
        "improper_indent_setext_in_block_quote.md",
    )
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "--disable-rules",
        "MD027,md022,md009",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:5: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + f"{source_path}:9:5: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + f"{source_path}:14:3: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + f"{source_path}:22:3: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indent_setext_in_block_quote_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading that does not start at the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "improper_indent_setext_in_block_quote.md"
    ) as temp_source_path:
        original_file_contents = """> Some text
>
>   Heading 2
>   ---------
>
> Some more text
>
> Another Heading 2
>   -----------------
>
> more text
>
>  Yet Another Heading 2
> -----------------
>
> more text
>
>   A Very 
>   Very1 
> Very2 
>   Long Heading
> -----------------
>
> Normal Heading
> ---------
>
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "-d",
            "md009,md027",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """> Some text
>
> Heading 2
> ---------
>
> Some more text
>
> Another Heading 2
> -----------------
>
> more text
>
> Yet Another Heading 2
> -----------------
>
> more text
>
> A Very 
> Very1 
> Very2 
> Long Heading
> -----------------
>
> Normal Heading
> ---------
>
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md023_good_proper_indent_setext_in_block_quote_no_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading that does not start at the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    original_file_contents = """> A Very\a
> Long Heading
> -----------------
""".replace(
        "\a", " "
    )
    with create_temporary_configuration_file(
        original_file_contents, file_name_suffix=".md"
    ) as temp_source_path:
        supplied_arguments = [
            "--stack-trace",
            "-d",
            "md009",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )


@pytest.mark.rules
def test_md023_bad_improper_indent_setext_in_list_item():
    """
    Test to make sure this rule does trigger with a document that
    contains a SetExt heading that any part of it does not start at
    the very left in a list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "improper_indent_setext_in_list_item.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "--disable-rules",
        "MD005,md030,md032",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:9:6: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
        + f"{source_path}:22:3: "
        + "MD023: Headings must start at the beginning of the line. (heading-start-left, header-start-left)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_bad_improper_indent_setext_in_list_item_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading that does not start at the very left.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "improper_indent_setext_in_list_item.md"
    ) as temp_source_path:
        original_file_contents = """- Some text

-   Heading 2 - md030 warns of too many spaces, md023 does not trigger
    ---------

- Some more text

- Another Heading 2 - md023 triggers
     -----------------

- more text

-  Yet Another Heading 2 - md030 warns of too many spaces, md023 does not trigger
  -----------------

- more text

- A Very1
   Very2
  Very3
   Long Heading  - md023 does trigger due to second and fourth lines
  -----------------

- Normal Heading
  ---------
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            # "--log-level",
            # "DEBUG",
            # "-x-fix-no-rescan-log",
            "-d",
            "md009,md005",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """- Some text

-   Heading 2 - md030 warns of too many spaces, md023 does not trigger
    ---------

- Some more text

- Another Heading 2 - md023 triggers
  -----------------

- more text

-  Yet Another Heading 2 - md030 warns of too many spaces, md023 does not trigger
  -----------------

- more text

- A Very1
  Very2
  Very3
  Long Heading  - md023 does trigger due to second and fourth lines
  -----------------

- Normal Heading
  ---------
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md023_good_proper_indented_atx_after_emphasis():
    """
    Test to make sure this rule does not trigger with a document that
    contains a "SetExt heading" that is encapsulated in emphasis.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "improper_indented_atx_after_emphasis.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_proper_indent_setext_trailing_x():
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that ends with spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "proper_indent_setext_trailing.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "MD009",
        "--enable-rules",
        "MD023",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_proper_indent_setext_trailing_first():
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that ends with spaces on the first line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "proper_indent_setext_trailing_first.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "--disable-rules",
        "MD009",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_proper_indent_setext_trailing_second():
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that ends with spaces on the second line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "proper_indent_setext_trailing_second.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "--disable-rules",
        "MD009",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_proper_indent_setext_trailing_third():
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that ends with spaces on the third line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md023", "proper_indent_setext_trailing_third.md"
    )
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "--disable-rules",
        "MD009",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md023_proper_indent_setext_larger_trailing_middle():
    """
    Test to make sure this rule does not trigger with a document that
    contains a SetExt heading that ends with spaces in the middle.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md023",
        "proper_indent_setext_larger_trailing_middle.md",
    )
    supplied_arguments = [
        "--enable-rules",
        "MD023",
        "--disable-rules",
        "MD009",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
