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


@pytest.mark.gfm
def test_paragraph_series_h_f_l_t():
    """
    Test case:  Paragraph with full link label text split over 2 lines
    was:        test_paragraph_extra_a6
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a[li
nk][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:li\nnk:::::]",
        "[text(1,3):li\nnk::\n]",
        "[end-link:::False]",
        "[text(2,9):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">li\nnk</a>a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_f_i_t():
    """
    Test case:  Paragraph with full image label text split over 2 lines
    was:        test_paragraph_extra_b8
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a![li
nk][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:li\nnk:::bar:li\nnk:::::]",
        "[text(2,9):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="li\nnk" title="title" />a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_f_l_cs():
    """
    Test case:  Paragraph with full link label code span split over 2 lines
    was:        test_paragraph_extra_a7
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a[li`de
fg`nk][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:li`de\a\n\a \afg`nk:::::]",
        "[text(1,3):li:]",
        "[icode-span(1,5):de\a\n\a \afg:`::]",
        "[text(2,4):nk:]",
        "[end-link:::False]",
        "[text(2,12):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = (
        """<p>a<a href="/url" title="title">li<code>de fg</code>nk</a>a</p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_f_i_cs():
    """
    Test case:  Paragraph with full image label code span split over 2 lines
    was:        test_paragraph_extra_b9
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a![li`de
fg`nk][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:lide fgnk:::bar:li`de\a\n\a \afg`nk:::::]",
        "[text(2,12):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="lide fgnk" title="title" />a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_f_l_rh():
    """
    Test case:  Paragraph with full link label raw html split over 2 lines
    was:        test_paragraph_extra_a8
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a[li<de
fg>nk][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):full:/url:title:::bar:li<de\nfg>nk:::::]",
        "[text(1,3):li:]",
        "[raw-html(1,5):de\nfg]",
        "[text(2,4):nk:]",
        "[end-link:::False]",
        "[text(2,12):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">li<de\nfg>nk</a>a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_f_i_rh():
    """
    Test case:  Paragraph with full image label raw html split over 2 lines
    was:        test_paragraph_extra_c0
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a![li<de
fg>nk][bar]a

[bar]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):full:/url:title:li<de\nfg>nk:::bar:li<de\nfg>nk:::::]",
        "[text(2,12):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="li<de\nfg>nk" title="title" />a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_c_l_t():
    """
    Test case:  Paragraph with collapsed link label text split over 2 lines
    was:        test_paragraph_extra_a9
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a[li
nk][]a

[li\nnk]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::li\nnk:::::]",
        "[text(1,3):li\nnk::\n]",
        "[end-link:::False]",
        "[text(2,6):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::li nk:li\nnk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">li\nnk</a>a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_c_i_t():
    """
    Test case:  Paragraph with collapsed image label text split over 2 lines
    was:        test_paragraph_extra_c1
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a![li
nk][]a

[li\nnk]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:li\nnk::::li\nnk:::::]",
        "[text(2,6):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::li nk:li\nnk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="li\nnk" title="title" />a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_c_l_cs():
    """
    Test case:  Paragraph with collapsed link label code span split over 2 lines
    was:        test_paragraph_extra_b0
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a[li`de
fg`nk][]a

[li`de\nfg`nk]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::li`de\a\n\a \afg`nk:::::]",
        "[text(1,3):li:]",
        "[icode-span(1,5):de\a\n\a \afg:`::]",
        "[text(2,4):nk:]",
        "[end-link:::False]",
        "[text(2,9):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::li`de fg`nk:li`de\nfg`nk: :/url:: :title:'title':]",
    ]
    expected_gfm = (
        """<p>a<a href="/url" title="title">li<code>de fg</code>nk</a>a</p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_c_i_cs():
    """
    Test case:  Paragraph with collapsed image label code span split over 2 lines
    was:        test_paragraph_extra_c2
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a![li`de
fg`nk][]a

[li`de\nfg`nk]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:lide fgnk::::li`de\a\n\a \afg`nk:::::]",
        "[text(2,9):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::li`de fg`nk:li`de\nfg`nk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="lide fgnk" title="title" />a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_c_l_rh():
    """
    Test case:  Paragraph with collapsed link label raw html split over 2 lines
    was:        test_paragraph_extra_b1
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a[li<de
fg>nk][]a

[li<de\nfg>nk]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):collapsed:/url:title::::li<de\nfg>nk:::::]",
        "[text(1,3):li:]",
        "[raw-html(1,5):de\nfg]",
        "[text(2,4):nk:]",
        "[end-link:::False]",
        "[text(2,9):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::li<de fg>nk:li<de\nfg>nk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">li<de\nfg>nk</a>a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_c_i_rh():
    """
    Test case:  Paragraph with collapsed image label raw html split over 2 lines
    was:        test_paragraph_extra_c3
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a![li<de
fg>nk][]a

[li<de\nfg>nk]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):collapsed:/url:title:li<de\nfg>nk::::li<de\nfg>nk:::::]",
        "[text(2,9):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::li<de fg>nk:li<de\nfg>nk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="li<de\nfg>nk" title="title" />a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_s_l_t():
    """
    Test case:  Paragraph with shortcut link label text split over 2 lines
    was:        test_paragraph_extra_b2
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a[li
nk]a

[li\nnk]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::li\nnk:::::]",
        "[text(1,3):li\nnk::\n]",
        "[end-link:::False]",
        "[text(2,4):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::li nk:li\nnk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">li\nnk</a>a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_s_i_t():
    """
    Test case:  Paragraph with shortcut image label text split over 2 lines
    was:        test_paragraph_extra_c4
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a![li
nk]a

