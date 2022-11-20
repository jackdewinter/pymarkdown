"""
Testing various aspects of whitespaces around setext headers.
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_only_enough_spaces_before():
    """
    Test case:  SetExt Headings preceeded by spaces.
    """

    # Arrange
    source_markdown = """abc
   ---"""
    expected_tokens = [
        "[setext(2,4):-:3::(1,1)]",
        "[text(1,1):abc:]",
        "[end-setext:   :]",
    ]
    expected_gfm = """<h2>abc</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_spaces_before():
    """
    Test case:  SetExt Headings preceeded by spaces.
    """

    # Arrange
    source_markdown = """abc
    ---"""
    expected_tokens = [
        "[para(1,1):\n    ]",
        "[text(1,1):abc\n---::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
---</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_setext_headings_with_spaces_before_within_list():
    """
    Test case:  SetExt Headings preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc
    ---"""
    expected_tokens = [
        "[setext(2,3):-:3::(1,1)]",
        "[text(1,1):abc:]",
        "[end-setext:  :]",
    ]
    expected_gfm = """<h2>abc</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_spaces_before_within_block_quotes():
    """
    Test case:  SetExt Headings preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> def
    ---"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n    ]",
        "[text(1,3):abc\ndef\n---::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
---</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_spaces_before_within_double_block_quotes():
    """
    Test case:  SetExt Headings preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
    ---"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n    ]",
        "[text(2,5):def\n---::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
---</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_spaces_before_within_double_block_quotes_with_single():
    """
    Test case:  SetExt Headings preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   ---"""
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
        "[tbreak(3,5):-:  :---]",
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
def test_whitespaces_setext_headings_with_tabs_before():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # https://github.github.com/gfm/#example-77 - is not indent block because part of para, not setext or sep due to 4 spaces
    # Arrange
    source_markdown = """abc
\t---"""
    expected_tokens = [
        "[para(1,1):\n\t]",
        "[text(1,1):abc\n---::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
---</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_before_within_list():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  \t---"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,5):-:3::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext:\t:]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_before_within_block_quote():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
\t---"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n\t]",
        "[text(1,3):abc\ndef\n---::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
---</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_before_within_block_quote_bare():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\tabc
>\tdef
>\t---"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>]",
        "[setext(3,5):-:3:\t:(1,5)]",
        "[text(1,5):abc\ndef::\n\t\x02]",
        "[end-setext:\t:]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h2>abc
def</h2>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_before_within_block_quote_bare_2_x():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\tabc\t
>\tdef\t
>\t---\t"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>]",
        "[setext(3,5):-:3:\t:(1,5):\t]",
        "[text(1,5):abc\t\ndef::\n\t\x02]",
        "[end-setext:\t:\t]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h2>abc\t
def</h2>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_before_within_block_quote_bare_2_plus_space():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\tabc\t\a
>\tdef\t\a
>\t---\t""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>]",
        "[setext(3,5):-:3:\t:(1,5):\t ]",
        "[text(1,5):abc\t\ndef:: \n\t\x02]",
        "[end-setext:\t:\t]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h2>abc\t
def</h2>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_before_within_block_quote_bare_2_plus_space_and_tab():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\tabc\t\a\t
>\tdef\t\a\t
>\t---\t""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>]",
        "[setext(3,5):-:3:\t:(1,5):\t \t]",
        "[text(1,5):abc\t \t\ndef::\n\t\x02]",
        "[end-setext:\t:\t]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h2>abc\t \t
def</h2>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_before_within_block_quote_bare_2_plus_space_and_tab_and_space():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\tabc\t\a\t\a
>\tdef\t\a\t
>\t---\t""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>]",
        "[setext(3,5):-:3:\t:(1,5):\t \t]",
        "[text(1,5):abc\t \t\ndef:: \n\t\x02]",
        "[end-setext:\t:\t]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h2>abc\t \t
def</h2>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_before_within_block_quote_bare_3():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\tabc\t
>\tdef\t
>\tghi\t
>\t---\t"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>\n>]",
        "[setext(4,5):-:3:\t:(1,5):\t]",
        "[text(1,5):abc\t\ndef\t\nghi::\n\t\x02\n\t\x02]",
        "[end-setext:\t:\t]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h2>abc\t
def\t
ghi</h2>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_before_within_block_quote_bare_with_space():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\tabc
>\tdef
> \t---"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n> ]",
        "[setext(3,5):-:3:\t:(1,5)]",
        "[text(1,5):abc\ndef::\n\t\x02]",
        "[end-setext:\t:]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h2>abc
def</h2>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_before_within_double_block_quote():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
\t---"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n\t]",
        "[text(2,5):def\n---::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
---</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_before_within_double_block_quote_with_single():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
>\t---"""
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
        "[tbreak(3,5):-:\t:---]",
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
def test_whitespaces_setext_headings_with_tabs_before_within_double_block_quote_with_single_and_space():
    """
    Test case:  SetExt Headings preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> \t---"""
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
        "[tbreak(3,5):-:\t:---]",
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
def test_whitespaces_setext_headings_with_form_feeds_before():
    """
    Test case:  SetExt Headings preceeded by form feeds.
    """

    # Arrange
    source_markdown = """abc
\u000C---"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):abc\n\u000C---::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
\u000C---</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_spaces_after():
    """
    Test case:  SetExt Headings followed by spaces.
    """

    # Arrange
    source_markdown = """abc
---  """
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):abc:]",
        "[end-setext::  ]",
    ]
    expected_gfm = """<h2>abc</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_after():
    """
    Test case:  SetExt Headings followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """abc
---\t"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):abc:]",
        "[end-setext::\t]",
    ]
    expected_gfm = """<h2>abc</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_tabs_after_within():
    """
    Test case:  SetExt Headings followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  ---\t"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):-:3::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::\t]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_setext_headings_with_form_feeds_after():
    """
    Test case:  SetExt Headings followed by form feeds.
    """

    # Arrange
    source_markdown = """abc
--- \u000C"""
    expected_tokens = [
        "[para(1,1):\n: \u000C]",
        "[text(1,1):abc\n---::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
---</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
