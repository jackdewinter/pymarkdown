"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""
import pytest

from .utils import act_and_assert


@pytest.mark.gfm
def test_emphasis_366():
    """
    Test case 366:  Rule 2:
    """

    # Arrange
    source_markdown = """_foo bar_"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:_]",
        "[text(1,2):foo bar:]",
        "[end-emphasis(1,9):::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo bar</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_367():
    """
    Test case 367:  This is not emphasis, because the opening _ is followed by whitespace:
    """

    # Arrange
    source_markdown = """_ foo bar_"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):_:]",
        "[text(1,2): foo bar:]",
        "[text(1,10):_:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>_ foo bar_</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_368():
    """
    Test case 368:  This is not emphasis, because the opening _ is preceded by an alphanumeric and followed by punctuation:
    """

    # Arrange
    source_markdown = """a_"foo"_"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[text(1,2):_:]",
        '[text(1,3):\a"\a&quot;\afoo\a"\a&quot;\a:]',
        "[text(1,8):_:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a_&quot;foo&quot;_</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_369():
    """
    Test case 369:  (part 1) Emphasis with _ is not allowed inside words:
    """

    # Arrange
    source_markdown = """foo_bar_"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo:]",
        "[text(1,4):_:]",
        "[text(1,5):bar:]",
        "[text(1,8):_:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo_bar_</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_370():
    """
    Test case 370:  (part 2) Emphasis with _ is not allowed inside words:
    """

    # Arrange
    source_markdown = """5_6_78"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):5:]",
        "[text(1,2):_:]",
        "[text(1,3):6:]",
        "[text(1,4):_:]",
        "[text(1,5):78:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>5_6_78</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_371():
    """
    Test case 371:  (part 3) Emphasis with _ is not allowed inside words:
    """

    # Arrange
    source_markdown = """пристаням_стремятся_"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):пристаням:]",
        "[text(1,10):_:]",
        "[text(1,11):стремятся:]",
        "[text(1,20):_:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>пристаням_стремятся_</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_372():
    """
    Test case 372:  Here _ does not generate emphasis, because the first delimiter run is right-flanking and the second left-flanking:
    """

    # Arrange
    source_markdown = """aa_"bb"_cc"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):aa:]",
        "[text(1,3):_:]",
        '[text(1,4):\a"\a&quot;\abb\a"\a&quot;\a:]',
        "[text(1,8):_:]",
        "[text(1,9):cc:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>aa_&quot;bb&quot;_cc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_emphasis_373():
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
        "[end-emphasis(1,11):::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo-<em>(bar)</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
