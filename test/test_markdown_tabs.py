"""
https://github.github.com/gfm/#precedence
"""
import pytest

from .utils import act_and_assert


@pytest.mark.gfm
def test_tabs_001():
    """
    Test case 001:  (part a) a tab can be used instead of four spaces in an indented code block.
    """

    # Arrange
    source_markdown = """\tfoo\tbaz\t\tbim"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):foo baz     bim:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>foo baz     bim
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_002():
    """
    Test case 002:  (part b) a tab can be used instead of four spaces in an indented code block.
    """

    # Arrange
    source_markdown = """  \tfoo\tbaz\t\tbim"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):foo baz     bim:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>foo baz     bim
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_002a():
    """
    Test case 002a:  variation on 002 with spaces instead of tabs
    """

    # Arrange
    source_markdown = """      foo    baz        bim"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):foo    baz        bim:  ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>  foo    baz        bim
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_002b():
    """
    Test case 002b:  variation of 002 tested against Babelmark
    """

    # Arrange
    source_markdown = """    a simple
      indented code block
---
      a simple
      indented code block"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):a simple\n  indented code block:]",
        "[end-icode-block:::False]",
        "[tbreak(3,1):-::---]",
        "[icode-block(4,5):    :\n    ]",
        "[text(4,5):a simple\n  indented code block:  ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>a simple
  indented code block
</code></pre>
<hr />
<pre><code>  a simple
  indented code block
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_003():
    """
    Test case 003:  (part c) a tab can be used instead of four spaces in an indented code block.
    """

    # Arrange
    source_markdown = """    a\ta
    ὐ\ta"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):a   a\nὐ   a:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>a   a
ὐ   a
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_004x():
    """
    Test case 004:  (part a) a continuation paragraph of a list item is indented
                    with a tab; this has exactly the same effect as indentation
                    with four spaces would
    """

    # Arrange
    source_markdown = """  - foo

\tbar"""  # noqa: E101,W191
    # noqa: E101,W191
    expected_tokens = [
        "[ulist(1,3):-::4:  :\n    ]",
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
def test_tabs_004a():
    """
    Test case 004a:  variation on 004 with spaces instead of tabs
    """

    # Arrange
    source_markdown = """  - foo

    bar"""  # noqa: E101,W191
    # noqa: E101,W191
    expected_tokens = [
        "[ulist(1,3):-::4:  :\n    ]",
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
def test_tabs_005():
    """
    Test case 005:  (part b) a continuation paragraph of a list item is indented
                    with a tab; this has exactly the same effect as indentation
                    with four spaces would
    """

    # Arrange
    source_markdown = """- foo

\t\tbar"""  # noqa: E101,W191
    # noqa: E101,W191
    expected_tokens = [
        "[ulist(1,1):-::2::\n  ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,7):    :]",
        "[text(3,7):bar:  ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>foo</p>
<pre><code>  bar
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_006x():
    """
    Test case 006:  case > is followed by a tab, which is treated as if it were expanded into three spaces.
    """

    # Arrange
    source_markdown = """>\t\tfoo"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[icode-block(1,7):    :]",
        "[text(1,7):foo:  ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>  foo
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_006a():
    """
    Test case 006a:  variation of 006 with spaces leading in instead of tab
    """

    # Arrange
    source_markdown = """>   \tfoo"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[icode-block(1,7):    :]",
        "[text(1,7):foo:  ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>  foo
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_006b():
    """
    Test case 006b:  variation of 006 with spaces leading in instead of tab
    """

    # Arrange
    source_markdown = """>\t    foo"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[icode-block(1,7):    :]",
        "[text(1,7):foo:  ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>  foo
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_006c():
    """
    Test case 006c:  variation of 006 with spaces leading in instead of tab
    """

    # Arrange
    source_markdown = """>       foo"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[icode-block(1,7):    :]",
        "[text(1,7):foo:  ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>  foo
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_007x():
    """
    Test case 007:  none
    """

    # Arrange
    source_markdown = """-\t\tfoo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[icode-block(1,7):    :]",
        "[text(1,7):foo:  ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>  foo
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_007a():
    """
    Test case 007a:  variation on 007 with ordered list
    """

    # Arrange
    source_markdown = """1)\t\tfoo"""
    expected_tokens = [
        "[olist(1,1):):1:3:]",
        "[icode-block(1,8):    :]",
        "[text(1,8):foo: ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code> foo
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_007b():
    """
    Test case 007b:  variation on 007 with ordered list
    """

    # Arrange
    source_markdown = """01)\t\tfoo"""
    expected_tokens = [
        "[olist(1,1):):01:4:]",
        "[icode-block(1,9):    :]",
        "[text(1,9):foo:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol start="1">
<li>
<pre><code>foo
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_007c():
    """
    Test case 007c:  variation on 007 with ordered list
    """

    # Arrange
    source_markdown = """001)\t\tfoo"""
    expected_tokens = [
        "[olist(1,1):):001:5:]",
        "[icode-block(1,10):    :]",
        "[text(1,10):foo:   ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol start="1">
<li>
<pre><code>   foo
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_008():
    """
    Test case 008:  none
    """

    # Arrange
    source_markdown = """    foo
\tbar"""  # noqa: E101,W191
    # noqa: E101
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):foo\nbar:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>foo
bar
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_009():
    """
    Test case 009:  none
    """

    # Arrange
    source_markdown = """ - foo
   - bar
\t - baz"""  # noqa: E101,W191
    # noqa: E101
    expected_tokens = [
        "[ulist(1,2):-::3: ]",
        "[para(1,4):]",
        "[text(1,4):foo:]",
        "[end-para:::True]",
        "[ulist(2,4):-::5:   ]",
        "[para(2,6):]",
        "[text(2,6):bar:]",
        "[end-para:::True]",
        "[ulist(3,6):-::7:     ]",
        "[para(3,8):]",
        "[text(3,8):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_010():
    """
    Test case 010:  none
    """

    # Arrange
    source_markdown = """#\tFoo"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,5):Foo:   ]", "[end-atx::]"]
    expected_gfm = """<h1>Foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tabs_011():
    """
    Test case 011:  none
    """

    # Arrange
    source_markdown = """*\t*\t*\t"""
    expected_tokens = ["[tbreak(1,1):*::*   *   *   ]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
