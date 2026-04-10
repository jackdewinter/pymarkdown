"""
Extra tests.
"""

from test.utils import act_and_assert


def test_extra_issue_1574_a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
1. first list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
    1. second list
       > inner block
       > inner block
       ----
       first line
  another fn list
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[olist(2,1):.:1:3:]",
        "[para(2,4):]",
        "[text(2,4):first list:]",
        "[end-para:::True]",
        "[olist(3,4):.:1:6:   :\n\n      \n      \n      \n\n\n       \n       \n\n]",
        "[para(3,7):]",
        "[text(3,7):second list:]",
        "[end-para:::True]",
        "[block-quote(4,7):      :      > \n      > ]",
        "[para(4,9):\n]",
        "[text(4,9):inner block\ninner block::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[tbreak(6,7):-::----]",
        "[para(7,7):\n]",
        "[text(7,7):first line\nanother list::\n]",
        "[end-para:::True]",
        "[li(9,5):7:    :1]",
        "[para(9,8):]",
        "[text(9,8):second list:]",
        "[end-para:::True]",
        "[block-quote(10,8):       :       > \n       > ]",
        "[para(10,10):\n]",
        "[text(10,10):inner block\ninner block::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[tbreak(12,8):-::----]",
        "[para(13,8):\n  ]",
        "[text(13,8):first line\nanother fn list::\n]",
        "[end-para:::True]",
        "[BLANK(15,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>first list
<ol>
<li>second list
<blockquote>
<p>inner block
inner block</p>
</blockquote>
<hr />
first line
another list</li>
<li>second list
<blockquote>
<p>inner block
inner block</p>
</blockquote>
<hr />
first line
another fn list</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
    )


def test_extra_issue_1574_b() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
1. first list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
    1. second list
       > inner block
       > inner block
       ----
       first line
   another fn list
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[olist(2,1):.:1:3:]",
        "[para(2,4):]",
        "[text(2,4):first list:]",
        "[end-para:::True]",
        "[olist(3,4):.:1:6:   :\n\n      \n      \n      \n\n\n       \n       \n\n]",
        "[para(3,7):]",
        "[text(3,7):second list:]",
        "[end-para:::True]",
        "[block-quote(4,7):      :      > \n      > ]",
        "[para(4,9):\n]",
        "[text(4,9):inner block\ninner block::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[tbreak(6,7):-::----]",
        "[para(7,7):\n]",
        "[text(7,7):first line\nanother list::\n]",
        "[end-para:::True]",
        "[li(9,5):7:    :1]",
        "[para(9,8):]",
        "[text(9,8):second list:]",
        "[end-para:::True]",
        "[block-quote(10,8):       :       > \n       > ]",
        "[para(10,10):\n]",
        "[text(10,10):inner block\ninner block::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[tbreak(12,8):-::----]",
        "[para(13,8):\n   ]",
        "[text(13,8):first line\nanother fn list::\n]",
        "[end-para:::True]",
        "[BLANK(15,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>first list
<ol>
<li>second list
<blockquote>
<p>inner block
inner block</p>
</blockquote>
<hr />
first line
another list</li>
<li>second list
<blockquote>
<p>inner block
inner block</p>
</blockquote>
<hr />
first line
another fn list</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
    )


def test_extra_issue_1574_c() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
1. first list
   1. second list
      > inner block
      > inner block
      ----
      first line
      another list
    1. second list
       > inner block
       > inner block
       ----
       first line
    another fn list
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[olist(2,1):.:1:3:]",
        "[para(2,4):]",
        "[text(2,4):first list:]",
        "[end-para:::True]",
        "[olist(3,4):.:1:6:   :\n\n      \n      \n      \n\n\n       \n       \n\n]",
        "[para(3,7):]",
        "[text(3,7):second list:]",
        "[end-para:::True]",
        "[block-quote(4,7):      :      > \n      > ]",
        "[para(4,9):\n]",
        "[text(4,9):inner block\ninner block::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[tbreak(6,7):-::----]",
        "[para(7,7):\n]",
        "[text(7,7):first line\nanother list::\n]",
        "[end-para:::True]",
        "[li(9,5):7:    :1]",
        "[para(9,8):]",
        "[text(9,8):second list:]",
        "[end-para:::True]",
        "[block-quote(10,8):       :       > \n       > ]",
        "[para(10,10):\n]",
        "[text(10,10):inner block\ninner block::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[tbreak(12,8):-::----]",
        "[para(13,8):\n    ]",
        "[text(13,8):first line\nanother fn list::\n]",
        "[end-para:::True]",
        "[BLANK(15,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>first list
<ol>
<li>second list
<blockquote>
<p>inner block
inner block</p>
</blockquote>
<hr />
first line
another list</li>
<li>second list
<blockquote>
<p>inner block
inner block</p>
</blockquote>
<hr />
first line
another fn list</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
    )
