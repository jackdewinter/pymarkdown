"""
Module to provide tests related to the MD024 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import write_temporary_configuration

import pytest


@pytest.mark.rules
def test_md024_good_different_heading_content_atx():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with no duplicate content.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md024/different_heading_content_atx.md",
    ]

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
def test_md024_bad_same_heading_content_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md024/same_heading_content_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_content_atx.md:3:1: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_content_atx_with_extra_whitespace():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with content that is almost duplicate except for
    whitespace.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md024/same_heading_content_atx_with_extra_whitespace.md",
    ]

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
def test_md024_bad_same_heading_content_atx_with_extra_emphasis():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with content that is almost duplicate except for emphasis.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md024/same_heading_content_atx_with_extra_emphasis.md",
    ]

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
def test_md024_bad_same_heading_content_atx_in_same_list_item():
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content within the same list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md024/same_heading_content_atx_in_same_list_item.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_content_atx_in_same_list_item.md:3:3: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_content_atx_in_different_list_items():
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in different list items.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md024/same_heading_content_atx_in_different_list_items.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_content_atx_in_different_list_items.md:3:3: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_content_atx_in_same_block_quote():
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in the same block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md024/same_heading_content_atx_in_same_block_quote.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_content_atx_in_same_block_quote.md:3:3: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_content_atx_in_different_block_quotes():
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in the different block quotes.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md028",
        "scan",
        "test/resources/rules/md024/same_heading_content_atx_in_different_block_quotes.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_content_atx_in_different_block_quotes.md:3:3: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_in_siblings_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in sibling headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md024/same_heading_in_siblings_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_in_siblings_atx.md:7:1: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
        + "test/resources/rules/md024/same_heading_in_siblings_atx.md:11:1: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_but_not_in_siblings_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in non-siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md024/same_heading_but_not_in_siblings_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_but_not_in_siblings_atx.md:9:1: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_good_different_heading_content_atx_with_configuration():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with different content.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md024/different_heading_content_atx.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_good_same_heading_content_atx_with_configuration():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with duplicate content in non-siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md024/same_heading_content_atx.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_bad_same_heading_in_siblings_atx_with_configuration():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with duplicate content in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md024/same_heading_in_siblings_atx.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md024/same_heading_in_siblings_atx.md:7:1: "
            + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_good_same_heading_but_not_in_siblings_atx_with_configuration():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with duplicate content in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md024/same_heading_but_not_in_siblings_atx.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_good_same_heading_but_not_in_siblings_atx_with_alternate_configuration():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with duplicate content in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md024": {"allow_different_nesting": True}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md024/same_heading_but_not_in_siblings_atx.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_good_different_inline_heading_content_atx():
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with almost duplicate content.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md024/different_inline_heading_content_atx.md",
    ]

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
def test_md024_good_different_heading_content_setext():
    """
    Test to make sure this rule does not trigger with a document that
    contains SetExt headings with no duplicate content.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md024/different_heading_content_setext.md",
    ]

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
def test_md024_bad_same_heading_content_setext():
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "scan",
        "test/resources/rules/md024/same_heading_content_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_content_setext.md:4:1: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_in_siblings_setext():
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md025",
        "scan",
        "test/resources/rules/md024/same_heading_in_siblings_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_in_siblings_setext.md:7:1: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
        + "test/resources/rules/md024/same_heading_in_siblings_setext.md:13:1: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_but_not_in_siblings_setext():
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "--disable-rules",
        "md025",
        "scan",
        "test/resources/rules/md024/same_heading_but_not_in_siblings_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_but_not_in_siblings_setext.md:10:1: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_good_different_heading_content_setext_with_configuration():
    """
    Test to make sure this rule does not trigger with a document that
    contains SetExt headings with duplicate content in siblings with configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md024/different_heading_content_setext.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_good_same_heading_content_setext_with_configuration():
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content in siblings with configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md024/same_heading_content_setext.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_bad_same_heading_in_siblings_setext_with_configuration():
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content in siblings with configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "--disable-rules",
            "md025",
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md024/same_heading_in_siblings_setext.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md024/same_heading_in_siblings_setext.md:7:1: "
            + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_good_same_heading_but_not_in_siblings_setext_with_configuration():
    """
    Test to make sure this rule does not trigger with a document that
    contains SetExt headings with duplicate content in siblings with configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "--disable-rules",
            "md025",
            "-c",
            configuration_file,
            "scan",
            "test/resources/rules/md024/same_heading_but_not_in_siblings_setext.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)
