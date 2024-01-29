"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_emphasis_445():
    """
    Test case 445:  (part 1) Rule 11
    """

    # Arrange
    source_markdown = """foo ***"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo :]",
        "[text(1,5):***:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo ***</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_446():
    """
    Test case 446:  (part 2) Rule 11
    """

    # Arrange
    source_markdown = """foo *\\**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo :]",
        "[emphasis(1,5):1:*]",
        "[text(1,6):\\\b*:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <em>*</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_447():
    """
    Test case 447:  (part 3) Rule 11
    """

    # Arrange
    source_markdown = """foo *_*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo :]",
        "[emphasis(1,5):1:*]",
        "[text(1,6):_:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <em>_</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_448():
    """
    Test case 448:  (part 4) Rule 11
    """

    # Arrange
    source_markdown = """foo *****"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo :]",
        "[text(1,5):*****:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo *****</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_449():
    """
    Test case 449:  (part 5) Rule 11
    """

    # Arrange
    source_markdown = """foo **\\***"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo :]",
        "[emphasis(1,5):2:*]",
        "[text(1,7):\\\b*:]",
        "[end-emphasis(1,9)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <strong>*</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_450():
    """
    Test case 450:  (part 6) Rule 11
    """

    # Arrange
    source_markdown = """foo **_**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo :]",
        "[emphasis(1,5):2:*]",
        "[text(1,7):_:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo <strong>_</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_451():
    """
    Test case 451:  (part 1) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    source_markdown = """**foo*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*:]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):foo:]",
        "[end-emphasis(1,6)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*<em>foo</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_452():
    """
    Test case 452:  (part 2) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    source_markdown = """*foo**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo:]",
        "[end-emphasis(1,5)::]",
        "[text(1,6):*:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo</em>*</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_453():
    """
    Test case 453:  (part 3) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    source_markdown = """***foo**"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*:]",
        "[emphasis(1,2):2:*]",
        "[text(1,4):foo:]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*<strong>foo</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_454():
    """
    Test case 454:  (part 4) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    source_markdown = """****foo*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):***:]",
        "[emphasis(1,4):1:*]",
        "[text(1,5):foo:]",
        "[end-emphasis(1,8)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>***<em>foo</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_455():
    """
    Test case 455:  (part 5) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    source_markdown = """**foo***"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):foo:]",
        "[end-emphasis(1,6)::]",
        "[text(1,8):*:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo</strong>*</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_456():
    """
    Test case 456:  (part 6) Note that when delimiters do not match evenly, Rule 11 determines that the excess literal * characters will appear outside of the emphasis, rather than inside it:
    """

    # Arrange
    source_markdown = """*foo****"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo:]",
        "[end-emphasis(1,5)::]",
        "[text(1,6):***:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo</em>***</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
