"""
https://github.github.com/gfm/#paragraph
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_paragraph_series_e_cs():
    """
    Test case:  Paragraph with code span with newline inside
    was:        test_paragraph_extra_43
    """

    # Arrange
    source_markdown = """a`code
span`a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[icode-span(1,2):code\a\n\a \aspan:`::]",
        "[text(2,6):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<code>code span</code>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_e_rh():
    """
    Test case:  Paragraph with raw HTML with newline inside
    was:        test_paragraph_extra_44
    """

    # Arrange
    source_markdown = """a<raw
html='cool'>a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[raw-html(1,2):raw\nhtml='cool']",
        "[text(2,13):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<raw\nhtml='cool'>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_e_ua():
    """
    Test case:  Paragraph with URI autolink with newline inside, renders invalid
    was:        test_paragraph_extra_45
    """

    # Arrange
    source_markdown = """a<http://www.\ngoogle.com>a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a\a<\a&lt;\ahttp://www.\ngoogle.com\a>\a&gt;\aa::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a&lt;http://www.\ngoogle.com&gt;a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_e_ea():
    """
    Test case:  Paragraph with email autolink with newline inside, renders invalid
    was:        test_paragraph_extra_46
    """

    # Arrange
    source_markdown = """a<foo@bar\n.com>a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a\a<\a&lt;\afoo@bar\n.com\a>\a&gt;\aa::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a&lt;foo@bar\n.com&gt;a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_e_em():
    """
    Test case:  Paragraph with emphasis with newline inside
    was:        test_paragraph_extra_46b
    """

    # Arrange
    source_markdown = """a*foo\nbar*a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):foo\nbar::\n]",
        "[end-emphasis(2,4)::]",
        "[text(2,5):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<em>foo\nbar</em>a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
