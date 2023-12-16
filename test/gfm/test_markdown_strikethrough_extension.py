"""
https://github.github.com/gfm/#emphasis-and-strong-emphasis
"""

from test.utils import act_and_assert

config_map = {"extensions": {"markdown-strikethrough": {"enabled": True}}}


def test_strikethrough_491_x():
    """
    Test case 491:  Strikethrough text is any text wrapped in two tildes (~).
    """

    # Arrange
    source_markdown = """~~Hi~~ Hello, ~there~ world!"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):2:~]",
        "[text(1,3):Hi:]",
        "[end-emphasis(1,5)::]",
        "[text(1,7): Hello, :]",
        "[emphasis(1,15):1:~]",
        "[text(1,16):there:]",
        "[end-emphasis(1,21)::]",
        "[text(1,22): world!:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><del>Hi</del> Hello, <del>there</del> world!</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_strikethrough_491_a():
    """
    Test case 491:  Nothing happens if the configuration is not set.
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


def test_strikethrough_492_x():
    """
    Test case 492:  As with regular emphasis delimiters, a new paragraph will cause strikethrough parsing to cease:
    """

    # Arrange
    source_markdown = """This ~~has a

new paragraph~~."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This :]",
        "[text(1,6):~~:]",
        "[text(1,8):has a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):new paragraph:]",
        "[text(3,14):~~:]",
        "[text(3,16):.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>This ~~has a</p>\n<p>new paragraph~~.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_strikethrough_492_a():
    """
    Test case 492:  Nothing STILL happens if the configuration is not set.
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


def test_strikethrough_493_x():
    """
    Test case 492:  As with regular emphasis delimiters, a new paragraph will cause strikethrough parsing to cease:
    """

    # Arrange
    source_markdown = """This will ~~~not~~~ strike."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This will :]",
        "[text(1,11):~~~:]",
        "[text(1,14):not:]",
        "[text(1,17):~~~:]",
        "[text(1,20): strike.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>This will ~~~not~~~ strike.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_strikethrough_493_a():
    """
    Test case 492:  Nothing STILL happens if the configuration is not set.
    """

    # Arrange
    source_markdown = """This will ~~~not~~~ strike."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This will ~~~not~~~ strike.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>This will ~~~not~~~ strike.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_strikethrough_493_b():
    """
    Test case 492:  varient, allowing end to have less, still not valid
    """

    # Arrange
    source_markdown = """This will ~~~not~~ strike."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This will :]",
        "[text(1,11):~~~:]",
        "[text(1,14):not:]",
        "[text(1,17):~~:]",
        "[text(1,19): strike.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>This will ~~~not~~ strike.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )
