"""
Tests for the ApplicationProperties class
"""
from pymarkdown.application_properties import (
    ApplicationProperties,
    ApplicationPropertiesFacade,
)

# pylint: disable=too-many-lines


def test_property_name_separator():
    """
    Test to make sure that the property name separator is as expected.
    """

    # Arrange
    application_properties = ApplicationProperties()
    expected_separator = "."

    # Act
    actual_separator = application_properties.separator

    # Assert
    assert actual_separator == expected_separator


def test_properties_with_object():
    """
    Test to make sure that a default application properties object has no properties.
    """

    # Arrange
    application_properties = ApplicationProperties()
    expected_property_count = 0

    # Act
    actual_property_count = application_properties.number_of_properties

    # Assert
    assert actual_property_count == expected_property_count


def test_properties_with_single_property():
    """
    Test a configuration map with a single property, and how that property looks.
    """

    # Arrange
    application_properties = ApplicationProperties()
    config_map = {"enabled": True}
    expected_property_count = 1

    # Act
    application_properties.load_from_dict(config_map)
    actual_property_count = application_properties.number_of_properties
    found_names = application_properties.property_names

    # Assert
    assert actual_property_count == expected_property_count
    assert len(found_names) == expected_property_count
    assert "enabled" in found_names


def test_properties_with_single_nested_property():
    """
    Test a configuration map with a single nested property, and how that property looks.
    """

    # Arrange
    application_properties = ApplicationProperties()
    config_map = {"feature": {"enabled": True}}
    expected_property_count = 1

    # Act
    application_properties.load_from_dict(config_map)
    actual_property_count = application_properties.number_of_properties
    found_names = application_properties.property_names

    # Assert
    assert actual_property_count == expected_property_count
    assert len(found_names) == expected_property_count
    assert "feature.enabled" in found_names


def test_properties_with_mixed_properties():
    """
    Test a configuration map with properties at different levels, and how those properties look.
    """

    # Arrange
    application_properties = ApplicationProperties()
    config_map = {
        "feature": {"enabled": True},
        "other_feature": {"enabled": False, "other": 1},
    }
    expected_property_count = 3

    # Act
    application_properties.load_from_dict(config_map)
    actual_property_count = application_properties.number_of_properties
    found_names = application_properties.property_names

    # Assert
    assert actual_property_count == expected_property_count
    assert len(found_names) == expected_property_count
    assert "feature.enabled" in found_names
    assert "other_feature.enabled" in found_names
    assert "other_feature.other" in found_names


def test_properties_load_from_non_dictionary():
    """
    Test a loading a configuration map that is not a dictionary.
    """

    # Arrange
    application_properties = ApplicationProperties()
    config_map = [{"feature": True}]

    # Act
    raised_exception = None
    try:
        application_properties.load_from_dict(config_map)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "Specified parameter was not a dictionary."
    ), "Expected message was not present in exception."


def test_properties_load_with_non_string_key():
    """
    Test a loading a configuration map that contains a key that is not a string.
    """

    # Arrange
    application_properties = ApplicationProperties()
    config_map = {1: True}

    # Act
    raised_exception = None
    try:
        application_properties.load_from_dict(config_map)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "All keys in the main dictionary and nested dictionaries must be strings."
    ), "Expected message was not present in exception."


def test_properties_load_with_key_containing_dot():
    """
    Test a loading a configuration map that contains a key with a '.' character.
    """

    # Arrange
    application_properties = ApplicationProperties()
    config_map = {"my.property": True}

    # Act
    raised_exception = None
    try:
        application_properties.load_from_dict(config_map)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Keys strings cannot contain the separator character '.'."
    ), "Expected message was not present in exception."


def test_properties_get_generic_with_bad_type():
    """
    Test a fetching a configuration value where the generic function is
    used and the type and the default are confused.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_property("property", False)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The property_type argument for 'property' must be a type."
    ), "Expected message was not present in exception."


def test_properties_get_generic_with_required_and_found():
    """
    Test a fetching a configuration value where the value is required and present.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = True

    # Act
    actual_value = application_properties.get_property(
        "property", bool, is_required=True
    )

    # Assert
    assert actual_value == expected_value


def test_properties_get_generic_with_required_and_not_found():
    """
    Test a fetching a configuration value where the value is required and not present.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_property("other_property", bool, is_required=True)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "A value for property 'other_property' must be provided."
    ), "Expected message was not present in exception."


def test_properties_get_generic_with_strict_mode_and_bad_type():
    """
    Test a fetching a configuration value where strict mode is on and the type is not correct.
    """

    # Arrange
    config_map = {"property": 1}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_property("property", str, strict_mode=True)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The value for property 'property' must be of type 'str'."
    ), "Expected message was not present in exception."


def test_properties_get_generic_with_global_strict_mode_and_bad_type():
    """
    Test a fetching a configuration value where strict mode is on and the type is not correct.
    """

    # Arrange
    config_map = {"property": 1}
    application_properties = ApplicationProperties(strict_mode=True)
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_property("property", str)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert application_properties.strict_mode
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The value for property 'property' must be of type 'str'."
    ), "Expected message was not present in exception."


def sample_string_validation_function(property_value):
    """
    Simple string validation that throws an error if not "1" or "2".
    """
    if property_value not in ["1", "2"]:
        raise ValueError("Value '" + str(property_value) + "' is not '1' or '2'")


def test_properties_get_generic_with_strict_mode_and_bad_validity():
    """
    Test a fetching a configuration value where strict mode is on and the value is not valid.
    """

    # Arrange
    config_map = {"property": "3"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_property(
            "property",
            str,
            strict_mode=True,
            valid_value_fn=sample_string_validation_function,
        )
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The value for property 'property' is not valid: Value '3' is not '1' or '2'"
    ), "Expected message was not present in exception."


def test_properties_get_boolean_with_found_value():
    """
    Test fetching a configuration value that is present and boolean.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = True

    # Act
    actual_value = application_properties.get_boolean_property("property", False)

    # Assert
    assert expected_value == actual_value


def test_properties_get_boolean_with_found_value_but_wrong_type():
    """
    Test fetching a configuration value that is present and not boolean.
    """

    # Arrange
    config_map = {"property": 1}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = True

    # Act
    actual_value = application_properties.get_boolean_property("property", True)

    # Assert
    assert expected_value == actual_value


def test_properties_get_boolean_with_not_found_value():
    """
    Test fetching a configuration value that is not present and boolean.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = True

    # Act
    actual_value = application_properties.get_boolean_property("other_property", True)

    # Assert
    assert expected_value == actual_value


def test_properties_get_boolean_with_not_found_value_and_no_default_value():
    """
    Test fetching a configuration value that is not present, with no default, and boolean.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    actual_value = application_properties.get_boolean_property("other_property")

    # Assert
    assert actual_value is None


def test_properties_get_boolean_with_a_bad_property_name():
    """
    Test fetching a configuration value with a bad property name.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_boolean_property(1, 1)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "The propertyName argument must be a string."
    ), "Expected message was not present in exception."


def test_properties_get_boolean_with_a_bad_default():
    """
    Test fetching a configuration value with a default value that is not a boolean.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_boolean_property("property", 1)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The default value for property 'property' must either be None or a 'bool' value."
    ), "Expected message was not present in exception."


def test_properties_get_integer_with_found_value():
    """
    Test fetching a configuration value that is present and integer.
    """

    # Arrange
    config_map = {"property": 1}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = 1

    # Act
    actual_value = application_properties.get_integer_property("property", -1)

    # Assert
    assert expected_value == actual_value


def test_properties_get_integer_with_found_value_but_wrong_type():
    """
    Test fetching a configuration value that is present and not integer.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = -1

    # Act
    actual_value = application_properties.get_integer_property("property", -1)

    # Assert
    assert expected_value == actual_value


def test_properties_get_integer_with_not_found_value():
    """
    Test fetching a configuration value that is not present and integer.
    """

    # Arrange
    config_map = {"property": 2}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = 3

    # Act
    actual_value = application_properties.get_integer_property("other_property", 3)

    # Assert
    assert expected_value == actual_value


def test_properties_get_integer_with_not_found_value_and_no_default_value():
    """
    Test fetching a configuration value that is not present, with no default, and integer.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    actual_value = application_properties.get_integer_property("other_property")

    # Assert
    assert actual_value is None


def test_properties_get_integer_with_a_bad_property_name():
    """
    Test fetching a configuration value with a bad property name.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_integer_property(1, 1)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "The propertyName argument must be a string."
    ), "Expected message was not present in exception."


def test_properties_get_integer_with_a_bad_default():
    """
    Test fetching a configuration value with a default value that is not an integer.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_integer_property("property", True)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The default value for property 'property' must either be None or a 'int' value."
    ), "Expected message was not present in exception."


def test_properties_get_string_with_found_value():
    """
    Test fetching a configuration value that is present and string.
    """

    # Arrange
    config_map = {"property": "me"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = "me"

    # Act
    actual_value = application_properties.get_string_property("property", "")

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_with_found_value_but_wrong_type():
    """
    Test fetching a configuration value that is present and not string.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = ""

    # Act
    actual_value = application_properties.get_string_property("property", "")

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_with_not_found_value():
    """
    Test fetching a configuration value that is not present and string.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = "3"

    # Act
    actual_value = application_properties.get_string_property("other_property", "3")

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_with_not_found_value_and_no_default_value():
    """
    Test fetching a configuration value that is not present, with no default, and integer.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    actual_value = application_properties.get_string_property("other_property")

    # Assert
    assert actual_value is None


def test_properties_get_string_with_found_value_validated():
    """
    Test fetching a configuration value that is present and adheres to the validation function.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = "2"

    # Act
    actual_value = application_properties.get_string_property(
        "property", "-", lambda property_value: property_value in ["1", "2"]
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_with_found_value_not_validated():
    """
    Test fetching a configuration value that is present and does not adhere to the validation function.
    """

    # Arrange
    config_map = {"property": "3"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = "-"

    # Act
    actual_value = application_properties.get_string_property(
        "property", "-", sample_string_validation_function
    )

    # Assert
    assert expected_value == actual_value


def bad_validation_function(property_value):
    """
    Test validation function that always throws an exception.
    """
    raise Exception("huh? " + str(property_value))


def test_properties_get_string_with_found_value_validation_raises_error():
    """
    Test fetching a configuration value that is present and the validation function raises an error.
    """

    # Arrange
    config_map = {"property": "1"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = "-"

    # Act
    actual_value = application_properties.get_string_property(
        "property", "-", bad_validation_function
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_with_a_bad_property_name():
    """
    Test fetching a configuration value with a bad property name.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_property(1, "3")
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "The propertyName argument must be a string."
    ), "Expected message was not present in exception."


def test_properties_get_string_with_a_bad_default():
    """
    Test fetching a configuration value with a default value that is not a string.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_property("property", True)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The default value for property 'property' must either be None or a 'str' value."
    ), "Expected message was not present in exception."


def test_properties_facade_base_not_properties_object():
    """
    Test setting up a facade with properties object that is not a properties object.
    """

    # Arrange

    # Act
    raised_exception = None
    try:
        ApplicationPropertiesFacade(1, 1)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The base_properties of the facade must be an ApplicationProperties instance."
    ), "Expected message was not present in exception."


def test_properties_facade_prefix_not_string():
    """
    Test setting up a facade with a prefix that is not a string.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        ApplicationPropertiesFacade(application_properties, 1)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "The property_prefix argument must be a string."
    ), "Expected message was not present in exception."


def test_properties_facade_prefix_not_terminated_with_separator():
    """
    Test setting up a facade with a prefix that is not terminated with the separator.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        ApplicationPropertiesFacade(application_properties, "my")
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The property_prefix argument must end with the separator character '.'."
    ), "Expected message was not present in exception."


def test_properties_facade_get_with_found_value():
    """
    Test fetching through a configuration facade for a property that is present.
    """

    # Arrange
    config_map = {"upper": {"property": 1.2}}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "upper.")
    expected_value = 1.2

    # Act
    actual_value = facade.get_property("property", float)

    # Assert
    assert expected_value == actual_value


def test_properties_facade_get_boolean_with_found_value():
    """
    Test fetching through a configuration facade for a boolean property that is present.
    """

    # Arrange
    config_map = {"upper": {"property": True}}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "upper.")
    expected_value = True

    # Act
    actual_value = facade.get_boolean_property("property")

    # Assert
    assert expected_value == actual_value


def test_properties_facade_get_integer_with_found_value():
    """
    Test fetching through a configuration facade for an integer property that is present.
    """

    # Arrange
    config_map = {"upper": {"property": 2}}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "upper.")
    expected_value = 2

    # Act
    actual_value = facade.get_integer_property("property")

    # Assert
    assert expected_value == actual_value


def test_properties_facade_get_string_with_found_value():
    """
    Test fetching through a configuration facade for a string property that is present.
    """

    # Arrange
    config_map = {"upper": {"property": "2"}}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "upper.")
    expected_value = "2"

    # Act
    actual_value = facade.get_string_property("property")

    # Assert
    assert expected_value == actual_value


def test_properties_set_manual_property_with_non_string():
    """
    Test to make sure that a manual property with a non-string is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_string = 1

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Manual property form must either be a string or an iterable of strings."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_no_equals():
    """
    Test to make sure that a full key with no value part is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_string = "a_property"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Manual property key and value must be separated by the '=' character."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_single_part_string():
    """
    Test to make sure that a full key specifying an string without any format is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = "123"
    full_string = f"{full_property_key}={property_value}"

    # Act
    application_properties.set_manual_property(full_string)

    # Assert
    actual_value = application_properties.get_string_property(full_property_key)
    assert property_value == actual_value


def test_properties_set_manual_property_with_only_format_indicator():
    """
    Test to make sure that a full key specifying an string format but with no format character following is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = "$123"
    full_string = f"{full_property_key}={property_value}"

    # Act
    application_properties.set_manual_property(full_string)

    # Assert
    actual_value = application_properties.get_string_property(full_property_key)
    assert property_value[1:] == actual_value


def test_properties_set_manual_property_with_string_indicator():
    """
    Test to make sure that a full key specifying an string is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = "$$123"
    full_string = f"{full_property_key}={property_value}"

    # Act
    application_properties.set_manual_property(full_string)

    # Assert
    actual_value = application_properties.get_string_property(full_property_key)
    assert property_value[2:] == actual_value


def test_properties_set_manual_property_with_integer_indicator():
    """
    Test to make sure that a full key specifying an integer is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    application_properties.set_manual_property(full_string)

    # Assert
    actual_value = application_properties.get_integer_property(full_property_key)
    assert property_value == actual_value


def test_properties_set_manual_property_with_integer_indicator_and_bad_integer():
    """
    Test to make sure that a full key specifying a bad integer is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}a"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Manual property value '$#123a' cannot be translated into an integer."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_boolean_indicator():
    """
    Test to make sure that a full key specifying a True boolean is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = True
    full_string = f"{full_property_key}=$!{property_value}"

    # Act
    application_properties.set_manual_property(full_string)

    # Assert
    actual_value = application_properties.get_boolean_property(full_property_key)
    assert property_value == actual_value


def test_properties_set_manual_property_with_uncased_boolean_indicator():
    """
    Test to make sure that a full key specifying a True boolean in lower case is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = True
    full_string = f"{full_property_key}=$!{str(property_value).lower()}"

    # Act
    application_properties.set_manual_property(full_string)

    # Assert
    actual_value = application_properties.get_boolean_property(full_property_key)
    assert property_value == actual_value


def test_properties_set_manual_property_with_multiples():
    """
    Test to make sure that a list of full keys is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = True
    full_string = f"{full_property_key}=$!{property_value}"

    # Act
    application_properties.set_manual_property([full_string])

    # Assert
    actual_value = application_properties.get_boolean_property(full_property_key)
    assert property_value == actual_value


def test_properties_set_manual_property_with_bad_key_start():
    """
    Test to make sure that a full key starting with the key separator character is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = ".a"
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Full property key must not start or end with the '.' character."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_bad_key_end():
    """
    Test to make sure that a full key ending with the key separator character is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a."
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Full property key must not start or end with the '.' character."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_empty_key_middle():
    """
    Test to make sure that an empty key part for the full key is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a..a"
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Full property key cannot contain multiples of the . without any text between them."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_empty_key():
    """
    Test to make sure that a key with an empty key part is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = ""
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Each part of the property key must contain at least one character."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_whitespace_key():
    """
    Test to make sure that a key with whitespace is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a a"
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Each part of the property key must not contain a whitespace character or the '.' character."
    ), "Expected message was not present in exception."


def test_properties_verify_manual_property_form_with_non_string():
    """
    Test to make sure that if we try and test the verification form function
    with a non-string, it fails predictably.
    """

    # Arrange
    full_string = 1

    # Act
    raised_exception = None
    try:
        ApplicationProperties.verify_manual_property_form(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "Manual property form must be a string."
    ), "Expected message was not present in exception."
