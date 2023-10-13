"""
Module for specifying configuration properties through the API.
"""

import os
from test.utils import assert_that_exception_is_raised

from pymarkdown.api import (
    PyMarkdownApi,
    PyMarkdownApiArgumentException,
    PyMarkdownApiException,
    PyMarkdownScanFailure,
)


def test_api_properties_set_property_with_empty_property_name():
    """
    Test to make sure that a property name is always provided.
    """

    # Arrange
    property_name = ""
    property_value = "something"

    expected_output = "Parameter named 'property_name' cannot be empty."

    # Act & Assert
    caught_exception = assert_that_exception_is_raised(
        PyMarkdownApiArgumentException,
        expected_output,
        PyMarkdownApi().set_property,
        property_name,
        property_value,
    )
    assert caught_exception.argument_name == "property_name"


def test_api_properties_set_boolean_property_with_empty_property_name():
    """
    Test to make sure that a property name is always provided.
    """

    # Arrange
    property_name = ""
    property_value = True

    expected_output = "Parameter named 'property_name' cannot be empty."

    # Act & Assert
    caught_exception = assert_that_exception_is_raised(
        PyMarkdownApiArgumentException,
        expected_output,
        PyMarkdownApi().set_property,
        property_name,
        property_value,
    )
    assert caught_exception.argument_name == "property_name"


def test_api_properties_set_boolean_property_with_non_boolean_value():
    """
    Test to make sure that a property value for set_boolean_property is a boolean.
    """

    # Arrange
    property_name = "something"
    property_value = "something"

    expected_output = "The property value 'property_value' was not passed as a boolean."

    # Act & Assert
    caught_exception = assert_that_exception_is_raised(
        PyMarkdownApiArgumentException,
        expected_output,
        PyMarkdownApi().set_boolean_property,
        property_name,
        property_value,
    )
    assert caught_exception.argument_name == "property_value"


def test_api_properties_set_integer_property_with_empty_property_name():
    """
    Test to make sure that a property name is always provided.
    """

    # Arrange
    property_name = ""
    property_value = 1

    expected_output = "Parameter named 'property_name' cannot be empty."

    # Act & Assert
    caught_exception = assert_that_exception_is_raised(
        PyMarkdownApiArgumentException,
        expected_output,
        PyMarkdownApi().set_integer_property,
        property_name,
        property_value,
    )
    assert caught_exception.argument_name == "property_name"


def test_api_properties_set_integer_property_with_non_integer_value():
    """
    Test to make sure that a property value for set_integer_property is an integer.
    """

    # Arrange
    property_name = "something"
    property_value = "something"

    expected_output = (
        "The property value 'property_value' was not passed as an integer."
    )

    # Act & Assert
    caught_exception = assert_that_exception_is_raised(
        PyMarkdownApiArgumentException,
        expected_output,
        PyMarkdownApi().set_integer_property,
        property_name,
        property_value,
    )
    assert caught_exception.argument_name == "property_value"


def test_api_properties_set_string_property_with_empty_property_name():
    """
    Test to make sure that a property name is always provided.
    """

    # Arrange
    property_name = ""
    property_value = 1

    expected_output = "Parameter named 'property_name' cannot be empty."

    # Act & Assert
    caught_exception = assert_that_exception_is_raised(
        PyMarkdownApiArgumentException,
        expected_output,
        PyMarkdownApi().set_string_property,
        property_name,
        property_value,
    )
    assert caught_exception.argument_name == "property_name"


def test_api_properties_set_string_property_with_non_string_value():
    """
    Test to make sure that a property value for set_string_property is a string.
    """

    # Arrange
    property_name = "something"
    property_value = 1

    expected_output = "The property value 'property_value' was not passed as a string."

    # Act & Assert
    caught_exception = assert_that_exception_is_raised(
        PyMarkdownApiArgumentException,
        expected_output,
        PyMarkdownApi().set_string_property,
        property_name,
        property_value,
    )
    assert caught_exception.argument_name == "property_value"


def test_api_properties_with_strict_and_bad_extension_initialize():
    """
    Test to make sure that if we are setting an expected value and we do not
    set it with the right primitives while strict is enabled, it will raise
    an exception.

    This function shadows
    test_front_matter_21b
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "pragmas", "extensions_issue_637.md"
    )
    property_name = "extensions.front-matter.enabled"
    property_value = "true"

    expected_output = """Configuration error ValueError encountered while initializing extensions:
