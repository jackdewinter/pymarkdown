# pylint: disable=too-many-lines
"""
https://github.github.com/gfm/#lists
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
def test_list_blocks_231():
    """
    Test case 231:  If the list item is ordered, then it is also assigned a start number, based on the ordered list marker.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """A paragraph
with two lines.

    indented code

> A block quote."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text:A paragraph\nwith two lines.::\n]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[icode-block(4,5):    :]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK(5,1):]",
        "[block-quote(6,1):]",
        "[para(6,3):]",
        "[text:A block quote.:]",
        "[end-para]",
        "[end-block-quote]",
    ]
    expected_gfm = """<p>A paragraph
with two lines.</p>
<pre><code>indented code
</code></pre>
<blockquote>
<p>A block quote.</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_232():
    """
    Test case 232:  And let M be the marker 1., and N = 2. Then rule #1 says that the following is an ordered list item with start number 1, and the same contents as Ls:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.  A paragraph
    with two lines.

        indented code

    > A block quote."""
    expected_tokens = [
        "[olist(1,1):.:1:4::    \n    ]",
        "[para(1,5):\n]",
        "[text:A paragraph\nwith two lines.::\n]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[icode-block(4,9):    :]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK(5,1):]",
        "[block-quote(6,5):    ]",
        "[para(6,7):]",
        "[text:A block quote.:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>
<p>A paragraph
with two lines.</p>
<pre><code>indented code
</code></pre>
<blockquote>
<p>A block quote.</p>
</blockquote>
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
def test_list_blocks_233():
    """
    Test case 233:  (part 1) Here are some examples showing how far content must be indented to be put under the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- one

 two"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:one:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[end-ulist]",
        "[para(3,2): ]",
        "[text:two:]",
        "[end-para]",
    ]
    expected_gfm = """<ul>
<li>one</li>
</ul>
<p>two</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_234():
    """
    Test case 234:  (part 2) Here are some examples showing how far content must be indented to be put under the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- one

  two"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text:one:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,3):]",
        "[text:two:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>one</p>
<p>two</p>
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
def test_list_blocks_235():
    """
    Test case 235:  (part 3) Here are some examples showing how far content must be indented to be put under the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ -    one

     two"""
    expected_tokens = [
        "[ulist(1,2):-::6: ]",
        "[para(1,7):]",
        "[text:one:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[end-ulist]",
        "[icode-block(3,5):    :]",
        "[text:two: ]",
        "[end-icode-block]",
    ]
    expected_gfm = """<ul>
<li>one</li>
</ul>
<pre><code> two
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_236():
    """
    Test case 236:  (part 4) Here are some examples showing how far content must be indented to be put under the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ -    one

      two"""
    expected_tokens = [
        "[ulist(1,2):-::6: :      ]",
        "[para(1,7):]",
        "[text:one:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,7):]",
        "[text:two:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>one</p>
<p>two</p>
</li>
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
def test_list_blocks_237():
    """
    Test case 237:  The spaces after the list marker determine how much relative indentation is needed. Which column this indentation reaches will depend on how the list item is embedded in other constructions, as shown by this example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   > > 1.  one
>>
>>     two"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>
<p>one</p>
<p>two</p>
</li>
</ol>
</blockquote>
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
def test_list_blocks_238():
    """
    Test case 238:  The converse is also possible. In the following example, the word two occurs far to the right of the initial text of the list item, one, but it is not considered part of the list item, because it is not indented far enough past the blockquote marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """>>- one
>>
  >  > two"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>one</li>
</ul>
<p>two</p>
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
def test_list_blocks_239():
    """
    Test case 239:  Note that at least one space is needed between the list marker and any following content, so these are not list items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """-one

2.two"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:-one:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:2.two:]",
        "[end-para]",
    ]
    expected_gfm = """<p>-one</p>
<p>2.two</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_240():
    """
    Test case 240:  A list item may contain blocks that are separated by more than one blank line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo


  bar"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[BLANK(3,1):]",
        "[para(4,3):]",
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
def test_list_blocks_241():
    """
    Test case 241:  A list item may contain any kind of block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.  foo

    ```
    bar
    ```

    baz

    > bam"""
    expected_tokens = [
        "[olist(1,1):.:1:4::    \n    \n    \n    ]",
        "[para(1,5):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[fcode-block(3,5):`:3::::::]",
        "[text:bar:]",
        "[end-fcode-block::3]",
        "[BLANK(6,1):]",
        "[para(7,5):]",
        "[text:baz:]",
        "[end-para]",
        "[BLANK(8,1):]",
        "[block-quote(9,5):    ]",
        "[para(9,7):]",
        "[text:bam:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>
<p>foo</p>
<pre><code>bar
</code></pre>
<p>baz</p>
<blockquote>
<p>bam</p>
</blockquote>
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
def test_list_blocks_242():
    """
    Test case 242:  A list item that contains an indented code block will preserve empty lines within the code block verbatim.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- Foo

      bar


      baz"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[para(1,3):]",
        "[text:Foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[icode-block(3,7):    :\n\n\n    ]",
        "[text:bar\n\x03\n\x03\nbaz:]",
        "[end-icode-block]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>Foo</p>
<pre><code>bar


baz
</code></pre>
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
def test_list_blocks_243():
    """
    Test case 243:  (part 1) Note that ordered list start numbers must be nine digits or less:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """123456789. ok"""
    expected_tokens = [
        "[olist(1,1):.:123456789:11:]",
        "[para(1,12):]",
        "[text:ok:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol start="123456789">
<li>ok</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_244():
    """
    Test case 244:  (part 2) Note that ordered list start numbers must be nine digits or less:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1234567890. not ok"""
    expected_tokens = ["[para(1,1):]", "[text:1234567890. not ok:]", "[end-para]"]
    expected_gfm = """<p>1234567890. not ok</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_245():
    """
    Test case 245:  (part 1) A start number may begin with 0s:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """0. ok"""
    expected_tokens = [
        "[olist(1,1):.:0:3:]",
        "[para(1,4):]",
        "[text:ok:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol start="0">
<li>ok</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_246():
    """
    Test case 246:  (part 2) A start number may begin with 0s:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """003. ok"""
    expected_tokens = [
        "[olist(1,1):.:003:5:]",
        "[para(1,6):]",
        "[text:ok:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol start="3">
<li>ok</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_247():
    """
    Test case 247:  A start number may not be negative:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """-1. not ok"""
    expected_tokens = ["[para(1,1):]", "[text:-1. not ok:]", "[end-para]"]
    expected_gfm = """<p>-1. not ok</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_248():
    """
    Test case 248:  An indented code block will have to be indented four spaces beyond the edge of the region where text will be included in the list item. In the following case that is 6 spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo

      bar"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[icode-block(3,7):    :]",
        "[text:bar:]",
        "[end-icode-block]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>foo</p>
<pre><code>bar
</code></pre>
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
def test_list_blocks_248a():
    """
    Test case 248a:  mod'n
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo

     bar"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,6):   ]",
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
def test_list_blocks_249():
    """
    Test case 249:  And in this case it is 11 spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  10.  foo

           bar"""
    expected_tokens = [
        "[olist(1,3):.:10:7:  :       ]",
        "[para(1,8):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[icode-block(3,12):    :]",
        "[text:bar:]",
        "[end-icode-block]",
        "[end-olist]",
    ]
    expected_gfm = """<ol start="10">
<li>
<p>foo</p>
<pre><code>bar
</code></pre>
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
def test_list_blocks_250():
    """
    Test case 250:  (part 1) If the first block in the list item is an indented code block, then by rule #2, the contents must be indented one space after the list marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    indented code

paragraph

    more code"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:paragraph:]",
        "[end-para]",
        "[BLANK(4,1):]",
        "[icode-block(5,5):    :]",
        "[text:more code:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>indented code
</code></pre>
<p>paragraph</p>
<pre><code>more code
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_251():
    """
    Test case 251:  (part 2) If the first block in the list item is an indented code block, then by rule #2, the contents must be indented one space after the list marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.     indented code

   paragraph

       more code"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[icode-block(1,8):    :]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK(2,1):]",
        "[para(3,4):]",
        "[text:paragraph:]",
        "[end-para]",
        "[BLANK(4,1):]",
        "[icode-block(5,8):    :]",
        "[text:more code:]",
        "[end-icode-block]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>indented code
</code></pre>
<p>paragraph</p>
<pre><code>more code
</code></pre>
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
def test_list_blocks_252():
    """
    Test case 252:  (part 2) If the first block in the list item is an indented code block, then by rule #2, the contents must be indented one space after the list marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.      indented code

   paragraph

       more code"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[icode-block(1,8):    :]",
        "[text:indented code: ]",
        "[end-icode-block]",
        "[BLANK(2,1):]",
        "[para(3,4):]",
        "[text:paragraph:]",
        "[end-para]",
        "[BLANK(4,1):]",
        "[icode-block(5,8):    :]",
        "[text:more code:]",
        "[end-icode-block]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code> indented code
</code></pre>
<p>paragraph</p>
<pre><code>more code
</code></pre>
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
def test_list_blocks_253():
    """
    Test case 253:  (part 1) Note that rules #1 and #2 only apply to two cases: (a) cases in which the lines to be included in a list item begin with a non-whitespace character, and (b) cases in which they begin with an indented code block. In a case like the following, where the first block begins with a three-space indent, the rules do not allow us to form a list item by indenting the whole thing and prepending a list marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   foo

bar"""
    expected_tokens = [
        "[para(1,4):   ]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:bar:]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo</p>
<p>bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_254():
    """
    Test case 254:  (part 2) Note that rules #1 and #2 only apply to two cases: (a) cases in which the lines to be included in a list item begin with a non-whitespace character, and (b) cases in which they begin with an indented code block. In a case like the following, where the first block begins with a three-space indent, the rules do not allow us to form a list item by indenting the whole thing and prepending a list marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """-    foo

  bar"""
    expected_tokens = [
        "[ulist(1,1):-::5:]",
        "[para(1,6):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[end-ulist]",
        "[para(3,3):  ]",
        "[text:bar:]",
        "[end-para]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
</ul>
<p>bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_255():
    """
    Test case 255:  This is not a significant restriction, because when a block begins with 1-3 spaces indent, the indentation can always be removed without a change in interpretation, allowing rule #1 to be applied. So, in the above case:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """-  foo

   bar"""
    expected_tokens = [
        "[ulist(1,1):-::3::   ]",
        "[para(1,4):]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,4):]",
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
def test_list_blocks_256():
    """
    Test case 256:  Here are some list items that start with a blank line but are not empty:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """-
  foo
-
  ```
  bar
  ```
-
      baz"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  \n  ]",
        "[BLANK(1,2):]",
        "[para(2,3):]",
        "[text:foo:]",
        "[end-para]",
        "[li(3,1):2:]",
        "[BLANK(3,2):]",
        "[fcode-block(4,3):`:3::::::]",
        "[text:bar:]",
        "[end-fcode-block::3]",
        "[li(7,1):2:]",
        "[BLANK(7,2):]",
        "[icode-block(8,7):    :]",
        "[text:baz:]",
        "[end-icode-block]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
<li>
<pre><code>bar
</code></pre>
</li>
<li>
<pre><code>baz
</code></pre>
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
def test_list_blocks_257():
    """
    Test case 257:  When the list item starts with a blank line, the number of spaces following the list marker doesn’t change the required indentation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """-\a\a\a
  foo""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[BLANK(1,2):   ]",
        "[para(2,3):]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_257a():
    """
    Test case 257a:  Variation on 257
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """-
  foo"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[BLANK(1,2):]",
        "[para(2,3):]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_257b():
    """
    Test case 257b:  Variation on 257
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   foo"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[para(2,4):]",
        "[text:foo:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_258():
    """
    Test case 258:  A list item can begin with at most one blank line. In the following example, foo is not part of the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """-

  foo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[BLANK(1,2):]",
        "[end-ulist]",
        "[BLANK(2,1):]",
        "[para(3,3):  ]",
        "[text:foo:]",
        "[end-para]",
    ]
    expected_gfm = """<ul>
<li></li>
</ul>
<p>foo</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_259():
    """
    Test case 259:  Here is an empty bullet list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo
-
- bar"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[li(2,1):2:]",
        "[BLANK(2,2):]",
        "[li(3,1):2:]",
        "[para(3,3):]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
<li></li>
<li>bar</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_260():
    """
    Test case 260:  It does not matter whether there are spaces following the list marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo
-\a\a\a
- bar""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[li(2,1):2:]",
        "[BLANK(2,2):   ]",
        "[li(3,1):2:]",
        "[para(3,3):]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
<li></li>
<li>bar</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_261():
    """
    Test case 261:  Here is an empty ordered list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. foo
2.
3. bar"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text:foo:]",
        "[end-para]",
        "[li(2,1):3:]",
        "[BLANK(2,3):]",
        "[li(3,1):3:]",
        "[para(3,4):]",
        "[text:bar:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
<li></li>
<li>bar</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_262():
    """
    Test case 262:  A list may start or end with an empty list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*"""
    expected_tokens = ["[ulist(1,1):*::2:]", "[BLANK(1,2):]", "[end-ulist]"]
    expected_gfm = """<ul>
<li></li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_262a():
    """
    Test case 262a:  variation on 262
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1."""
    expected_tokens = ["[olist(1,1):.:1:3:]", "[BLANK(1,3):]", "[end-olist]"]
    expected_gfm = """<ol>
<li></li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_263():
    """
    Test case 263:  However, an empty list item cannot interrupt a paragraph:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo
*

foo
1."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text:foo\n::\n]",
        "[text:*:]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text:foo\n1.::\n]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo
*</p>
<p>foo
1.</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_264():
    """
    Test case 264:  Indented one space:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ 1.  A paragraph
     with two lines.

         indented code

     > A block quote."""
    expected_tokens = [
        "[olist(1,2):.:1:5: :     \n     ]",
        "[para(1,6):\n]",
        "[text:A paragraph\nwith two lines.::\n]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[icode-block(4,10):    :]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK(5,1):]",
        "[block-quote(6,6):     ]",
        "[para(6,8):]",
        "[text:A block quote.:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>
<p>A paragraph
with two lines.</p>
<pre><code>indented code
</code></pre>
<blockquote>
<p>A block quote.</p>
</blockquote>
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
def test_list_blocks_265():
    """
    Test case 265:  Indented two spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  1.  A paragraph
      with two lines.

          indented code

      > A block quote."""
    expected_tokens = [
        "[olist(1,3):.:1:6:  :      \n      ]",
        "[para(1,7):\n]",
        "[text:A paragraph\nwith two lines.::\n]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[icode-block(4,11):    :]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK(5,1):]",
        "[block-quote(6,7):      ]",
        "[para(6,9):]",
        "[text:A block quote.:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>
<p>A paragraph
with two lines.</p>
<pre><code>indented code
</code></pre>
<blockquote>
<p>A block quote.</p>
</blockquote>
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
def test_list_blocks_266():
    """
    Test case 266:  Indented three spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   1.  A paragraph
       with two lines.

           indented code

       > A block quote."""
    expected_tokens = [
        "[olist(1,4):.:1:7:   :       \n       ]",
        "[para(1,8):\n]",
        "[text:A paragraph\nwith two lines.::\n]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[icode-block(4,12):    :]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK(5,1):]",
        "[block-quote(6,8):       ]",
        "[para(6,10):]",
        "[text:A block quote.:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>
<p>A paragraph
with two lines.</p>
<pre><code>indented code
</code></pre>
<blockquote>
<p>A block quote.</p>
</blockquote>
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
def test_list_blocks_267():
    """
    Test case 267:  Four spaces indent gives a code block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    1.  A paragraph
        with two lines.

            indented code

        > A block quote."""
    expected_tokens = [
        "[icode-block(1,5):    :\n    \n\n    \n\n    ]",
        "[text:1.  A paragraph\n    with two lines.\n\x03\n        indented code\n\x03\n    \a>\a&gt;\a A block quote.:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>1.  A paragraph
    with two lines.

        indented code

    &gt; A block quote.
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_268():
    """
    Test case 268:  Here is an example with lazy continuation lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  1.  A paragraph
with two lines.

          indented code

      > A block quote."""
    expected_tokens = [
        "[olist(1,3):.:1:6:  :      ]",
        "[para(1,7):\n]",
        "[text:A paragraph\nwith two lines.::\n]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[icode-block(4,11):    :]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK(5,1):]",
        "[block-quote(6,7):      ]",
        "[para(6,9):]",
        "[text:A block quote.:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>
<p>A paragraph
with two lines.</p>
<pre><code>indented code
</code></pre>
<blockquote>
<p>A block quote.</p>
</blockquote>
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
def test_list_blocks_269():
    """
    Test case 269:  Indentation can be partially deleted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  1.  A paragraph
    with two lines."""
    expected_tokens = [
        "[olist(1,3):.:1:6:  :    ]",
        "[para(1,7):\n]",
        "[text:A paragraph\nwith two lines.::\n]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>A paragraph
with two lines.</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_269a():
    """
    Test case 269:  Variation on 269
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  1.  A paragraph
   with two lines."""
    expected_tokens = [
        "[olist(1,3):.:1:6:  ]",
        "[para(1,7):\n   ]",
        "[text:A paragraph\nwith two lines.::\n]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>A paragraph
with two lines.</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_269b():
    """
    Test case 269b:  Variation on 269
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  1.  A paragraph
     with two lines."""
    expected_tokens = [
        "[olist(1,3):.:1:6:  :    ]",
        "[para(1,7):\n ]",
        "[text:A paragraph\nwith two lines.::\n]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>A paragraph
with two lines.</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_list_blocks_270():
    """
    Test case 270:  (part 1) These examples show how laziness can work in nested structures:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> 1. > Blockquote
continued here."""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para(1,8):]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>Blockquote
continued here.</p>
</blockquote>
</li>
</ol>
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
def test_list_blocks_271():
    """
    Test case 271:  (part 2) These examples show how laziness can work in nested structures:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> 1. > Blockquote
> continued here."""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para(1,8):]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>Blockquote
continued here.</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_272():
    """
    Test case 272:  So, in this case we need two spaces indent:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo
  - bar
    - baz
      - boo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text:bar:]",
        "[end-para]",
        "[ulist(3,5):-::6:    ]",
        "[para(3,7):]",
        "[text:baz:]",
        "[end-para]",
        "[ulist(4,7):-::8:      ]",
        "[para(4,9):]",
        "[text:boo:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
        "[end-ulist]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar
<ul>
<li>baz
<ul>
<li>boo</li>
</ul>
</li>
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
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_273():
    """
    Test case 273:  One is not enough:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo
 - bar
  - baz
   - boo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[li(2,2):3: ]",
        "[para(2,4):]",
        "[text:bar:]",
        "[end-para]",
        "[li(3,3):4:  ]",
        "[para(3,5):]",
        "[text:baz:]",
        "[end-para]",
        "[li(4,4):5:   ]",
        "[para(4,6):]",
        "[text:boo:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
<li>bar</li>
<li>baz</li>
<li>boo</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_274():
    """
    Test case 274:  Here we need four, because the list marker is wider:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """10) foo
    - bar"""
    expected_tokens = [
        "[olist(1,1):):10:4:]",
        "[para(1,5):]",
        "[text:foo:]",
        "[end-para]",
        "[ulist(2,5):-::6:    ]",
        "[para(2,7):]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
        "[end-olist]",
    ]
    expected_gfm = """<ol start="10">
<li>foo
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
def test_list_blocks_274a():
    """
    Test case 274a:  modification for 274
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1) foo
   - bar
1. baz"""
    expected_tokens = [
        "[olist(1,1):):1:3:]",
        "[para(1,4):]",
        "[text:foo:]",
        "[end-para]",
        "[ulist(2,4):-::5:   ]",
        "[para(2,6):]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
        "[end-olist]",
        "[olist(3,1):.:1:3:]",
        "[para(3,4):]",
        "[text:baz:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>foo
<ul>
<li>bar</li>
</ul>
</li>
</ol>
<ol>
<li>baz</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_274b():
    """
    Test case 274b:  modification for 274
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1) foo
   - bar
