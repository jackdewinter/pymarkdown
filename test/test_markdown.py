"""
https://github.github.com/gfm/#paragraphs
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown


# pylint: disable=trailing-whitespace
def test_paragraph_blocks_197():
    """
    Test case 197:  Blank lines at the beginning and end of the document are also ignored.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """  

aaa
  

# aaa

  """
    expected_tokens = [
        "[BLANK:  ]",
        "[BLANK:]",
        "[para:]",
        "[text:aaa:]",
        "[end-para]",
        "[BLANK:  ]",
        "[BLANK:]",
        "[para:]",
        "[text:# aaa:]",
        "[end-para]",
        "[BLANK:]",
        "[BLANK:  ]",
    ]

    # Act
    actual_html = tokenizer.transform(source_markdown)

    # Assert
    print("expected_tokens:" + str(expected_tokens))
    print("actual_html:" + str(actual_html))
    # TODO Expect this to fail when headers are implemented
    assert expected_tokens == actual_html
