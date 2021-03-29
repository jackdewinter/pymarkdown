"""
https://github.github.com/gfm/#setext-headings
"""
import pytest

from .utils import act_and_assert

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_setext_headings_extra_01():
    """
    Test case extra 1:  SetExt heading starts with a backslash escape
    """

    # Arrange
    source_markdown = """\\\\this is a fun day
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\\\b\\this is a fun day:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>\\this is a fun day</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_02():
    """
    Test case extra 2:  SetExt heading starts with a backslash as in a hard line break
    """

    # Arrange
    source_markdown = """\\
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\\:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>\\</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_03():
    """
    Test case extra 3:  SetExt heading starts with 2+ spaces as in a hard line break
    """

    # Arrange
    source_markdown = """\a\a\a
---""".replace(
        "\a", " "
    )
    expected_tokens = ["[BLANK(1,1):   ]", "[tbreak(2,1):-::---]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_04():
    """
    Test case extra 4:  SetExt heading string starting with a code span.
    """

    # Arrange
    source_markdown = """``this`` is a fun day
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[icode-span(1,1):this:``::]",
        "[text(1,9): is a fun day:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><code>this</code> is a fun day</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_05():
    """
    Test case extra 5:  SetExt heading string starting with a character reference.
    """

    # Arrange
    source_markdown = """&amp; the band played on
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\a&amp;\a\a&\a&amp;\a\a the band played on:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>&amp; the band played on</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_06():
    """
    Test case extra 6:  SetExt heading string starting with a raw html block.
    """

    # Arrange
    source_markdown = """<there it='is'>, really
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[raw-html(1,1):there it='is']",
        "[text(1,16):, really:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><there it='is'>, really</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_07():
    """
    Test case extra 7:  SetExt heading string starting with an URI autolink
    """

    # Arrange
    source_markdown = """<http://www.google.com> is where to look
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[uri-autolink(1,1):http://www.google.com]",
        "[text(1,24): is where to look:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><a href="http://www.google.com">http://www.google.com</a> is where to look</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_08():
    """
    Test case extra 8:  SetExt heading string starting with an email autolink
    """

    # Arrange
    source_markdown = """<foo@bar.com> for more information
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[email-autolink(1,1):foo@bar.com]",
        "[text(1,14): for more information:]",
        "[end-setext::]",
    ]
    expected_gfm = (
        """<h2><a href="mailto:foo@bar.com">foo@bar.com</a> for more information</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_09():
    """
    Test case extra 9:  SetExt heading string starting with an emphasis
    """

    # Arrange
    source_markdown = """*it's* me!
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):it's:]",
        "[end-emphasis(1,6)::]",
        "[text(1,7): me!:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><em>it's</em> me!</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_10():
    """
    Test case extra 10:  SetExt heading string starting with a link.  also see 183
    """

    # Arrange
    source_markdown = """[Foo](/uri) is a link
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[link(1,1):inline:/uri:::::Foo:False::::]",
        "[text(1,2):Foo:]",
        "[end-link::]",
        "[text(1,12): is a link:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><a href="/uri">Foo</a> is a link</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_11():
    """
    Test case extra 11:  SetExt heading string starting with an image
    """

    # Arrange
    source_markdown = """![foo](/url "title") is an image
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        '[image(1,1):inline:/url:title:foo::::foo:False:":: :]',
        "[text(1,21): is an image:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><img src="/url" alt="foo" title="title" /> is an image</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_12():
    """
    Test case extra 12:  SetExt heading containing a backslash
    """

    # Arrange
    source_markdown = """this is a \\\\fun\\\\ day
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):this is a \\\b\\fun\\\b\\ day:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>this is a \\fun\\ day</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_13():
    """
    Test case extra 13:  SetExt heading containing a code span.
    """

    # Arrange
    source_markdown = """this is a ``fun`` day
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):this is a :]",
        "[icode-span(1,11):fun:``::]",
        "[text(1,18): day:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>this is a <code>fun</code> day</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_14():
    """
    Test case extra 14:  SetExt heading containing a character reference.
    """

    # Arrange
    source_markdown = """fun &amp; joy
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):fun \a&amp;\a\a&\a&amp;\a\a joy:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>fun &amp; joy</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_15():
    """
    Test case extra 15:  SetExt heading containing a raw html block.
    """

    # Arrange
    source_markdown = """where <there it='is'> it
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):where :]",
        "[raw-html(1,7):there it='is']",
        "[text(1,22): it:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>where <there it='is'> it</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_16():
    """
    Test case extra 16:  SetExt heading containing an URI autolink
    """

    # Arrange
    source_markdown = """look at <http://www.google.com> for answers
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):look at :]",
        "[uri-autolink(1,9):http://www.google.com]",
        "[text(1,32): for answers:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>look at <a href="http://www.google.com">http://www.google.com</a> for answers</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_17():
    """
    Test case extra 17:  SetExt heading containing an email autolink
    """

    # Arrange
    source_markdown = """email <foo@bar.com> for answers
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):email :]",
        "[email-autolink(1,7):foo@bar.com]",
        "[text(1,20): for answers:]",
        "[end-setext::]",
    ]
    expected_gfm = (
        """<h2>email <a href="mailto:foo@bar.com">foo@bar.com</a> for answers</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_18():
    """
    Test case extra 18:  SetExt heading containing emphasis
    """

    # Arrange
    source_markdown = """really! *it's me!* here!
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):really! :]",
        "[emphasis(1,9):1:*]",
        "[text(1,10):it's me!:]",
        "[end-emphasis(1,18)::]",
        "[text(1,19): here!:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>really! <em>it's me!</em> here!</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_19():
    """
    Test case extra 19:  SetExt heading containing a link.
    """

    # Arrange
    source_markdown = """look at [Foo](/uri) for more
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):look at :]",
        "[link(1,9):inline:/uri:::::Foo:False::::]",
        "[text(1,10):Foo:]",
        "[end-link::]",
        "[text(1,20): for more:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>look at <a href="/uri">Foo</a> for more</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_20():
    """
    Test case extra 20:  SetExt heading containing an image
    """

    # Arrange
    source_markdown = """special ![foo](/url "title") headings
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):special :]",
        '[image(1,9):inline:/url:title:foo::::foo:False:":: :]',
        "[text(1,29): headings:]",
        "[end-setext::]",
    ]
    expected_gfm = (
        """<h2>special <img src="/url" alt="foo" title="title" /> headings</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_21():
    """
    Test case extra 21:  SetExt headings ends with a backslash escape
    """

    # Arrange
    source_markdown = """this is a fun day\\\\
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):this is a fun day\\\b\\:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>this is a fun day\\</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_22():
    """
    Test case extra 22:  SetExt heading ends with a backslash as in a hard line break
    """

    # Arrange
    source_markdown = """this was \\
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):this was \\:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>this was \\</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_22a():
    """
    Test case extra 22a:  SetExt heading ends with a backslash as in a hard line break
    """

    # Arrange
    source_markdown = """this was \\
another line
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):this was :]",
        "[hard-break(1,10):\\:\n]",
        "[text(2,1):another line:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>this was <br />\nanother line</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_22b():
    """
    Test case extra 22a:  SetExt heading ends with a backslash as in a hard line break
    """

    # Arrange
    source_markdown = """this was
another line
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):this was\nanother line::\n]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>this was\nanother line</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_22c():
    """
    Test case extra 22a:  SetExt heading ends with a backslash as in a hard line break
    """

    # Arrange
    source_markdown = """this was\a\a\a
another line
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):this was:]",
        "[hard-break(1,9):   :\n]",
        "[text(2,1):another line:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>this was<br />\nanother line</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_22d():
    """
    Test case extra 22a:  SetExt heading ends with a backslash as in a hard line break
    """

    # Arrange
    source_markdown = """this was\a\a\a
 another line
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):this was:]",
        "[hard-break(1,9):   :\n]",
        "[text(2,2):another line:: \x02]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>this was<br />\nanother line</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_23():
    """
    Test case extra 23:  SetExt heading ends with 2+ spaces as in a hard line break
    """

    # Arrange
    source_markdown = """what? no line break?\a\a\a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(2,1):-:3::(1,1):   ]",
        "[text(1,1):what? no line break?:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>what? no line break?</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_23a():
    """
    Test case extra 23a:  SetExt heading ends with 2+ spaces as in a hard line break
    """

    # Arrange
    source_markdown = """what? no line break?\a\a\a
