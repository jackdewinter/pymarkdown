"""
https://github.github.com/gfm/#paragraphs
"""
import pytest

from .utils import (
    act_and_assert
)


@pytest.mark.gfm
def test_paragraph_blocks_189():
    """
    Test case 189:  simple case of paragraphs
    """

    # Arrange
    source_markdown = """aaa

bbb"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):aaa:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):bbb:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aaa</p>
<p>bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_190():
    """
    Test case 189:  Paragraphs can contain multiple lines, but no blank lines:
    """

    # Arrange
    source_markdown = """aaa
bbb

ccc
ddd"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):aaa\nbbb::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):ccc\nddd::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aaa
bbb</p>
<p>ccc
ddd</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_190a():
    """
    Test case 189:  Paragraphs can contain multiple lines, but no blank lines:
    """

    # Arrange
    source_markdown = """aaa
bbb
ccc

ddd
eee
fff"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):aaa\nbbb\nccc::\n\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):\n\n]",
        "[text(5,1):ddd\neee\nfff::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aaa
bbb
ccc</p>
<p>ddd
eee
fff</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_191():
    """
    Test case 191:  Multiple blank lines between paragraph have no effect:
    """

    # Arrange
    source_markdown = """aaa


bbb"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):aaa:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):bbb:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aaa</p>
<p>bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_192():
    """
    Test case 192:  Leading spaces are skipped:
    """

    # Arrange
    source_markdown = """  aaa
 bbb"""
    expected_tokens = [
        "[para(1,3):  \n ]",
        "[text(1,3):aaa\nbbb::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aaa
bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_193():
    """
    Test case 193:  Lines after the first may be indented any amount, since indented code blocks cannot interrupt paragraphs.
    """

    # Arrange
    source_markdown = """aaa
             bbb
                                       ccc"""
    expected_tokens = [
        "[para(1,1):\n             \n                                       ]",
        "[text(1,1):aaa\nbbb\nccc::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aaa
bbb
ccc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_194():
    """
    Test case 194: (part a) However, the first line may be indented at most three spaces, or an indented code block will be triggered:
    """

    # Arrange
    source_markdown = """   aaa
bbb"""
    expected_tokens = [
        "[para(1,4):   \n]",
        "[text(1,4):aaa\nbbb::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aaa
bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_195():
    """
    Test case 195:  (part b) However, the first line may be indented at most three spaces, or an indented code block will be triggered:
    """

    # Arrange
    source_markdown = """    aaa
bbb"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):aaa:]",
        "[end-icode-block:::False]",
        "[para(2,1):]",
        "[text(2,1):bbb:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>aaa
</code></pre>
<p>bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_196x():
    """
    Test case 196:  Final spaces are stripped before inline parsing, so a paragraph that ends with two or more spaces will not end with a hard line break.
    """

    # Arrange
    source_markdown = """aaa\a\a\a\a\a
bbb     """.replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n:     ]",
        "[text(1,1):aaa:]",
        "[hard-break(1,4):     ]",
        "[text(2,1):\nbbb::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aaa<br />
bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_196a():
    """
    Test case 196a:  Modification of 196, but with tabs instead of space.
    """

    # Arrange
    source_markdown = """aaa\t\t\t\t\t
bbb\t\t\t\t\t"""
    expected_tokens = [
        "[para(1,1):\n:\t\t\t\t\t]",
        "[text(1,1):aaa:]",
        "[hard-break(1,4):                    ]",
        "[text(2,1):\nbbb::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aaa<br />
bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