- baz"""
    expected_tokens = [
        "[olist(1,1):):1:3:]",
        "[para(1,4):]",
        "[text:foo:]",
        "[end-para]",
        "[ulist(2,4):-::5:   ]",
        "[para(2,6):]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
        "[end-olist]",
        "[ulist(3,1):-::2:]",
        "[para(3,3):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ol>
<li>foo
<ul>
<li>bar</li>
</ul>
</li>
</ol>
<ul>
<li>baz</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_274c():
    """
    Test case 274c:  modification for 274
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- foo
  1) bar
1) baz"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text:foo:]",
        "[end-para]",
        "[olist(2,3):):1:5:  ]",
        "[para(2,6):]",
        "[text:bar:]",
        "[end-para]",
        "[end-olist]",
        "[end-ulist]",
        "[olist(3,1):):1:3:]",
        "[para(3,4):]",
        "[text:baz:]",
        "[end-para]",
        "[end-olist]",
    ]
    expected_gfm = """<ul>
<li>foo
<ol>
<li>bar</li>
</ol>
</li>
</ul>
<ol>
<li>baz</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_list_blocks_275():
    """
    Test case 275:  Three is not enough:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """10) foo
   - bar"""
    expected_tokens = [
        "[olist(1,1):):10:4:]",
        "[para(1,5):]",
        "[text:foo:]",
        "[end-para]",
        "[end-olist]",
        "[ulist(2,4):-::5:   ]",
        "[para(2,6):]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ol start="10">
<li>foo</li>
</ol>
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


@pytest.mark.gfm
def test_list_blocks_276():
    """
    Test case 276:  (part 1) A list may be the first block in a list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- - foo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[ulist(1,3):-::4:  ]",
        "[para(1,5):]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>foo</li>
</ul>
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
def test_list_blocks_277():
    """
    Test case 277:  (part 2) A list may be the first block in a list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. - 2. foo"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[ulist(1,4):-::5:   ]",
        "[olist(1,6):.:2:8:     ]",
        "[para(1,9):]",
        "[text:foo:]",
        "[end-para]",
        "[end-olist]",
        "[end-ulist]",
        "[end-olist]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<ol start="2">
<li>foo</li>
</ol>
</li>
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
def test_list_blocks_278():
    """
    Test case 278:  A list item can contain a heading:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- # Foo
- Bar
  ---
  baz"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[atx(1,3):1:0:]",
        "[text:Foo: ]",
        "[end-atx::]",
        "[li(2,1):2:]",
        "[setext(3,3):-:3::(2,3)]",
        "[text:Bar:]",
        "[end-setext::]",
        "[para(4,3):]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<h1>Foo</h1>
</li>
<li>
<h2>Bar</h2>
baz</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
