"""
https://github.github.com/gfm/#paragraphs
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_blank_lines_197():
    """
    Test case 197:  Blank lines at the beginning and end of the document are also ignored.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
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
        "[para:]",
        "[text:aaa:]",
        "[end-para]",
        "[BLANK:  ]",
        "[BLANK:]",
        "[atx:1:0:]",
        "[text:aaa: ]",
        "[end-atx::]",
        "[BLANK:]",
        "[BLANK:  ]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
