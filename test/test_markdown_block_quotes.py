"""
https://github.github.com/gfm/#block-quotes
"""
import pytest

from .utils import act_and_assert

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_block_quotes_206x():
    """
    Test case 206:  Here is a simple example:
    """

    # Arrange
    source_markdown = """> # Foo
> bar
> baz"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[atx(1,3):1:0:]",
        "[text(1,5):Foo: ]",
        "[end-atx::]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_206a():
    """
    Test case 206:  Here is a simple example:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_206b():
    """
    Test case 206:  Here is a simple example:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_206c():
    """
    Test case 206:  Here is a simple example:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_207():
    """
    Test case 207:  The spaces after the > characters can be omitted:
    """

    # Arrange
    source_markdown = """># Foo
>bar
> baz"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n> ]",
        "[atx(1,2):1:0:]",
        "[text(1,4):Foo: ]",
        "[end-atx::]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_208():
    """
    Test case 208:  (part 1) The > characters can be indented 1-3 spaces:
    """

    # Arrange
    source_markdown = """   > # Foo
   > bar
 > baz"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > \n > ]",
        "[atx(1,6):1:0:]",
        "[text(1,8):Foo: ]",
        "[end-atx::]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_209():
    """
    Test case 209:  Four spaces gives us a code block:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_210():
    """
    Test case 210:  The Laziness clause allows us to omit the > before paragraph continuation text:
    """

    # Arrange
    source_markdown = """> # Foo
> bar
baz"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[atx(1,3):1:0:]",
        "[text(1,5):Foo: ]",
        "[end-atx::]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_211():
    """
    Test case 211:  A block quote can contain some lazy and some non-lazy continuation lines:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_211a():
    """
    Test case 211a:  variations
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_211b():
    """
    Test case 211b:  variations
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_211c():
    """
    Test case 211c:  variations
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_212():
    """
    Test case 212:  Laziness only applies to lines that would have been continuations of paragraphs had they been prepended with block quote markers.
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_212a():
    """
    Test case 212a:  variation
    """

    # Arrange
    source_markdown = """> foo
> ---"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[setext(2,3):-:3::(1,3)]",
        "[text(1,3):foo:]",
        "[end-setext::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h2>foo</h2>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_212b():
    """
    Test case 212b:  variation
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_212c():
    """
    Test case 212c:  variation
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_213():
    """
    Test case 213:  then the block quote ends after the first line:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_213ax():
    """
    Test case 213a:  variation
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_213aa():
    """
    Test case 213aa:  variation
    """

    # Arrange
    source_markdown = """> - foo
>   - boo
> - bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):-::4:  ]",
        "[para(1,5):]",
        "[text(1,5):foo:]",
        "[end-para:::True]",
        "[ulist(2,5):-::6:    ]",
        "[para(2,7):]",
        "[text(2,7):boo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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
<ul>
<li>boo</li>
</ul>
</li>
<li>bar</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_213ab():
    """
    Test case 213ab:  variation
    """

    # Arrange
    source_markdown = """- foo
  - boo
- bar"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):boo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(3,1):2::]",
        "[para(3,3):]",
        "[text(3,3):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>boo</li>
