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


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_nl_extra_block_drop_block_thematics_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    a new line and an extra block quote, drop the block quote, and then thematics around
    a fenced block.

    was: test_extra_044mct0
    refs: bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_with_thematics
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>     -----
>     ```block
>     A code block
>     ```
>     -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n  þ\n    \n    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   :True]",
        "[tbreak(4,7):-::-----]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-ulist:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_nl_extra_block_drop_block__with_thematics_around_blanks_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    a new line and an extra block quote, drop the block quote, and then thematics around
    a fenced block.

    was: test_extra_044mct1
    refs: bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_with_thematics
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>     -----
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n  þ\n\n    \n    \n    \n\n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   :True]",
        "[tbreak(4,7):-::-----]",
        "[BLANK(5,2):]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,7):-::-----]",
        "[end-ulist:::True]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_nl_extra_list_li_drop_list_with_thematics_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    a new line and an extra list, drop the block list, and then thematics around
    a fenced block.

    was: test_extra_044mcs0
    refs: bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_and_thematics
    """
    # Arrange
    source_markdown = """> + + -----
>     + list 1
>       list 2
>     + list 3
>     -----
>     ```block
>     A code block
>     ```
>     -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :    \n    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:    :      \n    ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):-::-----]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::-----]",
        "[end-ulist:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_nl_extra_list_li_drop_list_with_thematics_around_blanks_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    a new line and an extra list, drop the block list, and then thematics around
    blanks around a fenced block.

    was: test_extra_044mcs1
    refs: bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_and_thematics
    """
    # Arrange
    source_markdown = """> + + -----
>     + list 1
>       list 2
>     + list 3
>     -----
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n    \n    \n    \n\n    ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:    :      \n    ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):-::-----]",
        "[BLANK(6,2):]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,2):]",
        "[tbreak(11,7):-::-----]",
        "[end-ulist:::True]",
        "[li(12,3):4::]",
        "[para(12,5):]",
        "[text(12,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_nl_extra_block_drop_block_with_thematics_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    a new line and an extra block, drop the block, and then thematics around
    a fenced block.

    was: test_extra_044mcz0x
    refs: bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>     ```block
>     A code block
>     ```
>     -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n  þ\n    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   :True]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,7):-::-----]",
        "[end-ulist:::True]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_nl_extra_block_drop_block_with_thematics_around_blanks_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, with
    a new line and an extra block, drop the block, and then thematics around
    blanks around a fenced block.

    was: test_extra_044mcz0a
    refs: bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n\n    \n    \n    \n\n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n>]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[tbreak(9,7):-::-----]",
        "[end-ulist:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_drop_list_with_text_and_thematics_around_blanks_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_046dx
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_and_para_continue_with_thematics
    """
    # Arrange
    source_markdown = """> + list 1
>   + list 2
>   list 3
>   ------
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::\n  \n  \n  \n\n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :  \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::------]",
        "[BLANK(5,2):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,5):-::------]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<ul>
<li>list 2
list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_drop_list_with_text_and_thematics_around_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_046x
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_and_para_continue_with_thematics
    """
    # Arrange
    source_markdown = """> + list 1
>   + list 2
>   list 3
>   ------
>   ```block
>   A code block
>   ```
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :  \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::------]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::------]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<ul>
<li>list 2
list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_li_drop_list_with_thematics_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with thematics around fenced.

    was: test_extra_046e0
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_with_thematics_sub3
    """
    # Arrange
    source_markdown = """> + list 1
>   + list 2
>   + list 3
>   _____
>   ```block
>   A code block
>   ```
>   _____
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :  ]",
        "[para(2,7):]",
        "[text(2,7):list 2:]",
        "[end-para:::True]",
        "[li(3,5):6:  :]",
        "[para(3,7):]",
        "[text(3,7):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):_::_____]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):_::_____]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<ul>
<li>list 2</li>
<li>list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_li_drop_list_with_thematics_around_blanks_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with thematics around fenced.

    was: test_extra_046e1, test_extra_046b
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_with_thematics_sub3
    """
    # Arrange
    source_markdown = """> + list 1
>   + list 2
>   + list 3
>   _____
>
>   ```block
>   A code block
>   ```
>
>   _____
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::\n  \n  \n  \n\n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :  ]",
        "[para(2,7):]",
        "[text(2,7):list 2:]",
        "[end-para:::True]",
        "[li(3,5):6:  :]",
        "[para(3,7):]",
        "[text(3,7):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):_::_____]",
        "[BLANK(5,2):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,5):_::_____]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<ul>
<li>list 2</li>
<li>list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_drop_list_with_thematics_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with thematics around fenced.

    was: test_extra_044cx
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_with_thematics
    """
    # Arrange
    source_markdown = """> + list 1
>   + list 2
>     list 3
>   ------
>   ```block
>   A code block
>   ```
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :    \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::------]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::------]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<ul>
<li>list 2
list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_drop_list_with_thematics_around_blanks_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with thematics around fenced.

    was: test_extra_044ca
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_with_thematics
    """
    # Arrange
    source_markdown = """> + list 1
