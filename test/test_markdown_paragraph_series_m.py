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
def test_paragraph_series_m_ol_nl_tb():
    """
    Test case:  Ordered list newline thematic break
    was:        test_list_blocks_256fx
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[tbreak(2,1):-::---]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i2_tb():
    """
    Test case:  Ordered list new line indent of 2 thematic break
    was:        test_list_blocks_256fxa
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[tbreak(2,3):-:  :---]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_tb():
    """
    Test case:  Ordered list new line indent of 3 thematic break
    Test case:  Ordered list thematic break on next line after an indent of 3
    was:        test_list_blocks_256fxb
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[tbreak(2,4):-::---]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<hr />
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_tb():
    """
    Test case:  Ordered list text new line thematic break
    was:        test_list_blocks_256fa
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(2,1):-::---]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i2_tb():
    """
    Test case:  Ordered list text newline indent of 2 thematic break
    was:        test_list_blocks_256faa
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(2,3):-:  :---]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_tb():
    """
    Test case:  Ordered list text newline indent of 2 thematic break
    was:        test_list_blocks_256fab
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[setext(2,4):-:3::(1,4)]",
        "[text(1,4):abc:]",
        "[end-setext:::False]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>abc</h2>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_ol_nl_tb():
    """
    Test case:  Ordered list x2 new line thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. 1.
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(2,1):-::---]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_ol_t_nl_tb():
    """
    Test case:  Ordered list x2 text new line thematic break
    was:        test_list_blocks_256fb
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. 1. abc
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(2,1):-::---]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_ol_nl_tb():
    """
    Test case:  Ordered list newline ordered list new line thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_ol_nl_tb():
    """
    Test case:  Ordered list text newline ordered list new line thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_ol_t_nl_tb():
    """
    Test case:  Ordered list newline ordered list text new line thematic break
    was:        test_list_blocks_256fc
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. abc
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_ol_t_nl_tb():
    """
    Test case:  Ordered list text newline ordered list text new line thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. abc
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_ol_nl_i2_tb():
    """
    Test case:  Ordered list newline ordered list new line indent of 2 thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,3):-:  :---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_ol_nl_i2_tb():
    """
    Test case:  Ordered list text newline ordered list new line indent of 2 thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,3):-:  :---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_ol_t_nl_i2_tb():
    """
    Test case:  Ordered list newline ordered list text new line indent of 2 thematic break
    was:        test_list_blocks_256fd
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. abc
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,3):-:  :---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_ol_t_nl_i2_tb():
    """
    Test case:  Ordered list text newline ordered list text new line indent of 2 thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. abc
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,3):-:  :---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_ol_t_nl_i3_tb():
    """
    Test case:  Ordered list newline ordered list text new line indent of 3 thematic break
    was:        test_list_blocks_256fe
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. abc
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,4):-::---]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
<hr />
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_ol_t_nl_i3_tb():
    """
    Test case:  Ordered list text newline ordered list text new line indent of 3 thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. abc
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,4):-::---]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
<hr />
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_ol_nl_i3_tb():
    """
    Test case:  Ordered list newline ordered list new line indent of 3 thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[tbreak(3,4):-::---]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
<hr />
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_ol_nl_i3_tb():
    """
    Test case:  Ordered list text newline ordered list new line indent of 3 thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[tbreak(3,4):-::---]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>abc
