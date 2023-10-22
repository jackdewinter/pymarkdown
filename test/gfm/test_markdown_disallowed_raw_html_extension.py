"""
https://github.github.com/gfm/#disallowed-raw-html-extension-
"""
from test.utils import act_and_assert

import pytest

config_map = {"extensions": {"markdown-disallow-raw-html": {"enabled": True}}}


@pytest.mark.gfm
def test_disallowed_raw_html_extension_653():
    """
    Test case 653:  All other HTML tags are left untouched.
    """

    # Arrange
    source_markdown = """<strong> <title> <style> <em>

<blockquote>
  <xmp> is disallowed.  <XMP> is also disallowed.
</blockquote>"""
    expected_tokens = [
        "[para(1,1):]",
        "[raw-html(1,1):strong]",
        "[text(1,9): :]",
        "[text(1,10):\a<\a&lt;\atitle>:]",
        "[text(1,17): :]",
        "[text(1,18):\a<\a&lt;\astyle>:]",
        "[text(1,25): :]",
        "[raw-html(1,26):em]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[html-block(3,1)]",
        "[text(3,1):<blockquote>\n  \a<\a&lt;\axmp> is disallowed.  \a<\a&lt;\aXMP> is also disallowed.\n</blockquote>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<p><strong> &lt;title> &lt;style> <em></p>
<blockquote>
  &lt;xmp> is disallowed.  &lt;XMP> is also disallowed.
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )
