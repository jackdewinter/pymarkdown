"""
Module to provide tests related to the MD035 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import assert_file_is_as_expected, copy_to_temp_file

import pytest

source_path = os.path.join("test", "resources", "rules", "md035") + os.sep


@pytest.mark.rules
def test_md035_bad_configuration_style():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with an integer that is not a string.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "good_consistent_dash.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md035.style=$#1",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md035.style' must be of type 'str'."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md035_bad_configuration_style_leading_spaces():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with string specifying thematic break with leading spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "good_consistent_dash.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md035.style= ---",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md035.style' is not valid: Allowable values cannot including leading or trailing spaces."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md035_bad_configuration_style_empty():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with string specifying thematic break that is empty
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "good_consistent_dash.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md035.style=",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md035.style' is not valid: Allowable values are: consistent, '---', '***', `___`, or any other horizontal rule text."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md035_bad_configuration_style_trailing_spaces():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with string specifying thematic break with trailing spaces.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "good_consistent_dash.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md035.style=--- ",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md035.style' is not valid: Allowable values cannot including leading or trailing spaces."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md035_bad_configuration_style_bad_character():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with string specifying thematic break with a bad character.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "good_consistent_dash.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md035.style=-=-=-",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md035.style' is not valid: Allowable values are: consistent, '---', '***', `___`, or any other horizontal rule text."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md035_bad_configuration_style_mixed_characters():
    """
    Test to verify that a configuration error is thrown when supplying the
    style value with string specifying valid thematic break characters that
    are not the same as each other.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "good_consistent_dash.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md035.style=*-*-*-*",
        "--strict-config",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = (
        "BadPluginError encountered while configuring plugins:\n"
        + "The value for property 'plugins.md035.style' is not valid: Allowable values are: consistent, '---', '***', `___`, or any other horizontal rule text."
    )

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md035_good_configuration_style_consistent():
    """
    Test to make sure this rule does not trigger with a document that
    contains thematic breaks that are consistent dashes with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "good_consistent_dash.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md035.style=consistent",
        "--strict-config",
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
def test_md035_good_consistent_dash():
    """
    Test to make sure this rule does not trigger with a document that
    contains thematic breaks that are consistent dashes with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "good_consistent_dash.md"
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
def test_md035_bad_consistent_dash():
    """
    Test to make sure this rule does trigger with a document that
    contains thematic breaks that are not consistent dashes with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "bad_consistent_dash.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:1: "
        + "MD035: Horizontal rule style "
        + "[Expected: ---, Actual: - - -] (hr-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md035_bad_consistent_dash_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains thematic breaks that are not consistent dashes with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(source_path + "bad_consistent_dash.md") as temp_source_path:
        original_file_contents = """---

this is one section

- - -
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

        expected_file_contents = """---

this is one section

---
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md035_bad_consistent_dash_with_leading_spaces():
    """
    Test to make sure this rule does trigger with a document that
    contains thematic breaks that are not consistent dashes with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test",
        "resources",
        "rules",
        "md035",
        "bad_consistent_dash_with_leading_spaces.md",
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:2: "
        + "MD035: Horizontal rule style "
        + "[Expected: ---, Actual: - - -] (hr-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md035_bad_consistent_dash_with_leading_spaces_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains thematic breaks that are not consistent dashes with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_consistent_dash_with_leading_spaces.md"
    ) as temp_source_path:
        original_file_contents = """---

this is one section

 - - -
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

        expected_file_contents = """---

this is one section

 ---
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md035_good_dash_marker():
    """
    Test to make sure this rule does not trigger with a document that
    contains thematic breaks that are three dashes with configuration of three dashes.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "good_consistent_dash.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md035.style=---",
        "--strict-config",
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
def test_md035_bad_dash_marker():
    """
    Test to make sure this rule does trigger with a document that
    contains thematic breaks that are not three dashes with configuration of three dashes.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "bad_consistent_dash.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md035.style=---",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:1: "
        + "MD035: Horizontal rule style "
        + "[Expected: ---, Actual: - - -] (hr-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md035_bad_dash_marker_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains thematic breaks that are not consistent dashes with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(source_path + "bad_consistent_dash.md") as temp_source_path:
        original_file_contents = """---

this is one section

- - -
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

        expected_file_contents = """---

this is one section

---
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md035_good_consistent_asterisk():
    """
    Test to make sure this rule does not trigger with a document that
    contains thematic breaks that are asterisks with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "good_consistent_asterisk.md"
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
def test_md035_bad_consistent_asterisk():
    """
    Test to make sure this rule does trigger with a document that
    contains thematic breaks that are different asterisks with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "bad_consistent_asterisk.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:1: "
        + "MD035: Horizontal rule style "
        + "[Expected: ***, Actual: * * *] (hr-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md035_bad_consistent_asterisk_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains thematic breaks that are not consistent dashes with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_consistent_asterisk.md"
    ) as temp_source_path:
        original_file_contents = """***

this is one section

* * *
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

        expected_file_contents = """***

this is one section

***
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md035_good_asterisk_marker():
    """
    Test to make sure this rule does not trigger with a document that
    contains thematic breaks that are three asterisk with configuration of three asterisks.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "good_consistent_asterisk.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md035.style=* * *",
        "--strict-config",
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
def test_md035_bad_asterisk_marker():
    """
    Test to make sure this rule does trigger with a document that
    contains thematic breaks that are three asterisk with configuration of different three asterisks.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "bad_consistent_asterisk.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md035.style=* * *",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD035: Horizontal rule style "
        + "[Expected: * * *, Actual: ***] (hr-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md035_bad_asterisk_marker_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains thematic breaks that are not consistent dashes with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_consistent_asterisk.md"
    ) as temp_source_path:
        original_file_contents = """***

this is one section

* * *
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

        expected_file_contents = """***

this is one section

***
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md035_good_consistent_underscore():
    """
    Test to make sure this rule does not trigger with a document that
    contains thematic breaks that are three underscores with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "good_consistent_underscore.md"
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
def test_md035_bad_consistent_underscore():
    """
    Test to make sure this rule does not trigger with a document that
    contains thematic breaks that are underscores with consistent and different underscores.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "bad_consistent_underscore.md"
    )
    supplied_arguments = [
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:5:1: "
        + "MD035: Horizontal rule style "
        + "[Expected: ___, Actual: ______] (hr-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md035_bad_consistent_underscore_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains thematic breaks that are not consistent dashes with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_consistent_underscore.md"
    ) as temp_source_path:
        original_file_contents = """___

this is one section

______
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

        expected_file_contents = """___

this is one section

___
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)


@pytest.mark.rules
def test_md035_good_underscore_marker():
    """
    Test to make sure this rule does not trigger with a document that
    contains thematic breaks that are underscores with configuration to match.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "good_consistent_underscore.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md035.style=______",
        "--strict-config",
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
def test_md035_bad_underscore_marker():
    """
    Test to make sure this rule does trigger with a document that
    contains thematic breaks that are underscores with configuration that does not match.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md035", "bad_consistent_underscore.md"
    )
    supplied_arguments = [
        "--set",
        "plugins.md035.style=______",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: "
        + "MD035: Horizontal rule style "
        + "[Expected: ______, Actual: ___] (hr-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.rules
def test_md035_bad_underscore_marker_fix():
    """
    Test to make sure this rule does trigger with a document that
    contains thematic breaks that are not consistent dashes with consistent.
    """

    # Arrange
    scanner = MarkdownScanner()
    with copy_to_temp_file(
        source_path + "bad_consistent_underscore.md"
    ) as temp_source_path:
        original_file_contents = """___

this is one section

______
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

        expected_file_contents = """___

this is one section

___
"""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
        assert_file_is_as_expected(temp_source_path, expected_file_contents)
