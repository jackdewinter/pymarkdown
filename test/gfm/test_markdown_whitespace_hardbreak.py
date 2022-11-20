"""
Testing various aspects of whitespaces around hardbreaks.
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_hard_break_with_spaces():
    """
    Test case:  hard_break with spaces
    """

    # Arrange
    source_markdown = """foo   
bar"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo:]",
        "[hard-break(1,4):   :\n]",
        "[text(2,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<br />
bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_hard_break_with_tabs():
    """
    Test case:  hard_break with tabs
    """

    # Arrange
    source_markdown = """foo\t\t
bar"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo\nbar::\t\t\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo\t\t
bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_hard_break_with_form_feeds():
    """
    Test case: hard_break with form feeds
    """

    # Arrange
    source_markdown = """foo\u000c\u000c
bar"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo\u000c\u000c\nbar::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo\u000c\u000c
bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
