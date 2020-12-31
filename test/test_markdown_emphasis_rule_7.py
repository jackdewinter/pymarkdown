"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from .utils import act_and_assert


@pytest.mark.gfm
def test_emphasis_400():
    """
    Test case 400:  Rule 7: This is not strong emphasis, because the closing delimiter is preceded by whitespace:
    """

    # Arrange
    source_markdown = """**foo bar **"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):**:]",
        "[text(1,3):foo bar :]",
        "[text(1,11):**:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>**foo bar **</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_401():
    """
    Test case 401:  This is not strong emphasis, because the second ** is preceded by punctuation and followed by an alphanumeric:
    """

    # Arrange
    source_markdown = """**(**foo)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):**:]",
        "[text(1,3):(:]",
        "[text(1,4):**:]",
        "[text(1,6):foo):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>**(**foo)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_402():
    """
    Test case 402:  (part 1) The point of this restriction is more easily appreciated with these examples
    """

    # Arrange
    source_markdown = """*(**foo**)*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):(:]",
        "[emphasis(1,3):2:*]",
        "[text(1,5):foo:]",
        "[end-emphasis(1,8)::2:*:False]",
        "[text(1,10):):]",
        "[end-emphasis(1,11)::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>(<strong>foo</strong>)</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_403():
    """
    Test case 403:  (part 2) The point of this restriction is more easily appreciated with these examples
    """

    # Arrange
    source_markdown = """**Gomphocarpus (*Gomphocarpus physocarpus*, syn.
*Asclepias physocarpa*)**"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):Gomphocarpus (:]",
        "[emphasis(1,17):1:*]",
        "[text(1,18):Gomphocarpus physocarpus:]",
        "[end-emphasis(1,42)::1:*:False]",
        "[text(1,43):, syn.\n::\n]",
        "[emphasis(2,1):1:*]",
        "[text(2,2):Asclepias physocarpa:]",
        "[end-emphasis(2,22)::1:*:False]",
        "[text(2,23):):]",
        "[end-emphasis(2,24)::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>Gomphocarpus (<em>Gomphocarpus physocarpus</em>, syn.
<em>Asclepias physocarpa</em>)</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_404():
    """
    Test case 404:  (part 3) The point of this restriction is more easily appreciated with these examples
    """

    # Arrange
    source_markdown = """**foo "*bar*" foo**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        '[text(1,3):foo \a"\a&quot;\a:]',
        "[emphasis(1,8):1:*]",
        "[text(1,9):bar:]",
        "[end-emphasis(1,12)::1:*:False]",
        '[text(1,13):\a"\a&quot;\a foo:]',
        "[end-emphasis(1,18)::2:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo &quot;<em>bar</em>&quot; foo</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_405():
    """
    Test case 405:  Intraword emphasis:
    """

    # Arrange
    source_markdown = """**foo**bar"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):foo:]",
        "[end-emphasis(1,6)::2:*:False]",
        "[text(1,8):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo</strong>bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
