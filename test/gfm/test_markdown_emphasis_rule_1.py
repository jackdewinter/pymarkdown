"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_emphasis_360():
    """
    Test case 360:  Rule 1:
    """

    # Arrange
    source_markdown = """*foo bar*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo bar:]",
        "[end-emphasis(1,9)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo bar</em></p>"""

    # Act & Assert
    #
    # NOTE: The `show_debug` is present to allow for extra coverage of the emphasis_helper module.
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_emphasis_361():
    """
    Test case 361:  This is not emphasis, because the opening * is followed by whitespace,
                    and hence not part of a left-flanking delimiter run:
    """

    # Arrange
    source_markdown = """a * foo bar*"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):a * foo bar*:]", "[end-para:::True]"]
    expected_gfm = """<p>a * foo bar*</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_362():
    """
    Test case 362:  This is not emphasis, because the opening * is preceded by an
                    alphanumeric and followed by punctuation, and hence not part of
                    a left-flanking delimiter run:
    """

    # Arrange
    source_markdown = """a*"foo"*"""
    expected_tokens = [
        "[para(1,1):]",
        '[text(1,1):a*\a"\a&quot;\afoo\a"\a&quot;\a*:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a*&quot;foo&quot;*</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_363():
    """
    Test case 363:  Unicode nonbreaking spaces count as whitespace, too:
    """

    # Arrange
    source_markdown = """*\u00A0a\u00A0*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*\u00A0a\u00A0*:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*\u00A0a\u00A0*</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_364():
    """
    Test case 364:  (part 1) Intraword emphasis with * is permitted:
    """

    # Arrange
    source_markdown = """foo*bar*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo:]",
        "[emphasis(1,4):1:*]",
        "[text(1,5):bar:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<em>bar</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_365():
    """
    Test case 365:  (part 2) Intraword emphasis with * is permitted:
    """

    # Arrange
    source_markdown = """5*6*78"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):5:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):6:]",
        "[end-emphasis(1,4)::]",
        "[text(1,5):78:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>5<em>6</em>78</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