>   + list 2
>     list 3
>   ------
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::\n  \n  \n  \n\n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :    \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::------]",
        "[BLANK(5,2):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,5):-::------]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<ul>
<li>list 2
list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_drop_double_list_with_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with thematics around fenced.

    was: test_extra_046f0a
    """
    # Arrange
    source_markdown = """> + list 1
>   + list 2
>     list 3
> ```block
> A code block
> ```
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :    \n]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[ulist(7,3):+::4:]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<ul>
<li>list 2
list 3</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<ul>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_drop_list_with_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with thematics around fenced.

    was: test_extra_046f0
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_list
    """
    # Arrange
    source_markdown = """> + list 1
>   + list 2
>     list 3
>   ```block
>   A code block
>   ```
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :    \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<ul>
<li>list 2
list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_drop_list_with_blanks_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with thematics around fenced.

    was: test_extra_046f1
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_list
    """
    # Arrange
    source_markdown = """> + list 1
>   + list 2
>     list 3
>
>   ```block
>   A code block
>   ```
>
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> \n> \n> \n>\n> ]",
        "[ulist(1,3):+::4::  \n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :    \n\n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-ulist:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<ul>
<li>list 2
list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_para_cont_drop_list_with_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with thematics around fenced.

    was: test_extra_046da
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_and_para_continue
    """
    # Arrange
    source_markdown = """> + list 1
>   + list 2
>   list 3
>   ```block
>   A code block
>   ```
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :  \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,5):-::------]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<ul>
<li>list 2
list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_para_cont_drop_list_with_blanks_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with thematics around fenced.

    was: test_extra_046db
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_and_para_continue
    """
    # Arrange
    source_markdown = """> + list 1
>   + list 2
>   list 3
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n\n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :  \n\n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-ulist:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[tbreak(9,5):-::------]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<ul>
<li>list 2
list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_extra_list_li_drop_list_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_046cc0
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_and_para_continue_with_thematics
    """
    # Arrange
    source_markdown = """> + + -----
>     + list 1
>       list 2
>     + list 3
>     ```block
>     A code block
>     ```
>     -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:    :      \n    ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-ulist:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_extra_list_li_drop_list_blanks_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_046cc1
    refs: bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_and_para_continue_with_thematics
    """
    # Arrange
    source_markdown = """> + + -----
>     + list 1
>       list 2
>     + list 3
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :    \n    \n\n    ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:    :      \n\n    ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[BLANK(5,2):]",
        "[end-ulist:::True]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,7):-::-----]",
        "[end-ulist:::True]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_extra_list_li_drop_list_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_046cc2
    """
    # Arrange
    source_markdown = """> +
>   + -----
>     + list 1
>       list 2
>     + list 3
>     ```block
>     A code block
>     ```
>     -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[BLANK(1,4):]",
        "[ulist(2,5):+::6:  :    \n    \n    ]",
        "[tbreak(2,7):-::-----]",
        "[ulist(3,7):+::8:    :      \n    ]",
        "[para(3,9):\n]",
        "[text(3,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(5,7):8:    :]",
        "[para(5,9):]",
        "[text(5,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::-----]",
        "[end-ulist:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_extra_list_li_drop_list_blanks_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_046cc3
    """
    # Arrange
    source_markdown = """> +
>   + -----
>     + list 1
>       list 2
>     + list 3
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[BLANK(1,4):]",
        "[ulist(2,5):+::6:  :    \n    \n\n    ]",
        "[tbreak(2,7):-::-----]",
        "[ulist(3,7):+::8:    :      \n\n    ]",
        "[para(3,9):\n]",
        "[text(3,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(5,7):8:    :]",
        "[para(5,9):]",
        "[text(5,9):list 3:]",
        "[end-para:::True]",
        "[BLANK(6,2):]",
        "[end-ulist:::True]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,2):]",
        "[tbreak(11,7):-::-----]",
        "[end-ulist:::True]",
        "[li(12,3):4::]",
        "[para(12,5):]",
        "[text(12,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(13,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_thematics_unordered_extra_list_drop_list_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_046cc4
    """
    # Arrange
    source_markdown = """> +
>   + -----
>     + list 1
>       list 2
>     ```block
>     A code block
>     ```
>     -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[BLANK(1,4):]",
        "[ulist(2,5):+::6:  :    \n    \n    ]",
        "[tbreak(2,7):-::-----]",
        "[ulist(3,7):+::8:    :      \n    ]",
        "[para(3,9):\n]",
        "[text(3,9):list 1\nlist 2::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-ulist:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_nl_unordered_extra_list_drop_listx_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_046cc5
    """
    # Arrange
    source_markdown = """> +
