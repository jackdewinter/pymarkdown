"""
Testing various aspects of whitespaces around indented code blocks.
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
@pytest.mark.skip
def test_whitespaces_indented_code_with_spaces_before_within_list():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc
        indented block"""
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
def test_whitespaces_indented_code_with_spaces_before_within_block_quote():
    """
    Test case:  Indented Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> def
        indented block"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n        ]",
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
def test_whitespaces_indented_code_with_spaces_before_within_double_block_quote():
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
        "[para(2,5):\n        ]",
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
def test_whitespaces_indented_code_with_tabs_before():
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


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_with_block_quote():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
\tindented block"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n\t]",
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
def test_whitespaces_indented_code_with_tabs_before_with_block_quote_repeat():
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
def test_whitespaces_indented_code_with_tabs_before_with_block_quote_bare_repeat():
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
def test_whitespaces_indented_code_with_tabs_before_with_block_quote_bare_repeat_1():
    """
    Test case:  Indented Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t  indented block\t
>\t  indented block\t"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[icode-block(1,7):\t  :\n\t  ]",
        "[text(1,7):indented block\t\nindented block\t:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>indented block\t
indented block\t
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_indented_code_with_tabs_before_with_block_quote_bare_with_space_repeat():
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


@pytest.mark.gfm
def test_whitespaces_indented_code_with_form_feeds_before():
    """
    Test case:  Indented Code blocks preceeded by form feeds.
    """

    # Arrange
    source_markdown = """\u000C\u000C\u000C\u000Cindented block"""
    expected_tokens = [
        "[para(1,1):\u000C\u000C\u000C\u000C]",
        "[text(1,1):indented block:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>indented block</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
