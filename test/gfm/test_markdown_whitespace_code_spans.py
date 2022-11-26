"""
Testing various aspects of whitespaces around code spans.
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_code_span_with_spaces():
    """
    Test case:  code span with spaces at the front and end
    """

    # Arrange
    source_markdown = """a ` good ` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):good:`: : ]",
        "[text(1,11): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>good</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_0x():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a `\tgood\t` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):\tgood\t:`::]",
        "[text(1,14): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>\tgood\t</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_0a():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a `\tgood` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):\tgood:`::]",
        "[text(1,10): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>\tgood</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_0b():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a `good\t` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):good\t:`::]",
        "[text(1,10): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>good\t</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_0c():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """`\tgood\t`"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):\tgood\t:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>\tgood\t</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_1():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a `&#09;good&#09;` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):\a&\a&amp;\a#09;good\a&\a&amp;\a#09;:`::]",
        "[text(1,19): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>&amp;#09;good&amp;#09;</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_2():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a &#09;`good`&#09; paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \a&#09;\a\t\a:]",
        "[icode-span(1,8):good:`::]",
        "[text(1,14):\a&#09;\a\t\a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a \t<code>good</code>\t paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_3():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a &#09;`&#09;good&#09;`&#09; paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \a&#09;\a\t\a:]",
        "[icode-span(1,8):\a&\a&amp;\a#09;good\a&\a&amp;\a#09;:`::]",
        "[text(1,24):\a&#09;\a\t\a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a \t<code>&amp;#09;good&amp;#09;</code>\t paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_4():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a \t`&#09;good&#09;`\t paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \t:]",
        "[icode-span(1,5):\a&\a&amp;\a#09;good\a&\a&amp;\a#09;:`::]",
        "[text(1,21):\t paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a \t<code>&amp;#09;good&amp;#09;</code>\t paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_4a():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a \t`&#09;good&#09;` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \t:]",
        "[icode-span(1,5):\a&\a&amp;\a#09;good\a&\a&amp;\a#09;:`::]",
        "[text(1,21): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a \t<code>&amp;#09;good&amp;#09;</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_4b():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a `&#09;good&#09;`\t paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):\a&\a&amp;\a#09;good\a&\a&amp;\a#09;:`::]",
        "[text(1,19):\t paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>&amp;#09;good&amp;#09;</code>\t paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_4c():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """\t`&#09;good&#09;`\t"""
    expected_tokens = [
        "[icode-block(1,5):\t:]",
        "[text(1,5):`\a&\a&amp;\a#09;good\a&\a&amp;\a#09;`\t:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>`&amp;#09;good&amp;#09;`\t
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_5():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a &#09;`\tgood\t`&#09; paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \a&#09;\a\t\a:]",
        "[icode-span(1,8):\tgood\t:`::]",
        "[text(1,22):\a&#09;\a\t\a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a 	<code>\tgood\t</code>	 paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_5a():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a &#09;`\tgood`&#09; paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \a&#09;\a\t\a:]",
        "[icode-span(1,8):\tgood:`::]",
        "[text(1,18):\a&#09;\a\t\a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a 	<code>\tgood</code>\t paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_5b():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a &#09;`good\t`&#09; paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a \a&#09;\a\t\a:]",
        "[icode-span(1,8):good\t:`::]",
        "[text(1,18):\a&#09;\a\t\a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a 	<code>good\t</code>\t paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_5c():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """`\tgood\t`"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):\tgood\t:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>\tgood\t</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_6():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a\tvery `&#09;good&#09;`xx\t paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a\tvery :]",
        "[icode-span(1,10):\a&\a&amp;\a#09;good\a&\a&amp;\a#09;:`::]",
        "[text(1,26):xx\t paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>a\tvery <code>&amp;#09;good&amp;#09;</code>xx\t paragraph</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_span_with_tabs_6a():
    """
    Test case:  code span with tabs at the front and end
    """

    # Arrange
    source_markdown = """a\tvery `&#09;good&#09;`"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a\tvery :]",
        "[icode-span(1,10):\a&\a&amp;\a#09;good\a&\a&amp;\a#09;:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a\tvery <code>&amp;#09;good&amp;#09;</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_code_spans_with_form_feeds():
    """
    Test case: code span with form feeds at the front and end
    """

    # Arrange
    source_markdown = """a `\u000cgood\u000c` paragraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a :]",
        "[icode-span(1,3):\u000cgood\u000c:`::]",
        "[text(1,11): paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a <code>\u000cgood\u000c</code> paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
