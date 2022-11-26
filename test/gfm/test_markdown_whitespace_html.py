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
    source_markdown = """  <!-- comment"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,3):<!-- comment:  ]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """  <!-- comment"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_spaces_before_in_block_quotes():
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
def test_whitespaces_html_with_spaces_before_in_double_block_quotes():
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
def test_whitespaces_html_with_spaces_before_in_double_block_quotes_with_single():
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
def test_whitespaces_html_with_tabs_before_inside_list():
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
def test_whitespaces_html_with_tabs_before_inside_block_quotes():
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
def test_whitespaces_html_with_tabs_before_inside_block_quotes_repeat():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>\t<!-- comment
>\t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::False]",
        "[html-block(3,3)]",
        "[text(3,5):<!-- comment\n\a\t\a  \a<!-- comment:\a\t\a  \a]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
  <!-- comment
  <!-- comment
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_inside_block_quotes_bare():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t<!-- comment
>\t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[html-block(1,3)]",
        "[text(1,5):<!-- comment\n\a\t\a  \a<!-- comment:\a\t\a  \a]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
  <!-- comment
  <!-- comment
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_inside_block_quotes_bare_1():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t<!--\tcomment\t
>\t<!--\tcomment\t"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[html-block(1,3)]",
        "[text(1,5):<!--\tcomment\t\n\a\t\a  \a<!--\tcomment\t:\a\t\a  \a]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
  <!--\tcomment\t
  <!--\tcomment\t
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_inside_block_quotes_bare_with_spaces():
    """
    Test case:  HTML block followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """> \t<!-- comment
> \t<!-- comment"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[html-block(1,3)]",
        "[text(1,5):<!-- comment\n\t<!-- comment:\t]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
\t<!-- comment
\t<!-- comment
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_with_tabs_before_inside_double_block_quotes():
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
def test_whitespaces_html_with_tabs_before_inside_double_block_quotes_with_single():
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
def test_whitespaces_html_with_tabs_before_inside_double_block_quotes_with_single_and_space():
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


@pytest.mark.gfm
def test_whitespaces_html_with_form_feeds_before():
    """
    Test case:  HTML blocks followed by form feeds.
    """

    # Arrange
    source_markdown = """ \u000C<!-- comment"""
    expected_tokens = [
        "[para(1,2): \u000C]",
        "[text(1,2):\a<\a&lt;\a!-- comment:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;!-- comment</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
