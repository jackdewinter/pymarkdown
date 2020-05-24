"""
https://github.github.com/gfm/#precedence
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_tabs_001():
    """
    Test case 001:  (part a) a tab can be used instead of four spaces in an indented code block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\tfoo\tbaz\t\tbim"""
    expected_tokens = [
        "[icode-block(1,2):    ]",
        "[text:foo\tbaz\t\tbim:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>foo\tbaz\t\tbim
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_002():
    """
    Test case 002:  (part b) a tab can be used instead of four spaces in an indented code block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  \tfoo\tbaz\t\tbim"""
    expected_tokens = [
        "[icode-block(1,4):    ]",
        "[text:foo\tbaz\t\tbim:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>foo\tbaz\t\tbim
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_002a():
    """
    Test case 002a:  002 with spaces instead of tabs
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """      foo    baz        bim"""
    expected_tokens = [
        "[icode-block(1,7):    ]",
        "[text:foo    baz        bim:  ]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>  foo    baz        bim
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_002b():
    """
    Test case 002b:  Variation of 002 tested against Babelmark
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    a simple
      indented code block
---
      a simple
      indented code block"""
    expected_tokens = [
        "[icode-block(1,5):    ]",
        "[text:a simple\n  indented code block:]",
        "[end-icode-block]",
        "[tbreak(3,1):-::---]",
        "[icode-block(4,7):    ]",
        "[text:a simple\n  indented code block:  ]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>a simple
  indented code block
</code></pre>
<hr />
<pre><code>  a simple
  indented code block
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_003():
    """
    Test case 003:  (part c) a tab can be used instead of four spaces in an indented code block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    a\ta
    ὐ\ta"""
    expected_tokens = [
        "[icode-block(1,5):    ]",
        "[text:a\ta\nὐ\ta:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>a\ta
ὐ\ta
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_004():
    """
    Test case 004:  (part a) a continuation paragraph of a list item is indented with a tab; this has exactly the same effect as indentation with four spaces would
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  - foo

\tbar"""  # noqa: E101,W191
    # noqa: E101,W191
    expected_tokens = [
        "[ulist:-::4:  ]",
        "[para(1,5):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,2):]",
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


@pytest.mark.gfm
def test_tabs_005():
    """
    Test case 005:  (part b) a continuation paragraph of a list item is indented with a tab; this has exactly the same effect as indentation with four spaces would
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo

\t\tbar"""  # noqa: E101,W191
    # noqa: E101,W191
    expected_tokens = [
        "[ulist:-::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[icode-block(3,3):    ]",
        "[text:bar:  ]",
        "[end-icode-block]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>foo</p>
<pre><code>  bar
</code></pre>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


# @pytest.mark.skip
@pytest.mark.gfm
def test_tabs_006():
    """
    Test case 006:  case > is followed by a tab, which is treated as if it were expanded into three spaces.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>\t\tfoo"""
    expected_tokens = [
        "[block-quote:]",
        "[icode-block(1,4):    ]",
        "[text:foo:  ]",
        "[end-icode-block]",
        "[end-block-quote]",
    ]
    expected_gfm = """<blockquote>
<pre><code>  foo
</code></pre>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_006a():
    """
    Test case 006a:  modified version of 006 with spaces leading in instead of tab
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>   \tfoo"""
    expected_tokens = [
        "[block-quote:]",
        "[icode-block(1,6):    ]",
        "[text:foo:  ]",
        "[end-icode-block]",
        "[end-block-quote]",
    ]
    expected_gfm = """<blockquote>
<pre><code>  foo
</code></pre>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_006b():
    """
    Test case 006b:  modified version of 006 with spaces leading in instead of tab
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>\t    foo"""
    expected_tokens = [
        "[block-quote:]",
        "[icode-block(1,7):    ]",
        "[text:foo:  ]",
        "[end-icode-block]",
        "[end-block-quote]",
    ]
    expected_gfm = """<blockquote>
<pre><code>  foo
</code></pre>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_006c():
    """
    Test case 006c:  modified version of 006 with spaces leading in instead of tab
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>       foo"""
    expected_tokens = [
        "[block-quote:]",
        "[icode-block(1,9):    ]",
        "[text:foo:  ]",
        "[end-icode-block]",
        "[end-block-quote]",
    ]
    expected_gfm = """<blockquote>
<pre><code>  foo
</code></pre>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_007():
    """
    Test case 007:  none
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """-\t\tfoo"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[icode-block(1,4):    ]",
        "[text:foo:  ]",
        "[end-icode-block]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>  foo
</code></pre>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_007a():
    """
    Test case 007a:  variation on 007 with ordered list
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1)\t\tfoo"""
    expected_tokens = [
        "[olist:):1:3:]",
        "[icode-block(1,5):    ]",
        "[text:foo: ]",
        "[end-icode-block]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code> foo
</code></pre>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_007b():
    """
    Test case 007b:  variation on 007 with ordered list
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """01)\t\tfoo"""
    expected_tokens = [
        "[olist:):01:4:]",
        "[icode-block(1,6):    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[end-olist]",
    ]
    expected_gfm = """<ol start="1">
<li>
<pre><code>foo
</code></pre>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_007c():
    """
    Test case 007c:  variation on 007 with ordered list
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """001)\t\tfoo"""
    expected_tokens = [
        "[olist:):001:5:]",
        "[icode-block(1,7):    ]",
        "[text:foo:   ]",
        "[end-icode-block]",
        "[end-olist]",
    ]
    expected_gfm = """<ol start="1">
<li>
<pre><code>   foo
</code></pre>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_008():
    """
    Test case 008:  none
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    foo
\tbar"""  # noqa: E101,W191
    # noqa: E101
    expected_tokens = [
        "[icode-block(1,5):    ]",
        "[text:foo\nbar:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>foo
bar
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_009():
    """
    Test case 009:  none
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ - foo
   - bar
\t - baz"""  # noqa: E101,W191
    # noqa: E101
    expected_tokens = [
        "[ulist:-::3: ]",
        "[para(1,4):]",
        "[text:foo:]",
        "[end-para]",
        "[ulist:-::5:   ]",
        "[para(2,6):]",
        "[text:bar:]",
        "[end-para]",
        "[ulist:-::7:\t ]",
        "[para(3,5):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar
<ul>
<li>baz</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_010():
    """
    Test case 010:  none
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """#\tFoo"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text:Foo:    ]", "[end-atx::]"]
    expected_gfm = """<h1>Foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_tabs_011():
    """
    Test case 011:  none
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*\t*\t*\t"""
    expected_tokens = ["[tbreak(1,1):*::*    *    *    ]"]
    expected_gfm = """<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
