"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_emphasis_374():
    """
    Test case 374:  Rule 3:  This is not emphasis, because the closing delimiter does not match the opening delimiter:
    """

    # Arrange
    source_markdown = """_foo*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):_:]",
        "[text(1,2):foo:]",
        "[text(1,5):*:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>_foo*</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_375():
    """
    Test case 375:  This is not emphasis, because the closing * is preceded by whitespace
    """

    # Arrange
    source_markdown = """*foo bar *"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*:]",
        "[text(1,2):foo bar :]",
        "[text(1,10):*:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*foo bar *</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_376():
    """
    Test case 376:  A newline also counts as whitespace:
    """

    # Arrange
    source_markdown = """*foo bar
*"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):*:]",
        "[text(1,2):foo bar\n::\n]",
        "[text(2,1):*:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*foo bar
*</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_377():
    """
    Test case 377:  This is not emphasis, because the second * is preceded by punctuation and followed by an alphanumeric (hence it is not part of a right-flanking delimiter run:
    """

    # Arrange
    source_markdown = """*(*foo)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*:]",
        "[text(1,2):(:]",
        "[text(1,3):*:]",
        "[text(1,4):foo):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*(*foo)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_378():
    """
    Test case 378:  The point of this restriction is more easily appreciated with this example:
    """

    # Arrange
    source_markdown = """*(*foo*)*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):(:]",
        "[emphasis(1,3):1:*]",
        "[text(1,4):foo:]",
        "[end-emphasis(1,7)::]",
        "[text(1,8):):]",
        "[end-emphasis(1,9)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>(<em>foo</em>)</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_379():
    """
    Test case 379:  Intraword emphasis with * is allowed:
    """

    # Arrange
    source_markdown = """*foo*bar"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo:]",
        "[end-emphasis(1,5)::]",
        "[text(1,6):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo</em>bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
