"""
Test the top level transform functions.
"""

from .utils import act_and_assert


def test_transform_with_debug_on():
    """
    Copy of test case 012 to test with debug logging.
    """

    # Arrange
    source_markdown = """- `one
- two`"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):`one:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):two`:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>\n<li>`one</li>\n<li>two`</li>\n</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


def test_transform_with_debug_off():
    """
    Copy of test case 012 to test with debug logging off.
    """

    # Arrange
    source_markdown = """- `one
- two`"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):`one:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):two`:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>\n<li>`one</li>\n<li>two`</li>\n</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)
