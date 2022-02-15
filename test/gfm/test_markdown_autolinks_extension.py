"""
https://github.github.com/gfm/#autolinks-extension-
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.skip
def test_autolinks_621():
    """
    Test case 621:  The scheme http will be inserted automatically:
    """

    # Arrange
    source_markdown = """www.commonmark.org"""
    expected_tokens = ["[para:]", "[uri-autolink:http://foo.bar.baz]", "[end-para]"]
    expected_gfm = """
"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
def test_autolinks_622():
    """
    Test case 622:  After a valid domain, zero or more non-space non-< characters may follow
    """

    # Arrange
    source_markdown = """Visit www.commonmark.org/help for more information."""
    expected_tokens = ["[para:]", "[uri-autolink:http://foo.bar.baz]", "[end-para]"]
    expected_gfm = """
"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
def test_autolinks_623():
    """
    Test case 623:  Trailing punctuation (specifically, ?, !, ., ,, :, *, _, and ~) will not be considered part of the autolink, though they may be included in the interior of the link:
    """

    # Arrange
    source_markdown = """Visit www.commonmark.org.

Visit www.commonmark.org/a.b."""
    expected_tokens = ["[para:]", "[uri-autolink:http://foo.bar.baz]", "[end-para]"]
    expected_gfm = """
"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
def test_autolinks_624():
    """
    Test case 624:  When an autolink ends in ), we scan the entire autolink for the total number of parentheses. If there is a greater number of closing parentheses than opening ones, we don’t consider the unmatched trailing parentheses part of the autolink, in order to facilitate including an autolink inside a parenthesis:
    """

    # Arrange
    source_markdown = """www.google.com/search?q=Markup+(business)

www.google.com/search?q=Markup+(business)))

(www.google.com/search?q=Markup+(business))

(www.google.com/search?q=Markup+(business)"""
    expected_tokens = ["[para:]", "[uri-autolink:http://foo.bar.baz]", "[end-para]"]
    expected_gfm = """
"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
def test_autolinks_625():
    """
    Test case 625:  This check is only done when the link ends in a closing parentheses ), so if the only parentheses are in the interior of the autolink, no special rules are applied:
    """

    # Arrange
    source_markdown = """www.google.com/search?q=(business))+ok"""
    expected_tokens = ["[para:]", "[uri-autolink:http://foo.bar.baz]", "[end-para]"]
    expected_gfm = """
"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
def test_autolinks_626():
    """
    Test case 626:  If an autolink ends in a semicolon (;), we check to see if it appears to resemble an entity reference; if the preceding text is & followed by one or more alphanumeric characters. If so, it is excluded from the autolink:
    """

    # Arrange
    source_markdown = """www.google.com/search?q=commonmark&hl=en

www.google.com/search?q=commonmark&hl;"""
    expected_tokens = ["[para:]", "[uri-autolink:http://foo.bar.baz]", "[end-para]"]
    expected_gfm = """
"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
def test_autolinks_627():
    """
    Test case 627:  < immediately ends an autolink.
    """

    # Arrange
    source_markdown = """www.commonmark.org/he<lp"""
    expected_tokens = ["[para:]", "[uri-autolink:http://foo.bar.baz]", "[end-para]"]
    expected_gfm = """
"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
def test_autolinks_628():
    """
    Test case 628:  An extended url autolink will be recognised when one of the schemes http://, or https://, followed by a valid domain, then zero or more non-space non-< characters according to extended autolink path validation:
    """

    # Arrange
    source_markdown = """http://commonmark.org

(Visit https://encrypted.google.com/search?q=Markup+(business))"""
    expected_tokens = ["[para:]", "[uri-autolink:http://foo.bar.baz]", "[end-para]"]
    expected_gfm = """
"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
def test_autolinks_629():
    """
    Test case 629:  The scheme mailto: will automatically be added to the generated link:
    """

    # Arrange
    source_markdown = """foo@bar.baz"""
    expected_tokens = ["[para:]", "[uri-autolink:http://foo.bar.baz]", "[end-para]"]
    expected_gfm = """
"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
def test_autolinks_630():
    """
    Test case 630:  + can occur before the @, but not after.
    """

    # Arrange
    source_markdown = (
        """hello@mail+xyz.example isn't valid, but hello+xyz@mail.example is."""
    )
    expected_tokens = ["[para:]", "[uri-autolink:http://foo.bar.baz]", "[end-para]"]
    expected_gfm = """
"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
def test_autolinks_631():
    """
    Test case 631:  ., -, and _ can occur on both sides of the @, but only . may occur at the end of the email address, in which case it will not be considered part of the address:
    """

    # Arrange
    source_markdown = """a.b-c_d@a.b

a.b-c_d@a.b.

a.b-c_d@a.b-

a.b-c_d@a.b_"""
    expected_tokens = ["[para:]", "[uri-autolink:http://foo.bar.baz]", "[end-para]"]
    expected_gfm = """
"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
