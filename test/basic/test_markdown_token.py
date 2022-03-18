"""
Module to test the StackToken class.
"""
from pymarkdown.stack_token import StackToken


def test_stack_token_equal():
    """
    Test to make sure two equal StackToken instances are equal.
    """

    # Arrange
    token1 = StackToken("type1", extra_data="extra1")
    token2 = StackToken("type1", extra_data="extra1")

    # Act
    are_equal = token1 == token2

    # Assert
    assert are_equal


def test_stack_token_not_equal_type():
    """
    Test to make sure two StackToken instances with a different type name are not equal.
    """

    # Arrange
    token1 = StackToken("type1", extra_data="extra1")
    token2 = StackToken("type2", extra_data="extra1")

    # Act
    are_equal = token1 == token2

    # Assert
    assert not are_equal


def test_stack_token_not_equal_extra():
    """
    Test to make sure two StackToken instances with a different extra data are not equal.
    """

    # Arrange
    token1 = StackToken("type1", extra_data="extra1")
    token2 = StackToken("type1", extra_data="extra2")

    # Act
    are_equal = token1 == token2

    # Assert
    assert not are_equal


def test_stack_token_not_equal_not_same_type():
    """
    Test to make sure a StackToken instance is not equal to a non-StackToken.
    """

    # Arrange
    token1 = StackToken("type1", extra_data="extra1")
    caught_exception = None

    # Act
    try:
        _ = token1 == 1
    except AssertionError as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception
