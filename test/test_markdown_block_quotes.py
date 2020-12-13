"""
https://github.github.com/gfm/#block-quotes
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    assert_if_lists_different,
    assert_if_strings_different,
    assert_token_consistency,
)

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_block_quotes_206():
    """
    Test case 206:  Here is a simple example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> # Foo
> bar
> baz"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[atx(1,3):1:0:]",
        "[text(1,5):Foo: ]",
        "[end-atx:::False]",
        "[para(2,3):\n]",
        "[text(2,3):bar\nbaz::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h1>Foo</h1>
<p>bar
baz</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_206a():
    """
    Test case 206:  Here is a simple example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> Foo
> bar
> baz"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):\n\n]",
        "[text(1,3):Foo\nbar\nbaz::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>Foo
bar
baz</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_206b():
    """
    Test case 206:  Here is a simple example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> Foo
bar
baz"""
    expected_tokens = [
        "[block-quote(1,1)::> \n\n]",
        "[para(1,3):\n\n]",
        "[text(1,3):Foo\nbar\nbaz::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>Foo
bar
baz</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_206c():
    """
    Test case 206:  Here is a simple example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> Foo
 bar
  baz
   bofo"""
    expected_tokens = [
        "[block-quote(1,1)::> \n\n\n]",
        "[para(1,3):\n \n  \n   ]",
        "[text(1,3):Foo\nbar\nbaz\nbofo::\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>Foo
bar
baz
bofo</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_207():
    """
    Test case 207:  The spaces after the > characters can be omitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """># Foo
>bar
> baz"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n> ]",
        "[atx(1,2):1:0:]",
        "[text(1,4):Foo: ]",
        "[end-atx:::False]",
        "[para(2,2):\n]",
        "[text(2,2):bar\nbaz::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h1>Foo</h1>
<p>bar
baz</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_208():
    """
    Test case 208:  (part 1) The > characters can be indented 1-3 spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   > # Foo
   > bar
 > baz"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > \n > ]",
        "[atx(1,6):1:0:]",
        "[text(1,8):Foo: ]",
        "[end-atx:::False]",
        "[para(2,6):\n]",
        "[text(2,6):bar\nbaz::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h1>Foo</h1>
<p>bar
baz</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_209():
    """
    Test case 209:  Four spaces gives us a code block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    > # Foo
    > bar
    > baz"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    \n    ]",
        "[text(1,5):\a>\a&gt;\a # Foo\n\a>\a&gt;\a bar\n\a>\a&gt;\a baz:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt; # Foo
&gt; bar
&gt; baz
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_210():
    """
    Test case 210:  The Laziness clause allows us to omit the > before paragraph continuation text:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> # Foo
> bar
baz"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[atx(1,3):1:0:]",
        "[text(1,5):Foo: ]",
        "[end-atx:::False]",
        "[para(2,3):\n]",
        "[text(2,3):bar\nbaz::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h1>Foo</h1>
<p>bar
baz</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_211():
    """
    Test case 211:  A block quote can contain some lazy and some non-lazy continuation lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> bar
baz
> foo"""
    expected_tokens = [
        "[block-quote(1,1)::> \n\n> ]",
        "[para(1,3):\n\n]",
        "[text(1,3):bar\nbaz\nfoo::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>bar
baz
foo</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_211a():
    """
    Test case 211a:  variations
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> bar
> baz
> foo"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):\n\n]",
        "[text(1,3):bar\nbaz\nfoo::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>bar
baz
foo</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_211b():
    """
    Test case 211b:  variations
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> bar

> baz

> foo"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):]",
        "[text(1,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> \n]",
        "[para(3,3):]",
        "[text(3,3):baz:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[block-quote(5,1)::> ]",
        "[para(5,3):]",
        "[text(5,3):foo:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>bar</p>
</blockquote>
<blockquote>
<p>baz</p>
</blockquote>
<blockquote>
<p>foo</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_211c():
    """
    Test case 211c:  variations
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> bar
>
> baz
>
> foo"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n>\n> ]",
        "[para(1,3):]",
        "[text(1,3):bar:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[para(3,3):]",
        "[text(3,3):baz:]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[para(5,3):]",
        "[text(5,3):foo:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>bar</p>
<p>baz</p>
<p>foo</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_212():
    """
    Test case 212:  Laziness only applies to lines that would have been continuations of paragraphs had they been prepended with block quote markers.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
---"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[tbreak(2,1):-::---]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
</blockquote>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_212a():
    """
    Test case 212a:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
> ---"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[setext(2,3):-:3::(1,3)]",
        "[text(1,3):foo:]",
        "[end-setext:::False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h2>foo</h2>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_212b():
    """
    Test case 212b:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo

> ---"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> ]",
        "[tbreak(3,3):-::---]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
</blockquote>
<blockquote>
<hr />
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_212c():
    """
    Test case 212c:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
>
> ---"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[tbreak(3,3):-::---]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
<hr />
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_213():
    """
    Test case 213:  then the block quote ends after the first line:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> - foo
- bar"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):-::4:  ]",
        "[para(1,5):]",
        "[text(1,5):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[ulist(2,1):-::2:]",
        "[para(2,3):]",
        "[text(2,3):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>foo</li>
</ul>
</blockquote>
<ul>
<li>bar</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_block_quotes_213a():
    """
    Test case 213a:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> - foo
> - bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):-::4:  ]",
        "[para(1,5):]",
        "[text(1,5):foo:]",
        "[end-para:::True]",
        "[li(2,3):4:  :]",
        "[para(2,5):]",
        "[text(2,5):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>foo</li>
<li>bar</li>
</ul>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_block_quotes_213b():
    """
    Test case 213b:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> - foo
> - bar
> - bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):-::4:  ]",
        "[para(1,5):]",
        "[text(1,5):foo:]",
        "[end-para:::True]",
        "[li(2,3):4:  :]",
        "[para(2,5):]",
        "[text(2,5):bar:]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text(3,5):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>foo</li>
