"""
https://github.github.com/gfm/#block-quotes
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


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
        "[block-quote:]",
        "[atx(1,3):1:0:]",
        "[text:Foo: ]",
        "[end-atx::]",
        "[para(2,3):\n]",
        "[text:bar\nbaz::\n]",
        "[end-para]",
        "[end-block-quote]",
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
        "[block-quote:]",
        "[atx(1,2):1:0:]",
        "[text:Foo: ]",
        "[end-atx::]",
        "[para(2,2):\n]",
        "[text:bar\nbaz::\n]",
        "[end-para]",
        "[end-block-quote]",
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
        "[block-quote:   ]",
        "[atx(1,6):1:0:]",
        "[text:Foo: ]",
        "[end-atx::]",
        "[para(2,6):\n]",
        "[text:bar\nbaz::\n]",
        "[end-para]",
        "[end-block-quote]",
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
        "[icode-block(1,5):    ]",
        "[text:&gt; # Foo\n&gt; bar\n&gt; baz:]",
        "[end-icode-block]",
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
        "[block-quote:]",
        "[atx(1,3):1:0:]",
        "[text:Foo: ]",
        "[end-atx::]",
        "[para(2,3):\n]",
        "[text:bar\nbaz::\n]",
        "[end-para]",
        "[end-block-quote]",
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
        "[block-quote:]",
        "[para(1,3):\n\n]",
        "[text:bar\nbaz\nfoo::\n\n]",
        "[end-para]",
        "[end-block-quote]",
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


@pytest.mark.gfm
def test_block_quotes_212():
    """
    Test case 212:  Laziness only applies to lines that would have been continuations of paragraphs had they been prepended with block quote markers.
    """
    # TODO add case with >

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
---"""
    expected_tokens = [
        "[block-quote:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[end-block-quote]",
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


@pytest.mark.gfm
def test_block_quotes_213():
    """
    Test case 213:  then the block quote ends after the first line:
    """
    # TODO add case with >

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> - foo
- bar"""
    expected_tokens = [
        "[block-quote:]",
        "[ulist:-::4:  ]",
        "[para(1,5):]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
        "[end-block-quote]",
        "[ulist:-::2:]",
        "[para(2,3):]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
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


@pytest.mark.gfm
def test_block_quotes_214():
    """
    Test case 214:  (part 1) For the same reason, we can’t omit the > in front of subsequent lines of an indented or fenced code block:
    """
    # TODO add case with >

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>     foo
    bar"""
    expected_tokens = [
        "[block-quote:]",
        "[icode-block(1,7):    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[end-block-quote]",
        "[icode-block(2,5):    ]",
        "[text:bar:]",
        "[end-icode-block]",
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


@pytest.mark.gfm
def test_block_quotes_215():
    """
    Test case 215:  (part 2) For the same reason, we can’t omit the > in front of subsequent lines of an indented or fenced code block:
    """
    # TODO add case with >

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> ```
foo
```"""
    expected_tokens = [
        "[block-quote:]",
        "[fcode-block(1,3):`:3::::]",
        "[end-fcode-block]",
        "[end-block-quote]",
        "[para(2,1):]",
        "[text:foo:]",
        "[end-para]",
        "[fcode-block(3,1):`:3::::]",
        "[end-fcode-block]",
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


@pytest.mark.gfm
def test_block_quotes_216():
    """
    Test case 216:  Note that in the following case, we have a lazy continuation line:
    """
    # TODO add case with > to show same

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> foo
    - bar"""
    expected_tokens = [
        "[block-quote:]",
        "[para(1,3):\n    ]",
        "[text:foo\n- bar::\n]",
        "[end-para]",
        "[end-block-quote]",
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


@pytest.mark.gfm
def test_block_quotes_217():
    """
    Test case 217:  (part 1) A block quote can be empty:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>"""
    expected_tokens = ["[block-quote:]", "[BLANK:]", "[end-block-quote]"]
    expected_gfm = """<blockquote>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[block-quote:]",
        "[BLANK:]",
        "[BLANK: ]",
        "[BLANK:]",
        "[BLANK:]",
        "[end-block-quote]",
    ]
    expected_gfm = """<blockquote>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[block-quote:]",
        "[BLANK:]",
        "[para(2,3):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK: ]",
        "[BLANK:]",
        "[end-block-quote]",
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
        "[block-quote:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[end-block-quote]",
        "[BLANK:]",
        "[block-quote:]",
        "[para(3,3):]",
        "[text:bar:]",
        "[end-para]",
        "[end-block-quote]",
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
        "[block-quote:]",
        "[para(1,3):\n]",
        "[text:foo\nbar::\n]",
        "[end-para]",
        "[end-block-quote]",
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
        "[block-quote:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
        "[para(3,3):]",
        "[text:bar:]",
        "[end-para]",
        "[end-block-quote]",
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
        "[text:foo:]",
        "[end-para]",
        "[block-quote:]",
        "[para(2,3):]",
        "[text:bar:]",
        "[end-para]",
        "[end-block-quote]",
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
        "[block-quote:]",
        "[para(1,3):]",
        "[text:aaa:]",
        "[end-para]",
        "[end-block-quote]",
        "[tbreak(2,1):*::***]",
        "[block-quote:]",
        "[para(3,3):]",
        "[text:bbb:]",
        "[end-para]",
        "[end-block-quote]",
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
        "[block-quote:]",
        "[para(1,3):\n]",
        "[text:bar\nbaz::\n]",
        "[end-para]",
        "[end-block-quote]",
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
        "[block-quote:]",
        "[para(1,3):]",
        "[text:bar:]",
        "[end-para]",
        "[end-block-quote]",
        "[BLANK:]",
        "[para(3,1):]",
        "[text:baz:]",
        "[end-para]",
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
        "[block-quote:]",
        "[para(1,3):]",
        "[text:bar:]",
        "[end-para]",
        "[BLANK:]",
        "[end-block-quote]",
        "[para(3,1):]",
        "[text:baz:]",
        "[end-para]",
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
        "[block-quote:]",
        "[block-quote:]",
        "[block-quote:]",
        "[para(1,7):\n]",
        "[text:foo\nbar::\n]",
        "[end-para]",
        "[end-block-quote]",
        "[end-block-quote]",
        "[end-block-quote]",
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
        "[block-quote:]",
        "[block-quote:]",
        "[block-quote:]",
        "[para(1,5):\n\n]",
        "[text:foo\nbar\nbaz::\n\n]",
        "[end-para]",
        "[end-block-quote]",
        "[end-block-quote]",
        "[end-block-quote]",
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
        "[block-quote:]",
        "[icode-block(1,7):    ]",
        "[text:code:]",
        "[end-icode-block]",
        "[end-block-quote]",
        "[BLANK:]",
        "[block-quote:]",
        "[para(3,6):   ]",
        "[text:not code:]",
        "[end-para]",
        "[end-block-quote]",
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
