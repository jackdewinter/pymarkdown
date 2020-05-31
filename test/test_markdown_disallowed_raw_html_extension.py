"""
https://github.github.com/gfm/#disallowed-raw-html-extension-
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different, assert_token_consistency


@pytest.mark.skip
def test_disallowed_raw_html_extension_653():
    """
    Test case 653:  All other HTML tags are left untouched.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
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

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_token_consistency(source_markdown, actual_tokens)
