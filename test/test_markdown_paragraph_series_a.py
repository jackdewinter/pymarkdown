"""
https://github.github.com/gfm/#paragraph
"""
import pytest

from .utils import act_and_assert


@pytest.mark.gfm
def test_paragraph_series_a_b():
    """
    Test case:  Paragraph starts with a backslash escape
    was:        test_paragraph_extra_01
    """

    # Arrange
    source_markdown = """\\\\this is a fun day"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b\\this is a fun day:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\\this is a fun day</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_a_bh():
    """
    Test case:  Paragraph starts with a backslash as in a hard line break
    was:        test_paragraph_extra_02
    """

    # Arrange
    source_markdown = """\\
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = """<p>\\</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_a_sh():
    """
    Test case:  Paragraph starts with spaces as in a hard line break
    was:        test_paragraph_extra_03
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
def test_paragraph_series_a_cs():
    """
    Test case:  Paragraph string starting with a code span.
    was:        test_paragraph_extra_04
    """

    # Arrange
    source_markdown = """`this` is a fun day"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):this:`::]",
        "[text(1,7): is a fun day:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>this</code> is a fun day</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_a_cr():
    """
    Test case:  Paragraph string starting with a character reference.
    was:        test_paragraph_extra_05
    """

    # Arrange
    source_markdown = """&amp; the band played on"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a&amp;\a\a&\a&amp;\a\a the band played on:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&amp; the band played on</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_a_rh():
    """
    Test case:  Paragraph string starting with a raw html block.
    was:        test_paragraph_extra_06
    """

    # Arrange
    source_markdown = """<there it='is'>, really"""
    expected_tokens = [
        "[para(1,1):]",
        "[raw-html(1,1):there it='is']",
        "[text(1,16):, really:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><there it='is'>, really</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_a_ua():
    """
    Test case:  Paragraph string starting with an URI autolink
    was:        test_paragraph_extra_07
    """

    # Arrange
    source_markdown = """<http://www.google.com> to look"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://www.google.com]",
        "[text(1,24): to look:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="http://www.google.com">http://www.google.com</a> to look</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_a_ea():
    """
    Test case:  Paragraph string starting with an email autolink
    was:        test_paragraph_extra_08
    """

    # Arrange
    source_markdown = """<foo@bar.com> for info"""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink(1,1):foo@bar.com]",
        "[text(1,14): for info:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="mailto:foo@bar.com">foo@bar.com</a> for info</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_a_e():
    """
    Test case:  Paragraph string starting with an emphasis
    was:        test_paragraph_extra_09
    """

    # Arrange
    source_markdown = """*it's* me!"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):it's:]",
        "[end-emphasis(1,6):::False]",
        "[text(1,7): me!:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>it's</em> me!</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_a_l():
    """
    Test case:  Paragraph string starting with a link
    was:        test_paragraph_extra_10
    """

    # Arrange
    source_markdown = """[Foo](/uri "t") is a link"""
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/uri:t::::Foo:False:":: :]',
        "[text(1,2):Foo:]",
        "[end-link:::False]",
        "[text(1,16): is a link:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri" title="t">Foo</a> is a link</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_a_i():
    """
    Test case:  Paragraph string starting with an image
    was:        test_paragraph_extra_11
    """

    # Arrange
    source_markdown = """![foo](/url "t") is an image"""
    expected_tokens = [
        "[para(1,1):]",
        '[image(1,1):inline:/url:t:foo::::foo:False:":: :]',
        "[text(1,17): is an image:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="t" /> is an image</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
