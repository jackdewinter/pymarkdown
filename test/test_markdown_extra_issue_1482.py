"""
Extra tests.
"""

from test.utils import act_and_assert


def test_extra_issue_1482_x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
- a
  - b
    - c
      - d
        > - e
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):-::2:]",
        "[para(2,3):]",
        "[text(2,3):a:]",
        "[end-para:::True]",
        "[ulist(3,3):-::4:  ]",
        "[para(3,5):]",
        "[text(3,5):b:]",
        "[end-para:::True]",
        "[ulist(4,5):-::6:    ]",
        "[para(4,7):]",
        "[text(4,7):c:]",
        "[end-para:::True]",
        "[ulist(5,7):-::8:      :]",
        "[para(5,9):]",
        "[text(5,9):d:]",
        "[end-para:::True]",
        "[block-quote(6,9):        :        > ]",
        "[ulist(6,11):-::12:]",
        "[para(6,13):]",
        "[text(6,13):e:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<ul>
<li>b
<ul>
<li>c
<ul>
<li>d
<blockquote>
<ul>
<li>e</li>
</ul>
</blockquote>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        show_debug=False,
    )


def test_extra_issue_1482_a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
- a
  - b
    - c
      - d
        > e
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):-::2:]",
        "[para(2,3):]",
        "[text(2,3):a:]",
        "[end-para:::True]",
        "[ulist(3,3):-::4:  ]",
        "[para(3,5):]",
        "[text(3,5):b:]",
        "[end-para:::True]",
        "[ulist(4,5):-::6:    ]",
        "[para(4,7):]",
        "[text(4,7):c:]",
        "[end-para:::True]",
        "[ulist(5,7):-::8:      :\n]",
        "[para(5,9):]",
        "[text(5,9):d:]",
        "[end-para:::True]",
        "[block-quote(6,9):        :        > \n]",
        "[para(6,11):]",
        "[text(6,11):e:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<ul>
<li>b
<ul>
<li>c
<ul>
<li>d
<blockquote>
<p>e</p>
</blockquote>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        show_debug=False,
    )


def test_extra_issue_1482_b() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
- a
  - b
    - c
      - d
        > > e
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):-::2:]",
        "[para(2,3):]",
        "[text(2,3):a:]",
        "[end-para:::True]",
        "[ulist(3,3):-::4:  ]",
        "[para(3,5):]",
        "[text(3,5):b:]",
        "[end-para:::True]",
        "[ulist(4,5):-::6:    ]",
        "[para(4,7):]",
        "[text(4,7):c:]",
        "[end-para:::True]",
        "[ulist(5,7):-::8:      :\n]",
        "[para(5,9):]",
        "[text(5,9):d:]",
        "[end-para:::True]",
        "[block-quote(6,9):        :]",
        "[block-quote(6,11):        :        > > \n]",
        "[para(6,13):]",
        "[text(6,13):e:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<ul>
<li>b
<ul>
<li>c
<ul>
<li>d
<blockquote>
<blockquote>
<p>e</p>
</blockquote>
</blockquote>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        show_debug=False,
    )


def test_extra_issue_1482_c() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
- a
  - b
    - c
      - d
        > 
        > - e
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):-::2:]",
        "[para(2,3):]",
        "[text(2,3):a:]",
        "[end-para:::True]",
        "[ulist(3,3):-::4:  ]",
        "[para(3,5):]",
        "[text(3,5):b:]",
        "[end-para:::True]",
        "[ulist(4,5):-::6:    ]",
        "[para(4,7):]",
        "[text(4,7):c:]",
        "[end-para:::True]",
        "[ulist(5,7):-::8:      :\n]",
        "[para(5,9):]",
        "[text(5,9):d:]",
        "[end-para:::True]",
        "[block-quote(6,9):        :        > \n        > ]",
        "[BLANK(6,11):]",
        "[ulist(7,11):-::12:]",
        "[para(7,13):]",
        "[text(7,13):e:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<ul>
<li>b
<ul>
<li>c
<ul>
<li>d
<blockquote>
<ul>
<li>e</li>
</ul>
</blockquote>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        show_debug=False,
    )


def test_extra_issue_1482_d() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
- a
  - b
    - c
      > - d
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):-::2:]",
        "[para(2,3):]",
        "[text(2,3):a:]",
        "[end-para:::True]",
        "[ulist(3,3):-::4:  ]",
        "[para(3,5):]",
        "[text(3,5):b:]",
        "[end-para:::True]",
        "[ulist(4,5):-::6:    :]",
        "[para(4,7):]",
        "[text(4,7):c:]",
        "[end-para:::True]",
        "[block-quote(5,7):      :      > ]",
        "[ulist(5,9):-::10:]",
        "[para(5,11):]",
        "[text(5,11):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<ul>
