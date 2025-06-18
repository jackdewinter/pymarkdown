"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_emphasis_366() -> None:
    """
    Test case 366:  Rule 2:
    """

    # Arrange
    source_markdown = """_foo bar_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):foo bar:]",
        "[end-emphasis(1,9)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo bar</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_367() -> None:
    """
    Test case 367:  This is not emphasis, because the opening _ is followed by whitespace:
    """

    # Arrange
    source_markdown = """_ foo bar_"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):_ foo bar_:]", "[end-para:::True]"]
    expected_gfm = """<p>_ foo bar_</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_368() -> None:
    """
    Test case 368:  This is not emphasis, because the opening _ is preceded by an alphanumeric and followed by punctuation:
    """

    # Arrange
    source_markdown = """a_"foo"_"""
    expected_tokens = [
        "[para(1,1):]",
        '[text(1,1):a_\a"\a&quot;\afoo\a"\a&quot;\a_:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a_&quot;foo&quot;_</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_369() -> None:
    """
    Test case 369:  (part 1) Emphasis with _ is not allowed inside words:
    """

    # Arrange
    source_markdown = """foo_bar_"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):foo_bar_:]", "[end-para:::True]"]
    expected_gfm = """<p>foo_bar_</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_370() -> None:
    """
    Test case 370:  (part 2) Emphasis with _ is not allowed inside words:
    """

    # Arrange
    source_markdown = """5_6_78"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):5_6_78:]", "[end-para:::True]"]
    expected_gfm = """<p>5_6_78</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_371() -> None:
    """
    Test case 371:  (part 3) Emphasis with _ is not allowed inside words:
    """

    # Arrange
    source_markdown = """пристаням_стремятся_"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):пристаням_стремятся_:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>пристаням_стремятся_</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_372() -> None:
    """
    Test case 372:  Here _ does not generate emphasis, because the first delimiter run is right-flanking and the second left-flanking:
    """

    # Arrange
    source_markdown = """aa_"bb"_cc"""
    expected_tokens = [
        "[para(1,1):]",
        '[text(1,1):aa_\a"\a&quot;\abb\a"\a&quot;\a_cc:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aa_&quot;bb&quot;_cc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_373() -> None:
    """
    Test case 373:  This is emphasis, even though the opening delimiter is both left- and right-flanking, because it is preceded by punctuation:
    """

    # Arrange
    source_markdown = """foo-_(bar)_"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo-:]",
        "[emphasis(1,5):1:_]",
        "[text(1,6):(bar):]",
        "[end-emphasis(1,11)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo-<em>(bar)</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
