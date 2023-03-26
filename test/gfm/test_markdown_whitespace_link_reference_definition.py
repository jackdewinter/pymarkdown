"""
Testing various aspects of whitespaces around link reference definitions.
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before():
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """   [fred]: /url
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,4):True:   :fred:: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_too_many_spaces_before():
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """[fred]
    [fred]: /url"""
    expected_tokens = [
        "[para(1,1):\n    ]",
        "[text(1,1):[:]",
        "[text(1,2):fred:]",
        "[text(1,6):]:]",
        "[text(1,7):\n::\n]",
        "[text(2,5):[:]",
        "[text(2,6):fred:]",
        "[text(2,10):]:]",
        "[text(2,11):: /url:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[fred]
[fred]: /url</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """\t[fred]: /url
[fred]"""
    expected_tokens = [
        "[icode-block(1,5):\t:]",
        "[text(1,5):[fred]: /url:]",
        "[end-icode-block:::False]",
        "[para(2,1):]",
        "[text(2,1):[:]",
        "[text(2,2):fred:]",
        "[text(2,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>[fred]: /url
</code></pre>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_repeat():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """\t[abc]: /url
\t[def]: /url
[abc]
[def]"""
    expected_tokens = [
        "[icode-block(1,5):\t:\n\t]",
        "[text(1,5):[abc]: /url\n[def]: /url:]",
        "[end-icode-block:::False]",
        "[para(3,1):\n]",
        "[text(3,1):[:]",
        "[text(3,2):abc:]",
        "[text(3,5):]:]",
        "[text(3,6):\n::\n]",
        "[text(4,1):[:]",
        "[text(4,2):def:]",
        "[text(4,5):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>[abc]: /url
[def]: /url
</code></pre>
<p>[abc]
[def]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_before():
    """
    Test case:  LRD preceeded by form feeds.
    """

    # Arrange
    source_markdown = """\u000c[fred]: /url
[fred]"""
    expected_tokens = [
        "[para(1,1):\u000c\n]",
        "[text(1,1):[:]",
        "[text(1,2):fred:]",
        "[text(1,6):]:]",
        "[text(1,7):: /url\n::\n]",
        "[text(2,1):[:]",
        "[text(2,2):fred:]",
        "[text(2,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[fred]: /url
[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_within_list():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
    [fred]: /url
[fred]"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n]",
        "[para(1,3):\n  \n]",
        "[text(1,3):abc\n::\n]",
        "[text(2,3):[:]",
        "[text(2,4):fred:]",
        "[text(2,8):]:]",
        "[text(2,9):: /url\n::\n]",
        "[text(3,1):[:]",
        "[text(3,2):fred:]",
        "[text(3,6):]:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
[fred]: /url
[fred]</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_within_block_quotes():
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> def
    [fred]: /url
[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):\n\n    \n]",
        "[text(1,3):abc\ndef\n::\n\n]",
        "[text(3,5):[:]",
        "[text(3,6):fred:]",
        "[text(3,10):]:]",
        "[text(3,11):: /url\n::\n]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
[fred]: /url
[fred]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_within_double_block_quotes():
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
    [fred]: /url
[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n    \n]",
        "[text(2,5):def\n::\n]",
        "[text(3,5):[:]",
        "[text(3,6):fred:]",
        "[text(3,10):]:]",
        "[text(3,11):: /url\n::\n]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
[fred]: /url
[fred]</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_within_double_block_quote_with_single():
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   [fred]: /url
[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> \n]",
        "[para(2,5):\n  \n]",
        "[text(2,5):def\n::\n]",
        "[text(3,5):[:]",
        "[text(3,6):fred:]",
        "[text(3,10):]:]",
        "[text(3,11):: /url\n::\n]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
[fred]: /url
[fred]</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_unordered_list_x():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
\t[fred]: /url

[fred]"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n]",
        "[para(1,3):\n\t]",
        "[text(1,3):abc\n::\n]",
        "[text(2,2):[:]",
        "[text(2,3):fred:]",
        "[text(2,7):]:]",
        "[text(2,8):: /url:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
        "[para(4,1):]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
[fred]: /url</li>
</ul>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_unordered_list_and_single_space():
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc
 \t[fred]: /url

[fred]"""
    expected_tokens = [
        "[ulist(1,1):-::2:: \n]",
        "[para(1,3):\n\t]",
        "[text(1,3):abc\n::\n]",
        "[text(2,2):[:]",
        "[text(2,3):fred:]",
        "[text(2,7):]:]",
        "[text(2,8):: /url:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
        "[para(4,1):]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
[fred]: /url</li>
</ul>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_unordered_list_and_spaces():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  \t[fred]: /url

[fred]"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n]",
        "[para(1,3):\n\t]",
        "[text(1,3):abc\n::\n]",
        "[text(2,2):[:]",
        "[text(2,3):fred:]",
        "[text(2,7):]:]",
        "[text(2,8):: /url:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
        "[para(4,1):]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
[fred]: /url</li>
</ul>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_unordered_double_list():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  - def
\t[fred]: /url

[fred]"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :\t\n]",
        "[para(2,5):\n]",
        "[text(2,5):def\n::\n]",
        "[text(3,1):[:]",
        "[text(3,2):fred:]",
        "[text(3,6):]:]",
        "[text(3,7):: /url:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):fred:]",
        "[text(5,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>def
[fred]: /url</li>
</ul>
</li>
</ul>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_ordered_list_x():
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
\t[fred]: /url

[fred]"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[para(1,4):\n\t]",
        "[text(1,4):abc\n::\n]",
        "[text(2,2):[:]",
        "[text(2,3):fred:]",
        "[text(2,7):]:]",
        "[text(2,8):: /url:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
[fred]: /url</li>
</ol>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_within_ordered_list():
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
    [fred]: /url

[fred]"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n]",
        "[para(1,4):\n ]",
        "[text(1,4):abc\n::\n]",
        "[text(2,2):[:]",
        "[text(2,3):fred:]",
        "[text(2,7):]:]",
        "[text(2,8):: /url:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
[fred]: /url</li>
</ol>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_ordered_list_and_single_space():
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
 \t[fred]: /url

[fred]"""
    expected_tokens = [
        "[olist(1,1):.:1:3:: \n]",
        "[para(1,4):\n\t]",
        "[text(1,4):abc\n::\n]",
        "[text(2,2):[:]",
        "[text(2,3):fred:]",
        "[text(2,7):]:]",
        "[text(2,8):: /url:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
[fred]: /url</li>
</ol>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_ordered_list_and_spaces():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
  \t[fred]: /url

[fred]"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  \n]",
        "[para(1,4):\n\t]",
        "[text(1,4):abc\n::\n]",
        "[text(2,2):[:]",
        "[text(2,3):fred:]",
        "[text(2,7):]:]",
        "[text(2,8):: /url:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
[fred]: /url</li>
</ol>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_ordered_double_list_x():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t  [fred]: /url

[fred]"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\t  \n]",
        "[para(2,7):\n]",
        "[text(2,7):def\n::\n]",
        "[text(3,1):[:]",
        "[text(3,2):fred:]",
        "[text(3,6):]:]",
        "[text(3,7):: /url:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):fred:]",
        "[text(5,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
[fred]: /url</li>
</ol>
</li>
</ol>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_ordered_double_list_no_spaces():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t[fred]: /url

[fred]"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n]",
        "[para(2,7):\n\t]",
        "[text(2,7):def\n::\n]",
        "[text(3,2):[:]",
        "[text(3,3):fred:]",
        "[text(3,7):]:]",
        "[text(3,8):: /url:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):fred:]",
        "[text(5,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
[fred]: /url</li>
</ol>
</li>
</ol>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_ordered_double_list_tab_after_indent():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
   \t[fred]:\t/url\t

[fred]"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n]",
        "[para(2,7):\n   \t:\t]",
        "[text(2,7):def\n::\n]",
        "[text(3,5):[:]",
        "[text(3,6):fred:]",
        "[text(3,10):]:]",
        "[text(3,11)::\t/url:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):fred:]",
        "[text(5,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
[fred]:\t/url</li>
</ol>
</li>
</ol>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_ordered_double_list_one_space():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t [fred]: /url

[fred]"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n]",
        "[para(2,7):\n\t ]",
        "[text(2,7):def\n::\n]",
        "[text(3,3):[:]",
        "[text(3,4):fred:]",
        "[text(3,8):]:]",
        "[text(3,9):: /url:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):fred:]",
        "[text(5,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
[fred]: /url</li>
</ol>
</li>
</ol>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_ordered_double_list_only_spaces():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
    [fred]: /url

[fred]"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n]",
        "[para(2,7):\n    ]",
        "[text(2,7):def\n::\n]",
        "[text(3,5):[:]",
        "[text(3,6):fred:]",
        "[text(3,10):]:]",
        "[text(3,11):: /url:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):fred:]",
        "[text(5,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
[fred]: /url</li>
</ol>
</li>
</ol>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_formfeeds_before_within_list():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
 \u000C \u000C[fred]: /url

[fred]"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n]",
        "[para(1,3):\n ]",
        "[text(1,3):abc\n\u000C \u000C::\n]",
        "[text(2,5):[:]",
        "[text(2,6):fred:]",
        "[text(2,10):]:]",
        "[text(2,11):: /url:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
        "[para(4,1):]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
\u000C \u000C[fred]: /url</li>
</ul>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_within_double_block_quotes_with_zero_and_zero_spaces_at_start():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
[fred]: /url

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n]",
        "[text(2,5):def\n::\n]",
        "[text(3,1):[:]",
        "[text(3,2):fred:]",
        "[text(3,6):]:]",
        "[text(3,7):: /url:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):fred:]",
        "[text(5,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
[fred]: /url</p>
</blockquote>
</blockquote>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_within_double_block_quotes_with_zero_and_one_space_at_start():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
 [fred]: /url

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n ]",
        "[text(2,5):def\n::\n]",
        "[text(3,2):[:]",
        "[text(3,3):fred:]",
        "[text(3,7):]:]",
        "[text(3,8):: /url:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):fred:]",
        "[text(5,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
[fred]: /url</p>
</blockquote>
</blockquote>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_within_double_block_quotes_with_zero_and_two_spaces_at_start():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
  [fred]: /url

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n  ]",
        "[text(2,5):def\n::\n]",
        "[text(3,3):[:]",
        "[text(3,4):fred:]",
        "[text(3,8):]:]",
        "[text(3,9):: /url:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):fred:]",
        "[text(5,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
[fred]: /url</p>
</blockquote>
</blockquote>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_within_double_block_quotes_with_zero_and_three_spaces_at_start():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
   [fred]: /url

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n   ]",
        "[text(2,5):def\n::\n]",
        "[text(3,4):[:]",
        "[text(3,5):fred:]",
        "[text(3,9):]:]",
        "[text(3,10):: /url:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):fred:]",
        "[text(5,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
[fred]: /url</p>
</blockquote>
</blockquote>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_within_double_block_quotes_with_zero_and_four_spaces_at_start():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    test_whitespaces_lrd_with_spaces_before_within_double_block_quotes()


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_x1():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
\t[fred]: /url
[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):\n\n\t\n]",
        "[text(1,3):abc\ndef\n::\n\n]",
        "[text(3,2):[:]",
        "[text(3,3):fred:]",
        "[text(3,7):]:]",
        "[text(3,8):: /url\n::\n]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
