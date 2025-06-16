"""
https://github.github.com/gfm/#backslash-escapes
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_backslash_escapes_extra_1() -> None:
    """
    Test case backslash extra 1:  backslash before the code span open
    """

    # Arrange
    source_markdown = """\\`code span`"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b`code span`:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>`code span`</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_1a() -> None:
    """
    Test case backslash extra 1a:  backslash before the code span closed
    """

    # Arrange
    source_markdown = """`code span\\`"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):code span\\:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>code span\\</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_2() -> None:
    """
    Test case backslash extra 2:  backslash before the character reference
    """

    # Arrange
    source_markdown = """\\&amp; the band played on"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b\a&\a&amp;\aamp; the band played on:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&amp;amp; the band played on</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_3() -> None:
    """
    Test case backslash extra 3:  backslash before the inline html open
    """

    # Arrange
    source_markdown = """\\<there it='is'>, really"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b\a<\a&lt;\athere it='is'\a>\a&gt;\a, really:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;there it='is'&gt;, really</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_4() -> None:
    """
    Test case backslash extra 4:  backslash before the inline html close
    """

    # Arrange
    source_markdown = """<there it='is'\\>, really"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\athere it='is'\\\b\a>\a&gt;\a, really:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;there it='is'&gt;, really</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_5() -> None:
    """
    Test case backslash extra 5:  backslash before the autolink open
    """

    # Arrange
    source_markdown = """\\<http://www.google.com> is where to look"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b\a<\a&lt;\ahttp://www.google.com\a>\a&gt;\a is where to look:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;http://www.google.com&gt; is where to look</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_6() -> None:
    """
    Test case backslash extra 6:  backslash before the autolink close
    """

    # Arrange
    source_markdown = """<http://www.google.com\\> is where to look"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://www.google.com\\]",
        "[text(1,25): is where to look:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://www.google.com%5C">http://www.google.com\\</a> is where to look</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_7() -> None:
    """
    Test case backslash extra 7:  backslash before the emphasis start
    """

    # Arrange
    source_markdown = """\\*it's* me!"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b*it's* me!:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*it's* me!</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_8() -> None:
    """
    Test case backslash extra 8:  backslash before the emphasis end
    """

    # Arrange
    source_markdown = """*it's\\* me!"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*it's\\\b* me!:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*it's* me!</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_9() -> None:
    """
    Test case backslash extra 9:  backslash before the first emphasis start
    """

    # Arrange
    source_markdown = """*\\*it's** me!"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):\\\b*it's:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):* me!:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>*it's</em>* me!</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_10() -> None:
    """
    Test case backslash extra 10:  backslash before the first emphasis end
    """

    # Arrange
    source_markdown = """**it's\\** me!"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):it's\\\b*:]",
        "[end-emphasis(1,9)::]",
        "[text(1,10): me!:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*<em>it's*</em> me!</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_11() -> None:
    """
    Test case backslash extra 11:  backslash before the link open
    """

    # Arrange
    source_markdown = """\\[Foo](/uri) is a link"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b[Foo](/uri) is a link:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[Foo](/uri) is a link</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_12() -> None:
    """
    Test case backslash extra 12:  backslash before the image open
    """

    # Arrange
    source_markdown = """\\![foo](/url "title") is an image"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b!:]",
        '[link(1,3):inline:/url:title::::foo:False:":: :]',
        "[text(1,4):foo:]",
        "[end-link::]",
        "[text(1,22): is an image:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>!<a href="/url" title="title">foo</a> is an image</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_13() -> None:
    """
    Test case backslash extra 13:  backslash between the image open characters
    Also see: 600
    """

    # Arrange
    source_markdown = """!\\[foo](/url "title") is an image"""
    expected_tokens = [
        "[para(1,1):]",
        '[text(1,1):!\\\b[foo](/url \a"\a&quot;\atitle\a"\a&quot;\a) is an image:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>![foo](/url &quot;title&quot;) is an image</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_14() -> None:
    """
    Test case backslash extra 14:  backslash before the code span open in setext
    """

    # Arrange
    source_markdown = """\\`code span`
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\\\b`code span`:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>`code span`</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_14a() -> None:
    """
    Test case backslash extra 14a:  backslash before the code span closed in setext
    """

    # Arrange
    source_markdown = """`code span\\`
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[icode-span(1,1):code span\\:`::]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><code>code span\\</code></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_15() -> None:
    """
    Test case backslash extra 15:  backslash before the character reference in setext
    """

    # Arrange
    source_markdown = """\\&amp; the band played on
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\\\b\a&\a&amp;\aamp; the band played on:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>&amp;amp; the band played on</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_16() -> None:
    """
    Test case backslash extra 16:  backslash before the inline html open in setext
    """

    # Arrange
    source_markdown = """\\<there it='is'>, really
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\\\b\a<\a&lt;\athere it='is'\a>\a&gt;\a, really:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>&lt;there it='is'&gt;, really</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_17() -> None:
    """
    Test case backslash extra 17:  backslash before the inline html close in setext
    """

    # Arrange
    source_markdown = """<there it='is'\\>, really
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\a<\a&lt;\athere it='is'\\\b\a>\a&gt;\a, really:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>&lt;there it='is'&gt;, really</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_18() -> None:
    """
    Test case backslash extra 18:  backslash before the autolink open in setext
    """

    # Arrange
    source_markdown = """\\<http://www.google.com> is where to look
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\\\b\a<\a&lt;\ahttp://www.google.com\a>\a&gt;\a is where to look:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>&lt;http://www.google.com&gt; is where to look</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_19() -> None:
    """
    Test case backslash extra 19:  backslash before the autolink close in setext
    """

    # Arrange
    source_markdown = """<http://www.google.com\\> is where to look
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[uri-autolink(1,1):http://www.google.com\\]",
        "[text(1,25): is where to look:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><a href="http://www.google.com%5C">http://www.google.com\\</a> is where to look</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_20() -> None:
    """
    Test case backslash extra 20:  backslash before the emphasis start in setext
    """

    # Arrange
    source_markdown = """\\*it's* me!
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\\\b*it's* me!:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>*it's* me!</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_21() -> None:
    """
    Test case backslash extra 21:  backslash before the emphasis end in setext
    """

    # Arrange
    source_markdown = """*it's\\* me!
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):*it's\\\b* me!:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>*it's* me!</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_22() -> None:
    """
    Test case backslash extra 22:  backslash before the first emphasis start in setext
    """

    # Arrange
    source_markdown = """*\\*it's** me!
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):\\\b*it's:]",
        "[end-emphasis(1,8)::]",
        "[text(1,9):* me!:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><em>*it's</em>* me!</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_23() -> None:
    """
    Test case backslash extra 23:  backslash before the first emphasis end in setext
    """

    # Arrange
    source_markdown = """**it's\\** me!
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):*:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):it's\\\b*:]",
        "[end-emphasis(1,9)::]",
        "[text(1,10): me!:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>*<em>it's*</em> me!</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_24() -> None:
    """
    Test case backslash extra 24:  backslash before the link open in setext
    """

    # Arrange
    source_markdown = """\\[Foo](/uri) is a link
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\\\b[Foo](/uri) is a link:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>[Foo](/uri) is a link</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_25() -> None:
    """
    Test case backslash extra 25:  backslash before the image open in setext
    """

    # Arrange
    source_markdown = """\\![foo](/url "title") is an image
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\\\b!:]",
        '[link(1,3):inline:/url:title::::foo:False:":: :]',
        "[text(1,4):foo:]",
        "[end-link::]",
        "[text(1,22): is an image:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>!<a href="/url" title="title">foo</a> is an image</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_26() -> None:
    """
    Test case backslash extra 26:  backslash between the image open characters in setext
    """

    # Arrange
    source_markdown = """!\\[foo](/url "title") is an image
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        '[text(1,1):!\\\b[foo](/url \a"\a&quot;\atitle\a"\a&quot;\a) is an image:]',
        "[end-setext::]",
    ]
    expected_gfm = """<h2>![foo](/url &quot;title&quot;) is an image</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_27() -> None:
    """
    Test case backslash extra 27:  backslash before the code span open in atx
    """

    # Arrange
    source_markdown = """# \\`code span`"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):\\\b`code span`: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>`code span`</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_27a() -> None:
    """
    Test case backslash extra 27a:  backslash before the code span closed in atx
    """

    # Arrange
    source_markdown = """# `code span\\`"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3)::\a \a\x03\a]",
        "[icode-span(1,3):code span\\:`::]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1><code>code span\\</code></h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_28() -> None:
    """
    Test case backslash extra 28:  backslash before the character reference in atx
    """

    # Arrange
    source_markdown = """# \\&amp; the band played on"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):\\\b\a&\a&amp;\aamp; the band played on: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>&amp;amp; the band played on</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_29() -> None:
    """
    Test case backslash extra 29:  backslash before the inline html open in atx
    """

    # Arrange
    source_markdown = """# \\<there it='is'>, really"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):\\\b\a<\a&lt;\athere it='is'\a>\a&gt;\a, really: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>&lt;there it='is'&gt;, really</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_30() -> None:
    """
    Test case backslash extra 30:  backslash before the inline html close in atx
    """

    # Arrange
    source_markdown = """# <there it='is'\\>, really"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):\a<\a&lt;\athere it='is'\\\b\a>\a&gt;\a, really: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>&lt;there it='is'&gt;, really</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_31() -> None:
    """
    Test case backslash extra 31:  backslash before the autolink open in atx
    """

    # Arrange
    source_markdown = """# \\<http://www.google.com> is where to look"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):\\\b\a<\a&lt;\ahttp://www.google.com\a>\a&gt;\a is where to look: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>&lt;http://www.google.com&gt; is where to look</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_32() -> None:
    """
    Test case backslash extra 32:  backslash before the autolink close in atx
    """

    # Arrange
    source_markdown = """# <http://www.google.com\\> is where to look"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3)::\a \a\x03\a]",
        "[uri-autolink(1,3):http://www.google.com\\]",
        "[text(1,27): is where to look:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1><a href="http://www.google.com%5C">http://www.google.com\\</a> is where to look</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_33() -> None:
    """
    Test case backslash extra 33:  backslash before the emphasis start in atx
    """

    # Arrange
    source_markdown = """# \\*it's* me!"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):\\\b*it's* me!: ]", "[end-atx::]"]
    expected_gfm = """<h1>*it's* me!</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_34() -> None:
    """
    Test case backslash extra 34:  backslash before the emphasis end in atx
    """

    # Arrange
    source_markdown = """# *it's\\* me!"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):*it's\\\b* me!:\a \a\x03\a]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>*it's* me!</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_35() -> None:
    """
    Test case backslash extra 35:  backslash before the first emphasis start in atx
    """

    # Arrange
    source_markdown = """# *\\*it's** me!"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3)::\a \a\x03\a]",
        "[emphasis(1,3):1:*]",
        "[text(1,4):\\\b*it's:]",
        "[end-emphasis(1,10)::]",
        "[text(1,11):* me!:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1><em>*it's</em>* me!</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_36() -> None:
    """
    Test case backslash extra 36:  backslash before the first emphasis end in atx
    """

    # Arrange
    source_markdown = """# **it's\\** me!"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):*:\a \a\x03\a]",
        "[emphasis(1,4):1:*]",
        "[text(1,5):it's\\\b*:]",
        "[end-emphasis(1,11)::]",
        "[text(1,12): me!:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>*<em>it's*</em> me!</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_37() -> None:
    """
    Test case backslash extra 37:  backslash before the link open in atx
    """

    # Arrange
    source_markdown = """# \\[Foo](/uri) is a link"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):\\\b[Foo](/uri) is a link: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>[Foo](/uri) is a link</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_38() -> None:
    """
    Test case backslash extra 38:  backslash before the image open in atx
    """

    # Arrange
    source_markdown = """# \\![foo](/url "title") is an image"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):\\\b!: ]",
        '[link(1,5):inline:/url:title::::foo:False:":: :]',
        "[text(1,6):foo:]",
        "[end-link::]",
        "[text(1,24): is an image:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>!<a href="/url" title="title">foo</a> is an image</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_backslash_escapes_extra_39() -> None:
    """
    Test case backslash extra 39:  backslash between the image open characters in atx
    """

    # Arrange
    source_markdown = """# !\\[foo](/url "title") is an image"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        '[text(1,3):!\\\b[foo](/url \a"\a&quot;\atitle\a"\a&quot;\a) is an image: ]',
        "[end-atx::]",
    ]
    expected_gfm = """<h1>![foo](/url &quot;title&quot;) is an image</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
