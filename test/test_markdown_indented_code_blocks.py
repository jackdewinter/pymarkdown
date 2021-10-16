"""
https://github.github.com/gfm/#indented-code-blocks
"""
import pytest

from .utils import act_and_assert


@pytest.mark.gfm
def test_indented_code_blocks_077():
    """
    Test case 077:  Simple examples:
    """

    # Arrange
    source_markdown = """    a simple
      indented code block"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):a simple\n  indented code block:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>a simple
  indented code block
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_078():
    """
    Test case 078:  (part a) If there is any ambiguity between an interpretation of indentation as a code block and as indicating that material belongs to a list item, the list item interpretation takes precedence:
    """

    # Arrange
    source_markdown = """  - foo

    bar"""
    expected_tokens = [
        "[ulist(1,3):-::4:  :    ]",
        "[para(1,5):]",
        "[text(1,5):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,5):]",
        "[text(3,5):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>foo</p>
<p>bar</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_079():
    """
    Test case 079:  (part b) If there is any ambiguity between an interpretation of indentation as a code block and as indicating that material belongs to a list item, the list item interpretation takes precedence:
    """

    # Arrange
    source_markdown = """1.  foo

    - bar"""
    expected_tokens = [
        "[olist(1,1):.:1:4:]",
        "[para(1,5):]",
        "[text(1,5):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[ulist(3,5):-::6:    ]",
        "[para(3,7):]",
        "[text(3,7):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<p>foo</p>
<ul>
<li>bar</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_080():
    """
    Test case 080:  The contents of a code block are literal text, and do not get parsed as Markdown:
    """

    # Arrange
    source_markdown = """    <a/>
    *hi*

    - one"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    \n\n    ]",
        "[text(1,5):\a<\a&lt;\aa/\a>\a&gt;\a\n*hi*\n\x03\n- one:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&lt;a/&gt;
*hi*

- one
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_081():
    """
    Test case 081:  Here we have three chunks separated by blank lines:
    """

    # Arrange
    source_markdown = """    chunk1

    chunk2
  
 
 
    chunk3"""
    expected_tokens = [
        "[icode-block(1,5):    :\n\n    \n  \n \n \n    ]",
        "[text(1,5):chunk1\n\x03\nchunk2\n\x03\n\x03\n\x03\nchunk3:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>chunk1

chunk2



chunk3
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_082():
    """
    Test case 082:  Any initial spaces beyond four will be included in the content, even in interior blank lines:
    """

    # Arrange
    source_markdown = """    chunk1
\a\a\a\a\a\a
      chunk2""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[icode-block(1,5):    :\n    \n    ]",
        "[text(1,5):chunk1\n\x03  \n  chunk2:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>chunk1
  
  chunk2
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_082a():
    """
    Test case 082a:  variation of 82 with just enough indentation on second line
    """

    # Arrange
    source_markdown = """    chunk1
\a\a\a\a
      chunk2""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[icode-block(1,5):    :\n    \n    ]",
        "[text(1,5):chunk1\n\x03\n  chunk2:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>chunk1

  chunk2
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_083():
    """
    Test case 083:  An indented code block cannot interrupt a paragraph. (This allows hanging indents and the like.)
    """

    # Arrange
    source_markdown = """Foo
    bar"""
    expected_tokens = [
        "[para(1,1):\n    ]",
        "[text(1,1):Foo\nbar::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo
bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_084():
    """
    Test case 084:  However, any non-blank line with fewer than four leading spaces ends the code block immediately. So a paragraph may occur immediately after indented code:
    """

    # Arrange
    source_markdown = """    foo
bar"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):foo:]",
        "[end-icode-block:::False]",
        "[para(2,1):]",
        "[text(2,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>foo
</code></pre>
<p>bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_084a():
    """
    Test case 084a:  Copied from 84 with extra lines inserted to verify trailing blanks are not part of section.
    """

    # Arrange
    source_markdown = """    foo


bar"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):foo:]",
        "[end-icode-block:::False]",
        "[BLANK(2,1):]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>foo
</code></pre>
<p>bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_085():
    """
    Test case 085:  And indented code can occur immediately before and after other kinds of blocks:
    """

    # Arrange
    source_markdown = """# Heading
    foo
Heading
------
    foo
----"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):Heading: ]",
        "[end-atx::]",
        "[icode-block(2,5):    :]",
        "[text(2,5):foo:]",
        "[end-icode-block:::False]",
        "[setext(4,1):-:6::(3,1)]",
        "[text(3,1):Heading:]",
        "[end-setext::]",
        "[icode-block(5,5):    :]",
        "[text(5,5):foo:]",
        "[end-icode-block:::False]",
        "[tbreak(6,1):-::----]",
    ]
    expected_gfm = """<h1>Heading</h1>
<pre><code>foo
</code></pre>
<h2>Heading</h2>
<pre><code>foo
</code></pre>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_086():
    """
    Test case 086:  The first line can be indented more than four spaces:
    """

    # Arrange
    source_markdown = """        foo
    bar"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):foo\nbar:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>    foo
bar
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_086a():
    """
    Test case 086a:  variation of 86 to include more spaces so extracted != left
    """

    # Arrange
    source_markdown = """         foo
    bar"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):foo\nbar:     ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>     foo
bar
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_086b():
    """
    Test case 086b:  variation of 86 to play around with spaces
    """

    # Arrange
    source_markdown = """    foo
         bar"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):foo\n     bar:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>foo
     bar
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_087():
    """
    Test case 087:  Blank lines preceding or following an indented code block are not included in it:
    """

    # Arrange
    source_markdown = """
    
    foo
    """
    expected_tokens = [
        "[BLANK(1,1):]",
        "[BLANK(2,1):    ]",
        "[icode-block(3,5):    :]",
        "[text(3,5):foo:]",
        "[end-icode-block:::True]",
        "[BLANK(4,1):    ]",
    ]
    expected_gfm = """<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_088():
    """
    Test case 088:  Trailing spaces are included in the code block’s content:
    """

    # Arrange
    source_markdown = """    foo  """
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):foo  :]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>foo\a\a
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
