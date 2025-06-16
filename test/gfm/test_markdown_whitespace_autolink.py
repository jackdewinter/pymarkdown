"""
Testing various aspects of whitespaces around autolinks.
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_autolink_uri_with_spaces() -> None:
    """
    Test case:  autolink_uri with spaces
    """

    # Arrange
    source_markdown = """<http://foo.bar.baz/test?q=hello man&id=22&boolean>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\ahttp://foo.bar.baz/test?q=hello man\a&\a&amp;\aid=22\a&\a&amp;\aboolean\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>&lt;http://foo.bar.baz/test?q=hello man&amp;id=22&amp;boolean&gt;</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_autolink_uri_with_tabs_inside() -> None:
    """
    Test case:  autolink_uri with tabs
    """

    # Arrange
    source_markdown = """<http://foo.bar.baz/test?q=hello\tman&id=22&boolean>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\ahttp://foo.bar.baz/test?q=hello\tman\a&\a&amp;\aid=22\a&\a&amp;\aboolean\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>&lt;http://foo.bar.baz/test?q=hello\tman&amp;id=22&amp;boolean&gt;</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_autolink_uri_with_tabs_outside() -> None:
    """
    Test case:  autolink_uri with tabs
    """

    # Arrange
    source_markdown = """this\tis <http://foo.bar.baz> an\tautolink"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this\tis :]",
        "[uri-autolink(1,12):http://foo.bar.baz]",
        "[text(1,32): an\tautolink:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this\tis <a href="http://foo.bar.baz">http://foo.bar.baz</a> an\tautolink</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_autolink_uri_with_form_feeds() -> None:
    """
    Test case: autolink_uri with form feeds
    """

    # Arrange
    source_markdown = """<http://foo.bar.baz/test?q=hello\u000cman&id=22&boolean>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\ahttp://foo.bar.baz/test?q=hello\u000cman\a&\a&amp;\aid=22\a&\a&amp;\aboolean\a>\a&gt;\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;http://foo.bar.baz/test?q=hello\u000cman&amp;id=22&amp;boolean&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
