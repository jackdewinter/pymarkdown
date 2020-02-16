"""
https://github.github.com/gfm/#paragraphs
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_paragraph_blocks_189():
    """
    Test case 189:  simple case of paragraphs
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """aaa

bbb"""
    expected_tokens = [
        "[para:]",
        "[text:aaa:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:bbb:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_paragraph_blocks_190():
    """
    Test case 189:  Paragraphs can contain multiple lines, but no blank lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """aaa
bbb

ccc
ddd"""
    expected_tokens = [
        "[para:\n]",
        "[text:aaa\nbbb:]",
        "[end-para]",
        "[BLANK:]",
        "[para:\n]",
        "[text:ccc\nddd:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_paragraph_blocks_191():
    """
    Test case 191:  Multiple blank lines between paragraph have no effect:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """aaa


bbb"""
    expected_tokens = [
        "[para:]",
        "[text:aaa:]",
        "[end-para]",
        "[BLANK:]",
        "[BLANK:]",
        "[para:]",
        "[text:bbb:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_paragraph_blocks_192():
    """
    Test case 192:  Leading spaces are skipped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """  aaa
 bbb"""
    expected_tokens = ["[para:  \n ]", "[text:aaa\nbbb:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_paragraph_blocks_193():
    """
    Test case 193:  Lines after the first may be indented any amount, since indented code blocks cannot interrupt paragraphs.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """aaa
             bbb
                                       ccc"""
    expected_tokens = [
        "[para:\n             \n                                       ]",
        "[text:aaa\nbbb\nccc:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_paragraph_blocks_194():
    """
    Test case 194: (part a) However, the first line may be indented at most three spaces, or an indented code block will be triggered:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """   aaa
bbb"""
    expected_tokens = ["[para:   \n]", "[text:aaa\nbbb:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_paragraph_blocks_195():
    """
    Test case 195:  (part b) However, the first line may be indented at most three spaces, or an indented code block will be triggered:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    aaa
bbb"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:aaa:]",
        "[end-icode-block]",
        "[para:]",
        "[text:bbb:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_paragraph_blocks_196():
    """
    Test case 196:  (part b) However, the first line may be indented at most three spaces, or an indented code block will be triggered:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """aaa\a\a\a\a\a
bbb     """.replace(
        "\a", " "
    )
    expected_tokens = ["[para:\n:     ]", "[text:aaa     \nbbb:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when hard line breaks is implemented
    assert_if_lists_different(expected_tokens, actual_tokens)
