"""
https://github.com/jackdewinter/pymarkdown/issues/456
"""
from test.utils import act_and_assert

import pytest

## need doubles and mixes with list cases
# test_whitespaces_thematic_breaks_with_tabs_before_within_double_block_quotes_with_single


@pytest.mark.gfm
def test_whitespaces_block_quotes_with_spaces():
    """
    Test case:  Block quotes preceeded by spaces.
    """

    # Arrange
    source_markdown = """   > block quote"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[para(1,6):]",
        "[text(1,6):block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>block quote</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_block_quotes_with_tabs():
    """
    Test case:  Block quotes preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ > block quote
 >\t> another block quote"""
    expected_tokens = [
        "[block-quote(1,2): : > \n > ]",
        "[para(1,4):]",
        "[text(1,4):block quote:]",
        "[end-para:::True]",
        "[block-quote(2,5):: >  > ]",
        "[para(2,7):]",
        "[text(2,7):another block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>block quote</p>
<blockquote>
<p>another block quote</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_block_quotes_with_tabs_2():
    """
    Test case:  Block quotes preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ > block quote
 >\t> another block quote
 >\t> same block quote"""
    expected_tokens = [
        "[block-quote(1,2): : > \n > ]",
        "[para(1,4):]",
        "[text(1,4):block quote:]",
        "[end-para:::True]",
        "[block-quote(2,5):: >  > \n >  > ]",
        "[para(2,7):\n]",
        "[text(2,7):another block quote\nsame block quote::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>block quote</p>
<blockquote>
<p>another block quote
same block quote</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_block_quotes_with_form_feeds():
    """
    Test case:  Block quotes preceeded by spaces and form feeds (ascii whitespace).
    """

    # Arrange
    source_markdown = """ > block quote
 >\u000C> another block quote"""
    expected_tokens = [
        "[block-quote(1,2): : > \n >]",
        "[para(1,4):\n]",
        "[text(1,4):block quote\n\u000C\a>\a&gt;\a another block quote::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>block quote
\u000C&gt; another block quote</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_ordered_lists_with_spaces():
    """
    Test case:  Ordered lists preceeded by spaces.
    """

    # Arrange
    source_markdown = """   1. list item"""
    expected_tokens = [
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):list item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>list item</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_ordered_lists_with_tabs():
    """
    Test case:  Ordered lists preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. list item
 \t1. inner list item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):list item:]",
        "[end-para:::True]",
        "[olist(2,5):.:1:7:    ]",
        "[para(2,8):]",
        "[text(2,8):inner list item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>list item
<ol>
<li>inner list item</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_ordered_lists_with_form_feeds():
    """
    Test case:  Ordered lists preceeded by spaces and form feeds (ascii whitespace).
    """

    # Arrange
    source_markdown = """1. list item
 \u000C1. inner list item"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n ]",
        "[text(1,4):list item\n\u000C1. inner list item::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>list item
\u000C1. inner list item</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_unordered_lists_with_spaces():
    """
    Test case:  Unordered lists preceeded by spaces.
    """

    # Arrange
    source_markdown = """   + list item"""
    expected_tokens = [
        "[ulist(1,4):+::5:   ]",
        "[para(1,6):]",
        "[text(1,6):list item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>list item</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_unordered_lists_with_tabs():
    """
    Test case:  Unordered lists preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """+ list item
 \t+ inner list item"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[para(1,3):]",
        "[text(1,3):list item:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:    ]",
        "[para(2,7):]",
        "[text(2,7):inner list item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>list item
<ul>
<li>inner list item</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_unordered_lists_with_form_feeds():
    """
    Test case:  Unordered lists preceeded by spaces and form feeds (ascii whitespace).
    """

    # Arrange
    source_markdown = """+ list item
 \u000C + inner list item"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[para(1,3):\n ]",
        "[text(1,3):list item\n\u000C + inner list item::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>list item
\u000C + inner list item</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
