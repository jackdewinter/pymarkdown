"""
Testing various aspects of whitespaces around emphasis.
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_emphasis_1x() -> None:
    """
    Test case:  open left is followed by whitespace
    """

    # Arrange
    source_markdown = """* *"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[ulist(1,3):*::4:  ]",
        "[BLANK(1,4):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li></li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1xa() -> None:
    """
    Test case:  open left is followed by whitespace
    """

    # Arrange
    source_markdown = """** **"""
    expected_tokens = ["[tbreak(1,1):*::** **]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1a() -> None:
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """*\u00a0*"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):*\u00a0*:]", "[end-para:::True]"]
    expected_gfm = """<p>*\u00a0*</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1ax() -> None:
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """**\u00a0**"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):**\u00a0**:]", "[end-para:::True]"]
    expected_gfm = """<p>**\u00a0**</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1b() -> None:
    """
    Test case:  open left is followed by whitespace
    """

    # Arrange
    source_markdown = """_ _"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):_ _:]", "[end-para:::True]"]
    expected_gfm = """<p>_ _</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1bx() -> None:
    """
    Test case:  open left is followed by whitespace
    """

    # Arrange
    source_markdown = """__ __"""
    expected_tokens = ["[tbreak(1,1):_::__ __]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1c() -> None:
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """_\u00a0_"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):_\u00a0_:]", "[end-para:::True]"]
    expected_gfm = """<p>_\u00a0_</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1cx() -> None:
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """__\u00a0__"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):__\u00a0__:]", "[end-para:::True]"]
    expected_gfm = """<p>__\u00a0__</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1d() -> None:
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """*\u2000*"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):*\u2000*:]", "[end-para:::True]"]
    expected_gfm = """<p>*\u2000*</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1dx() -> None:
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """**\u2000**"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):**\u2000**:]", "[end-para:::True]"]
    expected_gfm = """<p>**\u2000**</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1e() -> None:
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """_\u2000_"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):_\u2000_:]", "[end-para:::True]"]
    expected_gfm = """<p>_\u2000_</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_1ex() -> None:
    """
    Test case:  open left is followed by unicode whitespace
    """

    # Arrange
    source_markdown = """__\u2000__"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):__\u2000__:]", "[end-para:::True]"]
    expected_gfm = """<p>__\u2000__</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_2x() -> None:
    """
    Test case:  open left is not followed by unicode whitespace or punctuation
    """

    # Arrange
    source_markdown = """_a_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):a:]",
        "[end-emphasis(1,3)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>a</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_2xx() -> None:
    """
    Test case:  open left is not followed by unicode whitespace or punctuation
    """

    # Arrange
    source_markdown = """__a__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):a:]",
        "[end-emphasis(1,4)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>a</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_2a() -> None:
    """
    Test case:  open left is not followed by unicode whitespace or punctuation
    """

    # Arrange
    source_markdown = """*a*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):a:]",
        "[end-emphasis(1,3)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>a</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_2ax() -> None:
    """
    Test case:  open left is not followed by unicode whitespace or punctuation
    """

    # Arrange
    source_markdown = """**a**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):a:]",
        "[end-emphasis(1,4)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>a</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3x() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """*.foo.*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):.foo.:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>.foo.</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3xx() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """**.foo.**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>.foo.</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3a() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """*\u007efoo\u007e*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):~foo~:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>~foo~</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3ax() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """**\u007efoo\u007e**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):~foo~:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>~foo~</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3b() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """_.foo._"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):.foo.:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>.foo.</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3bx() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """__.foo.__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>.foo.</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3c() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """_\u007efoo\u007e_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):~foo~:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>~foo~</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3cx() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """__\u007efoo\u007e__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):~foo~:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>~foo~</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3d() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line Pc
    """

    # Arrange
    source_markdown = """*\u203ffoo\u203f*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):\u203ffoo\u203f:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>\u203ffoo\u203f</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3dx() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line Pc
    """

    # Arrange
    source_markdown = """**\u203ffoo\u203f**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):\u203ffoo\u203f:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>\u203ffoo\u203f</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3e() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line Pc
    """

    # Arrange
    source_markdown = """_\u203ffoo\u203f_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):\u203ffoo\u203f:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>\u203ffoo\u203f</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_3ex() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by beginning of line
    """

    # Arrange
    source_markdown = """__\u203ffoo\u203f__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):\u203ffoo\u203f:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>\u203ffoo\u203f</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4x() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """ *.foo.* """
    expected_tokens = [
        "[para(1,2): : ]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>.foo.</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4xa() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """ **.foo.** """
    expected_tokens = [
        "[para(1,2): : ]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>.foo.</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4a() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u00a0*.foo.*\u00a0"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u00a0:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):\u00a0:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u00a0<em>.foo.</em>\u00a0</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4ax() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u00a0**.foo.**\u00a0"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u00a0:]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):\u00a0:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u00a0<strong>.foo.</strong>\u00a0</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4b() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """ _.foo._ """
    expected_tokens = [
        "[para(1,2): : ]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>.foo.</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4bx() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """ __.foo.__ """
    expected_tokens = [
        "[para(1,2): : ]",
        "[emphasis(1,2):2:_]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>.foo.</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4c() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u00a0_.foo._\u00a0"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u00a0:]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):\u00a0:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u00a0<em>.foo.</em>\u00a0</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4cx() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u00a0__.foo.__\u00a0"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u00a0:]",
        "[emphasis(1,2):2:_]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):\u00a0:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u00a0<strong>.foo.</strong>\u00a0</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4d() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u2000*.foo.*\u2000"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u2000:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):\u2000:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u2000<em>.foo.</em>\u2000</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4dx() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u2000**.foo.**\u2000"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u2000:]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):\u2000:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u2000<strong>.foo.</strong>\u2000</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4e() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u2000_.foo._\u2000"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u2000:]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):\u2000:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u2000<em>.foo.</em>\u2000</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_4ex() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by whitespace
    """

    # Arrange
    source_markdown = """\u2000__.foo.__\u2000"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\u2000:]",
        "[emphasis(1,2):2:_]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):\u2000:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u2000<strong>.foo.</strong>\u2000</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5x() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """.*.foo.*."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):.:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>.<em>.foo.</em>.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5xx() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """.**.foo.**."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):.:]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>.<strong>.foo.</strong>.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5a() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u007e*.foo.*\u007e"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):~:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):~:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>~<em>.foo.</em>~</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5ax() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u007e**.foo.**\u007e"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):~:]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):~:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>~<strong>.foo.</strong>~</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5b() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """._.foo._."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):.:]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>.<em>.foo.</em>.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5bx() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """.__.foo.__."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):.:]",
        "[emphasis(1,2):2:_]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>.<strong>.foo.</strong>.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5c() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u007e_.foo._\u007e"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):~:]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):~:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>~<em>.foo.</em>~</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5cx() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u007e__.foo.__\u007e"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):~:]",
        "[emphasis(1,2):2:_]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):~:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>~<strong>.foo.</strong>~</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5d() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u203f*.foo.*\u203f"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):‿:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):‿:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u203f<em>.foo.</em>\u203f</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5dx() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u203f**.foo.**\u203f"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):‿:]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):‿:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u203f<strong>.foo.</strong>\u203f</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5e() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u203f_.foo._\u203f"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):‿:]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):.foo.:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):‿:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u203f<em>.foo.</em>\u203f</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_5ex() -> None:
    """
    Test case:  open left is followed by punctuation and preceeded by punctuation
    """

    # Arrange
    source_markdown = """\u203f__.foo.__\u203f"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):‿:]",
        "[emphasis(1,2):2:_]",
        "[text(1,4):.foo.:]",
        "[end-emphasis(1,9)::]",
        "[text(1,11):‿:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\u203f<strong>.foo.</strong>\u203f</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6x() -> None:
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a*.foo.*.a"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):a*.foo.*.a:]", "[end-para:::True]"]
    expected_gfm = """<p>a*.foo.*.a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6xx() -> None:
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a**.foo.**.a"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):a**.foo.**.a:]", "[end-para:::True]"]
    expected_gfm = """<p>a**.foo.**.a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6a() -> None:
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a*\u007efoo\u007e*a"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):a*~foo~*a:]", "[end-para:::True]"]
    expected_gfm = """<p>a*~foo~*a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6ax() -> None:
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a**\u007efoo\u007e**a"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):a**~foo~**a:]", "[end-para:::True]"]
    expected_gfm = """<p>a**~foo~**a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6b() -> None:
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a_.foo._.a"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):a_.foo._.a:]", "[end-para:::True]"]
    expected_gfm = """<p>a_.foo._.a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6bx() -> None:
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a__.foo.__.a"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):a__.foo.__.a:]", "[end-para:::True]"]
    expected_gfm = """<p>a__.foo.__.a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6c() -> None:
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a_\u007efoo\u007e_a"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):a_~foo~_a:]", "[end-para:::True]"]
    expected_gfm = """<p>a_~foo~_a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6cx() -> None:
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a__\u007efoo\u007e__a"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):a__~foo~__a:]", "[end-para:::True]"]
    expected_gfm = """<p>a__~foo~__a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6d() -> None:
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a*\u203ffoo\u203f*a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a*\u203ffoo\u203f*a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a*\u203ffoo\u203f*a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6dx() -> None:
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a**\u203ffoo\u203f**a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a**\u203ffoo\u203f**a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a**\u203ffoo\u203f**a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6e() -> None:
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a_\u203ffoo\u203f_a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a_\u203ffoo\u203f_a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a_\u203ffoo\u203f_a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_emphasis_6ex() -> None:
    """
    Test case:  open left is followed by punctuation and not preceeded by punctuation or whitespace
    """

    # Arrange
    source_markdown = """a__\u203ffoo\u203f__a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a__\u203ffoo\u203f__a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a__\u203ffoo\u203f__a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
