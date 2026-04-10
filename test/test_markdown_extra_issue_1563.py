"""
Extra tests.
"""

from test.utils import act_and_assert


def test_extra_issue_1563_a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
> a block
>
> 1. another list
     properly indented content
>  1. another list
      properly indented content
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[block-quote(2,1)::> \n>\n> \n\n> \n]",
        "[para(2,3):]",
        "[text(2,3):a block:]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[olist(4,3):.:1:5::     \n      ]",
        "[para(4,6):\n]",
        "[text(4,6):another list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[li(6,4):6: :1]",
        "[para(6,7):\n]",
        "[text(6,7):another list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<p>a block</p>
<ol>
<li>another list
properly indented content</li>
<li>another list
properly indented content</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_extra_issue_1563_b() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
> a block
>
> 1. another list
     properly indented content
> 1. another list
     properly indented content
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[block-quote(2,1)::> \n>\n> \n\n> \n]",
        "[para(2,3):]",
        "[text(2,3):a block:]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[olist(4,3):.:1:5::     \n     ]",
        "[para(4,6):\n]",
        "[text(4,6):another list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[li(6,3):5::1]",
        "[para(6,6):\n]",
        "[text(6,6):another list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<p>a block</p>
<ol>
<li>another list
properly indented content</li>
<li>another list
properly indented content</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_extra_issue_1563_c() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
> a block
>
> 1. another list
     properly indented content
>  1. another list
      properly indented content
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[block-quote(2,1)::> \n>\n> \n\n> \n]",
        "[para(2,3):]",
        "[text(2,3):a block:]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[olist(4,3):.:1:5::     \n      ]",
        "[para(4,6):\n]",
        "[text(4,6):another list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[li(6,4):6: :1]",
        "[para(6,7):\n]",
        "[text(6,7):another list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<p>a block</p>
<ol>
<li>another list
properly indented content</li>
<li>another list
properly indented content</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_extra_issue_1563_d() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
> > a block
> >
> > 1. another list
> >   improperly indented content
> > 1. another list
       properly indented content
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[block-quote(2,1)::]",
        "[block-quote(2,3)::> > \n> >\n> > \n> > \n> > \n]",
        "[para(2,5):]",
        "[text(2,5):a block:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[olist(4,5):.:1:7::  \n       ]",
        "[para(4,8):\n]",
        "[text(4,8):another list\nimproperly indented content::\n]",
        "[end-para:::True]",
        "[li(6,5):7::1]",
        "[para(6,8):\n]",
        "[text(6,8):another list\nproperly indented content::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>a block</p>
<ol>
<li>another list
improperly indented content</li>
<li>another list
properly indented content</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
    )