</ul>
</li>
<li>bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_213b():
    """
    Test case 213b:  variation
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_213c():
    """
    Test case 213b:  variation
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_213d():
    """
    Test case 213d:  variation
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_block_quotes_214():
    """
    Test case 214:  (part 1) For the same reason, we can’t omit the > in front of subsequent lines of an indented or fenced code block:
    Variation: - test_paragraph_series_n_bq_i4_t_nl_bq_i4_t
                 - proper indent and block quotes on both
               - test_paragraph_series_n_bq_i4_t_nl_bq_i3_t
                 - same as above, but second line with 1 less ws
               - test_paragraph_series_n_bq_i4_t_nl_bq_nl_bq_i4_t
                 - over multiple lines, each starting with block quote
               - test_paragraph_series_n_bq_i4_t_nl_nl_bq_i4_t
                 - over multiple lines, blank lines without block quote
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_215():
    """
    Test case 215:  (part 2) For the same reason, we can’t omit the > in front of subsequent lines of an indented or fenced code block:

    Variation: - test_paragraph_series_n_bq_t_nl_bq_fb
                 - for the entire block to be considered a fcb, all must be prefaced
                   with ">"
               - test_paragraph_series_n_bq_t_nl_bq_fb_nl_with_bq
                 - for any blank lines within block to not abort block quotes, must
                   prefix ">"
               - test_paragraph_series_n_bq_t_nl_bq_fb_nl_without_bq
                 - same as above, but lack of ">" causes block to be split up
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_216():
    """
    Test case 216:  Note that in the following case, we have a lazy continuation line:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_216a():
    """
    Test case 216a:  variation
    """

    # Arrange
    source_markdown = """> foo
>    - bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[ulist(2,6):-::7:     ]",
        "[para(2,8):]",
        "[text(2,8):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
<ul>
<li>bar</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_217():
    """
    Test case 217:  (part 1) A block quote can be empty:
    """

    # Arrange
    source_markdown = """>"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_218():
    """
    Test case 218:  (part 2) A block quote can be empty:
    """

    # Arrange
    source_markdown = """>
>\a\a
> """.replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[BLANK(2,3): ]",
        "[BLANK(3,3):]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_219():
    """
    Test case 219:  A block quote can have initial or final blank lines:
    """

    # Arrange
    source_markdown = """>
> foo
>  """
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[para(2,3):]",
        "[text(2,3):foo:]",
        "[end-para:::True]",
        "[BLANK(3,3): ]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_220():
    """
    Test case 220:  A blank line always separates block quotes:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_221():
    """
    Test case 221:  Consecutiveness means that if we put these block quotes together, we get a single block quote:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_222():
    """
    Test case 222:  To get a block quote with two paragraphs, use:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_222a():
    """
    Test case 222a:  To get a block quote with two paragraphs, use:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_222b():
    """
    Test case 222a:  To get a block quote with two paragraphs, use:
    """

    # Arrange
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
        "[BLANK(2,3): ]",
        "[para(3,3):]",
        "[text(3,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>foo</p>
<p>bar</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_222c():
    """
    Test case 222a:  To get a block quote with two paragraphs, use:
    """

    # Arrange
    source_markdown = """> foo
>
>
> bar"""
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_223():
    """
    Test case 223:  Block quotes can interrupt paragraphs:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_224():
    """
    Test case 224:  In general, blank lines are not needed before or after block quotes:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_225():
    """
    Test case 225:  (part 1) However, because of laziness, a blank line is needed between a block quote and a following paragraph:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_226():
    """
    Test case 226:  (part 2) However, because of laziness, a blank line is needed between a block quote and a following paragraph:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_227():
    """
    Test case 227:  (part 3) However, because of laziness, a blank line is needed between a block quote and a following paragraph:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_228():
    """
    Test case 228:  (part 1) It is a consequence of the Laziness rule that any number of initial >s may be omitted on a continuation line of a nested block quote:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229():
    """
    Test case 229:  (part 2) It is a consequence of the Laziness rule that any number of initial >s may be omitted on a continuation line of a nested block quote:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229a():
    """
    Test case 229a:  variation
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229b():
    """
    Test case 229b:  variation
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229cx():
    """
    Test case 229b:  variation
    """

    # Arrange
    source_markdown = """>     1
>>     2
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[icode-block(1,7):    :]",
        "[text(1,7):1:]",
        "[end-icode-block:::True]",
        "[block-quote(2,1)::>> \n]",
        "[icode-block(2,8):    :]",
        "[text(2,8):2:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<pre><code>1
</code></pre>
<blockquote>
<pre><code>2
</code></pre>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229ca():
    """
    Test case 229b:  variation
    """

    # Arrange
    source_markdown = """>     1
>>>     2
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[icode-block(1,7):    :]",
        "[text(1,7):1:]",
        "[end-icode-block:::True]",
        "[block-quote(2,1)::]",
        "[block-quote(2,2)::>>> \n]",
        "[icode-block(2,9):    :]",
        "[text(2,9):2:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<pre><code>1
</code></pre>
<blockquote>
<blockquote>
<pre><code>2
</code></pre>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229dx():
    """
    Test case 229d:  variation
    """

    # Arrange
    source_markdown = """>>     1
>     2
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[block-quote(1,2)::>> ]",
        "[icode-block(1,8):    :]",
        "[text(1,8):1:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,7):    :]",
        "[text(2,7):2:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>1
</code></pre>
</blockquote>
<pre><code>2
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229da():
    """
    Test case 229d:  variation
    """

    # Arrange
    source_markdown = """>>>     1
>     2
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[block-quote(1,2)::]",
        "[block-quote(1,3)::>>> ]",
        "[icode-block(1,9):    :]",
        "[text(1,9):1:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,7):    :]",
        "[text(2,7):2:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<pre><code>1
</code></pre>
</blockquote>
</blockquote>
<pre><code>2
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229ex():
    """
    Test case 229d:  variation
    """

    # Arrange
    source_markdown = """> ```
>> 2
>> ```
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n>\n]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,2):\a>\a&gt;\a 2\n\a>\a&gt;\a ```:]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt; 2
&gt; ```
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229ea():
    """
    Test case 229d:  variation
    """

    # Arrange
    source_markdown = """> ```
>>> 2
>>> ```
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n>\n]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,2):\a>\a&gt;\a\a>\a&gt;\a 2\n\a>\a&gt;\a\a>\a&gt;\a ```:]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt;&gt; 2
&gt;&gt; ```
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229fx():
    """
    Test case 229e:  variation
    """

    # Arrange
    source_markdown = """> ```
> 2
>> ```
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,3):2\n\a>\a&gt;\a ```:]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<pre><code>2
&gt; ```
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229fa():
    """
    Test case 229e:  variation
    """

    # Arrange
    source_markdown = """> ```
> 2
>>> ```
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,3):2\n\a>\a&gt;\a\a>\a&gt;\a ```:]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<pre><code>2
&gt;&gt; ```
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229gx():
    """
    Test case 229f:  variation
    """

    # Arrange
    source_markdown = """>> ```
> 2
> ```
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[block-quote(1,2)::>> ]",
        "[fcode-block(1,4):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,3):]",
        "[text(2,3):2:]",
        "[end-para:::False]",
        "[fcode-block(3,3):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code></code></pre>
</blockquote>
<p>2</p>
<pre><code></code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229ga():
    """
    Test case 229f:  variation
    """

    # Arrange
    source_markdown = """>>> ```
> 2
> ```
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[block-quote(1,2)::]",
        "[block-quote(1,3)::>>> ]",
        "[fcode-block(1,5):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[para(2,3):]",
        "[text(2,3):2:]",
        "[end-para:::False]",
        "[fcode-block(3,3):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<pre><code></code></pre>
</blockquote>
</blockquote>
<p>2</p>
<pre><code></code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229hx():
    """
    Test case 229g:  variation
    """

    # Arrange
    source_markdown = """>> ```
>> 2
> ```
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[block-quote(1,2)::>> \n>> ]",
        "[fcode-block(1,4):`:3::::::]",
        "[text(2,4):2:]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,3):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<pre><code>2
</code></pre>
</blockquote>
<pre><code></code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229ha():
    """
    Test case 229g:  variation
    """

    # Arrange
    source_markdown = """>>> ```
>>> 2
> ```
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[block-quote(1,2)::]",
        "[block-quote(1,3)::>>> \n>>> ]",
        "[fcode-block(1,5):`:3::::::]",
        "[text(2,5):2:]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,3):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<pre><code>2
</code></pre>
</blockquote>
</blockquote>
<pre><code></code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229ix():
    """
    Test case 229g:  variation
    """

    # Arrange
    source_markdown = """> <script>
> comments
>> </script>
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n]",
        "[html-block(1,3)]",
        "[text(1,3):<script>\ncomments\n> </script>:]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<script>
comments
> </script>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229ia():
    """
    Test case 229ia:  variation
    """

    # Arrange
    source_markdown = """> <script>
> comments
>>> </script>
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n]",
        "[html-block(1,3)]",
        "[text(1,3):<script>\ncomments\n>> </script>:]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<script>
comments
>> </script>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229jx():
    """
    Test case 229j:  variation
    """

    # Arrange
    source_markdown = """>> <script>
>> comments
> </script>
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[block-quote(1,2)::>> \n>> ]",
        "[html-block(1,4)]",
        "[text(1,4):<script>\ncomments:]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
        "[html-block(3,3)]",
        "[text(3,3):</script>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<script>
comments
</blockquote>
</script>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_229ja():
    """
    Test case 229j:  variation
    """

    # Arrange
    source_markdown = """>>> <script>
>>> comments
> </script>
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[block-quote(1,2)::]",
        "[block-quote(1,3)::>>> \n>>> ]",
        "[html-block(1,5)]",
        "[text(1,5):<script>\ncomments:]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[html-block(3,3)]",
        "[text(3,3):</script>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<script>
comments
</blockquote>
</blockquote>
</script>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_230():
    """
    Test case 230:  When including an indented code block in a block quote, remember that the block quote marker includes both the > and a following space. So five spaces are needed after the >:
    """

    # Arrange
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_01():
    """
    Test case Bq01:  Indents should work properly for a list block containing a
                     block quote where the block quote ends and there is
                     more data for that item within the list
    """

    # Arrange
    source_markdown = """* start
  > quote
* end"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):start:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(3,1):2::]",
        "[para(3,3):]",
        "[text(3,3):end:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>start
<blockquote>
<p>quote</p>
</blockquote>
</li>
<li>end</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_01a():
    """
    Test case Bq01a:  same as 01, just more levels of list
    """

    # Arrange
    source_markdown = """* start
  > quote
  * middle
    > middle
      quote
  * more middle
* end"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):start:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(3,3):*::4:  :    ]",
        "[para(3,5):]",
        "[text(3,5):middle:]",
        "[end-para:::True]",
        "[block-quote(4,5):    :    > \n    ]",
        "[para(4,7):\n  ]",
        "[text(4,7):middle\nquote::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(6,3):4:  :]",
        "[para(6,5):]",
        "[text(6,5):more middle:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(7,1):2::]",
        "[para(7,3):]",
        "[text(7,3):end:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>start
<blockquote>
<p>quote</p>
</blockquote>
<ul>
<li>middle
<blockquote>
<p>middle
quote</p>
</blockquote>
</li>
<li>more middle</li>
</ul>
</li>
<li>end</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_02x():
    """
    Test case Bq02:  Indents should work properly for a block quote containing a
                     list block where the list block ends and there is
                     more data for that block quote within the list
    """

    # Arrange
    source_markdown = """> start
> - quote
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):start:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):\n]",
        "[text(2,5):quote\nend::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>start</p>
<ul>
<li>quote
end</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_02ax():
    """
    Test case Bq02a:  variant
    """

    # Arrange
    source_markdown = """> start
> - quote
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> ]",
        "[para(1,3):]",
        "[text(1,3):start:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):quote:]",
        "[end-para:::True]",
        "[end-ulist:::False]",
        "[BLANK(3,2):]",
        "[para(4,3):]",
        "[text(4,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>start</p>
<ul>
<li>quote</li>
</ul>
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_02aa():
    """
    Test case Bq02aa:  variant
    """

    # Arrange
    source_markdown = """- quote

end"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):quote:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[end-ulist:::True]",
        "[para(3,1):]",
        "[text(3,1):end:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ul>
