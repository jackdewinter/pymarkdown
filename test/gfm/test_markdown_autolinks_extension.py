"""
https://github.github.com/gfm/#autolinks-extension-
"""

from test.utils import act_and_assert

config_map = {"extensions": {"markdown-extended-autolinks": {"enabled": True}}}


def test_autolinks_621x():
    """
    Test case 621:  The scheme http will be inserted automatically:
    """

    # Arrange
    source_markdown = """www.commonmark.org"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):1:www.commonmark.org]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="http://www.commonmark.org">www.commonmark.org</a></p>"""
    )

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621a():
    """
    Test case 621:  Not if disabled.
    """

    # Arrange
    source_markdown = """www.commonmark.org"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):www.commonmark.org:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>www.commonmark.org</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_autolinks_621b():
    """
    Test case 621:  variation, with minimal domains.
    """

    # Arrange
    source_markdown = """www.a.b"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):1:www.a.b]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://www.a.b">www.a.b</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621c():
    """
    Test case 621:  variation, with spaces on either side.
    """

    # Arrange
    source_markdown = """ www.a.b """
    expected_tokens = [
        "[para(1,2): : ]",
        "[uri-autolink(1,2):1:www.a.b]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://www.a.b">www.a.b</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621d():
    """
    Test case 621:  variation, with too few ws
    """

    # Arrange
    source_markdown = """ ww.a.b """
    expected_tokens = ["[para(1,2): : ]", "[text(1,2):ww.a.b:]", "[end-para:::True]"]
    expected_gfm = """<p>ww.a.b</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621e():
    """
    Test case 621:  variation, with too many ws
    """

    # Arrange
    source_markdown = """ wwww.a.b """
    expected_tokens = ["[para(1,2): : ]", "[text(1,2):wwww.a.b:]", "[end-para:::True]"]
    expected_gfm = """<p>wwww.a.b</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621f():
    """
    Test case 621:  variation, with double start..
    """

    # Arrange
    source_markdown = """ www..a.b """
    expected_tokens = ["[para(1,2): : ]", "[text(1,2):www..a.b:]", "[end-para:::True]"]
    expected_gfm = """<p>www..a.b</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621fa():
    """
    Test case 621:  variation, with only double start..
    """

    # Arrange
    source_markdown = """ www.. """
    expected_tokens = ["[para(1,2): : ]", "[text(1,2):www..:]", "[end-para:::True]"]
    expected_gfm = """<p>www..</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621g():
    """
    Test case 621:  variation, with empty domain
    """

    # Arrange
    source_markdown = """ www.a..b """
    expected_tokens = ["[para(1,2): : ]", "[text(1,2):www.a..b:]", "[end-para:::True]"]
    expected_gfm = """<p>www.a..b</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621h():
    """
    Test case 621:  variation, with single domain
    """

    # Arrange
    source_markdown = """ www.a """
    expected_tokens = ["[para(1,2): : ]", "[text(1,2):www.a:]", "[end-para:::True]"]
    expected_gfm = """<p>www.a</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621ia():
    """
    Test case 621:  variation, with underscore in first of three domain parts
    """

    # Arrange
    source_markdown = """ www.a_b.c.d """
    expected_tokens = [
        "[para(1,2): : ]",
        "[uri-autolink(1,2):1:www.a_b.c.d]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://www.a_b.c.d">www.a_b.c.d</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621ib():
    """
    Test case 621:  variation, with underscore in second of three domain parts
    """

    # Arrange
    source_markdown = """ www.a.b_c.d """
    expected_tokens = [
        "[para(1,2): : ]",
        "[text(1,2):www.a.b_c.d:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>www.a.b_c.d</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621ic():
    """
    Test case 621:  variation, with underscore in second of three domain parts
    """

    # Arrange
    source_markdown = """ www.a.b.c_d """
    expected_tokens = [
        "[para(1,2): : ]",
        "[text(1,2):www.a.b.c_d:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>www.a.b.c_d</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621j():
    """
    Test case 621:  variation, simple case
    """

    # Arrange
    source_markdown = """ www """
    expected_tokens = ["[para(1,2): : ]", "[text(1,2):www:]", "[end-para:::True]"]
    expected_gfm = """<p>www</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621k():
    """
    Test case 621:  variation, with emphasis
    """

    # Arrange
    source_markdown = """ *www.google.com* """
    expected_tokens = [
        "[para(1,2): : ]",
        "[emphasis(1,2):1:*]",
        "[uri-autolink(1,3):1:www.google.com]",
        "[end-emphasis(1,17)::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><em><a href="http://www.google.com">www.google.com</a></em></p>"""
    )

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621l():
    """
    Test case 621:  variation, with emphasis
    """

    # Arrange
    source_markdown = """ *this* www.google.com"""
    expected_tokens = [
        "[para(1,2): ]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):this:]",
        "[end-emphasis(1,7)::]",
        "[text(1,8): :]",
        "[uri-autolink(1,9):1:www.google.com]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        '<p><em>this</em> <a href="http://www.google.com">www.google.com</a></p>'
    )

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_621m():
    """
    Test case 621:  variation, with emphasis
    """

    # Arrange
    source_markdown = """ wah www.google.com"""
    expected_tokens = [
        "[para(1,2): ]",
        "[text(1,2):wah :]",
        "[uri-autolink(1,6):1:www.google.com]",
        "[end-para:::True]",
    ]
    expected_gfm = '<p>wah <a href="http://www.google.com">www.google.com</a></p>'

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_622x():
    """
    Test case 622:  After a valid domain, zero or more non-space non-< characters may follow
    """

    # Arrange
    source_markdown = """Visit www.commonmark.org/help for more information."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):Visit :]",
        "[uri-autolink(1,7):1:www.commonmark.org/help]",
        "[text(1,30): for more information.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Visit <a href="http://www.commonmark.org/help">www.commonmark.org/help</a> for more information.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_622a():
    """
    Test case 622:  only if enabled
    """

    # Arrange
    source_markdown = """Visit www.commonmark.org/help for more information."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):Visit www.commonmark.org/help for more information.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Visit www.commonmark.org/help for more information.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_autolinks_623x():
    """
    Test case 623:  Trailing punctuation (specifically, ?, !, ., ,, :, *, _, and ~) will not be considered part of the autolink, though they may be included in the interior of the link:
    """

    # Arrange
    source_markdown = """Visit www.commonmark.org.

Visit www.commonmark.org/a.b."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):Visit :]",
        "[uri-autolink(1,7):1:www.commonmark.org]",
        "[text(1,25):.:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):Visit :]",
        "[uri-autolink(3,7):1:www.commonmark.org/a.b]",
        "[text(3,29):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Visit <a href="http://www.commonmark.org">www.commonmark.org</a>.</p>
<p>Visit <a href="http://www.commonmark.org/a.b">www.commonmark.org/a.b</a>.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_623a():
    """
    Test case 623:  variant, double .
    """

    # Arrange
    source_markdown = """Visit www.commonmark.org..

Visit www.commonmark.org/a.b.."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):Visit :]",
        "[uri-autolink(1,7):1:www.commonmark.org]",
        "[text(1,25):..:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):Visit :]",
        "[uri-autolink(3,7):1:www.commonmark.org/a.b]",
        "[text(3,29):..:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Visit <a href="http://www.commonmark.org">www.commonmark.org</a>..</p>
<p>Visit <a href="http://www.commonmark.org/a.b">www.commonmark.org/a.b</a>..</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_623b():
    """
    Test case 623:  variant, double .
    """

    # Arrange
    source_markdown = """Visit www.commonmark.org?
Visit www.commonmark.org!
Visit www.commonmark.org, now!
Visit www.commonmark.org: the best!
Visit www.commonmark.org* now!
Visit www.commonmark.org_ now!
Visit www.commonmark.org~ now!"""
    expected_tokens = [
        "[para(1,1):\n\n\n\n\n\n]",
        "[text(1,1):Visit :]",
        "[uri-autolink(1,7):1:www.commonmark.org]",
        "[text(1,25):?\nVisit ::\n]",
        "[uri-autolink(2,7):1:www.commonmark.org]",
        "[text(2,25):!\nVisit ::\n]",
        "[uri-autolink(3,7):1:www.commonmark.org]",
        "[text(3,25):, now!\nVisit ::\n]",
        "[uri-autolink(4,7):1:www.commonmark.org]",
        "[text(4,25):: the best!\nVisit ::\n]",
        "[uri-autolink(5,7):1:www.commonmark.org]",
        "[text(5,25):* now!\nVisit www.commonmark.org_ now!\nVisit ::\n\n]",
        "[uri-autolink(7,7):1:www.commonmark.org]",
        "[text(7,25):~ now!:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Visit <a href="http://www.commonmark.org">www.commonmark.org</a>?
Visit <a href="http://www.commonmark.org">www.commonmark.org</a>!
Visit <a href="http://www.commonmark.org">www.commonmark.org</a>, now!
Visit <a href="http://www.commonmark.org">www.commonmark.org</a>: the best!
Visit <a href="http://www.commonmark.org">www.commonmark.org</a>* now!
Visit www.commonmark.org_ now!
Visit <a href="http://www.commonmark.org">www.commonmark.org</a>~ now!</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_623c():
    """
    Test case 623:  variant, double .
    """

    # Arrange
    source_markdown = """Visit www.commonmark.org/a=b?
Visit www.commonmark.org/a=b!
Visit www.commonmark.org/a=b, now!
Visit www.commonmark.org/a=b: the best!
Visit www.commonmark.org/a=b* now!
Visit www.commonmark.org/a=b_ now!
Visit www.commonmark.org/a=b~ now!"""
    expected_tokens = [
        "[para(1,1):\n\n\n\n\n\n]",
        "[text(1,1):Visit :]",
        "[uri-autolink(1,7):1:www.commonmark.org/a=b]",
        "[text(1,29):?\nVisit ::\n]",
        "[uri-autolink(2,7):1:www.commonmark.org/a=b]",
        "[text(2,29):!\nVisit ::\n]",
        "[uri-autolink(3,7):1:www.commonmark.org/a=b]",
        "[text(3,29):, now!\nVisit ::\n]",
        "[uri-autolink(4,7):1:www.commonmark.org/a=b]",
        "[text(4,29):: the best!\nVisit ::\n]",
        "[uri-autolink(5,7):1:www.commonmark.org/a=b]",
        "[text(5,29):* now!\nVisit ::\n]",
        "[uri-autolink(6,7):1:www.commonmark.org/a=b]",
        "[text(6,29):_ now!\nVisit ::\n]",
        "[uri-autolink(7,7):1:www.commonmark.org/a=b]",
        "[text(7,29):~ now!:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Visit <a href="http://www.commonmark.org/a=b">www.commonmark.org/a=b</a>?
Visit <a href="http://www.commonmark.org/a=b">www.commonmark.org/a=b</a>!
Visit <a href="http://www.commonmark.org/a=b">www.commonmark.org/a=b</a>, now!
Visit <a href="http://www.commonmark.org/a=b">www.commonmark.org/a=b</a>: the best!
Visit <a href="http://www.commonmark.org/a=b">www.commonmark.org/a=b</a>* now!
Visit <a href="http://www.commonmark.org/a=b">www.commonmark.org/a=b</a>_ now!
Visit <a href="http://www.commonmark.org/a=b">www.commonmark.org/a=b</a>~ now!</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_624x():
    """
    Test case 624:  When an autolink ends in ), we scan the entire autolink for the total number of parentheses. If there is a greater number of closing parentheses than opening ones, we don’t consider the unmatched trailing parentheses part of the autolink, in order to facilitate including an autolink inside a parenthesis:
    """

    # Arrange
    source_markdown = """www.google.com/search?q=Markup+(business)

www.google.com/search?q=Markup+(business)))

(www.google.com/search?q=Markup+(business))

(www.google.com/search?q=Markup+(business)"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):1:www.google.com/search?q=Markup+(business)]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[uri-autolink(3,1):1:www.google.com/search?q=Markup+(business)]",
        "[text(3,42):)):]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):(:]",
        "[uri-autolink(5,2):1:www.google.com/search?q=Markup+(business)]",
        "[text(5,43):):]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[para(7,1):]",
        "[text(7,1):(:]",
        "[uri-autolink(7,2):1:www.google.com/search?q=Markup+(business)]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://www.google.com/search?q=Markup+(business)">www.google.com/search?q=Markup+(business)</a></p>
<p><a href="http://www.google.com/search?q=Markup+(business)">www.google.com/search?q=Markup+(business)</a>))</p>
<p>(<a href="http://www.google.com/search?q=Markup+(business)">www.google.com/search?q=Markup+(business)</a>)</p>
<p>(<a href="http://www.google.com/search?q=Markup+(business)">www.google.com/search?q=Markup+(business)</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_624a():
    """
    Test case 624a:  variant
    """

    # Arrange
    source_markdown = """((www.google.com/search?q=Markup+(business)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):((:]",
        "[uri-autolink(1,3):1:www.google.com/search?q=Markup+(business)]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>((<a href="http://www.google.com/search?q=Markup+(business)">www.google.com/search?q=Markup+(business)</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_625():
    """
    Test case 625:  This check is only done when the link ends in a closing parentheses ), so if the only parentheses are in the interior of the autolink, no special rules are applied:
    """

    # Arrange
    source_markdown = """www.google.com/search?q=(business))+ok"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):1:www.google.com/search?q=(business))+ok]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://www.google.com/search?q=(business))+ok">www.google.com/search?q=(business))+ok</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_626x():
    """
    Test case 626:  If an autolink ends in a semicolon (;), we check to see if it appears to resemble an entity reference; if the preceding text is & followed by one or more alphanumeric characters. If so, it is excluded from the autolink:
    """

    # Arrange
    source_markdown = """www.google.com/search?q=commonmark&hl=en

www.google.com/search?q=commonmark&hl;"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):1:www.google.com/search?q=commonmark&hl=en]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[uri-autolink(3,1):1:www.google.com/search?q=commonmark]",
        "[text(3,35):\a&\a&amp;\ahl;:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://www.google.com/search?q=commonmark&amp;hl=en">www.google.com/search?q=commonmark&amp;hl=en</a></p>
<p><a href="http://www.google.com/search?q=commonmark">www.google.com/search?q=commonmark</a>&amp;hl;</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_626a():
    """
    Test case 626:  variant, without &
    """

    # Arrange
    source_markdown = """www.google.com/search?q=commonmark:hl;"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):1:www.google.com/search?q=commonmark:hl;]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://www.google.com/search?q=commonmark:hl;">www.google.com/search?q=commonmark:hl;</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_626b():
    """
    Test case 626:  variant, without non-alpha
    """

    # Arrange
    source_markdown = """www.google.com/search?q=commonmark&-hl;"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):1:www.google.com/search?q=commonmark&-hl;]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://www.google.com/search?q=commonmark&amp;-hl;">www.google.com/search?q=commonmark&amp;-hl;</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_627():
    """
    Test case 627:  < immediately ends an autolink.
    """

    # Arrange
    source_markdown = """www.commonmark.org/he<lp"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):1:www.commonmark.org/he]",
        "[text(1,22):\a<\a&lt;\alp:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://www.commonmark.org/he">www.commonmark.org/he</a>&lt;lp</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_628x():
    """
    Test case 628:  An extended url autolink will be recognised when one of the schemes http://, or https://, followed by a valid domain, then zero or more non-space non-< characters according to extended autolink path validation:
    """

    # Arrange
    source_markdown = """http://commonmark.org

(Visit https://encrypted.google.com/search?q=Markup+(business))"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://commonmark.org]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):(Visit :]",
        "[uri-autolink(3,8):https://encrypted.google.com/search?q=Markup+(business)]",
        "[text(3,63):):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://commonmark.org">http://commonmark.org</a></p>
<p>(Visit <a href="https://encrypted.google.com/search?q=Markup+(business)">https://encrypted.google.com/search?q=Markup+(business)</a>)</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_628a():
    """
    Test case 628:  but only if enabled
    """

    # Arrange
    source_markdown = """http://commonmark.org

(Visit https://encrypted.google.com/search?q=Markup+(business))"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):http://commonmark.org:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):(Visit https://encrypted.google.com/search?q=Markup+(business)):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>http://commonmark.org</p>\n<p>(Visit https://encrypted.google.com/search?q=Markup+(business))</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_autolinks_628b():
    """
    Test case 628:  variant
    """

    # Arrange
    source_markdown = """hTtP://commonmark.org"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):hTtP://commonmark.org:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>hTtP://commonmark.org</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_628c():
    """
    Test case 628:  variant
    """

    # Arrange
    source_markdown = """http://com"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):http://com:]", "[end-para:::True]"]
    expected_gfm = """<p>http://com</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_629x():
    """
    Test case 629:  The scheme mailto: will automatically be added to the generated link:
    """

    # Arrange
    source_markdown = """foo@bar.baz"""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink(1,1):foo@bar.baz]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="mailto:foo@bar.baz">foo@bar.baz</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_629a():
    """
    Test case 629:  variant, not activated
    """

    # Arrange
    source_markdown = """foo@bar.baz"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):foo@bar.baz:]", "[end-para:::True]"]
    expected_gfm = """<p>foo@bar.baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_autolinks_629b():
    """
    Test case 629:  variant, in middle of sentence
    """

    # Arrange
    source_markdown = """this is foo@bar.baz my address"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this is :]",
        "[email-autolink(1,9):foo@bar.baz]",
        "[text(1,20): my address:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>this is <a href="mailto:foo@bar.baz">foo@bar.baz</a> my address</p>"""
    )

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_629c():
    """
    Test case 629:  variant, surrounded by emphasis
    """

    # Arrange
    source_markdown = """this is *foo@bar.baz* my address"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this is :]",
        "[emphasis(1,9):1:*]",
        "[email-autolink(1,10):foo@bar.baz]",
        "[end-emphasis(1,21)::]",
        "[text(1,22): my address:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this is <em><a href="mailto:foo@bar.baz">foo@bar.baz</a></em> my address</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_629d():
    """
    Test case 629:  variant, emphasis and new lines
    """

    # Arrange
    source_markdown = """this is\n*foo@bar.baz*\n my address"""
    expected_tokens = [
        "[para(1,1):\n\n ]",
        "[text(1,1):this is\n::\n]",
        "[emphasis(2,1):1:*]",
        "[email-autolink(2,2):foo@bar.baz]",
        "[end-emphasis(2,13)::]",
        "[text(2,14):\nmy address::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this is\n<em><a href="mailto:foo@bar.baz">foo@bar.baz</a></em>\nmy address</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_629e():
    """
    Test case 629:  variant, just middle and second half
    """

    # Arrange
    source_markdown = """@bar.baz my address"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):@bar.baz my address:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>@bar.baz my address</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_629f():
    """
    Test case 629:  variant, with special characters
    """

    # Arrange
    source_markdown = """My address is my_address_is@bar.baz."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):My address is :]",
        "[email-autolink(1,15):my_address_is@bar.baz]",
        "[text(1,36):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>My address is <a href="mailto:my_address_is@bar.baz">my_address_is@bar.baz</a>.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_629g():
    """
    Test case 629:  variant, just middle and second half
    """

    # Arrange
    source_markdown = """foo@bar. my address"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo@bar. my address:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo@bar. my address</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_630x():
    """
    Test case 630:  + can occur before the @, but not after.
    """

    # Arrange
    source_markdown = (
        """hello@mail+xyz.example isn't valid, but hello+xyz@mail.example is."""
    )
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):hello@mail+xyz.example isn't valid, but :]",
        "[email-autolink(1,41):hello+xyz@mail.example]",
        "[text(1,63): is.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>hello@mail+xyz.example isn't valid, but <a href="mailto:hello+xyz@mail.example">hello+xyz@mail.example</a> is.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_630xa():
    """
    Test case 630:  variant
    """

    # Arrange
    source_markdown = """but hello+xyz@mail.example is."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):but :]",
        "[email-autolink(1,5):hello+xyz@mail.example]",
        "[text(1,27): is.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>but <a href="mailto:hello+xyz@mail.example">hello+xyz@mail.example</a> is.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_630a():
    """
    Test case 630:  variant
    """

    # Arrange
    source_markdown = """a.b-c_d@a.b."""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink(1,1):a.b-c_d@a.b]",
        "[text(1,12):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="mailto:a.b-c_d@a.b">a.b-c_d@a.b</a>.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_630b():
    """
    Test case 630:  variant
    """

    # Arrange
    source_markdown = """a.b-c_d@a.b."""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink(1,1):a.b-c_d@a.b]",
        "[text(1,12):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="mailto:a.b-c_d@a.b">a.b-c_d@a.b</a>.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_630c():
    """
    Test case 630:  variant
    """

    # Arrange
    source_markdown = """my_address_is@bar.baz."""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink(1,1):my_address_is@bar.baz]",
        "[text(1,22):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="mailto:my_address_is@bar.baz">my_address_is@bar.baz</a>.</p>"""
    )

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_630d():
    """
    Test case 630:  variant
    """

    # Arrange
    source_markdown = """my_real_address_is@bar.baz."""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink(1,1):my_real_address_is@bar.baz]",
        "[text(1,27):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="mailto:my_real_address_is@bar.baz">my_real_address_is@bar.baz</a>.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_630e():
    """
    Test case 630:  variant
    """

    # Arrange
    source_markdown = """my_real_add_ress_is@bar.baz."""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink(1,1):my_real_add_ress_is@bar.baz]",
        "[text(1,28):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="mailto:my_real_add_ress_is@bar.baz">my_real_add_ress_is@bar.baz</a>.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_631():
    """
    Test case 631:  ., -, and _ can occur on both sides of the @, but only . may occur at the end of the email address, in which case it will not be considered part of the address:
    """

    # Arrange
    source_markdown = """a.b-c_d@a.b

a.b-c_d@a.b.

a.b-c_d@a.b-

a.b-c_d@a.b_"""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink(1,1):a.b-c_d@a.b]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[email-autolink(3,1):a.b-c_d@a.b]",
        "[text(3,12):.:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):a.b-c_d@a.b-:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[para(7,1):]",
        "[text(7,1):a.b-c_d@a.b_:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="mailto:a.b-c_d@a.b">a.b-c_d@a.b</a></p>
<p><a href="mailto:a.b-c_d@a.b">a.b-c_d@a.b</a>.</p>
<p>a.b-c_d@a.b-</p>
<p>a.b-c_d@a.b_</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_633():
    """
    Test case 633:  The scheme of the protocol will automatically be added to the generated link. All the rules of email address autolinking apply.
    """

    # Arrange
    source_markdown = """mailto:foo@bar.baz

mailto:a.b-c_d@a.b

mailto:a.b-c_d@a.b.

mailto:a.b-c_d@a.b/

mailto:a.b-c_d@a.b-

mailto:a.b-c_d@a.b_

xmpp:foo@bar.baz

xmpp:foo@bar.baz."""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):mailto:foo@bar.baz]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[uri-autolink(3,1):mailto:a.b-c_d@a.b]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[uri-autolink(5,1):mailto:a.b-c_d@a.b]",
        "[text(5,19):.:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[para(7,1):]",
        "[uri-autolink(7,1):mailto:a.b-c_d@a.b]",
        "[text(7,19):/:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[para(9,1):]",
        "[text(9,1):mailto:a.b-c_d@a.b-:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[para(11,1):]",
        "[text(11,1):mailto:a.b-c_d@a.b_:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[para(13,1):]",
        "[uri-autolink(13,1):xmpp:foo@bar.baz]",
        "[end-para:::True]",
        "[BLANK(14,1):]",
        "[para(15,1):]",
        "[uri-autolink(15,1):xmpp:foo@bar.baz]",
        "[text(15,17):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="mailto:foo@bar.baz">mailto:foo@bar.baz</a></p>
