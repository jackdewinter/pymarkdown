"""
https://github.github.com/gfm/#indented-code-blocks
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
def test_indented_code_blocks_077():
    """
    Test case 077:  Simple examples:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    a simple
      indented code block"""
    expected_tokens = [
        "[icode-block(1,5):    ]",
        "[text:a simple\n  indented code block:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>a simple
  indented code block
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_078():
    """
    Test case 078:  (part a) If there is any ambiguity between an interpretation of indentation as a code block and as indicating that material belongs to a list item, the list item interpretation takes precedence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  - foo

    bar"""
    expected_tokens = [
        "[ulist(1,3):-::4:  ]",
        "[para(1,5):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,5):]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>foo</p>
<p>bar</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_079():
    """
    Test case 079:  (part b) If there is any ambiguity between an interpretation of indentation as a code block and as indicating that material belongs to a list item, the list item interpretation takes precedence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.  foo

    - bar"""
    expected_tokens = [
        "[olist(1,1):.:1:4:]",
        "[para(1,5):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[ulist(3,5):-::6:    ]",
        "[para(3,7):]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>
<p>foo</p>
<ul>
<li>bar</li>
</ul>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_080():
    """
    Test case 080:  The contents of a code block are literal text, and do not get parsed as Markdown:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    <a/>
    *hi*

    - one"""
    expected_tokens = [
        "[icode-block(1,5):    ]",
        "[text:&lt;a/&gt;\n*hi*\n\n- one:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>&lt;a/&gt;
*hi*

- one
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_081():
    """
    Test case 081:  Here we have three chunks separated by blank lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    chunk1

    chunk2
  
 
 
    chunk3"""
    expected_tokens = [
        "[icode-block(1,5):    ]",
        "[text:chunk1\n\nchunk2\n\n\n\nchunk3:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>chunk1

chunk2



chunk3
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_082():
    """
    Test case 082:  Any initial spaces beyond four will be included in the content, even in interior blank lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    chunk1
      
      chunk2"""
    expected_tokens = [
        "[icode-block(1,5):    ]",
        "[text:chunk1\n  \n  chunk2:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>chunk1
  
  chunk2
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_083():
    """
    Test case 083:  An indented code block cannot interrupt a paragraph. (This allows hanging indents and the like.)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
    bar"""
    expected_tokens = ["[para(1,1):\n    ]", "[text:Foo\nbar::\n]", "[end-para]"]
    expected_gfm = """<p>Foo
bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_084():
    """
    Test case 084:  However, any non-blank line with fewer than four leading spaces ends the code block immediately. So a paragraph may occur immediately after indented code:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    foo
bar"""
    expected_tokens = [
        "[icode-block(1,5):    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[para(2,1):]",
        "[text:bar:]",
        "[end-para]",
    ]
    expected_gfm = """<pre><code>foo
</code></pre>
<p>bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_084a():
    """
    ADDED:
    Test case 084a:  Copied from 84 with extra lines inserted to verify trailing blanks are not part of section.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    foo


bar"""
    expected_tokens = [
        "[icode-block(1,5):    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[BLANK(3,1):]",
        "[BLANK(2,1):]",
        "[para(4,1):]",
        "[text:bar:]",
        "[end-para]",
    ]
    expected_gfm = """<pre><code>foo
</code></pre>
<p>bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_085():
    """
    Test case 085:  And indented code can occur immediately before and after other kinds of blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """# Heading
    foo
Heading
------
    foo
----"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text:Heading: ]",
        "[end-atx::]",
        "[icode-block(2,5):    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[setext(4,1):-::(3,1)]",
        "[text:Heading:]",
        "[end-setext::]",
        "[icode-block(5,5):    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[tbreak(6,1):-::----]",
    ]
    expected_gfm = """<h1>Heading</h1>
<pre><code>foo
</code></pre>
<h2>Heading</h2>
<pre><code>foo
</code></pre>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_086():
    """
    Test case 086:  The first line can be indented more than four spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """        foo
    bar"""
    expected_tokens = [
        "[icode-block(1,9):    ]",
        "[text:foo\nbar:    ]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>    foo
bar
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_087():
    """
    Test case 087:  Blank lines preceding or following an indented code block are not included in it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """
    
    foo
    """
    expected_tokens = [
        "[BLANK(1,1):]",
        "[BLANK(2,1):    ]",
        "[icode-block(3,5):    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[BLANK(4,1):    ]",
    ]
    expected_gfm = """<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_indented_code_blocks_088():
    """
    Test case 088:  Trailing spaces are included in the code block’s content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    foo  """
    expected_tokens = ["[icode-block(1,5):    ]", "[text:foo  :]", "[end-icode-block]"]
    expected_gfm = """<pre><code>foo\a\a
</code></pre>""".replace(
        "\a", " "
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
