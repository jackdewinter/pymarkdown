"""
Testing various aspects of whitespaces around atx headers.
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_spaces_before():
    """
    Test case:  Atx Headings preceeded by spaces.
    """

    # Arrange
    source_markdown = """  # abc"""
    expected_tokens = ["[atx(1,3):1:0:  ]", "[text(1,5):abc: ]", "[end-atx::]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_atx_headings_with_spaces_before_within_list():
    """
    Test case:  Atx Headings preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc
\t# abc"""
    expected_tokens = ["[atx(1,3):1:0:  ]", "[text(1,5):abc: ]", "[end-atx::]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_spaces_before_within_block_quotes():
    """
    Test case:  Atx Headings preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> def
    # abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n    ]",
        "[text(1,3):abc\ndef\n# abc::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
# abc</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_spaces_before_within_double_block_quotes():
    """
    Test case:  Atx Headings preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
    # abc"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n    ]",
        "[text(2,5):def\n# abc::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
# abc</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_spaces_before_within_double_block_quotes_with_single():
    """
    Test case:  Atx Headings preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   # abc"""
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
        "[atx(3,5):1:0:  ]",
        "[text(3,7):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<h1>abc</h1>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_before():
    """
    Test case:  Atx Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t # abc"""
    expected_tokens = [
        "[icode-block(1,5): \t:]",
        "[text(1,5): # abc:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code> # abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_before_within_list():
    """
    Test case:  Atx Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  \t# abc"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[atx(2,5):1:0:\t]",
        "[text(2,7):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<h1>abc</h1>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_before_within_block_quotes_x():
    """
    Test case:  Atx Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
  \t# abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n  \t]",
        "[text(1,3):abc\ndef\n# abc::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
# abc</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_before_within_block_quotes_repeat():
    """
    Test case:  Atx Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>\t# abc
>\t# abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::False]",
        "[atx(3,5):1:0:\t]",
        "[text(3,7):abc: ]",
        "[end-atx::]",
        "[atx(4,5):1:0:\t]",
        "[text(4,7):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
<h1>abc</h1>
<h1>abc</h1>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_before_within_block_quotes_bare_repeat():
    """
    Test case:  Atx Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t# abc
>\t# abc"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[atx(1,5):1:0:\t]",
        "[text(1,7):abc: ]",
        "[end-atx::]",
        "[atx(2,5):1:0:\t]",
        "[text(2,7):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h1>abc</h1>
<h1>abc</h1>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_before_within_block_quotes_bare_repeat_1():
    """
    Test case:  Atx Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t#\tabc\tdef\t
>\t#\tabc\tdef\t"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[atx(1,5):1:0:\t]",
        "[text(1,7):abc\tdef:\t]",
        "[end-atx:\t:]",
        "[atx(2,5):1:0:\t]",
        "[text(2,7):abc\tdef:\t]",
        "[end-atx:\t:]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h1>abc\tdef</h1>
<h1>abc\tdef</h1>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_before_within_block_quotes_bare_with_space_repeat():
    """
    Test case:  Atx Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> \t# abc
> \t# abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[atx(1,5):1:0:\t]",
        "[text(1,7):abc: ]",
        "[end-atx::]",
        "[atx(2,5):1:0:\t]",
        "[text(2,7):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h1>abc</h1>
<h1>abc</h1>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_before_within_double_block_quotes():
    """
    Test case:  Atx Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
  \t# abc"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n  \t]",
        "[text(2,5):def\n# abc::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
# abc</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_before_within_double_block_quotes_with_single():
    """
    Test case:  Atx Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
>\t# abc"""
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
        "[atx(3,5):1:0:\t]",
        "[text(3,7):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<h1>abc</h1>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_before_within_double_block_quotes_with_single_and_space():
    """
    Test case:  Atx Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> \t# abc"""
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
        "[atx(3,5):1:0:\t]",
        "[text(3,7):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<h1>abc</h1>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_form_feeds_before():
    """
    Test case:  Atx Headings preceeded by spaces and form feeds.
    """

    # Arrange
    source_markdown = """ \u000C # abc"""
    expected_tokens = [
        "[para(1,2): \u000C ]",
        "[text(1,2):# abc:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p># abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_inside():
    """
    Test case:  Atx Headings containing spaces and tabs.
    """

    # Arrange
    source_markdown = """#\tabc"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc:\t]", "[end-atx::]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_inside_2():
    """
    Test case:  Atx Headings containing spaces and tabs.
    """

    # Arrange
    source_markdown = """# abc\tdef"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc\tdef: ]", "[end-atx::]"]
    expected_gfm = """<h1>abc\tdef</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_form_feeds_inside():
    """
    Test case:  Atx Headings containing form feeds.
    """

    # Arrange
    source_markdown = """#\u000Cabc"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):#\u000Cabc:]", "[end-para:::True]"]
    expected_gfm = """<p>#\u000Cabc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_spaces_after():
    """
    Test case:  Atx Headings followed by spaces.
    """

    # Arrange
    source_markdown = """# abc  """
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc: ]", "[end-atx:  :]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_after():
    """
    Test case:  Atx Headings followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """# abc \t"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc: ]", "[end-atx: \t:]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_form_feeds_after():
    """
    Test case:  Atx Headings containing form feeds.
    """

    # Arrange
    source_markdown = """# abc\u000C"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc\u000C: ]", "[end-atx::]"]
    expected_gfm = """<h1>abc\u000C</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_inside_closed():
    """
    Test case:  Atx Headings followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """# abc\tdef #"""
    expected_tokens = ["[atx(1,1):1:1:]", "[text(1,3):abc\tdef: ]", "[end-atx:: ]"]
    expected_gfm = """<h1>abc\tdef</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_spaces_after_closed():
    """
    Test case:  Atx Headings followed by spaces.
    """

    # Arrange
    source_markdown = """# abc #"""
    expected_tokens = ["[atx(1,1):1:1:]", "[text(1,3):abc: ]", "[end-atx:: ]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_tabs_after_closed():
    """
    Test case:  Atx Headings followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """# abc\t#"""
    expected_tokens = ["[atx(1,1):1:1:]", "[text(1,3):abc: ]", "[end-atx::\t]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_with_form_feeds_after_closed():
    """
    Test case:  Atx Headings followed by form feeds.
    """

    # Arrange
    source_markdown = """# abc\u000C#"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc\u000C#: ]", "[end-atx::]"]
    expected_gfm = """<h1>abc\u000C#</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_closed_with_spaces_after():
    """
    Test case:  Atx Headings followed by spaces.
    """

    # Arrange
    source_markdown = """# abc #  """
    expected_tokens = ["[atx(1,1):1:1:]", "[text(1,3):abc: ]", "[end-atx:  : ]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_closed_with_tabs_after():
    """
    Test case:  Atx Headings followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """# abc #\t"""
    expected_tokens = ["[atx(1,1):1:1:]", "[text(1,3):abc: ]", "[end-atx:\t: ]"]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_atx_headings_closed_with_form_feeds_after():
    """
    Test case:  Atx Headings followed by form feeds.
    """

    # Arrange
    source_markdown = """# abc #\u000C"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):abc #\u000C: ]", "[end-atx::]"]
    expected_gfm = """<h1>abc #\u000C</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