woe is me
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):what? no line break?:]",
        "[hard-break(1,21):   :\n]",
        "[text(2,1):woe is me:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>what? no line break?<br />\nwoe is me</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_24():
    """
    Test case extra 24:  SetExt heading string ending with a code span.
    """

    # Arrange
    source_markdown = """this is a fun ``day``
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):this is a fun :]",
        "[icode-span(1,15):day:``::]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>this is a fun <code>day</code></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_25():
    """
    Test case extra 25:  SetExt heading string ending with a character reference.
    """

    # Arrange
    source_markdown = """the band played on &amp;
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):the band played on \a&amp;\a\a&\a&amp;\a\a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>the band played on &amp;</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_26():
    """
    Test case extra 26:  SetExt heading string ending with a raw html block.
    """

    # Arrange
    source_markdown = """really, <there it='is'>
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):really, :]",
        "[raw-html(1,9):there it='is']",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>really, <there it='is'></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_27():
    """
    Test case extra 27:  SetExt heading string ending with an URI autolink
    """

    # Arrange
    source_markdown = """look at <http://www.google.com>
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):look at :]",
        "[uri-autolink(1,9):http://www.google.com]",
        "[end-setext::]",
    ]
    expected_gfm = (
        """<h2>look at <a href="http://www.google.com">http://www.google.com</a></h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_28():
    """
    Test case extra 28:  SetExt heading string ending with an email autolink
    """

    # Arrange
    source_markdown = """for more information, contact <foo@bar.com>
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):for more information, contact :]",
        "[email-autolink(1,31):foo@bar.com]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>for more information, contact <a href="mailto:foo@bar.com">foo@bar.com</a></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_29():
    """
    Test case extra 29:  SetExt heading string ending with an emphasis
    """

    # Arrange
    source_markdown = """it's *me*
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):it's :]",
        "[emphasis(1,6):1:*]",
        "[text(1,7):me:]",
        "[end-emphasis(1,9)::]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>it's <em>me</em></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_30():
    """
    Test case extra 30:  SetExt heading string ending with a link.
    """

    # Arrange
    source_markdown = """a link looks like [Foo](/uri)
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a link looks like :]",
        "[link(1,19):inline:/uri:::::Foo:False::::]",
        "[text(1,20):Foo:]",
        "[end-link::]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a link looks like <a href="/uri">Foo</a></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_31():
    """
    Test case extra 31:  SetExt heading string ending with an image
    """

    # Arrange
    source_markdown = """an image is ![foo](/url "title")
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):an image is :]",
        '[image(1,13):inline:/url:title:foo::::foo:False:":: :]',
        "[end-setext::]",
    ]
    expected_gfm = """<h2>an image is <img src="/url" alt="foo" title="title" /></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_32():
    """
    Test case extra 32:  SetExt heading this is only a backslash escape
    """

    # Arrange
    source_markdown = """\\\\
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\\\b\\:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>\\</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_33():
    """
    Test case extra 33:  SetExt heading this is only a backslash as in a hard line break
    """

    # Arrange
    source_markdown = """ \\
---"""
    expected_tokens = [
        "[setext(2,1):-:3: :(1,2)]",
        "[text(1,2):\\:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>\\</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_34():
    """
    Test case extra 34:  SetExt heading this is only 2+ spaces as in a hard line break
    """

    # Arrange
    source_markdown = """\a\a\a\a
---""".replace(
        "\a", " "
    )
    expected_tokens = ["[BLANK(1,1):    ]", "[tbreak(2,1):-::---]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_35():
    """
    Test case extra 35:  SetExt heading this is only a code span.
    """

    # Arrange
    source_markdown = """``day``
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[icode-span(1,1):day:``::]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><code>day</code></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_36():
    """
    Test case extra 36:  SetExt heading this is only a character reference.
    """

    # Arrange
    source_markdown = """&amp;
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\a&amp;\a\a&\a&amp;\a\a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>&amp;</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_37():
    """
    Test case extra 37:  SetExt heading this is only a raw html block.
    """

    # Arrange
    source_markdown = """<there it='is'>
