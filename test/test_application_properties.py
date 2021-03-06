"""
Tests for the ApplicationProperties class
"""
from pymarkdown.application_properties import ApplicationProperties


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
        str(raised_exception) == "The default value must either be None or a boolean."
    ), "Expected message was not present in exception."
