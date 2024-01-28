"""
https://github.github.com/gfm/#atx-headings
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_atx_headings_extra_1():
    """
    Test case extra 1:  ATX headings starts with a backslash escape
    """

    # Arrange
    source_markdown = """## \\\\this is a fun day"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):\\\b\\this is a fun day: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>\\this is a fun day</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_2():
    """
    Test case extra 2:  ATX headings starts with a backslash as in a hard line break
    """

    # Arrange
    source_markdown = """## \\"""
    expected_tokens = ["[atx(1,1):2:0:]", "[text(1,4):\\: ]", "[end-atx::]"]
    expected_gfm = """<h2>\\</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_3():
    """
    Test case extra 3:  ATX headings starts with 2+ spaces as in a hard line break
    """

    # Arrange
    source_markdown = """##    """
    expected_tokens = ["[atx(1,1):2:0:]", "[text(1,7)::    ]", "[end-atx::]"]
    expected_gfm = """<h2></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_4():
    """
    Test case extra 4:  ATX headings string starting with a code span.
    """

    # Arrange
    source_markdown = """## ``this`` is a fun day"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        "[icode-span(1,4):this:``::]",
        "[text(1,12): is a fun day:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2><code>this</code> is a fun day</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_5():
    """
    Test case extra 5:  ATX headings string starting with a character reference.
    """

    # Arrange
    source_markdown = """## &amp; the band played on"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):\a&amp;\a\a&\a&amp;\a\a the band played on: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>&amp; the band played on</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_6():
    """
    Test case extra 6:  ATX headings string starting with a raw html block.
    """

    # Arrange
    source_markdown = """## <there it='is'>, really"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        "[raw-html(1,4):there it='is']",
        "[text(1,19):, really:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2><there it='is'>, really</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_7():
    """
    Test case extra 7:  ATX headings string starting with an URI autolink
    """

    # Arrange
    source_markdown = """## <http://www.google.com> is where to look"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        "[uri-autolink(1,4):http://www.google.com]",
        "[text(1,27): is where to look:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2><a href="http://www.google.com">http://www.google.com</a> is where to look</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_8():
    """
    Test case extra 8:  ATX headings string starting with an email autolink
    """

    # Arrange
    source_markdown = """## <foo@bar.com> for more information"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        "[email-autolink(1,4):foo@bar.com]",
        "[text(1,17): for more information:]",
        "[end-atx::]",
    ]
    expected_gfm = (
        """<h2><a href="mailto:foo@bar.com">foo@bar.com</a> for more information</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_9():
    """
    Test case extra 9:  ATX headings string starting with an emphasis
    """

    # Arrange
    source_markdown = """## *it's* me!"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        "[emphasis(1,4):1:*]",
        "[text(1,5):it's:]",
        "[end-emphasis(1,9)::]",
        "[text(1,10): me!:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2><em>it's</em> me!</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_10():
    """
    Test case extra 10:  ATX headings string starting with a link.  also see 183
    """

    # Arrange
    source_markdown = """## [Foo](/uri) is a link"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        "[link(1,4):inline:/uri:::::Foo:False::::]",
        "[text(1,5):Foo:]",
        "[end-link::]",
        "[text(1,15): is a link:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2><a href="/uri">Foo</a> is a link</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_11():
    """
    Test case extra 11:  ATX headings string starting with an image
    """

    # Arrange
    source_markdown = """## ![foo](/url "title") is an image"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        '[image(1,4):inline:/url:title:foo::::foo:False:":: :]',
        "[text(1,24): is an image:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2><img src="/url" alt="foo" title="title" /> is an image</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_12():
    """
    Test case extra 12:  ATX headings containing a backslash
    """

    # Arrange
    source_markdown = """## this is a \\\\fun\\\\ day"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):this is a \\\b\\fun\\\b\\ day: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>this is a \\fun\\ day</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_13():
    """
    Test case extra 13:  ATX headings containing a code span.
    """

    # Arrange
    source_markdown = """## this is a ``fun`` day"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):this is a : ]",
        "[icode-span(1,14):fun:``::]",
        "[text(1,21): day:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>this is a <code>fun</code> day</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_14():
    """
    Test case extra 14:  ATX headings containing a character reference.
    """

    # Arrange
    source_markdown = """## fun &amp; joy"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):fun \a&amp;\a\a&\a&amp;\a\a joy: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>fun &amp; joy</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_15():
    """
    Test case extra 15:  ATX heading containing a raw html block.
    """

    # Arrange
    source_markdown = """## where <there it='is'> it"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):where : ]",
        "[raw-html(1,10):there it='is']",
        "[text(1,25): it:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>where <there it='is'> it</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_16():
    """
    Test case extra 16:  ATX heading containing an URI autolink
    """

    # Arrange
    source_markdown = """## look at <http://www.google.com> for answers"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):look at : ]",
        "[uri-autolink(1,12):http://www.google.com]",
        "[text(1,35): for answers:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>look at <a href="http://www.google.com">http://www.google.com</a> for answers</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_17():
    """
    Test case extra 17:  ATX heading containing an email autolink
    """

    # Arrange
    source_markdown = """## email <foo@bar.com> for answers"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):email : ]",
        "[email-autolink(1,10):foo@bar.com]",
        "[text(1,23): for answers:]",
        "[end-atx::]",
    ]
    expected_gfm = (
        """<h2>email <a href="mailto:foo@bar.com">foo@bar.com</a> for answers</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_18():
    """
    Test case extra 18:  ATX heading containing emphasis
    """

    # Arrange
    source_markdown = """## really! *it's me!* here!"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):really! : ]",
        "[emphasis(1,12):1:*]",
        "[text(1,13):it's me!:]",
        "[end-emphasis(1,21)::]",
        "[text(1,22): here!:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>really! <em>it's me!</em> here!</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_19():
    """
    Test case extra 19:  ATX heading containing a link.
    """

    # Arrange
    source_markdown = """## look at [Foo](/uri) for more"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):look at : ]",
        "[link(1,12):inline:/uri:::::Foo:False::::]",
        "[text(1,13):Foo:]",
        "[end-link::]",
        "[text(1,23): for more:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>look at <a href="/uri">Foo</a> for more</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_20():
    """
    Test case extra 20:  ATX heading containing an image
    """

    # Arrange
    source_markdown = """## special ![foo](/url "title") headings"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):special : ]",
        '[image(1,12):inline:/url:title:foo::::foo:False:":: :]',
        "[text(1,32): headings:]",
        "[end-atx::]",
    ]
    expected_gfm = (
        """<h2>special <img src="/url" alt="foo" title="title" /> headings</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_21():
    """
    Test case extra 21:  ATX headings ends with a backslash escape
    """

    # Arrange
    source_markdown = """## this is a fun day\\\\"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):this is a fun day\\\b\\: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>this is a fun day\\</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_22():
    """
    Test case extra 22:  ATX headings ends with a backslash as in a hard line break
    """

    # Arrange
    source_markdown = """## this was \\"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):this was \\: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>this was \\</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_23():
    """
    Test case extra 23:  ATX headings ends with 2+ spaces as in a hard line break
    """

    # Arrange
    source_markdown = """## what? no line break?   """
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):what? no line break?: ]",
        "[end-atx:   :]",
    ]
    expected_gfm = """<h2>what? no line break?</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_24():
    """
    Test case extra 24:  ATX headings string ending with a code span.
    """

    # Arrange
    source_markdown = """## this is a fun ``day``"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):this is a fun : ]",
        "[icode-span(1,18):day:``::]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>this is a fun <code>day</code></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_25():
    """
    Test case extra 25:  ATX headings string ending with a character reference.
    """

    # Arrange
    source_markdown = """## the band played on &amp;"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):the band played on \a&amp;\a\a&\a&amp;\a\a: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>the band played on &amp;</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_26():
    """
    Test case extra 26:  ATX headings string ending with a raw html block.
    """

    # Arrange
    source_markdown = """## really, <there it='is'>"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):really, : ]",
        "[raw-html(1,12):there it='is']",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>really, <there it='is'></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_27():
    """
    Test case extra 27:  ATX headings string ending with an URI autolink
    """

    # Arrange
    source_markdown = """## look at <http://www.google.com>"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):look at : ]",
        "[uri-autolink(1,12):http://www.google.com]",
        "[end-atx::]",
    ]
    expected_gfm = (
        """<h2>look at <a href="http://www.google.com">http://www.google.com</a></h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_28():
    """
    Test case extra 28:  ATX headings string ending with an email autolink
    """

    # Arrange
    source_markdown = """## for more information, contact <foo@bar.com>"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):for more information, contact : ]",
        "[email-autolink(1,34):foo@bar.com]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>for more information, contact <a href="mailto:foo@bar.com">foo@bar.com</a></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_29():
    """
    Test case extra 29:  ATX headings string ending with an emphasis
    """

    # Arrange
    source_markdown = """## it's *me*"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):it's : ]",
        "[emphasis(1,9):1:*]",
        "[text(1,10):me:]",
        "[end-emphasis(1,12)::]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>it's <em>me</em></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_30():
    """
    Test case extra 30:  ATX headings string ending with a link.
    """

    # Arrange
    source_markdown = """## a link looks like [Foo](/uri)"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):a link looks like : ]",
        "[link(1,22):inline:/uri:::::Foo:False::::]",
        "[text(1,23):Foo:]",
        "[end-link::]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>a link looks like <a href="/uri">Foo</a></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_31():
    """
    Test case extra 31:  ATX headings string ending with an image
    """

    # Arrange
    source_markdown = """## an image is ![foo](/url "title")"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):an image is : ]",
        '[image(1,16):inline:/url:title:foo::::foo:False:":: :]',
        "[end-atx::]",
    ]
    expected_gfm = """<h2>an image is <img src="/url" alt="foo" title="title" /></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_32():
    """
    Test case extra 32:  ATX heading this is only a backslash escape
    """

    # Arrange
    source_markdown = """## \\\\"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):\\\b\\: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>\\</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_33():
    """
    Test case extra 33:  ATX heading this is only a backslash as in a hard line break
    """

    # Arrange
    source_markdown = """## \\"""
    expected_tokens = ["[atx(1,1):2:0:]", "[text(1,4):\\: ]", "[end-atx::]"]
    expected_gfm = """<h2>\\</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_34():
    """
    Test case extra 34:  ATX heading this is only 2+ spaces as in a hard line break
    """

    # Arrange
    source_markdown = """##    """
    expected_tokens = ["[atx(1,1):2:0:]", "[text(1,7)::    ]", "[end-atx::]"]
    expected_gfm = """<h2></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_35():
    """
    Test case extra 35:  ATX heading this is only a code span.
    """

    # Arrange
    source_markdown = """## ``day``"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        "[icode-span(1,4):day:``::]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2><code>day</code></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_36():
    """
    Test case extra 36:  ATX heading this is only a character reference.
    """

    # Arrange
    source_markdown = """## &amp;"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):\a&amp;\a\a&\a&amp;\a\a: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>&amp;</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_37():
    """
    Test case extra 37:  ATX heading this is only a raw html block.
    """

    # Arrange
    source_markdown = """## <there it='is'>"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        "[raw-html(1,4):there it='is']",
        "[end-atx::]",
    ]
    expected_gfm = """<h2><there it='is'></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_38():
    """
    Test case extra 38:  ATX heading this is only an URI autolink
    """

    # Arrange
    source_markdown = """## <http://www.google.com>"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        "[uri-autolink(1,4):http://www.google.com]",
        "[end-atx::]",
    ]
    expected_gfm = (
        """<h2><a href="http://www.google.com">http://www.google.com</a></h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_39():
    """
    Test case extra 39:  ATX heading this is only an email autolink
    """

    # Arrange
    source_markdown = """## <foo@bar.com>"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        "[email-autolink(1,4):foo@bar.com]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2><a href="mailto:foo@bar.com">foo@bar.com</a></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_40():
    """
    Test case extra 40:  ATX heading this is only an emphasis
    """

    # Arrange
    source_markdown = """## *me*"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        "[emphasis(1,4):1:*]",
        "[text(1,5):me:]",
        "[end-emphasis(1,7)::]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2><em>me</em></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_41():
    """
    Test case extra 41:  ATX heading this is only a link.
    """

    # Arrange
    source_markdown = """## [Foo](/uri)"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        "[link(1,4):inline:/uri:::::Foo:False::::]",
        "[text(1,5):Foo:]",
        "[end-link::]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2><a href="/uri">Foo</a></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_42():
    """
    Test case extra 42:  ATX heading this is only an image
    """

    # Arrange
    source_markdown = """## ![foo](/url "title")"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4)::\a \a\x03\a]",
        '[image(1,4):inline:/url:title:foo::::foo:False:":: :]',
        "[end-atx::]",
    ]
    expected_gfm = """<h2><img src="/url" alt="foo" title="title" /></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_43x():
    """
    Test case extra 43x:  Not quote ATX.
    """

    # Arrange
    source_markdown = """#Heading 1 with no blank lines"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):#Heading 1 with no blank lines:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>#Heading 1 with no blank lines</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_43a():
    """
    Test case extra 43:  Not quote ATX, on either of two possible lines.
    """

    # Arrange
    source_markdown = """#Heading 1 with no blank lines
##Heading 2 with no blank lines"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):#Heading 1 with no blank lines\n##Heading 2 with no blank lines::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>#Heading 1 with no blank lines\n##Heading 2 with no blank lines</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_44x():
    """
    Test case extra 44:  Tab character instead of space between the # and text.
    """

    # Arrange
    source_markdown = """#\tHeading 1 with no blank lines"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):Heading 1 with no blank lines:\t]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>Heading 1 with no blank lines</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_extra_44a():
    """
    Test case extra 44:  Tab character instead of space between the # and text at the end.
    """

    # Arrange
    source_markdown = """# Heading 1 with no blank lines\t#"""
    expected_tokens = [
        "[atx(1,1):1:1:]",
        "[text(1,3):Heading 1 with no blank lines: ]",
        "[end-atx::\t]",
    ]
    expected_gfm = """<h1>Heading 1 with no blank lines</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
