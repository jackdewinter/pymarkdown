"""
https://github.github.com/gfm/#setext-headings
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
def test_setext_headings_extra_01():
    """
    Test case extra 1:  SetExt heading starts with a backslash escape
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\\\this is a fun day
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\\\b\\this is a fun day:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>\\this is a fun day</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_02():
    """
    Test case extra 2:  SetExt heading starts with a backslash as in a hard line break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\\:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>\\</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_03():
    """
    Test case extra 3:  SetExt heading starts with 2+ spaces as in a hard line break
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
def test_setext_headings_extra_04():
    """
    Test case extra 4:  SetExt heading string starting with a code span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """``this`` is a fun day
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[icode-span(1,1):this:``::]",
        "[text(1,9): is a fun day:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2><code>this</code> is a fun day</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_05():
    """
    Test case extra 5:  SetExt heading string starting with a character reference.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """&amp; the band played on
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\a&amp;\a\a&\a&amp;\a\a the band played on:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>&amp; the band played on</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_06():
    """
    Test case extra 6:  SetExt heading string starting with a raw html block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<there it='is'>, really
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[raw-html(1,1):there it='is']",
        "[text(1,16):, really:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2><there it='is'>, really</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_07():
    """
    Test case extra 7:  SetExt heading string starting with an URI autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<http://www.google.com> is where to look
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[uri-autolink(1,1):http://www.google.com]",
        "[text(1,24): is where to look:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2><a href="http://www.google.com">http://www.google.com</a> is where to look</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_08():
    """
    Test case extra 8:  SetExt heading string starting with an email autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<foo@bar.com> for more information
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[email-autolink(1,1):foo@bar.com]",
        "[text(1,14): for more information:]",
        "[end-setext:::False]",
    ]
    expected_gfm = (
        """<h2><a href="mailto:foo@bar.com">foo@bar.com</a> for more information</h2>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_09():
    """
    Test case extra 9:  SetExt heading string starting with an emphasis
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*it's* me!
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):it's:]",
        "[end-emphasis(1,6)::1:*:False]",
        "[text(1,7): me!:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2><em>it's</em> me!</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_10():
    """
    Test case extra 10:  SetExt heading string starting with a link.  also see 183
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[Foo](/uri) is a link
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[link(1,1):inline:/uri:::::Foo:False::::]",
        "[text(1,2):Foo:]",
        "[end-link:::False]",
        "[text(1,12): is a link:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2><a href="/uri">Foo</a> is a link</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_11():
    """
    Test case extra 11:  SetExt heading string starting with an image
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo](/url "title") is an image
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        '[image(1,1):inline:/url:title:foo::::foo:False:":: :]',
        "[text(1,21): is an image:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2><img src="/url" alt="foo" title="title" /> is an image</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_12():
    """
    Test case extra 12:  SetExt heading containing a backslash
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """this is a \\\\fun\\\\ day
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):this is a \\\b\\fun\\\b\\ day:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>this is a \\fun\\ day</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_13():
    """
    Test case extra 13:  SetExt heading containing a code span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """this is a ``fun`` day
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):this is a :]",
        "[icode-span(1,11):fun:``::]",
        "[text(1,18): day:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>this is a <code>fun</code> day</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_14():
    """
    Test case extra 14:  SetExt heading containing a character reference.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """fun &amp; joy
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):fun \a&amp;\a\a&\a&amp;\a\a joy:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>fun &amp; joy</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_15():
    """
    Test case extra 15:  SetExt heading containing a raw html block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """where <there it='is'> it
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):where :]",
        "[raw-html(1,7):there it='is']",
        "[text(1,22): it:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>where <there it='is'> it</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_16():
    """
    Test case extra 16:  SetExt heading containing an URI autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """look at <http://www.google.com> for answers
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):look at :]",
        "[uri-autolink(1,9):http://www.google.com]",
        "[text(1,32): for answers:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>look at <a href="http://www.google.com">http://www.google.com</a> for answers</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_17():
    """
    Test case extra 17:  SetExt heading containing an email autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """email <foo@bar.com> for answers
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):email :]",
        "[email-autolink(1,7):foo@bar.com]",
        "[text(1,20): for answers:]",
        "[end-setext:::False]",
    ]
    expected_gfm = (
        """<h2>email <a href="mailto:foo@bar.com">foo@bar.com</a> for answers</h2>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_18():
    """
    Test case extra 18:  SetExt heading containing emphasis
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """really! *it's me!* here!
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):really! :]",
        "[emphasis(1,9):1:*]",
        "[text(1,10):it's me!:]",
        "[end-emphasis(1,18)::1:*:False]",
        "[text(1,19): here!:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>really! <em>it's me!</em> here!</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_19():
    """
    Test case extra 19:  SetExt heading containing a link.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """look at [Foo](/uri) for more
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):look at :]",
        "[link(1,9):inline:/uri:::::Foo:False::::]",
        "[text(1,10):Foo:]",
        "[end-link:::False]",
        "[text(1,20): for more:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>look at <a href="/uri">Foo</a> for more</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_20():
    """
    Test case extra 20:  SetExt heading containing an image
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """special ![foo](/url "title") headings
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):special :]",
        '[image(1,9):inline:/url:title:foo::::foo:False:":: :]',
        "[text(1,29): headings:]",
        "[end-setext:::False]",
    ]
    expected_gfm = (
        """<h2>special <img src="/url" alt="foo" title="title" /> headings</h2>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_21():
    """
    Test case extra 21:  SetExt headings ends with a backslash escape
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """this is a fun day\\\\
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):this is a fun day\\\b\\:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>this is a fun day\\</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_22():
    """
    Test case extra 22:  SetExt heading ends with a backslash as in a hard line break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """this was \\
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):this was \\:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>this was \\</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_23():
    """
    Test case extra 23:  SetExt heading ends with 2+ spaces as in a hard line break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """what? no line break?\a\a\a
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[setext(2,1):-:3::(1,1):   ]",
        "[text(1,1):what? no line break?:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>what? no line break?</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_24():
    """
    Test case extra 24:  SetExt heading string ending with a code span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """this is a fun ``day``
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):this is a fun :]",
        "[icode-span(1,15):day:``::]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>this is a fun <code>day</code></h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_25():
    """
    Test case extra 25:  SetExt heading string ending with a character reference.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """the band played on &amp;
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):the band played on \a&amp;\a\a&\a&amp;\a\a:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>the band played on &amp;</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_26():
    """
    Test case extra 26:  SetExt heading string ending with a raw html block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """really, <there it='is'>
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):really, :]",
        "[raw-html(1,9):there it='is']",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>really, <there it='is'></h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_27():
    """
    Test case extra 27:  SetExt heading string ending with an URI autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """look at <http://www.google.com>
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):look at :]",
        "[uri-autolink(1,9):http://www.google.com]",
        "[end-setext:::False]",
    ]
    expected_gfm = (
        """<h2>look at <a href="http://www.google.com">http://www.google.com</a></h2>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_28():
    """
    Test case extra 28:  SetExt heading string ending with an email autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """for more information, contact <foo@bar.com>
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):for more information, contact :]",
        "[email-autolink(1,31):foo@bar.com]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>for more information, contact <a href="mailto:foo@bar.com">foo@bar.com</a></h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_29():
    """
    Test case extra 29:  SetExt heading string ending with an emphasis
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """it's *me*
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):it's :]",
        "[emphasis(1,6):1:*]",
        "[text(1,7):me:]",
        "[end-emphasis(1,9)::1:*:False]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>it's <em>me</em></h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_30():
    """
    Test case extra 30:  SetExt heading string ending with a link.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a link looks like [Foo](/uri)
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):a link looks like :]",
        "[link(1,19):inline:/uri:::::Foo:False::::]",
        "[text(1,20):Foo:]",
        "[end-link:::False]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>a link looks like <a href="/uri">Foo</a></h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_31():
    """
    Test case extra 31:  SetExt heading string ending with an image
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """an image is ![foo](/url "title")
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):an image is :]",
        '[image(1,13):inline:/url:title:foo::::foo:False:":: :]',
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>an image is <img src="/url" alt="foo" title="title" /></h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_32():
    """
    Test case extra 32:  SetExt heading this is only a backslash escape
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\\\
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\\\b\\:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>\\</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_33():
    """
    Test case extra 33:  SetExt heading this is only a backslash as in a hard line break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ \\
---"""
    expected_tokens = [
        "[setext(2,1):-:3: :(1,2)]",
        "[text(1,2):\\:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>\\</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_34():
    """
    Test case extra 34:  SetExt heading this is only 2+ spaces as in a hard line break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\a\a\a\a
---""".replace(
        "\a", " "
    )
    expected_tokens = ["[BLANK(1,1):    ]", "[tbreak(2,1):-::---]"]
    expected_gfm = """<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_35():
    """
    Test case extra 35:  SetExt heading this is only a code span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """``day``
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[icode-span(1,1):day:``::]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2><code>day</code></h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_36():
    """
    Test case extra 36:  SetExt heading this is only a character reference.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """&amp;
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\a&amp;\a\a&\a&amp;\a\a:]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2>&amp;</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_37():
    """
    Test case extra 37:  SetExt heading this is only a raw html block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<there it='is'>
---"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<there it='is'>\n---:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<there it='is'>\n---"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_38():
    """
    Test case extra 38:  SetExt heading this is only an URI autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<http://www.google.com>
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[uri-autolink(1,1):http://www.google.com]",
        "[end-setext:::False]",
    ]
    expected_gfm = (
        """<h2><a href="http://www.google.com">http://www.google.com</a></h2>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_39():
    """
    Test case extra 39:  SetExt heading this is only an email autolink
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<foo@bar.com>
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[email-autolink(1,1):foo@bar.com]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2><a href="mailto:foo@bar.com">foo@bar.com</a></h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_40():
    """
    Test case extra 40:  SetExt heading this is only an emphasis
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*me*
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):me:]",
        "[end-emphasis(1,4)::1:*:False]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2><em>me</em></h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_41():
    """
    Test case extra 41:  SetExt heading this is only a link.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[Foo](/uri)
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[link(1,1):inline:/uri:::::Foo:False::::]",
        "[text(1,2):Foo:]",
        "[end-link:::False]",
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2><a href="/uri">Foo</a></h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_setext_headings_extra_42():
    """
    Test case extra 42:  SetExt heading this is only an image
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![foo](/url "title")
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        '[image(1,1):inline:/url:title:foo::::foo:False:":: :]',
        "[end-setext:::False]",
    ]
    expected_gfm = """<h2><img src="/url" alt="foo" title="title" /></h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
