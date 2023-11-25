"""
Testing various aspects of whitespaces around indented code blocks.

Note that there are various functions that are `x_with_blank_line` where
     `x` is the function before it.  As indented code blocks do not interupt
     paragraphs, the blank line is needed to force the indented code block.
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """    indented block"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):indented block:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>indented block
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_too_many_spaces_before():
    """
    Test case:  Indented Code blocks preceeded by spaces. Because the behavior
                of too many spaces is to be declared as an indented block,
                this is a replication of a previous test.
    """
    test_whitespaces_indented_code_with_spaces_before()


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
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
def test_whitespaces_indented_code_with_tabs_before_repeat():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
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
def test_whitespaces_indented_code_with_form_feeds_before():
    """
    Test case:  Indented Code blocks preceeded by spaces and form feeds.
                Because the form feed does not equate to a space character,
                it resets the space counter, making this into a normal
                paragraph.
    """

    # Arrange
    source_markdown = """ \u000C  abc"""
    expected_tokens = ["[para(1,2): \u000C  ]", "[text(1,2):abc:]", "[end-para:::True]"]
    expected_gfm = """<p>abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before_within_list():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc
      indented block"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n    ]",
        "[text(1,3):abc\nindented block::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
indented block</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before_within_list_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc

      indented block"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,7):    :]",
        "[text(3,7):indented block:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>abc</p>
<pre><code>indented block
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before_within_block_quotes():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> def
      indented block"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n      ]",
        "[text(1,3):abc\ndef\nindented block::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
indented block</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before_within_block_quotes_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> def

      indented block"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[icode-block(4,5):    :]",
        "[text(4,5):indented block:  ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
</blockquote>
<pre><code>  indented block
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before_within_double_block_quotes():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
      indented block"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n      ]",
        "[text(2,5):def\nindented block::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
indented block</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before_within_double_block_quotes_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc

> > def
      indented block"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::]",
        "[block-quote(3,3)::> > \n]",
        "[para(3,5):\n      ]",
        "[text(3,5):def\nindented block::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<blockquote>
<blockquote>
<p>def
indented block</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before_within_double_block_quote_with_single():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
>       indented block"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> ]",
        "[para(2,5):\n      ]",
        "[text(2,5):def\nindented block::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
indented block</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before_within_double_block_quote_with_single_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def

>       indented block"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[block-quote(4,1)::> ]",
        "[icode-block(4,7):    :]",
        "[text(4,7):indented block:  ]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<blockquote>
<pre><code>  indented block
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_unordered_list_x():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
\t  def"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n\t  ]",
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
def test_whitespaces_indented_code_with_tabs_before_within_unordered_list_x_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc

\t  def"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,7):\t  :]",
        "[text(3,7):def:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>abc</p>
<pre><code>def
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_unordered_list_and_single_space():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc
 \t  def"""
    expected_tokens = [
        "[ulist(1,1):-::2:: ]",
        "[para(1,3):\n\t  ]",
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
def test_whitespaces_indented_code_with_tabs_before_within_unordered_list_and_single_space_and_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc

 \t  def"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,7):\t  :]",
        "[text(3,7):def:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>abc</p>
<pre><code>def
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_unordered_list_and_spaces():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  \t  def"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n\t  ]",
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
def test_whitespaces_indented_code_with_tabs_before_within_unordered_list_and_spaces_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc

  \t  def"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,7):\t  :]",
        "[text(3,7):def:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>abc</p>
<pre><code>def
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_unordered_double_list():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  - def
\t\tghi"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :\t]",
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_unordered_double_list_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  - def

\t\tghi"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :\n\t]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[icode-block(4,9):\t:]",
        "[text(4,9):\tghi:]",
        "[end-icode-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>
<p>def</p>
<pre><code>ghi
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_ordered_list_x():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
\t   def"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n\t   ]",
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
def test_whitespaces_indented_code_with_tabs_before_within_ordered_list_x_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc

\t   def"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,8):\t   :]",
        "[text(3,8):def:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<p>abc</p>
<pre><code>def
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before_within_ordered_list():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
       def"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n    ]",
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
def test_whitespaces_indented_code_with_spaces_before_within_ordered_list_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc

       def"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,8):    :]",
        "[text(3,8):def:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<p>abc</p>
<pre><code>def
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_ordered_list_and_single_space():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
 \t   def"""
    expected_tokens = [
        "[olist(1,1):.:1:3:: ]",
        "[para(1,4):\n\t   ]",
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
def test_whitespaces_indented_code_with_tabs_before_within_ordered_list_and_single_space_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc

 \t   def"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,8):\t   :]",
        "[text(3,8):def:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<p>abc</p>
<pre><code>def
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_ordered_list_and_spaces():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
  \t   def"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  ]",
        "[para(1,4):\n\t   ]",
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
def test_whitespaces_indented_code_with_tabs_before_within_ordered_list_and_spaces_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc

  \t   def"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n  ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,8):\t   :]",
        "[text(3,8):def:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<p>abc</p>
<pre><code>def
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_ordered_double_list_x():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_ordered_double_list_no_spaces():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t    ghi"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\t  ]",
        "[para(2,7):\n  ]",
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
def test_whitespaces_indented_code_with_tabs_before_within_ordered_double_list_no_spaces_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def

\t    ghi"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n\t  ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,9):  ]",
        "[text(4,9):ghi:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>
<p>def</p>
<p>ghi</p>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_ordered_double_list_tab_after_indent():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1.   def
       ghi\tjkl"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:8:   :]",
        "[para(2,9):\n       ]",
        "[text(2,9):def\nghi\tjkl::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
ghi	jkl</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_ordered_double_list_tab_after_indent_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1.   def

       ghi\tjkl"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:8:   :]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[icode-block(4,8):    :]",
        "[text(4,8):ghi\tjkl:]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<p>abc</p>
<ol>
<li>def</li>
</ol>
<pre><code>ghi\tjkl
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_ordered_double_list_one_space():
    """
    Test case:  Due to the whitespace being interpretted as a continuation
                of the second list, this should not be interepreted as an
                indented block.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t     ghi"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\t  ]",
        "[para(2,7):\n   ]",
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
def test_whitespaces_indented_code_with_tabs_before_within_ordered_double_list_one_space_with_blank_line():
    """
    Test case:  Due to the whitespace being interpretted as a continuation
                of the second list, this should not be interepreted as an
                indented block.
    """

    # Arrange
    source_markdown = """1. abc
   1. def

\t     ghi"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n\t  ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,10):   ]",
        "[text(4,10):ghi:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>
<p>def</p>
<p>ghi</p>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_ordered_double_list_only_spaces():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1.    def
        ghi"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:9:   :]",
        "[para(2,10):\n        ]",
        "[text(2,10):def\nghi::\n]",
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
def test_whitespaces_indented_code_with_tabs_before_within_ordered_double_list_only_spaces_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1.    def

        ghi"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:9:   :]",
        "[para(2,10):]",
        "[text(2,10):def:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[icode-block(4,8):    :]",
        "[text(4,8):ghi: ]",
        "[end-icode-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<p>abc</p>
<ol>
<li>def</li>
</ol>
<pre><code> ghi
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_formfeeds_before_within_list():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
 \u000C \u000C    def"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n ]",
        "[text(1,3):abc\n\u000C \u000C    def::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
\u000C \u000C    def</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before_within_double_block_quotes_with_zero_and_zero_spaces_at_start():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
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
        "[para(2,5):\n    ]",
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
def test_whitespaces_indented_code_with_spaces_before_within_double_block_quotes_with_zero_and_zero_spaces_at_start_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> >
    ghi"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> >]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(4,5):    :]",
        "[text(4,5):ghi:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<pre><code>ghi
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before_within_double_block_quotes_with_zero_and_one_space_at_start():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
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
        "[para(2,5):\n     ]",
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
def test_whitespaces_indented_code_with_spaces_before_within_double_block_quotes_with_zero_and_one_space_at_start_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> >
     ghi"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> >]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(4,5):    :]",
        "[text(4,5):ghi: ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<pre><code> ghi
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before_within_double_block_quotes_with_zero_and_three_spaces_at_start():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
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
        "[para(2,5):\n       ]",
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
def test_whitespaces_indented_code_with_spaces_before_within_double_block_quotes_with_zero_and_three_spaces_at_start_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> >
       ghi"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> >]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(4,5):    :]",
        "[text(4,5):ghi:   ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<pre><code>   ghi
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_spaces_before_within_double_block_quotes_with_zero_and_four_spaces_at_start():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
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
        "[para(2,5):\n        ]",
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
def test_whitespaces_indented_code_with_spaces_before_within_double_block_quotes_with_zero_and_four_spaces_at_start_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> >
        ghi"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> >]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(4,5):    :]",
        "[text(4,5):ghi:    ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<pre><code>    ghi
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_block_quotes_x1():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
\t  ghi"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n\t  ]",
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
def test_whitespaces_indented_code_with_tabs_before_within_block_quotes_x1_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>
\t  ghi"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[end-block-quote:::False]",
        "[icode-block(4,5):\t:]",
        "[text(4,5):  ghi:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
</blockquote>
<pre><code>  ghi
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_block_quotes_x2():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
  \t  ghi"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n  \t  ]",
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
def test_whitespaces_indented_code_with_tabs_before_within_block_quotes_x2_with_blank_line():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>
  \t  ghi"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[end-block-quote:::False]",
        "[icode-block(4,5):  \t:]",
        "[text(4,5):  ghi:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
</blockquote>
<pre><code>  ghi
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_block_quotes_repeat():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>
>\t  indented block
>\t  indented block"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>\n>]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[icode-block(4,7):\t  :\n\t  ]",
        "[text(4,7):indented block\nindented block:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
<pre><code>indented block
indented block
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_block_quotes_bare_repeat():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t  indented block
>\t  indented block"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[icode-block(1,7):\t  :\n\t  ]",
        "[text(1,7):indented block\nindented block:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>indented block
indented block
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_block_quotes_bare_with_space_repeat():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> \t  indented block
> \t  indented block"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[icode-block(1,7):\t  :\n\t  ]",
        "[text(1,7):indented block\nindented block:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>indented block
indented block
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_within_block_quotes_bare_with_many_tabs():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t  abc\tdef
>\t  abc\tdef"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[icode-block(1,7):\t  :\n\t  ]",
        "[text(1,7):abc\tdef\nabc\tdef:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>abc\tdef
abc\tdef
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


###


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_with_block_quote_with_blank():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>
\tindented block"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[end-block-quote:::False]",
        "[icode-block(4,5):\t:]",
        "[text(4,5):indented block:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
</blockquote>
<pre><code>indented block
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_with_double_block_quote():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
\tindented block"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n\t]",
        "[text(2,5):def\nindented block::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
indented block</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_with_double_block_quote_with_blank():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> >
\tindented block"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> >]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[end-block-quote:::False]",
        "[end-block-quote:::False]",
        "[icode-block(4,5):\t:]",
        "[text(4,5):indented block:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<pre><code>indented block
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_with_double_block_quote_with_single_with_blank():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> >
>\tindented block"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> >]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[end-block-quote:::True]",
        "[para(4,5):\t]",
        "[text(4,5):indented block:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<p>indented block</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_with_double_block_quote_with_single_with_blank_and_space():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> >
> \tindented block"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> >]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[end-block-quote:::True]",
        "[para(4,5):\t]",
        "[text(4,5):indented block:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<p>indented block</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_with_double_block_quote_with_single_with_spaces_and_blank_x():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> >
> \t  indented block"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> >]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[end-block-quote:::True]",
        "[icode-block(4,7):\t  :]",
        "[text(4,7):indented block:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<pre><code>indented block
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_with_double_block_quote_with_single_with_spaces_and_blank_and_tab():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> >
> \t\tindented block"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> >]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[end-block-quote:::True]",
        "[icode-block(4,7):\t:]",
        "[text(4,7):\a\t\a  \aindented block:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<pre><code>  indented block
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


###


@pytest.mark.gfm
def test_whitespaces_indented_code_with_single_tab_before():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """\tindented block"""
    expected_tokens = [
        "[icode-block(1,5):\t:]",
        "[text(1,5):indented block:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>indented block
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
