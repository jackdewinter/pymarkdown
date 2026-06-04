"""
Module to provide tests related to the MD024 rule.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.rules.utils import execute_query_configuration_test, pluginQueryConfigTest
from test.utils import create_temporary_configuration_file
from typing import Tuple

import pytest


def __generate_source_path(source_file_name: str) -> Tuple[str, str]:
    source_path = os.path.join("test", "resources", "rules", "md024", source_file_name)
    return source_path, os.path.abspath(source_path)


@pytest.mark.rules
def test_md024_good_different_heading_content_atx(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with no duplicate content.
    """

    # Arrange
    source_path, _ = __generate_source_path("different_heading_content_atx.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_content_atx(scanner_default: MarkdownScanner) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path("same_heading_content_atx.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:1: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_content_atx_with_extra_whitespace(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with content that is almost duplicate except for
    whitespace.
    """

    # Arrange
    source_path, _ = __generate_source_path(
        "same_heading_content_atx_with_extra_whitespace.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_content_atx_with_extra_emphasis(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with content that is almost duplicate except for emphasis.
    """

    # Arrange
    source_path, _ = __generate_source_path(
        "same_heading_content_atx_with_extra_emphasis.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_content_atx_in_same_list_item(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content within the same list item.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "same_heading_content_atx_in_same_list_item.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:3: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_content_atx_in_different_list_items(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in different list items.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "same_heading_content_atx_in_different_list_items.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:3: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_content_atx_in_same_block_quote(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in the same block quote.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "same_heading_content_atx_in_same_block_quote.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:3: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_content_atx_in_different_block_quotes(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in the different block quotes.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "same_heading_content_atx_in_different_block_quotes.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md028",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:3: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_in_siblings_atx(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in sibling headings.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "same_heading_in_siblings_atx.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:7:1: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)
{abs_source_path}:11:1: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_but_not_in_siblings_atx(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains Atx headings with duplicate content in non-siblings.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "same_heading_but_not_in_siblings_atx.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:9:1: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_good_different_heading_content_atx_with_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with different content.
    """

    # Arrange
    source_path, _ = __generate_source_path("different_heading_content_atx.md")
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

        expected_results = ExpectedResults()

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_good_same_heading_content_atx_with_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with duplicate content in non-siblings.
    """

    # Arrange
    source_path, _ = __generate_source_path("same_heading_content_atx.md")
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

        expected_results = ExpectedResults()

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_in_siblings_atx_with_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with duplicate content in siblings.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "same_heading_in_siblings_atx.md"
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

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{abs_source_path}:7:1: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_good_same_heading_but_not_in_siblings_atx_with_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with duplicate content in siblings.
    """

    # Arrange
    source_path, _ = __generate_source_path("same_heading_but_not_in_siblings_atx.md")
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

        expected_results = ExpectedResults()

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_good_same_heading_but_not_in_siblings_atx_with_alternate_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with duplicate content in siblings.
    """

    # Arrange
    source_path, _ = __generate_source_path("same_heading_but_not_in_siblings_atx.md")
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

        expected_results = ExpectedResults()

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_good_different_inline_heading_content_atx(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains Atx headings with almost duplicate content.
    """

    # Arrange
    source_path, _ = __generate_source_path("different_inline_heading_content_atx.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_good_different_heading_content_setext(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains SetExt headings with no duplicate content.
    """

    # Arrange
    source_path, _ = __generate_source_path("different_heading_content_setext.md")
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults()

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_content_setext(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "same_heading_content_setext.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:4:1: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_content_atx_then_setext(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains an Atx heading and then a SetExt heading, with duplicate content.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "same_heading_content_atx_then_setext.md"
    )
    supplied_arguments = [
        "-d",
        "md003",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:3:1: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_in_siblings_setext(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content in siblings.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "same_heading_in_siblings_setext.md"
    )
    supplied_arguments = [
        "--disable-rules",
        "md025",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:7:1: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)
{abs_source_path}:13:1: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_but_not_in_siblings_setext(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content in siblings.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "same_heading_but_not_in_siblings_setext.md",
    )
    supplied_arguments = [
        "--disable-rules",
        "md025",
        "scan",
        source_path,
    ]

    expected_results = ExpectedResults(
        return_code=1,
        expected_output=f"""{abs_source_path}:10:1: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)""",
    )

    # Act
    execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_good_different_heading_content_setext_with_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains SetExt headings with duplicate content in siblings with configuration.
    """

    # Arrange
    source_path, _ = __generate_source_path("different_heading_content_setext.md")
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

        expected_results = ExpectedResults()

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_good_same_heading_content_setext_with_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content in siblings with configuration.
    """

    # Arrange
    source_path, _ = __generate_source_path("same_heading_content_setext.md")
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

        expected_results = ExpectedResults()

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_bad_same_heading_in_siblings_setext_with_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does trigger with a document that
    contains SetExt headings with duplicate content in siblings with configuration.
    """

    # Arrange
    source_path, abs_source_path = __generate_source_path(
        "same_heading_in_siblings_setext.md"
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

        expected_results = ExpectedResults(
            return_code=1,
            expected_output=f"""{abs_source_path}:7:1: MD024: Multiple headings cannot contain the same content. (no-duplicate-heading,no-duplicate-header)\n""",
        )

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
def test_md024_good_same_heading_but_not_in_siblings_setext_with_configuration(
    scanner_default: MarkdownScanner,
) -> None:
    """
    Test to make sure this rule does not trigger with a document that
    contains SetExt headings with duplicate content in siblings with configuration.
    """

    # Arrange
    source_path, _ = __generate_source_path(
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

        expected_results = ExpectedResults()

        # Act
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(expected_results=expected_results)


@pytest.mark.rules
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