---"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<there it='is'>\n---:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<there it='is'>\n---"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_38():
    """
    Test case extra 38:  SetExt heading this is only an URI autolink
    """

    # Arrange
    source_markdown = """<http://www.google.com>
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[uri-autolink(1,1):http://www.google.com]",
        "[end-setext::]",
    ]
    expected_gfm = (
        """<h2><a href="http://www.google.com">http://www.google.com</a></h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_39():
    """
    Test case extra 39:  SetExt heading this is only an email autolink
    """

    # Arrange
    source_markdown = """<foo@bar.com>
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[email-autolink(1,1):foo@bar.com]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><a href="mailto:foo@bar.com">foo@bar.com</a></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_40():
    """
    Test case extra 40:  SetExt heading this is only an emphasis
    """

    # Arrange
    source_markdown = """*me*
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):me:]",
        "[end-emphasis(1,4)::]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><em>me</em></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_41():
    """
    Test case extra 41:  SetExt heading this is only a link.
    """

    # Arrange
    source_markdown = """[Foo](/uri)
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[link(1,1):inline:/uri:::::Foo:False::::]",
        "[text(1,2):Foo:]",
        "[end-link::]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2><a href="/uri">Foo</a></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_42():
    """
    Test case extra 42:  SetExt heading this is only an image
    """

    # Arrange
    source_markdown = """![foo](/url "title")
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        '[image(1,1):inline:/url:title:foo::::foo:False:":: :]',
        "[end-setext::]",
    ]
    expected_gfm = """<h2><img src="/url" alt="foo" title="title" /></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_43():
    """
    Test case extra 43:  SetExt heading with code span with newline inside
    """

    # Arrange
    source_markdown = """a`code
span`a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[icode-span(1,2):code\a\n\a \aspan:`::]",
        "[text(2,6):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<code>code span</code>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_44():
    """
    Test case extra 44:  SetExt heading with raw HTML with newline inside
    """

    # Arrange
    source_markdown = """a<raw
html='cool'>a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[raw-html(1,2):raw\nhtml='cool']",
        "[text(2,13):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<raw\nhtml='cool'>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_45():
    """
    Test case extra 45:  SetExt heading with URI autolink with newline inside, renders invalid
    """

    # Arrange
    source_markdown = """a<http://www.
google.com>a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a\a<\a&lt;\ahttp://www.\ngoogle.com\a>\a&gt;\aa::\n]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a&lt;http://www.\ngoogle.com&gt;a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_46():
    """
    Test case extra 46:  SetExt heading with email autolink with newline inside, renders invalid
    """

    # Arrange
    source_markdown = """a<foo@bar
.com>a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a\a<\a&lt;\afoo@bar\n.com\a>\a&gt;\aa::\n]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a&lt;foo@bar\n.com&gt;a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_47():
    """
    Test case extra 47:  SetExt heading with inline link with newline in label
    ??? repeat of 518 series?
    """

    # Arrange
    source_markdown = """a[Fo
o](/uri "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Fo\no:False:":: :]',
        "[text(1,3):Fo\no::\n]",
        "[end-link::]",
        "[text(2,19):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Fo\no</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_48():
    """
    Test case extra 48:  SetExt heading with inline link with newline in pre-URI space
    """

    # Arrange
    source_markdown = """a[Foo](
/uri "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":\n: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,16):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_48a():
    """
    Test case extra 48a:  48 with whitespace before newline
    """

    # Arrange
    source_markdown = """a[Foo](\a\a
/uri "testing")a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":  \n: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,16):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_48b():
    """
    Test case extra 48b:  48 with whitespace after newline
    """

    # Arrange
    source_markdown = """a[Foo](
   /uri "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":\n   : :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,19):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_48c():
    """
    Test case extra 48c:  48 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a[Foo](\a\a
   /uri "testing")a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":  \n   : :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,19):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_49():
    """
    Test case extra 49:  SetExt heading with inline link with newline in URI, invalidating it
    """

    # Arrange
    source_markdown = """a[Foo](/ur
i "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):Foo:]",
        "[text(1,6):]:]",
        '[text(1,7):(/ur\ni \a"\a&quot;\atesting\a"\a&quot;\a)a::\n]',
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a[Foo](/ur\ni &quot;testing&quot;)a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_50x():
    """
    Test case extra 50:  SetExt heading with inline link with newline in post-URI space
    """

    # Arrange
    source_markdown = """a[Foo](/uri\a
"testing")a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: \n:]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,11):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_50a():
    """
    Test case extra 50:  50 with whitespace before newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri\a\a
"testing")a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:"::  \n:]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,11):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_50b():
    """
    Test case extra 50:  50 with whitespace after newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri
   "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:"::\n   :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,14):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_50c():
    """
    Test case extra 50c:  50 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri\a\a
   "testing")a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:"::  \n   :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,14):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_51():
    """
    Test case extra 51:  SetExt heading with inline link with newline in title
    """

    # Arrange
    source_markdown = """a[Foo](/uri "test
ing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:test\ning::::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,6):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="test\ning">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_52x():
    """
    Test case extra 52:  SetExt heading with inline link with newline after title
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing"
)a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :\n]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,2):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_52a():
    """
    Test case extra 52:  52 with whitespace before newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing"\a\a
)a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :  \n]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,2):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_52b():
    """
    Test case extra 52b:  52 with whitespace after newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing"
  )a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :\n  ]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,4):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_52c():
    """
    Test case extra 52c:  52 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing"\a\a
  )a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :  \n  ]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,4):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_53():
    """
    Test case extra 53:  SetExt heading with full link with newline in label
    """

    # Arrange
    source_markdown = """a[foo
bar][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo\nbar:::::]",
        "[text(1,3):foo\nbar::\n]",
        "[end-link::]",
        "[text(2,10):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo\nbar</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_54():
    """
    Test case extra 54:  SetExt heading with full link with newline in reference
    """

    # Arrange
    source_markdown = """a[foo][ba
r]a
---

[ba\nr]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::ba\nr:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(2,3):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba r:ba\nr: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_55():
    """
    Test case extra 55:  SetExt heading with shortcut link with newline in label
    """

    # Arrange
    source_markdown = """a[ba
r]a
---

[ba\nr]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::ba\nr:::::]",
        "[text(1,3):ba\nr::\n]",
        "[end-link::]",
        "[text(2,3):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba r:ba\nr: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">ba\nr</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_56():
    """
    Test case extra 56:  SetExt heading with collapsed link with newline in label
    """

    # Arrange
    source_markdown = """a[ba
r][]a
---

[ba\nr]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::ba\nr:::::]",
        "[text(1,3):ba\nr::\n]",
        "[end-link::]",
        "[text(2,5):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba r:ba\nr: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">ba\nr</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_57():
    """
    Test case extra 57:  SetExt heading with collapsed link with newline in label
    """

    # Arrange
    source_markdown = """a[
bar][]a
---

[\nbar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::\nbar:::::]",
        "[text(1,3):\nbar::\n]",
        "[end-link::]",
        "[text(2,7):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:\nbar: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">\nbar</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_58():
    """
    Test case extra 58:  SetExt heading with full link with newline in reference
    """

    # Arrange
    source_markdown = """a[foo][
bar]a
---

[\nbar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::\nbar:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(2,5):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:\nbar: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_59():
    """
    Test case extra 59:  SetExt heading with inline image with newline between image chars, invalidating it.
    """

    # Arrange
    source_markdown = """a!
[Foo](/uri "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a!\n::\n]",
        '[link(2,1):inline:/uri:testing::::Foo:False:":: :]',
        "[text(2,2):Foo:]",
        "[end-link::]",
        "[text(2,22):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a!\n<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_60():
    """
    Test case extra 60:  SetExt heading with inline link with newline in label but not title.
    """

    # Arrange
    source_markdown = """a[Fo
o](/uri)a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/uri:::::Fo\no:False::::]",
        "[text(1,3):Fo\no::\n]",
        "[end-link::]",
        "[text(2,9):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri">Fo\no</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_61():
    """
    Test case extra 61:  SetExt heading with inline image with newline in label
    """

    # Arrange
    source_markdown = """a![fo
o](/url "title")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/url:title:fo\no::::fo\no:False:":: :]',
        "[text(2,17):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="fo\no" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_62():
    """
    Test case extra 62:  SetExt heading with inline image with newline before URI
    """

    # Arrange
    source_markdown = """a![Foo](
/uri "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":\n: :]',
        "[text(2,16):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_62a():
    """
    Test case extra 62a:  62 with whitespace before newline
    """

    # Arrange
    source_markdown = """a![Foo](\a\a
/uri "testing")a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":  \n: :]',
        "[text(2,16):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_62b():
    """
    Test case extra 62b:  62 with whitespace after newline
    """

    # Arrange
    source_markdown = """a![Foo](
   /uri "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":\n   : :]',
        "[text(2,19):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_62c():
    """
    Test case extra 62c:  62 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a![Foo](\a\a
   /uri "testing")a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":  \n   : :]',
        "[text(2,19):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_63():
    """
    Test case extra 63:  SetExt heading with inline image with newline in the URI, invalidating it
    """

    # Arrange
    source_markdown = """a![Foo](/ur
i "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):Foo:]",
        "[text(1,7):]:]",
        '[text(1,8):(/ur\ni \a"\a&quot;\atesting\a"\a&quot;\a)a::\n]',
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a![Foo](/ur\ni &quot;testing&quot;)a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_64x():
    """
    Test case extra 64:  SetExt heading with inline image with newline after the URI
    """

    # Arrange
    source_markdown = """a![Foo](/uri
"testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:"::\n:]',
        "[text(2,11):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_64a():
    """
    Test case extra 64a:  64 with whitespace before newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri\a\a
"testing")a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:"::  \n:]',
        "[text(2,11):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_64b():
    """
    Test case extra 64b:  64 with whitespace after newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri
 "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:"::\n :]',
        "[text(2,12):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_64c():
    """
    Test case extra 64c:  64 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri\a\a
 "testing")a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:"::  \n :]',
        "[text(2,12):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_65():
    """
    Test case extra 65:  SetExt heading with inline image with newline after the URI and no text
    """

    # Arrange
    source_markdown = """a![Foo](/uri
)a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/uri::Foo::::Foo:False:::\n:]",
        "[text(2,2):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_66():
    """
    Test case extra 66:  SetExt heading with inline image with newline in the title
    """

    # Arrange
    source_markdown = """a![Foo](/uri "test
ing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:test\ning:Foo::::Foo:False:":: :]',
        "[text(2,6):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="test\ning" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_67():
    """
    Test case extra 67:  SetExt heading with inline image with newline after the title
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing"
)a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :\n]',
        "[text(2,2):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_67a():
    """
    Test case extra 67a:  67 with whitespace before newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing"\a\a
)a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :  \n]',
        "[text(2,2):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_67b():
    """
    Test case extra 67b:  67 with whitespace after newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing"
   )a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :\n   ]',
        "[text(2,5):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_67c():
    """
    Test case extra 67c:  67 with whitespace before and after newline
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing"\a\a
   )a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :  \n   ]',
        "[text(2,5):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_68x():
    """
    Test case extra 68:  SetExt heading with link containing label with replacement
    """

    # Arrange
    source_markdown = """a[Fo&beta;o](/uri "testing")a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Fo&beta;o:False:":: :]',
        "[text(1,3):Fo\a&beta;\aβ\ao:]",
        "[end-link::]",
        "[text(1,29):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foβo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_68a():
    """
    Test case extra 68a:  68 without special characters
    """

    # Arrange
    source_markdown = """a[Foo](/uri "testing")a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(1,23):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_68b():
    """
    Test case extra 68b:  68 with newline before special characters
    """

    # Arrange
    source_markdown = """a[Fo
&beta;o](/uri "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Fo\n&beta;o:False:":: :]',
        "[text(1,3):Fo\n\a&beta;\aβ\ao::\n]",
        "[end-link::]",
        "[text(2,25):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Fo\nβo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_69():
    """
    Test case extra 69:  SetExt heading with link containing label with backslash
    """

    # Arrange
    source_markdown = """a[Fo\\]o](/uri "testing")a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Fo\\]o:False:":: :]',
        "[text(1,3):Fo\\\b]o:]",
        "[end-link::]",
        "[text(1,25):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Fo]o</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_69a():
    """
    Test case extra 69a:  69 with newline before special characters
    """

    # Arrange
    source_markdown = """a[Fo
\\]o](/uri "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testing::::Fo\n\\]o:False:":: :]',
        "[text(1,3):Fo\n\\\b]o::\n]",
        "[end-link::]",
        "[text(2,21):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testing">Fo\n]o</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_70():
    """
    Test case extra 70:  SetExt heading with link containing uri with space
    """

    # Arrange
    source_markdown = """a[Foo](</my uri> "testing")a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/my%20uri:testing:/my uri:::Foo:True:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(1,28):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/my%20uri" title="testing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_70a():
    """
    Test case extra 70a:  70 with newline before special characters, rendering it invalid
    """

    # Arrange
    source_markdown = """a[Foo](</my
 uri> "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[text(1,2):[:]",
        "[text(1,3):Foo:]",
        "[text(1,6):]:]",
        '[text(1,7):(\a<\a&lt;\a/my\nuri\a>\a&gt;\a \a"\a&quot;\atesting\a"\a&quot;\a)a::\n \x02]',
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a[Foo](&lt;/my\nuri&gt; &quot;testing&quot;)a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_71():
    """
    Test case extra 71:  SetExt heading with link containing title with replacement
    """

    # Arrange
    source_markdown = """a[Foo](/uri "test&beta;ing")a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:testβing::test&beta;ing::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(1,29):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="testβing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_71a():
    """
    Test case extra 71a:  71 with newline before special characters
    """

    # Arrange
    source_markdown = """a[Foo](/uri "test
&beta;ing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:test\nβing::test\n&beta;ing::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,12):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="test\nβing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_72():
    """
    Test case extra 72:  SetExt heading with link containing title with backslash
    """

    # Arrange
    source_markdown = """a[Foo](/uri "test\\#ing")a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:test#ing::test\\#ing::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(1,25):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="test#ing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_72a():
    """
    Test case extra 72a:  72 with newline before special characters
    """

    # Arrange
    source_markdown = """a[Foo](/uri "test
\\#ing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:test\n#ing::test\n\\#ing::Foo:False:":: :]',
        "[text(1,3):Foo:]",
        "[end-link::]",
        "[text(2,8):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<a href="/uri" title="test\n#ing">Foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_73():
    """
    Test case extra 73:  SetExt heading with image containing label with replacement
    """

    # Arrange
    source_markdown = """a![Fo&beta;o](/uri "testing")a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foβo::::Fo&beta;o:False:":: :]',
        "[text(1,30):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foβo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_73a():
    """
    Test case extra 73a:  73 without special characters
    """

    # Arrange
    source_markdown = """a![Foo](/uri "testing")a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Foo::::Foo:False:":: :]',
        "[text(1,24):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_73b():
    """
    Test case extra 73b:  73 with newline before special characters
    """

    # Arrange
    source_markdown = """a![Fo
&beta;o](/uri "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Fo\nβo::::Fo\n&beta;o:False:":: :]',
        "[text(2,25):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Fo\nβo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_74():
    """
    Test case extra 74:  SetExt heading with image containing label with backslash
    """

    # Arrange
    source_markdown = """a![Fo\\]o](/uri "testing")a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Fo]o::::Fo\\]o:False:":: :]',
        "[text(1,26):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Fo]o" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_74a():
    """
    Test case extra 74a:  74 with newline before special characters
    """

    # Arrange
    source_markdown = """a![Fo
\\]o](/uri "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testing:Fo\n]o::::Fo\n\\]o:False:":: :]',
        "[text(2,21):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Fo\n]o" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_75():
    """
    Test case extra 75:  SetExt heading with image containing uri with space
    """

    # Arrange
    source_markdown = """a![Foo](</my uri> "testing")a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/my%20uri:testing:Foo:/my uri:::Foo:True:":: :]',
        "[text(1,29):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/my%20uri" alt="Foo" title="testing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_75a():
    """
    Test case extra 75a:  75 with newline before special characters, invalidating it
    """

    # Arrange
    source_markdown = """a![Foo](</my
 uri> "testing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[text(1,2):![:]",
        "[text(1,4):Foo:]",
        "[text(1,7):]:]",
        '[text(1,8):(\a<\a&lt;\a/my\nuri\a>\a&gt;\a \a"\a&quot;\atesting\a"\a&quot;\a)a::\n \x02]',
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a![Foo](&lt;/my\nuri&gt; &quot;testing&quot;)a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_76():
    """
    Test case extra 76:  SetExt heading with image containing title with replacement
    """

    # Arrange
    source_markdown = """a![Foo](/uri "test&beta;ing")a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:testβing:Foo::test&beta;ing::Foo:False:":: :]',
        "[text(1,30):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="testβing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_76a():
    """
    Test case extra 76a:  76 with newline before special characters
    """

    # Arrange
    source_markdown = """a![Foo](/uri "test
&beta;ing")a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:test\nβing:Foo::test\n&beta;ing::Foo:False:":: :]',
        "[text(2,12):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="test\nβing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_77():
    """
    Test case extra 77:  SetExt heading with image containing title with backslash
    """

    # Arrange
    source_markdown = """a![Foo](/uri "test\\#ing")a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:test#ing:Foo::test\\#ing::Foo:False:":: :]',
        "[text(1,26):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="test#ing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_77a():
    """
    Test case extra 77a:  77 with newline before special characters
    """

    # Arrange
    source_markdown = """a![Foo](/uri "test\\#ing")a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:test#ing:Foo::test\\#ing::Foo:False:":: :]',
        "[text(1,26):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/uri" alt="Foo" title="test#ing" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_78():
    """
    Test case extra 78:  SetExt heading with full link with backslash in label
    """

    # Arrange
    source_markdown = """a[foo\\#bar][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo\\#bar:::::]",
        "[text(1,3):foo\\\b#bar:]",
        "[end-link::]",
        "[text(1,17):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo#bar</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_78a():
    """
    Test case extra 78a:  78 with newline before special chars
    """

    # Arrange
    source_markdown = """a[foo
\\#bar][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo\n\\#bar:::::]",
        "[text(1,3):foo\n\\\b#bar::\n]",
        "[end-link::]",
        "[text(2,12):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo\n#bar</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_79():
    """
    Test case extra 79:  SetExt heading with full link with replacement in label
    """

    # Arrange
    source_markdown = """a[foo&beta;bar][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo&beta;bar:::::]",
        "[text(1,3):foo\a&beta;\aβ\abar:]",
        "[end-link::]",
        "[text(1,21):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">fooβbar</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_79a():
    """
    Test case extra 79a:  79 with newline before special characters
    """

    # Arrange
    source_markdown = """a[foo
&beta;bar][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:foo\n&beta;bar:::::]",
        "[text(1,3):foo\n\a&beta;\aβ\abar::\n]",
        "[end-link::]",
        "[text(2,16):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo\nβbar</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_80():
    """
    Test case extra 80:  SetExt heading with full link with replacement in reference
    """

    # Arrange
    source_markdown = """a[foo][ba&beta;r]a
---

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::ba&beta;r:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(1,18):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_80a():
    """
    Test case extra 80a:  80 with newline before special characters
    """

    # Arrange
    source_markdown = """a[foo][ba
&beta;r]a
---

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::ba\n&beta;r:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(2,9):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_81():
    """
    Test case extra 81:  SetExt heading with full link with backspace in reference
    """

    # Arrange
    source_markdown = """a[foo][ba\\]r]a
---

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::ba\\]r:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(1,14):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_81a():
    """
    Test case extra 81a:  81 with newline before special characters
    """

    # Arrange
    source_markdown = """a[foo][ba
\\]r]a
---

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::ba\n\\]r:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(2,5):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_82():
    """
    Test case extra 82:  SetExt heading with shortcut link with replacement in label
    """

    # Arrange
    source_markdown = """a[ba&beta;r]a
---

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::ba&beta;r:::::]",
        "[text(1,3):ba\a&beta;\aβ\ar:]",
        "[end-link::]",
        "[text(1,13):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">baβr</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_82a():
    """
    Test case extra 82a:  82 with newline before special characters
    """

    # Arrange
    source_markdown = """a[ba
&beta;r]a
---

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::ba\n&beta;r:::::]",
        "[text(1,3):ba\n\a&beta;\aβ\ar::\n]",
        "[end-link::]",
        "[text(2,9):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">ba\nβr</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_83():
    """
    Test case extra 83:  SetExt heading with shortcut link with backslash in label
    """

    # Arrange
    source_markdown = """a[ba\\]r]a
---

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::ba\\]r:::::]",
        "[text(1,3):ba\\\b]r:]",
        "[end-link::]",
        "[text(1,9):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">ba]r</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_83a():
    """
    Test case extra 83a:  83 with newline before special characters
    """

    # Arrange
    source_markdown = """a[ba
\\]r]a
---

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::ba\n\\]r:::::]",
        "[text(1,3):ba\n\\\b]r::\n]",
        "[end-link::]",
        "[text(2,5):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">ba\n]r</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_84x():
    """
    Test case extra 84:  SetExt heading with collapsed link with replacement in label
    """

    # Arrange
    source_markdown = """a[ba&beta;r][]a
---

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::ba&beta;r:::::]",
        "[text(1,3):ba\a&beta;\aβ\ar:]",
        "[end-link::]",
        "[text(1,15):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">baβr</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_84a():
    """
    Test case extra 84a:  84 with newline before special characters
    """

    # Arrange
    source_markdown = """a[ba
&beta;r][]a
---

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::ba\n&beta;r:::::]",
        "[text(1,3):ba\n\a&beta;\aβ\ar::\n]",
        "[end-link::]",
        "[text(2,11):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">ba\nβr</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_85():
    """
    Test case extra 85:  SetExt heading with collapsed link with backslash in label
    """

    # Arrange
    source_markdown = """a[ba\\]r][]a
---

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::ba\\]r:::::]",
        "[text(1,3):ba\\\b]r:]",
        "[end-link::]",
        "[text(1,11):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">ba]r</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_85a():
    """
    Test case extra 85a:  85 with newline before special characters
    """

    # Arrange
    source_markdown = """a[ba
\\]r][]a
---

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::ba\n\\]r:::::]",
        "[text(1,3):ba\n\\\b]r::\n]",
        "[end-link::]",
        "[text(2,7):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">ba\n]r</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_86x():
    """
    Test case extra 86:  SetExt heading with full link with replacement in label
    """

    # Arrange
    source_markdown = """a[fo&beta;o][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:fo&beta;o:::::]",
        "[text(1,3):fo\a&beta;\aβ\ao:]",
        "[end-link::]",
        "[text(1,18):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foβo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_86a():
    """
    Test case extra 86a:  86 with newline before special characters
    """

    # Arrange
    source_markdown = """a[fo
&beta;o][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:fo\n&beta;o:::::]",
        "[text(1,3):fo\n\a&beta;\aβ\ao::\n]",
        "[end-link::]",
        "[text(2,14):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">fo\nβo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_87():
    """
    Test case extra 87:  SetExt heading with full link with backslash in label
    """

    # Arrange
    source_markdown = """a[fo\\]o][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:fo\\]o:::::]",
        "[text(1,3):fo\\\b]o:]",
        "[end-link::]",
        "[text(1,14):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">fo]o</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_87a():
    """
    Test case extra 87a:  87 with newline before special characters
    """

    # Arrange
    source_markdown = """a[fo
\\]o][bar]a
---

[\nbar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:fo\n\\]o:::::]",
        "[text(1,3):fo\n\\\b]o::\n]",
        "[end-link::]",
        "[text(2,10):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:\nbar: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">fo\n]o</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_88x():
    """
    Test case extra 88:  SetExt heading with full link with backslash in link
    """

    # Arrange
    source_markdown = """a[foo][ba\\]r]a
---

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::ba\\]r:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(1,14):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_88a():
    """
    Test case extra 88a:  88 with newline before special characters
    """

    # Arrange
    source_markdown = """a[foo][ba
\\]r]a
---

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::ba\n\\]r:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(2,5):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_89x():
    """
    Test case extra 89:  SetExt heading with full link with replacement in link
    """

    # Arrange
    source_markdown = """a[foo][ba&beta;r]a
---

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::ba&beta;r:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(1,18):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_89a():
    """
    Test case extra 88a:  88 with newline before special characters
    """

    # Arrange
    source_markdown = """a[foo][ba
&beta;r]a
---

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::ba\n&beta;r:foo:::::]",
        "[text(1,3):foo:]",
        "[end-link::]",
        "[text(2,9):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">foo</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_90x():
    """
    Test case extra 90:  SetExt heading with full image with backslash in label
    """

    # Arrange
    source_markdown = """a![foo\\#bar][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo#bar:::bar:foo\\#bar:::::]",
        "[text(1,18):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="foo#bar" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_90a():
    """
    Test case extra 90a:  90 with newline before special chars
    """

    # Arrange
    source_markdown = """a![foo
\\#bar][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo\n#bar:::bar:foo\n\\#bar:::::]",
        "[text(2,12):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="foo\n#bar" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_91x():
    """
    Test case extra 91:  SetExt heading with full image with replacement in label
    """

    # Arrange
    source_markdown = """a![foo&beta;bar][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:fooβbar:::bar:foo&beta;bar:::::]",
        "[text(1,22):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="fooβbar" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_91a():
    """
    Test case extra 91a:  91 with newline before special characters
    """

    # Arrange
    source_markdown = """a![foo
&beta;bar][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo\nβbar:::bar:foo\n&beta;bar:::::]",
        "[text(2,16):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="foo\nβbar" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_92x():
    """
    Test case extra 92:  SetExt heading with full image with replacement in reference
    """

    # Arrange
    source_markdown = """a![foo][ba&beta;r]a
---

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo:::ba&beta;r:foo:::::]",
        "[text(1,19):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="foo" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_92a():
    """
    Test case extra 92a:  92 with newline before special characters
    """

    # Arrange
    source_markdown = """a![foo][ba
&beta;r]a
---

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo:::ba\n&beta;r:foo:::::]",
        "[text(2,9):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="foo" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_93x():
    """
    Test case extra 93:  SetExt heading with full image with backspace in reference
    """

    # Arrange
    source_markdown = """a![foo][ba\\]r]a
---

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo:::ba\\]r:foo:::::]",
        "[text(1,15):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="foo" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_93a():
    """
    Test case extra 93a:  93 with newline before special characters
    """

    # Arrange
    source_markdown = """a![foo][ba
\\]r]a
---

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo:::ba\n\\]r:foo:::::]",
        "[text(2,5):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="foo" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_94x():
    """
    Test case extra 94:  SetExt heading with shortcut image with replacement in label
    """

    # Arrange
    source_markdown = """a![ba&beta;r]a
---

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:baβr::::ba&beta;r:::::]",
        "[text(1,14):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="baβr" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_94a():
    """
    Test case extra 94a:  94 with newline before special characters
    """

    # Arrange
    source_markdown = """a![ba
&beta;r]a
---

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:ba\nβr::::ba\n&beta;r:::::]",
        "[text(2,9):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="ba\nβr" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_95x():
    """
    Test case extra 95:  SetExt heading with shortcut image with backslash in label
    """

    # Arrange
    source_markdown = """a![ba\\]r]a
---

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:ba]r::::ba\\]r:::::]",
        "[text(1,10):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="ba]r" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_95a():
    """
    Test case extra 95a:  95 with newline before special characters
    """

    # Arrange
    source_markdown = """a![ba
\\]r]a
---

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:ba\n]r::::ba\n\\]r:::::]",
        "[text(2,5):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="ba\n]r" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_96x():
    """
    Test case extra 96:  SetExt heading with collapsed image with replacement in label
    """

    # Arrange
    source_markdown = """a![ba&beta;r][]a
---

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:baβr::::ba&beta;r:::::]",
        "[text(1,16):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="baβr" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_96a():
    """
    Test case extra 96a:  96 with newline before special characters
    """

    # Arrange
    source_markdown = """a![ba
&beta;r][]a
---

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:ba\nβr::::ba\n&beta;r:::::]",
        "[text(2,11):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="ba\nβr" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_97x():
    """
    Test case extra 97:  SetExt heading with collapsed image with backslash in label
    """

    # Arrange
    source_markdown = """a![ba\\]r][]a
---

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:ba]r::::ba\\]r:::::]",
        "[text(1,12):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="ba]r" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_97a():
    """
    Test case extra 97a:  97 with newline before special characters
    """

    # Arrange
    source_markdown = """a![ba
\\]r][]a
---

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:ba\n]r::::ba\n\\]r:::::]",
        "[text(2,7):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="ba\n]r" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_98x():
    """
    Test case extra 98:  SetExt heading with full image with replacement in label
    """

    # Arrange
    source_markdown = """a![fo&beta;o][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foβo:::bar:fo&beta;o:::::]",
        "[text(1,19):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="foβo" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_98a():
    """
    Test case extra 98a:  98 with newline before special characters
    """

    # Arrange
    source_markdown = """a![fo
&beta;o][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:fo\nβo:::bar:fo\n&beta;o:::::]",
        "[text(2,14):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="fo\nβo" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_99x():
    """
    Test case extra 99:  SetExt heading with full image with backslash in label
    """

    # Arrange
    source_markdown = """a![fo\\]o][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:fo]o:::bar:fo\\]o:::::]",
        "[text(1,15):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="fo]o" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_99a():
    """
    Test case extra 99a:  99 with newline before special characters
    """

    # Arrange
    source_markdown = """a![fo
\\]o][bar]a
---

[\nbar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:fo\n]o:::bar:fo\n\\]o:::::]",
        "[text(2,10):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:\nbar: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="fo\n]o" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_a0x():
    """
    Test case extra A0:  SetExt heading with full image with backslash in link
    """

    # Arrange
    source_markdown = """a![foo][ba\\]r]a
---

[ba\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo:::ba\\]r:foo:::::]",
        "[text(1,15):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba\\]r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="foo" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_a0a():
    """
    Test case extra A0a:  A0 with newline before special characters
    """

    # Arrange
    source_markdown = """a![foo][ba
\\]r]a
---

[ba
\\]r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo:::ba\n\\]r:foo:::::]",
        "[text(2,5):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba \\]r:ba\n\\]r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="foo" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_a1x():
    """
    Test case extra A1:  SetExt heading with full image with replacement in link
    """

    # Arrange
    source_markdown = """a![foo][ba&beta;r]a
---

[ba&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo:::ba&beta;r:foo:::::]",
        "[text(1,19):a:]",
        "[end-setext::]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::ba&beta;r:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="foo" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_a1a():
    """
    Test case extra A1a:  A1 with newline before special characters
    """

    # Arrange
    source_markdown = """a![foo][ba
&beta;r]a
---

[ba
&beta;r]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:foo:::ba\n&beta;r:foo:::::]",
        "[text(2,9):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::ba &beta;r:ba\n&beta;r: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="foo" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_a2():
    """
    Test case extra A2:  SetExt heading with full image with x in url link
    """

    # Arrange
    source_markdown = """a![fo
o](</my url>)a
---"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/my%20url::fo\no:/my url:::fo\no:True::::]",
        "[text(2,14):a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>a<img src="/my%20url" alt="fo\no" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_a3():
    """
    Test case extra A3:  SetExt with inline link label text split over 2 lines
    """

    # Arrange
    source_markdown = """abc
[li
nk](/uri "title" )
 def
---"""
    expected_tokens = [
        "[setext(5,1):-:3::(1,1)]",
        "[text(1,1):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::li\nnk:False:":: : ]',
        "[text(2,2):li\nnk::\n]",
        "[end-link::]",
        "[text(3,19):\ndef::\n \x02]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>abc\n<a href="/uri" title="title">li\nnk</a>\ndef</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_a4():
    """
    Test case extra A4:  SetText with inline link label code span split over 2 lines
    """

    # Arrange
    source_markdown = """abc
[li`de
fg`nk](/uri "title" )
 def
---"""
    expected_tokens = [
        "[setext(5,1):-:3::(1,1)]",
        "[text(1,1):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::li`de\nfg`nk:False:":: : ]',
        "[text(2,2):li:]",
        "[icode-span(2,4):de\a\n\a \afg:`::]",
        "[text(3,4):nk:]",
        "[end-link::]",
        "[text(3,22):\ndef::\n \x02]",
        "[end-setext::]",
    ]
    expected_gfm = (
        """<h2>abc\n<a href="/uri" title="title">li<code>de fg</code>nk</a>\ndef</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_a5():
    """
    Test case extra A5:  SetExt with inline link label raw html split over 2 lines
    """

    # Arrange
    source_markdown = """abc
[li<de
fg>nk](/uri "title" )
 def
---"""
    expected_tokens = [
        "[setext(5,1):-:3::(1,1)]",
        "[text(1,1):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::li<de\nfg>nk:False:":: : ]',
        "[text(2,2):li:]",
        "[raw-html(2,4):de\nfg]",
        "[text(3,4):nk:]",
        "[end-link::]",
        "[text(3,22):\ndef::\n \x02]",
        "[end-setext::]",
    ]
    expected_gfm = (
        """<h2>abc\n<a href="/uri" title="title">li<de\nfg>nk</a>\ndef</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_a6():
    """
    Test case extra A6:  SetExt with inline link label text split over 2 lines
    """

    # Arrange
    source_markdown = """a[li
nk][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:li\nnk:::::]",
        "[text(1,3):li\nnk::\n]",
        "[end-link::]",
        "[text(2,9):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">li\nnk</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_a7():
    """
    Test case extra A7:  SetExt with full link label code span split over 2 lines
    """

    # Arrange
    source_markdown = """a[li`de
fg`nk][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:li`de\nfg`nk:::::]",
        "[text(1,3):li:]",
        "[icode-span(1,5):de\a\n\a \afg:`::]",
        "[text(2,4):nk:]",
        "[end-link::]",
        "[text(2,12):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = (
        """<h2>a<a href="/url" title="title">li<code>de fg</code>nk</a>a</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_a8():
    """
    Test case extra A8:  SetExt with full link label raw html split over 2 lines
    """

    # Arrange
    source_markdown = """a[li<de
fg>nk][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:li<de\nfg>nk:::::]",
        "[text(1,3):li:]",
        "[raw-html(1,5):de\nfg]",
        "[text(2,4):nk:]",
        "[end-link::]",
        "[text(2,12):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">li<de\nfg>nk</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_a9():
    """
    Test case extra A9:  SetExt with collapsed link label text split over 2 lines
    """

    # Arrange
    source_markdown = """a[li
nk][]a
---

[li\nnk]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::li\nnk:::::]",
        "[text(1,3):li\nnk::\n]",
        "[end-link::]",
        "[text(2,6):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::li nk:li\nnk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">li\nnk</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_b0():
    """
    Test case extra b0:  SetExt with collapsed link label code span split over 2 lines
    """

    # Arrange
    source_markdown = """a[li`de
fg`nk][]a
---

[li`de\nfg`nk]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::li`de\nfg`nk:::::]",
        "[text(1,3):li:]",
        "[icode-span(1,5):de\a\n\a \afg:`::]",
        "[text(2,4):nk:]",
        "[end-link::]",
        "[text(2,9):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::li`de fg`nk:li`de\nfg`nk: :/url:: :title:'title':]",
    ]
    expected_gfm = (
        """<h2>a<a href="/url" title="title">li<code>de fg</code>nk</a>a</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_b1():
    """
    Test case extra b1:  SetExt with collapsed link label raw html split over 2 lines
    """

    # Arrange
    source_markdown = """a[li<de
fg>nk][]a
---

[li<de\nfg>nk]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::li<de\nfg>nk:::::]",
        "[text(1,3):li:]",
        "[raw-html(1,5):de\nfg]",
        "[text(2,4):nk:]",
        "[end-link::]",
        "[text(2,9):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::li<de fg>nk:li<de\nfg>nk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">li<de\nfg>nk</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_b2():
    """
    Test case extra b2:  SetExt with shortcut link label text split over 2 lines
    """

    # Arrange
    source_markdown = """a[li
nk]a
---

[li\nnk]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::li\nnk:::::]",
        "[text(1,3):li\nnk::\n]",
        "[end-link::]",
        "[text(2,4):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::li nk:li\nnk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">li\nnk</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_b3():
    """
    Test case extra b3:  Paragraph with shortcut link label code span split over 2 lines
    """

    # Arrange
    source_markdown = """a[li`de
fg`nk]a
---

[li`de\nfg`nk]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::li`de\nfg`nk:::::]",
        "[text(1,3):li:]",
        "[icode-span(1,5):de\a\n\a \afg:`::]",
        "[text(2,4):nk:]",
        "[end-link::]",
        "[text(2,7):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::li`de fg`nk:li`de\nfg`nk: :/url:: :title:'title':]",
    ]
    expected_gfm = (
        """<h2>a<a href="/url" title="title">li<code>de fg</code>nk</a>a</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_b4():
    """
    Test case extra b4:  SetExt with shortcut link label raw html split over 2 lines
    """

    # Arrange
    source_markdown = """a[li<de
fg>nk]a
---

[li<de\nfg>nk]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::li<de\nfg>nk:::::]",
        "[text(1,3):li:]",
        "[raw-html(1,5):de\nfg]",
        "[text(2,4):nk:]",
        "[end-link::]",
        "[text(2,7):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::li<de fg>nk:li<de\nfg>nk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<a href="/url" title="title">li<de\nfg>nk</a>a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_b5():
    """
    Test case extra b5:  SetExt with inline image label text split over 2 lines
    """

    # Arrange
    source_markdown = """abc
![li
nk](/uri "title" )
 def
---"""
    expected_tokens = [
        "[setext(5,1):-:3::(1,1)]",
        "[text(1,1):abc\n::\n]",
        '[image(2,1):inline:/uri:title:li\nnk::::li\nnk:False:":: : ]',
        "[text(3,19):\ndef::\n \x02]",
        "[end-setext::]",
    ]
    expected_gfm = (
        """<h2>abc\n<img src="/uri" alt="li\nnk" title="title" />\ndef</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_b6():
    """
    Test case extra b6:  SetExt with inline image label code span split over 2 lines
    """

    # Arrange
    source_markdown = """abc
![li`de
fg`nk](/uri "title" )
 def
---"""
    expected_tokens = [
        "[setext(5,1):-:3::(1,1)]",
        "[text(1,1):abc\n::\n]",
        '[image(2,1):inline:/uri:title:lide fgnk::::li`de\nfg`nk:False:":: : ]',
        "[text(3,22):\ndef::\n \x02]",
        "[end-setext::]",
    ]
    expected_gfm = (
        """<h2>abc\n<img src="/uri" alt="lide fgnk" title="title" />\ndef</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_b7():
    """
    Test case extra b7:  SetExt with inline image label raw html split over 2 lines
    """

    # Arrange
    source_markdown = """abc
![li<de
fg>nk](/uri "title" )
 def
---"""
    expected_tokens = [
        "[setext(5,1):-:3::(1,1)]",
        "[text(1,1):abc\n::\n]",
        '[image(2,1):inline:/uri:title:li<de\nfg>nk::::li<de\nfg>nk:False:":: : ]',
        "[text(3,22):\ndef::\n \x02]",
        "[end-setext::]",
    ]
    expected_gfm = (
        """<h2>abc\n<img src="/uri" alt="li<de\nfg>nk" title="title" />\ndef</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_b8():
    """
    Test case extra b8:  SetExt with inline image label text split over 2 lines
    """

    # Arrange
    source_markdown = """a![li
nk][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:li\nnk:::bar:li\nnk:::::]",
        "[text(2,9):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="li\nnk" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_b9():
    """
    Test case extra b9:  SetExt with full image label code span split over 2 lines
    """

    # Arrange
    source_markdown = """a![li`de
fg`nk][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:lide fgnk:::bar:li`de\nfg`nk:::::]",
        "[text(2,12):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="lide fgnk" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_c0():
    """
    Test case extra c0:  SetExt with full image label raw html split over 2 lines
    """

    # Arrange
    source_markdown = """a![li<de
fg>nk][bar]a
---

[bar]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:li<de\nfg>nk:::bar:li<de\nfg>nk:::::]",
        "[text(2,12):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="li<de\nfg>nk" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_c1():
    """
    Test case extra c1:  SetExt with collapsed image label text split over 2 lines
    """

    # Arrange
    source_markdown = """a![li
nk][]a
---

[li\nnk]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:li\nnk::::li\nnk:::::]",
        "[text(2,6):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::li nk:li\nnk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="li\nnk" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_c2():
    """
    Test case extra c2:  SetExt with collapsed image label code span split over 2 lines
    """

    # Arrange
    source_markdown = """a![li`de
fg`nk][]a
---

[li`de\nfg`nk]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:lide fgnk::::li`de\nfg`nk:::::]",
        "[text(2,9):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::li`de fg`nk:li`de\nfg`nk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="lide fgnk" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_c3():
    """
    Test case extra c3:  SetExt with collapsed image label raw html split over 2 lines
    """

    # Arrange
    source_markdown = """a![li<de
fg>nk][]a
---

[li<de\nfg>nk]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:li<de\nfg>nk::::li<de\nfg>nk:::::]",
        "[text(2,9):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::li<de fg>nk:li<de\nfg>nk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="li<de\nfg>nk" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_c4():
    """
    Test case extra c4:  SetExt with shortcut image label text split over 2 lines
    """

    # Arrange
    source_markdown = """a![li
nk]a
---

[li\nnk]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:li\nnk::::li\nnk:::::]",
        "[text(2,4):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::li nk:li\nnk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="li\nnk" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_c5():
    """
    Test case extra c5:  SetExt with shortcut image label code span split over 2 lines
    """

    # Arrange
    source_markdown = """a![li`de
fg`nk]a
---

[li`de\nfg`nk]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:lide fgnk::::li`de\nfg`nk:::::]",
        "[text(2,7):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::li`de fg`nk:li`de\nfg`nk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="lide fgnk" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_c6():
    """
    Test case extra c6:  SetExt with shortcut image label raw html split over 2 lines
    """

    # Arrange
    source_markdown = """a![li<de
fg>nk]a
---

[li<de\nfg>nk]: /url 'title'"""
    expected_tokens = [
        "[setext(3,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:li<de\nfg>nk::::li<de\nfg>nk:::::]",
        "[text(2,7):a:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::li<de fg>nk:li<de\nfg>nk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="li<de\nfg>nk" title="title" />a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_setext_headings_extra_c7():
    """
    Test case extra c7:  SetExt with link split over 2 lines followed by text split over 2 lines
    """

    # Arrange
    source_markdown = """a[li<de
fg>nk](/url)a
b
---
"""
    expected_tokens = [
        "[setext(4,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/url:::::li<de\nfg>nk:False::::]",
        "[text(1,3):li:]",
        "[raw-html(1,5):de\nfg]",
        "[text(2,4):nk:]",
        "[end-link::]",
        "[text(2,13):a\nb::\n]",
        "[end-setext::]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<h2>a<a href="/url">li<de\nfg>nk</a>a\nb</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_c8():
    """
    Test case extra c8:  SetExt with image split over 2 lines followed by text split over 2 lines
    """

    # Arrange
    source_markdown = """a![li<de
fg>nk](/url)a
b
---
"""
    expected_tokens = [
        "[setext(4,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/url::li<de\nfg>nk::::li<de\nfg>nk:False::::]",
        "[text(2,13):a\nb::\n]",
        "[end-setext::]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="li<de\nfg>nk" />a\nb</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_c9():
    """
    Test case extra c9:  SetExt with link split over 2 lines followed by code span split over 2 lines
    """

    # Arrange
    source_markdown = """a[li<de
fg>nk](/url)`a
b`
---
"""
    expected_tokens = [
        "[setext(4,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/url:::::li<de\nfg>nk:False::::]",
        "[text(1,3):li:]",
        "[raw-html(1,5):de\nfg]",
        "[text(2,4):nk:]",
        "[end-link::]",
        "[icode-span(2,13):a\a\n\a \ab:`::]",
        "[end-setext::]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<h2>a<a href="/url">li<de\nfg>nk</a><code>a b</code></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_d0():
    """
    Test case extra d0:  SetExt with image split over 2 lines followed by code span split over 2 lines
    """

    # Arrange
    source_markdown = """a![li<de
fg>nk](/url)`a
b`
---
"""
    expected_tokens = [
        "[setext(4,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/url::li<de\nfg>nk::::li<de\nfg>nk:False::::]",
        "[icode-span(2,13):a\a\n\a \ab:`::]",
        "[end-setext::]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="li<de\nfg>nk" /><code>a b</code></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_d1():
    """
    Test case extra d1:  SetExt with image split over 2 lines followed by raw html split over 2 lines
    """

    # Arrange
    source_markdown = """a[li<de
fg>nk](/url)<a
b>
---
"""
    expected_tokens = [
        "[setext(4,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/url:::::li<de\nfg>nk:False::::]",
        "[text(1,3):li:]",
        "[raw-html(1,5):de\nfg]",
        "[text(2,4):nk:]",
        "[end-link::]",
        "[raw-html(2,13):a\nb]",
        "[end-setext::]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<h2>a<a href="/url">li<de\nfg>nk</a><a\nb></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_d2():
    """
    Test case extra d2:  SetExt with image split over 2 lines followed by raw html split over 2 lines
    """

    # Arrange
    source_markdown = """a![li<de
fg>nk](/url)<a
b>
---
"""
    expected_tokens = [
        "[setext(4,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/url::li<de\nfg>nk::::li<de\nfg>nk:False::::]",
        "[raw-html(2,13):a\nb]",
        "[end-setext::]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="li<de\nfg>nk" /><a\nb></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_d3():
    """
    Test case extra d3:  SetExt with link split over 2 lines followed by emphasis split over 2 lines
    """

    # Arrange
    source_markdown = """a[li<de
fg>nk](/url)*a
b*
---
"""
    expected_tokens = [
        "[setext(4,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[link(1,2):inline:/url:::::li<de\nfg>nk:False::::]",
        "[text(1,3):li:]",
        "[raw-html(1,5):de\nfg]",
        "[text(2,4):nk:]",
        "[end-link::]",
        "[emphasis(2,13):1:*]",
        "[text(2,14):a\nb::\n]",
        "[end-emphasis(3,2)::]",
        "[end-setext::]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<h2>a<a href="/url">li<de\nfg>nk</a><em>a\nb</em></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_d4():
    """
    Test case extra d4:  SetExt with image split over 2 lines followed by emphasis split over 2 lines
    """

    # Arrange
    source_markdown = """a![li<de
fg>nk](/url)*a
b*
---
"""
    expected_tokens = [
        "[setext(4,1):-:3::(1,1)]",
        "[text(1,1):a:]",
        "[image(1,2):inline:/url::li<de\nfg>nk::::li<de\nfg>nk:False::::]",
        "[emphasis(2,13):1:*]",
        "[text(2,14):a\nb::\n]",
        "[end-emphasis(3,2)::]",
        "[end-setext::]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<h2>a<img src="/url" alt="li<de\nfg>nk" /><em>a\nb</em></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_d5():
    """
    Test case extra d5:  SetExt with link split at the whitespaces
    """

    # Arrange
    source_markdown = """abc
