"""
Module to provide tests related to the MD027 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import assert_file_is_as_expected, copy_to_temp_file

import pytest

source_path = os.path.join("test", "resources", "rules", "md027") + os.sep


@pytest.mark.rules
def test_md027_bad_block_quote_atx_heading_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and an Atx Heading, which has
    an extra space before it.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_atx_heading_plus_one.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md022,md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_atx_heading_plus_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_atx_heading_plus_one.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >  # New Heading
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md022,md023",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ > this is text
 > # New Heading
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_atx_heading_misaligned():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and an Atx Heading, which has
    is aligned to the text, not the block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_atx_heading_misaligned.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md022,md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_atx_heading_misaligned_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_atx_heading_misaligned.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
>  # New Heading
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md022,md023",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ > this is text
> # New Heading
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_fenced_first_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and a Fenced code block with
    an extra space before the start.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_fenced_first_plus_one.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md031",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:2:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_fenced_first_plus_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_fenced_first_plus_one.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >  ```code
 > this is a fenced block
 > ```
 > a real test
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md031",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ > this is text
 > ```code
 > this is a fenced block
 > ```
 > a real test
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_fenced_last_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and a Fenced code block with
    an extra space before the end.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_fenced_last_plus_one.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md031",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_fenced_last_plus_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_fenced_last_plus_one.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 > ```code
 > this is a fenced block
 >   ```
 > a real test
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md031",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ > this is text
 > ```code
 > this is a fenced block
 > ```
 > a real test
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_fenced_last_misaligned():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and a Fenced code block with
    an extra space before the end, in misalligned block quotes.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_fenced_last_misaligned.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md031",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_fenced_last_misaligned_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_fenced_last_misaligned.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 > ```code
 > this is a fenced block
>   ```
> a real test
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md031",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ > this is text
 > ```code
 > this is a fenced block
> ```
> a real test
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_lrd_multiple_one_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and a LRD that has extr soace
    before line 1.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_lrd_multiple_one_plus_one.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_lrd_multiple_one_plus_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_lrd_multiple_one_plus_one.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 >  [lab
 > el]:
 > /url
 > "tit
 > le"
 >
 > a real test
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

        expected_file_contents = """ > this is text
 >
 > [lab
 > el]:
 > /url
 > "tit
 > le"
 >
 > a real test
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_lrd_multiple_three_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and a LRD that has extr soace
    before line 3.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_lrd_multiple_three_plus_one.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_lrd_multiple_three_plus_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_lrd_multiple_three_plus_one.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 > [lab
 > el]:
 >  /url
 > "tit
 > le"
 >
 > a real test
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

        expected_file_contents = """ > this is text
 >
 > [lab
 > el]:
 > /url
 > "tit
 > le"
 >
 > a real test
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_lrd_multiple_three_misaligned():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and a LRD that has extr soace
    before line 3, misaligned.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_lrd_multiple_three_misaligned.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_lrd_multiple_three_misaligned_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_lrd_multiple_three_misaligned.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 > [lab
 > el]:
>  /url
> "tit
> le"
>
> a real test
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

        expected_file_contents = """ > this is text
 >
 > [lab
 > el]:
> /url
> "tit
> le"
>
> a real test
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_lrd_multiple_four_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and a LRD that has extr soace
    before line 4.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_lrd_multiple_four_plus_one.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:6:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_lrd_multiple_four_plus_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_lrd_multiple_four_plus_one.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 > [lab
 > el]:
 > /url
 >  "tit
 > le"
 >
 > a real test
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

        expected_file_contents = """ > this is text
 >
 > [lab
 > el]:
 > /url
 > "tit
 > le"
 >
 > a real test
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_lrd_multiple_four_misaligned():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and a LRD that has extr soace
    before line 4, misaligned.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_lrd_multiple_four_misaligned.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:6:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_lrd_multiple_four_misaligned_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_lrd_multiple_four_misaligned.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 > [lab
 > el]:
 > /url
>  "tit
> le"
>
> a real test
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

        expected_file_contents = """ > this is text
 >
 > [lab
 > el]:
 > /url
> "tit
> le"
>
> a real test
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_thematic_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with text and a thematic break with extra.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md027", "bad_block_quote_thematic_plus_one.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_thematic_plus_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_thematic_plus_one.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 >  ------
 >
 > a real test
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

        expected_file_contents = """ > this is text
 >
 > ------
 >
 > a real test
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_first_line_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with SetExt with extra space in first line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_setext_heading_first_line_plus_one.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_first_line_plus_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_setext_heading_first_line_plus_one.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 >  a setext heading
 > ---
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md023",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ > this is text
 >
 > a setext heading
 > ---
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_multiples_first_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with SetExt with extra space in first line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_setext_heading_multiples_first_plus_one.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:3:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_multiples_first_plus_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_setext_heading_multiples_first_plus_one.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 >  a setext heading
 > that is not properly
 > indented
 > ---
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md023",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ > this is text
 >
 > a setext heading
 > that is not properly
 > indented
 > ---
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_multiples_middle_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with SetExt with extra space in middle line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_setext_heading_multiples_middle_plus_one.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_multiples_middle_plus_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_setext_heading_multiples_middle_plus_one.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 > a setext heading
 >  that is not properly
 > indented
 > ---
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md023",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ > this is text
 >
 > a setext heading
 > that is not properly
 > indented
 > ---
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_multiples_middle_misaligned():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with SetExt with extra space in middle line,
    with misaligned block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_setext_heading_multiples_middle_misaligned.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_multiples_middle_misaligned_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_setext_heading_multiples_middle_misaligned.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 > a setext heading
>  that is not properly
> indented
> ---
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md023",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ > this is text
 >
 > a setext heading
> that is not properly
> indented
> ---
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_multiples_last_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with SetExt with extra space in last line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_setext_heading_multiples_last_plus_one.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_multiples_last_plus_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_setext_heading_multiples_last_plus_one.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 > a setext heading
 > that is not properly
 >  indented
 > ---
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md023",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ > this is text
 >
 > a setext heading
 > that is not properly
 > indented
 > ---
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_multiples_last_misaligned():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with SetExt with extra space in last line, misaligned.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_setext_heading_multiples_last_misaligned.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_multiples_last_misaligned_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_setext_heading_multiples_last_misaligned.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 > a setext heading
 > that is not properly
>  indented
> ---
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md023",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ > this is text
 >
 > a setext heading
 > that is not properly
> indented
> ---
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_second_line_plus_one():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with SetExt with extra space in second line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_setext_heading_second_line_plus_one.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:4: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_second_line_plus_one_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_setext_heading_second_line_plus_one.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 > a setext heading
 >  ---
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md023",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ > this is text
 >
 > a setext heading
 > ---
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_second_line_misaligned():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with SetExt with extra space in second line, misaligned.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md027",
        "bad_block_quote_setext_heading_second_line_misaligned.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md023",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:4:3: "
        + "MD027: Multiple spaces after blockquote symbol (no-multiple-space-blockquote)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md027_bad_block_quote_setext_heading_second_line_misaligned_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains a block quote with more than 1 space after it.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_block_quote_setext_heading_second_line_misaligned.md"
    ) as temp_source_path:
        original_file_contents = """ > this is text
 >
 > a setext heading
>  ---
"""
        assert_file_is_as_expected(temp_source_path, original_file_contents)

        supplied_arguments = [
            "--disable-rules",
            "md023",
            "-x-fix",
            "scan",
            temp_source_path,
        ]

        expected_return_code = 3
        expected_output = f"Fixed: {temp_source_path}"
        expected_error = ""

        expected_file_contents = """ > this is text
 >
 > a setext heading
> ---
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)
