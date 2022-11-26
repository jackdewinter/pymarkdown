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
    source_markdown = """  a paragraph"""
    expected_tokens = [
        "[para(1,3):  ]",
        "[text(1,3):a paragraph:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>a paragraph</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_spaces_before_within_block_quote():
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
def test_whitespaces_paragraph_with_spaces_before_within_double_block_quote():
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
def test_whitespaces_paragraph_with_spaces_before_within_double_block_quote_with_single():
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
def test_whitespaces_paragraph_with_tabs_before():
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
def test_whitespaces_paragraph_with_tabs_before_within_block_quote():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
\ta paragraph"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n\t]",
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
def test_whitespaces_paragraph_with_tabs_before_within_block_quote_repeat():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>\ta paragraph
>\ta paragraph"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>]",
        "[para(1,3):\n\n\t\n\t]",
        "[text(1,3):abc\ndef\na paragraph\na paragraph::\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
a paragraph
a paragraph</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_block_quote_bare_repeat_x():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\ta paragraph
>\ta paragraph"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[para(1,5):\t\n\t]",
        "[text(1,5):a paragraph\na paragraph::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>a paragraph
a paragraph</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_block_quote_bare_repeat_1():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\ta\tparagraph\t
>\ta\tparagraph\t"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
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
def test_whitespaces_paragraph_with_tabs_before_within_block_quote_bare_with_space_repeat():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \ta paragraph
> \ta paragraph"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,5):\t\n\t]",
        "[text(1,5):a paragraph\na paragraph::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>a paragraph
a paragraph</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_paragraph_with_tabs_before_within_double_block_quote():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
\ta paragraph"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n\t]",
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
def test_whitespaces_paragraph_with_tabs_before_within_double_block_quote_with_single():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
>\ta paragraph"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n>]",
        "[para(2,5):\n\t]",
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
def test_whitespaces_paragraph_with_tabs_before_within_double_block_quote_with_single_and_space():
    """
    Test case:  paragraph preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> \ta paragraph"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> ]",
        "[para(2,5):\n\t]",
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
def test_whitespaces_paragraph_with_form_feeds_before():
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
