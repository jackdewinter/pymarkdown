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
def test_paragraph_series_n_bq_t_nl_bq_t():
    """
    Test case:  Block Quote with text, newline, block quote, text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw
> xyz"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):\n]",
        "[text(1,3):uvw\nxyz::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>uvw
xyz</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_bq_t_nl_i2_t():
    """
    Test case:  Block Quote with text, newline, indent of 2, text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw
  xyz"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):\n  ]",
        "[text(1,3):uvw\nxyz::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>uvw
xyz</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i2_bq_t():
    """
    Test case:  unordered list, text, newline, indent of 2, block Quote, text, newline,
                indent of 2, block quote, text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw
  > xyz
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > ]",
        "[para(2,5):\n]",
        "[text(2,5):uvw\nxyz::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>uvw
xyz</p>
</blockquote>
</li>
<li>def</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i4_t():
    """
    Test case:  unordered list, text, newline, indent of 2, block Quote, text, newline,
                indent of 4, text
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw
    xyz
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  ]",
        "[para(2,5):\n  ]",
        "[text(2,5):uvw\nxyz::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>uvw
xyz</p>
</blockquote>
</li>
<li>def</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_bq_t_nl_bq_ha():
    """
    Test case:  Block Quote with text, newline, block quote, atx heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw
> # head"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):]",
        "[text(1,3):uvw:]",
        "[end-para:::False]",
        "[atx(2,3):1:0:]",
        "[text(2,5):head: ]",
        "[end-atx:::False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>uvw</p>
<h1>head</h1>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_bq_t_nl_i2_ha():
    """
    Test case:  Block Quote with text, newline, proper indent for lazy, atx heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw
  # head"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):uvw:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[atx(2,3):1:0:  ]",
        "[text(2,5):head: ]",
        "[end-atx:::False]",
    ]
    expected_gfm = """<blockquote>
<p>uvw</p>
</blockquote>
<h1>head</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i2_bq_ha():
    """
    Test case:  Unordered list, text, newline, Indent of 2, Block Quote with text,
    newline, ident of 2, block quote, atx heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw
  > # head
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > ]",
        "[para(2,5):]",
        "[text(2,5):uvw:]",
        "[end-para:::False]",
        "[atx(3,5):1:0:]",
        "[text(3,7):head: ]",
        "[end-atx:::False]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>uvw</p>
<h1>head</h1>
</blockquote>
</li>
<li>def</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_i2_bq_t_nl_i4_ha():
    """
    Test case:  Unordered list, text, newline, Indent of 2, Block Quote with text,
    newline, ident of 4, atx heading
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw
    # head
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):uvw:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[atx(3,5):1:0:  ]",
        "[text(3,7):head: ]",
        "[end-atx:::False]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>uvw</p>
</blockquote>
<h1>head</h1>
</li>
<li>def</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_bq_t_nl_bq_tb():
    """
    Test case:  Block quote, text, newline, block quote, thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw
> ---"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[setext(2,3):-:3::(1,3)]",
        "[text(1,3):uvw:]",
        "[end-setext:::False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h2>uvw</h2>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_bq_t_nl_i2_tb():
    """
    Test case:  Block quote, text, newline, indent of 2, thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw
  ---"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):uvw:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[tbreak(2,3):-:  :---]",
    ]
    expected_gfm = """<blockquote>
<p>uvw</p>
</blockquote>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i2_bq_tb():
    """
    Test case:  Unordered list, text, newline, ident of 2, block quote, text, newline,
                indent of 2, block quote, thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw
  > ---
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > ]",
        "[setext(3,5):-:3::(2,5)]",
        "[text(2,5):uvw:]",
        "[end-setext:::False]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<h2>uvw</h2>
</blockquote>
</li>
<li>def</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i4_tb():
    """
    Test case:  Unordered list, text, newline, ident of 2, block quote, text, newline,
                indent of 4, thematic break
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw
    ---
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):uvw:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[tbreak(3,5):-:  :---]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>uvw</p>
</blockquote>
<hr />
</li>
<li>def</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_bq_t_nl_bq_hb():
    """
    Test case:  Block quote, text, newline, block quote, html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw
> <!-- comment -->"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):]",
        "[text(1,3):uvw:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,3):<!-- comment -->:]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>uvw</p>
<!-- comment -->
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_bq_t_nl_i2_hb():
    """
    Test case:  Block quote, text, newline, indent of 2, html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw
  <!-- comment -->"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):uvw:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[html-block(2,1)]",
        "[text(2,3):<!-- comment -->:  ]",
        "[end-html-block:::False]",
    ]
    expected_gfm = """<blockquote>
<p>uvw</p>
</blockquote>
  <!-- comment -->"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i2_bq_hb():
    """
    Test case:  Unordered list, text, newline, ident of 2, block quote, text, newline,
                indent of 2, block quote, html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw
  > <!-- comment -->
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > ]",
        "[para(2,5):]",
        "[text(2,5):uvw:]",
        "[end-para:::False]",
        "[html-block(3,5)]",
        "[text(3,5):<!-- comment -->:]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>uvw</p>
<!-- comment -->
</blockquote>
</li>
<li>def</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i4_hb():
    """
    Test case:  Unordered list, text, newline, ident of 2, block quote, text, newline,
                indent of 4, html block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw
    <!-- comment -->
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):uvw:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[html-block(3,3)]",
        "[text(3,5):<!-- comment -->:  ]",
        "[end-html-block:::False]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>uvw</p>
</blockquote>
  <!-- comment -->
</li>
<li>def</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_bq_t_nl_bq_fb():
    """
    Test case:  Block quote, text, newline, block quote, fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw
> ```
> def
> ```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):uvw:]",
        "[end-para:::False]",
        "[fcode-block(2,3):`:3::::::]",
        "[text(3,3):def:]",
        "[end-fcode-block::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>uvw</p>
<pre><code>def
</code></pre>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_bq_t_nl_i2_fb():
    """
    Test case:  Block quote, text, newline, indent of 2, fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw
  ```
  def
  ```"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):uvw:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(2,3):`:3:::::  :]",
        "[text(3,3):def:\a  \a\x03\a]",
        "[end-fcode-block:  :3:False]",
    ]
    expected_gfm = """<blockquote>
<p>uvw</p>
</blockquote>
<pre><code>def
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i2_bq_fb():
    """
    Test case:  Unordered list, text, newline, ident of 2, block quote, text, newline,
                indent of 2, block quote, fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw
  > ```
  > def
  > ```
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > \n  > \n  > ]",
        "[para(2,5):]",
        "[text(2,5):uvw:]",
        "[end-para:::False]",
        "[fcode-block(3,5):`:3::::::]",
        "[text(4,5):def:]",
        "[end-fcode-block::3:False]",
        "[end-block-quote:::True]",
        "[li(6,1):2::]",
        "[para(6,3):]",
        "[text(6,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>uvw</p>
<pre><code>def
</code></pre>
</blockquote>
</li>
<li>def</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i4_fb():
    """
    Test case:  Unordered list, text, newline, ident of 2, block quote, text, newline,
                indent of 4, fenced block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw
    ```
    def
    ```
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2::  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):uvw:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,5):`:3:::::  :]",
        "[text(4,3):def:\a  \a\x03\a]",
        "[end-fcode-block:  :3:False]",
        "[li(6,1):2::]",
        "[para(6,3):]",
        "[text(6,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>uvw</p>
</blockquote>
<pre><code>def
</code></pre>
</li>
<li>def</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_bq_t_nl_bq_ib():
    """
    Test case:  Block quote, text, newline, block quote, indented block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw
>     def"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):\n    ]",
        "[text(1,3):uvw\ndef::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>uvw
def</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_bq_t_nl_bq_nl_bq_ib():
    """
    Test case:  Block quote, text, newline, block quote, newline block quote, indented block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw
>
>     def"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> ]",
        "[para(1,3):]",
        "[text(1,3):uvw:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[icode-block(3,7):    :]",
        "[text(3,7):def:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>uvw</p>
<pre><code>def
</code></pre>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_bq_t_nl_i6_ib():
    """
    Test case:  Block quote, text, newline, indent of 6, indented block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw
      def"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):\n      ]",
        "[text(1,3):uvw\ndef::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>uvw
def</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_bq_t_nl_nl_nl_i6_ib():
    """
    Test case:  Block quote, text, newline, newline, indent of 6, indented block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> uvw

      def"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):]",
        "[text(1,3):uvw:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,5):    :]",
        "[text(3,5):def:  ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>uvw</p>
</blockquote>
<pre><code>  def
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i2_bq_ib():
    """
    Test case:  Unordered list, text, newline, ident of 2, block quote, text, newline,
                indent of 2, block quote, indented block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw
  >     def
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > ]",
        "[para(2,5):\n    ]",
        "[text(2,5):uvw\ndef::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>uvw
def</p>
</blockquote>
</li>
<li>def</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_bq_nl_i2_bq_ib():
    """
    Test case:  Unordered list, text, newline, ident of 2, block quote, text, newline,
                block quote, newline, indent of 2, block quote, indented block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw
  >
  >     def
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  >\n  > ]",
        "[para(2,5):]",
        "[text(2,5):uvw:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[icode-block(4,9):    :]",
        "[text(4,9):def:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>uvw</p>
<pre><code>def
</code></pre>
</blockquote>
</li>
<li>def</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_i6_ib():
    """
    Test case:  Unordered list, text, newline, ident of 2, block quote, text, newline,
                indent of 6, indented block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw
      def
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  ]",
        "[para(2,5):\n    ]",
        "[text(2,5):uvw\ndef::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<blockquote>
<p>uvw
def</p>
</blockquote>
</li>
<li>def</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_paragraph_series_n_ul_t_nl_i2_bq_t_nl_nl_i6_ib():
    """
    Test case:  Unordered list, text, newline, ident of 2, block quote, text, newline,
                newline, indent of 6, indented block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """* abc
  > uvw

      def
* def"""
    expected_tokens = [
        "[ulist(1,1):*::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n]",
        "[para(2,5):]",
        "[text(2,5):uvw:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[icode-block(4,7):    :]",
        "[text(4,7):def:]",
        "[end-icode-block:::True]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>abc</p>
<blockquote>
<p>uvw</p>
</blockquote>
<pre><code>def
</code></pre>
</li>
<li>
<p>def</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


# setext?
