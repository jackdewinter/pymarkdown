"""
https://github.github.com/gfm/#paragraphs
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


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
        "[BLANK:  ]",
        "[BLANK:]",
        "[para(3,1):]",
        "[text:aaa:]",
        "[end-para]",
        "[BLANK:  ]",
        "[BLANK:]",
        "[atx(6,1):1:0:]",
        "[text:aaa: ]",
        "[end-atx::]",
        "[BLANK:]",
        "[BLANK:  ]",
    ]
    expected_gfm = """<p>aaa</p>
<h1>aaa</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
