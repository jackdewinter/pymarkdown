"""
Module to provide tests related to the MD003 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner

import pytest

from .utils import write_temporary_configuration

# pylint: disable=too-many-lines

CONSISTENT_ATX_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_consistent_headings_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only atx headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md003/headings_atx.md",
    ]

    expected_return_code = 0
    expected_output = CONSISTENT_ATX_HEADINGS_SAMPLE_OUTPUT
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


CONSISTENT_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_consistent_headings_atx_closed():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only closed atx headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md003/headings_atx_closed.md",
    ]

    expected_return_code = 0
    expected_output = CONSISTENT_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


CONSISTENT_SETEXT_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_consistent_headings_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md003/headings_setext.md",
    ]

    expected_return_code = 0
    expected_output = CONSISTENT_SETEXT_HEADINGS_SAMPLE_OUTPUT
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


CONSISTENT_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_setext_with_atx.md:7:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_consistent_headings_setext_with_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings for the first two
    levels and then atx headings beyond that.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md003/headings_setext_with_atx.md",
    ]

    expected_return_code = 1
    expected_output = CONSISTENT_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


CONSISTENT_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_setext_with_atx_closed.md:7:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_consistent_headings_setext_with_atx_closed():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings for the first two
    levels and then atx closed headings beyond that.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = [
        "test/resources/rules/md003/headings_setext_with_atx_closed.md",
    ]

    expected_return_code = 1
    expected_output = CONSISTENT_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md003_consistent_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md003 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    suppplied_arguments = ["test/resources/rules/md003"]

    expected_return_code = 1
    expected_output = (
        CONSISTENT_ATX_HEADINGS_SAMPLE_OUTPUT
        + CONSISTENT_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
        + CONSISTENT_SETEXT_HEADINGS_SAMPLE_OUTPUT
        + CONSISTENT_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
        + CONSISTENT_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=suppplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


ATX_ATX_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_atx_headings_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only atx headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "atx"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_atx.md",
        ]

        expected_return_code = 0
        expected_output = ATX_ATX_HEADINGS_SAMPLE_OUTPUT
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


ATX_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_atx_closed.md:1:1: "
    + "MD003: Heading style [Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_atx_closed.md:3:1: "
    + "MD003: Heading style [Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atx_headings_atx_closed():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only closed atx headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "atx"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = ATX_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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


ATX_SETEXT_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_setext.md:0:0: "
    + "MD003: Heading style [Expected: atx; Actual: setext] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_setext.md:0:0: "
    + "MD003: Heading style [Expected: atx; Actual: setext] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atx_headings_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "atx"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext.md",
        ]

        expected_return_code = 1
        expected_output = ATX_SETEXT_HEADINGS_SAMPLE_OUTPUT
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


ATX_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_setext_with_atx.md:0:0: "
    + "MD003: Heading style [Expected: atx; Actual: setext] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_setext_with_atx.md:0:0: "
    + "MD003: Heading style [Expected: atx; Actual: setext] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atx_headings_setext_with_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings for the first two
    levels and then atx headings beyond that.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "atx"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext_with_atx.md",
        ]

        expected_return_code = 1
        expected_output = ATX_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
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


ATX_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_setext_with_atx_closed.md:0:0: "
    + "MD003: Heading style [Expected: atx; Actual: setext] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_setext_with_atx_closed.md:0:0: "
    + "MD003: Heading style [Expected: atx; Actual: setext] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_setext_with_atx_closed.md:7:1: "
    + "MD003: Heading style [Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atx_headings_setext_with_atx_closed():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings for the first two
    levels and then atx closed headings beyond that.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "atx"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext_with_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = ATX_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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
def test_md003_atx_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md003 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "atx"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = ["-c", configuration_file, "test/resources/rules/md003"]

        expected_return_code = 1
        expected_output = (
            ATX_ATX_HEADINGS_SAMPLE_OUTPUT
            + ATX_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
            + ATX_SETEXT_HEADINGS_SAMPLE_OUTPUT
            + ATX_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
            + ATX_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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


ATXCLOSED_ATX_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_atx.md:1:1: "
    + "MD003: Heading style [Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_atx.md:3:1: "
    + "MD003: Heading style [Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atxclosed_headings_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only atx headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "atx_closed"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_atx.md",
        ]

        expected_return_code = 1
        expected_output = ATXCLOSED_ATX_HEADINGS_SAMPLE_OUTPUT
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


ATXCLOSED_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_atxclosed_headings_atx_closed():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only closed atx headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "atx_closed"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_atx_closed.md",
        ]

        expected_return_code = 0
        expected_output = ATXCLOSED_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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


ATXCLOSED_SETEXT_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_setext.md:0:0: "
    + "MD003: Heading style [Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_setext.md:0:0: "
    + "MD003: Heading style [Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atxclosed_headings_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "atx_closed"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext.md",
        ]

        expected_return_code = 1
        expected_output = ATXCLOSED_SETEXT_HEADINGS_SAMPLE_OUTPUT
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


ATXCLOSED_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_setext_with_atx.md:0:0: "
    + "MD003: Heading style [Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_setext_with_atx.md:0:0: "
    + "MD003: Heading style [Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_setext_with_atx.md:7:1: "
    + "MD003: Heading style [Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atxclosed_headings_setext_with_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings for the first two
    levels and then atx headings beyond that.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "atx_closed"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext_with_atx.md",
        ]

        expected_return_code = 1
        expected_output = ATXCLOSED_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
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


ATXCLOSED_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_setext_with_atx_closed.md:0:0: "
    + "MD003: Heading style [Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_setext_with_atx_closed.md:0:0: "
    + "MD003: Heading style [Expected: atx_closed; Actual: setext] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_atxclosed_headings_setext_with_atx_closed():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings for the first two
    levels and then atx closed headings beyond that.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "atx_closed"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext_with_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = ATXCLOSED_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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
def test_md003_atxclosed_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md003 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "atx_closed"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = ["-c", configuration_file, "test/resources/rules/md003"]

        expected_return_code = 1
        expected_output = (
            ATXCLOSED_ATX_HEADINGS_SAMPLE_OUTPUT
            + ATXCLOSED_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
            + ATXCLOSED_SETEXT_HEADINGS_SAMPLE_OUTPUT
            + ATXCLOSED_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
            + ATXCLOSED_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_ATX_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_atx.md:1:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_atx.md:3:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_headings_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only atx headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_atx.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_ATX_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_atx_closed.md:1:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_atx_closed.md:3:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_headings_atx_closed():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only closed atx headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_SETEXT_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_setext_headings_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext.md",
        ]

        expected_return_code = 0
        expected_output = SETEXT_SETEXT_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_setext_with_atx.md:7:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_headings_setext_with_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings for the first two
    levels and then atx headings beyond that.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext_with_atx.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_setext_with_atx_closed.md:7:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_headings_setext_with_atx_closed():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings for the first two
    levels and then atx closed headings beyond that.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext_with_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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
def test_md003_setext_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md003 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = ["-c", configuration_file, "test/resources/rules/md003"]

        expected_return_code = 1
        expected_output = (
            SETEXT_ATX_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_SETEXT_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_WITH_ATX_ATX_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_atx.md:1:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_atx.md:3:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_with_atx_headings_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only atx headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext_with_atx"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_atx.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_WITH_ATX_ATX_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_WITH_ATX_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_atx_closed.md:1:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_atx_closed.md:3:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_with_atx_headings_atx_closed():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only closed atx headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext_with_atx"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_WITH_ATX_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_WITH_ATX_SETEXT_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_setext_with_atx_headings_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext_with_atx"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext.md",
        ]

        expected_return_code = 0
        expected_output = SETEXT_WITH_ATX_SETEXT_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_WITH_ATX_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_setext_with_atx_headings_setext_with_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings for the first two
    levels and then atx headings beyond that.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext_with_atx"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext_with_atx.md",
        ]

        expected_return_code = 0
        expected_output = SETEXT_WITH_ATX_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_WITH_ATX_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_setext_with_atx_closed.md:7:1: "
    + "MD003: Heading style [Expected: atx; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_with_atx_headings_setext_with_atx_closed():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings for the first two
    levels and then atx closed headings beyond that.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext_with_atx"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext_with_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_WITH_ATX_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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
def test_md003_setext_with_atx_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md003 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext_with_atx"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = ["-c", configuration_file, "test/resources/rules/md003"]

        expected_return_code = 1
        expected_output = (
            SETEXT_WITH_ATX_ATX_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_WITH_ATX_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_WITH_ATX_SETEXT_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_WITH_ATX_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_WITH_ATX_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_WITH_ATX_CLOSED_ATX_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_atx.md:1:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_atx.md:3:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_with_atx_closed_headings_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only atx headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext_with_atx_closed"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_atx.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_WITH_ATX_CLOSED_ATX_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_WITH_ATX_CLOSED_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_atx_closed.md:1:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
    + "test/resources/rules/md003/headings_atx_closed.md:3:1: "
    + "MD003: Heading style [Expected: setext; Actual: atx_closed] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_with_atx_closed_headings_atx_closed():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only closed atx headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext_with_atx_closed"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_atx_closed.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_WITH_ATX_CLOSED_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_WITH_ATX_CLOSED_SETEXT_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_setext_with_atx_closed_headings_setext():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext_with_atx_closed"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext.md",
        ]

        expected_return_code = 0
        expected_output = SETEXT_WITH_ATX_CLOSED_SETEXT_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_WITH_ATX_CLOSED_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT = (
    "test/resources/rules/md003/headings_setext_with_atx.md:7:1: "
    + "MD003: Heading style [Expected: atx_closed; Actual: atx] (heading-style,header-style)\n"
)


@pytest.mark.rules
def test_md003_bad_setext_with_atx_closed_headings_setext_with_atx():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings for the first two
    levels and then atx headings beyond that.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext_with_atx_closed"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext_with_atx.md",
        ]

        expected_return_code = 1
        expected_output = SETEXT_WITH_ATX_CLOSED_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
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


SETEXT_WITH_ATX_CLOSED_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT = ""


@pytest.mark.rules
def test_md003_good_setext_with_atx_closed_headings_setext_with_atx_closed():
    """
    Test to make sure we get the expected behavior after scanning a good file from the
    test/resources/rules/md003 directory that has only setext headings for the first two
    levels and then atx closed headings beyond that.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext_with_atx_closed"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = [
            "-c",
            configuration_file,
            "test/resources/rules/md003/headings_setext_with_atx_closed.md",
        ]

        expected_return_code = 0
        expected_output = (
            SETEXT_WITH_ATX_CLOSED_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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
def test_md003_setext_with_atx_closed_all_samples():
    """
    Test to make sure we get the expected behavior after scanning the files in the
    test/resources/rules/md003 directory.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_configuration = {"MD003": {"style": "setext_with_atx_closed"}}
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        suppplied_arguments = ["-c", configuration_file, "test/resources/rules/md003"]

        expected_return_code = 1
        expected_output = (
            SETEXT_WITH_ATX_CLOSED_ATX_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_WITH_ATX_CLOSED_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_WITH_ATX_CLOSED_SETEXT_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_WITH_ATX_CLOSED_SETEXT_WITH_ATX_HEADINGS_SAMPLE_OUTPUT
            + SETEXT_WITH_ATX_CLOSED_SETEXT_WITH_ATX_CLOSED_HEADINGS_SAMPLE_OUTPUT
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
