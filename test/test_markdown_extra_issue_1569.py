"""
Extra tests.
"""

from test.utils import act_and_assert


def test_extra_issue_1569_a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
> 1. first list
>    1. inner list
        properly indented content
>    1. another list
>      properly indented content
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[block-quote(2,1)::> \n> \n\n> \n> ]",
        "[olist(2,3):.:1:5:]",
        "[para(2,6):]",
        "[text(2,6):first list:]",
        "[end-para:::True]",
        "[olist(3,6):.:1:8:   :        \n     ]",
        "[para(3,9):\n]",
        "[text(3,9):inner list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[li(5,6):8:   :1]",
        "[para(5,9):\n]",
        "[text(5,9):another list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>first list
<ol>
<li>inner list
properly indented content</li>
<li>another list
properly indented content</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
    )


def test_extra_issue_1569_b() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
> 1. first list
>    1. inner list
        properly indented content
>    1. another list
>       properly indented content
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[block-quote(2,1)::> \n> \n\n> \n> ]",
        "[olist(2,3):.:1:5:]",
        "[para(2,6):]",
        "[text(2,6):first list:]",
        "[end-para:::True]",
        "[olist(3,6):.:1:8:   :        \n      ]",
        "[para(3,9):\n]",
        "[text(3,9):inner list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[li(5,6):8:   :1]",
        "[para(5,9):\n]",
        "[text(5,9):another list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>first list
<ol>
<li>inner list
properly indented content</li>
<li>another list
properly indented content</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
    )


def test_extra_issue_1569_c() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
+ > first list
  > + inner list
  >  properly indented content
  > + another list
      properly indented content
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):+::2::]",
        "[block-quote(2,3):  :  > \n  > \n  > \n  > \n]",
        "[para(2,5):]",
        "[text(2,5):first list:]",
        "[end-para:::True]",
        "[ulist(3,5):+::6:: \n      ]",
        "[para(3,7):\n]",
        "[text(3,7):inner list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[li(5,5):6::]",
        "[para(5,7):\n]",
        "[text(5,7):another list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<p>first list</p>
<ul>
<li>inner list
properly indented content</li>
<li>another list
properly indented content</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
    )
