"""
https://github.github.com/gfm/#lists
"""
import pytest

from pymarkdown.tokens.markdown_token import (
    EndMarkdownToken,
    MarkdownToken,
    MarkdownTokenClass,
)
from pymarkdown.transform_gfm.transform_to_gfm import TransformToGfm


@pytest.mark.gfm
def test_gfm_bad_token():
    """
    Test to ensure that a bad markdown token asserts an error.
    """

    # Arrange
    transformer = TransformToGfm()
    tokens_to_test = [
        MarkdownToken("bad", MarkdownTokenClass.INLINE_BLOCK),
    ]

    # Act
    captured_exception = None
    try:
        transformer.transform(tokens_to_test)
        raise AssertionError("should have failed")
    except AssertionError as this_exception:
        captured_exception = this_exception

    # Assert
    assert (
        str(captured_exception)
        == "Markdown token type <class 'pymarkdown.tokens.markdown_token.MarkdownToken'> not supported."
    )


@pytest.mark.gfm
def test_gfm_bad_end_token():
    """
    Test to ensure that a bad markdown end token asserts an error.
    """

    # Arrange
    transformer = TransformToGfm()
    tokens_to_test = [
        EndMarkdownToken("bad", "", None, "hi", False),
    ]

    # Act
    captured_exception = None
    try:
        transformer.transform(tokens_to_test)
        raise AssertionError("should have failed")
    except AssertionError as this_exception:
        captured_exception = this_exception

    # Assert
    assert str(captured_exception) == "Markdown token end type bad not supported."