The value for property 'extensions.front-matter.enabled' must be of type 'bool'."""

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiException,
        expected_output,
        PyMarkdownApi()
        .enable_strict_configuration()
        .set_property(property_name, property_value)
        .scan_path,
        source_path,
    )


def test_api_properties_without_strict_and_bad_extension_initialize():
    """
    Test to make sure that if we are setting an expected value and we do not
    set it with the right primitives without strict enabled, it will fail silently.
    In this case, wiuthout front-matter enabled, the document looks like it is
    poorly formed.

    This function shadows
    test_front_matter_21a
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "pragmas", "extensions_issue_637.md"
    )
    property_name = "extensions.front-matter.enabledd"
    property_value = "true"

    # Act
    scan_result = (
        PyMarkdownApi()
        .enable_strict_configuration()
        .set_property(property_name, property_value)
        .scan_path(source_path)
    )

    # Assert
    assert scan_result
    assert not scan_result.pragma_errors
    assert len(scan_result.scan_failures) == 4
    assert scan_result.scan_failures[0].partial_equals(
        PyMarkdownScanFailure(source_path, 1, 1, "MD041", "", "", None)
    )
    assert scan_result.scan_failures[1].partial_equals(
        PyMarkdownScanFailure(source_path, 2, 1, "MD022", "", "", None)
    )
    assert scan_result.scan_failures[2].partial_equals(
        PyMarkdownScanFailure(source_path, 6, 1, "MD003", "", "", None)
    )
    assert scan_result.scan_failures[3].partial_equals(
        PyMarkdownScanFailure(source_path, 8, 1, "MD003", "", "", None)
    )


def test_api_properties_with_strict_and_good_extension_initialize():
    """
    Test to make sure that if we are setting an expected value and we set it
    with the right primitives with strict enabled, it will succeed.

    This function shadows
    test_front_matter_21
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "pragmas", "extensions_issue_637.md"
    )
    property_name = "extensions.front-matter.enabled"
    property_value = True

    # Act
    scan_result = (
        PyMarkdownApi()
        .enable_strict_configuration()
        .set_boolean_property(property_name, property_value)
        .scan_path(source_path)
    )

    # Assert
    assert scan_result
    assert not scan_result.scan_failures
    assert not scan_result.pragma_errors


def test_api_properties_with_good_integer_property_but_exception():
    """
    Test to make sure that we can still provide a valid integer property, but get a configuration exception.

    This function shadows
    test_md002_bad_configuration_level_value
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "pragmas", "extensions_issue_637.md"
    )
    property_name = "extensions.front-matter.enabled"
    property_value = 10

    expected_output = """Configuration error ValueError encountered while initializing extensions:
The value for property 'extensions.front-matter.enabled' must be of type 'bool'."""

    # Act & Assert
    assert_that_exception_is_raised(
        PyMarkdownApiException,
        expected_output,
        PyMarkdownApi()
        .enable_strict_configuration()
        .set_integer_property(property_name, property_value)
        .enable_rule_by_identifier("MD002")
        .scan_path,
        source_path,
    )


def test_api_properties_with_good_integer_property():
    """
    Test to make sure that we can still provide a valid integer property.

    This function shadows
    test_md007_good_list_indentation_by_four
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md007", "good_list_indentation_by_four.md"
    )
    property_name = "plugins.md007.indent"
    property_value = 4

    # Act
    scan_result = (
        PyMarkdownApi()
        .enable_strict_configuration()
        .set_integer_property(property_name, property_value)
        .disable_rule_by_identifier("MD041")
        .enable_rule_by_identifier("MD002")
        .scan_path(source_path)
    )

    # Assert
    assert scan_result
    assert not scan_result.scan_failures
    assert not scan_result.pragma_errors


def test_api_properties_with_good_string_property():
    """
    Test to make sure that we can still provide a valid string property.

    This function shadows
    test_md004_good_asterisk_single_level
    """

    # Arrange
    source_path = os.path.join(
        "test", "resources", "rules", "md004", "good_list_asterisk_single_level.md"
    )
    property_name = "plugins.md004.style"
    property_value = "asterisk"

    # Act
    scan_result = (
        PyMarkdownApi()
        .enable_strict_configuration()
        .set_string_property(property_name, property_value)
        .disable_rule_by_identifier("MD041")
        .scan_path(source_path)
    )

    # Assert
    assert scan_result
    assert not scan_result.scan_failures
    assert not scan_result.pragma_errors
