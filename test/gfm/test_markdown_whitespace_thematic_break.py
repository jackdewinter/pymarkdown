"""
Testing various aspects of whitespaces around atx headers.
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before() -> None:
    """
    Test case:  Thematic breaks preceeded by spaces.
    """

    # Arrange
    source_markdown = """   * * *"""
    expected_tokens = ["[tbreak(1,4):*:   :* * *]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_too_many_spaces_before() -> None:
    """
    Test case:  Thematic breaks preceeded by spaces.
    """

    # Arrange
    source_markdown = """abc
    ---"""
    expected_tokens = [
        "[para(1,1):\n    ]",
        "[text(1,1):abc\n---::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
---</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before() -> None:
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t * * *"""
    expected_tokens = [
        "[icode-block(1,5): \t:]",
        "[text(1,5): * * *:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code> * * *
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_repeat() -> None:
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t * * *
 \t * * *"""
    expected_tokens = [
        "[icode-block(1,5): \t:\n \t]",
        "[text(1,5): * * *\n * * *:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code> * * *
 * * *
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_form_feeds_before() -> None:
    """
    Test case:  Thematic breaks preceeded by spaces and form feeds.
    """

    # Arrange
    source_markdown = """ \u000C * * *"""
    expected_tokens = [
        "[para(1,2): \u000C ]",
        "[text(1,2):* * *:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>* * *</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before_within_list() -> None:
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
    * * *"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[tbreak(2,5):*:  :* * *]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<hr />
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before_within_block_quotes() -> None:
    """
    Test case:  Thematic breaks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> def
    * * *"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n    ]",
        "[text(1,3):abc\ndef\n* * *::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
* * *</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before_within_double_block_quotes() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
    * * *"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n    ]",
        "[text(2,5):def\n* * *::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
* * *</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before_within_double_block_quotes_with_single() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   * * *"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[tbreak(3,5):*:  :* * *]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_unordered_list_x() -> None:
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
\t* * *"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[tbreak(2,5):*:\t:* * *]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<hr />
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_unordered_list_and_single_space() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc
 \t* * *"""
    expected_tokens = [
        "[ulist(1,1):-::2:: ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[tbreak(2,5):*:\t:* * *]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<hr />
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_unordered_list_and_spaces() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  \t* * *"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[tbreak(2,5):*:\t:* * *]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<hr />
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_unordered_double_list() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  - def
\t---"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :\t]",
        "[setext(3,5):-:3::(2,5)]",
        "[text(2,5):def:]",
        "[end-setext::]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>
<h2>def</h2>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_list_x() -> None:
    """
    Test case:  Thematic breaks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
\t* * *"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[tbreak(2,5):*:\t:* * *]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before_within_ordered_list() -> None:
    """
    Test case:  Thematic breaks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
    * * *"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[tbreak(2,5):*: :* * *]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_list_and_single_space() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
 \t* * *"""
    expected_tokens = [
        "[olist(1,1):.:1:3:: ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[tbreak(2,5):*:\t:* * *]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_list_and_spaces() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
  \t* * *"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[tbreak(2,5):*:\t:* * *]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_double_list_x() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t  * * *"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\t  ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[tbreak(3,7):*::* * *]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
<hr />
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_double_list_no_spaces() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t* * *"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,5):*:\t:* * *]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_double_list_tab_after_indent() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
   *\t*\t*"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,4):*::*\t*\t*]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_double_list_one_space() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t * * *"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,6):*:\t :* * *]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_double_list_only_spaces() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
    * * *"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[tbreak(3,5):*: :* * *]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_formfeeds_before_within_list() -> None:
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
 \u000C \u000C* * *"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n ]",
        "[text(1,3):abc\n\u000C \u000C* * *::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
\u000C \u000C* * *</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before_within_double_block_quotes_with_zero_and_zero_spaces_at_start() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
* * *"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[tbreak(3,1):*::* * *]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before_within_double_block_quotes_with_zero_and_one_space_at_start() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
 * * *"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[tbreak(3,2):*: :* * *]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before_within_double_block_quotes_with_zero_and_two_spaces_at_start() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
  * * *"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[tbreak(3,3):*:  :* * *]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before_within_double_block_quotes_with_zero_and_three_spaces_at_start() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
   * * *"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[tbreak(3,4):*:   :* * *]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before_within_double_block_quotes_with_zero_and_four_spaces_at_start() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    test_whitespaces_thematic_breaks_with_spaces_before_within_double_block_quotes()


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_block_quotes_x1() -> None:
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
\t* * *"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n\t]",
        "[text(1,3):abc\ndef\n* * *::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
* * *</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_block_quotes_x2() -> None:
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
  \t* * *"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n  \t]",
        "[text(1,3):abc\ndef\n* * *::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
* * *</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_block_quotes_repeat() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>\t* * *
>\t* * *"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::False]",
        "[tbreak(3,5):*:\t:* * *]",
        "[tbreak(4,5):*:\t:* * *]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
<hr />
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_block_quotes_bare_repeat() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t* * *
>\t* * *"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[tbreak(1,5):*:\t:* * *]",
        "[tbreak(2,5):*:\t:* * *]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<hr />
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_block_quotes_bare_with_space_repeat() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> \t* * *
> \t* * *"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[tbreak(1,5):*:\t:* * *]",
        "[tbreak(2,5):*:\t:* * *]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<hr />
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_block_quotes_bare_with_many_tabs() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t*\t*\t*\t
>\t*\t*\t*\t"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[tbreak(1,5):*:\t:*\t*\t*\t]",
        "[tbreak(2,5):*:\t:*\t*\t*\t]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<hr />
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


###


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_double_block_quotes_1() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
\t* * *"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n\t]",
        "[text(2,5):def\n* * *::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
* * *</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_double_block_quotes_2() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
 \t* * *"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n \t]",
        "[text(2,5):def\n* * *::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
* * *</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_double_block_quotes_3() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
  \t* * *"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n  \t]",
        "[text(2,5):def\n* * *::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
* * *</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_double_block_quotes_with_single() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
>\t* * *"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n>]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::False]",
        "[end-block-quote::>:True]",
        "[tbreak(3,5):*:\t:* * *]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_double_block_quotes_with_single_and_space() -> (
    None
):
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> \t* * *"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[tbreak(3,5):*:\t:* * *]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


###


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_inside() -> None:
    """
    Test case:  Thematic breaks containing spaces and tabs.
    """

    # Arrange
    source_markdown = """* *\t*"""
    expected_tokens = ["[tbreak(1,1):*::* *\t*]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_form_feeds_inside() -> None:
    """
    Test case:  Thematic breaks containing spaces and form feeds.
    """

    # Arrange
    source_markdown = """* *\u000C*"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):*\u000C*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>*\u000C*</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_after() -> None:
    """
    Test case:  Thematic breaks followed by spaces.
    """

    # Arrange
    source_markdown = """* * * """
    expected_tokens = ["[tbreak(1,1):*::* * * ]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_after() -> None:
    """
    Test case:  Thematic breaks followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """* * *\t"""
    expected_tokens = ["[tbreak(1,1):*::* * *\t]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_form_feeds_after() -> None:
    """
    Test case:  Thematic breaks followed by spaces and form feeds.
    """

    # Arrange
    source_markdown = """* * *\u000C"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[ulist(1,3):*::4:  ]",
        "[para(1,5)::\u000C]",
        "[text(1,5):*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>*</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
