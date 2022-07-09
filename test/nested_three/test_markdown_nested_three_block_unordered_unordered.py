"""
Extra tests.
"""
from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> + + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :    ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_with_li1():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly, with a list item.
    """

    # Arrange
    source_markdown = """> + + list
> +   item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  ]",
        "[para(1,7):]",
        "[text(1,7):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,3):6::]",
        "[para(2,7):]",
        "[text(2,7):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list</li>
</ul>
</li>
<li>item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_with_li2():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly, with a list item.
    """

    # Arrange
    source_markdown = """> + + list
>   + item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  ]",
        "[para(1,7):]",
        "[text(1,7):list:]",
        "[end-para:::True]",
        "[li(2,5):6:  :]",
        "[para(2,7):]",
        "[text(2,7):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list</li>
<li>item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_with_li3():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly, with a list item.
    """

    # Arrange
    source_markdown = """> + + list
> + + item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  ]",
        "[para(1,7):]",
        "[text(1,7):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,3):4::]",
        "[ulist(2,5):+::6:  ]",
        "[para(2,7):]",
        "[text(2,7):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list</li>
</ul>
</li>
<li>
<ul>
<li>item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[ulist(3,5):+::6:  :    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
  +
>   + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[BLANK(2,4):]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> \n> ]",
        "[ulist(3,5):+::6:  :    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ul>
<li></li>
</ul>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
    + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :]",
        "[text(3,5):+ list:]",
        "[end-icode-block:::True]",
        "[block-quote(4,1)::> ]",
        "[icode-block(4,7):    :]",
        "[text(4,7):item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>+ list
</code></pre>
<blockquote>
<pre><code>item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_nl_unordered_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[ulist(3,5):+::6:  :    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  + def
>   + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> \n> ]",
        "[ulist(3,5):+::6:  :    ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ul>
<li>def</li>
</ul>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
    + list
>     item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::    \n  ]",
        "[para(2,5):\n\n  ]",
        "[text(2,5):def\n+ list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
+ list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_text_nl_unordered_text_nl_unordered_no_bq3():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_unordered_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> + + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :      ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
>   + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
  +
>   + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[BLANK(2,4):]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> \n]",
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ul>
<li></li>
</ul>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_nl_unordered_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """>
> +
    + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[BLANK(1,2):]",
        "[ulist(2,3):+::4:]",
        "[BLANK(2,4):]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(3,5):    :\n    ]",
        "[text(3,5):+ list\n  item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<pre><code>+ list
  item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_unordered_text_nl_unordered():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
>   + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_unordered_text_nl_unordered_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
  + def
>   + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:  ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> \n]",
        "[ulist(3,5):+::6:  :      ]",
        "[para(3,7):\n]",
        "[text(3,7):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<ul>
<li>def</li>
</ul>
<blockquote>
<ul>
<li>list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_skip_text_nl_unordered_text_nl_unordered_no_bq2():
    """
    Verify that a nesting of block quote, unordered list, unordered list works
    properly.
    """

    # Arrange
    source_markdown = """> abc
> + def
    + list
      item"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4::    \n    ]",
        "[para(2,5):\n\n  ]",
        "[text(2,5):def\n+ list\nitem::\n\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<ul>
<li>def
+ list
item</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    +    + list
   >           item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        :          ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_with_li1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    + list
   >    +      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,9):10:   :]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list</li>
</ul>
</li>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_with_li2():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    + list
   >         + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[li(2,14):15:        :]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list</li>
<li>item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_with_li3():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    + list
   >    +    + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        ]",
        "[para(1,16):]",
        "[text(1,16):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,9):13:   :]",
        "[ulist(2,14):+::15:        ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list</li>
</ul>
</li>
<li>
<ul>
<li>item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_empty():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly.
    """

    # Arrange
    source_markdown = """   >    +    +
   >           item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        :          ]",
        "[BLANK(1,15):]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_empty_with_li1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    +
   >    +      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[li(2,9):10:   :]",
        "[icode-block(2,15):    :]",
        "[text(2,15):item: ]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li></li>
</ul>
</li>
<li>
<pre><code> item
</code></pre>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_empty_with_li2():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    +
   >         + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        ]",
        "[BLANK(1,15):]",
        "[li(2,14):15:        :]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li></li>
<li>item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_empty_with_li3():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    +
   >    +    + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        ]",
        "[BLANK(1,15):]",
        "[end-ulist:::True]",
        "[li(2,9):13:   :]",
        "[ulist(2,14):+::15:        ]",
        "[para(2,16):]",
        "[text(2,16):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li></li>
</ul>
</li>
<li>
<ul>
<li>item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +    + list
               item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        :               ]",
        "[para(1,16):\n]",
        "[text(1,16):list\nitem::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_no_bq1_with_li1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    + list
        +      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        :        ]",
        "[para(1,16):\n]",
        "[text(1,16):list\n+      item::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
+      item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_no_bq1_with_li2():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    + list
             + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        :             ]",
        "[para(1,16):\n]",
        "[text(1,16):list\n+ item::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
+ item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_no_bq1_with_li3():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    + list
        +    + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        :        ]",
        "[para(1,16):\n]",
        "[text(1,16):list\n+    + item::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list
+    + item</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_empty_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +    +
               item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        ]",
        "[BLANK(1,15):]",
        "[end-ulist:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:           ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li></li>
</ul>
</li>
</ul>
</blockquote>
<pre><code>           item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_empty_no_bq1_with_li1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    +
        +      item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        ]",
        "[BLANK(1,15):]",
        "[end-ulist:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):+      item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li></li>
</ul>
</li>
</ul>
</blockquote>
<pre><code>    +      item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_empty_no_bq1_with_li2():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    +
             + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        ]",
        "[BLANK(1,15):]",
        "[end-ulist:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):+ item:         ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li></li>
</ul>
</li>
</ul>
</blockquote>
<pre><code>         + item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_empty_no_bq1_with_li3():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces allowed, and no text on the first line, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """   >    +    +
        +    + item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::13:   ]",
        "[ulist(1,14):+::15:        ]",
        "[BLANK(1,15):]",
        "[end-ulist:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):+    + item:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li></li>
</ul>
</li>
</ul>
</blockquote>
<pre><code>    +    + item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_unordered_max_unordered_max():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly.
    """

    # Arrange
    source_markdown = """    >    +    + list
    >           item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    +    + list\n\a>\a&gt;\a           item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    +    + list
&gt;           item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_plus_one_unordered_max_unordered_max_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces (plus one for the first) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """    >    +    + list
                item"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    ]",
        "[text(1,5):\a>\a&gt;\a    +    + list\n            item:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&gt;    +    + list
            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_plus_one_unordered_max():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >     +    + list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[icode-block(1,10):    :\n    ]",
        "[text(1,10):+    + list\n       item:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>+    + list
       item
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_plus_one_unordered_max_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces (plus one for the second) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >     +    + list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[icode-block(1,10):    :]",
        "[text(1,10):+    + list:]",
        "[end-icode-block:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>+    + list
</code></pre>
</blockquote>
<pre><code>            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_plus_one():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly.
    """

    # Arrange
    source_markdown = """   >    +     + list
   >            item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,9):+::10:   :     ]",
        "[icode-block(1,15):    :\n    ]",
        "[text(1,15):+ list\n  item:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<pre><code>+ list
  item
</code></pre>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_max_unordered_max_unordered_max_plus_one_no_bq1():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    the maximum number of spaces (plus one for the third) allowed, works properly,
    with no block quote characters on the second line.
    """

    # Arrange
    source_markdown = """   >    +     + list
                item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,9):+::10:   ]",
        "[icode-block(1,15):    :]",
        "[text(1,15):+ list:]",
        "[end-icode-block:::False]",
        "[end-ulist:::False]",
        "[end-block-quote:::False]",
        "[icode-block(2,5):    :]",
        "[text(2,5):item:            ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<pre><code>+ list
</code></pre>
</li>
</ul>
</blockquote>
<pre><code>            item
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
