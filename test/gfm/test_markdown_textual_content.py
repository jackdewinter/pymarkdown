"""
https://github.github.com/gfm/#textual-content
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_textual_content_671() -> None:
    """
    Test case 671:  (part 1) Any characters not given an interpretation by the above rules will be parsed as plain textual content.
    """

    # Arrange
    source_markdown = """hello $.;'there"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):hello $.;'there:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>hello $.;'there</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_672() -> None:
    """
    Test case 672:  (part 2) Any characters not given an interpretation by the above rules will be parsed as plain textual content.
    """

    # Arrange
    source_markdown = """Foo χρῆν"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):Foo χρῆν:]", "[end-para:::True]"]
    expected_gfm = """<p>Foo χρῆν</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_673() -> None:
    """
    Test case 673:  Internal spaces are preserved verbatim:
    """

    # Arrange
    source_markdown = """Multiple     spaces"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):Multiple     spaces:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Multiple     spaces</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
