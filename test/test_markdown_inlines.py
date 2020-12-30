"""
https://github.github.com/gfm/#inlines
"""
import pytest

from .utils import (
    act_and_assert
)


@pytest.mark.gfm
def test_inlines_307():
    """
    Test case 307:  Thus, for example, in
    """

    # Arrange
    source_markdown = """`hi`lo`"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):hi:`::]",
        "[text(1,5):lo`:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>hi</code>lo`</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
