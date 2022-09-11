"""
https://github.github.com/gfm/#soft-line-breaks
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_soft_line_breaks_669():
    """
    Test case 669:  A regular line break (not in a code span or HTML tag) that is not preceded by two or more spaces or a backslash is parsed as a softbreak.
    """

    # Arrange
    source_markdown = """foo
baz"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo\nbaz::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo
baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_soft_line_breaks_670():
    """
    Test case 670:  Spaces at the end of the line and beginning of the next line are removed:
    """

    # Arrange
    source_markdown = """foo\a
 baz""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n ]",
        "[text(1,1):foo\nbaz:: \n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo 
baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
