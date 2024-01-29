"""
Tests for the calculate_length function
"""

from pymarkdown.general.constants import ConstantWrapper


def test_values_are_equal():
    """
    Make sure that an simple equality is possible.
    """

    # Arrange
    input_string = "value"
    constant_value = ConstantWrapper(input_string)

    # Act

    # Assert
    assert constant_value.value() == input_string


def test_contains():
    """
    Make sure that instead of "in" using the value, a "contains" can be used.
    """

    # Arrange
    input_string = "value"
    constant_value = ConstantWrapper(input_string)

    # Act

    # Assert
    assert constant_value.contains("al")
