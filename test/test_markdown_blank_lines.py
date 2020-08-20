"""
https://github.github.com/gfm/#paragraphs
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    assert_if_lists_different,
    assert_if_strings_different,
    assert_token_consistency,
)


@pytest.mark.gfm
def test_blank_lines_197():
    """
    Test case 197:  Blank lines at the beginning and end of the document are also ignored.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\a\a

aaa
\a\a

# aaa

  """.replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):  ]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:aaa:]",
        "[end-para:::True]",
        "[BLANK(4,1):  ]",
        "[BLANK(5,1):]",
        "[atx(6,1):1:0:]",
        "[text:aaa: ]",
        "[end-atx:::False]",
        "[BLANK(7,1):]",
        "[BLANK(8,1):  ]",
    ]
    expected_gfm = """<p>aaa</p>
<h1>aaa</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_blank_lines_197a():
    """
    Test case 197a:  Extra blanks to test
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\a\a
\a
aaa
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):  ]",
        "[BLANK(2,1): ]",
        "[para(3,1):]",
        "[text:aaa:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>aaa</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