[fred]: /url
[fred]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_x2():
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
  \t[fred]: /url

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):\n\n  \t]",
        "[text(1,3):abc\ndef\n::\n\n]",
        "[text(3,4):[:]",
        "[text(3,5):fred:]",
        "[text(3,9):]:]",
        "[text(3,10):: /url:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):fred:]",
        "[text(5,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
[fred]: /url</p>
</blockquote>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_repeat():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>\t[fred]: /url1
>\t[barney]: /url2

[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>\n]",
        "[para(1,3):\n\n\t\n\t]",
        "[text(1,3):abc\ndef\n::\n\n]",
        "[text(3,3):[:]",
        "[text(3,4):fred:]",
        "[text(3,8):]:]",
        "[text(3,9):: /url1\n::\n]",
        "[text(4,3):[:]",
        "[text(4,4):barney:]",
        "[text(4,10):]:]",
        "[text(4,11):: /url2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[para(6,1):\n]",
        "[text(6,1):[:]",
        "[text(6,2):fred:]",
        "[text(6,6):]:]",
        "[text(6,7):\n::\n]",
        "[text(7,1):[:]",
        "[text(7,2):barney:]",
        "[text(7,8):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
[fred]: /url1
[barney]: /url2</p>
</blockquote>
<p>[fred]
[barney]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\t[fred]: /url1
>\t[barney]: /url2
[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[link-ref-def(1,5):True:\t:fred:: :/url1:::::]",
        "[link-ref-def(2,5):True:\t:barney:: :/url2:::::]",
        "[end-block-quote:::True]",
        "[para(3,1):\n]",
        "[link(3,1):shortcut:/url1:::::fred:False::::]",
        "[text(3,2):fred:]",
        "[end-link::]",
        "[text(3,7):\n::\n]",
        "[link(4,1):shortcut:/url2:::::barney:False::::]",
        "[text(4,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1">fred</a>
<a href="/url2">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]: /url1
> \t[barney]: /url2
[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[link-ref-def(1,5):True:\t:fred:: :/url1:::::]",
        "[link-ref-def(2,5):True:\t:barney:: :/url2:::::]",
        "[end-block-quote:::True]",
        "[para(3,1):\n]",
        "[link(3,1):shortcut:/url1:::::fred:False::::]",
        "[text(3,2):fred:]",
        "[end-link::]",
        "[text(3,7):\n::\n]",
        "[link(4,1):shortcut:/url2:::::barney:False::::]",
        "[text(4,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1">fred</a>
<a href="/url2">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_many_tabs():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\t[fred]:\t/url1\t
>\t[barney]:\t/url2\t
[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[link-ref-def(1,5):True:\t:fred::\t:/url1::\t:::]",
        "[link-ref-def(2,5):True:\t:barney::\t:/url2::\t:::]",
        "[end-block-quote:::True]",
        "[para(3,1):\n]",
        "[link(3,1):shortcut:/url1:::::fred:False::::]",
        "[text(3,2):fred:]",
        "[end-link::]",
        "[text(3,7):\n::\n]",
        "[link(4,1):shortcut:/url2:::::barney:False::::]",
        "[text(4,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1">fred</a>
<a href="/url2">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


###


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_within_block_quote_just_enough():
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> def
   [fred]: /url
[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):\n\n   \n]",
        "[text(1,3):abc\ndef\n::\n\n]",
        "[text(3,4):[:]",
        "[text(3,5):fred:]",
        "[text(3,9):]:]",
        "[text(3,10):: /url\n::\n]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
[fred]: /url
[fred]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_within_block_quote_bare():
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """> [fred]: /url
> [fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[link-ref-def(1,3):True::fred:: :/url:::::]",
        "[para(2,3):]",
        "[link(2,3):shortcut:/url:::::fred:False::::]",
        "[text(2,4):fred:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><a href="/url">fred</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_1a():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\t[fred]: /url1
>\t[barney]: /url2

[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[link-ref-def(1,5):True:\t:fred:: :/url1:::::]",
        "[link-ref-def(2,5):True:\t:barney:: :/url2:::::]",
        "[end-block-quote:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[link(4,1):shortcut:/url1:::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[text(4,7):\n::\n]",
        "[link(5,1):shortcut:/url2:::::barney:False::::]",
        "[text(5,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1">fred</a>
<a href="/url2">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_1b():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\t[fred]: /url1 "title"
>\t[barney]: /url2 "other title"
[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        '[link-ref-def(1,5):True:\t:fred:: :/url1:: :title:"title":]',
        '[link-ref-def(2,5):True:\t:barney:: :/url2:: :other title:"other title":]',
        "[end-block-quote:::True]",
        "[para(3,1):\n]",
        "[link(3,1):shortcut:/url1:title::::fred:False::::]",
        "[text(3,2):fred:]",
        "[end-link::]",
        "[text(3,7):\n::\n]",
        "[link(4,1):shortcut:/url2:other title::::barney:False::::]",
        "[text(4,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1" title="title">fred</a>
<a href="/url2" title="other title">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_1c():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\t[fred]: /url1 "title"
>\t[barney]: /url2 "other title"

[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n]",
        '[link-ref-def(1,5):True:\t:fred:: :/url1:: :title:"title":]',
        '[link-ref-def(2,5):True:\t:barney:: :/url2:: :other title:"other title":]',
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[link(4,1):shortcut:/url1:title::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[text(4,7):\n::\n]",
        "[link(5,1):shortcut:/url2:other title::::barney:False::::]",
        "[text(5,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1" title="title">fred</a>
<a href="/url2" title="other title">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_2a():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\t[fred]:\t/url1\t
>\t[barney]:\t/url2\t

[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[link-ref-def(1,5):True:\t:fred::\t:/url1::\t:::]",
        "[link-ref-def(2,5):True:\t:barney::\t:/url2::\t:::]",
        "[end-block-quote:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[link(4,1):shortcut:/url1:::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[text(4,7):\n::\n]",
        "[link(5,1):shortcut:/url2:::::barney:False::::]",
        "[text(5,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1">fred</a>
<a href="/url2">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_2b():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\t[fred]:\t/url1\t"title"\t
>\t[barney]:\t/url2\t"other title"\t
[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        '[link-ref-def(1,5):True:\t:fred::\t:/url1::\t:title:"title":\t]',
        '[link-ref-def(2,5):True:\t:barney::\t:/url2::\t:other title:"other title":\t]',
        "[end-block-quote:::True]",
        "[para(3,1):\n]",
        "[link(3,1):shortcut:/url1:title::::fred:False::::]",
        "[text(3,2):fred:]",
        "[end-link::]",
        "[text(3,7):\n::\n]",
        "[link(4,1):shortcut:/url2:other title::::barney:False::::]",
        "[text(4,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1" title="title">fred</a>
<a href="/url2" title="other title">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_2c():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\t[fred]:\t/url1\t"title"\t
>\t[barney]:\t/url2\t"other title"\t

[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n]",
        '[link-ref-def(1,5):True:\t:fred::\t:/url1::\t:title:"title":\t]',
        '[link-ref-def(2,5):True:\t:barney::\t:/url2::\t:other title:"other title":\t]',
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[link(4,1):shortcut:/url1:title::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[text(4,7):\n::\n]",
        "[link(5,1):shortcut:/url2:other title::::barney:False::::]",
        "[text(5,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1" title="title">fred</a>
<a href="/url2" title="other title">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_repeat_3():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\t[fred]:\t/url1\t
>\t[barney]:\t/url2\t
>\t[fred]
>\t[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>\n>]",
        "[link-ref-def(1,5):True:\t:fred::\t:/url1::\t:::]",
        "[link-ref-def(2,5):True:\t:barney::\t:/url2::\t:::]",
        "[para(3,5):\t\n\t]",
        "[link(3,5):shortcut:/url1:::::fred:False::::]",
        "[text(3,6):fred:]",
        "[end-link::]",
        "[text(3,11):\n::\n]",
        "[link(4,3):shortcut:/url2:::::barney:False::::]",
        "[text(4,4):barney:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p><a href="/url1">fred</a>
<a href="/url2">barney</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_1a():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]: /url1
> \t[barney]: /url2

[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[link-ref-def(1,5):True:\t:fred:: :/url1:::::]",
        "[link-ref-def(2,5):True:\t:barney:: :/url2:::::]",
        "[end-block-quote:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[link(4,1):shortcut:/url1:::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[text(4,7):\n::\n]",
        "[link(5,1):shortcut:/url2:::::barney:False::::]",
        "[text(5,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1">fred</a>
<a href="/url2">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_1b():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]: /url1 "title"
> \t[barney]: /url2 "other title"
[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        '[link-ref-def(1,5):True:\t:fred:: :/url1:: :title:"title":]',
        '[link-ref-def(2,5):True:\t:barney:: :/url2:: :other title:"other title":]',
        "[end-block-quote:::True]",
        "[para(3,1):\n]",
        "[link(3,1):shortcut:/url1:title::::fred:False::::]",
        "[text(3,2):fred:]",
        "[end-link::]",
        "[text(3,7):\n::\n]",
        "[link(4,1):shortcut:/url2:other title::::barney:False::::]",
        "[text(4,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1" title="title">fred</a>
<a href="/url2" title="other title">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_1c():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]: /url1 "title"
> \t[barney]: /url2 "other title"

[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        '[link-ref-def(1,5):True:\t:fred:: :/url1:: :title:"title":]',
        '[link-ref-def(2,5):True:\t:barney:: :/url2:: :other title:"other title":]',
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[link(4,1):shortcut:/url1:title::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[text(4,7):\n::\n]",
        "[link(5,1):shortcut:/url2:other title::::barney:False::::]",
        "[text(5,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1" title="title">fred</a>
<a href="/url2" title="other title">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_2x():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t/url1\t
> \t[barney]:\t/url2\t
[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[link-ref-def(1,5):True:\t:fred::\t:/url1::\t:::]",
        "[link-ref-def(2,5):True:\t:barney::\t:/url2::\t:::]",
        "[end-block-quote:::True]",
        "[para(3,1):\n]",
        "[link(3,1):shortcut:/url1:::::fred:False::::]",
        "[text(3,2):fred:]",
        "[end-link::]",
        "[text(3,7):\n::\n]",
        "[link(4,1):shortcut:/url2:::::barney:False::::]",
        "[text(4,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1">fred</a>
<a href="/url2">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_2a():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t/url1\t
> \t[barney]:\t/url2\t

[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[link-ref-def(1,5):True:\t:fred::\t:/url1::\t:::]",
        "[link-ref-def(2,5):True:\t:barney::\t:/url2::\t:::]",
        "[end-block-quote:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[link(4,1):shortcut:/url1:::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[text(4,7):\n::\n]",
        "[link(5,1):shortcut:/url2:::::barney:False::::]",
        "[text(5,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1">fred</a>
<a href="/url2">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_2b():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t/url1\t"title"\t
> \t[barney]:\t/url2\t"other\ttitle"\t
[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        '[link-ref-def(1,5):True:\t:fred::\t:/url1::\t:title:"title":\t]',
        '[link-ref-def(2,5):True:\t:barney::\t:/url2::\t:other\ttitle:"other\ttitle":\t]',
        "[end-block-quote:::True]",
        "[para(3,1):\n]",
        "[link(3,1):shortcut:/url1:title::::fred:False::::]",
        "[text(3,2):fred:]",
        "[end-link::]",
        "[text(3,7):\n::\n]",
        "[link(4,1):shortcut:/url2:other\ttitle::::barney:False::::]",
        "[text(4,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1" title="title">fred</a>
<a href="/url2" title="other\ttitle">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_2c():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t/url1\t"title"\t
> \t[barney]:\t/url2\t"other\ttitle"\t

[fred]
[barney]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        '[link-ref-def(1,5):True:\t:fred::\t:/url1::\t:title:"title":\t]',
        '[link-ref-def(2,5):True:\t:barney::\t:/url2::\t:other\ttitle:"other\ttitle":\t]',
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[link(4,1):shortcut:/url1:title::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[text(4,7):\n::\n]",
        "[link(5,1):shortcut:/url2:other\ttitle::::barney:False::::]",
        "[text(5,2):barney:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url1" title="title">fred</a>
<a href="/url2" title="other\ttitle">barney</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_3x():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t/url1\t"abc"def
[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,5):\t\n]",
        "[text(1,5):[:]",
        "[text(1,6):fred:]",
        "[text(1,10):]:]",
        '[text(1,11)::\t/url1\t\a"\a&quot;\aabc\a"\a&quot;\adef\n::\n]',
        "[text(2,1):[:]",
        "[text(2,2):fred:]",
        "[text(2,6):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>[fred]:	/url1	&quot;abc&quot;def
[fred]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_3a():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t/url1\t"abc"def

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,5):\t]",
        "[text(1,5):[:]",
        "[text(1,6):fred:]",
        "[text(1,10):]:]",
        '[text(1,11)::\t/url1\t\a"\a&quot;\aabc\a"\a&quot;\adef:]',
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):fred:]",
        "[text(3,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>[fred]:	/url1	&quot;abc&quot;def</p>
</blockquote>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_4x():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t/url1\t"abc
[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,5):\t\n]",
        "[text(1,5):[:]",
        "[text(1,6):fred:]",
        "[text(1,10):]:]",
        '[text(1,11)::\t/url1\t\a"\a&quot;\aabc\n::\n]',
        "[text(2,1):[:]",
        "[text(2,2):fred:]",
        "[text(2,6):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>[fred]:\t/url1\t&quot;abc
[fred]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_4a():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t/url1\t"abc

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,5):\t]",
        "[text(1,5):[:]",
        "[text(1,6):fred:]",
        "[text(1,10):]:]",
        '[text(1,11)::\t/url1\t\a"\a&quot;\aabc:]',
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):fred:]",
        "[text(3,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>[fred]:\t/url1\t&quot;abc</p>
</blockquote>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_5x():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t</url1
[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,5):\t\n]",
        "[text(1,5):[:]",
        "[text(1,6):fred:]",
        "[text(1,10):]:]",
        "[text(1,11)::\t\a<\a&lt;\a/url1\n::\n]",
        "[text(2,1):[:]",
        "[text(2,2):fred:]",
        "[text(2,6):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>[fred]:\t&lt;/url1
[fred]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_5a():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t</url1

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,5):\t]",
        "[text(1,5):[:]",
        "[text(1,6):fred:]",
        "[text(1,10):]:]",
        "[text(1,11)::\t\a<\a&lt;\a/url1:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):fred:]",
        "[text(3,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>[fred]:\t&lt;/url1</p>
</blockquote>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_6():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t
[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,5):\t\n]",
        "[text(1,5):[:]",
        "[text(1,6):fred:]",
        "[text(1,10):]:]",
        "[text(1,11)::\n::\t\n]",
        "[text(2,1):[:]",
        "[text(2,2):fred:]",
        "[text(2,6):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>[fred]:	
[fred]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_with_space_repeat_6a():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,5):\t:\t]",
        "[text(1,5):[:]",
        "[text(1,6):fred:]",
        "[text(1,10):]:]",
        "[text(1,11):::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):fred:]",
        "[text(3,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>[fred]:</p>
</blockquote>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1xx():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t
> \t/url\t

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[link-ref-def(1,5):True:\t:fred::\t\n\t:/url::\t:::]",
        "[end-block-quote:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[link(4,1):shortcut:/url:::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1xa():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:
> \t/url

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[link-ref-def(1,5):True:\t:fred::\n\t:/url:::::]",
        "[end-block-quote:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[link(4,1):shortcut:/url:::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1xb():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> [fred]:\t
> /url\t

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[link-ref-def(1,3):True::fred::\t\n:/url::\t:::]",
        "[end-block-quote:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[link(4,1):shortcut:/url:::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1a():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\t[fred]:\t
> \t/url\t

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> ]",
        "[link-ref-def(1,5):True:\t:fred::\t\n\t:/url::\t:::]",
        "[end-block-quote:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[link(4,1):shortcut:/url:::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1b():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t
>\t/url\t

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>]",
        "[link-ref-def(1,5):True:\t:fred::\t\n\t:/url::\t:::]",
        "[end-block-quote:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[link(4,1):shortcut:/url:::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1c():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\t[fred]:\t
>\t/url\t

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[link-ref-def(1,5):True:\t:fred::\t\n\t:/url::\t:::]",
        "[end-block-quote:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[link(4,1):shortcut:/url:::::fred:False::::]",
        "[text(4,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1d():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
>\t[fred]:\t
>\t/url\t

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n>\n]",
        "[para(1,3):\n\t\n\t:\t]",
        "[text(1,3):abc\n::\n]",
        "[text(2,3):[:]",
        "[text(2,4):fred:]",
        "[text(2,8):]:]",
        "[text(2,9)::\n/url::\t\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):fred:]",
        "[text(5,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
[fred]:	
/url</p>
</blockquote>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1ea():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
>
>\t[fred]:\t
>\t/url\t

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n>]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n>]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[end-block-quote:::True]",
        "[link-ref-def(4,5):True:\t:fred::\t\n\t:/url::\t:::]",
        "[end-block-quote:::False]",
        "[BLANK(6,1):]",
        "[para(7,1):]",
        "[link(7,1):shortcut:/url:::::fred:False::::]",
        "[text(7,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_two_lines_1f():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
>
> 	[fred]:	
> 	/url	
> abc

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> \n> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[link-ref-def(3,5):True:\t:fred::\t\n\t:/url::\t:::]",
        "[para(5,3):]",
        "[text(5,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[para(7,1):]",
        "[link(7,1):shortcut:/url:::::fred:False::::]",
        "[text(7,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<p>abc</p>
</blockquote>
<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_more_lines_2x():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t[fred]:\t
> \t/url\t
> \t"title"\t

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        '[link-ref-def(1,5):True:\t:fred::\t\n\t:/url::\t\n\t:title:"title":\t]',
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[link(5,1):shortcut:/url:title::::fred:False::::]",
        "[text(5,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_more_lines_2a():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
>
> \t[fred]:\t
> \t/url\t
> \t"title"\t
> abc

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> \n> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        '[link-ref-def(3,5):True:\t:fred::\t\n\t:/url::\t\n\t:title:"title":\t]',
        "[para(6,3):]",
        "[text(6,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[para(8,1):]",
        "[link(8,1):shortcut:/url:title::::fred:False::::]",
        "[text(8,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<p>abc</p>
</blockquote>
<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_more_lines_2b():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
>
> \t[fred]:\t
> \t/url\t
> \t"title"\t
> abc

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> \n> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        '[link-ref-def(3,5):True:\t:fred::\t\n\t:/url::\t\n\t:title:"title":\t]',
        "[para(6,3):]",
        "[text(6,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[para(8,1):]",
        "[link(8,1):shortcut:/url:title::::fred:False::::]",
        "[text(8,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<p>abc</p>
</blockquote>
<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_more_lines_3x():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
>
> \t[fred]:\t
> \t/url\t
> \t"times\t
> \tnew\troman\t
> abc

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> \n> \n> \n> \n> \n> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[link-ref-def(3,5):True:\t:fred::\t\n\t:/url::\t:::]",
        "[para(5,5):\t\n\t\n]",
        '[text(5,5):\a"\a&quot;\atimes\nnew\troman\nabc::\t\n\t\n]',
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[para(9,1):]",
        "[link(9,1):shortcut:/url:::::fred:False::::]",
        "[text(9,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<p>&quot;times	
new	roman	
abc</p>
</blockquote>
<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_more_lines_3a():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
>
> \t[fred]:\t
> \t</url\t
> abc

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[para(3,5):\t\n\t\n]",
        "[text(3,5):[:]",
        "[text(3,6):fred:]",
        "[text(3,10):]:]",
        "[text(3,11)::\n\a<\a&lt;\a/url\nabc::\t\n\t\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[para(7,1):]",
        "[text(7,1):[:]",
        "[text(7,2):fred:]",
        "[text(7,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<p>[fred]:	
&lt;/url	
abc</p>
</blockquote>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_more_lines_3b():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
>
> \t[fred]:\t

[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[para(3,5):\t:\t]",
        "[text(3,5):[:]",
        "[text(3,6):fred:]",
        "[text(3,10):]:]",
        "[text(3,11):::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):fred:]",
        "[text(5,6):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<p>[fred]:</p>
</blockquote>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_double_block_quotes():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
\t[fred]: /url
[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n\t\n]",
        "[text(2,5):def\n::\n]",
        "[text(3,2):[:]",
        "[text(3,3):fred:]",
        "[text(3,7):]:]",
        "[text(3,8):: /url\n::\n]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
[fred]: /url
[fred]</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_double_block_quotes_with_single():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
>\t[fred]: /url
[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n>\n]",
        "[para(2,5):\n\t\n]",
        "[text(2,5):def\n::\n]",
        "[text(3,3):[:]",
        "[text(3,4):fred:]",
        "[text(3,8):]:]",
        "[text(3,9):: /url\n::\n]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
[fred]: /url
[fred]</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_within_double_block_quotes_with_single_and_space():
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> \t[fred]: /url
[fred]"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> \n]",
        "[para(2,5):\n\t\n]",
        "[text(2,5):def\n::\n]",
        "[text(3,4):[:]",
        "[text(3,5):fred:]",
        "[text(3,9):]:]",
        "[text(3,10):: /url\n::\n]",
        "[text(4,1):[:]",
        "[text(4,2):fred:]",
        "[text(4,6):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
[fred]: /url
[fred]</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


###


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_label():
    """
    Test case:  LRD link label preceeded by spaces.
    """

    # Arrange
    source_markdown = """[  fred]: /url
[ fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:  fred: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url::::: fred:False::::]",
        "[text(2,2): fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url"> fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_label():
    """
    Test case:  LRD link label preceeded by tabs.
    """

    # Arrange
    source_markdown = """[\t\tfred]: /url
[ fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:\t\tfred: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url::::: fred:False::::]",
        "[text(2,2): fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url"> fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_before_label():
    """
    Test case:  LRD link label preceeded by form feeds.
    """

    # Arrange
    source_markdown = """[\u000cfred]: /url
[ fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:\u000cfred: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url::::: fred:False::::]",
        "[text(2,2): fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url"> fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_after_label():
    """
    Test case:  LRD link label followed by spaces.
    """

    # Arrange
    source_markdown = """[fred  ]: /url
[fred ]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:fred  : :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred :False::::]",
        "[text(2,2):fred :]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred </a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_after_label():
    """
    Test case:  LRD link label followwed by tabs.
    """

    # Arrange
    source_markdown = """[fred\t\t]: /url
[fred ]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:fred\t\t: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred :False::::]",
        "[text(2,2):fred :]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred </a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_after_label():
    """
    Test case:  LRD link label followed by form feeds.
    """

    # Arrange
    source_markdown = """[fred\u000c]: /url
[fred ]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:fred\u000c: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred :False::::]",
        "[text(2,2):fred :]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred </a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_in_label():
    """
    Test case:  LRD link label with spaces inside.
    """

    # Arrange
    source_markdown = """[fred  boy]: /url
[fred boy]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred boy:fred  boy: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred boy:False::::]",
        "[text(2,2):fred boy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred boy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_in_label():
    """
    Test case:  LRD link label followwed by tabs.
    """

    # Arrange
    source_markdown = """[fred\t\tboy]: /url
[fred boy]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred boy:fred\t\tboy: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred boy:False::::]",
        "[text(2,2):fred boy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred boy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_in_label():
    """
    Test case:  LRD link label followed by form feeds.
    """

    # Arrange
    source_markdown = """[fred\u000c\u000cboy]: /url
[fred boy]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred boy:fred\u000c\u000cboy: :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred boy:False::::]",
        "[text(2,2):fred boy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred boy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_destination():
    """
    Test case:  LRD destination preceeded by spaces.
    """

    # Arrange
    source_markdown = """[fred]:  /url
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred::  :/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_destination():
    """
    Test case:  LRD destination preceeded by tabs.
    """

    # Arrange
    source_markdown = """[fred]:\t/url
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred::\t:/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_before_destination():
    """
    Test case:  LRD destination preceeded by form feeds.
    """

    # Arrange
    source_markdown = """[fred]:\u000c/url
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred::\u000c:/url:::::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_after_destination():
    """
    Test case:  LRD destination followed by spaces.
    """

    # Arrange
    source_markdown = """[fred]: /url  
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:: :/url::  :::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_after_destination():
    """
    Test case:  LRD destination followed by tabs.
    """

    # Arrange
    source_markdown = """[fred]: /url\t\t
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:: :/url::\t\t:::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_after_destination():
    """
    Test case:  LRD destination followed by form feeds.
    """

    # Arrange
    source_markdown = """[fred]: /url\u000c\u000c
[fred]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::fred:: :/url::\u000c\u000c:::]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_before_title():
    """
    Test case:  LRD title preceeded by spaces.
    """

    # Arrange
    source_markdown = """[fred]: /url "title"
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url:: :title:"title":]',
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:title::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_before_title():
    """
    Test case:  LRD title preceeded by tabs.
    """

    # Arrange
    source_markdown = """[fred]: /url\t"title"
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url::\t:title:"title":]',
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:title::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_before_title():
    """
    Test case:  LRD title preceeded by form feeds.
    """

    # Arrange
    source_markdown = """[fred]: /url\u000c"title"
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url::\u000c:title:"title":]',
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:title::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_spaces_after_title():
    """
    Test case:  LRD title followed by spaces.
    """

    # Arrange
    source_markdown = """[fred]: /url "title"   
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url:: :title:"title":   ]',
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:title::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_tabs_after_title():
    """
    Test case:  LRD title followed by tabs.
    """

    # Arrange
    source_markdown = """[fred]: /url "title"\t\t
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url:: :title:"title":\t\t]',
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:title::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_lrd_with_form_feeds_after_title():
    """
    Test case:  LRD title followed by form feeds.
    """

    # Arrange
    source_markdown = """[fred]: /url "title"\u000c\u000c
[fred]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::fred:: :/url:: :title:"title":\u000c\u000c]',
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:title::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
