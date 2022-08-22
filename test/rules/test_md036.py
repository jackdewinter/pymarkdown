"""
Module to provide tests related to the MD036 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import write_temporary_configuration

import pytest


@pytest.mark.rules
def test_md036_bad_configuration_punctuation():
    """
    Test to verify that a configuration error is thrown when supplying the
    punctuation value with an integer that is not a string.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md036", "proper_headings_atx.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md036.punctuation=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md036.punctuation' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_good_proper_headings_atx():
    """
    Test to make sure this rule does trigger with a document that
    contains valid Atx Headings and not emphasis.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md036", "proper_headings_atx.md"
    )
    supplied_arguments = [
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
def test_md036_good_proper_headings_setext():
    """
    Test to make sure this rule does not trigger with a document that
    contains valid SetExt Headings and not emphasis.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md036", "proper_headings_setext.md"
    )
    supplied_arguments = [
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
def test_md036_good_proper_emphasis_with_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains an emphasis "heading" containing a link.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md036", "proper_emphasis_with_link.md"
    )
    supplied_arguments = [
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
def test_md036_good_proper_emphasis_with_text_then_link():
    """
    Test to make sure this rule does not trigger with a document that
    contains an emphasis "heading" containing text and then a link.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md036", "proper_emphasis_with_text_then_link.md"
    )
    supplied_arguments = [
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
def test_md036_good_proper_emphasis_with_text_then_link_then_text():
    """
    Test to make sure this rule does not trigger with a document that
    contains an emphasis "heading" containing text and then a link and then text.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md036",
        "proper_emphasis_with_text_then_link_then_text.md",
    )
    supplied_arguments = [
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
def test_md036_good_proper_emphasis_with_text_end_emphasis_more_text():
    """
    Test to make sure this rule does not trigger with a document that
    contains an emphasis "heading" containing text in the emphasis and
    more text after.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md036",
        "proper_emphasis_with_text_end_emphasis_more_text.md",
    )
    supplied_arguments = [
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
def test_md036_good_proper_emphasis_within_text():
    """
    Test to make sure this rule does not trigger with a document that
    contains a line containing text and emphasis within the line.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md036", "proper_emphasis_within_text.md"
    )
    supplied_arguments = [
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
def test_md036_good_proper_emphasis_within_multiline_text():
    """
    Test to make sure this rule does not trigger with a document that
    contains an emphasis "heading", with the emphasis going over 2 lines.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md036",
        "proper_emphasis_within_multiline_text.md",
    )
    supplied_arguments = [
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
def test_md036_good_proper_emphasis_ending_with_punctuation():
    """
    Test to make sure this rule does not trigger with a document that
    contains an emphasis "heading" where the text ends with punctuation.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md036",
        "proper_emphasis_ending_with_punctuation.md",
    )
    supplied_arguments = [
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
def test_md036_bad_proper_emphasis_ending_with_punctuation_with_configuration():
    """
    Test to make sure this rule does trigger with a document that
    contains an emphasis "heading" ending with punctuation, but not punctuation
    according to configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md036",
        "proper_emphasis_ending_with_punctuation.md",
    )
    supplied_configuration = {"plugins": {"md036": {"punctuation": ".!"}}}
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"{source_path}:1:1: "
            + "MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)\n"
            + f"{source_path}:5:1: "
            + "MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)\n"
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
def test_md036_bad_valid_emphasis_headings():
    """
    Test to make sure this rule does trigger with a document that
    contains a valid emphasis "heading".
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md036", "valid_emphasis_headings.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)\n"
        + f"{source_path}:5:1: "
        + "MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_bad_valid_emphasis_headings_in_list():
    """
    Test to make sure this rule does trigger with a document that
    contains a valid emphasis "heading" in a list.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md036", "valid_emphasis_headings_in_list.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:3: "
        + "MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)\n"
        + f"{source_path}:5:3: "
        + "MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md036_bad_valid_emphasis_headings_in_block_quote():
    """
    Test to make sure this rule does trigger with a document that
    contains a valid emphasis "heading" in a block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md036",
        "valid_emphasis_headings_in_block_quote.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:3: "
        + "MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)\n"
        + f"{source_path}:5:3: "
        + "MD036: Emphasis possibly used instead of a heading element. (no-emphasis-as-heading,no-emphasis-as-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
