"""
https://github.github.com/gfm/#paragraph
"""
import pytest

from .utils import (
    act_and_assert
)


@pytest.mark.gfm
def test_paragraph_series_c_b():
    """
    Test case:  Paragraphs ends with a backslash escape
    was:        test_paragraph_extra_21
    """

    # Arrange
    source_markdown = """a fun day\\\\"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a fun day\\\b\\:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a fun day\\</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_c_bh():
    """
    Test case:  Paragraph ends with a backslash as in a hard line break
    was:        test_paragraph_extra_22
    """

    # Arrange
    source_markdown = """this was \\
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this was \\:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = """<p>this was \\</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_c_sh():
    """
    Test case:  Paragraph ends with 2+ spaces as in a hard line break
    was:        test_paragraph_extra_23
    """

    # Arrange
    source_markdown = """no line break?\a\a\a
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1)::   ]",
        "[text(1,1):no line break?:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = """<p>no line break?</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_c_cs():
    """
    Test case:  Paragraph string ending with a code span.
    was:        test_paragraph_extra_24
    """

    # Arrange
    source_markdown = """a fun ``day``"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a fun :]",
        "[icode-span(1,7):day:``::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a fun <code>day</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_c_cr():
    """
    Test case:  Paragraph string ending with a character reference.
    was:        test_paragraph_extra_25
    """

    # Arrange
    source_markdown = """played on &amp;"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):played on \a&amp;\a\a&\a&amp;\a\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>played on &amp;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_c_rh():
    """
    Test case:  Paragraph string ending with a raw html block.
    was:        test_paragraph_extra_26
    """

    # Arrange
    source_markdown = """really, <there it='is'>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):really, :]",
        "[raw-html(1,9):there it='is']",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>really, <there it='is'></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_c_ua():
    """
    Test case:  Paragraph string ending with an URI autolink
    was:        test_paragraph_extra_27
    """

    # Arrange
    source_markdown = """at <http://www.google.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):at :]",
        "[uri-autolink(1,4):http://www.google.com]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>at <a href="http://www.google.com">http://www.google.com</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_c_ea():
    """
    Test case:  Paragraph string ending with an email autolink
    was:        test_paragraph_extra_28
    """

    # Arrange
    source_markdown = """contact <foo@bar.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):contact :]",
        "[email-autolink(1,9):foo@bar.com]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>contact <a href="mailto:foo@bar.com">foo@bar.com</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_c_e():
    """
    Test case:  Paragraph string ending with an emphasis
    was:        test_paragraph_extra_29
    """

    # Arrange
    source_markdown = """it's *me*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):it's :]",
        "[emphasis(1,6):1:*]",
        "[text(1,7):me:]",
        "[end-emphasis(1,9)::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>it's <em>me</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_c_l():
    """
    Test case:  Paragraph string ending with a link.
    was:        test_paragraph_extra_30
    """

    # Arrange
    source_markdown = """like [Foo](/uri "t")"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):like :]",
        '[link(1,6):inline:/uri:t::::Foo:False:":: :]',
        "[text(1,7):Foo:]",
        "[end-link:::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>like <a href="/uri" title="t">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_c_i():
    """
    Test case:  Paragraph string ending with an image
    was:        test_paragraph_extra_31
    """

    # Arrange
    source_markdown = """an ![foo](/url "t")"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):an :]",
        '[image(1,4):inline:/url:t:foo::::foo:False:":: :]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an <img src="/url" alt="foo" title="t" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
