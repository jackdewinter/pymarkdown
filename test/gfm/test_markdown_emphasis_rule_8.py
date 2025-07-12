"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_emphasis_406() -> None:
    """
    Test case 406:  Rule 8: This is not strong emphasis, because the closing delimiter is preceded by whitespace:
    """

    # Arrange
    source_markdown = """__foo bar __"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):__foo bar __:]", "[end-para:::True]"]
    expected_gfm = """<p>__foo bar __</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_407() -> None:
    """
    Test case 407:  This is not strong emphasis, because the second __ is preceded by punctuation and followed by an alphanumeric:
    """

    # Arrange
    source_markdown = """__(__foo)"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):__(__foo):]", "[end-para:::True]"]
    expected_gfm = """<p>__(__foo)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_408() -> None:
    """
    Test case 408:  The point of this restriction is more easily appreciated with this example:
    """

    # Arrange
    source_markdown = """_(__foo__)_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):(:]",
        "[emphasis(1,3):2:_]",
        "[text(1,5):foo:]",
        "[end-emphasis(1,8)::]",
        "[text(1,10):):]",
        "[end-emphasis(1,11)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>(<strong>foo</strong>)</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_409() -> None:
    """
    Test case 409:  (part 1) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    source_markdown = """__foo__bar"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):__foo__bar:]", "[end-para:::True]"]
    expected_gfm = """<p>__foo__bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_410() -> None:
    """
    Test case 410:  (part 2) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    source_markdown = """__пристаням__стремятся"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):__пристаням__стремятся:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>__пристаням__стремятся</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_411() -> None:
    """
    Test case 411:  (part 3) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    source_markdown = """__foo__bar__baz__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):foo__bar__baz:]",
        "[end-emphasis(1,16)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo__bar__baz</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_412() -> None:
    """
    Test case 412:  This is strong emphasis, even though the closing delimiter is both left- and right-flanking, because it is followed by punctuation:
    """

    # Arrange
    source_markdown = """__(bar)__."""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):(bar):]",
        "[end-emphasis(1,8)::]",
        "[text(1,10):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>(bar)</strong>.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