<li>bar</li>
<li>bar</li>
</ul>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_block_quotes_213c():
    """
    Test case 213b:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> - foo
    brr
> - bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):-::4:  :    ]",
        "[para(1,5):\n]",
        "[text(1,5):foo\nbrr::\n]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text(3,5):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>foo
brr</li>
<li>bar</li>
</ul>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_block_quotes_213d():
    """
    Test case 213d:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> - foo
>   brr
> - bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):-::4:  ]",
        "[para(1,5):\n  ]",
        "[text(1,5):foo\nbrr::\n]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text(3,5):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>foo
brr</li>
<li>bar</li>
</ul>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_214():
    """
    Test case 214:  (part 1) For the same reason, we can’t omit the > in front of subsequent lines of an indented or fenced code block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>     foo
    bar"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[icode-block(1,7):    :]",
        "[text(1,7):foo:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,5):    :]",
        "[text(2,5):bar:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>foo
</code></pre>
</blockquote>
<pre><code>bar
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_214a():
    """
    Test case 214a:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>     foo
>     bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[icode-block(1,7):    :\n    ]",
        "[text(1,7):foo\nbar:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>foo
bar
</code></pre>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_214b():
    """
    Test case 214b:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>     foo
>    bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[icode-block(1,7):    :]",
        "[text(1,7):foo:]",
        "[end-icode-block:::False]",
        "[para(2,6):   ]",
        "[text(2,6):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>foo
</code></pre>
<p>bar</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_214c():
    """
    Test case 214c:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>     foo

>     bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[icode-block(1,7):    :]",
        "[text(1,7):foo:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> ]",
        "[icode-block(3,7):    :]",
        "[text(3,7):bar:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>foo
</code></pre>
</blockquote>
<blockquote>
<pre><code>bar
</code></pre>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_214d():
    """
    Test case 214d:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>     foo
>
>     bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> ]",
        "[icode-block(1,7):    :\n\n    ]",
        "[text(1,7):foo\n\x03\nbar:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>foo

bar
</code></pre>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_215():
    """
    Test case 215:  (part 2) For the same reason, we can’t omit the > in front of subsequent lines of an indented or fenced code block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> ```
foo
```"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(3,1):`:3::::::]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code></code></pre>
</blockquote>
<p>foo</p>
<pre><code></code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_215a():
    """
    Test case 215a:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> ```
> foo
> ```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,3):foo:]",
        "[end-fcode-block::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>foo
</code></pre>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_215b():
    """
    Test case 215b:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> ```

> foo

> ```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[fcode-block(1,3):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> \n]",
        "[para(3,3):]",
        "[text(3,3):foo:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[block-quote(5,1)::> ]",
        "[fcode-block(5,3):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code></code></pre>
</blockquote>
<blockquote>
<p>foo</p>
</blockquote>
<blockquote>
<pre><code></code></pre>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_215c():
    """
    Test case 215c:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> ```
>
> foo
>
> ```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n>\n> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,2):\nfoo\n:]",
        "[end-fcode-block::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>
foo

</code></pre>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_216():
    """
    Test case 216:  Note that in the following case, we have a lazy continuation line:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
    - bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):\n    ]",
        "[text(1,3):foo\n- bar::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo
- bar</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_216a():
    """
    Test case 216a:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
>    - bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):\n   ]",
        "[text(1,3):foo\n- bar::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo
- bar</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_217():
    """
    Test case 217:  (part 1) A block quote can be empty:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_218():
    """
    Test case 218:  (part 2) A block quote can be empty:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>
>  
> """
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[BLANK(2,4): ]",
        "[BLANK(3,3):]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_219():
    """
    Test case 219:  A block quote can have initial or final blank lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>
> foo
>  """
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[para(2,3):]",
        "[text(2,3):foo:]",
        "[end-para:::True]",
        "[BLANK(3,4): ]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_220():
    """
    Test case 220:  A blank line always separates block quotes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo

> bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
</blockquote>
<blockquote>
<p>bar</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_221():
    """
    Test case 221:  Consecutiveness means that if we put these block quotes together, we get a single block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
> bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):\n]",
        "[text(1,3):foo\nbar::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo
bar</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_222():
    """
    Test case 222:  To get a block quote with two paragraphs, use:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
>
> bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[para(3,3):]",
        "[text(3,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
<p>bar</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_222a():
    """
    Test case 222a:  To get a block quote with two paragraphs, use:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
>\a
> bar""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[BLANK(2,3):]",
        "[para(3,3):]",
        "[text(3,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
<p>bar</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_222b():
    """
    Test case 222a:  To get a block quote with two paragraphs, use:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
>\a\a
> bar""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[BLANK(2,4): ]",
        "[para(3,3):]",
        "[text(3,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
<p>bar</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_222c():
    """
    Test case 222a:  To get a block quote with two paragraphs, use:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
>
>
> bar""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n>\n> ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[BLANK(3,2):]",
        "[para(4,3):]",
        "[text(4,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
<p>bar</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_223():
    """
    Test case 223:  Block quotes can interrupt paragraphs:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo
> bar"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> ]",
        "[para(2,3):]",
        "[text(2,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p>foo</p>
<blockquote>
<p>bar</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_224():
    """
    Test case 224:  In general, blank lines are not needed before or after block quotes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> aaa
***
> bbb"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):aaa:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[tbreak(2,1):*::***]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):bbb:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>aaa</p>
</blockquote>
<hr />
<blockquote>
<p>bbb</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_225():
    """
    Test case 225:  (part 1) However, because of laziness, a blank line is needed between a block quote and a following paragraph:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> bar
baz"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):\n]",
        "[text(1,3):bar\nbaz::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>bar
baz</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_226():
    """
    Test case 226:  (part 2) However, because of laziness, a blank line is needed between a block quote and a following paragraph:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> bar

baz"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):]",
        "[text(1,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):baz:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>bar</p>
</blockquote>
<p>baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_227():
    """
    Test case 227:  (part 3) However, because of laziness, a blank line is needed between a block quote and a following paragraph:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> bar
>
baz"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n]",
        "[para(1,3):]",
        "[text(1,3):bar:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[end-block-quote:::False]",
        "[para(3,1):]",
        "[text(3,1):baz:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>bar</p>
</blockquote>
<p>baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_228():
    """
    Test case 228:  (part 1) It is a consequence of the Laziness rule that any number of initial >s may be omitted on a continuation line of a nested block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> > > foo
bar"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > > \n]",
        "[para(1,7):\n]",
        "[text(1,7):foo\nbar::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>foo
bar</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_229():
    """
    Test case 229:  (part 2) It is a consequence of the Laziness rule that any number of initial >s may be omitted on a continuation line of a nested block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>>> foo
> bar
>>baz"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::]",
        "[block-quote(1,3)::>>> \n> \n>>]",
        "[para(1,5):\n\n]",
        "[text(1,5):foo\nbar\nbaz::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>foo
bar
baz</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_229a():
    """
    Test case 229a:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> 1
>> 2
> 1
>> > 3
> > 2
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):1:]",
        "[end-para:::True]",
        "[block-quote(2,1)::>> \n> ]",
        "[para(2,4):\n]",
        "[text(2,4):2\n1::\n]",
        "[end-para:::True]",
        "[block-quote(4,1)::>> > \n> > \n]",
        "[para(4,6):\n]",
        "[text(4,6):3\n2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<p>1</p>
<blockquote>
<p>2
1</p>
<blockquote>
<p>3
2</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_229b():
    """
    Test case 229b:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> 1

>> 2

> 1

>> > 3

> > 2
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):]",
        "[text(1,3):1:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::]",
        "[block-quote(3,2)::>> \n]",
        "[para(3,4):]",
        "[text(3,4):2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[block-quote(5,1)::> \n]",
        "[para(5,3):]",
        "[text(5,3):1:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[block-quote(7,1)::]",
        "[block-quote(7,2)::]",
        "[block-quote(7,4)::>> > \n]",
        "[para(7,6):]",
        "[text(7,6):3:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[block-quote(9,1)::]",
        "[block-quote(9,3)::> > \n]",
        "[para(9,5):]",
        "[text(9,5):2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<p>1</p>
</blockquote>
<blockquote>
<blockquote>
<p>2</p>
</blockquote>
</blockquote>
<blockquote>
<p>1</p>
</blockquote>
<blockquote>
<blockquote>
<blockquote>
<p>3</p>
</blockquote>
</blockquote>
</blockquote>
<blockquote>
<blockquote>
<p>2</p>
</blockquote>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_block_quotes_230():
    """
    Test case 230:  When including an indented code block in a block quote, remember that the block quote marker includes both the > and a following space. So five spaces are needed after the >:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>     code

>    not code"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[icode-block(1,7):    :]",
        "[text(1,7):code:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> ]",
        "[para(3,6):   ]",
        "[text(3,6):not code:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>code
</code></pre>
</blockquote>
<blockquote>
<p>not code</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