[li\nnk]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:li\nnk::::li\nnk:::::]",
        "[text(2,4):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::li nk:li\nnk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="li\nnk" title="title" />a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_s_l_cs():
    """
    Test case:  Paragraph with shortcut link label code span split over 2 lines
    was:        test_paragraph_extra_b3
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a[li`de
fg`nk]a

[li`de\nfg`nk]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::li`de\a\n\a \afg`nk:::::]",
        "[text(1,3):li:]",
        "[icode-span(1,5):de\a\n\a \afg:`::]",
        "[text(2,4):nk:]",
        "[end-link:::False]",
        "[text(2,7):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::li`de fg`nk:li`de\nfg`nk: :/url:: :title:'title':]",
    ]
    expected_gfm = (
        """<p>a<a href="/url" title="title">li<code>de fg</code>nk</a>a</p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_s_i_cs():
    """
    Test case:  Paragraph with shortcut image label code span split over 2 lines
    was:        test_paragraph_extra_c5
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a![li`de
fg`nk]a

[li`de\nfg`nk]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:lide fgnk::::li`de\a\n\a \afg`nk:::::]",
        "[text(2,7):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::li`de fg`nk:li`de\nfg`nk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="lide fgnk" title="title" />a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_s_l_rh():
    """
    Test case:  Paragraph with shortcut link label raw html split over 2 lines
    was:        test_paragraph_extra_b4
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a[li<de
fg>nk]a

[li<de\nfg>nk]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[link(1,2):shortcut:/url:title::::li<de\nfg>nk:::::]",
        "[text(1,3):li:]",
        "[raw-html(1,5):de\nfg]",
        "[text(2,4):nk:]",
        "[end-link:::False]",
        "[text(2,7):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::li<de fg>nk:li<de\nfg>nk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<a href="/url" title="title">li<de\nfg>nk</a>a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_s_i_rh():
    """
    Test case:  Paragraph with shortcut image label raw html split over 2 lines
    was:        test_paragraph_extra_c6
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a![li<de
fg>nk]a

[li<de\nfg>nk]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        "[image(1,2):shortcut:/url:title:li<de\nfg>nk::::li<de\nfg>nk:::::]",
        "[text(2,7):a:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::li<de fg>nk:li<de\nfg>nk: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p>a<img src="/url" alt="li<de\nfg>nk" title="title" />a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_i_l_t():
    """
    Test case:  Paragraph with inline link label text split over 2 lines
    was:        test_paragraph_extra_a3
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a[li
nk](/uri "title" )a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:title::::li\nnk:False:":: : ]',
        "[text(1,3):li\nnk::\n]",
        "[end-link:::False]",
        "[text(2,19):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="title">li\nnk</a>a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_i_i_t():
    """
    Test case:  Paragraph with inline image label text split over 2 lines
    was:        test_paragraph_extra_b5
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a![li\nnk](/uri "title" )a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:title:li\nnk::::li\nnk:False:":: : ]',
        "[text(2,19):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="li\nnk" title="title" />a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_i_l_cs():
    """
    Test case:  Paragraph with inline link label code span split over 2 lines
    was:        test_paragraph_extra_a4
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a[li`de
fg`nk](/uri "title" )a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:title::::li`de\a\n\a \afg`nk:False:":: : ]',
        "[text(1,3):li:]",
        "[icode-span(1,5):de\a\n\a \afg:`::]",
        "[text(2,4):nk:]",
        "[end-link:::False]",
        "[text(2,22):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>a<a href="/uri" title="title">li<code>de fg</code>nk</a>a</p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_i_i_cs():
    """
    Test case:  Paragraph with inline image label code span split over 2 lines
    was:        test_paragraph_extra_b6
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a![li`de\nfg`nk](/uri "title" )a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:title:lide fgnk::::li`de\a\n\a \afg`nk:False:":: : ]',
        "[text(2,22):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="lide fgnk" title="title" />a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_i_l_rh():
    """
    Test case:  Paragraph with inline link label raw html split over 2 lines
    was:        test_paragraph_extra_a5
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a[li<de
fg>nk](/uri "title" )a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[link(1,2):inline:/uri:title::::li<de\nfg>nk:False:":: : ]',
        "[text(1,3):li:]",
        "[raw-html(1,5):de\nfg]",
        "[text(2,4):nk:]",
        "[end-link:::False]",
        "[text(2,22):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<a href="/uri" title="title">li<de\nfg>nk</a>a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_h_i_i_rh():
    """
    Test case:  Paragraph with inline image label raw html split over 2 lines
    was:        test_paragraph_extra_b7
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """a![li<de
fg>nk](/uri "title" )a"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a:]",
        '[image(1,2):inline:/uri:title:li<de\nfg>nk::::li<de\nfg>nk:False:":: : ]',
        "[text(2,22):a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a<img src="/uri" alt="li<de\nfg>nk" title="title" />a</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
