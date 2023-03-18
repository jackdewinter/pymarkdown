"""
Testing various aspects of whitespaces around atx headers.
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before():
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
def test_whitespaces_thematic_breaks_with_tabs_before():
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
def test_whitespaces_thematic_breaks_with_tabs_before_repeat():
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
def test_whitespaces_thematic_breaks_with_form_feeds_before():
    """
    Test case:  Thematic breaks preceeded by spaces and form feeds.
    """

    # Arrange
    source_markdown = """ \u000C * * *"""
    expected_tokens = [
        "[para(1,2): \u000C ]",
        "[text(1,2):*:]",
        "[text(1,3): :]",
        "[text(1,4):*:]",
        "[text(1,5): :]",
        "[text(1,6):*:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>* * *</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before_within_list():
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)
    # assert False


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_before_within_block_quotes():
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
        "[text(1,3):abc\ndef\n::\n\n]",
        "[text(3,5):*:]",
        "[text(3,6): :]",
        "[text(3,7):*:]",
        "[text(3,8): :]",
        "[text(3,9):*:]",
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
def test_whitespaces_thematic_breaks_with_spaces_before_within_double_block_quotes():
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
        "[text(2,5):def\n::\n]",
        "[text(3,5):*:]",
        "[text(3,6): :]",
        "[text(3,7):*:]",
        "[text(3,8): :]",
        "[text(3,9):*:]",
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
def test_whitespaces_thematic_breaks_with_spaces_before_within_double_block_quotes_with_single():
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_unordered_list_x():
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)
    # assert False


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_unordered_list_and_single_space():
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_unordered_list_and_spaces():
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_unordered_double_list():
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  - def
\t* * *"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :\t]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::False]",
        "[tbreak(3,5):*::* * *]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>def
<hr />
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_list_x():
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
        "[atx(2,5):1:0:\t]",
        "[text(2,7):abc: ]",
        "[end-atx::]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_list_and_single_space():
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
        "[atx(2,5):1:0:\t]",
        "[text(2,7):abc: ]",
        "[end-atx::]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_list_and_spaces():
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
        "[atx(2,5):1:0:\t]",
        "[text(2,7):abc: ]",
        "[end-atx::]",
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_double_list_x():
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


@pytest.mark.skip
@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_double_list_no_spaces():
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
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[atx(3,5):1:0:\t]",
        "[text(3,7):abc: ]",
        "[end-atx::]",
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_double_list_tab_after_indent():
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


@pytest.mark.skip
@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_double_list_one_space():
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
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[atx(3,6):1:0:\t ]",
        "[text(3,8):abc: ]",
        "[end-atx::]",
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_ordered_double_list_only_spaces():
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
def test_whitespaces_thematic_breaks_with_formfeeds_before_within_list():
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
 \u000C \u000C* * *"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n ]",
        "[text(1,3):abc\n\u000C \u000C::\n]",
        "[text(2,5):*:]",
        "[text(2,6): :]",
        "[text(2,7):*:]",
        "[text(2,8): :]",
        "[text(2,9):*:]",
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
def test_whitespaces_thematic_breaks_with_spaces_before_within_double_block_quotes_with_zero_and_three_spaces_at_start():
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_block_quotes_x1():
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
        "[text(1,3):abc\ndef\n::\n\n]",
        "[text(3,2):*:]",
        "[text(3,3): :]",
        "[text(3,4):*:]",
        "[text(3,5): :]",
        "[text(3,6):*:]",
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_block_quotes_x2():
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
        "[text(1,3):abc\ndef\n::\n\n]",
        "[text(3,4):*:]",
        "[text(3,5): :]",
        "[text(3,6):*:]",
        "[text(3,7): :]",
        "[text(3,8):*:]",
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_block_quotes_repeat():
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_block_quotes_bare_repeat():
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_block_quotes_bare_with_space_repeat():
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_block_quotes_bare_with_many_tabs():
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


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_before_within_double_block_quotes_1():
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
        "[text(2,5):def\n::\n]",
        "[text(3,2):*:]",
        "[text(3,3): :]",
        "[text(3,4):*:]",
        "[text(3,5): :]",
        "[text(3,6):*:]",
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_double_block_quotes_2():
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
        "[text(2,5):def\n::\n]",
        "[text(3,3):*:]",
        "[text(3,4): :]",
        "[text(3,5):*:]",
        "[text(3,6): :]",
        "[text(3,7):*:]",
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_double_block_quotes_3():
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
        "[text(2,5):def\n::\n]",
        "[text(3,4):*:]",
        "[text(3,5): :]",
        "[text(3,6):*:]",
        "[text(3,7): :]",
        "[text(3,8):*:]",
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_double_block_quotes_with_single():
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
        "[block-quote(2,1)::> > \n> ]",
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
def test_whitespaces_thematic_breaks_with_tabs_before_within_double_block_quotes_with_single_and_space():
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
def test_whitespaces_thematic_breaks_with_formfeeds_before_within_block_quotes():
    """
    Test case:  Thematic breaks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
 \u000C \u000C* * *"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n ]",
        "[text(1,3):abc\n\u000C \u000C::\n]",
        "[text(2,5):*:]",
        "[text(2,6): :]",
        "[text(2,7):*:]",
        "[text(2,8): :]",
        "[text(2,9):*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
\u000C \u000C* * *</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


###


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_tabs_inside():
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
def test_whitespaces_thematic_breaks_with_form_feeds_inside():
    """
    Test case:  Thematic breaks containing spaces and form feeds.
    """

    # Arrange
    source_markdown = """* *\u000C*"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):*:]",
        "[text(1,4):\u000C:]",
        "[text(1,5):*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>*\u000C*</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_thematic_breaks_with_spaces_after():
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
def test_whitespaces_thematic_breaks_with_tabs_after():
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
def test_whitespaces_thematic_breaks_with_form_feeds_after():
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
