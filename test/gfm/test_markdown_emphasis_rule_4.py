"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_emphasis_380() -> None:
    """
    Test case 380:  Rule 4:  This is not emphasis, because the closing _ is preceded by whitespace:
    """

    # Arrange
    source_markdown = """_foo bar _"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):_foo bar _:]", "[end-para:::True]"]
    expected_gfm = """<p>_foo bar _</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_381() -> None:
    """
    Test case 381:  This is not emphasis, because the second _ is preceded by punctuation and followed by an alphanumeric:
    """

    # Arrange
    source_markdown = """_(_foo)"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):_(_foo):]", "[end-para:::True]"]
    expected_gfm = """<p>_(_foo)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_382() -> None:
    """
    Test case 382:  This is emphasis within emphasis:
    """

    # Arrange
    source_markdown = """_(_foo_)_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):(:]",
        "[emphasis(1,3):1:_]",
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
def test_emphasis_383() -> None:
    """
    Test case 383:  (part 1) Intraword emphasis is disallowed for _:
    """

    # Arrange
    source_markdown = """_foo_bar"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):_foo_bar:]", "[end-para:::True]"]
    expected_gfm = """<p>_foo_bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_384() -> None:
    """
    Test case 384:  (part 2) Intraword emphasis is disallowed for _:
    """

    # Arrange
    source_markdown = """_пристаням_стремятся"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):_пристаням_стремятся:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>_пристаням_стремятся</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_385() -> None:
    """
    Test case 385:  (part 3) Intraword emphasis is disallowed for _:
    """

    # Arrange
    source_markdown = """_foo_bar_baz_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):foo_bar_baz:]",
        "[end-emphasis(1,13)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo_bar_baz</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_386() -> None:
    """
    Test case 386:  This is emphasis, even though the closing delimiter is both left- and right-flanking, because it is followed by punctuation:
    """

    # Arrange
    source_markdown = """_(bar)_."""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):(bar):]",
        "[end-emphasis(1,7)::]",
        "[text(1,8):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>(bar)</em>.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
