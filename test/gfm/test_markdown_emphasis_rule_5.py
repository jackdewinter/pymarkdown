"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_emphasis_387():
    """
    Test case 387:  Rule 5:
    """

    # Arrange
    source_markdown = """**foo bar**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):foo bar:]",
        "[end-emphasis(1,10)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo bar</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_388():
    """
    Test case 388:  This is not strong emphasis, because the opening delimiter is followed by whitespace:
    """

    # Arrange
    source_markdown = """** foo bar**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):**:]",
        "[text(1,3): foo bar:]",
        "[text(1,11):**:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>** foo bar**</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_389():
    """
    Test case 389:  This is not strong emphasis, because the opening ** is preceded by an alphanumeric and followed by punctuation, and hence not part of a left-flanking delimiter run:
    """

    # Arrange
    source_markdown = """a**"foo"**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):**:]",
        '[text(1,4):\a"\a&quot;\afoo\a"\a&quot;\a:]',
        "[text(1,9):**:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a**&quot;foo&quot;**</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_390():
    """
    Test case 390:  Intraword strong emphasis with ** is permitted:
    """

    # Arrange
    source_markdown = """foo**bar**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo:]",
        "[emphasis(1,4):2:*]",
        "[text(1,6):bar:]",
        "[end-emphasis(1,9)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<strong>bar</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
