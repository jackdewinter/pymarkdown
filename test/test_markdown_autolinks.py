"""
https://github.github.com/gfm/#autolinks
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    act_and_assert
)


@pytest.mark.gfm
def test_autolinks_602():
    """
    Test case 602:  (part 1) Here are some valid autolinks:
    """

    # Arrange
    source_markdown = """<http://foo.bar.baz>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://foo.bar.baz]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://foo.bar.baz">http://foo.bar.baz</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_603():
    """
    Test case 603:  (part 2) Here are some valid autolinks:
    """

    # Arrange
    source_markdown = """<http://foo.bar.baz/test?q=hello&id=22&boolean>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://foo.bar.baz/test?q=hello&id=22&boolean]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://foo.bar.baz/test?q=hello&amp;id=22&amp;boolean">http://foo.bar.baz/test?q=hello&amp;id=22&amp;boolean</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_604():
    """
    Test case 604:  (part 3) Here are some valid autolinks:
    """

    # Arrange
    source_markdown = """<irc://foo.bar:2233/baz>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):irc://foo.bar:2233/baz]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="irc://foo.bar:2233/baz">irc://foo.bar:2233/baz</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_604a():
    """
    Test case 604a:  variations
    """

    # Arrange
    source_markdown = """<irc:foo.bar>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):irc:foo.bar]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="irc:foo.bar">irc:foo.bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_604b():
    """
    Test case 604b:  variations
    """

    # Arrange
    source_markdown = """<my+weird-custom.scheme1:foo.bar>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):my+weird-custom.scheme1:foo.bar]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="my+weird-custom.scheme1:foo.bar">my+weird-custom.scheme1:foo.bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_605():
    """
    Test case 605:  Uppercase is also fine
    """

    # Arrange
    source_markdown = """<MAILTO:FOO@BAR.BAZ>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):MAILTO:FOO@BAR.BAZ]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="MAILTO:FOO@BAR.BAZ">MAILTO:FOO@BAR.BAZ</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_606():
    """
    Test case 606:  (part 1) Note that many strings that count as absolute URIs for purposes of this spec are not valid URIs, because their schemes are not registered or because of other problems with their syntax:
    """

    # Arrange
    source_markdown = """<a+b+c:d>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):a+b+c:d]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="a+b+c:d">a+b+c:d</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_607():
    """
    Test case 607:  (part 2) Note that many strings that count as absolute URIs for purposes of this spec are not valid URIs, because their schemes are not registered or because of other problems with their syntax:
    """

    # Arrange
    source_markdown = """<made-up-scheme://foo,bar>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):made-up-scheme://foo,bar]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="made-up-scheme://foo,bar">made-up-scheme://foo,bar</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_608():
    """
    Test case 608:  (part 3) Note that many strings that count as absolute URIs for purposes of this spec are not valid URIs, because their schemes are not registered or because of other problems with their syntax:
    """

    # Arrange
    source_markdown = """<http://../>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://../]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://../">http://../</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_609():
    """
    Test case 609:  (part 4) Note that many strings that count as absolute URIs for purposes of this spec are not valid URIs, because their schemes are not registered or because of other problems with their syntax:
    """

    # Arrange
    source_markdown = """<localhost:5001/foo>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):localhost:5001/foo]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="localhost:5001/foo">localhost:5001/foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_610():
    """
    Test case 610:  Spaces are not allowed in autolinks:
    """

    # Arrange
    source_markdown = """<http://foo.bar/baz bim>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\ahttp://foo.bar/baz bim\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;http://foo.bar/baz bim&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_611():
    """
    Test case 611:  Backslash-escapes do not work inside autolinks:
    """

    # Arrange
    source_markdown = """<http://example.com/\\[\\>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://example.com/\\[\\]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="http://example.com/%5C%5B%5C">http://example.com/\\[\\</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_611a():
    """
    Test case 611a:  Backslash-escapes do not work inside autolinks:
    """

    # Arrange
    source_markdown = """<http://example.com/\u2122\u20AC>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://example.com/™€]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://example.com/%E2%84%A2%E2%82%AC">http://example.com/™€</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_611b():
    """
    Test case 611b:  Backslash-escapes do not work inside autolinks:
    """

    # Arrange
    source_markdown = """<http://abcdefjhijklmnopqrstuvwxyz!"#$%&'()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`{}|~ABC>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://abcdefjhijklmnopqrstuvwxyz!\"#$%&'()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`{}|~ABC]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://abcdefjhijklmnopqrstuvwxyz!%22#$%25&amp;'()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ%5B%5C%5D%5E_%60%7B%7D%7C~ABC">http://abcdefjhijklmnopqrstuvwxyz!&quot;#$%&amp;'()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`{}|~ABC</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_612():
    """
    Test case 612:  (part 1) Examples of email autolinks:
    """

    # Arrange
    source_markdown = """<foo@bar.example.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink(1,1):foo@bar.example.com]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="mailto:foo@bar.example.com">foo@bar.example.com</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_613():
    """
    Test case 613:  (part 2) Examples of email autolinks:
    """

    # Arrange
    source_markdown = """<foo+special@Bar.baz-bar0.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink(1,1):foo+special@Bar.baz-bar0.com]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="mailto:foo+special@Bar.baz-bar0.com">foo+special@Bar.baz-bar0.com</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_613a():
    """
    Test case 613a:  variations
    """

    # Arrange
    source_markdown = """<l@f>"""
    expected_tokens = ["[para(1,1):]", "[email-autolink(1,1):l@f]", "[end-para:::True]"]
    expected_gfm = """<p><a href="mailto:l@f">l@f</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_614():
    """
    Test case 614:  Backslash-escapes do not work inside email autolinks:
    """

    # Arrange
    source_markdown = """<foo\\+@bar.example.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\afoo\\\b+@bar.example.com\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;foo+@bar.example.com&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_615():
    """
    Test case 615:  (part 1) These are not autolinks:
    """

    # Arrange
    source_markdown = """<>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\a\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_616():
    """
    Test case 616:  (part 2) These are not autolinks:
    """

    # Arrange
    source_markdown = """< http://foo.bar >"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\a http://foo.bar \a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt; http://foo.bar &gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_617():
    """
    Test case 617:  (part 3) These are not autolinks:
    """

    # Arrange
    source_markdown = """<m:abc>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\am:abc\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;m:abc&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_618():
    """
    Test case 618:  (part 4) These are not autolinks:
    """

    # Arrange
    source_markdown = """<foo.bar.baz>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\afoo.bar.baz\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;foo.bar.baz&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_619():
    """
    Test case 619:  (part 5) These are not autolinks:
    """

    # Arrange
    source_markdown = """http://example.com"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):http://example.com:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>http://example.com</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_620():
    """
    Test case 620:  (part 6) These are not autolinks:
    """

    # Arrange
    source_markdown = """foo@bar.example.com"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo@bar.example.com:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo@bar.example.com</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_620a():
    """
    Test case 620a:  variation (not enough in scheme)
    """

    # Arrange
    source_markdown = """<f:foo.bar>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\af:foo.bar\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;f:foo.bar&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_620b():
    """
    Test case 620b:  variation (too much in scheme)
    """

    # Arrange
    source_markdown = """<f012345678901234567890123456789f0:foo.bar>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\af012345678901234567890123456789f0:foo.bar\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;f012345678901234567890123456789f0:foo.bar&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_620c():
    """
    Test case 620c:  variation (illegal char in scheme)
    """

    # Arrange
    source_markdown = """<my_scheme:foo.bar>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\amy:]",
        "[text(1,4):_:]",
        "[text(1,5):scheme:foo.bar\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;my_scheme:foo.bar&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_620d():
    """
    Test case 620d:  variation (no domain part)
    """

    # Arrange
    source_markdown = """<no_domain@>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\ano:]",
        "[text(1,4):_:]",
        "[text(1,5):domain@\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;no_domain@&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_autolinks_620e():
    """
    Test case 620e:  variation (no mailbox part)
    """

    # Arrange
    source_markdown = """<@no.mailbox>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\a@no.mailbox\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;@no.mailbox&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
