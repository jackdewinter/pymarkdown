"""
https://github.github.com/gfm/#disallowed-raw-html-extension-
"""
import pytest

from .utils import act_and_assert


@pytest.mark.skip
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
        "[para:]",
        "[raw-html:a]",
        "[raw-html:bab]",
        "[raw-html:c2c]",
        "[end-para]",
    ]
    expected_gfm = """
"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
