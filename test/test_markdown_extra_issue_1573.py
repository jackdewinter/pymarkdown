"""
Extra tests.
"""

from test.utils import act_and_assert


def test_extra_issue_1573_a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
> 1. first list
>    1. inner list
        properly indented content
>    1. another list
>        properly indented content
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
        "[para(5,9):\n ]",
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


def test_extra_issue_1573_b() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
1. > first list
   > 1. inner list
        properly indented content
   > 1. another list
        properly indented content
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[olist(2,1):.:1:3::]",
        "[block-quote(2,4):   :   > \n   > \n\n   > \n]",
        "[para(2,6):]",
        "[text(2,6):first list:]",
        "[end-para:::True]",
        "[olist(3,6):.:1:8::        \n        ]",
        "[para(3,9):\n]",
        "[text(3,9):inner list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[li(5,6):8::1]",
        "[para(5,9):\n]",
        "[text(5,9):another list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>first list</p>
<ol>
<li>inner list
properly indented content</li>
<li>another list
properly indented content</li>
</ol>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
    )
