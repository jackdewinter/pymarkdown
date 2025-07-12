"""
https://github.github.com/gfm/#paragraphs
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_blank_lines_197() -> None:
    """
    Test case 197:  Blank lines at the beginning and end of the document are also ignored.
    """

    # Arrange
    source_markdown = """\a\a

aaa
\a\a

# aaa

  """.replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):  ]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):aaa:]",
        "[end-para:::True]",
        "[BLANK(4,1):  ]",
        "[BLANK(5,1):]",
        "[atx(6,1):1:0:]",
        "[text(6,3):aaa: ]",
        "[end-atx::]",
        "[BLANK(7,1):]",
        "[BLANK(8,1):  ]",
    ]
    expected_gfm = """<p>aaa</p>
<h1>aaa</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_blank_lines_197a() -> None:
    """
    Test case 197a:  variation of 197 with extra spaces
    """

    # Arrange
    source_markdown = """\a\a
\a
aaa
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):  ]",
        "[BLANK(2,1): ]",
        "[para(3,1):]",
        "[text(3,1):aaa:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>aaa</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
