"""
https://github.github.com/gfm/#html-blocks
"""
from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_html_blocks_extrax_01():
    """
    Test case 01:  Pragma alone in a document.
    """

    # Arrange
    source_markdown = """<!-- pyml -->"""
    expected_tokens = ["[pragma:1:<!-- pyml -->]"]
    expected_gfm = """"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_html_blocks_extrax_02():
    """
    Test case 02:  Pargma within a paragraph.
    """

    # Arrange
    source_markdown = """This is a paragraph
<!-- pyml -->
still a paragraph
<!-- pyml -->
and still going.
"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):This is a paragraph\nstill a paragraph\nand still going.::\n\n]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[pragma:2:<!-- pyml -->;4:<!-- pyml -->]",
    ]
    expected_gfm = """<p>This is a paragraph\nstill a paragraph\nand still going.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_html_blocks_extrax_03():
    """
    Test case 03:  Pragma at the start and end of the document.
    """

    # Arrange
    source_markdown = """<!-- pyml -->
This is a paragraph
still a paragraph
and still going.
<!-- pyml -->"""
    expected_tokens = [
        "[para(2,1):\n\n]",
        "[text(2,1):This is a paragraph\nstill a paragraph\nand still going.::\n\n]",
        "[end-para:::True]",
        "[pragma:1:<!-- pyml -->;5:<!-- pyml -->]",
    ]
    expected_gfm = """<p>This is a paragraph\nstill a paragraph\nand still going.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_html_blocks_extrax_03a():
    """
    Test case 03a:  Pragma at start and end with a single line paragraph.
    """

    # Arrange
    source_markdown = """<!-- pyml -->
This is a paragraph.
<!-- pyml -->"""
    expected_tokens = [
        "[para(2,1):]",
        "[text(2,1):This is a paragraph.:]",
        "[end-para:::True]",
        "[pragma:1:<!-- pyml -->;3:<!-- pyml -->]",
    ]
    expected_gfm = """<p>This is a paragraph.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_html_blocks_extrax_04():
    """
    Test case 04:  Only two pragmas in entire document.
    """

    # Arrange
    source_markdown = """<!-- pyml -->
<!-- pyml -->"""
    expected_tokens = ["[pragma:1:<!-- pyml -->;2:<!-- pyml -->]"]
    expected_gfm = ""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_html_blocks_extrax_05():
    """
    Test case 05:  Single line paragraph with double pragmas to start and end document.
    """

    # Arrange
    source_markdown = """<!-- pyml -->
<!-- pyml -->
this is a paragraph
<!-- pyml -->
<!-- pyml -->"""
    expected_tokens = [
        "[para(3,1):]",
        "[text(3,1):this is a paragraph:]",
        "[end-para:::True]",
        "[pragma:1:<!-- pyml -->;2:<!-- pyml -->;4:<!-- pyml -->;5:<!-- pyml -->]",
    ]
    expected_gfm = "<p>this is a paragraph</p>"

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_html_blocks_extrax_06():
    """
    Test case 06:  Verify that an HTML comment followed by the "pyml " title without any whitespace is parsed.
    """

    # Arrange
    source_markdown = """<!--pyml -->
this is a paragraph
"""
    expected_tokens = [
        "[para(2,1):]",
        "[text(2,1):this is a paragraph:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[pragma:1:<!--pyml -->]",
    ]
    expected_gfm = "<p>this is a paragraph</p>"

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_html_blocks_extrax_07():
    """
    Test case 07:  Verify that an HTML comment followed by the "pyml " title with multiple whitespace is parsed.
    """

    # Arrange
    source_markdown = """<!-- \t \tpyml -->
this is a paragraph
"""
    expected_tokens = [
        "[para(2,1):]",
        "[text(2,1):this is a paragraph:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[pragma:1:<!-- \t \tpyml -->]",
    ]
    expected_gfm = "<p>this is a paragraph</p>"

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_html_blocks_extrax_08():
    """
    Test case 08:  Pragma-like, without the space after the pragma title.
    """

    # Arrange
    source_markdown = """<!-- pyml-->
this is a paragraph
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<!-- pyml-->:]",
        "[end-html-block:::False]",
        "[para(2,1):]",
        "[text(2,1):this is a paragraph:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = "<!-- pyml-->\n<p>this is a paragraph</p>"

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_html_blocks_extrax_09():
    """
    Test case 08:  Pragma-like, without the closing comment sequence.
    """

    # Arrange
    source_markdown = """<!-- pyml--
this is a paragraph
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<!-- pyml--\nthis is a paragraph:]",
        "[BLANK(3,1):]",
        "[end-html-block:::True]",
    ]
    expected_gfm = "<!-- pyml--\nthis is a paragraph\n"

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_html_blocks_extrax_010():
    """
    Test case 10:  Pragma heading, but with different casing.
    """

    # Arrange
    source_markdown = """<!-- PyML -->
this is a paragraph
"""
    expected_tokens = [
        "[para(2,1):]",
        "[text(2,1):this is a paragraph:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[pragma:1:<!-- PyML -->]",
    ]
    expected_gfm = "<p>this is a paragraph</p>"

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_html_blocks_extrax_011():
    """
    Test case 11:  Pragma heading, but with extra spacing after the closing comment.
    """

    # Arrange
    source_markdown = """<!-- pyml -->\a\a\a
this is a paragraph
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(2,1):]",
        "[text(2,1):this is a paragraph:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[pragma:1:<!-- pyml -->   ]",
    ]
    expected_gfm = "<p>this is a paragraph</p>"

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )
