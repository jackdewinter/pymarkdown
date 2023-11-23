"""
Testing various aspects of whitespaces around html blocks.
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_html_with_spaces_before():
    """
    Test case:  Html blocks closed followed by spaces.
    """

    # Arrange
    source_markdown = """   <!-- comment"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,4):<!-- comment:   ]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """   <!-- comment"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_too_many_spaces_before():
    """
    Test case:  Html blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """abc
    <!-- comment"""
    expected_tokens = [
        "[para(1,1):\n    ]",
        "[text(1,1):abc\n\a<\a&lt;\a!-- comment::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
&lt;!-- comment</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t<!-- comment"""
    expected_tokens = [
        "[icode-block(1,5): \t:]",
        "[text(1,5):\a<\a&lt;\a!-- comment:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>&lt;!-- comment
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_repeat():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t <!-- comment
  \t <!-- comment"""
    expected_tokens = [
        "[icode-block(1,5): \t:\n  \t]",
        "[text(1,5): \a<\a&lt;\a!-- comment\n \a<\a&lt;\a!-- comment:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code> &lt;!-- comment
 &lt;!-- comment
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_form_feeds_before():
    """
    Test case:  Html blocks preceeded by spaces and form feeds.
    """

    # Arrange
    source_markdown = """ \u000C <!-- comment"""
    expected_tokens = [
        "[para(1,2): \u000C ]",
        "[text(1,2):\a<\a&lt;\a!-- comment:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;!-- comment</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_spaces_before_within_list():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
    <!-- comment"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,5):<!-- comment:  ]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
  <!-- comment
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_spaces_before_within_block_quotes():
    """
    Test case:  Html blocks closed followed by spaces.
    """

    # Arrange
    source_markdown = """> abc
> def
    <!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n    ]",
        "[text(1,3):abc\ndef\n\a<\a&lt;\a!-- comment::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
&lt;!-- comment</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_spaces_before_within_double_block_quotes():
    """
    Test case:  Html blocks closed followed by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
    <!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n    ]",
        "[text(2,5):def\n\a<\a&lt;\a!-- comment::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
&lt;!-- comment</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_spaces_before_within_double_block_quotes_with_single():
    """
    Test case:  Html blocks closed followed by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   <!-- comment"""
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
        "[html-block(3,3)]",
        "[text(3,5):<!-- comment:  ]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
  <!-- comment
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_unordered_list_x():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
\t<!-- comment"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
\a<!-- comment
</li>
</ul>""".replace(
        "\a", "\t"
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_unordered_list_and_single_space():
    """
    Test case:  Html blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc
 \t<!-- comment"""
    expected_tokens = [
        "[ulist(1,1):-::2:: ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
\a<!-- comment
</li>
</ul>""".replace(
        "\a", "\t"
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_unordered_list_and_spaces():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  \t<!-- comment"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
\t<!-- comment
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_blockquote_and_unordered_list_minus_space():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """> - abc
>\t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>]",
        "[ulist(1,3):-::4::\t]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::False]",
        "[html-block(2,5)]",
        "[text(2,5):<!-- comment:]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>abc
<!-- comment
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_blockquote_and_unordered_list_no_spaces():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """> - abc
> \t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):-::4::\t]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::False]",
        "[html-block(2,5)]",
        "[text(2,5):<!-- comment:]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>abc
<!-- comment
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_blockquote_and_unordered_list_one_space():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """> - abc
>  \t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):-::4:: \t]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::False]",
        "[html-block(2,5)]",
        "[text(2,5):<!-- comment:]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>abc
<!-- comment
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_unordered_double_list():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  - def
\t<!-- comment"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :\t]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::False]",
        "[html-block(3,5)]",
        "[text(3,5):<!-- comment:]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>def
<!-- comment
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_list_x():
    """
    Test case:  Html blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
\t<!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[html-block(2,4)]",
        "[text(2,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
\a<!-- comment
</li>
</ol>""".replace(
        "\a", "\t"
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_spaces_before_within_ordered_list():
    """
    Test case:  Html blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
    <!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[html-block(2,4)]",
        "[text(2,5):<!-- comment: ]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
 <!-- comment
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_list_and_single_space():
    """
    Test case:  Html blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
 \t<!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3:: ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[html-block(2,4)]",
        "[text(2,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
\a<!-- comment
</li>
</ol>""".replace(
        "\a", "\t"
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_list_and_spaces():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
  \t<!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[html-block(2,4)]",
        "[text(2,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
\a<!-- comment
</li>
</ol>""".replace(
        "\a", "\t"
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_list_and_spaces2():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   \t<!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[html-block(2,4)]",
        "[text(2,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
\a<!-- comment
</li>
</ol>""".replace(
        "\a", "\t"
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_x():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t  <!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\t  ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[html-block(3,7)]",
        "[text(3,7):<!-- comment:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
<!-- comment
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_no_spaces():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t<!-- comment"""
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
        "[html-block(3,4)]",
        "[text(3,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
\t<!-- comment
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_tab_after_indent():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
   <!-- comment\there"""
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
        "[html-block(3,4)]",
        "[text(3,4):<!-- comment\there:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<!-- comment\there
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_one_space():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t <!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   : ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,4)]",
        "[text(3,6):<!-- comment:\t ]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
\t <!-- comment
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_one_before_none_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
 \t<!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3:: ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,4)]",
        "[text(3,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
\t<!-- comment
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_one_before_two_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
 \t  <!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   : \t  ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[html-block(3,7)]",
        "[text(3,7):<!-- comment:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
<!-- comment
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_two_before_none_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
  \t<!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,4)]",
        "[text(3,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
\t<!-- comment
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_two_before_two_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
 \t  <!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   : \t  ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[html-block(3,7)]",
        "[text(3,7):<!-- comment:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
<!-- comment
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_three_before_none_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
   \t<!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,4)]",
        "[text(3,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
\t<!-- comment
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_three_before_two_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
   \t  <!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :   \t  ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[html-block(3,7)]",
        "[text(3,7):<!-- comment:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
<!-- comment
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_four_before():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
    \t<!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   : ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[html-block(3,7)]",
        "[text(3,9):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
\t<!-- comment
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_five_before():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
     \t<!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   : ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[html-block(3,7)]",
        "[text(3,9):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
\t<!-- comment
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_six_before():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
      \t<!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :      ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[html-block(3,7)]",
        "[text(3,9):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
\t<!-- comment
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quote_ordered_double_list_zero_before_zero_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> 1. abc
>    1. def
>\t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>]",
        "[olist(1,3):.:1:5:]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[olist(2,6):.:1:8:   : ]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,3)]",
        "[text(3,5):<!-- comment:\a\t\a  \a]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>abc
<ol>
<li>def</li>
</ol>
</li>
</ol>
  <!-- comment
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quote_ordered_double_list_zero_before_double_zero_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> 1. abc
>    1. def
>\t\t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>]",
        "[olist(1,3):.:1:5:]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[olist(2,6):.:1:8:   :\t\t]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::False]",
        "[html-block(3,9)]",
        "[text(3,9):<!-- comment:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>abc
<ol>
<li>def
<!-- comment
</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quote_ordered_double_list_one_before_zero_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> 1. abc
>    1. def
> \t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[olist(2,6):.:1:8:   :  ]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,3)]",
        "[text(3,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>abc
<ol>
<li>def</li>
</ol>
</li>
</ol>
\a<!-- comment
</blockquote>""".replace(
        "\a", "\t"
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quote_ordered_double_list_one_before_one_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> 1. abc
>    1. def
> \t <!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[olist(1,3):.:1:5::\t ]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[olist(2,6):.:1:8:   :   ]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,6)]",
        "[text(3,6):<!-- comment:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<!-- comment
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quote_ordered_double_list_one_before_two_after_x():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> 1. abc
>    1. def
> \t  <!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[olist(1,3):.:1:5::\t ]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[olist(2,6):.:1:8:   :    ]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,6)]",
        "[text(3,7):<!-- comment: ]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>abc
<ol>
<li>def</li>
</ol>
 <!-- comment
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quote_ordered_double_list_one_before_two_after_y():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> 1. abc
>    1. def
>     <!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[olist(1,3):.:1:5::   ]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[olist(2,6):.:1:8:   :    ]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,6)]",
        "[text(3,7):<!-- comment: ]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>abc
<ol>
<li>def</li>
</ol>
 <!-- comment
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quote_ordered_double_list_one_before_three_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> 1. abc
>    1. def
> \t   <!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[olist(1,3):.:1:5::\t ]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[olist(2,6):.:1:8:   :     ]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,6)]",
        "[text(3,8):<!-- comment:  ]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>abc
<ol>
<li>def</li>
</ol>
  <!-- comment
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quote_ordered_double_list_one_before_four_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> 1. abc
>    1. def
> \t    <!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[olist(2,6):.:1:8:   :\t    ]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::False]",
        "[html-block(3,9)]",
        "[text(3,9):<!-- comment:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>abc
<ol>
<li>def
<!-- comment
</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quote_ordered_double_list_two_before_zero_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> 1. abc
>    1. def
>  \t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[olist(2,6):.:1:8:   :  ]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,3)]",
        "[text(3,5):<!-- comment: \t]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>abc
<ol>
<li>def</li>
</ol>
</li>
</ol>
 \a<!-- comment
</blockquote>""".replace(
        "\a", "\t"
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quote_ordered_double_list_two_before_one_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> 1. abc
>    1. def
>  \t <!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[olist(1,3):.:1:5:: \t ]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[olist(2,6):.:1:8:   :   ]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,6)]",
        "[text(3,6):<!-- comment:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<!-- comment
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quote_ordered_double_list_two_before_two_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> 1. abc
>    1. def
>  \t  <!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[olist(1,3):.:1:5:: \t ]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[olist(2,6):.:1:8:   :    ]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,6)]",
        "[text(3,7):<!-- comment: ]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>abc
<ol>
<li>def</li>
</ol>
 <!-- comment
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quote_ordered_double_list_two_before_three_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> 1. abc
>    1. def
>  \t   <!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[olist(1,3):.:1:5:: \t ]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[olist(2,6):.:1:8:   :     ]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,6)]",
        "[text(3,8):<!-- comment:  ]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>abc
<ol>
<li>def</li>
</ol>
  <!-- comment
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quote_ordered_double_list_three_before_zero_after():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> 1. abc
>    1. def
>   \t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[olist(2,6):.:1:8:   :  \t]",
        "[para(2,9):]",
        "[text(2,9):def:]",
        "[end-para:::False]",
        "[html-block(3,9)]",
        "[text(3,9):<!-- comment:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>abc
<ol>
<li>def
<!-- comment
</li>
</ol>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_only_spaces_beta():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
     <!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,4)]",
        "[text(3,6):<!-- comment:  ]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
  <!-- comment
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_ordered_double_list_only_spaces():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
    <!-- comment"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,4)]",
        "[text(3,5):<!-- comment: ]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
 <!-- comment
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_formfeeds_before_within_list():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
 \u000C \u000C<!-- comment"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n ]",
        "[text(1,3):abc\n\u000C \u000C\a<\a&lt;\a!-- comment::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
\u000C \u000C&lt;!-- comment</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_spaces_before_within_double_block_quotes_with_zero_and_zero_spaces_at_start():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
<!-- comment"""
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
        "[html-block(3,1)]",
        "[text(3,1):<!-- comment:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<!-- comment"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_spaces_before_within_double_block_quotes_with_zero_and_one_space_at_start():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
 <!-- comment"""
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
        "[html-block(3,1)]",
        "[text(3,2):<!-- comment: ]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
 <!-- comment"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_spaces_before_within_double_block_quotes_with_zero_and_two_spaces_at_start():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
  <!-- comment"""
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
        "[html-block(3,1)]",
        "[text(3,3):<!-- comment:  ]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
  <!-- comment"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_spaces_before_within_double_block_quotes_with_zero_and_three_spaces_at_start():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
   <!-- comment"""
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
        "[html-block(3,1)]",
        "[text(3,4):<!-- comment:   ]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
   <!-- comment"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_spaces_before_within_double_block_quotes_with_zero_and_four_spaces_at_start():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    test_whitespaces_html_with_spaces_before_within_double_block_quotes()


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quotes_x1():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
\t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n\t]",
        "[text(1,3):abc\ndef\n\a<\a&lt;\a!-- comment::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
&lt;!-- comment</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quotes_x2():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
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
def test_whitespaces_html_with_tabs_before_within_block_quotes_repeat():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>\t<!-- comment -->
>\t<!-- comment -->"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::False]",
        "[html-block(3,3)]",
        "[text(3,5):<!-- comment -->:\a\t\a  \a]",
        "[end-html-block:::False]",
        "[html-block(4,3)]",
        "[text(4,5):<!-- comment -->:\a\t\a  \a]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
  <!-- comment -->
  <!-- comment -->
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quotes_bare_repeat():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t<!-- comment -->
>\t<!-- comment -->"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[html-block(1,3)]",
        "[text(1,5):<!-- comment -->:\a\t\a  \a]",
        "[end-html-block:::False]",
        "[html-block(2,3)]",
        "[text(2,5):<!-- comment -->:\a\t\a  \a]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
  <!-- comment -->
  <!-- comment -->
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quotes_bare_with_space_repeat():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """> \t<!-- comment -->
> \t<!-- comment -->"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[html-block(1,3)]",
        "[text(1,5):<!-- comment -->:\t]",
        "[end-html-block:::False]",
        "[html-block(2,3)]",
        "[text(2,5):<!-- comment -->:\t]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
