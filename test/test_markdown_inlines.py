"""
https://github.github.com/gfm/#inlines
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_inlines_307():
    """
    Test case 307:  Thus, for example, in
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """`hi`lo`"""
    expected_tokens = ["[para(1,1):]", "[icode-span:hi]", "[text:lo`:]", "[end-para]"]
    expected_gfm = """<p><code>hi</code>lo`</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
