"""
Module to provide tests related to the MD024 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from test.utils import create_temporary_configuration_file

import pytest


@pytest.mark.rules
def test_md024_good_different_heading_content_atx() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with no duplicate content.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "different_heading_content_atx.md"
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
def test_md024_bad_same_heading_content_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "same_heading_content_atx.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:3:1: "
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
def test_md024_bad_same_heading_content_atx_with_extra_whitespace() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with content that is almost duplicate except for
    whitespace.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md024",
        "same_heading_content_atx_with_extra_whitespace.md",
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
def test_md024_bad_same_heading_content_atx_with_extra_emphasis() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with content that is almost duplicate except for emphasis.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md024",
        "same_heading_content_atx_with_extra_emphasis.md",
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
def test_md024_bad_same_heading_content_atx_in_same_list_item() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content within the same list item.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md024",
        "same_heading_content_atx_in_same_list_item.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:3:3: "
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
def test_md024_bad_same_heading_content_atx_in_different_list_items() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in different list items.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md024",
        "same_heading_content_atx_in_different_list_items.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:3:3: "
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
def test_md024_bad_same_heading_content_atx_in_same_block_quote() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in the same block quote.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md024",
        "same_heading_content_atx_in_same_block_quote.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:3:3: "
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
def test_md024_bad_same_heading_content_atx_in_different_block_quotes() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in the different block quotes.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md024",
        "same_heading_content_atx_in_different_block_quotes.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md028",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:3:3: "
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
def test_md024_bad_same_heading_in_siblings_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in sibling headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "same_heading_in_siblings_atx.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:7:1: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
        + f"{os.path.abspath(source_path)}:11:1: "
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
def test_md024_bad_same_heading_but_not_in_siblings_atx() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in non-siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "same_heading_but_not_in_siblings_atx.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:9:1: "
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
def test_md024_good_different_heading_content_atx_with_configuration() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with different content.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "different_heading_content_atx.md"
    )
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
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
def test_md024_good_same_heading_content_atx_with_configuration() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with duplicate content in non-siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "same_heading_content_atx.md"
    )
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
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
def test_md024_bad_same_heading_in_siblings_atx_with_configuration() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with duplicate content in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "same_heading_in_siblings_atx.md"
    )
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"{os.path.abspath(source_path)}:7:1: "
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
def test_md024_good_same_heading_but_not_in_siblings_atx_with_configuration() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with duplicate content in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "same_heading_but_not_in_siblings_atx.md"
    )
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
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
def test_md024_good_same_heading_but_not_in_siblings_atx_with_alternate_configuration() -> (
    None
):
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with duplicate content in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "same_heading_but_not_in_siblings_atx.md"
    )
    supplied_configuration = {"plugins": {"md024": {"allow_different_nesting": True}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
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
def test_md024_good_different_inline_heading_content_atx() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with almost duplicate content.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "different_inline_heading_content_atx.md"
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
def test_md024_good_different_heading_content_setext() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains SetExt headings with no duplicate content.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "different_heading_content_setext.md"
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
def test_md024_bad_same_heading_content_setext() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "same_heading_content_setext.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:4:1: "
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
def test_md024_bad_same_heading_content_atx_then_setext() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading and then a SetExt heading, with duplicate content.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "same_heading_content_atx_then_setext.md"
    )
    supplied_arguments = [
        "-d",
        "md003",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:3:1: "
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
def test_md024_bad_same_heading_in_siblings_setext() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "same_heading_in_siblings_setext.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md025",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:7:1: "
        + "MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n"
        + f"{os.path.abspath(source_path)}:13:1: "
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
def test_md024_bad_same_heading_but_not_in_siblings_setext() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md024",
        "same_heading_but_not_in_siblings_setext.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md025",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{os.path.abspath(source_path)}:10:1: "
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
def test_md024_good_different_heading_content_setext_with_configuration() -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains SetExt headings with duplicate content in siblings with configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "different_heading_content_setext.md"
    )
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
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
def test_md024_good_same_heading_content_setext_with_configuration() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content in siblings with configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "same_heading_content_setext.md"
    )
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
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
def test_md024_bad_same_heading_in_siblings_setext_with_configuration() -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content in siblings with configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md024", "same_heading_in_siblings_setext.md"
    )
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "--disable-rules",
            "md025",
            "-c",
            configuration_file,
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = (
            f"{os.path.abspath(source_path)}:7:1: "
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
def test_md024_good_same_heading_but_not_in_siblings_setext_with_configuration() -> (
    None
):
    """
    Test to make sure this rule does not trigger with a document that
    contains SetExt headings with duplicate content in siblings with configuration.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md024",
        "same_heading_but_not_in_siblings_setext.md",
    )
    supplied_configuration = {"plugins": {"md024": {"siblings_only": True}}}
    with create_temporary_configuration_file(
        supplied_configuration
    ) as configuration_file:
        supplied_arguments = [
            "--disable-rules",
            "md025",
            "-c",
            configuration_file,
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


def test_md024_query_config() -> None:
    config_test = pluginQueryConfigTest(
        "md024",
        """
  ITEM               DESCRIPTION

  Id                 md024
  Name(s)            no-duplicate-heading,no-duplicate-header
  Short Description  Multiple headings cannot contain the same content.
  Description Url    https://pymarkdown.readthedocs.io/en/latest/plugins/rule_
                     md024.md


  CONFIGURATION ITEM       TYPE     VALUE

  siblings_only            boolean  False
  allow_different_nesting  boolean  False

""",
    )
    execute_query_configuration_test(config_test)