<li>quote</li>
</ul>
<p>end</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_02ab():
    """
    Test case Bq02ab:  variant
    """

    # Arrange
    source_markdown = """> - start
> quote
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> ]",
        "[ulist(1,3):-::4:  ]",
        "[para(1,5):\n]",
        "[text(1,5):start\nquote::\n]",
        "[end-para:::True]",
        "[end-ulist:::False]",
        "[BLANK(3,2):]",
        "[para(4,3):]",
        "[text(4,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>start
quote</li>
</ul>
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_02ac():
    """
    Test case Bq02ac:  variant
    """

    # Arrange
    source_markdown = """> - start
> - quote
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> ]",
        "[ulist(1,3):-::4:  ]",
        "[para(1,5):]",
        "[text(1,5):start:]",
        "[end-para:::True]",
        "[li(2,3):4:  :]",
        "[para(2,5):]",
        "[text(2,5):quote:]",
        "[end-para:::True]",
        "[end-ulist:::False]",
        "[BLANK(3,2):]",
        "[para(4,3):]",
        "[text(4,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>start</li>
<li>quote</li>
</ul>
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_02ad():
    """
    Test case Bq02ad:  variant
    """

    # Arrange
    source_markdown = """> - start
>   - quote
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> ]",
        "[ulist(1,3):-::4:  ]",
        "[para(1,5):]",
        "[text(1,5):start:]",
        "[end-para:::True]",
        "[ulist(2,5):-::6:    ]",
        "[para(2,7):]",
        "[text(2,7):quote:]",
        "[end-para:::True]",
        "[end-ulist:::False]",
        "[end-ulist:::False]",
        "[BLANK(3,2):]",
        "[para(4,3):]",
        "[text(4,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>start
<ul>
<li>quote</li>
</ul>
</li>
</ul>
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_02ae():
    """
    Test case Bq02ad:  variant
    """

    # Arrange
    source_markdown = """> - start
> - quote
>
>   end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> ]",
        "[ulist(1,3):-::4:  ]",
        "[para(1,5):]",
        "[text(1,5):start:]",
        "[end-para:::True]",
        "[li(2,3):4:  :]",
        "[para(2,5):]",
        "[text(2,5):quote:]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[para(4,5):  ]",
        "[text(4,5):end:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>start</p>
</li>
<li>
<p>quote</p>
<p>end</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        disable_consistency_checks=True,
        show_debug=True,
    )


@pytest.mark.gfm
def test_block_quotes_extra_03x():
    """
    Test case Bq03:  link definition within a block quote
                     copy of test_link_reference_definitions_161 but within single block
    """

    # Arrange
    source_markdown = """> [foo]: /url "title"
>
> [foo]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> ]",
        '[link-ref-def(1,3):True::foo:: :/url:: :title:"title":]',
        "[BLANK(2,2):]",
        "[para(3,3):]",
        "[link(3,3):shortcut:/url:title::::foo:::::]",
        "[text(3,4):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><a href="/url" title="title">foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_03xa():
    """
    Test case Bq03:  link definition within a block quote
                     copy of test_link_reference_definitions_161 but within single block
    """

    # Arrange
    source_markdown = """>
> [foo]: /url "title"
>
> [foo]"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n>\n> ]",
        "[BLANK(1,2):]",
        '[link-ref-def(2,3):True::foo:: :/url:: :title:"title":]',
        "[BLANK(3,2):]",
        "[para(4,3):]",
        "[link(4,3):shortcut:/url:title::::foo:::::]",
        "[text(4,4):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><a href="/url" title="title">foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_03xb():
    """
    Test case Bq03:  link definition within a block quote
                     copy of test_link_reference_definitions_161 but within single block
    """

    # Arrange
    source_markdown = """> abc
>
> [foo]: /url "title"
>
> [foo]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n>\n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        '[link-ref-def(3,3):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,2):]",
        "[para(5,3):]",
        "[link(5,3):shortcut:/url:title::::foo:::::]",
        "[text(5,4):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<p><a href="/url" title="title">foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_03a():
    """
    Test case Bq03a:  link definition within a block quote
                      copy of test_link_reference_definitions_161 but within
                      two distinct blocks
    """

    # Arrange
    source_markdown = """> [foo]: /url "title"

