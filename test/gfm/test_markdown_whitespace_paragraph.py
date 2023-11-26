"""
Testing various aspects of whitespaces around paragraphs.
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_before():
    """
    Test case:  paragraph preceeded by spaces.
    """

    # Arrange
    source_markdown = """   a paragraph"""
    expected_tokens = [
        "[para(1,4):   ]",
        "[text(1,4):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_too_many_spaces_before():
    """
    Test case:  Paragraph preceeded by spaces.
    """

    # Arrange
    source_markdown = """abc
    def"""
    expected_tokens = [
        "[para(1,1):\n    ]",
        "[text(1,1):abc\ndef::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
def</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t abc"""
    expected_tokens = [
        "[icode-block(1,5): \t:]",
        "[text(1,5): abc:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code> abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_repeat():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t abc
 \t abc"""
    expected_tokens = [
        "[icode-block(1,5): \t:\n \t]",
        "[text(1,5): abc\n abc:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code> abc
 abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_form_feeds_before():
    """
    Test case:  Paragraph preceeded by spaces and form feeds.
    """

    # Arrange
    source_markdown = """ \u000C abc"""
    expected_tokens = ["[para(1,2): \u000C ]", "[text(1,2):abc:]", "[end-para:::True]"]
    expected_gfm = """<p>abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_before_within_list():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
    def"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n  ]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
def</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_before_within_block_quotes():
    """
    Test case:  paragraph preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> def
    a paragraph"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n    ]",
        "[text(1,3):abc\ndef\na paragraph::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
a paragraph</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_before_within_double_block_quotes():
    """
    Test case:  paragraph preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
    a paragraph"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n    ]",
        "[text(2,5):def\na paragraph::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
a paragraph</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_before_within_double_block_quotes_with_single():
    """
    Test case:  paragraph preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   a paragraph"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> ]",
        "[para(2,5):\n  ]",
        "[text(2,5):def\na paragraph::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
a paragraph</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_unordered_list_x():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
\tdef"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n\t]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
def</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_unordered_list_and_single_space():
    """
    Test case:  Paragraph preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc
 \tdef"""
    expected_tokens = [
        "[ulist(1,1):-::2:: ]",
        "[para(1,3):\n\t]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
def</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_unordered_list_and_spaces():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  \tdef"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n\t]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
def</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_unordered_double_list():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  - def
\tghi"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :\t]",
        "[para(2,5):\n]",
        "[text(2,5):def\nghi::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>def
ghi</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_unordered_double_list_double_tabs():
    """
    Test case:  TBD
    """

    # Arrange
    source_markdown = """+ abc
  + def
\t\tghi"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:  :\t]",
        "[para(2,5):\n\t]",
        "[text(2,5):def\nghi::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>def
ghi</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_ordered_list_x():
    """
    Test case:  Paragraph preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
\tdef"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n\t]",
        "[text(1,4):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
def</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_before_within_ordered_list():
    """
    Test case:  Paragraph preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
    def"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n ]",
        "[text(1,4):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
def</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_ordered_list_and_single_space():
    """
    Test case:  Paragraph preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
 \tdef"""
    expected_tokens = [
        "[olist(1,1):.:1:3:: ]",
        "[para(1,4):\n\t]",
        "[text(1,4):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
def</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_ordered_list_and_spaces():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
  \tdef"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  ]",
        "[para(1,4):\n\t]",
        "[text(1,4):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
def</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_ordered_double_list_x():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t  ghi"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\t  ]",
        "[para(2,7):\n]",
        "[text(2,7):def\nghi::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
ghi</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_paragraph_with_tabs_before_within_ordered_double_list_double_tabs():
    """
    Test case:  This was intended to be an indented block, but is not due to a
    paragraph continutation
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t\t  ghi"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n\t  ]",
        "[text(2,7):def\nghi::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
ghi</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_ordered_double_list_no_spaces():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\tghi"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n\t]",
        "[text(2,7):def\nghi::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
ghi</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_ordered_double_list_tab_after_indent():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
   ghi\tjkl\tmno"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n   ]",
        "[text(2,7):def\nghi\tjkl\tmno::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
ghi\tjkl\tmno</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_ordered_double_list_one_space():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t ghi"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n\t ]",
        "[text(2,7):def\nghi::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
ghi</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_ordered_double_list_only_spaces():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
    ghi"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n    ]",
        "[text(2,7):def\nghi::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
ghi</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_formfeeds_before_within_list():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
 \u000C \u000Cdef"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n ]",
        "[text(1,3):abc\n\u000C \u000Cdef::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
\u000C \u000Cdef</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_before_within_double_block_quotes_with_zero_and_zero_spaces_at_start():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
ghi"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n]",
        "[text(2,5):def\nghi::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
ghi</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_before_within_double_block_quotes_with_zero_and_one_space_at_start():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
 ghi"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n ]",
        "[text(2,5):def\nghi::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
ghi</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_before_within_double_block_quotes_with_zero_and_two_spaces_at_start():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
  ghi"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n  ]",
        "[text(2,5):def\nghi::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
ghi</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_before_within_double_block_quotes_with_zero_and_three_spaces_at_start():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
   ghi"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n   ]",
        "[text(2,5):def\nghi::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
ghi</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_before_within_double_block_quotes_with_zero_and_four_spaces_at_start():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    test_whitespaces_paragraph_with_spaces_before_within_double_block_quotes()


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_block_quotes_x1():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
\tghi"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n\t]",
        "[text(1,3):abc\ndef\nghi::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
ghi</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_block_quotes_x2():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
  \tghi"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n  \t]",
        "[text(1,3):abc\ndef\nghi::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
ghi</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_block_quotes_repeat():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>\tghi
>\tjkl"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>]",
        "[para(1,3):\n\n\t\n\t]",
        "[text(1,3):abc\ndef\nghi\njkl::\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
ghi
jkl</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_block_quotes_bare_repeat():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\tabc
>\tdef"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[para(1,5):\t\n\t]",
        "[text(1,5):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_block_quotes_bare_with_space_repeat():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> \tabc
> \tdef"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,5):\t\n\t]",
        "[text(1,5):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_block_quotes_bare_with_many_tabs():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\ta\tb\tc\t
>\td\te\tf\t"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[para(1,5):\t\n\t:\t]",
        "[text(1,5):a\tb\tc\nd\te\tf::\t\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>a\tb\tc	
d\te\tf</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_double_block_quotes_1():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
\tghi"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n\t]",
        "[text(2,5):def\nghi::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
ghi</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_double_block_quotes_2():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
 \tghi"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n \t]",
        "[text(2,5):def\nghi::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
ghi</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_double_block_quotes_3():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
  \tghi"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n  \t]",
        "[text(2,5):def\nghi::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
ghi</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_double_block_quotes_with_single():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
>\tghi"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n>]",
        "[para(2,5):\n\t]",
        "[text(2,5):def\nghi::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
ghi</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_double_block_quotes_with_single_and_space():
    """
    Test case:  Paragraph preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> \tghi"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> ]",
        "[para(2,5):\n\t]",
        "[text(2,5):def\nghi::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
ghi</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


###


@pytest.mark.gfm
def test_whitespaces_paragraph_with_just_tabs_before():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """\ta paragraph"""
    expected_tokens = [
        "[icode-block(1,5):\t:]",
        "[text(1,5):a paragraph:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>a paragraph
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_block_quote_bare_repeat_2():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \ta\tparagraph\t
> \ta\tparagraph\t"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,5):\t\n\t:\t]",
        "[text(1,5):a\tparagraph\na\tparagraph::\t\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>a\tparagraph\t
a\tparagraph</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_double_block_quote_with_single_and_space_within():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   a\tparagraph"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> ]",
        "[para(2,5):\n  ]",
        "[text(2,5):def\na\tparagraph::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
a\tparagraph</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


###


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_inside():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """a\tlong\tparagraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a\tlong\tparagraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a\tlong\tparagraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_inside_and_emphasis():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """a\t*long*\tparagraph"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a\t:]",
        "[emphasis(1,5):1:*]",
        "[text(1,6):long:]",
        "[end-emphasis(1,10)::]",
        "[text(1,11):\tparagraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a\t<em>long</em>\tparagraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_just_form_feeds_before():
    """
    Test case:  paragraph preceeded by form feeds.
    """

    # Arrange
    source_markdown = """\u000ca paragraph"""
    expected_tokens = [
        "[para(1,1):\u000c]",
        "[text(1,1):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_and_form_feeds_before():
    """
    Test case:  paragraph preceeded by form feeds.
    """

    # Arrange
    source_markdown = """ \u000ca paragraph"""
    expected_tokens = [
        "[para(1,2): \u000c]",
        "[text(1,2):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_and_form_feeds_before_and_after():
    """
    Test case:  paragraph preceeded by form feeds.
    """

    # Arrange
    source_markdown = """ \u000c a paragraph"""
    expected_tokens = [
        "[para(1,2): \u000c ]",
        "[text(1,2):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_after():
    """
    Test case:  paragraph followed by spaces.
    """

    # Arrange
    source_markdown = """a paragraph  """
    expected_tokens = [
        "[para(1,1)::  ]",
        "[text(1,1):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_after():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """a paragraph\t"""
    expected_tokens = [
        "[para(1,1)::\t]",
        "[text(1,1):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_after_double():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """a paragraph\t
another paragraph\t\t"""
    expected_tokens = [
        "[para(1,1):\n:\t\t]",
        "[text(1,1):a paragraph\nanother paragraph::\t\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph\t
another paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_after_double_only_first():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """a paragraph\t
another paragraph"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):a paragraph\nanother paragraph::\t\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph\t
another paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_after_double_only_second():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """a paragraph
another paragraph\t\t"""
    expected_tokens = [
        "[para(1,1):\n:\t\t]",
        "[text(1,1):a paragraph\nanother paragraph::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph
another paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_after_only_middle():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """a paragraph
another paragraph\t\t
yet another paragraph"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):a paragraph\nanother paragraph\nyet another paragraph::\n\t\t\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph
another paragraph\t\t
yet another paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_mixed_and_no_newline():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """before-tab\tafter-tab
before-tab\tafter-tab
before-tab\tafter-tab\tafter-another
a\tbb\tccc\tddd"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):before-tab\tafter-tab\nbefore-tab\tafter-tab\nbefore-tab\tafter-tab\tafter-another\na\tbb\tccc\tddd::\n\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>before-tab\tafter-tab
before-tab\tafter-tab
before-tab\tafter-tab\tafter-another
a\tbb\tccc\tddd</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_mixed_and_newline():
    """
    Test case:  paragraph followed by tabs.
    """

    # Arrange
    source_markdown = """before-tab\tafter-tab
before-tab\tafter-tab
before-tab\tafter-tab\tafter-another
a\tbb\tccc\tddd
"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):before-tab\tafter-tab\nbefore-tab\tafter-tab\nbefore-tab\tafter-tab\tafter-another\na\tbb\tccc\tddd::\n\n\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<p>before-tab\tafter-tab
before-tab\tafter-tab
before-tab\tafter-tab\tafter-another
a\tbb\tccc\tddd</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_form_feeds_after():
    """
    Test case:  paragraph followed by form feeds.
    """

    # Arrange
    source_markdown = """a paragraph\u000c"""
    expected_tokens = [
        "[para(1,1)::\u000c]",
        "[text(1,1):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
