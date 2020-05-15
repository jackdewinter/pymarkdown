"""
Module to provide tests related to the MD024 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

from .utils import write_temporary_configuration


@pytest.mark.rules
def test_md024_good_different_heading_content_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has atx headings that all have different
    text in them.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md024/different_heading_content_atx.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_content_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has atx headings that have some duplicated
    text in them.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md024/same_heading_content_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_content_atx.md:0:0: "
        + "MD024: Multiple headings with the same content (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_in_siblings_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has atx headings that have some duplicated
    text in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md024/same_heading_in_siblings_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_in_siblings_atx.md:0:0: "
        + "MD024: Multiple headings with the same content (no-duplicate-heading,no-duplicate-header)\n"
        + "test/resources/rules/md024/same_heading_in_siblings_atx.md:0:0: "
        + "MD024: Multiple headings with the same content (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_but_not_in_siblings_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has atx headings that have some duplicated
    text but not in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md024/same_heading_but_not_in_siblings_atx.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_but_not_in_siblings_atx.md:0:0: "
        + "MD024: Multiple headings with the same content (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_good_different_heading_content_atx_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has atx headings that all have different
    text in them, with configuration allowing for duplicated text except for in
    sibling headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD024": {"siblings_only": True}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md024/different_heading_content_atx.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_good_same_heading_content_atx_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has atx headings that have some duplicated
    text in them, with configuration allowing for duplicated text except for in
    sibling headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD024": {"siblings_only": True}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md024/same_heading_content_atx.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_bad_same_heading_in_siblings_atx_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has atx headings that have some duplicated
    text in siblings, with configuration allowing for duplicated text except for in
    sibling headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD024": {"siblings_only": True}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md024/same_heading_in_siblings_atx.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md024/same_heading_in_siblings_atx.md:0:0: "
            + "MD024: Multiple headings with the same content (no-duplicate-heading,no-duplicate-header)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_good_same_heading_but_not_in_siblings_atx_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has atx headings that have some duplicated
    text but not in siblings, with configuration allowing for duplicated text except for
    in sibling headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD024": {"siblings_only": True}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md024/same_heading_but_not_in_siblings_atx.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_good_same_heading_but_not_in_siblings_atx_with_alternate_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has atx headings that have some duplicated
    text but not in siblings, with the alternate configuration name allowing for
    duplicated text except for in sibling headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD024": {"allow_different_nesting": True}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md024/same_heading_but_not_in_siblings_atx.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_good_different_inline_heading_content_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md021 directory that has good atx heading start spacing
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md024/different_inline_heading_content_atx.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_good_different_heading_content_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has setext headings that all have different
    text in them.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md024/different_heading_content_setext.md",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_content_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has setext headings that have some duplicated
    text in them.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md024/same_heading_content_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_content_setext.md:0:0: "
        + "MD024: Multiple headings with the same content (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_in_siblings_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has setext headings that have some duplicated
    text in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md024/same_heading_in_siblings_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_in_siblings_setext.md:0:0: "
        + "MD024: Multiple headings with the same content (no-duplicate-heading,no-duplicate-header)\n"
        + "test/resources/rules/md024/same_heading_in_siblings_setext.md:0:0: "
        + "MD024: Multiple headings with the same content (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_bad_same_heading_but_not_in_siblings_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has setext headings that have some duplicated
    text but not in siblings.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md024/same_heading_but_not_in_siblings_setext.md",
    ]

    expected_return_code = 1
    expected_output = (
        "test/resources/rules/md024/same_heading_but_not_in_siblings_setext.md:0:0: "
        + "MD024: Multiple headings with the same content (no-duplicate-heading,no-duplicate-header)\n"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md024_good_different_heading_content_setext_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has setext headings that all have different
    text in them, with configuration allowing for duplicated text except for in
    sibling headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD024": {"siblings_only": True}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md024/different_heading_content_setext.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_good_same_heading_content_setext_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has setext headings that have some
    duplicated text in them, with configuration allowing for duplicated text except for
    in sibling headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD024": {"siblings_only": True}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md024/same_heading_content_setext.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_bad_same_heading_in_siblings_setext_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has setext headings that have some duplicated
    text in siblings, with configuration allowing for duplicated text except for in
    sibling headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD024": {"siblings_only": True}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md024/same_heading_in_siblings_setext.md",
        ]

        expected_return_code = 1
        expected_output = (
            "test/resources/rules/md024/same_heading_in_siblings_setext.md:0:0: "
            + "MD024: Multiple headings with the same content (no-duplicate-heading,no-duplicate-header)\n"
        )
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md024_good_same_heading_but_not_in_siblings_setext_with_configuration():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/MD024 directory that has setext headings that have some duplicated
    text but not in siblings, with configuration allowing for duplicated text except for
    in sibling headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD024": {"siblings_only": True}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md024/same_heading_but_not_in_siblings_setext.md",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=suppplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if os.path.exists(configuration_file):
            os.remove(configuration_file)