<li>b
<ul>
<li>c
<blockquote>
<ul>
<li>d</li>
</ul>
</blockquote>
</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        show_debug=False,
    )


def test_extra_issue_1482_e() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
- a
  - b
    - c
      - d
        > e
        > - f
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):-::2:]",
        "[para(2,3):]",
        "[text(2,3):a:]",
        "[end-para:::True]",
        "[ulist(3,3):-::4:  ]",
        "[para(3,5):]",
        "[text(3,5):b:]",
        "[end-para:::True]",
        "[ulist(4,5):-::6:    ]",
        "[para(4,7):]",
        "[text(4,7):c:]",
        "[end-para:::True]",
        "[ulist(5,7):-::8:      :\n]",
        "[para(5,9):]",
        "[text(5,9):d:]",
        "[end-para:::True]",
        "[block-quote(6,9):        :        > \n        > ]",
        "[para(6,11):]",
        "[text(6,11):e:]",
        "[end-para:::True]",
        "[ulist(7,11):-::12:]",
        "[para(7,13):]",
        "[text(7,13):f:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<ul>
<li>b
<ul>
<li>c
<ul>
<li>d
<blockquote>
<p>e</p>
<ul>
<li>f</li>
</ul>
</blockquote>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        show_debug=False,
    )


def test_extra_issue_1482_f() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
- a
  - b
    - c
      - d
        - e
          > - f
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):-::2:]",
        "[para(2,3):]",
        "[text(2,3):a:]",
        "[end-para:::True]",
        "[ulist(3,3):-::4:  ]",
        "[para(3,5):]",
        "[text(3,5):b:]",
        "[end-para:::True]",
        "[ulist(4,5):-::6:    ]",
        "[para(4,7):]",
        "[text(4,7):c:]",
        "[end-para:::True]",
        "[ulist(5,7):-::8:      ]",
        "[para(5,9):]",
        "[text(5,9):d:]",
        "[end-para:::True]",
        "[ulist(6,9):-::10:        :]",
        "[para(6,11):]",
        "[text(6,11):e:]",
        "[end-para:::True]",
        "[block-quote(7,11):          :          > ]",
        "[ulist(7,13):-::14:]",
        "[para(7,15):]",
        "[text(7,15):f:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<ul>
<li>b
<ul>
<li>c
<ul>
<li>d
<ul>
<li>e
<blockquote>
<ul>
<li>f</li>
</ul>
</blockquote>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        show_debug=False,
    )


def test_extra_issue_1482_g() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
- a
  - b
    - c
      - d
        - e
          > f
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):-::2:]",
        "[para(2,3):]",
        "[text(2,3):a:]",
        "[end-para:::True]",
        "[ulist(3,3):-::4:  ]",
        "[para(3,5):]",
        "[text(3,5):b:]",
        "[end-para:::True]",
        "[ulist(4,5):-::6:    ]",
        "[para(4,7):]",
        "[text(4,7):c:]",
        "[end-para:::True]",
        "[ulist(5,7):-::8:      ]",
        "[para(5,9):]",
        "[text(5,9):d:]",
        "[end-para:::True]",
        "[ulist(6,9):-::10:        :\n]",
        "[para(6,11):]",
        "[text(6,11):e:]",
        "[end-para:::True]",
        "[block-quote(7,11):          :          > \n]",
        "[para(7,13):]",
        "[text(7,13):f:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<ul>
<li>b
<ul>
<li>c
<ul>
<li>d
<ul>
<li>e
<blockquote>
<p>f</p>
</blockquote>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
    )


def test_extra_issue_1482_h() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
- a
  > b
  > - c
  >   > d
  >   > - e
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):-::2::\n]",
        "[para(2,3):]",
        "[text(2,3):a:]",
        "[end-para:::True]",
        "[block-quote(3,3):  :  > \n  > \n  > ]",
        "[para(3,5):]",
        "[text(3,5):b:]",
        "[end-para:::True]",
        "[ulist(4,5):-::6::]",
        "[para(4,7):]",
        "[text(4,7):c:]",
        "[end-para:::True]",
        "[block-quote(5,7)::> \n  >   > ]",
        "[para(5,9):]",
        "[text(5,9):d:]",
        "[end-para:::True]",
        "[ulist(6,9):-::10:]",
        "[para(6,11):]",
        "[text(6,11):e:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<blockquote>
<p>b</p>
<ul>
<li>c
<blockquote>
<p>d</p>
<ul>
<li>e</li>
</ul>
</blockquote>
</li>
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
