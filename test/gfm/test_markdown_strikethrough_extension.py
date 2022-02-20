"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""

from test.utils import act_and_assert


def test_strikethrough_491():
    """
    Test case 491:  Strikethrough text is any text wrapped in two tildes (~).
    """

    # Arrange
    source_markdown = """~~Hi~~ Hello, world!"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):~~Hi~~ Hello, world!:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>~~Hi~~ Hello, world!</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_strikethrough_492():
    """
    Test case 492:  As with regular emphasis delimiters, a new paragraph will cause strikethrough parsing to cease:
    """

    # Arrange
    source_markdown = """This ~~has a

new paragraph~~."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This ~~has a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):new paragraph~~.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>This ~~has a</p>\n<p>new paragraph~~.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
