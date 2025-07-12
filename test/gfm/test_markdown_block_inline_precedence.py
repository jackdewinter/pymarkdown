"""
https://github.github.com/gfm/#precedence
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_block_inline_precedence_012() -> None:
    """
    Test case 012:  Indicators of block structure always take precedence over indicators of inline structure.
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
    expected_gfm = """<ul>
<li>`one</li>
<li>two`</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
