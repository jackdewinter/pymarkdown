"""
https://github.github.com/gfm/#lists
"""
from test.utils import act_and_assert, assert_that_exception_is_raised

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

    expected_output = "Markdown token type <class 'pymarkdown.tokens.markdown_token.MarkdownToken'> not supported."

    # Act & Assert
    assert_that_exception_is_raised(
        AssertionError, expected_output, transformer.transform, tokens_to_test
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
    expected_output = "Markdown token end type bad not supported."

    # Act & Assert
    assert_that_exception_is_raised(
        AssertionError, expected_output, transformer.transform, tokens_to_test
    )


@pytest.mark.gfm
def test_do_add_end_of_stream_token():
    """
    Test to...

    This function shadows test_atx_headings_033.
    """

    # Arrange
    source_markdown = """####### foo"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):####### foo:]",
        "[end-para:::True]",
        "[end-of-stream(2,0)]",
    ]
    expected_gfm = """<p>####### foo</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, do_add_end_of_stream_token=True
    )
