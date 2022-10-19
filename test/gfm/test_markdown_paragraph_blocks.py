"""
https://github.github.com/gfm/#paragraphs
"""
from test.utils import act_and_assert

import pytest


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
    Test case 190a:  variation of 190 with extra lines
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
    Test case 193:  Lines after the first may be indented any amount, since indented
                    code blocks cannot interrupt paragraphs.
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
    Test case 194: (part a) However, the first line may be indented at most three
                    spaces, or an indented code block will be triggered:
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
    Test case 195:  (part b) However, the first line may be indented at most three
                    spaces, or an indented code block will be triggered:
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
    Test case 196:  Final spaces are stripped before inline parsing, so a paragraph
                    that ends with two or more spaces will not end with a hard line
                    break.
    """

    # Arrange
    source_markdown = """aaa\a\a\a\a\a
bbb     """.replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n:     ]",
        "[text(1,1):aaa:]",
        "[hard-break(1,4):     :\n]",
        "[text(2,1):bbb:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aaa<br />
bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_blocks_196a():
    """
    Test case 196a:  variation of 196, but with tabs instead of space.
    """

    # Arrange
    source_markdown = """aaa\t\t\t
bbb\t\t\t\t\t"""
    expected_tokens = [
        "[para(1,1):\n:\t\t\t\t\t]",
        "[text(1,1):aaa\nbbb::\t\t\t\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aaa\t\t\t
bbb</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_paragraph_blocks_196b():
    """
    Test case 196a:  variation of 196, but with tabs instead of spaces, and in a list
    """

    # Arrange
    source_markdown = """- aaa\t\t\t\t\t
  bbb\t\t\t"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n:\t\t\t]",
        "[text(1,3):aaa\nbbb::\t\t\t\t\t\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>aaa\t\t\t\t\t
bbb</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_paragraph_blocks_196c():
    """
    Test case 196a:  variation of 196, but with tabs instead of spaces, and in a list
    """

    # Arrange
    source_markdown = """- abc
  - aaa\t\t\t\t\t
    bbb\t\t\t\t\t"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :    ]",
        "[para(2,5):\n:\t\t\t\t\t]",
        "[text(2,5):aaa\nbbb::\t\t\t\t\t\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>aaa\t\t\t\t\t
bbb</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
def test_paragraph_blocks_196d():
    """
    Test case 196a:  variation of 196, but with tabs instead of spaces, and in a list
    """

    # Arrange
    source_markdown = """1. aaa\t\t\t\t\t
   bbb\t\t\t"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n:\t\t\t]",
        "[text(1,4):aaa\nbbb::\t\t\t\t\t\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>aaa\t\t\t\t\t
bbb</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        allow_alternate_markdown=False,
        show_debug=True,
    )


@pytest.mark.gfm
def test_paragraph_blocks_196e():
    """
    Test case 196a:  variation of 196, but with tabs instead of spaces, and in a list
    """

    # Arrange
    source_markdown = """1. abc
   1. aaa\t\t\t\t\t
      bbb\t\t\t\t\t"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :      ]",
        "[para(2,7):\n:\t\t\t\t\t]",
        "[text(2,7):aaa\nbbb::\t\t\t\t\t\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>aaa\t\t\t\t\t
bbb</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=False
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_paragraph_blocks_196f():
    """
    Test case 196a:  variation of 196, but with tabs instead of spaces, and in a list
    """

    # Arrange
    source_markdown = """- abc
  - def
\t- aaa\t\t\t\t\t
\t  bbb\t\t\t\t\t"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[ulist(3,5):-::6:    :      ]",
        "[para(3,7):\n:                   ]",
        "[text(3,7):aaa\nbbb::                   \n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>def
<ul>
<li>aaa\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a
bbb</li>
</ul>
</li>
</ul>
</li>
</ul>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        allow_alternate_markdown=False,
        show_debug=False,
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_paragraph_blocks_196g():
    """
    Test case 196a:  variation of 196, but with tabs instead of spaces, and in a list
    """

    # Arrange
    source_markdown = """- abc
  - def
\t - aaa\t\t\t\t\t
\t   bbb\t\t\t\t\t"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[ulist(3,6):-::7:     :       ]",
        "[para(3,8):\n:                  ]",
        "[text(3,8):aaa\nbbb::                  \n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>def
<ul>
<li>aaa\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a
bbb</li>
</ul>
</li>
</ul>
</li>
</ul>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        allow_alternate_markdown=False,
        show_debug=False,
    )
