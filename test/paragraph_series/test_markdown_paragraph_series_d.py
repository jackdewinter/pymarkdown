"""
https://github.github.com/gfm/#paragraph
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_paragraph_series_d_b():
    """
    Test case:  Paragraph this is only a backslash escape
    was:        test_paragraph_extra_32
    """

    # Arrange
    source_markdown = """\\\\"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b\\:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\\</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_d_bh():
    """
    Test case:  Paragraph this is only a backslash as in a hard line break
    was:        test_paragraph_extra_33
    """

    # Arrange
    source_markdown = """ \\
"""
    expected_tokens = [
        "[para(1,2): ]",
        "[text(1,2):\\:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = """<p>\\</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_d_sh():
    """
    Test case:  Paragraph this is only 2+ spaces as in a hard line break
    was:        test_paragraph_extra_34
    """

    # Arrange
    source_markdown = """\a\a\a\a
""".replace(
        "\a", " "
    )
    expected_tokens = ["[BLANK(1,1):    ]", "[BLANK(2,1):]"]
    expected_gfm = """"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_d_cs():
    """
    Test case:  Paragraph this is only a code span.
    was:        test_paragraph_extra_35
    """

    # Arrange
    source_markdown = """``day``"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):day:``::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>day</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_d_cr():
    """
    Test case:  Paragraph this is only a character reference.
    was:        test_paragraph_extra_36
    """

    # Arrange
    source_markdown = """&amp;"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a&amp;\a\a&\a&amp;\a\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&amp;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_d_rh():
    """
    Test case:  Paragraph this is only a raw html block.
    was:        test_paragraph_extra_37
    """

    # Arrange
    source_markdown = """<there it='is'>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<there it='is'>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<there it='is'>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_d_ua():
    """
    Test case:  Paragraph this is only an URI autolink
    was:        test_paragraph_extra_38
    """

    # Arrange
    source_markdown = """<http://www.google.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://www.google.com]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="http://www.google.com">http://www.google.com</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_d_ea():
    """
    Test case:  Paragraph this is only an email autolink
    was:        test_paragraph_extra_39
    """

    # Arrange
    source_markdown = """<foo@bar.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink(1,1):foo@bar.com]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="mailto:foo@bar.com">foo@bar.com</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_d_e():
    """
    Test case:  Paragraph this is only an emphasis
    was:        test_paragraph_extra_40
    """

    # Arrange
    source_markdown = """*me*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):me:]",
        "[end-emphasis(1,4)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>me</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_d_l_nt():
    """
    Test case:  Paragraph this is only a link without a title
    was:        test_paragraph_extra_41
    """

    # Arrange
    source_markdown = """[Foo](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/uri:::::Foo:False::::]",
        "[text(1,2):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_d_i_nt():
    """
    Test case:  Paragraph this is only an image without a title
    was:        test_paragraph_extra_41a
    """

    # Arrange
    source_markdown = """![Foo](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:/uri::Foo::::Foo:False::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/uri" alt="Foo" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_d_i_t():
    """
    Test case:  Paragraph this is only an image
    was:        test_paragraph_extra_42
    """

    # Arrange
    source_markdown = """![foo](/url "title")"""
    expected_tokens = [
        "[para(1,1):]",
        '[image(1,1):inline:/url:title:foo::::foo:False:":: :]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_d_l_t():
    """
    Test case:  Paragraph this is only a link
    was:        test_paragraph_extra_42a
    """

    # Arrange
    source_markdown = """[foo](/url "title")"""
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/url:title::::foo:False:":: :]',
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
