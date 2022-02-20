"""
https://github.github.com/gfm/#paragraph
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_paragraph_series_b_b():
    """
    Test case:  Paragraph containing a backslash
    was:        test_paragraph_extra_12
    """

    # Arrange
    source_markdown = """a \\\\fun\\\\ day"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \\\b\\fun\\\b\\ day:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a \\fun\\ day</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_b_cs():
    """
    Test case:  Paragraph containing a code span.
    was:        test_paragraph_extra_13
    """

    # Arrange
    source_markdown = """a ``fun`` day"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):fun:``::]",
        "[text(1,10): day:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>fun</code> day</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_b_cr():
    """
    Test case:  Paragraph containing a character reference.
    was:        test_paragraph_extra_14
    """

    # Arrange
    source_markdown = """fun &amp; joy"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):fun \a&amp;\a\a&\a&amp;\a\a joy:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>fun &amp; joy</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_b_rh():
    """
    Test case:  Paragraph containing a raw html block.
    was:        test_paragraph_extra_15
    """

    # Arrange
    source_markdown = """where <there it='is'> it"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):where :]",
        "[raw-html(1,7):there it='is']",
        "[text(1,22): it:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>where <there it='is'> it</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_b_ua():
    """
    Test case:  Paragraph containing an URI autolink
    was:        test_paragraph_extra_16
    """

    # Arrange
    source_markdown = """look <http://www.google.com> for"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):look :]",
        "[uri-autolink(1,6):http://www.google.com]",
        "[text(1,29): for:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>look <a href="http://www.google.com">http://www.google.com</a> for</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_b_ea():
    """
    Test case:  Paragraph containing an email autolink
    was:        test_paragraph_extra_17
    """

    # Arrange
    source_markdown = """email <foo@bar.com> for"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):email :]",
        "[email-autolink(1,7):foo@bar.com]",
        "[text(1,20): for:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>email <a href="mailto:foo@bar.com">foo@bar.com</a> for</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_b_e():
    """
    Test case:  Paragraph containing emphasis
    was:        test_paragraph_extra_18
    """

    # Arrange
    source_markdown = """really! *it's me!* here!"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):really! :]",
        "[emphasis(1,9):1:*]",
        "[text(1,10):it's me!:]",
        "[end-emphasis(1,18)::]",
        "[text(1,19): here!:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>really! <em>it's me!</em> here!</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_b_l():
    """
    Test case:  Paragraph containing a link.
    was:        test_paragraph_extra_19
    """

    # Arrange
    source_markdown = """at [Foo](/uri "t") more"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):at :]",
        '[link(1,4):inline:/uri:t::::Foo:False:":: :]',
        "[text(1,5):Foo:]",
        "[end-link::]",
        "[text(1,19): more:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>at <a href="/uri" title="t">Foo</a> more</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_b_i():
    """
    Test case:  Paragraph containing an image
    was:        test_paragraph_extra_20
    """

    # Arrange
    source_markdown = """my ![foo](/url "t") image"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):my :]",
        '[image(1,4):inline:/url:t:foo::::foo:False:":: :]',
        "[text(1,20): image:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>my <img src="/url" alt="foo" title="t" /> image</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
