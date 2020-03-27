"""
Extra tests.
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_extra_001():
    """
    Test a totally blank input.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = ""
    expected_tokens = ["[BLANK:]"]
    expected_gfm = ""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_extra_002():
    """
    Test a blank input with only whitespace.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = "   "
    expected_tokens = ["[BLANK:   ]"]
    expected_gfm = ""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
