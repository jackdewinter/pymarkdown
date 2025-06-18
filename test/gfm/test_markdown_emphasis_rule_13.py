"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_emphasis_469() -> None:
    """
    Test case 469:  (part 1) Rule 13 implies that if you want emphasis nested directly inside emphasis, you must use different delimiters:
    """

    # Arrange
    source_markdown = """**foo**"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[text(1,3):foo:]",
        "[end-emphasis(1,6)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_470() -> None:
    """
    Test case 470:  (part 2) Rule 13 implies that if you want emphasis nested directly inside emphasis, you must use different delimiters:
    """

    # Arrange
    source_markdown = """*_foo_*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[emphasis(1,2):1:_]",
        "[text(1,3):foo:]",
        "[end-emphasis(1,6)::]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em><em>foo</em></em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_471() -> None:
    """
    Test case 471:  (part 3) Rule 13 implies that if you want emphasis nested directly inside emphasis, you must use different delimiters:
    """

    # Arrange
    source_markdown = """__foo__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):foo:]",
        "[end-emphasis(1,6)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_472() -> None:
    """
    Test case 472:  (part 4) Rule 13 implies that if you want emphasis nested directly inside emphasis, you must use different delimiters:
    """

    # Arrange
    source_markdown = """_*foo*_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):foo:]",
        "[end-emphasis(1,6)::]",
        "[end-emphasis(1,7)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em><em>foo</em></em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_473() -> None:
    """
    Test case 473:  (part 1) However, strong emphasis within strong emphasis is possible without switching delimiters:
    """

    # Arrange
    source_markdown = """****foo****"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[emphasis(1,3):2:*]",
        "[text(1,5):foo:]",
        "[end-emphasis(1,8)::]",
        "[end-emphasis(1,10)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong><strong>foo</strong></strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_474() -> None:
    """
    Test case 474:  (part 2) However, strong emphasis within strong emphasis is possible without switching delimiters:
    """

    # Arrange
    source_markdown = """____foo____"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[emphasis(1,3):2:_]",
        "[text(1,5):foo:]",
        "[end-emphasis(1,8)::]",
        "[end-emphasis(1,10)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong><strong>foo</strong></strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_475() -> None:
    """
    Test case 475:  Rule 13 can be applied to arbitrarily long sequences of delimiters:
    """

    # Arrange
    source_markdown = """******foo******"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:*]",
        "[emphasis(1,3):2:*]",
        "[emphasis(1,5):2:*]",
        "[text(1,7):foo:]",
        "[end-emphasis(1,10)::]",
        "[end-emphasis(1,12)::]",
        "[end-emphasis(1,14)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong><strong><strong>foo</strong></strong></strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