\t<!-- comment -->
\t<!-- comment -->
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_block_quotes_bare_with_many_tabs():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t<!--\tcomment\t
>\tcomment\t-->"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[html-block(1,3)]",
        "[text(1,5):<!--\tcomment\t\n\a\t\a  \acomment\t-->:\a\t\a  \a]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
  <!--	comment	
  comment	-->
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_double_block_quotes_1():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
\t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n\t]",
        "[text(2,5):def\n\a<\a&lt;\a!-- comment::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
&lt;!-- comment</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_double_block_quotes_2():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
 \t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n \t]",
        "[text(2,5):def\n\a<\a&lt;\a!-- comment::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
&lt;!-- comment</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_double_block_quotes_3():
    """
    Test case:  Html blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
  \t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n  \t]",
        "[text(2,5):def\n\a<\a&lt;\a!-- comment::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
&lt;!-- comment</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_double_block_quotes_with_single():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
>\t<!-- comment"""
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
        "[html-block(3,3)]",
        "[text(3,5):<!-- comment:\a\t\a  \a]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
  <!-- comment
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_within_double_block_quotes_with_single_and_space():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> \t<!-- comment"""
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
        "[html-block(3,3)]",
        "[text(3,5):<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
\t<!-- comment
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


###


@pytest.mark.gfm
def test_whitespaces_html_start_6_with_spaces_after():
    """
    Test case:  Html blocks type 6 followed by spaces.
    """

    # Arrange
    source_markdown = """<dialog  """
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<dialog  :]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<dialog  """

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_start_6_with_tabs_after():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """<dialog\t"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<dialog\t:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<dialog\t"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_start_6_with_form_feeds_after():
    """
    Test case:  HTML blocks followed by form feeds.
    """

    # Arrange
    source_markdown = """<dialog\u000c"""
    expected_tokens = [
        "[para(1,1)::\u000c]",
        "[text(1,1):\a<\a&lt;\adialog:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;dialog</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_start_7_with_spaces_after():
    """
    Test case:  Html blocks type 7 followed by spaces.
    """

    # Arrange
    source_markdown = """<dialog>  """
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<dialog>  :]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<dialog>  """

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_start_7_with_tabs_after():
    """
    Test case:  HTML block type 7 followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """<dialog>\t"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<dialog>\t:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<dialog>\t"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_start_7_with_tabs_within():
    """
    Test case:  HTML block type 7 followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """<dialog>
<something>\t</something>

"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<dialog>\n<something>\t</something>:]",
        "[end-html-block:::False]",
        "[BLANK(3,1):]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<dialog>
<something>\t</something>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_start_7_with_form_feeds_after():
    """
    Test case:  HTML blocks type 7 followed by form feeds.
    """

    # Arrange
    source_markdown = """<dialog>\u000c"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<dialog>\u000c:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<dialog>\u000c"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
