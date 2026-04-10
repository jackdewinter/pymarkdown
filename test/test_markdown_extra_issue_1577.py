"""
Extra tests.
"""

from test.utils import act_and_assert


def test_extra_issue_1577_a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
> block start
>
> + first list
>   > block within list
>   ----
>   first line
>   another list
>  + second list
>    > block within list
>    ----
>    first line
>    another list
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[block-quote(2,1)::> \n>\n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[para(2,3):]",
        "[text(2,3):block start:]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[ulist(4,3):+::4::\n  þ\n  \n  \n\n   þ\n   \n   ]",
        "[para(4,5):]",
        "[text(4,5):first list:]",
        "[end-para:::True]",
        "[block-quote(5,5)::> \n> ]",
        "[para(5,7):]",
        "[text(5,7):block within list:]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[tbreak(6,5):-::----]",
        "[para(7,5):\n]",
        "[text(7,5):first line\nanother list::\n]",
        "[end-para:::True]",
        "[li(9,4):5: :]",
        "[para(9,6):]",
        "[text(9,6):second list:]",
        "[end-para:::True]",
        "[block-quote(10,6)::> \n> ]",
        "[para(10,8):]",
        "[text(10,8):block within list:]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[tbreak(11,6):-::----]",
        "[para(12,6):\n]",
        "[text(12,6):first line\nanother list::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(14,1):]",
    ]
    expected_gfm = """<blockquote>
<p>block start</p>
<ul>
<li>first list
<blockquote>
<p>block within list</p>
</blockquote>
<hr />
first line
another list</li>
<li>second list
<blockquote>
<p>block within list</p>
</blockquote>
<hr />
first line
another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        show_debug=False,
    )


def test_extra_issue_1577_b() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
> block start
>
> + first list
>   > block within list
>   ----
>   first line
>   another list
> + second list
>   > block within list
>   ----
>   first line
>   another list
>  + third list
>    > block within list
>    ----
>    first line
>    another list
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[block-quote(2,1)::> \n>\n> \n> \n> \n> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[para(2,3):]",
        "[text(2,3):block start:]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[ulist(4,3):+::4::\n  þ\n  \n  \n\n  þ\n  \n  \n\n   þ\n   \n   ]",
        "[para(4,5):]",
        "[text(4,5):first list:]",
        "[end-para:::True]",
        "[block-quote(5,5)::> \n> ]",
        "[para(5,7):]",
        "[text(5,7):block within list:]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[tbreak(6,5):-::----]",
        "[para(7,5):\n]",
        "[text(7,5):first line\nanother list::\n]",
        "[end-para:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):second list:]",
        "[end-para:::True]",
        "[block-quote(10,5)::> \n> ]",
        "[para(10,7):]",
        "[text(10,7):block within list:]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[tbreak(11,5):-::----]",
        "[para(12,5):\n]",
        "[text(12,5):first line\nanother list::\n]",
        "[end-para:::True]",
        "[li(14,4):5: :]",
        "[para(14,6):]",
        "[text(14,6):third list:]",
        "[end-para:::True]",
        "[block-quote(15,6)::> \n> ]",
        "[para(15,8):]",
        "[text(15,8):block within list:]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[tbreak(16,6):-::----]",
        "[para(17,6):\n]",
        "[text(17,6):first line\nanother list::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(19,1):]",
    ]
    expected_gfm = """<blockquote>
<p>block start</p>
<ul>
<li>first list
<blockquote>
<p>block within list</p>
</blockquote>
<hr />
first line
another list</li>
<li>second list
<blockquote>
<p>block within list</p>
</blockquote>
<hr />
first line
another list</li>
<li>third list
<blockquote>
<p>block within list</p>
</blockquote>
<hr />
first line
another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        show_debug=False,
    )
