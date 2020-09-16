"""
https://github.github.com/gfm/#paragraph
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    assert_if_lists_different,
    assert_if_strings_different,
    assert_token_consistency,
)


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_paragraph_extra_01():
    """
    Test case extra 1:  Paragraph starts with a backslash escape
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\\\this is a fun day"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b\\this is a fun day:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\\this is a fun day</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_02():
    """
    Test case extra 2:  Paragraph starts with a backslash as in a hard line break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = """<p>\\</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_03():
    """
    Test case extra 3:  Paragraph starts with 2+ spaces as in a hard line break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\a\a\a
---""".replace(
        "\a", " "
    )
    expected_tokens = ["[BLANK(1,1):   ]", "[tbreak(2,1):-::---]"]
    expected_gfm = """<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_04():
    """
    Test case extra 4:  Paragraph string starting with a code span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """``this`` is a fun day"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):this:``::]",
        "[text(1,9): is a fun day:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>this</code> is a fun day</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_05():
    """
    Test case extra 5:  Paragraph string starting with a character reference.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """&amp; the band played on"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a&amp;\a\a&\a&amp;\a\a the band played on:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&amp; the band played on</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_06():
    """
    Test case extra 6:  Paragraph string starting with a raw html block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<there it='is'>, really"""
    expected_tokens = [
        "[para(1,1):]",
        "[raw-html(1,1):there it='is']",
        "[text(1,16):, really:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><there it='is'>, really</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_07():
    """
    Test case extra 7:  Paragraph string starting with an URI autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<http://www.google.com> is where to look"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://www.google.com]",
        "[text(1,24): is where to look:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://www.google.com">http://www.google.com</a> is where to look</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_08():
    """
    Test case extra 8:  Paragraph string starting with an email autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<foo@bar.com> for more information"""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink(1,1):foo@bar.com]",
        "[text(1,14): for more information:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="mailto:foo@bar.com">foo@bar.com</a> for more information</p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_09():
    """
    Test case extra 9:  Paragraph string starting with an emphasis
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*it's* me!"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):it's:]",
        "[end-emphasis(1,6)::1:*:False]",
        "[text(1,7): me!:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>it's</em> me!</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_10():
    """
    Test case extra 10:  Paragraph string starting with a link.  also see 183
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[Foo](/uri) is a link"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/uri:::::Foo:False::::]",
        "[text(1,2):Foo:]",
        "[end-link:::False]",
        "[text(1,12): is a link:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">Foo</a> is a link</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_11():
    """
    Test case extra 11:  Paragraph string starting with an image
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo](/url "title") is an image"""
    expected_tokens = [
        "[para(1,1):]",
        '[image(1,1):inline:/url:title:foo::::foo:False:":: :]',
        "[text(1,21): is an image:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /> is an image</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_12():
    """
    Test case extra 12:  Paragraph containing a backslash
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """this is a \\\\fun\\\\ day"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this is a \\\b\\fun\\\b\\ day:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this is a \\fun\\ day</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_13():
    """
    Test case extra 13:  Paragraph containing a code span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """this is a ``fun`` day"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this is a :]",
        "[icode-span(1,11):fun:``::]",
        "[text(1,18): day:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this is a <code>fun</code> day</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_14():
    """
    Test case extra 14:  Paragraph containing a character reference.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """fun &amp; joy"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):fun \a&amp;\a\a&\a&amp;\a\a joy:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>fun &amp; joy</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_15():
    """
    Test case extra 15:  Paragraph containing a raw html block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """where <there it='is'> it"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):where :]",
        "[raw-html(1,7):there it='is']",
        "[text(1,22): it:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>where <there it='is'> it</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_16():
    """
    Test case extra 16:  Paragraph containing an URI autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """look at <http://www.google.com> for answers"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):look at :]",
        "[uri-autolink(1,9):http://www.google.com]",
        "[text(1,32): for answers:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>look at <a href="http://www.google.com">http://www.google.com</a> for answers</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_17():
    """
    Test case extra 17:  Paragraph containing an email autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """email <foo@bar.com> for answers"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):email :]",
        "[email-autolink(1,7):foo@bar.com]",
        "[text(1,20): for answers:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>email <a href="mailto:foo@bar.com">foo@bar.com</a> for answers</p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_18():
    """
    Test case extra 18:  Paragraph containing emphasis
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """really! *it's me!* here!"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):really! :]",
        "[emphasis(1,9):1:*]",
        "[text(1,10):it's me!:]",
        "[end-emphasis(1,18)::1:*:False]",
        "[text(1,19): here!:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>really! <em>it's me!</em> here!</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_19():
    """
    Test case extra 19:  Paragraph containing a link.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """look at [Foo](/uri) for more"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):look at :]",
        "[link(1,9):inline:/uri:::::Foo:False::::]",
        "[text(1,10):Foo:]",
        "[end-link:::False]",
        "[text(1,20): for more:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>look at <a href="/uri">Foo</a> for more</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_20():
    """
    Test case extra 20:  Paragraph containing an image
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """special ![foo](/url "title") headings"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):special :]",
        '[image(1,9):inline:/url:title:foo::::foo:False:":: :]',
        "[text(1,29): headings:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>special <img src="/url" alt="foo" title="title" /> headings</p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_21():
    """
    Test case extra 21:  Paragraphs ends with a backslash escape
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """this is a fun day\\\\"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this is a fun day\\\b\\:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this is a fun day\\</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_22():
    """
    Test case extra 22:  Paragraph ends with a backslash as in a hard line break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """this was \\
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this was \\:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = """<p>this was \\</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_23():
    """
    Test case extra 23:  Paragraph ends with 2+ spaces as in a hard line break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """what? no line break?\a\a\a
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1)::   ]",
        "[text(1,1):what? no line break?:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = """<p>what? no line break?</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_24():
    """
    Test case extra 24:  Paragraph string ending with a code span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """this is a fun ``day``"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this is a fun :]",
        "[icode-span(1,15):day:``::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this is a fun <code>day</code></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_25():
    """
    Test case extra 25:  Paragraph string ending with a character reference.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """the band played on &amp;"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):the band played on \a&amp;\a\a&\a&amp;\a\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>the band played on &amp;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_26():
    """
    Test case extra 26:  Paragraph string ending with a raw html block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """really, <there it='is'>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):really, :]",
        "[raw-html(1,9):there it='is']",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>really, <there it='is'></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_27():
    """
    Test case extra 27:  Paragraph string ending with an URI autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """look at <http://www.google.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):look at :]",
        "[uri-autolink(1,9):http://www.google.com]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>look at <a href="http://www.google.com">http://www.google.com</a></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_28():
    """
    Test case extra 28:  Paragraph string ending with an email autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """for more information, contact <foo@bar.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):for more information, contact :]",
        "[email-autolink(1,31):foo@bar.com]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>for more information, contact <a href="mailto:foo@bar.com">foo@bar.com</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_29():
    """
    Test case extra 29:  Paragraph string ending with an emphasis
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """it's *me*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):it's :]",
        "[emphasis(1,6):1:*]",
        "[text(1,7):me:]",
        "[end-emphasis(1,9)::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>it's <em>me</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_30():
    """
    Test case extra 30:  Paragraph string ending with a link.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a link looks like [Foo](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a link looks like :]",
        "[link(1,19):inline:/uri:::::Foo:False::::]",
        "[text(1,20):Foo:]",
        "[end-link:::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a link looks like <a href="/uri">Foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_31():
    """
    Test case extra 31:  Paragraph string ending with an image
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """an image is ![foo](/url "title")"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):an image is :]",
        '[image(1,13):inline:/url:title:foo::::foo:False:":: :]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>an image is <img src="/url" alt="foo" title="title" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_32():
    """
    Test case extra 32:  Paragraph this is only a backslash escape
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\\\"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b\\:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\\</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_33():
    """
    Test case extra 33:  Paragraph this is only a backslash as in a hard line break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ \\
"""
    expected_tokens = [
        "[para(1,2): ]",
        "[text(1,2):\\:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = """<p>\\</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_34():
    """
    Test case extra 34:  Paragraph this is only 2+ spaces as in a hard line break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\a\a\a\a
""".replace(
        "\a", " "
    )
    expected_tokens = ["[BLANK(1,1):    ]", "[BLANK(2,1):]"]
    expected_gfm = """"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_35():
    """
    Test case extra 35:  Paragraph this is only a code span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """``day``"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):day:``::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>day</code></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_36():
    """
    Test case extra 36:  Paragraph this is only a character reference.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """&amp;"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a&amp;\a\a&\a&amp;\a\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&amp;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_37():
    """
    Test case extra 37:  Paragraph this is only a raw html block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<there it='is'>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<there it='is'>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<there it='is'>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_38():
    """
    Test case extra 38:  Paragraph this is only an URI autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<http://www.google.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://www.google.com]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="http://www.google.com">http://www.google.com</a></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_39():
    """
    Test case extra 39:  Paragraph this is only an email autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<foo@bar.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink(1,1):foo@bar.com]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="mailto:foo@bar.com">foo@bar.com</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_40():
    """
    Test case extra 40:  Paragraph this is only an emphasis
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*me*"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):me:]",
        "[end-emphasis(1,4)::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>me</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_41():
    """
    Test case extra 41:  Paragraph this is only a link.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[Foo](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/uri:::::Foo:False::::]",
        "[text(1,2):Foo:]",
        "[end-link:::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">Foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_extra_42():
    """
    Test case extra 42:  Paragraph this is only an image
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo](/url "title")"""
    expected_tokens = [
        "[para(1,1):]",
        '[image(1,1):inline:/url:title:foo::::foo:False:":: :]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/url" alt="foo" title="title" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