<p><a href="mailto:a.b-c_d@a.b">mailto:a.b-c_d@a.b</a></p>
<p><a href="mailto:a.b-c_d@a.b">mailto:a.b-c_d@a.b</a>.</p>
<p><a href="mailto:a.b-c_d@a.b">mailto:a.b-c_d@a.b</a>/</p>
<p>mailto:a.b-c_d@a.b-</p>
<p>mailto:a.b-c_d@a.b_</p>
<p><a href="xmpp:foo@bar.baz">xmpp:foo@bar.baz</a></p>
<p><a href="xmpp:foo@bar.baz">xmpp:foo@bar.baz</a>.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_634():
    """
    Test case 634:  A described in the specification xmpp offers an optional / followed by a resource. The resource can contain all alphanumeric characters, as well as @ and ..
    """

    # Arrange
    source_markdown = """xmpp:foo@bar.baz/txt

xmpp:foo@bar.baz/txt@bin

xmpp:foo@bar.baz/txt@bin.com
"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):xmpp:foo@bar.baz/txt]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[uri-autolink(3,1):xmpp:foo@bar.baz/txt@bin]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[uri-autolink(5,1):xmpp:foo@bar.baz/txt@bin.com]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<p><a href="xmpp:foo@bar.baz/txt">xmpp:foo@bar.baz/txt</a></p>
<p><a href="xmpp:foo@bar.baz/txt@bin">xmpp:foo@bar.baz/txt@bin</a></p>
<p><a href="xmpp:foo@bar.baz/txt@bin.com">xmpp:foo@bar.baz/txt@bin.com</a></p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_634a():
    """
    Test case 634:  variant
    """

    # Arrange
    source_markdown = """My xmpp:foo@bar.baz/txt jabber link."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):My :]",
        "[uri-autolink(1,1):xmpp:foo@bar.baz/txt]",
        "[text(1,24): jabber link.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>My <a href="xmpp:foo@bar.baz/txt">xmpp:foo@bar.baz/txt</a> jabber link.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_635x():
    """
    Test case 635:  Further / characters are not considered part of the domain:
    """

    # Arrange
    source_markdown = """xmpp:foo@bar.baz/txt/bin"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):xmpp:foo@bar.baz/txt]",
        "[text(1,21):/bin:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="xmpp:foo@bar.baz/txt">xmpp:foo@bar.baz/txt</a>/bin</p>"""
    )

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_autolinks_635a():
    """
    Test case 635:  variant
    """

    # Arrange
    source_markdown = """xmpp:foo@bar.baz/"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):xmpp:foo@bar.baz]",
        "[text(1,17):/:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="xmpp:foo@bar.baz">xmpp:foo@bar.baz</a>/</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )
