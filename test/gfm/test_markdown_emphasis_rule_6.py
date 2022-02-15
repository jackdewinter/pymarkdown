"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_emphasis_391():
    """
    Test case 391:  Rule 6:
    """

    # Arrange
    source_markdown = """__foo bar__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):foo bar:]",
        "[end-emphasis(1,10)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo bar</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_392():
    """
    Test case 392:  This is not strong emphasis, because the opening delimiter is followed by whitespace:
    """

    # Arrange
    source_markdown = """__ foo bar__"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):__:]",
        "[text(1,3): foo bar:]",
        "[text(1,11):__:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>__ foo bar__</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_393():
    """
    Test case 393:  A newline counts as whitespace:
    """

    # Arrange
    source_markdown = """__
foo bar__"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):__:]",
        "[text(1,3):\nfoo bar::\n]",
        "[text(2,8):__:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>__
foo bar__</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_394():
    """
    Test case 394:  This is not strong emphasis, because the opening __ is preceded by an alphanumeric and followed by punctuation:
    """

    # Arrange
    source_markdown = """a__"foo"__"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):__:]",
        '[text(1,4):\a"\a&quot;\afoo\a"\a&quot;\a:]',
        "[text(1,9):__:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a__&quot;foo&quot;__</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_395():
    """
    Test case 395:  (part 1) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    source_markdown = """foo__bar__"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo:]",
        "[text(1,4):__:]",
        "[text(1,6):bar:]",
        "[text(1,9):__:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo__bar__</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_396():
    """
    Test case 396:  (part 2) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    source_markdown = """5__6__78"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):5:]",
        "[text(1,2):__:]",
        "[text(1,4):6:]",
        "[text(1,5):__:]",
        "[text(1,7):78:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>5__6__78</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_397():
    """
    Test case 397:  (part 3) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    source_markdown = """пристаням__стремятся__"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):пристаням:]",
        "[text(1,10):__:]",
        "[text(1,12):стремятся:]",
        "[text(1,21):__:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>пристаням__стремятся__</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_398():
    """
    Test case 398:  (part 4) Intraword strong emphasis is forbidden with __:
    """

    # Arrange
    source_markdown = """__foo, __bar__, baz__"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:_]",
        "[text(1,3):foo, :]",
        "[emphasis(1,8):2:_]",
        "[text(1,10):bar:]",
        "[end-emphasis(1,13)::]",
        "[text(1,15):, baz:]",
        "[end-emphasis(1,20)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><strong>foo, <strong>bar</strong>, baz</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_399():
    """
    Test case 399:  This is strong emphasis, even though the opening delimiter is both left- and right-flanking, because it is preceded by punctuation:
    """

    # Arrange
    source_markdown = """foo-__(bar)__"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo-:]",
        "[emphasis(1,5):2:_]",
        "[text(1,7):(bar):]",
        "[end-emphasis(1,12)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo-<strong>(bar)</strong></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