1.</h2>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_ha_t():
    """
    Test case:  Ordered list newline atx heading text
    was:        test_list_blocks_256g
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[atx(2,1):1:0:]",
        "[text(2,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i2_ha_t():
    """
    Test case:  Ordered list newline indent of 2 atx heading text
    was:        test_list_blocks_256gxa
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
  # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[atx(2,3):1:0:  ]",
        "[text(2,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ha_t():
    """
    Test case:  Ordered list newline indent of 3 atx heading text
    was:        test_list_blocks_256gxb
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[atx(2,4):1:0:]",
        "[text(2,6):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h1>foo</h1>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_ha_t():
    """
    Test case:  Ordered list text newline atx heading text
    was:        test_list_blocks_256ga
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[atx(2,1):1:0:]",
        "[text(2,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i2_ha_t():
    """
    Test case:  Ordered list text newline indent of 2 atx heading text
    was:        test_list_blocks_256gaa
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
  # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[atx(2,3):1:0:  ]",
        "[text(2,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ha_t():
    """
    Test case:  Ordered list text newline indent of 3 atx heading text
    was:        test_list_blocks_256gab
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[atx(2,4):1:0:]",
        "[text(2,6):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<h1>foo</h1>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_ol_nl_ha_t():
    """
    Test case:  Ordered list x2 newline atx heading text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. 1.
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[atx(2,1):1:0:]",
        "[text(2,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_ol_t_nl_ha_t():
    """
    Test case:  Ordered list x2 text newline atx heading text
    was:        test_list_blocks_256gb
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. 1. abc
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[atx(2,1):1:0:]",
        "[text(2,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_ol_nl_ha_t():
    """
    Test case:  Ordered list newline ordered list new line atx heading text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[atx(3,1):1:0:]",
        "[text(3,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_ol_nl_ha_t():
    """
    Test case:  Ordered list text newline ordered list new line atx heading text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[atx(3,1):1:0:]",
        "[text(3,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_ol_t_nl_ha_t():
    """
    Test case:  Ordered list newline ordered list text new line atx heading text
    was:        test_list_blocks_256gc
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. abc
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[atx(3,1):1:0:]",
        "[text(3,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_ol_t_nl_ha_t():
    """
    Test case:  Ordered list text newline ordered list text new line atx heading text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. abc
# foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[atx(3,1):1:0:]",
        "[text(3,3):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_ol_nl_i2_ha_t():
    """
    Test case:  Ordered list newline ordered list new line indent of 2 atx heading text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
  # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[atx(3,3):1:0:  ]",
        "[text(3,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_ol_nl_i2_ha_t():
    """
    Test case:  Ordered list text newline ordered list new line indent of 2 atx heading text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
  # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[atx(3,3):1:0:]",
        "[text(3,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """
<ol>
<li>abc
1.</li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_ol_t_nl_i2_ha_t():
    """
    Test case:  Ordered list newline ordered list text new line indent of 2 atx heading text
    was:        test_list_blocks_256gd
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. abc
  # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[atx(3,3):1:0:  ]",
        "[text(3,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_ol_t_nl_i2_ha_t():
    """
    Test case:  Ordered list text newline ordered list text new line indent of 2 atx heading text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. abc
  # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[atx(3,3):1:0:  ]",
        "[text(3,5):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_ol_nl_i3_ha_t():
    """
    Test case:  Ordered list newline ordered list new line indent of 3 atx heading text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
   # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[atx(3,4):1:0:]",
        "[text(3,6):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
<h1>foo</h1>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_ol_nl_i3_ha_t():
    """
    Test case:  Ordered list text newline ordered list new line indent of 3 atx heading text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
   # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[atx(3,4):1:0:]",
        "[text(3,6):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
<h1>foo</h1>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_ol_t_nl_i3_ha_t():
    """
    Test case:  Ordered list newline ordered list text new line indent of 3 atx heading text
    was:        test_list_blocks_256ge
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. abc
   # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[atx(3,4):1:0:]",
        "[text(3,6):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
<h1>foo</h1>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_ol_t_nl_i3_ha_t():
    """
    Test case:  Ordered list text newline ordered list text new line indent of 3 atx heading text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. abc
   # foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[atx(3,4):1:0:]",
        "[text(3,6):foo: ]",
        "[end-atx:::False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
<h1>foo</h1>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_t_nl_hs():
    """
    Test case:  Ordered list newline text new line setext heading
    was:        test_list_blocks_256hx
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[setext(3,1):-:3::(2,1)]",
        "[text(2,1):foo:]",
        "[end-setext:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<h2>foo</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i2_t_nl_hs():
    """
    Test case:  Ordered list newline indent of 2 text new line setext heading
    was:        test_list_blocks_256hxa
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
  foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[setext(3,1):-:3:  :(2,3)]",
        "[text(2,3):foo:]",
        "[end-setext:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<h2>foo</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_t_nl_hs():
    """
    Test case:  Ordered list newline indent of 3 text new line setext heading
    was:        test_list_blocks_256hxb
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[para(2,4):]",
        "[text(2,4):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_t_nl_i3_hs():
    """
    Test case:  Ordered list newline indent of 3 text new line indent of 3 setext heading
    was:        test_list_blocks_256hxc
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[BLANK(1,3):]",
        "[setext(3,4):-:3::(2,4)]",
        "[text(2,4):foo:]",
        "[end-setext:::False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>foo</h2>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_t_nl_hs():
    """
    Test case:  Ordered list text newline text new line setext heading
    was:        test_list_blocks_256ha
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n]",
        "[text(1,4):abc\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
foo</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i2_t_nl_hs():
    """
    Test case:  Ordered list text newline indent of 2 text new line setext heading
    was:        test_list_blocks_256haa
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
  foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
foo</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_t_nl_hs():
    """
    Test case:  Ordered list text newline indent of 3 text new line setext heading
    was:        test_list_blocks_256hab
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
foo</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_t_nl_i3_hs():
    """
    Test case:  Ordered list text newline indent of 3 text new line indent of 3 setext heading
    was:        test_list_blocks_256hac
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[setext(3,4):-:3::(1,4)]",
        "[text(1,4):abc\nfoo::\n]",
        "[end-setext:::False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>abc
foo</h2>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_ol_nl_t_nl_hs():
    """
    Test case:  Ordered list x2 text newline new line setext heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. 1. abc
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :]",
        "[para(1,7):\n]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_ol_t_nl_t_nl_hs():
    """
    Test case:  Ordered list x2 text newline text new line setext heading
    was:        test_list_blocks_256hb
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. 1. abc
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :]",
        "[para(1,7):\n]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(3,1):-::---]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_nl_t_nl_hs():
    """
    Test case:  Ordered list newline indent of 3 ordered list new line text newline setext heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[setext(4,1):-:3::(3,1)]",
        "[text(3,1):foo:]",
        "[end-setext:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<h2>foo</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_nl_t_nl_hs():
    """
    Test case:  Ordered list text newline indent of 3 ordered list new line text newline setext heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[para(3,1):]",
        "[text(3,1):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
foo</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_t_nl_t_nl_hs():
    """
    Test case:  Ordered list newline indent of 3 ordered list text new line text newline setext heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. def
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_t_nl_t_nl_hs():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text new line text newline setext heading
    was:        test_list_blocks_256hc
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. def
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_nl_i2_t_nl_i2_hs():
    """
    Test case:  Ordered list newline indent of 3 ordered list new line indent of 2 text newline indent of 2 setext heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
  foo
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[setext(4,3):-:3:  :(3,3)]",
        "[text(3,3):foo:]",
        "[end-setext:  ::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<h2>foo</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_nl_i2_t_nl_i2_hs():
    """
    Test case:  Ordered list text newline indent of 3 ordered list new line indent of 2 text newline indent of 2 setext heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
  foo
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[para(3,3):]",
        "[text(3,3):foo:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(4,3):-:  :---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
foo</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_t_nl_i2_t_nl_i2_hs():
    """
    Test case:  Ordered list newline indent of 3 ordered list text new line indent of 2 text newline indent of 2 setext heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. def
  foo
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :  ]",
        "[para(2,7):\n]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(4,3):-:  :---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_t_nl_i2_t_nl_i2_hs():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text new line indent of 2 text newline indent of 2 setext heading
    was:        test_list_blocks_256hd
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. def
  foo
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :  ]",
        "[para(2,7):\n]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(4,3):-:  :---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_nl_i3_t_nl_i3_hs():
    """
    Test case:  Ordered list newline indent of 3 ordered list new line indent of 3 text newline indent of 3 setext heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[setext(4,4):-:3::(3,4)]",
        "[text(3,4):foo:]",
        "[end-setext:::False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
<h2>foo</h2>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_nl_i3_t_nl_i3_hs():
    """
    Test case:  Ordered list text newline indent of 3 ordered list new line indent of 3 text newline indent of 3 setext heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[setext(4,4):-:3::(3,4)]",
        "[text(3,4):foo:]",
        "[end-setext:::False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>abc
1.
foo</h2>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_t_nl_i3_t_nl_i3_hs():
    """
    Test case:  Ordered list newline indent of 3 ordered list text new line indent of 3 text newline indent of 3 setext heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. def
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :   ]",
        "[para(2,7):\n]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(4,4):-::---]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def
foo</li>
</ol>
<hr />
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_t_nl_i3_t_nl_i3_hs():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text new line indent of 3 text newline indent of 3 setext heading
    was:        test_list_blocks_256he
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. def
   foo
   ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :   ]",
        "[para(2,7):\n]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(4,4):-::---]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
foo</li>
</ol>
<hr />
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_fb():
    """
    Test case:  Ordered list newline fenced block
    was:        test_list_blocks_256jx
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[fcode-block(2,1):`:3::::::]",
        "[text(3,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i2_fb():
    """
    Test case:  Ordered list newline indent of 2 fenced block
    was:        test_list_blocks_256jxa
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
  ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[fcode-block(2,3):`:3:::::  :]",
        "[text(3,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_fb():
    """
    Test case:  Ordered list newline indent of 2 fenced block
    was:        test_list_blocks_256jxb
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[fcode-block(2,4):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-olist:::True]",
        "[para(3,1):]",
        "[text(3,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(4,1):`:3::::::]",
        "[BLANK(5,1):]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code></code></pre>
</li>
</ol>
<p>foo</p>
<pre><code></code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_fb():
    """
    Test case:  Ordered list text newline fenced block
    was:        test_list_blocks_256ja
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.  abc
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:4:]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(2,1):`:3::::::]",
        "[text(3,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i2_fb():
    """
    Test case:  Ordered list text newline indent of 2 fenced block
    was:        test_list_blocks_256jaa
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.  abc
  ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:4:]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(2,3):`:3:::::  :]",
        "[text(3,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_fb():
    """
    Test case:  Ordered list text newline indent of 3 fenced block
    was:        test_list_blocks_256jab
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.  abc
   ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:4:]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(2,4):`:3:::::   :]",
        "[text(3,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_ol_nl_fb():
    """
    Test case:  Ordered list x2 newline fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. 1.
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(2,1):`:3::::::]",
        "[text(3,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_ol_t_nl_fb():
    """
    Test case:  Ordered list x2 text newline fenced block
    was:        test_list_blocks_256jb
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. 1. abc
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(2,1):`:3::::::]",
        "[text(3,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_nl_fb():
    """
    Test case:  Ordered list newline indent of 3 ordered list newline fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,1):`:3::::::]",
        "[text(4,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_nl_fb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[fcode-block(3,1):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(5,1):`:3::::::]",
        "[BLANK(6,1):]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_t_nl_fb():
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline fenced block
    was:        test_list_blocks_256jc
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. abc
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,1):`:3::::::]",
        "[text(4,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_t_nl_fb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. abc
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,1):`:3::::::]",
        "[text(4,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_nl_i2_fb():
    """
    Test case:  Ordered list newline indent of 3 ordered list newline indent of 2 fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
  ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,3):`:3:::::  :]",
        "[text(4,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_nl_i2_fb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline indent of 2 fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
  ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[fcode-block(3,3):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(5,1):`:3::::::]",
        "[BLANK(6,1):]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_t_nl_i2_fb():
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline indent of 2 fenced block
    was:        test_list_blocks_256jd
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. abc
  ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,3):`:3:::::  :]",
        "[text(4,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_t_nl_i2_fb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline indent of 2 fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. abc
  ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,3):`:3:::::  :]",
        "[text(4,1):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_nl_i3_fb():
    """
    Test case:  Ordered list newline indent of 3 ordered list newline indent of 3 fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
   ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[fcode-block(3,4):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(5,1):`:3::::::]",
        "[BLANK(6,1):]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
<pre><code></code></pre>
</li>
</ol>
<p>foo</p>
<pre><code></code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown, show_debug=True)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_nl_i3_fb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline indent of 3 fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
   ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[fcode-block(3,4):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(5,1):`:3::::::]",
        "[BLANK(6,1):]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
<pre><code></code></pre>
</li>
</ol>
<p>foo</p>
<pre><code></code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_t_nl_i3_fb():
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline indent of 3 fenced block
    was:        test_list_blocks_256je
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. abc
   ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[fcode-block(3,4):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(5,1):`:3::::::]",
        "[BLANK(6,1):]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
<pre><code></code></pre>
</li>
</ol>
<p>foo</p>
<pre><code></code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_t_nl_i3_fb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline indent of 3 fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. abc
   ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[fcode-block(3,4):`:3::::::]",
        "[end-fcode-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(5,1):`:3::::::]",
        "[BLANK(6,1):]",
        "[end-fcode-block:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
<pre><code></code></pre>
</li>
</ol>
<p>foo</p>
<pre><code></code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_i3_ol_nl_i4_t_ib():
    """
    Test case:  Indent of 3 ordered list newline indent of 4 text (indented block)
    was:        test_list_blocks_256ix
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   1.
    foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[icode-block(2,5):    :]",
        "[text(2,5):foo:]",
        "[end-icode-block:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_i3_ol_nl_i5_t_ib():
    """
    Test case:  Indent of 3 ordered list newline indent of 5 text (indented block)
    was:        test_list_blocks_256ixa
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   1.
     foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[icode-block(2,5):    :]",
        "[text(2,5):foo: ]",
        "[end-icode-block:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<pre><code> foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_i3_ol_nl_i6_t_fb():
    """
    Test case:  Indent of 3 ordered list newline indent of 6 text (indented block)
    was:        test_list_blocks_256ixb
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   1.
      foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[BLANK(1,6):]",
        "[para(2,7):]",
        "[text(2,7):foo:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_i3_ol_t_nl_i4_t_ib():
    """
    Test case:  Indent of 3 ordered list text newline indent of 4 text (indented block)
    was:        test_list_blocks_256ia
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :    ]",
        "[para(1,7):\n]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
foo</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_i3_ol_t_nl_i5_t_ib():
    """
    Test case:  Indent of 3 ordered list text newline indent of 5 text (indented block)
    was:        test_list_blocks_256iaa
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   1. abc
     foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :     ]",
        "[para(1,7):\n]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
foo</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_i3_ol_t_nl_i6_t_ib():
    """
    Test case:  Indent of 3 ordered list text newline indent of 6 text (indented block)
    was:        test_list_blocks_256iab
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   1. abc
      foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   :      ]",
        "[para(1,7):\n]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
foo</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_ol_nl_i4_t_ib():
    """
    Test case:  Ordered list x2 newline indent of 4 text (indented block)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. 1.
    foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[para(2,5): ]",
        "[text(2,5):foo:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
foo</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_ol_t_nl_i4_t_ib():
    """
    Test case:  Ordered list x2 text newline indent of 4 text (indented block)
    was:        test_list_blocks_256ib
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. 1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :    ]",
        "[para(1,7):\n]",
        "[text(1,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_nl_i4_t_ib():
    """
    Test case:  Ordered list newline indent of 3 ordered list newline indent of 4 text (indented block)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
    foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[para(3,5): ]",
        "[text(3,5):foo:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
foo</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_nl_i4_t_ib():
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline indent of 4 text (indented block)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
    foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[para(3,5):]",
        "[text(3,5):foo:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
foo</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_t_nl_i4_t_ib():
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline indent of 4 text (indented block)
    was:        test_list_blocks_256ic
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :    ]",
        "[para(2,7):\n]",
        "[text(2,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_t_nl_i4_t_ib():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline indent of 4 text (indented block)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :    ]",
        "[para(2,7):\n]",
        "[text(2,7):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_i3_ol_nl_i5_ol_nl_i4_t_ib():
    """
    Test case:  Indent of 3 ordered list newline indent of 5 ordered list newline indent of 4 text (indented block)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   1.
      1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[olist(2,7):.:1:9:      :    ]",
        "[para(2,10):\n]",
        "[text(2,10):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_i3_ol_t_nl_i5_ol_nl_i4_t_ib():
    """
    Test case:  Indent of 3 ordered list text newline indent of 5 ordered list newline indent of 4 text (indented block)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   1. abc
      1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[olist(2,7):.:1:9:      :    ]",
        "[para(2,10):\n]",
        "[text(2,10):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_i3_ol_nl_i5_ol_t_nl_i4__t_ib():
    """
    Test case:  Indent of 3 ordered list newline indent of 5 ordered list text newline indent of 4 text (indented block)
    was:        test_list_blocks_256id
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   1.
      1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[olist(2,7):.:1:9:      :    ]",
        "[para(2,10):\n]",
        "[text(2,10):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_i3_ol_t_nl_i5_ol_t_nl_i4_t_ib():
    """
    Test case:  Indent of 3 ordered list text newline indent of 5 ordered list text newline indent of 4 text (indented block)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   1. abc
      1. abc
    foo
"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[olist(2,7):.:1:9:      :    ]",
        "[para(2,10):\n]",
        "[text(2,10):abc\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc
foo</li>
</ol>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_i1_ol_nl_i4_ol_nl_i4_t_ib():
    """
    Test case:  Indent of 1 ordered list newline indent of 4 ordered list newline indent of 4 text (indented block)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ 1. abc
    1.
    foo
"""
    expected_tokens = [
        "[olist(1,2):.:1:4: :    ]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[olist(2,5):.:1:7:    ]",
        "[BLANK(2,7):]",
        "[end-olist:::True]",
        "[para(3,5):]",
        "[text(3,5):foo:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
foo</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_i1_ol_t_nl_i4_ol_nl_i4_t_ib():
    """
    Test case:  Indent of 1 ordered list text newline indent of 4 ordered list newline indent of 4 text (indented block)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ 1. abc
    1.
    foo
"""
    expected_tokens = [
        "[olist(1,2):.:1:4: :    ]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[olist(2,5):.:1:7:    ]",
        "[BLANK(2,7):]",
        "[end-olist:::True]",
        "[para(3,5):]",
        "[text(3,5):foo:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
foo</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_i1_ol_nl_i4_ol_t_nl_i4_t_ib():
    """
    Test case:  Indent of 1 ordered list newline indent of 4 ordered list text newline indent of 4 text (indented block)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ 1.
    1. def
    foo
"""
    expected_tokens = [
        "[olist(1,2):.:1:4: ]",
        "[BLANK(1,4):]",
        "[olist(2,5):.:1:7:    :    ]",
        "[para(2,8):\n]",
        "[text(2,8):def\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_i1_ol_t_nl_i4_ol_t_nl_i4_t_ib():
    """
    Test case:  Indent of 1 ordered list text newline indent of 4 ordered list text newline indent of 4 text (indented block)
    was:        test_list_blocks_256ie
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ 1. abc
    1. def
    foo
"""
    expected_tokens = [
        "[olist(1,2):.:1:4: ]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[olist(2,5):.:1:7:    :    ]",
        "[para(2,8):\n]",
        "[text(2,8):def\nfoo::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_hb():
    """
    Test case:  Ordered list newline html block
    was:        test_list_blocks_256k
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[html-block(2,1)]",
        "[text(2,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i2_hb():
    """
    Test case:  Ordered list newline indent of 2 html block
    was:        test_list_blocks_256kxa
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
  <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[html-block(2,1)]",
        "[text(2,3):<script>\nfoo\n</script>:  ]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
  <script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_hb():
    """
    Test case:  Ordered list newline indent of 3 html block
    was:        test_list_blocks_256kxb
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[html-block(2,4)]",
        "[text(2,4):<script>:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[para(3,1):\n]",
        "[text(3,1):foo\n::\n]",
        "[raw-html(4,1):/script]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<script>
</li>
</ol>
<p>foo
</script></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_hb():
    """
    Test case:  Ordered list text newline html block
    was:        test_list_blocks_256ka
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.  abc
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:4:]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[html-block(2,1)]",
        "[text(2,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_hb():
    """
    Test case:  Ordered list text newline indent of 3 html block
    was:        test_list_blocks_256kaa
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.  abc
   <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:4:]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[html-block(2,1)]",
        "[text(2,4):<script>\nfoo\n</script>:   ]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
   <script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i4_hb():
    """
    Test case:  Ordered list text newline indent of 4 html block
    was:        test_list_blocks_256kab
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.  abc
    <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:4::    ]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::False]",
        "[html-block(2,5)]",
        "[text(2,5):<script>:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[para(3,1):\n]",
        "[text(3,1):foo\n::\n]",
        "[raw-html(4,1):/script]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<script>
</li>
</ol>
<p>foo
</script></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_ol_nl_hb():
    """
    Test case:  Ordered list x2 newline html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. 1.
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(2,1)]",
        "[text(2,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_ol_t_nl_hb():
    """
    Test case:  Ordered list x2 text newline html block
    was:        test_list_blocks_256kb
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. 1. abc
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(2,1)]",
        "[text(2,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_nl_hb():
    """
    Test case:  Ordered list newline indent of 3 ordered list newline html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_nl_hb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
<script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_t_nl_hb():
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. def
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def</li>
</ol>
</li>
</ol>
<script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_t_nl_hb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline html block
    was:        test_list_blocks_256kc
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. def
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
</li>
</ol>
<script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_nl_i2_hb():
    """
    Test case:  Ordered list newline indent of 3 ordered list newline indent of 2 html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
  <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,3):<script>\nfoo\n</script>:  ]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
  <script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_nl_i2_hb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline indent of 2 html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
  <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[html-block(3,3)]",
        "[text(3,3):<script>:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):\n]",
        "[text(4,1):foo\n::\n]",
        "[raw-html(5,1):/script]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
  <script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_t_nl_i2_hb():
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline indent of 2 html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. def
  <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,3):<script>\nfoo\n</script>:  ]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def</li>
</ol>
</li>
</ol>
  <script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_t_nl_i2_hb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline indent of 2 html block
    was:        test_list_blocks_256kd
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. def
  <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,3):<script>\nfoo\n</script>:  ]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
</li>
</ol>
  <script>
foo
</script>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_nl_i3_hb():
    """
    Test case:  Ordered list newline indent of 3 ordered list newline indent of 2 html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1.
   <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[html-block(3,4)]",
        "[text(3,4):<script>:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):\n]",
        "[text(4,1):foo\n::\n]",
        "[raw-html(5,1):/script]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
<script>
</li>
</ol>
<p>foo
</script></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_nl_i3_hb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline indent of 2 html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1.
   <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[html-block(3,4)]",
        "[text(3,4):<script>:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):\n]",
        "[text(4,1):foo\n::\n]",
        "[raw-html(5,1):/script]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
<script>
</li>
</ol>
<p>foo
</script></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_nl_i3_ol_t_nl_i3_hb():
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline indent of 2 html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1.
   1. def
   <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,4)]",
        "[text(3,4):<script>:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):\n]",
        "[text(4,1):foo\n::\n]",
        "[raw-html(5,1):/script]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def</li>
</ol>
<script>
</li>
</ol>
<p>foo
</script></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_ol_t_nl_i3_ol_t_nl_i3_hb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline indent of 2 html block
    was:        test_list_blocks_256ke
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """1. abc
   1. def
   <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,4)]",
        "[text(3,4):<script>:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):\n]",
        "[text(4,1):foo\n::\n]",
        "[raw-html(5,1):/script]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<script>
</li>
</ol>
<p>foo
</script></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