[link](
 /uri
  "title"
   )
  def
---"""
    expected_tokens = [
        "[setext(7,1):-:3::(1,1)]",
        "[text(1,1):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::link:False:":\n :\n  :\n   ]',
        "[text(2,2):link:]",
        "[end-link::]",
        "[text(5,5):\ndef::\n  \x02]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>abc\n<a href="/uri" title="title">link</a>\ndef</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_d6():
    """
    Test case extra d6:  SetExt with image split at the whitespaces
    """

    # Arrange
    source_markdown = """abc
![link](
 /uri
  "title"
   )
  def
---"""
    expected_tokens = [
        "[setext(7,1):-:3::(1,1)]",
        "[text(1,1):abc\n::\n]",
        '[image(2,1):inline:/uri:title:link::::link:False:":\n :\n  :\n   ]',
        "[text(5,5):\ndef::\n  \x02]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>abc\n<img src="/uri" alt="link" title="title" />\ndef</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_d7():
    """
    Test case extra d7:  SetExt with link surrounded by emphasis
    """

    # Arrange
    source_markdown = """abc
*[link](/uri "title")*
def
---"""
    expected_tokens = [
        "[setext(4,1):-:3::(1,1)]",
        "[text(1,1):abc\n::\n]",
        "[emphasis(2,1):1:*]",
        '[link(2,2):inline:/uri:title::::link:False:":: :]',
        "[text(2,3):link:]",
        "[end-link::]",
        "[end-emphasis(2,22)::]",
        "[text(2,23):\ndef::\n]",
        "[end-setext::]",
    ]
    expected_gfm = (
        """<h2>abc\n<em><a href="/uri" title="title">link</a></em>\ndef</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_d8():
    """
    Test case extra d8:  SetExt with image surrounded by emphasis
    """

    # Arrange
    source_markdown = """abc
*![link](/uri "title")*
def
---"""
    expected_tokens = [
        "[setext(4,1):-:3::(1,1)]",
        "[text(1,1):abc\n::\n]",
        "[emphasis(2,1):1:*]",
        '[image(2,2):inline:/uri:title:link::::link:False:":: :]',
        "[end-emphasis(2,23)::]",
        "[text(2,24):\ndef::\n]",
        "[end-setext::]",
    ]
    expected_gfm = (
        """<h2>abc\n<em><img src="/uri" alt="link" title="title" /></em>\ndef</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_d9():
    """
    Test case extra d9:  SetExt with emphasis inside of link label
    """

    # Arrange
    source_markdown = """abc
[*link*](/uri "title")
def
---"""
    expected_tokens = [
        "[setext(4,1):-:3::(1,1)]",
        "[text(1,1):abc\n::\n]",
        '[link(2,1):inline:/uri:title::::*link*:False:":: :]',
        "[emphasis(2,2):1:*]",
        "[text(2,3):link:]",
        "[end-emphasis(2,7)::]",
        "[end-link::]",
        "[text(2,23):\ndef::\n]",
        "[end-setext::]",
    ]
    expected_gfm = (
        """<h2>abc\n<a href="/uri" title="title"><em>link</em></a>\ndef</h2>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_e0():
    """
    Test case extra e0:  SetExt with emphasis inside of image label
    """

    # Arrange
    source_markdown = """abc
![*link*](/uri "title")
def
---"""
    expected_tokens = [
        "[setext(4,1):-:3::(1,1)]",
        "[text(1,1):abc\n::\n]",
        '[image(2,1):inline:/uri:title:link::::*link*:False:":: :]',
        "[text(2,24):\ndef::\n]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>abc\n<img src="/uri" alt="link" title="title" />\ndef</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