> [foo]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        '[link-ref-def(1,3):True::foo:: :/url:: :title:"title":]',
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[link(3,3):shortcut:/url:title::::foo:::::]",
        "[text(3,4):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<blockquote>
<p><a href="/url" title="title">foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_03aa():
    """
    Test case Bq03a:  link definition within a block quote
                      copy of test_link_reference_definitions_161 but within
                      two distinct blocks
    """

    # Arrange
    source_markdown = """> [foo]: /url "title"
> [foo]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        '[link-ref-def(1,3):True::foo:: :/url:: :title:"title":]',
        "[para(2,3):]",
        "[link(2,3):shortcut:/url:title::::foo:::::]",
        "[text(2,4):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><a href="/url" title="title">foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_03ab():
    """
    Test case Bq03a:  link definition within a block quote
                      copy of test_link_reference_definitions_161 but within
                      two distinct blocks
    """

    # Arrange
    source_markdown = """> abc

> [foo]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[:]",
        "[text(3,4):foo:]",
        "[text(3,7):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<blockquote>
<p>[foo]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_03b():
    """
    Test case Bq03a:  link definition within a block quote
                      copy of test_link_reference_definitions_164 but within
                      a single block
    """

    # Arrange
    source_markdown = """> [Foo bar]:
> <my url>
> 'title'
>
> [Foo bar]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> ]",
        "[link-ref-def(1,3):True::foo bar:Foo bar:\n:my%20url:<my url>:\n:title:'title':]",
        "[BLANK(4,2):]",
        "[para(5,3):]",
        "[link(5,3):shortcut:my%20url:title::::Foo bar:::::]",
        "[text(5,4):Foo bar:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><a href="my%20url" title="title">Foo bar</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_03ba():
    """
    Test case Bq03a:  link definition within a block quote
                      copy of test_link_reference_definitions_164 but within
                      a single block
    """

    # Arrange
    source_markdown = """> [Foo bar]:
> <my url>
> 'my
> title'
>
> [Foo bar]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> ]",
        "[link-ref-def(1,3):True::foo bar:Foo bar:\n:my%20url:<my url>:\n:my\ntitle:'my\ntitle':]",
        "[BLANK(5,2):]",
        "[para(6,3):]",
        "[link(6,3):shortcut:my%20url:my\ntitle::::Foo bar:::::]",
        "[text(6,4):Foo bar:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><a href="my%20url" title="my
title">Foo bar</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_03bb():
    """
    Test case Bq03a:  link definition within a block quote
                      copy of test_link_reference_definitions_164 but within
                      a single block
    """

    # Arrange
    source_markdown = """> [Foo
> bar]:
> <my url>
> 'my
> title'
>
> [Foo
> bar]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> \n> ]",
        "[link-ref-def(1,3):True::foo bar:Foo\nbar:\n:my%20url:<my url>:\n:my\ntitle:'my\ntitle':]",
        "[BLANK(6,2):]",
        "[para(7,3):\n]",
        "[link(7,3):shortcut:my%20url:my\ntitle::::Foo\nbar:::::]",
        "[text(7,4):Foo\nbar::\n]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><a href="my%20url" title="my
title">Foo
bar</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_04():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """> start
> quote
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> ]",
        "[para(1,3):\n]",
        "[text(1,3):start\nquote::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[para(4,3):]",
        "[text(4,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>start
quote</p>
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_04a():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """> start
> *the* quote
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> ]",
        "[para(1,3):\n]",
        "[text(1,3):start\n::\n]",
        "[emphasis(2,1):1:*]",
        "[text(2,2):the:]",
        "[end-emphasis(2,5)::]",
        "[text(2,6): quote:]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[para(4,3):]",
        "[text(4,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>start
<em>the</em> quote</p>
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_04b():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """> start
> *the* quote
> ---
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> ]",
        "[setext(3,3):-:3::(1,3)]",
        "[text(1,3):start\n::\n]",
        "[emphasis(2,1):1:*]",
        "[text(2,2):the:]",
        "[end-emphasis(2,5)::]",
        "[text(2,6): quote:]",
        "[end-setext::]",
        "[BLANK(4,2):]",
        "[para(5,3):]",
        "[text(5,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h2>start
<em>the</em> quote</h2>
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_04c():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """> ```
> start
> *the* quote
> ```
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,3):start\n*the* quote:]",
        "[end-fcode-block::3:False]",
        "[BLANK(5,2):]",
        "[para(6,3):]",
        "[text(6,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>start
*the* quote
</code></pre>
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_04d():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """>     start
>     *the* quote
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> ]",
        "[icode-block(1,7):    :\n    ]",
        "[text(1,7):start\n*the* quote:]",
        "[end-icode-block:::False]",
        "[BLANK(3,2):]",
        "[para(4,3):]",
        "[text(4,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>start
*the* quote
</code></pre>
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_04e():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """> <!--
> script
> -->
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> ]",
        "[html-block(1,3)]",
        "[text(1,3):<!--\nscript\n-->:]",
        "[end-html-block:::False]",
        "[BLANK(4,2):]",
        "[para(5,3):]",
        "[text(5,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<!--
script
-->
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_04f():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """> [
> abc
> ](/uri)
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> ]",
        "[para(1,3):\n\n]",
        "[link(1,3):inline:/uri:::::\nabc\n:False::::]",
        "[text(1,4):\nabc\n::\n\n]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[para(5,3):]",
        "[text(5,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><a href="/uri">
abc
</a></p>
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_04g():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """> ![
> abc
> ](/uri)
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> ]",
        "[para(1,3):\n\n]",
        "[image(1,3):inline:/uri::\nabc\n::::\nabc\n:False::::]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[para(5,3):]",
        "[text(5,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><img src="/uri" alt="
abc
" /></p>
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_04h():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """> a <html
> is="1">
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> ]",
        "[para(1,3):\n]",
        "[text(1,3):a :]",
        '[raw-html(1,5):html\nis="1"]',
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[para(4,3):]",
        "[text(4,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>a <html
is="1"></p>
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_04j():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """> a``html
> maybe``
>
> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> ]",
        "[para(1,3):\n]",
        "[text(1,3):a:]",
        "[icode-span(1,4):html\a\n\a \amaybe:``::]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[para(4,3):]",
        "[text(4,3):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>a<code>html maybe</code></p>
<p>end</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_05x():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """>> start
>> - quote
> end"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::>> \n>> \n> ]",
        "[para(1,4):]",
        "[text(1,4):start:]",
        "[end-para:::True]",
        "[ulist(2,4):-::5:   ]",
        "[para(2,6):\n]",
        "[text(2,6):quote\nend::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>start</p>
<ul>
<li>quote
end</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_05xa():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """>>> start
>>> - quote
> end"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::]",
        "[block-quote(1,3)::>>> \n>>> \n> ]",
        "[para(1,5):]",
        "[text(1,5):start:]",
        "[end-para:::True]",
        "[ulist(2,5):-::6:    ]",
        "[para(2,7):\n]",
        "[text(2,7):quote\nend::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>start</p>
<ul>
<li>quote
end</li>
</ul>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_05a():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """> start
> - quote
>> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):]",
        "[text(1,3):start:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):quote:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::>> ]",
        "[para(3,4):]",
        "[text(3,4):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>start</p>
<ul>
<li>quote</li>
</ul>
<blockquote>
<p>end</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_block_quotes_extra_05aa():
    """
    Test case Bq04:  variant
    """

    # Arrange
    source_markdown = """> start
> - quote
>>> end"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):]",
        "[text(1,3):start:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):quote:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::]",
        "[block-quote(3,2)::>>> ]",
        "[para(3,5):]",
        "[text(3,5):end:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>start</p>
<ul>
<li>quote</li>
</ul>
<blockquote>
<blockquote>
<p>end</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
