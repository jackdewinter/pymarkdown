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
def test_paragraph_blocks_189():
    """
    Test case 189:  simple case of paragraphs
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """aaa

bbb"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:aaa:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:bbb:]",
        "[end-para]",
    ]
    expected_gfm = """<p>aaa</p>
<p>bbb</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_190():
    """
    Test case 189:  Paragraphs can contain multiple lines, but no blank lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """aaa
bbb

ccc
ddd"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text:aaa\nbbb::\n]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text:ccc\nddd::\n]",
        "[end-para]",
    ]
    expected_gfm = """<p>aaa
bbb</p>
<p>ccc
ddd</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_191():
    """
    Test case 191:  Multiple blank lines between paragraph have no effect:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """aaa


bbb"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:aaa:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text:bbb:]",
        "[end-para]",
    ]
    expected_gfm = """<p>aaa</p>
<p>bbb</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_192():
    """
    Test case 192:  Leading spaces are skipped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  aaa
 bbb"""
    expected_tokens = ["[para(1,3):  \n ]", "[text:aaa\nbbb::\n]", "[end-para]"]
    expected_gfm = """<p>aaa
bbb</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_193():
    """
    Test case 193:  Lines after the first may be indented any amount, since indented code blocks cannot interrupt paragraphs.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """aaa
             bbb
                                       ccc"""
    expected_tokens = [
        "[para(1,1):\n             \n                                       ]",
        "[text:aaa\nbbb\nccc::\n\n]",
        "[end-para]",
    ]
    expected_gfm = """<p>aaa
bbb
ccc</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_194():
    """
    Test case 194: (part a) However, the first line may be indented at most three spaces, or an indented code block will be triggered:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   aaa
bbb"""
    expected_tokens = ["[para(1,4):   \n]", "[text:aaa\nbbb::\n]", "[end-para]"]
    expected_gfm = """<p>aaa
bbb</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_195():
    """
    Test case 195:  (part b) However, the first line may be indented at most three spaces, or an indented code block will be triggered:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    aaa
bbb"""
    expected_tokens = [
        "[icode-block(1,5):    ]",
        "[text:aaa:]",
        "[end-icode-block]",
        "[para(2,1):]",
        "[text:bbb:]",
        "[end-para]",
    ]
    expected_gfm = """<pre><code>aaa
</code></pre>
<p>bbb</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_196():
    """
    Test case 196:  Final spaces are stripped before inline parsing, so a paragraph that ends with two or more spaces will not end with a hard line break.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """aaa\a\a\a\a\a
bbb     """.replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n:     ]",
        "[text:aaa:]",
        "[hard-break:     ]",
        "[text:\nbbb::\n]",
        "[end-para]",
    ]
    expected_gfm = """<p>aaa<br />
bbb</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_196a():
    """
    Test case 196a:  Modification of 196, but with tabs instead of space.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """aaa\t\t\t\t\t
bbb\t\t\t\t\t"""
    expected_tokens = [
        "[para(1,1):\n:\t\t\t\t\t]",
        "[text:aaa:]",
        "[hard-break:                    ]",
        "[text:\nbbb::\n]",
        "[end-para]",
    ]
    expected_gfm = """<p>aaa<br />
bbb</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
