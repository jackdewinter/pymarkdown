# pylint: disable=too-many-lines
"""
https://github.github.com/gfm/#lists
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_list_blocks_231x():
    """
    Test case 231:  If the list item is ordered, then it is also assigned a start number, based on the ordered list marker.
    """

    # Arrange
    source_markdown = """A paragraph
with two lines.

    indented code

> A block quote."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[icode-block(4,5):    :]",
        "[text(4,5):indented code:]",
        "[end-icode-block:::True]",
        "[BLANK(5,1):]",
        "[block-quote(6,1)::> ]",
        "[para(6,3):]",
        "[text(6,3):A block quote.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p>A paragraph
with two lines.</p>
<pre><code>indented code
</code></pre>
<blockquote>
<p>A block quote.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_231a():
    """
    Test case 231:  If the list item is ordered, then it is also assigned a start number, based on the ordered list marker.
    """

    # Arrange
    source_markdown = """A paragraph
with two lines.
\x0c
    indented code
\x0c
> A block quote."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):\x0c]",
        "[icode-block(4,5):    :]",
        "[text(4,5):indented code:]",
        "[end-icode-block:::True]",
        "[BLANK(5,1):\x0c]",
        "[block-quote(6,1)::> ]",
        "[para(6,3):]",
        "[text(6,3):A block quote.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p>A paragraph
with two lines.</p>
<pre><code>indented code
</code></pre>
<blockquote>
<p>A block quote.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_231b():
    """
    Test case 231:  variant
    """

    # Arrange
    source_markdown = """A paragraph
with two lines.
\u00a0
    indented code
\u00a0
> A block quote."""
    expected_tokens = [
        "[para(1,1):\n\n\n    \n]",
        "[text(1,1):A paragraph\nwith two lines.\n\u00a0\nindented code\n\u00a0::\n\n\n\n]",
        "[end-para:::True]",
        "[block-quote(6,1)::> ]",
        "[para(6,3):]",
        "[text(6,3):A block quote.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p>A paragraph\nwith two lines.\n\u00a0\nindented code\n\u00a0</p>\n<blockquote>\n<p>A block quote.</p>\n</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_232():
    """
    Test case 232:  And let M be the marker 1., and N = 2. Then rule #1 says that
                    the following is an ordered list item with start number 1, and
                    the same contents as Ls:
    """

    # Arrange
    source_markdown = """1.  A paragraph
    with two lines.

        indented code

    > A block quote."""
    expected_tokens = [
        "[olist(1,1):.:1:4::    \n\n    \n\n]",
        "[para(1,5):\n]",
        "[text(1,5):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[icode-block(4,9):    :]",
        "[text(4,9):indented code:]",
        "[end-icode-block:::True]",
        "[BLANK(5,1):]",
        "[block-quote(6,5):    :    > ]",
        "[para(6,7):]",
        "[text(6,7):A block quote.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_233():
    """
    Test case 233:  (part 1) Here are some examples showing how far content must be indented to be put under the list item:

    Note: The tokens are correct.  The blank line on line 2 forces the paragraph closed.
          As it is still allowed inside of the list, only affecting the looseness of
          the list , the list remains open.  With the paragraph closed, the `two` on
          line 3 is not paragraph continuation, and due to the indent, it is not
          part of the list.  At that point, the list is closed and the new paragraph
          is started.
    """

    # Arrange
    source_markdown = """- one

 two"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):]",
        "[text(1,3):one:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[end-ulist:::True]",
        "[para(3,2): ]",
        "[text(3,2):two:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ul>
<li>one</li>
</ul>
<p>two</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_234():
    """
    Test case 234:  (part 2) Here are some examples showing how far content must be indented to be put under the list item:
    """

    # Arrange
    source_markdown = """- one

  two"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n  ]",
        "[para(1,3):]",
        "[text(1,3):one:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,3):]",
        "[text(3,3):two:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>one</p>
<p>two</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_235():
    """
    Test case 235:  (part 3) Here are some examples showing how far content must be indented to be put under the list item:

    Note: See comments for 233.  Same thought process, except more indents.
    """

    # Arrange
    source_markdown = """ -    one

     two"""
    expected_tokens = [
        "[ulist(1,2):-::6: :]",
        "[para(1,7):]",
        "[text(1,7):one:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[end-ulist:::True]",
        "[icode-block(3,5):    :]",
        "[text(3,5):two: ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<ul>
<li>one</li>
</ul>
<pre><code> two
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_236():
    """
    Test case 236:  (part 4) Here are some examples showing how far content must be indented to be put under the list item:
    """

    # Arrange
    source_markdown = """ -    one

      two"""
    expected_tokens = [
        "[ulist(1,2):-::6: :\n      ]",
        "[para(1,7):]",
        "[text(1,7):one:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,7):]",
        "[text(3,7):two:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>one</p>
<p>two</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_list_blocks_237x():
    """
    Test case 237:  The spaces after the list marker determine how much relative indentation is needed. Which column this indentation reaches will depend on how the list item is embedded in other constructions, as shown by this example:
    """

    # Arrange
    source_markdown = """   > > 1.  one
>>
>>     two"""
    expected_tokens = [
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n>>\n>> ]",
        "[olist(1,8):.:1:11:]",
        "[para(1,12):]",
        "[text(1,12):one:]",
        "[end-para:::True]",
        "[BLANK(2,3):]",
        "[para(3,8):]",
        "[text(3,8):two:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_237a():
    """
    Test case 237a:  variation of 237 properly indented
    """

    # Arrange
    source_markdown = """>> one
>>
>>    two"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::>> \n>>\n>> ]",
        "[para(1,4):]",
        "[text(1,4):one:]",
        "[end-para:::True]",
        "[BLANK(2,3):]",
        "[para(3,7):   ]",
        "[text(3,7):two:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>one</p>
<p>two</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_237bx():
    """
    Test case 237a:  variation of 237 improperly indented
    """

    # Arrange
    source_markdown = """ > > one
>>
>>    two"""
    expected_tokens = [
        "[block-quote(1,2): :]",
        "[block-quote(1,4): : > > \n>>\n>> ]",
        "[para(1,6):]",
        "[text(1,6):one:]",
        "[end-para:::True]",
        "[BLANK(2,3):]",
        "[para(3,7):   ]",
        "[text(3,7):two:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>one</p>
<p>two</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_237ba():
    """
    Test case 237ba:  variation of 237b improperly indented
    """

    # Arrange
    source_markdown = """  > > one
>>
>>    two"""
    expected_tokens = [
        "[block-quote(1,3):  :]",
        "[block-quote(1,5):  :  > > \n>>\n>> ]",
        "[para(1,7):]",
        "[text(1,7):one:]",
        "[end-para:::True]",
        "[BLANK(2,3):]",
        "[para(3,7):   ]",
        "[text(3,7):two:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>one</p>
<p>two</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_237c():
    """
    Test case 237c:  variation of 237 properly indented
    """

    # Arrange
    source_markdown = """ >  > one
>>
>>    two"""
    expected_tokens = [
        "[block-quote(1,2): : > ]",
        "[block-quote(1,5):: >  > \n>>\n>> ]",
        "[para(1,7):]",
        "[text(1,7):one:]",
        "[end-para:::True]",
        "[BLANK(2,3):]",
        "[para(3,7):   ]",
        "[text(3,7):two:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>one</p>
<p>two</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_237d():
    """
    Test case 237d:  variation of 237 properly indented
    """

    # Arrange
    source_markdown = """   >   > one
>>
>>    two"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,8)::   >   > \n>>\n>> ]",
        "[para(1,10):]",
        "[text(1,10):one:]",
        "[end-para:::True]",
        "[BLANK(2,3):]",
        "[para(3,7):   ]",
        "[text(3,7):two:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>one</p>
<p>two</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_237e():
    """
    Test case 237:  variation of 237 with not enough on final
    """

    # Arrange
    source_markdown = """   > > 1.  one
>>
>>    two"""
    expected_tokens = [
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n>>\n>> ]",
        "[olist(1,8):.:1:11::]",
        "[para(1,12):]",
        "[text(1,12):one:]",
        "[end-para:::True]",
        "[end-olist:::False]",
        "[BLANK(2,3):]",
        "[para(3,7):   ]",
        "[text(3,7):two:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>one</li>
</ol>
<p>two</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_list_blocks_237f():
    """
    Test case 237:  variation of 237 with blank lines before and after
    """

    # Arrange
    source_markdown = """
   > > 1.  one
>>
>>     two
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[block-quote(2,4):   :]",
        "[block-quote(2,6):   :   > > \n>>\n>> ]",
        "[olist(2,8):.:1:11:]",
        "[para(2,12):]",
        "[text(2,12):one:]",
        "[end-para:::True]",
        "[BLANK(3,3):]",
        "[para(4,8):]",
        "[text(4,8):two:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_list_blocks_237g():
    """
    Test case 237:  variation of 237 where bq starts before
    """

    # Arrange
    source_markdown = """ >   >
   > > 1.  one
>>
>>     two"""
    expected_tokens = [
        "[block-quote(1,2): : > ]",
        "[block-quote(1,6):: >   >\n   > > \n>>\n>> ]",
        "[BLANK(1,7):]",
        "[olist(2,8):.:1:11:]",
        "[para(2,12):]",
        "[text(2,12):one:]",
        "[end-para:::True]",
        "[BLANK(3,3):]",
        "[para(4,8):]",
        "[text(4,8):two:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_238x():
    """
    Test case 238:  The converse is also possible. In the following example, the word two occurs far to the right of the initial text of the list item, one, but it is not considered part of the list item, because it is not indented far enough past the blockquote marker:
    """

    # Arrange
    source_markdown = """>>- one
>>
  >  > two"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::>>\n>>\n  >  > ]",
        "[ulist(1,3):-::4::]",
        "[para(1,5):]",
        "[text(1,5):one:]",
        "[end-para:::True]",
        "[end-ulist:::False]",
        "[BLANK(2,3):]",
        "[para(3,8):]",
        "[text(3,8):two:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>one</li>
</ul>
<p>two</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_list_blocks_238a():
    """
    Test case 238a:  variation of 238 with  more spacing
    """

    # Arrange
    source_markdown = """>>- one
>>
  >  >   two"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::>>\n>>\n  >  > ]",
        "[ulist(1,3):-::4::\n]",
        "[para(1,5):]",
        "[text(1,5):one:]",
        "[end-para:::True]",
        "[BLANK(2,3):]",
        "[para(3,10):]",
        "[text(3,10):two:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<p>one</p>
<p>two</p>
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_list_blocks_238b():
    """
    Test case 238:  variation of 238 with blanks before and after
    """

    # Arrange
    source_markdown = """
>>- one
>>
  >  > two
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[block-quote(2,1)::]",
        "[block-quote(2,2)::>>\n>>\n  >  > \n]",
        "[ulist(2,3):-::4::]",
        "[para(2,5):]",
        "[text(2,5):one:]",
        "[end-para:::True]",
        "[end-ulist:::False]",
        "[BLANK(3,3):]",
        "[para(4,8):]",
        "[text(4,8):two:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>one</li>
</ul>
<p>two</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_238c():
    """
    Test case 238:  variation of 238 where bq starts before
    """

    # Arrange
    source_markdown = """>>
>>- one
>>
  >  > two"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::>>\n>>\n>>\n  >  > ]",
        "[BLANK(1,3):]",
        "[ulist(2,3):-::4::]",
        "[para(2,5):]",
        "[text(2,5):one:]",
        "[end-para:::True]",
        "[end-ulist:::False]",
        "[BLANK(3,3):]",
        "[para(4,8):]",
        "[text(4,8):two:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>one</li>
</ul>
<p>two</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_239():
    """
    Test case 239:  Note that at least one space is needed between the list marker and any following content, so these are not list items:
    """

    # Arrange
    source_markdown = """-one

2.two"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):-one:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):2.two:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>-one</p>
<p>2.two</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_240():
    """
    Test case 240:  A list item may contain blocks that are separated by more than one blank line.
    """

    # Arrange
    source_markdown = """- foo


  bar"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n\n  ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[BLANK(3,1):]",
        "[para(4,3):]",
        "[text(4,3):bar:]",
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
def test_list_blocks_241():
    """
    Test case 241:  A list item may contain any kind of block:
    """

    # Arrange
    source_markdown = """1.  foo

    ```
    bar
    ```

    baz

    > bam"""
    expected_tokens = [
        "[olist(1,1):.:1:4::\n    \n    \n    \n\n    \n\n]",
        "[para(1,5):]",
        "[text(1,5):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[fcode-block(3,5):`:3::::::]",
        "[text(4,5):bar:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
        "[para(7,5):]",
        "[text(7,5):baz:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[block-quote(9,5):    :    > ]",
        "[para(9,7):]",
        "[text(9,7):bam:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_242():
    """
    Test case 242:  A list item that contains an indented code block will preserve empty lines within the code block verbatim.
    """

    # Arrange
    source_markdown = """- Foo

      bar


      baz"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n  \n\n\n  ]",
        "[para(1,3):]",
        "[text(1,3):Foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,7):    :\n\n\n    ]",
        "[text(3,7):bar\n\x03\n\x03\nbaz:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>Foo</p>
<pre><code>bar


baz
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_242a():
    """
    Test case 242a:  variation of 242 with no blank line after first line
    """

    # Arrange
    source_markdown = """- Foo
      bar


      baz"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n\n\n  ]",
        "[para(1,3):\n    ]",
        "[text(1,3):Foo\nbar::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[BLANK(4,1):]",
        "[icode-block(5,7):    :]",
        "[text(5,7):baz:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>Foo
bar</p>
<pre><code>baz
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_242b():
    """
    Test case 242b:  variation of 242 with extra blank lines
    """

    # Arrange
    source_markdown = """- Foo

      bar


      baz


"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n  \n\n\n  \n\n\n]",
        "[para(1,3):]",
        "[text(1,3):Foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,7):    :\n\n\n    ]",
        "[text(3,7):bar\n\x03\n\x03\nbaz:]",
        "[end-icode-block:::True]",
        "[BLANK(7,1):]",
        "[BLANK(8,1):]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>Foo</p>
<pre><code>bar


baz
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_242c():
    """
    Test case 242c:  variation of 242 with extra blank lines
    """

    # Arrange
    source_markdown = """- Foo

      bar




      baz"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n  \n\n\n\n\n  ]",
        "[para(1,3):]",
        "[text(1,3):Foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,7):    :\n\n\n\n\n    ]",
        "[text(3,7):bar\n\x03\n\x03\n\x03\n\x03\nbaz:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>Foo</p>
<pre><code>bar




baz
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_242d():
    """
    Test case 242d:  variation of 242, if in a paragraph, the text's indents are split
                     between the paragraph and the enclosing list
    """

    # Arrange
    source_markdown = """- Foo

     bar
     baz"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):Foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,6):   \n   ]",
        "[text(3,6):bar\nbaz::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>Foo</p>
<p>bar
baz</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_243():
    """
    Test case 243:  (part 1) Note that ordered list start numbers must be nine digits or less:
    """

    # Arrange
    source_markdown = """123456789. ok"""
    expected_tokens = [
        "[olist(1,1):.:123456789:11:]",
        "[para(1,12):]",
        "[text(1,12):ok:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol start="123456789">
<li>ok</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_244():
    """
    Test case 244:  (part 2) Note that ordered list start numbers must be nine digits or less:
    """

    # Arrange
    source_markdown = """1234567890. not ok"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):1234567890. not ok:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>1234567890. not ok</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_245():
    """
    Test case 245:  (part 1) A start number may begin with 0s:
    """

    # Arrange
    source_markdown = """0. ok"""
    expected_tokens = [
        "[olist(1,1):.:0:3:]",
        "[para(1,4):]",
        "[text(1,4):ok:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol start="0">
<li>ok</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_246():
    """
    Test case 246:  (part 2) A start number may begin with 0s:
    """

    # Arrange
    source_markdown = """003. ok"""
    expected_tokens = [
        "[olist(1,1):.:003:5:]",
        "[para(1,6):]",
        "[text(1,6):ok:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol start="3">
<li>ok</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_247():
    """
    Test case 247:  A start number may not be negative:
    """

    # Arrange
    source_markdown = """-1. not ok"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):-1. not ok:]", "[end-para:::True]"]
    expected_gfm = """<p>-1. not ok</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_248():
    """
    Test case 248:  An indented code block will have to be indented four spaces beyond the edge of the region where text will be included in the list item. In the following case that is 6 spaces:
    """

    # Arrange
    source_markdown = """- foo

      bar"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n  ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,7):    :]",
        "[text(3,7):bar:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>foo</p>
<pre><code>bar
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_248a():
    """
    Test case 248a:  variation of 248 with less indent on line three
    """

    # Arrange
    source_markdown = """- foo

     bar"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n  ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,6):   ]",
        "[text(3,6):bar:]",
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
def test_list_blocks_249():
    """
    Test case 249:  And in this case it is 11 spaces:
    """

    # Arrange
    source_markdown = """  10.  foo

           bar"""
    expected_tokens = [
        "[olist(1,3):.:10:7:  :\n       ]",
        "[para(1,8):]",
        "[text(1,8):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,12):    :]",
        "[text(3,12):bar:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol start="10">
<li>
<p>foo</p>
<pre><code>bar
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_250():
    """
    Test case 250:  (part 1) If the first block in the list item is an indented code block, then by rule #2, the contents must be indented one space after the list marker:
    """

    # Arrange
    source_markdown = """    indented code

paragraph

    more code"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):indented code:]",
        "[end-icode-block:::False]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):paragraph:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[icode-block(5,5):    :]",
        "[text(5,5):more code:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>indented code
</code></pre>
<p>paragraph</p>
<pre><code>more code
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_251():
    """
    Test case 251:  (part 2) If the first block in the list item is an indented code block, then by rule #2, the contents must be indented one space after the list marker:
    """

    # Arrange
    source_markdown = """1.     indented code

   paragraph

       more code"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n   \n\n   ]",
        "[icode-block(1,8):    :]",
        "[text(1,8):indented code:]",
        "[end-icode-block:::False]",
        "[BLANK(2,1):]",
        "[para(3,4):]",
        "[text(3,4):paragraph:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[icode-block(5,8):    :]",
        "[text(5,8):more code:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_252():
    """
    Test case 252:  (part 2) If the first block in the list item is an indented code block, then by rule #2, the contents must be indented one space after the list marker:
    """

    # Arrange
    source_markdown = """1.      indented code

   paragraph

       more code"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n   \n\n   ]",
        "[icode-block(1,8):    :]",
        "[text(1,8):indented code: ]",
        "[end-icode-block:::False]",
        "[BLANK(2,1):]",
        "[para(3,4):]",
        "[text(3,4):paragraph:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[icode-block(5,8):    :]",
        "[text(5,8):more code:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_253():
    """
    Test case 253:  (part 1) Note that rules #1 and #2 only apply to two cases: (a) cases in which the lines to be included in a list item begin with a non-whitespace character, and (b) cases in which they begin with an indented code block. In a case like the following, where the first block begins with a three-space indent, the rules do not allow us to form a list item by indenting the whole thing and prepending a list marker:
    """

    # Arrange
    source_markdown = """   foo

bar"""
    expected_tokens = [
        "[para(1,4):   ]",
        "[text(1,4):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo</p>
<p>bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_254():
    """
    Test case 254:  (part 2) Note that rules #1 and #2 only apply to two cases: (a) cases in which the lines to be included in a list item begin with a non-whitespace character, and (b) cases in which they begin with an indented code block. In a case like the following, where the first block begins with a three-space indent, the rules do not allow us to form a list item by indenting the whole thing and prepending a list marker:
    """

    # Arrange
    source_markdown = """-    foo

  bar"""
    expected_tokens = [
        "[ulist(1,1):-::5::]",
        "[para(1,6):]",
        "[text(1,6):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[end-ulist:::True]",
        "[para(3,3):  ]",
        "[text(3,3):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
</ul>
<p>bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_255():
    """
    Test case 255:  This is not a significant restriction, because when a block begins with 1-3 spaces indent, the indentation can always be removed without a change in interpretation, allowing rule #1 to be applied. So, in the above case:
    """

    # Arrange
    source_markdown = """-  foo

   bar"""
    expected_tokens = [
        "[ulist(1,1):-::3::\n   ]",
        "[para(1,4):]",
        "[text(1,4):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,4):]",
        "[text(3,4):bar:]",
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
def test_list_blocks_256x():
    """
    Test case 256:  Here are some list items that start with a blank line but are not empty:
    """

    # Arrange
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
        "[text(2,3):foo:]",
        "[end-para:::True]",
        "[li(3,1):2::]",
        "[BLANK(3,2):]",
        "[fcode-block(4,3):`:3::::::]",
        "[text(5,3):bar:]",
        "[end-fcode-block:::3:False]",
        "[li(7,1):2::]",
        "[BLANK(7,2):]",
        "[icode-block(8,7):    :]",
        "[text(8,7):baz:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_256a():
    """
    Test case 256a:  variation on 256 with extra spaces on blank lines don't make any impact
    """

    # Arrange
    source_markdown = """-\a
  foo
-\a
  ```
  bar
  ```
-\a
      baz""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  \n  ]",
        "[BLANK(1,3):]",
        "[para(2,3):]",
        "[text(2,3):foo:]",
        "[end-para:::True]",
        "[li(3,1):2::]",
        "[BLANK(3,3):]",
        "[fcode-block(4,3):`:3::::::]",
        "[text(5,3):bar:]",
        "[end-fcode-block:::3:False]",
        "[li(7,1):2::]",
        "[BLANK(7,3):]",
        "[icode-block(8,7):    :]",
        "[text(8,7):baz:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_256b():
    """
    Test case 256b:  variation on 256 with extra spaces on blank lines don't make any impact
    """

    # Arrange
    source_markdown = """-\a\a
  foo
-\a\a
  ```
  bar
  ```
-\a\a
      baz""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  \n  ]",
        "[BLANK(1,3): ]",
        "[para(2,3):]",
        "[text(2,3):foo:]",
        "[end-para:::True]",
        "[li(3,1):2::]",
        "[BLANK(3,3): ]",
        "[fcode-block(4,3):`:3::::::]",
        "[text(5,3):bar:]",
        "[end-fcode-block:::3:False]",
        "[li(7,1):2::]",
        "[BLANK(7,3): ]",
        "[icode-block(8,7):    :]",
        "[text(8,7):baz:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_256c():
    """
    Test case 256c:  variation of 256 with ordered list
    """

    # Arrange
    source_markdown = """1.
   foo
1.
   ```
   bar
   ```
1.
      baz"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n   \n   ]",
        "[BLANK(1,3):]",
        "[para(2,4):]",
        "[text(2,4):foo:]",
        "[end-para:::True]",
        "[li(3,1):3::1]",
        "[BLANK(3,3):]",
        "[fcode-block(4,4):`:3::::::]",
        "[text(5,4):bar:]",
        "[end-fcode-block:::3:False]",
        "[li(7,1):3::1]",
        "[BLANK(7,3):]",
        "[para(8,7):   ]",
        "[text(8,7):baz:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
<li>
<pre><code>bar
</code></pre>
</li>
<li>baz</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_256d():
    """
    Test case 256d:  variation of 256with (almost) ordered list
    """

    # Arrange
    source_markdown = """1.

  foo
1.

  ```
  bar
  ```
1.

      baz"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[BLANK(2,1):]",
        "[para(3,3):  \n]",
        "[text(3,3):foo\n1.::\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[fcode-block(6,3):`:3:::::  :]",
        "[text(7,3):bar:\a  \a\x03\a]",
        "[end-fcode-block:  ::3:False]",
        "[olist(9,1):.:1:3:]",
        "[BLANK(9,3):]",
        "[end-olist:::True]",
        "[BLANK(10,1):]",
        "[icode-block(11,5):    :]",
        "[text(11,5):baz:  ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<p>foo
1.</p>
<pre><code>bar
</code></pre>
<ol>
<li></li>
</ol>
<pre><code>  baz
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_256e():
    """
    Test case 256e:  variation of 256 with (almost) ordered list
    """

    # Arrange
    source_markdown = """1.
  foo
1.
  ```
  bar
  ```
1.
      baz"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[para(2,3):  \n]",
        "[text(2,3):foo\n1.::\n]",
        "[end-para:::False]",
        "[fcode-block(4,3):`:3:::::  :]",
        "[text(5,3):bar:\a  \a\x03\a]",
        "[end-fcode-block:  ::3:False]",
        "[olist(7,1):.:1:3::   ]",
        "[BLANK(7,3):]",
        "[para(8,7):   ]",
        "[text(8,7):baz:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<p>foo
1.</p>
<pre><code>bar
</code></pre>
<ol>
<li>baz</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_257xx():
    """
    Test case 257:  When the list item starts with a blank line, the number of spaces following the list marker doesn’t change the required indentation:
    """

    # Arrange
    source_markdown = """-\a\a\a
  foo""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[BLANK(1,3):  ]",
        "[para(2,3):]",
        "[text(2,3):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_257xa():
    """
    Test case 257:  TBD
    """

    # Arrange
    source_markdown = """- fred
  foo"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n]",
        "[text(1,3):fred\nfoo::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>fred
foo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_257xb():
    """
    Test case 257:  TBD
    """

    # Arrange
    source_markdown = """-  fred
  foo"""
    expected_tokens = [
        "[ulist(1,1):-::3::]",
        "[para(1,4):\n  ]",
        "[text(1,4):fred\nfoo::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>fred
foo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_257xc():
    """
    Test case 257:  TBD
    """

    # Arrange
    source_markdown = """- fred
  foo
  bar"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[para(1,3):\n\n]",
        "[text(1,3):fred\nfoo\nbar::\n\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>fred
foo
bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_257xd():
    """
    Test case 257:  TBD
    """

    # Arrange
    source_markdown = """- fred

  bar"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n  ]",
        "[para(1,3):]",
        "[text(1,3):fred:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,3):]",
        "[text(3,3):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>fred</p>
<p>bar</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_257xe():
    """
    Test case 257:  TBD
    """

    # Arrange
    source_markdown = """- fred
foo
  bar"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n  ]",
        "[para(1,3):\n\n]",
        "[text(1,3):fred\nfoo\nbar::\n\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>fred
foo
bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_257xf():
    """
    Test case 257:  TBD
    """

    # Arrange
    source_markdown = """- fred
- foo
  bar"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):fred:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):\n]",
        "[text(2,3):foo\nbar::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>fred</li>
<li>foo
bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_257a():
    """
    Test case 257a:  variation on 257 with no extra spaces on start line
    """

    # Arrange
    source_markdown = """-
  foo"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[BLANK(1,2):]",
        "[para(2,3):]",
        "[text(2,3):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_257b():
    """
    Test case 257b:  variation on 257 with no extra spaces on start line
        and ordered list
    """

    # Arrange
    source_markdown = """1.
   foo"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[para(2,4):]",
        "[text(2,4):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_258():
    """
    Test case 258:  A list item can begin with at most one blank line. In the following example, foo is not part of the list item:
    """

    # Arrange
    source_markdown = """-

  foo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[BLANK(1,2):]",
        "[end-ulist:::True]",
        "[BLANK(2,1):]",
        "[para(3,3):  ]",
        "[text(3,3):foo:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ul>
<li></li>
</ul>
<p>foo</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_259():
    """
    Test case 259:  Here is an empty bullet list item:
    """

    # Arrange
    source_markdown = """- foo
-
- bar"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[BLANK(2,2):]",
        "[li(3,1):2::]",
        "[para(3,3):]",
        "[text(3,3):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
<li></li>
<li>bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_260():
    """
    Test case 260:  It does not matter whether there are spaces following the list marker:
    """

    # Arrange
    source_markdown = """- foo
-\a\a\a
- bar""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[BLANK(2,3):  ]",
        "[li(3,1):2::]",
        "[para(3,3):]",
        "[text(3,3):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
<li></li>
<li>bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_261():
    """
    Test case 261:  Here is an empty ordered list item:
    """

    # Arrange
    source_markdown = """1. foo
2.
3. bar"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):foo:]",
        "[end-para:::True]",
        "[li(2,1):3::2]",
        "[BLANK(2,3):]",
        "[li(3,1):3::3]",
        "[para(3,4):]",
        "[text(3,4):bar:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
<li></li>
<li>bar</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_262():
    """
    Test case 262:  A list may start or end with an empty list item:
    """

    # Arrange
    source_markdown = """*"""
    expected_tokens = ["[ulist(1,1):*::2:]", "[BLANK(1,2):]", "[end-ulist:::True]"]
    expected_gfm = """<ul>
<li></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_262a():
    """
    Test case 262a:  variation on 262 with ordered list
    """

    # Arrange
    source_markdown = """1."""
    expected_tokens = ["[olist(1,1):.:1:3:]", "[BLANK(1,3):]", "[end-olist:::True]"]
    expected_gfm = """<ol>
<li></li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_263():
    """
    Test case 263:  However, an empty list item cannot interrupt a paragraph:
    """

    # Arrange
    source_markdown = """foo
*

foo
1."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo\n::\n]",
        "[text(2,1):*:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):foo\n1.::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo
*</p>
<p>foo
1.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_263a():
    """
    Test case 263a:  variation on 263
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_263b():
    """
    Test case 263b:  variation on 263a with following list number
    """

    # Arrange
    source_markdown = """1. abc
   2. abc
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n]",
        "[para(1,4):\n]",
        "[text(1,4):abc\n2. abc::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
2. abc</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_263bu():
    """
    Test case 257bu:  variation on 257b with unordered
    """

    # Arrange
    source_markdown = """- abc
  - abc
"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :]",
        "[para(2,5):]",
        "[text(2,5):abc:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>abc</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_264():
    """
    Test case 264:  Indented one space:
    """

    # Arrange
    source_markdown = """ 1.  A paragraph
     with two lines.

         indented code

     > A block quote."""
    expected_tokens = [
        "[olist(1,2):.:1:5: :     \n\n     \n\n]",
        "[para(1,6):\n]",
        "[text(1,6):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[icode-block(4,10):    :]",
        "[text(4,10):indented code:]",
        "[end-icode-block:::True]",
        "[BLANK(5,1):]",
        "[block-quote(6,6):     :     > ]",
        "[para(6,8):]",
        "[text(6,8):A block quote.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_265():
    """
    Test case 265:  Indented two spaces:
    """

    # Arrange
    source_markdown = """  1.  A paragraph
      with two lines.

          indented code

      > A block quote."""
    expected_tokens = [
        "[olist(1,3):.:1:6:  :      \n\n      \n\n]",
        "[para(1,7):\n]",
        "[text(1,7):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[icode-block(4,11):    :]",
        "[text(4,11):indented code:]",
        "[end-icode-block:::True]",
        "[BLANK(5,1):]",
        "[block-quote(6,7):      :      > ]",
        "[para(6,9):]",
        "[text(6,9):A block quote.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_266():
    """
    Test case 266:  Indented three spaces:
    """

    # Arrange
    source_markdown = """   1.  A paragraph
       with two lines.

           indented code

       > A block quote."""
    expected_tokens = [
        "[olist(1,4):.:1:7:   :       \n\n       \n\n]",
        "[para(1,8):\n]",
        "[text(1,8):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[icode-block(4,12):    :]",
        "[text(4,12):indented code:]",
        "[end-icode-block:::True]",
        "[BLANK(5,1):]",
        "[block-quote(6,8):       :       > ]",
        "[para(6,10):]",
        "[text(6,10):A block quote.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_267():
    """
    Test case 267:  Four spaces indent gives a code block
    """

    # Arrange
    source_markdown = """    1.  A paragraph
        with two lines.

            indented code

        > A block quote."""
    expected_tokens = [
        "[icode-block(1,5):    :\n    \n\n    \n\n    ]",
        "[text(1,5):1.  A paragraph\n    with two lines.\n\x03\n        indented code\n\x03\n    \a>\a&gt;\a A block quote.:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>1.  A paragraph
    with two lines.

        indented code

    &gt; A block quote.
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_268():
    """
    Test case 268:  Here is an example with lazy continuation lines:
    """

    # Arrange
    source_markdown = """  1.  A paragraph
 with two lines.

          indented code

      > A block quote."""
    expected_tokens = [
        "[olist(1,3):.:1:6:  :\n\n      \n\n]",
        "[para(1,7):\n ]",
        "[text(1,7):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[icode-block(4,11):    :]",
        "[text(4,11):indented code:]",
        "[end-icode-block:::True]",
        "[BLANK(5,1):]",
        "[block-quote(6,7):      :      > ]",
        "[para(6,9):]",
        "[text(6,9):A block quote.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_269x():
    """
    Test case 269:  Indentation can be partially deleted:
    """

    # Arrange
    source_markdown = """  1.  A paragraph
    with two lines."""
    expected_tokens = [
        "[olist(1,3):.:1:6:  :]",
        "[para(1,7):\n    ]",
        "[text(1,7):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>A paragraph
with two lines.</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_269a():
    """
    Test case 269a:  variation on 269 with less indent on second line
    """

    # Arrange
    source_markdown = """  1.  A paragraph
   with two lines."""
    expected_tokens = [
        "[olist(1,3):.:1:6:  :]",
        "[para(1,7):\n   ]",
        "[text(1,7):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>A paragraph
with two lines.</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_269b():
    """
    Test case 269b:  variation on 269 with more indent on second line
    """

    # Arrange
    source_markdown = """  1.  A paragraph
     with two lines."""
    expected_tokens = [
        "[olist(1,3):.:1:6:  :]",
        "[para(1,7):\n     ]",
        "[text(1,7):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>A paragraph
with two lines.</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_269c():
    """
    Test case 269c:  variation on 269 with extra line
    """

    # Arrange
    source_markdown = """  1.  A paragraph
     with more than
    the two lines."""
    expected_tokens = [
        "[olist(1,3):.:1:6:  :\n]",
        "[para(1,7):\n     \n    ]",
        "[text(1,7):A paragraph\nwith more than\nthe two lines.::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>A paragraph
with more than
the two lines.</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_270x():
    """
    Test case 270:  (part 1) These examples show how laziness can work in nested structures:
    """

    # Arrange
    source_markdown = """> 1. > Blockquote
continued here."""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::\n]",
        "[block-quote(1,6)::> \n]",
        "[para(1,8):\n]",
        "[text(1,8):Blockquote\ncontinued here.::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_270a():
    """
    Test case 270a: variation of 270 that starts and stops with a blank
    """

    # Arrange
    source_markdown = """
> 1. > Blockquote
continued here.
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[block-quote(2,1)::> ]",
        "[olist(2,3):.:1:5::\n\n]",
        "[block-quote(2,6)::> \n\n]",
        "[para(2,8):\n]",
        "[text(2,8):Blockquote\ncontinued here.::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_270b():
    """
    Test case 270a: variation of 270 with a list item
    """

    # Arrange
    source_markdown = """1. > 1. Blockquote
continued here."""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n]",
        "[olist(1,6):.:1:8::\n]",
        "[para(1,9):\n]",
        "[text(1,9):Blockquote\ncontinued here.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ol>
<li>Blockquote
continued here.</li>
</ol>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_270c():
    """
    Test case 270:  variation where bq starts before
    """

    # Arrange
    source_markdown = """>
> 1. > Blockquote
continued here."""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5::\n]",
        "[block-quote(2,6)::> \n]",
        "[para(2,8):\n]",
        "[text(2,8):Blockquote\ncontinued here.::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_270d():
    """
    Test case 270:  variation where bq starts before
    """

    # Arrange
    source_markdown = """>
> 1. test
>    > Blockquote
continued here."""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5::\n\n]",
        "[para(2,6):]",
        "[text(2,6):test:]",
        "[end-para:::True]",
        "[block-quote(3,6)::> \n]",
        "[para(3,8):\n]",
        "[text(3,8):Blockquote\ncontinued here.::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>test
<blockquote>
<p>Blockquote
continued here.</p>
</blockquote>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_271x():
    """
    Test case 271:  (part 2) These examples show how laziness can work in nested structures:
    """

    # Arrange
    source_markdown = """> 1. > Blockquote
> continued here."""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::]",
        "[block-quote(1,6)::> \n> ]",
        "[para(1,8):\n]",
        "[text(1,8):Blockquote\ncontinued here.::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_271ax():
    """
    Test case 271a:  variation of 271 with blank line after
    """

    # Arrange
    source_markdown = """> 1. > Blockquote
> continued here.
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::\n]",
        "[block-quote(1,6)::> \n> \n]",
        "[para(1,8):\n]",
        "[text(1,8):Blockquote\ncontinued here.::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_271aa():
    """
    Test case 271a:  variation of 271 with blank line after
    """

    # Arrange
    source_markdown = """> 1. > Blockquote
> continued here.

not here"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::\n]",
        "[block-quote(1,6)::> \n> \n]",
        "[para(1,8):\n]",
        "[text(1,8):Blockquote\ncontinued here.::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[para(4,1):]",
        "[text(4,1):not here:]",
        "[end-para:::True]",
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
</blockquote>
<p>not here</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_271b():
    """
    Test case 271:  variation of 271 with list item
    """

    # Arrange
    source_markdown = """1. > 1. Blockquote
> continued here."""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > ]",
        "[olist(1,6):.:1:8:]",
        "[para(1,9):]",
        "[text(1,9):Blockquote:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[block-quote(2,1)::> ]",
        "[para(2,3):]",
        "[text(2,3):continued here.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ol>
<li>Blockquote</li>
</ol>
</blockquote>
</li>
</ol>
<blockquote>
<p>continued here.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_271c():
    """
    Test case 271:  variation where bq starts before
    """

    # Arrange
    source_markdown = """>
> 1. > Blockquote
> continued here."""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[olist(2,3):.:1:5::]",
        "[block-quote(2,6)::> \n> ]",
        "[para(2,8):\n]",
        "[text(2,8):Blockquote\ncontinued here.::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_271d():
    """
    Test case 271:  variation of 271b without base list item
    """

    # Arrange
    source_markdown = """> 1. Blockquote
> continued here."""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[olist(1,3):.:1:5::]",
        "[para(1,6):\n]",
        "[text(1,6):Blockquote\ncontinued here.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>Blockquote
continued here.</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_271e():
    """
    Test case 271:  variation of 271b without inner list item
    """

    # Arrange
    source_markdown = """1. > Blockquote
> continued here."""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > ]",
        "[para(1,6):]",
        "[text(1,6):Blockquote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[block-quote(2,1)::> ]",
        "[para(2,3):]",
        "[text(2,3):continued here.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>Blockquote</p>
</blockquote>
</li>
</ol>
<blockquote>
<p>continued here.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_271fx():
    """
    Test case 271:  variation of 271e with extra nesting
    """

    # Arrange
    source_markdown = """1. > 1. > Blockquote
> continued here."""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > ]",
        "[olist(1,6):.:1:8:]",
        "[block-quote(1,9)::> ]",
        "[para(1,11):]",
        "[text(1,11):Blockquote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[block-quote(2,1)::> ]",
        "[para(2,3):]",
        "[text(2,3):continued here.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ol>
<li>
<blockquote>
<p>Blockquote</p>
</blockquote>
</li>
</ol>
</blockquote>
</li>
</ol>
<blockquote>
<p>continued here.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_271fa():
    """
    Test case 271:  variation of 271e with extra nesting
    """

    # Arrange
    source_markdown = """1. > 1. > Blockquote"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > ]",
        "[olist(1,6):.:1:8:]",
        "[block-quote(1,9)::> ]",
        "[para(1,11):]",
        "[text(1,11):Blockquote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ol>
<li>
<blockquote>
<p>Blockquote</p>
</blockquote>
</li>
</ol>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_272():
    """
    Test case 272:  So, in this case we need two spaces indent:
    """

    # Arrange
    source_markdown = """- foo
  - bar
    - baz
      - boo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):bar:]",
        "[end-para:::True]",
        "[ulist(3,5):-::6:    ]",
        "[para(3,7):]",
        "[text(3,7):baz:]",
        "[end-para:::True]",
        "[ulist(4,7):-::8:      ]",
        "[para(4,9):]",
        "[text(4,9):boo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_273():
    """
    Test case 273:  One is not enough:
    """

    # Arrange
    source_markdown = """- foo
 - bar
  - baz
   - boo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[li(2,2):3: :]",
        "[para(2,4):]",
        "[text(2,4):bar:]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text(3,5):baz:]",
        "[end-para:::True]",
        "[li(4,4):5:   :]",
        "[para(4,6):]",
        "[text(4,6):boo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
<li>bar</li>
<li>baz</li>
<li>boo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_274():
    """
    Test case 274:  Here we need four, because the list marker is wider:
    """

    # Arrange
    source_markdown = """10) foo
    - bar"""
    expected_tokens = [
        "[olist(1,1):):10:4:]",
        "[para(1,5):]",
        "[text(1,5):foo:]",
        "[end-para:::True]",
        "[ulist(2,5):-::6:    ]",
        "[para(2,7):]",
        "[text(2,7):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol start="10">
<li>foo
<ul>
<li>bar</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_274a():
    """
    Test case 274a:  variation on 274 with different start number and extra list
    """

    # Arrange
    source_markdown = """1) foo
   - bar
1. baz"""
    expected_tokens = [
        "[olist(1,1):):1:3:]",
        "[para(1,4):]",
        "[text(1,4):foo:]",
        "[end-para:::True]",
        "[ulist(2,4):-::5:   ]",
        "[para(2,6):]",
        "[text(2,6):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[olist(3,1):.:1:3:]",
        "[para(3,4):]",
        "[text(3,4):baz:]",
        "[end-para:::True]",
        "[end-olist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_274b():
    """
    Test case 274b:  variation on 274 with different start number and extra unordered list
    """

    # Arrange
    source_markdown = """1) foo
   - bar
- baz"""
    expected_tokens = [
        "[olist(1,1):):1:3:]",
        "[para(1,4):]",
        "[text(1,4):foo:]",
        "[end-para:::True]",
        "[ulist(2,4):-::5:   ]",
        "[para(2,6):]",
        "[text(2,6):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[ulist(3,1):-::2:]",
        "[para(3,3):]",
        "[text(3,3):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_274c():
    """
    Test case 274c:  variation on 274 with ul start and other lists as ordered
    """

    # Arrange
    source_markdown = """- foo
  1) bar
1) baz"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[olist(2,3):):1:5:  ]",
        "[para(2,6):]",
        "[text(2,6):bar:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[olist(3,1):):1:3:]",
        "[para(3,4):]",
        "[text(3,4):baz:]",
        "[end-para:::True]",
        "[end-olist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_275():
    """
    Test case 275:  Three is not enough:
    """

    # Arrange
    source_markdown = """10) foo
   - bar"""
    expected_tokens = [
        "[olist(1,1):):10:4:]",
        "[para(1,5):]",
        "[text(1,5):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[ulist(2,4):-::5:   ]",
        "[para(2,6):]",
        "[text(2,6):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ol start="10">
<li>foo</li>
</ol>
<ul>
<li>bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_276():
    """
    Test case 276:  (part 1) A list may be the first block in a list item:
    """

    # Arrange
    source_markdown = """- - foo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[ulist(1,3):-::4:  ]",
        "[para(1,5):]",
        "[text(1,5):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>foo</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_276a():
    """
    Test case 276a:  variation on 276 with ol as second list
    """

    # Arrange
    source_markdown = """- 1. foo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[olist(1,3):.:1:5:  ]",
        "[para(1,6):]",
        "[text(1,6):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>foo</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_276aa():
    """
    Test case 276aa:  variation on 276 with extra list
    """

    # Arrange
    source_markdown = """- 1. - foo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[olist(1,3):.:1:5:  ]",
        "[ulist(1,6):-::7:     ]",
        "[para(1,8):]",
        "[text(1,8):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ul>
<li>foo</li>
</ul>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_276ab():
    """
    Test case 276ab:  variation on 276 with extra list
    """

    # Arrange
    source_markdown = """- 1. 1. foo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[olist(1,3):.:1:5:  ]",
        "[olist(1,6):.:1:8:     ]",
        "[para(1,9):]",
        "[text(1,9):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<ol>
<li>foo</li>
</ol>
</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_276b():
    """
    Test case 276b:  variation on 276 inverted list types
    """

    # Arrange
    source_markdown = """1. - foo"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[ulist(1,4):-::5:   ]",
        "[para(1,6):]",
        "[text(1,6):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>foo</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_276ba():
    """
    Test case 276ba:  variation on 276b with extra list
    """

    # Arrange
    source_markdown = """1. - - foo"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[ulist(1,4):-::5:   ]",
        "[ulist(1,6):-::7:     ]",
        "[para(1,8):]",
        "[text(1,8):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<ul>
<li>foo</li>
</ul>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_276bb():
    """
    Test case 276bb:  variation on 276b with extra list
    """

    # Arrange
    source_markdown = """1. - 1. foo"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[ulist(1,4):-::5:   ]",
        "[olist(1,6):.:1:8:     ]",
        "[para(1,9):]",
        "[text(1,9):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ul>
<li>
<ol>
<li>foo</li>
</ol>
</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_276c():
    """
    Test case 276c:  variation on 276 both ordered
    """

    # Arrange
    source_markdown = """1. 1. foo"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>foo</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_276ca():
    """
    Test case 276ca:  variation on 276 both ordered and extra list
    """

    # Arrange
    source_markdown = """1. 1. - foo"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[ulist(1,7):-::8:      ]",
        "[para(1,9):]",
        "[text(1,9):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<ul>
<li>foo</li>
</ul>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_276cb():
    """
    Test case 276cb:  variation on 276 both ordered and extra list
    """

    # Arrange
    source_markdown = """1. 1. 1. foo"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[olist(1,7):.:1:9:      ]",
        "[para(1,10):]",
        "[text(1,10):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<ol>
<li>foo</li>
</ol>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_276d():
    """
    Test case 276d:  variation on 276 with ordered list increment
    """

    # Arrange
    source_markdown = """1. 2. foo"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:2:6:   ]",
        "[para(1,7):]",
        "[text(1,7):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol start="2">
<li>foo</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_276da():
    """
    Test case 276da:  variation on 276d with ordered list increment and extra list
    """

    # Arrange
    source_markdown = """1. 2. - foo"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:2:6:   ]",
        "[ulist(1,7):-::8:      ]",
        "[para(1,9):]",
        "[text(1,9):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol start="2">
<li>
<ul>
<li>foo</li>
</ul>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_276db():
    """
    Test case 276db:  variation on 276d with ordered list increment and extra list
    """

    # Arrange
    source_markdown = """1. 2. 3. foo"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:2:6:   ]",
        "[olist(1,7):.:3:9:      ]",
        "[para(1,10):]",
        "[text(1,10):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol start="2">
<li>
<ol start="3">
<li>foo</li>
</ol>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_277():
    """
    Test case 277:  (part 2) A list may be the first block in a list item:
    """

    # Arrange
    source_markdown = """1. - 2. foo"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[ulist(1,4):-::5:   ]",
        "[olist(1,6):.:2:8:     ]",
        "[para(1,9):]",
        "[text(1,9):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_278():
    """
    Test case 278:  A list item can contain a heading:
    """

    # Arrange
    source_markdown = """- # Foo
- Bar
  ---
  baz"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[atx(1,3):1:0:]",
        "[text(1,5):Foo: ]",
        "[end-atx::]",
        "[li(2,1):2::]",
        "[setext(3,3):-:3::(2,3)]",
        "[text(2,3):Bar:]",
        "[end-setext::]",
        "[para(4,3):]",
        "[text(4,3):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h1>Foo</h1>
</li>
<li>
<h2>Bar</h2>
baz</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_1():
    """
    Test case 01:  Lists and sublists
    """

    # Arrange
    source_markdown = """1. one
   1. one-A
1. two
   1. two-A
1. three"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):one:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):one-A:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(3,1):3::1]",
        "[para(3,4):]",
        "[text(3,4):two:]",
        "[end-para:::True]",
        "[olist(4,4):.:1:6:   ]",
        "[para(4,7):]",
        "[text(4,7):two-A:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(5,1):3::1]",
        "[para(5,4):]",
        "[text(5,4):three:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>one
<ol>
<li>one-A</li>
</ol>
</li>
<li>two
<ol>
<li>two-A</li>
</ol>
</li>
<li>three</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_2():
    """
    Test case 02:  Lists and sublists with increasing numbers
    """

    # Arrange
    source_markdown = """1. one
   1. one-A
1. two
   2. two-A
1. three"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):one:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):one-A:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(3,1):3::1]",
        "[para(3,4):\n]",
        "[text(3,4):two\n2. two-A::\n]",
        "[end-para:::True]",
        "[li(5,1):3::1]",
        "[para(5,4):]",
        "[text(5,4):three:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>one
<ol>
<li>one-A</li>
</ol>
</li>
<li>two
2. two-A</li>
<li>three</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_2u():
    """
    Test case 02u:  unordered lists and sublists
    """

    # Arrange
    source_markdown = """- one
  - one-A
- two
  - two-A
- three"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):one:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):one-A:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(3,1):2::]",
        "[para(3,3):]",
        "[text(3,3):two:]",
        "[end-para:::True]",
        "[ulist(4,3):-::4:  ]",
        "[para(4,5):]",
        "[text(4,5):two-A:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):three:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>one
<ul>
<li>one-A</li>
</ul>
</li>
<li>two
<ul>
<li>two-A</li>
</ul>
</li>
<li>three</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_2a():
    """
    Test case 02a:  ordered lists and sublists with text on next line
    """

    # Arrange
    source_markdown = """1. abc
def
   1. ghi
jkl
1. three"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n]",
        "[text(1,4):abc\ndef::\n]",
        "[end-para:::True]",
        "[olist(3,4):.:1:6:   :]",
        "[para(3,7):\n]",
        "[text(3,7):ghi\njkl::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(5,1):3::1]",
        "[para(5,4):]",
        "[text(5,4):three:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
def
<ol>
<li>ghi
jkl</li>
</ol>
</li>
<li>three</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_3():
    """
    Test case 03:  Code span in lists.
    """

    # Arrange
    source_markdown = """1. `one`
   1. ``one-A``
1. `two`
   1. ``two-A``
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[icode-span(1,4):one:`::]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[icode-span(2,7):one-A:``::]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(3,1):3::1]",
        "[para(3,4):]",
        "[icode-span(3,4):two:`::]",
        "[end-para:::True]",
        "[olist(4,4):.:1:6:   :]",
        "[para(4,7):]",
        "[icode-span(4,7):two-A:``::]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li><code>one</code>
<ol>
<li><code>one-A</code></li>
</ol>
</li>
<li><code>two</code>
<ol>
<li><code>two-A</code></li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_4():
    """
    Test case 04:  A list item can a link split over lines, regardless of any
                   spacing, as a paragraph has already been started.
    """

    # Arrange
    source_markdown = """1. [test](/me
"out")
   1. [really test](/me
"out")
1. three"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n]",
        '[link(1,4):inline:/me:out::::test:False:"::\n:]',
        "[text(1,5):test:]",
        "[end-link::]",
        "[end-para:::True]",
        "[olist(3,4):.:1:6:   :]",
        "[para(3,7):\n]",
        '[link(3,7):inline:/me:out::::really test:False:"::\n:]',
        "[text(3,8):really test:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(5,1):3::1]",
        "[para(5,4):]",
        "[text(5,4):three:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li><a href="/me" title="out">test</a>
<ol>
<li><a href="/me" title="out">really test</a></li>
</ol>
</li>
<li>three</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_4a():
    """
    Test case 04a:  A list item can a link split over lines, regardless of any
                    spacing, as a paragraph has already been started.
    """

    # Arrange
    source_markdown = """1. [test](/me
   "out")
   1. [really test](/me
   "out")
1. three"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n]",
        '[link(1,4):inline:/me:out::::test:False:"::\n:]',
        "[text(1,5):test:]",
        "[end-link::]",
        "[end-para:::True]",
        "[olist(3,4):.:1:6:   :]",
        "[para(3,7):\n   ]",
        '[link(3,7):inline:/me:out::::really test:False:"::\n:]',
        "[text(3,8):really test:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(5,1):3::1]",
        "[para(5,4):]",
        "[text(5,4):three:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li><a href="/me" title="out">test</a>
<ol>
<li><a href="/me" title="out">really test</a></li>
</ol>
</li>
<li>three</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_4b():
    """
    Test case 04b:  A list item can a link split over lines, regardless of any
                    spacing, as a paragraph has already been started.
    """

    # Arrange
    source_markdown = """1. [test](/me
      "out")
   1. [really test](/me
      "out")
1. three"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n   ]",
        '[link(1,4):inline:/me:out::::test:False:"::\n:]',
        "[text(1,5):test:]",
        "[end-link::]",
        "[end-para:::True]",
        "[olist(3,4):.:1:6:   :      ]",
        "[para(3,7):\n]",
        '[link(3,7):inline:/me:out::::really test:False:"::\n:]',
        "[text(3,8):really test:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(5,1):3::1]",
        "[para(5,4):]",
        "[text(5,4):three:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li><a href="/me" title="out">test</a>
<ol>
<li><a href="/me" title="out">really test</a></li>
</ol>
</li>
<li>three</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_5a():
    """
    Test case 05a:  A list item with one level and lazy continuation lines
    """

    # Arrange
    source_markdown = """1. abc
def"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n]",
        "[text(1,4):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
def</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_5b():
    """
    Test case 05a:  A list item with two levels and lazy continuation lines
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
def"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n]",
        "[text(2,7):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc
def</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_5c():
    """
    Test case 05c:  A list item with three levels and lazy continuation lines
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
      1. abc
def"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[olist(3,7):.:1:9:      :]",
        "[para(3,10):\n]",
        "[text(3,10):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc
<ol>
<li>abc
def</li>
</ol>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_5d():
    """
    Test case 05c:  A list item with four levels and lazy continuation lines
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
      1. abc
         1. abc
def"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[olist(3,7):.:1:9:      ]",
        "[para(3,10):]",
        "[text(3,10):abc:]",
        "[end-para:::True]",
        "[olist(4,10):.:1:12:         :]",
        "[para(4,13):\n]",
        "[text(4,13):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc
<ol>
<li>abc
<ol>
<li>abc
def</li>
</ol>
</li>
</ol>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_6xx():
    """
    Test case 06:  the sublist is properly idented, but the start is extra
                   indented to right justify the list
    """

    # Arrange
    source_markdown = """1. Item 1
    1. Item 1a
   10. Item 1b
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):Item 1:]",
        "[end-para:::True]",
        "[olist(2,5):.:1:7:    :]",
        "[para(2,8):]",
        "[text(2,8):Item 1a:]",
        "[end-para:::True]",
        "[li(3,4):7:   :10]",
        "[para(3,8):]",
        "[text(3,8):Item 1b:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item 1
<ol>
<li>Item 1a</li>
<li>Item 1b</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_6xa():
    """
    Test case 06:  the sublist is properly idented, but the list start is aligned
                   to left justify the list
    """

    # Arrange
    source_markdown = """1. Item 1
    1. Item 1a
    10. Item 1b
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):Item 1:]",
        "[end-para:::True]",
        "[olist(2,5):.:1:7:    :]",
        "[para(2,8):]",
        "[text(2,8):Item 1a:]",
        "[end-para:::True]",
        "[li(3,5):8:    :10]",
        "[para(3,9):]",
        "[text(3,9):Item 1b:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item 1
<ol>
<li>Item 1a</li>
<li>Item 1b</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_6xb():
    """
    Test case 06:  the sublist is properly idented, but the start is extra
                   indented to right justify the list
    """

    # Arrange
    source_markdown = """1. Item 1
      1. Item 1a
     10. Item 1b
    100. Item 1c
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):Item 1:]",
        "[end-para:::True]",
        "[olist(2,7):.:1:9:      :]",
        "[para(2,10):]",
        "[text(2,10):Item 1a:]",
        "[end-para:::True]",
        "[li(3,6):9:     :10]",
        "[para(3,10):]",
        "[text(3,10):Item 1b:]",
        "[end-para:::True]",
        "[li(4,5):9:    :100]",
        "[para(4,10):]",
        "[text(4,10):Item 1c:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item 1
<ol>
<li>Item 1a</li>
<li>Item 1b</li>
<li>Item 1c</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_6xc():
    """
    Test case 06:  the sublist is properly idented, but the start is extra
                   indented to right justify the list
    """

    # Arrange
    source_markdown = """  1. Item 1a
 10. Item 1b
100. Item 1c
"""
    expected_tokens = [
        "[olist(1,3):.:1:5:  :]",
        "[para(1,6):]",
        "[text(1,6):Item 1a:]",
        "[end-para:::True]",
        "[li(2,2):5: :10]",
        "[para(2,6):]",
        "[text(2,6):Item 1b:]",
        "[end-para:::True]",
        "[li(3,1):5::100]",
        "[para(3,6):]",
        "[text(3,6):Item 1c:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item 1a</li>
<li>Item 1b</li>
<li>Item 1c</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_6xd():
    """
    Test case 06:  the sublist is properly idented, but the start is extra
                   indented to right justify the list
    """

    # Arrange
    source_markdown = """* First
  * Second
* Third
"""
    expected_tokens = [
        "[ulist(1,1):*::2::]",
        "[para(1,3):]",
        "[text(1,3):First:]",
        "[end-para:::True]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text(2,5):Second:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(3,1):2::]",
        "[para(3,3):]",
        "[text(3,3):Third:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>First
<ul>
<li>Second</li>
</ul>
</li>
<li>Third</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_6xe():
    """
    Test case 06:  the sublist is properly idented, but the start is extra
                   indented to right justify the list
    """

    # Arrange
    source_markdown = """ *  First
    first paragraph

    *  Second

    second paragraph
 *  Third
"""
    expected_tokens = [
        "[ulist(1,2):*::4: :    \n\n    \n]",
        "[para(1,5):\n]",
        "[text(1,5):First\nfirst paragraph::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[ulist(4,5):*::7:    :]",
        "[para(4,8):]",
        "[text(4,8):Second:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[para(6,5):]",
        "[text(6,5):second paragraph:]",
        "[end-para:::True]",
        "[li(7,2):4: :]",
        "[para(7,5):]",
        "[text(7,5):Third:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>First
first paragraph</p>
<ul>
<li>Second</li>
</ul>
<p>second paragraph</p>
</li>
<li>
<p>Third</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_6ax():
    """
    Test case 06:  the sublist is properly idented, but the start is
                   indented an extra space "just because"
    """

    # Arrange
    source_markdown = """1. Item 1
   1. Item 1a
    10. Item 1b
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):Item 1:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):]",
        "[text(2,7):Item 1a:]",
        "[end-para:::True]",
        "[li(3,5):8:    :10]",
        "[para(3,9):]",
        "[text(3,9):Item 1b:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item 1
<ol>
<li>Item 1a</li>
<li>Item 1b</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_6aa():
    """
    Test case 06:  variation of 6ax with extra ident
    """

    # Arrange
    source_markdown = """1. Item 1
    1. Item 1a
      1. Item 1b
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):Item 1:]",
        "[end-para:::True]",
        "[olist(2,5):.:1:7:    :]",
        "[para(2,8):]",
        "[text(2,8):Item 1a:]",
        "[end-para:::True]",
        "[li(3,7):9:      :1]",
        "[para(3,10):]",
        "[text(3,10):Item 1b:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item 1
<ol>
<li>Item 1a</li>
<li>Item 1b</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_6ab():
    """
    Test case 06:  variation of 6ax with extra ident
    """

    # Arrange
    source_markdown = """1. Item 1
    1. Item 1a
       1. Item 1b
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):Item 1:]",
        "[end-para:::True]",
        "[olist(2,5):.:1:7:    ]",
        "[para(2,8):]",
        "[text(2,8):Item 1a:]",
        "[end-para:::True]",
        "[olist(3,8):.:1:10:       :]",
        "[para(3,11):]",
        "[text(3,11):Item 1b:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item 1
<ol>
<li>Item 1a
<ol>
<li>Item 1b</li>
</ol>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_6ac():
    """
    Test case 06:  variation of 6ax with unordered list
    """

    # Arrange
    source_markdown = """1. Item 1
   - Item 1a
    - Item 1b
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):Item 1:]",
        "[end-para:::True]",
        "[ulist(2,4):-::5:   :]",
        "[para(2,6):]",
        "[text(2,6):Item 1a:]",
        "[end-para:::True]",
        "[li(3,5):6:    :]",
        "[para(3,7):]",
        "[text(3,7):Item 1b:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item 1
<ul>
<li>Item 1a</li>
<li>Item 1b</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_6ad():
    """
    Test case 06:  variation of 6ax with first level list being unordered
    """

    # Arrange
    source_markdown = """- Item 1
  1. Item 1a
    2. Item 1b
"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):Item 1:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5:  :]",
        "[para(2,6):]",
        "[text(2,6):Item 1a:]",
        "[end-para:::True]",
        "[li(3,5):7:    :2]",
        "[para(3,8):]",
        "[text(3,8):Item 1b:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Item 1
<ol>
<li>Item 1a</li>
<li>Item 1b</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_blocks_extra_6ae():
    """
    Test case 06:  variation of 6ax with first level list being unordered
    """

    # Arrange
    source_markdown = """- Item 1
  1. Item 1a
  2. Item 1b
"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):Item 1:]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5:  :]",
        "[para(2,6):]",
        "[text(2,6):Item 1a:]",
        "[end-para:::True]",
        "[li(3,3):5:  :2]",
        "[para(3,6):]",
        "[text(3,6):Item 1b:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Item 1
<ol>
<li>Item 1a</li>
<li>Item 1b</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