>   + list 1
>     list 2
>   + list 3
>   ```block
>   A code block
>   ```
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  ]",
        "[BLANK(1,4):]",
        "[ulist(2,5):+::6:  :    \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,5):6:  :]",
        "[para(4,7):]",
        "[text(4,7):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::-----]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_extra_block_drop_block_headings_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_044ldb0
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>     # before
>     ```block
>     A code block
>     ```
>     # after
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n  þ\n    \n    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   :True]",
        "[atx(4,7):1:0:]",
        "[text(4,9):before: ]",
        "[end-atx::]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[atx(8,7):1:0:]",
        "[text(8,9):after: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<h1>before</h1>
<pre><code class="language-block">A code block
</code></pre>
<h1>after</h1>
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_extra_block_drop_block_html_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_044ldb1
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>     <!-- before -->
>     ```block
>     A code block
>     ```
>     <!-- after -->
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n  þ\n    \n    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   :True]",
        "[html-block(4,7)]",
        "[text(4,7):<!-- before -->:]",
        "[end-html-block:::False]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[html-block(8,7)]",
        "[text(8,7):<!-- after -->:]",
        "[end-html-block:::False]",
        "[end-ulist:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<!-- before -->
<pre><code class="language-block">A code block
</code></pre>
<!-- after -->
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_extra_block_with_extra_space_indent_drop_block_html_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_044ldb1a
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>    <!-- before -->
>    ```block
>    A code block
>    ```
>    <!-- after -->
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  ]",
        "[ulist(1,5):+::6:  :\n\n  þ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[html-block(4,5)]",
        "[text(4,6):<!-- before -->: ]",
        "[end-html-block:::False]",
        "[fcode-block(5,6):`:3:block:::: :]",
        "[text(6,5):A code block:\a \a\x03\a]",
        "[end-fcode-block: ::3:False]",
        "[html-block(8,5)]",
        "[text(8,6):<!-- after -->: ]",
        "[end-html-block:::False]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
 <!-- before -->
<pre><code class="language-block">A code block
</code></pre>
 <!-- after -->
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_extra_block_drop_list_html_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_044ldb1c
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>   <!-- before -->
>   ```block
>   A code block
>   ```
>   <!-- after -->
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  ]",
        "[ulist(1,5):+::6:  :\n\n  þ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[html-block(4,5)]",
        "[text(4,5):<!-- before -->:]",
        "[end-html-block:::False]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[html-block(8,5)]",
        "[text(8,5):<!-- after -->:]",
        "[end-html-block:::False]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<!-- before -->
<pre><code class="language-block">A code block
</code></pre>
<!-- after -->
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_extra_block_drop_list_extra_indent_html_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_044ldb1d
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>  <!-- before -->
>  ```block
>  A code block
>  ```
>  <!-- after -->
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[html-block(4,3)]",
        "[text(4,4):<!-- before -->: ]",
        "[end-html-block:::False]",
        "[fcode-block(5,4):`:3:block:::: :]",
        "[text(6,3):A code block:\a \a\x03\a]",
        "[end-fcode-block: ::3:False]",
        "[html-block(8,3)]",
        "[text(8,4):<!-- after -->: ]",
        "[end-html-block:::False]",
        "[ulist(9,3):+::4:]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
 <!-- before -->
<pre><code class="language-block">A code block
</code></pre>
 <!-- after -->
<ul>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_extra_block_drop_block_drop_list_drop_list_html_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_044ldb1e
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
> <!-- before -->
> ```block
> A code block
> ```
> <!-- after -->
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[html-block(4,3)]",
        "[text(4,3):<!-- before -->:]",
        "[end-html-block:::False]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[html-block(8,3)]",
        "[text(8,3):<!-- after -->:]",
        "[end-html-block:::False]",
        "[ulist(9,3):+::4:]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<!-- before -->
<pre><code class="language-block">A code block
</code></pre>
<!-- after -->
<ul>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_extra_block_drop_block_drop_list_thematics_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_044ldc
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>   -----
>   ```block
>   A code block
>   ```
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  ]",
        "[ulist(1,5):+::6:  :\n\n  þ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::-----]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::-----]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_extra_list_li_drop_list_thematics_around_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_044lea
    """
    # Arrange
    source_markdown = """> + + ______
>     + list 1
>       list 2
>     + list 3
>     ______
>     ```block
>     A code block
>     ```
>     ______
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :    \n    \n    \n    ]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:    :      \n    ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):_::______]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):_::______]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_extra_block_drop_double_list_fenced():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_044mcz5
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
> ```block
> A code block
> ```
> -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,3):-::-----]",
        "[ulist(8,3):+::4:]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<ul>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_nested_three_block_unordered_unordered_extra_block_drop_double_list_fenced_squashed_against_block_quote():
    """
    Verify that a nesting of block quote, unordered list, unordered list, dropping
    the new list, with text and thematics around fenced.

    was: test_extra_044mcz6
    """
    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>```block
>A code block
>```
>-----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>\n>\n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n>]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,2):`:3:block:::::]",
        "[text(5,2):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,2):-::-----]",
        "[ulist(8,3):+::4:]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<ul>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
