"""
Pragmas
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_pragma_parsing_01() -> None:
    """
    Test case 01:  Pragma alone in a document.
    """

    # Arrange
    source_markdown = """<!-- pyml -->"""
    expected_tokens = ["[pragma:1:<!-- pyml -->]"]
    expected_gfm = """"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_02() -> None:
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_03() -> None:
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_03a() -> None:
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_04() -> None:
    """
    Test case 04:  Only two pragmas in entire document.
    """

    # Arrange
    source_markdown = """<!-- pyml -->
<!-- pyml -->"""
    expected_tokens = ["[pragma:1:<!-- pyml -->;2:<!-- pyml -->]"]
    expected_gfm = ""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_05() -> None:
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_06() -> None:
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_07() -> None:
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
        source_markdown, expected_gfm, expected_tokens, allow_alternate_markdown=True
    )


@pytest.mark.gfm
def test_pragma_parsing_08() -> None:
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_09() -> None:
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_010() -> None:
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_011() -> None:
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_011a() -> None:
    """
    Test case 11:  Pragma heading, but with extra spacing after the closing comment.
    """

    # Arrange
    source_markdown = """<!-- pyml -->\x0c\x0c\x0c
this is a paragraph
"""
    expected_tokens = [
        "[para(2,1):]",
        "[text(2,1):this is a paragraph:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[pragma:1:<!-- pyml -->\x0c\x0c\x0c]",
    ]
    expected_gfm = "<p>this is a paragraph</p>"

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_011b() -> None:
    """
    Test case 11:  Pragma heading, but with extra spacing after the closing comment.
    """

    # Arrange
    source_markdown = """<!-- pyml -->\u00a0\u00a0
this is a paragraph
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<!-- pyml -->\u00a0\u00a0:]",
        "[end-html-block:::False]",
        "[para(2,1):]",
        "[text(2,1):this is a paragraph:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<!-- pyml -->\u00a0\u00a0
<p>this is a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_issue_1447_a() -> None:
    """
    Test case: TBD
    """

    # Arrange
    source_markdown = """<!--- pyml disable-next-line first-line-heading --->
-8<- "README.md"
"""
    expected_tokens = [
        "[para(2,1):]",
        '[text(2,1):-8\a<\a&lt;\a- \a"\a&quot;\aREADME.md\a"\a&quot;\a:]',
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[pragma:-1:<!--- pyml disable-next-line first-line-heading --->]",
    ]
    expected_gfm = """<p>-8&lt;- &quot;README.md&quot;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_issue_1447_b() -> None:
    """
    Test case: TBD
    """

    # Arrange
    source_markdown = """<!-- pyml disable-next-line first-line-heading -->
-8<- "README.md"
"""
    expected_tokens = [
        "[para(2,1):]",
        '[text(2,1):-8\a<\a&lt;\a- \a"\a&quot;\aREADME.md\a"\a&quot;\a:]',
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[pragma:1:<!-- pyml disable-next-line first-line-heading -->]",
    ]
    expected_gfm = """<p>-8&lt;- &quot;README.md&quot;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_issue_1447_c() -> None:
    """
    Test case: TBD
    """

    # Arrange
    source_markdown = """<!--- pyml disable-next-line first-line-heading --->
-8<- "README.md"
<!-- pyml disable-next-line first-line-heading -->
-8<- "README.md"
"""
    expected_tokens = [
        "[para(2,1):\n]",
        '[text(2,1):-8\a<\a&lt;\a- \a"\a&quot;\aREADME.md\a"\a&quot;\a\n-8\a<\a&lt;\a- \a"\a&quot;\aREADME.md\a"\a&quot;\a::\n]',
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[pragma:-1:<!--- pyml disable-next-line first-line-heading --->;3:<!-- pyml disable-next-line first-line-heading -->]",
    ]
    expected_gfm = """<p>-8&lt;- &quot;README.md&quot;
-8&lt;- &quot;README.md&quot;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_pragma_parsing_issue_1447_d() -> None:
    """
    Test case: TBD
    """

    # Arrange
    source_markdown = """<!--- pyml disable-next-line first-line-heading --->
-8<- "README.md"
<!-- pyml disable-next-line first-line-heading -->
-8<- "README.md"
<!--- pyml disable-next-line first-line-heading --->
-8<- "README.md"
<!-- pyml disable-next-line first-line-heading -->
-8<- "README.md"
"""
    expected_tokens = [
        "[para(2,1):\n\n\n]",
        '[text(2,1):-8\a<\a&lt;\a- \a"\a&quot;\aREADME.md\a"\a&quot;\a\n-8\a<\a&lt;\a- \a"\a&quot;\aREADME.md\a"\a&quot;\a\n-8\a<\a&lt;\a- \a"\a&quot;\aREADME.md\a"\a&quot;\a\n-8\a<\a&lt;\a- \a"\a&quot;\aREADME.md\a"\a&quot;\a::\n\n\n]',
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[pragma:-1:<!--- pyml disable-next-line first-line-heading --->;3:<!-- pyml disable-next-line first-line-heading -->;-5:<!--- pyml disable-next-line first-line-heading --->;7:<!-- pyml disable-next-line first-line-heading -->]",
    ]
    expected_gfm = """<p>-8&lt;- &quot;README.md&quot;
-8&lt;- &quot;README.md&quot;
-8&lt;- &quot;README.md&quot;
-8&lt;- &quot;README.md&quot;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
