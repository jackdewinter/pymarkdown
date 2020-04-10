"""
https://github.github.com/gfm/#precedence
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_block_inline_precedence_012():
    """
    Test case 012:  Indicators of block structure always take precedence over indicators of inline structure.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- `one
- two`"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:`one:]",
        "[end-para]",
        "[li:2]",
        "[para:]",
        "[text:two`:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>`one</li>
<li>two`</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
