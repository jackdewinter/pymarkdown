"""
Extra tests.
"""

import os
from test.markdown_scanner import MarkdownScanner
from test.utils import act_and_assert, create_temporary_configuration_file

import pytest

from pymarkdown.extensions.front_matter_markdown_token import FrontMatterMarkdownToken
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken

# pylint: disable=too-many-lines

tables_config_map = {"extensions": {"markdown-tables": {"enabled": True}}}


@pytest.mark.gfm
def test_extra_001() -> None:
    """
    Test a totally blank input.
    """

    # Arrange
    source_markdown = ""
    expected_tokens = ["[BLANK(1,1):]"]
    expected_gfm = ""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_002() -> None:
    """
    Test a blank input with only whitespace.
    """

    # Arrange
    source_markdown = "   "
    expected_tokens = ["[BLANK(1,1):   ]"]
    expected_gfm = ""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_003() -> None:
    """
    Test to make sure the wide range of characters meets the GRM/CommonMark encodings.
    Note that since % is not followed by a 2 digit hex value, it is encoded per
    the common mark libraries.
    """

    # Arrange
    source_markdown = "[link](!\"#$%&'\\(\\)*+,-./0123456789:;<=>?@A-Z[\\\\]^_`a-z{|}~)"
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:!%22#$%25&amp;'()*+,-./0123456789:;%3C=%3E?@A-Z%5B%5C%5D"
        + "%5E_%60a-z%7B%7C%7D~::!\"#$%&'\\(\\)*+,-./0123456789:;<=>?@A-Z[\\\\]^_`a-z{|}~:::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        "<p><a href=\"!%22#$%25&amp;'()*+,-./0123456789:;%3C=%3E?@A-Z%5B%5C%5D"
        + '%5E_%60a-z%7B%7C%7D~">link</a></p>'
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_004() -> None:
    """
    Test to make sure the wide range of characters meets the GRM/CommonMark encodings.
    Note that since % is followed by a 2 digit hex value, it is encoded per the common
    mark libraries except for the % and the 2 digit hex value following it.

    Another example of this is example 511:
    https://github.github.com/gfm/#example-511
    """

    # Arrange
    source_markdown = (
        "[link](!\"#$%12&'\\(\\)*+,-./0123456789:;<=>?@A-Z[\\\\]^_`a-z{|}~)"
    )
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:!%22#$%12&amp;'()*+,-./0123456789:;%3C=%3E?@A-Z%5B%5C%5D"
        + "%5E_%60a-z%7B%7C%7D~::!\"#$%12&'\\(\\)*+,-./0123456789:;<=>?@A-Z[\\\\]^_`a-z{|}~:::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        "<p><a href=\"!%22#$%12&amp;'()*+,-./0123456789:;%3C=%3E?@A-Z%5B%5C%5D"
        + '%5E_%60a-z%7B%7C%7D~">link</a></p>'
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_005() -> None:
    """
    When encoding link characters, special attention is used for the % characters as
    the CommonMark parser treats "%<hex-char><hex-char>" as non-encodable.  Make sure
    this is tested at the end of the link.
    """

    # Arrange
    source_markdown = "[link](http://google.com/search%)"
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:http://google.com/search%25::http://google.com/search%:::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = '<p><a href="http://google.com/search%25">link</a></p>'

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_006() -> None:
    """
    lists and fenced code blocks within a block quote
    """

    # Arrange
    source_markdown = """> + list
> ```block
> A code block
> ```
> 1. another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::]",
        "[para(1,5):]",
        "[text(1,5):list:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(2,3):`:3:block:::::]",
        "[text(3,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[olist(5,3):.:1:5:]",
        "[para(5,6):]",
        "[text(5,6):another list:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<ol>
<li>another list</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_007a() -> None:
    """
    Text and a link reference definition within a block quote.
    """

    # Arrange
    source_markdown = """> this is text
> [a not so
>  simple](/link
> "a title")
>   a real test
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n]",
        "[para(1,3):\n\n \n\n  ]",
        "[text(1,3):this is text\n::\n]",
        '[link(2,3):inline:/link:a title::::a not so\nsimple:False:"::\n:]',
        "[text(2,4):a not so\nsimple::\n]",
        "[end-link::]",
        "[text(4,13):\na real test::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text
<a href="/link" title="a title">a not so
simple</a>
a real test</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_007b() -> None:
    """
    Variation on 7a with more spacing
    """

    # Arrange
    source_markdown = """> this is text
> [a not
>  so simple](/link
> "a
>  title"
>  )
> a real test
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n]",
        "[para(1,3):\n\n \n\n \n \n]",
        "[text(1,3):this is text\n::\n]",
        '[link(2,3):inline:/link:a\ntitle::::a not\nso simple:False:"::\n:\n]',
        "[text(2,4):a not\nso simple::\n]",
        "[end-link::]",
        "[text(6,5):\na real test::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text
<a href="/link" title="a
title">a not
so simple</a>
a real test</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_007cx() -> None:
    """
    Variation on 7a with more spacing
    """

    # Arrange
    source_markdown = """> this is text
> [a\a
>  not
>  so simple](/link
> "a
>  title"
>  )
> a real test
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n]",
        "[para(1,3):\n\n \n \n\n \n \n]",
        "[text(1,3):this is text\n::\n]",
        '[link(2,3):inline:/link:a\ntitle::::a \nnot\nso simple:False:"::\n:\n]',
        "[text(2,4):a\nnot\nso simple:: \n\n]",
        "[end-link::]",
        "[text(7,5):\na real test::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text
<a href="/link" title="a
title">a\a
not
so simple</a>
a real test</p>
</blockquote>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_007ca() -> None:
    """
    Variation on 7a with more spacing
    """

    # Arrange
    source_markdown = """> this is text
> [a
>  not\a
>  so simple](/link
> "a
>  title"
>  )
> a real test
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n]",
        "[para(1,3):\n\n \n \n\n \n \n]",
        "[text(1,3):this is text\n::\n]",
        '[link(2,3):inline:/link:a\ntitle::::a\nnot \nso simple:False:"::\n:\n]',
        "[text(2,4):a\nnot\nso simple::\n \n]",
        "[end-link::]",
        "[text(7,5):\na real test::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text
<a href="/link" title="a
title">a
not 
so simple</a>
a real test</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_007d() -> None:
    """
    Variation on 7a with more spacing
    """

    # Arrange
    source_markdown = """> this is text
> [a
>  not
>  so simple](/link
> "a
>  title"
>  )
> a real test
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n]",
        "[para(1,3):\n\n \n \n\n \n \n]",
        "[text(1,3):this is text\n::\n]",
        '[link(2,3):inline:/link:a\ntitle::::a\nnot\nso simple:False:"::\n:\n]',
        "[text(2,4):a\nnot\nso simple::\n\n]",
        "[end-link::]",
        "[text(7,5):\na real test::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text
<a href="/link" title="a
title">a
not
so simple</a>
a real test</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_007e() -> None:
    """
    Almost looks like a fenced code block, but is really a code span.
    """

    # Arrange
    source_markdown = """> this is text
> ``
> foo
> bar  
> baz
> ``
> a real test
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n]",
        "[para(1,3):\n\n\n\n\n\n]",
        "[text(1,3):this is text\n::\n]",
        "[icode-span(2,3):foo\a\n\a \abar  \a\n\a \abaz:``:\a\n\a \a:\a\n\a \a]",
        "[text(6,5):\na real test::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text
<code>foo bar   baz</code>
a real test</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_008x() -> None:
    """
    Simple unordered list with increasing indent in a block quote.
    """

    # Arrange
    source_markdown = """> * this is level 1
>   * this is level 2
>     * this is level 3
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):*::4:]",
        "[para(1,5):]",
        "[text(1,5):this is level 1:]",
        "[end-para:::True]",
        "[ulist(2,5):*::6:  ]",
        "[para(2,7):]",
        "[text(2,7):this is level 2:]",
        "[end-para:::True]",
        "[ulist(3,7):*::8:    ]",
        "[para(3,9):]",
        "[text(3,9):this is level 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>this is level 1
<ul>
<li>this is level 2
<ul>
<li>this is level 3</li>
</ul>
</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_008a() -> None:
    """
    Variation on 8 with no block quote.
    """

    # Arrange
    source_markdown = """* this is level 1
  * this is level 2
    * this is level 3
"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):this is level 1:]",
        "[end-para:::True]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text(2,5):this is level 2:]",
        "[end-para:::True]",
        "[ulist(3,5):*::6:    :]",
        "[para(3,7):]",
        "[text(3,7):this is level 3:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>this is level 1
<ul>
<li>this is level 2
<ul>
<li>this is level 3</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_009x() -> None:
    """
    Simple block quote within an unordered list.
    """

    # Arrange
    source_markdown = """- > This is one section of a block quote
"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[block-quote(1,3):  :  > \n]",
        "[para(1,5):]",
        "[text(1,5):This is one section of a block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<p>This is one section of a block quote</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_009a() -> None:
    """
    Simple block quote within an ordered list.
    """

    # Arrange
    source_markdown = """1. > This is one section of a block quote
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[block-quote(1,4):   :   > \n]",
        "[para(1,6):]",
        "[text(1,6):This is one section of a block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>This is one section of a block quote</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_009b() -> None:
    """
    Simple block quote within an ordered list.
    """

    # Arrange
    source_markdown = """1.
   > This is one section of a block quote
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[BLANK(1,3):]",
        "[block-quote(2,4):   :   > \n]",
        "[para(2,6):]",
        "[text(2,6):This is one section of a block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>This is one section of a block quote</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_009c() -> None:
    """
    Simple block quote within an ordered list.
    """

    # Arrange
    source_markdown = """1. > This is one section of a block quote
   > Just one section.
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[block-quote(1,4):   :   > \n   > \n]",
        "[para(1,6):\n]",
        "[text(1,6):This is one section of a block quote\nJust one section.::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<p>This is one section of a block quote
Just one section.</p>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_010x() -> None:
    """
    List item with weird progression.
    """

    # Arrange
    source_markdown = """* First Item
  * First-First
   * First-Second
    * First-Third
* Second Item
"""
    expected_tokens = [
        "[ulist(1,1):*::2::]",
        "[para(1,3):]",
        "[text(1,3):First Item:]",
        "[end-para:::True]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text(2,5):First-First:]",
        "[end-para:::True]",
        "[li(3,4):5:   :]",
        "[para(3,6):]",
        "[text(3,6):First-Second:]",
        "[end-para:::True]",
        "[li(4,5):6:    :]",
        "[para(4,7):]",
        "[text(4,7):First-Third:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):Second Item:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>First Item
<ul>
<li>First-First</li>
<li>First-Second</li>
<li>First-Third</li>
</ul>
</li>
<li>Second Item</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_010a() -> None:
    """
    List item with weird progression.
    """

    # Arrange
    source_markdown = """* First Item
 * Second Item    
  * Third Item
"""
    expected_tokens = [
        "[ulist(1,1):*::2::]",
        "[para(1,3):]",
        "[text(1,3):First Item:]",
        "[end-para:::True]",
        "[li(2,2):3: :]",
        "[para(2,4)::    ]",
        "[text(2,4):Second Item:]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text(3,5):Third Item:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>First Item</li>
<li>Second Item</li>
<li>Third Item</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_010b() -> None:
    """
    List item with weird progression.
    """

    # Arrange
    source_markdown = """1. First Item
   1. First-First
    1. First-Second
     1. First-Third
      1. First-Four
1. Second Item
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):First Item:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):First-First:]",
        "[end-para:::True]",
        "[li(3,5):7:    :1]",
        "[para(3,8):]",
        "[text(3,8):First-Second:]",
        "[end-para:::True]",
        "[li(4,6):8:     :1]",
        "[para(4,9):]",
        "[text(4,9):First-Third:]",
        "[end-para:::True]",
        "[li(5,7):9:      :1]",
        "[para(5,10):]",
        "[text(5,10):First-Four:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(6,1):3::1]",
        "[para(6,4):]",
        "[text(6,4):Second Item:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>First Item
<ol>
<li>First-First</li>
<li>First-Second</li>
<li>First-Third</li>
<li>First-Four</li>
</ol>
</li>
<li>Second Item</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_011x() -> None:
    """
    Block quote followed directly by Atx Heading.
    """

    # Arrange
    source_markdown = """> simple text
> dd
> dd
# a
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):\n\n]",
        "[text(1,3):simple text\ndd\ndd::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[atx(4,1):1:0:]",
        "[text(4,3):a: ]",
        "[end-atx::]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<p>simple text
dd
dd</p>
</blockquote>
<h1>a</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_011a() -> None:
    """
    Variation of 11 with no newline after Atx Heading
    """

    # Arrange
    source_markdown = """> simple text
> dd
> dd
# a"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):\n\n]",
        "[text(1,3):simple text\ndd\ndd::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[atx(4,1):1:0:]",
        "[text(4,3):a: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<blockquote>
<p>simple text
dd
dd</p>
</blockquote>
<h1>a</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_011b() -> None:
    """
    Variation of 11 with newline after Block Quote and before Atx Heading
    """

    # Arrange
    source_markdown = """> simple text
> dd
> dd

# a"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[para(1,3):\n\n]",
        "[text(1,3):simple text\ndd\ndd::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[atx(5,1):1:0:]",
        "[text(5,3):a: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<blockquote>
<p>simple text
dd
dd</p>
</blockquote>
<h1>a</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_012() -> None:
    """
    Unordered lists, nested within each other with weird indents.
    """

    # Arrange
    source_markdown = """This is a test

 * this is level 1
 * this is also level 1
   * this is level 2
   * this is also level 2
      * this is level 3
   * this is also level 2
    * this is also level 2
    * this is also level 2
* this is also level 1
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This is a test:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[ulist(3,2):*::3: :]",
        "[para(3,4):]",
        "[text(3,4):this is level 1:]",
        "[end-para:::True]",
        "[li(4,2):3: :]",
        "[para(4,4):]",
        "[text(4,4):this is also level 1:]",
        "[end-para:::True]",
        "[ulist(5,4):*::5:   ]",
        "[para(5,6):]",
        "[text(5,6):this is level 2:]",
        "[end-para:::True]",
        "[li(6,4):5:   :]",
        "[para(6,6):]",
        "[text(6,6):this is also level 2:]",
        "[end-para:::True]",
        "[ulist(7,7):*::8:      ]",
        "[para(7,9):]",
        "[text(7,9):this is level 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(8,4):5:   :]",
        "[para(8,6):]",
        "[text(8,6):this is also level 2:]",
        "[end-para:::True]",
        "[li(9,5):6:    :]",
        "[para(9,7):]",
        "[text(9,7):this is also level 2:]",
        "[end-para:::True]",
        "[li(10,5):6:    :]",
        "[para(10,7):]",
        "[text(10,7):this is also level 2:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(11,1):2::]",
        "[para(11,3):]",
        "[text(11,3):this is also level 1:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<p>This is a test</p>
<ul>
<li>this is level 1</li>
<li>this is also level 1
<ul>
<li>this is level 2</li>
<li>this is also level 2
<ul>
<li>this is level 3</li>
</ul>
</li>
<li>this is also level 2</li>
<li>this is also level 2</li>
<li>this is also level 2</li>
</ul>
</li>
<li>this is also level 1</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_013x() -> None:
    """
    Paragraph followed by a blank line and a SetExt heading in a block quote
    """

    # Arrange
    source_markdown = """ > this is text
 >
 > a setext heading
 > that is not properly
>  indented
> ---
"""
    expected_tokens = [
        "[block-quote(1,2): : > \n >\n > \n > \n> \n> \n]",
        "[para(1,4):]",
        "[text(1,4):this is text:]",
        "[end-para:::True]",
        "[BLANK(2,3):]",
        "[setext(6,3):-:3::(3,4)]",
        "[text(3,4):a setext heading\nthat is not properly\nindented::\n\n \x02]",
        "[end-setext::]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text</p>
<h2>a setext heading
that is not properly
indented</h2>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_013a() -> None:
    """
    Variation of 13x without the block quote.
    """

    # Arrange
    source_markdown = """this is text

a setext heading
that is not properly
 indented
---
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this is text:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[setext(6,1):-:3::(3,1)]",
        "[text(3,1):a setext heading\nthat is not properly\nindented::\n\n \x02]",
        "[end-setext::]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<p>this is text</p>
<h2>a setext heading
that is not properly
indented</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_014x() -> None:
    """
    TBD - test_md027_good_block_quote_ordered_list_thematic_break
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>    *****
> 1. that

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[tbreak(3,6):*::*****]",
        "[li(4,3):5::1]",
        "[para(4,6):]",
        "[text(4,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<hr />
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_014a() -> None:
    """
    TBD - test_md027_good_block_quote_ordered_list_thematic_break_misaligned
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>     *****
> 1. that

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[tbreak(3,7):*: :*****]",
        "[li(4,3):5::1]",
        "[para(4,6):]",
        "[text(4,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<hr />
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_014bx() -> None:
    """
    TBD - test_md027_good_block_quote_ordered_list_thematic_break
    """

    # Arrange
    source_markdown = """> 1. *****
>    list
>    this
>    *****
> 1. that

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n   \n   ]",
        "[tbreak(1,6):*::*****]",
        "[para(2,6):\n]",
        "[text(2,6):list\nthis::\n]",
        "[end-para:::False]",
        "[tbreak(4,6):*::*****]",
        "[li(5,3):5::1]",
        "[para(5,6):]",
        "[text(5,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<hr />
list
this
<hr />
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_014ba() -> None:
    """
    TBD - test_md027_good_block_quote_ordered_list_thematic_break
    """

    # Arrange
    source_markdown = """1. *****
   list
   this
   *****
1. that

"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n\n]",
        "[tbreak(1,4):*::*****]",
        "[para(2,4):\n]",
        "[text(2,4):list\nthis::\n]",
        "[end-para:::False]",
        "[tbreak(4,4):*::*****]",
        "[li(5,1):3::1]",
        "[para(5,4):]",
        "[text(5,4):that:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<hr />
list
this
<hr />
</li>
<li>that</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_014bb() -> None:
    """
    TBD - test_md027_good_block_quote_ordered_list_thematic_break
    """

    # Arrange
    source_markdown = """> *****
> list
> this
> *****
> that

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n]",
        "[tbreak(1,3):*::*****]",
        "[para(2,3):\n]",
        "[text(2,3):list\nthis::\n]",
        "[end-para:::False]",
        "[tbreak(4,3):*::*****]",
        "[para(5,3):]",
        "[text(5,3):that:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<hr />
<p>list
this</p>
<hr />
<p>that</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_015() -> None:
    """
    TBD - test_md027_good_block_quote_ordered_list_atx_heading
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>    # Heading
> 1. that

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[atx(3,6):1:0:]",
        "[text(3,8):Heading: ]",
        "[end-atx::]",
        "[li(4,3):5::1]",
        "[para(4,6):]",
        "[text(4,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<h1>Heading</h1>
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_015a() -> None:
    """
    TBD - test_md027_good_block_quote_ordered_list_atx_heading
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>     # Heading
> 1. that

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[atx(3,7):1:0: ]",
        "[text(3,9):Heading: ]",
        "[end-atx::]",
        "[li(4,3):5::1]",
        "[para(4,6):]",
        "[text(4,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<h1>Heading</h1>
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_016() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>
>    Heading
>    ---
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n\n   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[setext(5,6):-:3::(4,6)]",
        "[text(4,6):Heading:]",
        "[end-setext::]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<p>list
this</p>
<h2>Heading</h2>
</li>
<li>
<p>that</p>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_016a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>
>    Heading
>    ---
> 1. that

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n\n   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[setext(5,6):-:3::(4,6)]",
        "[text(4,6):Heading:]",
        "[end-setext::]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<p>list
this</p>
<h2>Heading</h2>
</li>
<li>
<p>that</p>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_017() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>
>        indented
>        code block
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n\n   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[icode-block(4,10):    :\n    ]",
        "[text(4,10):indented\ncode block:]",
        "[end-icode-block:::True]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<p>list
this</p>
<pre><code>indented
code block
</code></pre>
</li>
<li>
<p>that</p>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_018x() -> None:
    """
    Validate that having a fenced block inside of a list does not close the list
    when the code block is started.

    Per: https://github.com/jackdewinter/pymarkdown/issues/98
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>    ```html
>    <html>
>    ```
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n   \n   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[fcode-block(3,6):`:3:html:::::]",
        "[text(4,6):\a<\a&lt;\ahtml\a>\a&gt;\a:]",
        "[end-fcode-block:::3:False]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<pre><code class="language-html">&lt;html&gt;
</code></pre>
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_018a() -> None:
    """
    variation of 18 with indent on first line
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>     ```html
>    <html>
>    ```
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n   \n   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[fcode-block(3,7):`:3:html:::: :]",
        "[text(4,6):\a<\a&lt;\ahtml\a>\a&gt;\a:]",
        "[end-fcode-block:::3:False]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<pre><code class="language-html">&lt;html&gt;
</code></pre>
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_018b() -> None:
    """
    variation of 18 with indent on second line
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>    ```html
>     <html>
>    ```
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n   \n   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[fcode-block(3,6):`:3:html:::::]",
        "[text(4,6):\a<\a&lt;\ahtml\a>\a&gt;\a: ]",
        "[end-fcode-block:::3:False]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<pre><code class="language-html"> &lt;html&gt;
</code></pre>
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_018c() -> None:
    """
    variation of 18 with indent on third line
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>    ```html
>    <html>
>     ```
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n   \n   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[fcode-block(3,6):`:3:html:::::]",
        "[text(4,6):\a<\a&lt;\ahtml\a>\a&gt;\a:]",
        "[end-fcode-block: ::3:False]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<pre><code class="language-html">&lt;html&gt;
</code></pre>
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_019x() -> None:
    """
    Validate that having an HTML block inside of a list does not close the list
    when the HTML block is started.
    Per: https://github.com/jackdewinter/pymarkdown/issues/99
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>    <!-- this is a comment -->
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[html-block(3,6)]",
        "[text(3,6):<!-- this is a comment -->:]",
        "[end-html-block:::False]",
        "[li(4,3):5::1]",
        "[para(4,6):]",
        "[text(4,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
<!-- this is a comment -->
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_019a() -> None:
    """
    Variation of 019 with extra space in front of html block.
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>     <!-- this is a comment -->
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[html-block(3,6)]",
        "[text(3,7):<!-- this is a comment -->: ]",
        "[end-html-block:::False]",
        "[li(4,3):5::1]",
        "[para(4,6):]",
        "[text(4,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
 <!-- this is a comment -->
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_019b() -> None:
    """
    Variation of 019 with extra space in front of html block.
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>     <!-- this is
>     a comment -->
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[html-block(3,6)]",
        "[text(3,7):<!-- this is\n a comment -->: ]",
        "[end-html-block:::False]",
        "[li(5,3):5::1]",
        "[para(5,6):]",
        "[text(5,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
 <!-- this is
 a comment -->
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_020x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>
>    [abc]: /url
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n]",
        "[olist(1,3):.:1:5::   \n\n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[link-ref-def(4,6):True::abc:: :/url:::::]",
        "[li(5,3):5::1]",
        "[para(5,6):]",
        "[text(5,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<p>list
this</p>
</li>
<li>
<p>that</p>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_020a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>
>    [abc]:
>     /url
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> \n]",
        "[olist(1,3):.:1:5::   \n\n   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[link-ref-def(4,6):True::abc::\n :/url:::::]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<p>list
this</p>
</li>
<li>
<p>that</p>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_020b() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    this
>
>    [abc]:
>     /url
>      "title"
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n\n   \n   \n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        '[link-ref-def(4,6):True::abc::\n :/url::\n  :title:"title":]',
        "[li(7,3):5::1]",
        "[para(7,6):]",
        "[text(7,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<p>list
this</p>
</li>
<li>
<p>that</p>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_020c() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    this
> \x0c
>    [abc]: /url
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n]",
        "[olist(1,3):.:1:5::   \n\n   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,3):\x0c]",
        "[link-ref-def(4,6):True::abc:: :/url:::::]",
        "[li(5,3):5::1]",
        "[para(5,6):]",
        "[text(5,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<p>list
this</p>
</li>
<li>
<p>that</p>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_020d() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    this
> \u00a0
>    [abc]: /url
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[olist(1,3):.:1:5::   \n\n   ]",
        "[para(1,6):\n\n\n]",
        "[text(1,6):list\nthis\n\u00a0\n[abc]: /url::\n\n\n]",
        "[end-para:::True]",
        "[li(5,3):5::1]",
        "[para(5,6):]",
        "[text(5,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
this
\u00a0
[abc]: /url</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_021x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
1. Item 1
   1. Item 1a
  100. Item 1b
"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[olist(2,1):.:1:3::]",
        "[para(2,4):]",
        "[text(2,4):Item 1:]",
        "[end-para:::True]",
        "[olist(3,4):.:1:6:   ]",
        "[para(3,7):]",
        "[text(3,7):Item 1a:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(4,3):7:  :100]",
        "[para(4,8):]",
        "[text(4,8):Item 1b:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item 1
<ol>
<li>Item 1a</li>
</ol>
</li>
<li>Item 1b</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_021a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """* Item 1
  * Item 1a
 * Item 2
   * Item 2a
"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):Item 1:]",
        "[end-para:::True]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text(2,5):Item 1a:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(3,2):3: :]",
        "[para(3,4):]",
        "[text(3,4):Item 2:]",
        "[end-para:::True]",
        "[ulist(4,4):*::5:   :]",
        "[para(4,6):]",
        "[text(4,6):Item 2a:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Item 1
<ul>
<li>Item 1a</li>
</ul>
</li>
<li>Item 2
<ul>
<li>Item 2a</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_021b() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """>  + list
>    this
> + that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,4):+::5: :   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this</li>
<li>that</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_021c() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """This is a test

>  * this is level 1
>    * this is level 2
>      * this is level 3
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This is a test:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> \n> \n> ]",
        "[ulist(3,4):*::5: ]",
        "[para(3,6):]",
        "[text(3,6):this is level 1:]",
        "[end-para:::True]",
        "[ulist(4,6):*::7:   ]",
        "[para(4,8):]",
        "[text(4,8):this is level 2:]",
        "[end-para:::True]",
        "[ulist(5,8):*::9:     ]",
        "[para(5,10):]",
        "[text(5,10):this is level 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<p>This is a test</p>
<blockquote>
<ul>
<li>this is level 1
<ul>
<li>this is level 2
<ul>
<li>this is level 3</li>
</ul>
</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_022() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. line 1
   * line 1a
2. line 2
3. line 3
   * line 3a
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):line 1:]",
        "[end-para:::True]",
        "[ulist(2,4):*::5:   ]",
        "[para(2,6):]",
        "[text(2,6):line 1a:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(3,1):3::2]",
        "[para(3,4):]",
        "[text(3,4):line 2:]",
        "[end-para:::True]",
        "[li(4,1):3::3]",
        "[para(4,4):]",
        "[text(4,4):line 3:]",
        "[end-para:::True]",
        "[ulist(5,4):*::5:   :]",
        "[para(5,6):]",
        "[text(5,6):line 3a:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>line 1
<ul>
<li>line 1a</li>
</ul>
</li>
<li>line 2</li>
<li>line 3
<ul>
<li>line 3a</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_023xx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. abc
   1. def
  foo
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n  ]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(4,3):-:  :---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_023xa() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. abc
   1. def
 foo
 ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n ]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(4,2):-: :---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_023xb() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. abc
   1. def
foo
---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :]",
        "[para(2,7):\n]",
        "[text(2,7):def\nfoo::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
foo</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_023xc() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. abc
   1. def
  foo
  bar
  ---
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n]",
        "[para(2,7):\n  \n  ]",
        "[text(2,7):def\nfoo\nbar::\n\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[tbreak(5,3):-:  :---]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
foo
bar</li>
</ol>
</li>
</ol>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_023ax() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """  1.  A paragraph
 with two lines."""
    expected_tokens = [
        "[olist(1,3):.:1:6:  :]",
        "[para(1,7):\n ]",
        "[text(1,7):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>A paragraph
with two lines.</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_023aa() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """   1.  A paragraph
  with two lines."""
    expected_tokens = [
        "[olist(1,4):.:1:7:   :]",
        "[para(1,8):\n  ]",
        "[text(1,8):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>A paragraph
with two lines.</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_023ab() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """   1.  A paragraph
 with two lines."""
    expected_tokens = [
        "[olist(1,4):.:1:7:   :]",
        "[para(1,8):\n ]",
        "[text(1,8):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>A paragraph
with two lines.</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_024x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> * Item 1
>   * Item 1a
>   * Item 1b
> * Item 2
>    * Item 2a
>    * Item 2b
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):*::4:]",
        "[para(1,5):]",
        "[text(1,5):Item 1:]",
        "[end-para:::True]",
        "[ulist(2,5):*::6:  ]",
        "[para(2,7):]",
        "[text(2,7):Item 1a:]",
        "[end-para:::True]",
        "[li(3,5):6:  :]",
        "[para(3,7):]",
        "[text(3,7):Item 1b:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(4,3):4::]",
        "[para(4,5):]",
        "[text(4,5):Item 2:]",
        "[end-para:::True]",
        "[ulist(5,6):*::7:   ]",
        "[para(5,8):]",
        "[text(5,8):Item 2a:]",
        "[end-para:::True]",
        "[li(6,6):7:   :]",
        "[para(6,8):]",
        "[text(6,8):Item 2b:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>Item 1
<ul>
<li>Item 1a</li>
<li>Item 1b</li>
</ul>
</li>
<li>Item 2
<ul>
<li>Item 2a</li>
<li>Item 2b</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_024a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> * Item 1
>   * Item 1a
>   * Item 1b
>  * Item 2
>    * Item 2a
>    * Item 2b
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):*::4:]",
        "[para(1,5):]",
        "[text(1,5):Item 1:]",
        "[end-para:::True]",
        "[ulist(2,5):*::6:  ]",
        "[para(2,7):]",
        "[text(2,7):Item 1a:]",
        "[end-para:::True]",
        "[li(3,5):6:  :]",
        "[para(3,7):]",
        "[text(3,7):Item 1b:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(4,4):5: :]",
        "[para(4,6):]",
        "[text(4,6):Item 2:]",
        "[end-para:::True]",
        "[ulist(5,6):*::7:   ]",
        "[para(5,8):]",
        "[text(5,8):Item 2a:]",
        "[end-para:::True]",
        "[li(6,6):7:   :]",
        "[para(6,8):]",
        "[text(6,8):Item 2b:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>Item 1
<ul>
<li>Item 1a</li>
<li>Item 1b</li>
</ul>
</li>
<li>Item 2
<ul>
<li>Item 2a</li>
<li>Item 2b</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025xx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list
>   this
>   >  good
>   > item
> + that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::4::  \n\n]",
        "[para(1,5):\n]",
        "[text(1,5):list\nthis::\n]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n>   > \n> ]",
        "[para(3,8): \n]",
        "[text(3,8):good\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(5,3):4::]",
        "[para(5,5):]",
        "[text(5,5):that:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this
<blockquote>
<p>good
item</p>
</blockquote>
</li>
<li>that</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025xa() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list
>   this
>   >  good
>   > item
>   that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::4::  \n\n\n  þ]",
        "[para(1,5):\n]",
        "[text(1,5):list\nthis::\n]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n>   > \n> \n]",
        "[para(3,8): \n\n]",
        "[text(3,8):good\nitem\nthat::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this
<blockquote>
<p>good
item
that</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025ax() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list
>   this
>   > good
>   > item
> + that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::4::  \n\n]",
        "[para(1,5):\n]",
        "[text(1,5):list\nthis::\n]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n>   > \n> ]",
        "[para(3,7):\n]",
        "[text(3,7):good\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(5,3):4::]",
        "[para(5,5):]",
        "[text(5,5):that:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this
<blockquote>
<p>good
item</p>
</blockquote>
</li>
<li>that</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025aa() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list
>   this
>   > good
>   > item
>   that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::4::  \n\n\n  þ]",
        "[para(1,5):\n]",
        "[text(1,5):list\nthis::\n]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n>   > \n> \n]",
        "[para(3,7):\n\n]",
        "[text(3,7):good\nitem\nthat::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this
<blockquote>
<p>good
item
that</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025bx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list
>   this
>   > item
> + that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::4::  \n]",
        "[para(1,5):\n]",
        "[text(1,5):list\nthis::\n]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n> ]",
        "[para(3,7):]",
        "[text(3,7):item:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(4,3):4::]",
        "[para(4,5):]",
        "[text(4,5):that:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this
<blockquote>
<p>item</p>
</blockquote>
</li>
<li>that</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025ba() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list
>   this
>   > item
>   that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::4::  \n\n  þ]",
        "[para(1,5):\n]",
        "[text(1,5):list\nthis::\n]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n> \n]",
        "[para(3,7):\n]",
        "[text(3,7):item\nthat::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this
<blockquote>
<p>item
that</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025cxx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list
>   > good
>   > item
> + that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n]",
        "[para(1,5):]",
        "[text(1,5):list:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n> ]",
        "[para(2,7):\n]",
        "[text(2,7):good\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(4,3):4::]",
        "[para(4,5):]",
        "[text(4,5):that:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
<blockquote>
<p>good
item</p>
</blockquote>
</li>
<li>that</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025cxb() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    > good
>    > item
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[olist(1,3):.:1:5::\n]",
        "[para(1,6):]",
        "[text(1,6):list:]",
        "[end-para:::True]",
        "[block-quote(2,6)::> \n>    > \n> ]",
        "[para(2,8):\n]",
        "[text(2,8):good\nitem::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(4,3):5::1]",
        "[para(4,6):]",
        "[text(4,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
<blockquote>
<p>good
item</p>
</blockquote>
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025cxc() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
>    > good
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[olist(1,3):.:1:5::]",
        "[para(1,6):]",
        "[text(1,6):list:]",
        "[end-para:::True]",
        "[block-quote(2,6)::> \n> ]",
        "[para(2,8):]",
        "[text(2,8):good:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(3,3):5::1]",
        "[para(3,6):]",
        "[text(3,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list
<blockquote>
<p>good</p>
</blockquote>
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025cxd() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[para(1,6):]",
        "[text(1,6):list:]",
        "[end-para:::True]",
        "[li(2,3):5::1]",
        "[para(2,6):]",
        "[text(2,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>list</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025cxe() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. > list
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5:]",
        "[block-quote(1,6)::> \n> ]",
        "[para(1,8):]",
        "[text(1,8):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(2,3):5::1]",
        "[para(2,6):]",
        "[text(2,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025cxf() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. > list
>    > is
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::]",
        "[block-quote(1,6)::> \n>    > \n> ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nis::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(3,3):5::1]",
        "[para(3,6):]",
        "[text(3,6):that:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list
is</p>
</blockquote>
</li>
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025cxg() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > list
>   > is
> + that
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n>   > \n> ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nis::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>list
is</p>
</blockquote>
</li>
<li>that</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025cxz() -> None:
    """
    Verify that a nesting of block quote, ordered list, block quote, with
    the maximum number of spaces allowed, works properly,
    with no block quote characters on the second line, with a list item.
    """

    # Arrange
    source_markdown = """> 1. > list
> 1.   item"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5:]",
        "[block-quote(1,6)::> \n> ]",
        "[para(1,8):]",
        "[text(1,8):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(2,3):7::1]",
        "[para(2,8):]",
        "[text(2,8):item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<blockquote>
<p>list</p>
</blockquote>
</li>
<li>item</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025ca() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list
>   > good
>   > item
>   that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n  þ]",
        "[para(1,5):]",
        "[text(1,5):list:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n> \n]",
        "[para(2,7):\n\n]",
        "[text(2,7):good\nitem\nthat::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
<blockquote>
<p>good
item
that</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_026x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. item
2.  ```python
    def foo_fun():
       \"\"\" 
       Does nothing. 

       Really.
       \"\"\"
       pass
    ```
3. another item
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::    \n    \n    \n\n    \n    \n    \n    \n]",
        "[para(1,4):]",
        "[text(1,4):item:]",
        "[end-para:::True]",
        "[li(2,1):4::2]",
        "[fcode-block(2,5):`:3:python:::::]",
        '[text(3,5):def foo_fun():\n   \a"\a&quot;\a\a"\a&quot;\a\a"\a&quot;\a \n   Does nothing. \n\x03\n   Really.\n   \a"\a&quot;\a\a"\a&quot;\a\a"\a&quot;\a\n   pass:]',
        "[end-fcode-block:::3:False]",
        "[li(11,1):3::3]",
        "[para(11,4):]",
        "[text(11,4):another item:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>item</li>
<li>
<pre><code class="language-python">def foo_fun():
   &quot;&quot;&quot; 
   Does nothing. 

   Really.
   &quot;&quot;&quot;
   pass
</code></pre>
</li>
<li>another item</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_026a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """# Minimal

1. Item
2. Item with code.

    ```python
    def foo_fun():
       \"\"\" 
       Does nothing. 
       \"\"\"
       pass
    ```

3. Another Item"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):Minimal: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[olist(3,1):.:1:3::\n   \n   \n   \n   \n   \n   \n   \n]",
        "[para(3,4):]",
        "[text(3,4):Item:]",
        "[end-para:::True]",
        "[li(4,1):3::2]",
        "[para(4,4):]",
        "[text(4,4):Item with code.:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[fcode-block(6,5):`:3:python:::: :]",
        '[text(7,4):def foo_fun():\n\a \a\x03\a   \a"\a&quot;\a\a"\a&quot;\a\a"\a&quot;\a \n\a \a\x03\a   Does nothing. \n\a \a\x03\a   \a"\a&quot;\a\a"\a&quot;\a\a"\a&quot;\a\n\a \a\x03\a   pass:\a \a\x03\a]',
        "[end-fcode-block: ::3:False]",
        "[BLANK(13,1):]",
        "[li(14,1):3::3]",
        "[para(14,4):]",
        "[text(14,4):Another Item:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<h1>Minimal</h1>
<ol>
<li>
<p>Item</p>
</li>
<li>
<p>Item with code.</p>
<pre><code class="language-python">def foo_fun():
   &quot;&quot;&quot; 
   Does nothing. 
   &quot;&quot;&quot;
   pass
</code></pre>
</li>
<li>
<p>Another Item</p>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_026b() -> None:
    """
    TBD
    note: this may look weird.  the ordered list has an indent of 3, with a single
          space before fenced code block.  therefore, the text within the fcb starts
          at column 4, with its first character being "special" space.
    """

    # Arrange
    source_markdown = """2. Item with code.

    ```python
    def foo_fun():
       \"\"\" 
       Does nothing. 
       \"\"\"
       pass
    ```
"""
    expected_tokens = [
        "[olist(1,1):.:2:3::\n   \n   \n   \n   \n   \n   \n   \n]",
        "[para(1,4):]",
        "[text(1,4):Item with code.:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[fcode-block(3,5):`:3:python:::: :]",
        '[text(4,4):def foo_fun():\n\a \a\x03\a   \a"\a&quot;\a\a"\a&quot;\a\a"\a&quot;\a \n\a \a\x03\a   Does nothing. \n\a \a\x03\a   \a"\a&quot;\a\a"\a&quot;\a\a"\a&quot;\a\n\a \a\x03\a   pass:\a \a\x03\a]',
        "[end-fcode-block: ::3:False]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol start="2">
<li>
<p>Item with code.</p>
<pre><code class="language-python">def foo_fun():
   &quot;&quot;&quot; 
   Does nothing. 
   &quot;&quot;&quot;
   pass
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_026cx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. Item with code.
      ## this
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n]",
        "[para(1,4):]",
        "[text(1,4):Item with code.:]",
        "[end-para:::False]",
        "[atx(2,7):2:0:   ]",
        "[text(2,10):this: ]",
        "[end-atx::]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item with code.
<h2>this</h2>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_026ca() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. Item with code.
       ## this
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n]",
        "[para(1,4):\n    ]",
        "[text(1,4):Item with code.\n## this::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item with code.
## this</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_026cb() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. Item with code.
   <html>
      <title>fred</title>
   </html>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n]",
        "[para(1,4):]",
        "[text(1,4):Item with code.:]",
        "[end-para:::False]",
        "[html-block(2,4)]",
        "[text(2,4):<html>\n   <title>fred</title>\n</html>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item with code.
<html>
   <title>fred</title>
</html>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_026cc() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. Item with code.
   <html>
       <title>fred</title>
   </html>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n]",
        "[para(1,4):]",
        "[text(1,4):Item with code.:]",
        "[end-para:::False]",
        "[html-block(2,4)]",
        "[text(2,4):<html>\n    <title>fred</title>\n</html>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item with code.
<html>
    <title>fred</title>
</html>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_026cd() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. Item with code.
   ```text
       this is some text
   ```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n]",
        "[para(1,4):]",
        "[text(1,4):Item with code.:]",
        "[end-para:::False]",
        "[fcode-block(2,4):`:3:text:::::]",
        "[text(3,4):this is some text:    ]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item with code.
<pre><code class="language-text">    this is some text
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_027a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """   1.    >    +
   1.    >    +
       abc"""
    expected_tokens = [
        "[olist(1,4):.:1:9:   ]",
        "[block-quote(1,10):         :         > ]",
        "[ulist(1,15):+::16:   ]",
        "[BLANK(1,16):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[li(2,4):9:   :1]",
        "[block-quote(2,10):         :         > ]",
        "[ulist(2,15):+::16:   ]",
        "[BLANK(2,16):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[icode-block(3,5):    :]",
        "[text(3,5):abc:   ]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
</li>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
</li>
</ol>
<pre><code>   abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_028() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """# Demo markdown

- Item
    - Sub item

1. Ordered item
    - Sub unordered item"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):Demo markdown: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[ulist(3,1):-::2:]",
        "[para(3,3):]",
        "[text(3,3):Item:]",
        "[end-para:::True]",
        "[ulist(4,5):-::6:    :]",
        "[para(4,7):]",
        "[text(4,7):Sub item:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[olist(6,1):.:1:3:]",
        "[para(6,4):]",
        "[text(6,4):Ordered item:]",
        "[end-para:::True]",
        "[ulist(7,5):-::6:    ]",
        "[para(7,7):]",
        "[text(7,7):Sub unordered item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<h1>Demo markdown</h1>
<ul>
<li>Item
<ul>
<li>Sub item</li>
</ul>
</li>
</ul>
<ol>
<li>Ordered item
<ul>
<li>Sub unordered item</li>
</ul>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_028a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. Item
    - Sub item

- Ordered item
    - Sub unordered item"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):Item:]",
        "[end-para:::True]",
        "[ulist(2,5):-::6:    :]",
        "[para(2,7):]",
        "[text(2,7):Sub item:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
        "[end-olist:::True]",
        "[ulist(4,1):-::2:]",
        "[para(4,3):]",
        "[text(4,3):Ordered item:]",
        "[end-para:::True]",
        "[ulist(5,5):-::6:    ]",
        "[para(5,7):]",
        "[text(5,7):Sub unordered item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ol>
<li>Item
<ul>
<li>Sub item</li>
</ul>
</li>
</ol>
<ul>
<li>Ordered item
<ul>
<li>Sub unordered item</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_029x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """- abc

  + def"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[ulist(3,3):+::4:  ]",
        "[para(3,5):]",
        "[text(3,5):def:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>abc</p>
<ul>
<li>def</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_029a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """- l2:
  + il2.1

  ip1
  + il2.2
- l3
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n]",
        "[para(1,3):]",
        "[text(1,3):l2::]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:  :]",
        "[para(2,5):]",
        "[text(2,5):il2.1:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
        "[para(4,3):]",
        "[text(4,3):ip1:]",
        "[end-para:::True]",
        "[ulist(5,3):+::4:  ]",
        "[para(5,5):]",
        "[text(5,5):il2.2:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(6,1):2::]",
        "[para(6,3):]",
        "[text(6,3):l3:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>l2:</p>
<ul>
<li>il2.1</li>
</ul>
<p>ip1</p>
<ul>
<li>il2.2</li>
</ul>
</li>
<li>
<p>l3</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_029b() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """- l2:
  - il2.1

  ip1
  - il2.2
- l3
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n]",
        "[para(1,3):]",
        "[text(1,3):l2::]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :]",
        "[para(2,5):]",
        "[text(2,5):il2.1:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
        "[para(4,3):]",
        "[text(4,3):ip1:]",
        "[end-para:::True]",
        "[ulist(5,3):-::4:  ]",
        "[para(5,5):]",
        "[text(5,5):il2.2:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(6,1):2::]",
        "[para(6,3):]",
        "[text(6,3):l3:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>l2:</p>
<ul>
<li>il2.1</li>
</ul>
<p>ip1</p>
<ul>
<li>il2.2</li>
</ul>
</li>
<li>
<p>l3</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_029c() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """# atx1

p1

- l1

- l2:

  + il2.1

  ip1

  + il2.2

- l3

p4
"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):atx1: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):p1:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[ulist(5,1):-::2::\n\n  \n\n]",
        "[para(5,3):]",
        "[text(5,3):l1:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[li(7,1):2::]",
        "[para(7,3):]",
        "[text(7,3):l2::]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[ulist(9,3):+::4:  :]",
        "[para(9,5):]",
        "[text(9,5):il2.1:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[para(11,3):]",
        "[text(11,3):ip1:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[ulist(13,3):+::4:  :]",
        "[para(13,5):]",
        "[text(13,5):il2.2:]",
        "[end-para:::True]",
        "[BLANK(14,1):]",
        "[end-ulist:::True]",
        "[li(15,1):2::]",
        "[para(15,3):]",
        "[text(15,3):l3:]",
        "[end-para:::True]",
        "[BLANK(16,1):]",
        "[end-ulist:::True]",
        "[para(17,1):]",
        "[text(17,1):p4:]",
        "[end-para:::True]",
        "[BLANK(18,1):]",
    ]
    expected_gfm = """<h1>atx1</h1>
<p>p1</p>
<ul>
<li>
<p>l1</p>
</li>
<li>
<p>l2:</p>
<ul>
<li>il2.1</li>
</ul>
<p>ip1</p>
<ul>
<li>il2.2</li>
</ul>
</li>
<li>
<p>l3</p>
</li>
</ul>
<p>p4</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_029d() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """- l2:
  1. il2.1

  ip1
  1. il2.2
- l3
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n]",
        "[para(1,3):]",
        "[text(1,3):l2::]",
        "[end-para:::True]",
        "[olist(2,3):.:1:5:  :]",
        "[para(2,6):]",
        "[text(2,6):il2.1:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[para(4,3):]",
        "[text(4,3):ip1:]",
        "[end-para:::True]",
        "[olist(5,3):.:1:5:  ]",
        "[para(5,6):]",
        "[text(5,6):il2.2:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(6,1):2::]",
        "[para(6,3):]",
        "[text(6,3):l3:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>l2:</p>
<ol>
<li>il2.1</li>
</ol>
<p>ip1</p>
<ol>
<li>il2.2</li>
</ol>
</li>
<li>
<p>l3</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_029e() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """- l1
+ l2
 """
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):l1:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[ulist(2,1):+::2::]",
        "[para(2,3):]",
        "[text(2,3):l2:]",
        "[end-para:::True]",
        "[BLANK(3,1): ]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>l1</li>
</ul>
<ul>
<li>l2</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_029f() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """- l1
1. l2
 """
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):l1:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[olist(2,1):.:1:3::]",
        "[para(2,4):]",
        "[text(2,4):l2:]",
        "[end-para:::True]",
        "[BLANK(3,1): ]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ul>
<li>l1</li>
</ul>
<ol>
<li>l2</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_029g() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. l1
+ l2
 """
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):l1:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[ulist(2,1):+::2::]",
        "[para(2,3):]",
        "[text(2,3):l2:]",
        "[end-para:::True]",
        "[BLANK(3,1): ]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ol>
<li>l1</li>
</ol>
<ul>
<li>l2</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_029h() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. l1
1) l2
 """
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):l1:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[olist(2,1):):1:3::]",
        "[para(2,4):]",
        "[text(2,4):l2:]",
        "[end-para:::True]",
        "[BLANK(3,1): ]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>l1</li>
</ol>
<ol>
<li>l2</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_030xx() -> None:
    """
    TBD - from test_md010_bad_xxx
    """

    # Arrange
    source_markdown = """1. ```text\tdef
   this contains\ta tab
   ```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n]",
        "[fcode-block(1,4):`:3:text::\tdef:::]",
        "[text(2,4):this contains\ta tab:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code class="language-text">this contains\ta tab
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_030xa() -> None:
    """
    TBD - from test_md010_bad_xxx
    """

    # Arrange
    source_markdown = """+ ```text\tdef
  this contains\ta tab
  ```
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n]",
        "[fcode-block(1,3):`:3:text::\tdef:::]",
        "[text(2,3):this contains\ta tab:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code class="language-text">this contains\ta tab
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_030ax() -> None:
    """
    TBD - from test_md010_bad_xxx
    """

    # Arrange
    source_markdown = """1.  ```text\tdef
    this contains\ta tab
    ```
"""
    expected_tokens = [
        "[olist(1,1):.:1:4::    \n    \n]",
        "[fcode-block(1,5):`:3:text::\tdef:::]",
        "[text(2,5):this contains\ta tab:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code class="language-text">this contains\ta tab
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_030aa() -> None:
    """
    TBD - from test_md010_bad_xxx
    """

    # Arrange
    source_markdown = """+   ```text\tdef
    this contains\ta tab
    ```
"""
    expected_tokens = [
        "[ulist(1,1):+::4::    \n    \n]",
        "[fcode-block(1,5):`:3:text::\tdef:::]",
        "[text(2,5):this contains\ta tab:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code class="language-text">this contains\ta tab
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_030bx() -> None:
    """
    TBD - from test_md010_bad_xxx
    """

    # Arrange
    source_markdown = """1.  ```text\tdef
\tthis contains\ta tab
\t```
"""
    expected_tokens = [
        "[olist(1,1):.:1:4::\t\n\t\n]",
        "[fcode-block(1,5):`:3:text::\tdef:::]",
        "[text(2,2):this contains\ta tab:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code class="language-text">this contains\ta tab
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_030ba() -> None:
    """
    TBD - from test_md010_bad_xxx
    """

    # Arrange
    source_markdown = """+   ```text\tdef
\tthis contains\ta tab
\t```
"""
    expected_tokens = [
        "[ulist(1,1):+::4::\t\n\t\n]",
        "[fcode-block(1,5):`:3:text::\tdef:::]",
        "[text(2,2):this contains\ta tab:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code class="language-text">this contains\ta tab
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_031x() -> None:
    """
    TBD - from test_md010_bad_xxx

    test_markdown_with_config_json_configuration_file
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = """This is an example of running `dig @8.8.8.8 MX +noall +ans oisix.com`:

```text
oisix.com.\t\t300\tIN\tMX\t10 mail01.oisix.com.
oisix.com.\t\t300\tIN\tMX\t100 mail02.oisix.com.
oisix.com.\t\t300\tIN\tMX\t150 mx.idc.jp.
oisix.com.\t\t300\tIN\tMX\t160 mx2.idc.jp.
oisix.com.\t\t300\tIN\tMX\t250 mx3.idc.jp.
```
"""
    specified_configuration = """{
    "plugins" : {
        "no-hard-tabs": {
            "enabled": true,
            "code_blocks": false
        }
    }
}
"""

    with create_temporary_configuration_file(
        specified_configuration, file_name="myconfig"
    ) as configuration_file:
        supplied_arguments = [
            "-c",
            configuration_file,
            "scan-stdin",
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments, standard_input_to_use=stdin_to_use
        )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_extra_032() -> None:
    """
    TBD - from test_md010_bad_xxx
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = """> > <html>
> >   <script>
> >     <!-- some script stuff -->
> >   </script>
> > </html>
"""

    supplied_arguments = [
        # "--log-level",
        # "DEBUG",
        # "--stack-trace",
        "-d",
        "md033,md041",
        "scan-stdin",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=stdin_to_use
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_extra_033x() -> None:
    """
    TBD
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = """> - <script>
>     <!-- some script stuff -->
>   </script>
"""

    supplied_arguments = [
        # "--log-level",
        # "DEBUG",
        "-d",
        "md033,md041",
        "scan-stdin",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=stdin_to_use
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_extra_033a() -> None:
    """
    TBD - from test_md010_bad_xxx
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = """> - ```abc
>   <!-- some script stuff -->
>   ```
"""

    supplied_arguments = [
        # "--log-level",
        # "DEBUG",
        "-d",
        "md033,md041",
        "scan-stdin",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=stdin_to_use
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_extra_034d() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = """- Test List
  > 1) Test1
  > 2) Test2

```text
block
```
"""

    supplied_arguments = [
        "scan-stdin",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=stdin_to_use
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_extra_034e() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/731
    """

    # Arrange
    scanner = MarkdownScanner()
    stdin_to_use = """# Headline 1

- Test List

  > 1) Test1
  > 2) Test2

  <!-- this is html-->
"""

    supplied_arguments = [
        "scan-stdin",
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, standard_input_to_use=stdin_to_use
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_extra_035x() -> None:
    """
    TBD - from https://github.com/jackdewinter/pymarkdown/issues/945
    """

    # Arrange
    scanner = MarkdownScanner()
    input_path = os.path.join("test", "resources", "test-issue-945.md")

    supplied_arguments = ["scan", input_path]

    expected_return_code = 1
    expected_output = """{input_path}:1:1: MD019: Multiple spaces are present after hash character on Atx Heading. (no-multiple-space-atx)
{input_path}:1:2: MD010: Hard tabs [Column: 2] (no-hard-tabs)""".replace(
        "{input_path}", input_path
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


@pytest.mark.gfm
def test_extra_035a() -> None:
    """
    This may look like a blank line, but according to GFM, no space characters above x20
    unless using emphasis.
    """

    # Arrange
    source_markdown = """The next line contains UTF characters c2a0 (NO-BREAK SPACE):
\u00a0
This page should not break pymarkdown"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):The next line contains UTF characters c2a0 (NO-BREAK SPACE):\n\u00a0\nThis page should not break pymarkdown::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>The next line contains UTF characters c2a0 (NO-BREAK SPACE):
\u00a0
This page should not break pymarkdown</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_036() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ # heading 1
  just some text
\t# heading 2
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n\n]",
        "[atx(1,3):1:0:]",
        "[text(1,5):heading 1: ]",
        "[end-atx::]",
        "[para(2,3):]",
        "[text(2,3):just some text:]",
        "[end-para:::False]",
        "[atx(3,5):1:0:\t]",
        "[text(3,7):heading 2: ]",
        "[end-atx::]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h1>heading 1</h1>
just some text
<h1>heading 2</h1>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_037() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1.  A paragraph
with two lines.

1.  A paragraph
    with two lines.
"""
    expected_tokens = [
        "[olist(1,1):.:1:4::\n\n    \n]",
        "[para(1,5):\n]",
        "[text(1,5):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[li(4,1):4::1]",
        "[para(4,5):\n]",
        "[text(4,5):A paragraph\nwith two lines.::\n]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<p>A paragraph
with two lines.</p>
</li>
<li>
<p>A paragraph
with two lines.</p>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_038x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
+ heading 1\a\a
  part 2
  part 3
  ---
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):+::2::  \n  \n  \n]",
        "[setext(5,3):-:3::(2,3)]",
        "[text(2,3):heading 1:]",
        "[hard-break(2,12):  :\n]",
        "[text(3,1):part 2\npart 3::\n]",
        "[end-setext::]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>heading 1<br />
part 2
part 3</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_038a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
heading 1\a\a
 part 2
part 3
---
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):]",
        "[setext(5,1):-:3::(2,1)]",
        "[text(2,1):heading 1:]",
        "[hard-break(2,10):  :\n]",
        "[text(3,2):part 2\npart 3:: \x02\n]",
        "[end-setext::]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<h2>heading 1<br />
part 2
part 3</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_038bx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
+ heading 1\a\a
\tpart 2
\tpart 3
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):+::2::\n\n]",
        "[para(2,3):\n\t\n\t]",
        "[text(2,3):heading 1:]",
        "[hard-break(2,12):  :\n]",
        "[text(3,2):part 2\npart 3::\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>heading 1<br />
part 2
part 3</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_038ba() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
+ heading 1\a\a
\tpart 2
\tpart 3
\t---
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):+::2::\n\n\n]",
        "[setext(5,5):-:3::(2,3)]",
        "[text(2,3):heading 1:]",
        "[hard-break(2,12):  :\n]",
        "[text(3,2):\a\t\a\x03\apart 2\npart 3::\n\t\x02]",
        "[end-setext:\t:]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>heading 1<br />
part 2
part 3</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_038bb() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
+ heading\t1\a\a
\tpart 2
\tpart 3
\t---
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):+::2::\n\n\n]",
        "[setext(5,5):-:3::(2,3)]",
        "[text(2,3):heading\t1:]",
        "[hard-break(2,12):  :\n]",
        "[text(3,2):\a\t\a\x03\apart 2\npart 3::\n\t\x02]",
        "[end-setext:\t:]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>heading\t1<br />
part 2
part 3</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_038bc() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
+ heading 1\t\t
\tpart 2
\tpart 3
\t---
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):+::2::\n\n\n]",
        "[setext(5,5):-:3::(2,3)]",
        "[text(2,3):heading 1\t\t\npart 2\npart 3::\n\t\x02\n\t\x02]",
        "[end-setext:\t:]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>heading 1\t\t
part 2
part 3</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_038bd() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
+ heading\t1\\
\t part 2
\tpart 3
\t---
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):+::2::\n\n\n]",
        "[setext(5,5):-:3::(2,3)]",
        "[text(2,3):heading\t1:]",
        "[hard-break(2,14):\\:\n]",
        "[text(3,3):\a\t \a\x03\apart 2\npart 3::\n\t\x02]",
        "[end-setext:\t:]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>heading	1<br />
part 2
part 3</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_038be() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
+ heading\t1
\tpart 2
\tpart 3
\t---
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):+::2::\n\n\n]",
        "[setext(5,5):-:3::(2,3)]",
        "[text(2,3):heading\t1\npart 2\npart 3::\n\t\x02\n\t\x02]",
        "[end-setext:\t:]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>heading\t1
part 2
part 3</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_038cx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
+ heading 1\a\a
  part 2
  part 3
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):+::2::  \n  \n]",
        "[para(2,3):\n\n]",
        "[text(2,3):heading 1:]",
        "[hard-break(2,12):  :\n]",
        "[text(3,1):part 2\npart 3::\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>heading 1<br />
part 2
part 3</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_038ca() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """
+ heading 1\a\a
  part 2
  part 3
  ---
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):+::2::  \n  \n  \n]",
        "[setext(5,3):-:3::(2,3)]",
        "[text(2,3):heading 1:]",
        "[hard-break(2,12):  :\n]",
        "[text(3,1):part 2\npart 3::\n]",
        "[end-setext::]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>heading 1<br />
part 2
part 3</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_038dx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. heading 1
\tpart 2
   part *3*\a
\tpart 4
   part *5*\a
\tpart 6
   ----
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[olist(1,1):.:1:3::\n   \n\n   \n\n   \n]",
        "[setext(7,4):-:4::(1,4)]",
        "[text(1,4):heading 1\npart 2\npart ::\n\t\x02\n]",
        "[emphasis(3,6):1:*]",
        "[text(3,7):3:]",
        "[end-emphasis(3,8)::]",
        "[text(3,9):\npart 4\npart :: \n\t\x02\n]",
        "[emphasis(5,6):1:*]",
        "[text(5,7):5:]",
        "[end-emphasis(5,8)::]",
        "[text(5,9):\npart 6:: \n\t\x02]",
        "[end-setext::]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>heading 1
part 2
part <em>3</em>
part 4
part <em>5</em>
part 6</h2>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_038da() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. heading *1*\a
\tpart 2
   part *3*\a
\tpart 4
   part *5*\a
\tpart 6
   ----
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[olist(1,1):.:1:3::\n   \n\n   \n\n   \n]",
        "[setext(7,4):-:4::(1,4)]",
        "[text(1,4):heading :]",
        "[emphasis(1,12):1:*]",
        "[text(1,13):1:]",
        "[end-emphasis(1,14)::]",
        "[text(1,15):\npart 2\npart :: \n\t\x02\n]",
        "[emphasis(3,6):1:*]",
        "[text(3,7):3:]",
        "[end-emphasis(3,8)::]",
        "[text(3,9):\npart 4\npart :: \n\t\x02\n]",
        "[emphasis(5,6):1:*]",
        "[text(5,7):5:]",
        "[end-emphasis(5,8)::]",
        "[text(5,9):\npart 6:: \n\t\x02]",
        "[end-setext::]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>heading <em>1</em>
part 2
part <em>3</em>
part 4
part <em>5</em>
part 6</h2>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_039x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ heading 2\a\a
\tpart 2
\tpart 3
\tpart 4
\t----
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n\n\n]",
        "[setext(5,5):-:4::(1,3)]",
        "[text(1,3):heading 2:]",
        "[hard-break(1,12):  :\n]",
        "[text(2,2):\a\t\a\x03\apart 2\npart 3\npart 4::\n\t\x02\n\t\x02]",
        "[end-setext:\t:]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>heading 2<br />
part 2
part 3
part 4</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_039a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. heading 1
\tpart 2
   part 3\a\a
\tpart 4
   part 5\a\a
\tpart 6
   ----
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[olist(1,1):.:1:3::\n   \n\n   \n\n   \n]",
        "[setext(7,4):-:4::(1,4)]",
        "[text(1,4):heading 1\npart 2\npart 3::\n\t\x02\n]",
        "[hard-break(3,7):  :\n]",
        "[text(4,2):\a\t\a\x03\apart 4\npart 5::\n]",
        "[hard-break(5,7):  :\n]",
        "[text(6,2):\a\t\a\x03\apart 6:]",
        "[end-setext::]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h2>heading 1
part 2
part 3<br />
part 4
part 5<br />
part 6</h2>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_040x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ heading `1` abc
\tpart 2
\tpart 3
\t----
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n\n]",
        "[setext(4,5):-:4::(1,3)]",
        "[text(1,3):heading :]",
        "[icode-span(1,11):1:`::]",
        "[text(1,14): abc\npart 2\npart 3::\n\t\x02\n\t\x02]",
        "[end-setext:\t:]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>heading <code>1</code> abc
part 2
part 3</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_040a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ heading `\t1` abc
\tpart 2
\tpart 3
\t----
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n\n]",
        "[setext(4,5):-:4::(1,3)]",
        "[text(1,3):heading :]",
        "[icode-span(1,11):\t1:`::]",
        "[text(1,15): abc\npart 2\npart 3::\n\t\x02\n\t\x02]",
        "[end-setext:\t:]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>heading <code>\t1</code> abc
part 2
part 3</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_040b() -> None:
    """
    TBD, when fixed, also fix bad_setext_four_unordered_list_with_tab_codespan_13
    """

    # Arrange
    source_markdown = """+ heading 1 `abc
\tdef` part 2
\tpart 3
\t----
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n\n]",
        "[setext(4,5):-:4::(1,3)]",
        "[text(1,3):heading 1 :]",
        "[icode-span(1,13):abc\a\n\a \a\tdef:`::]",
        "[text(2,6): part 2\npart 3::\n\t\x02]",
        "[end-setext:\t:]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>heading 1 <code>abc \tdef</code> part 2
part 3</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_040c() -> None:
    """
    TBD, when fixed, also fix bad_setext_four_unordered_list_with_tab_codespan_13
    """

    # Arrange
    source_markdown = """+ heading 1 `abc
  def` part 2
  part 3
  ----
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n]",
        "[setext(4,3):-:4::(1,3)]",
        "[text(1,3):heading 1 :]",
        "[icode-span(1,13):abc\a\n\a \adef:`::]",
        "[text(2,5): part 2\npart 3::\n]",
        "[end-setext::]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>heading 1 <code>abc def</code> part 2
part 3</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_040d() -> None:
    """
    TBD, when fixed, also fix bad_setext_four_unordered_list_with_tab_codespan_13
    """

    # Arrange
    source_markdown = """+ heading 1 `abc
   def` part 2
  part 3
  ----
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n]",
        "[setext(4,3):-:4::(1,3)]",
        "[text(1,3):heading 1 :]",
        "[icode-span(1,13):abc\a\n\a \a def:`::]",
        "[text(2,6): part 2\npart 3::\n]",
        "[end-setext::]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>heading 1 <code>abc  def</code> part 2
part 3</h2>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_040e() -> None:
    """
    TBD, when fixed, also fix bad_setext_four_unordered_list_with_tab_codespan_13
    """

    # Arrange
    source_markdown = """+ heading 1 `abc
\tdef` part 2
\tpart 3

"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n\n]",
        "[para(1,3):\n\t\n\t]",
        "[text(1,3):heading 1 :]",
        "[icode-span(1,13):abc\a\n\a \a\a\x03\a\t\adef:`::]",
        "[text(2,5): part 2\npart 3::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>heading 1 <code>abc \tdef</code> part 2
part 3</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_041x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """Consider this code:

\tcode block here
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):Consider this code::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[icode-block(3,5):\t:]",
        "[text(3,5):code block here:]",
        "[end-icode-block:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>Consider this code:</p>
<pre><code>code block here
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_041a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """- Consider this code:

\tcode block here
"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n\n]",
        "[para(1,3):]",
        "[text(1,3):Consider this code::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,5):\t]",
        "[text(3,5):code block here:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>Consider this code:</p>
<p>code block here</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_042b() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """- Consider this code:

\tcode block here
- **resource**: produces a resource

\t```mcl
\tfile "/tmp/hello" {
\t}
\t```

"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n\n\n\n\n\n\n\n]",
        "[para(1,3):]",
        "[text(1,3):Consider this code::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,5):\t]",
        "[text(3,5):code block here:]",
        "[end-para:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[emphasis(4,3):2:*]",
        "[text(4,5):resource:]",
        "[end-emphasis(4,13)::]",
        "[text(4,15):: produces a resource:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[fcode-block(6,5):`:3:mcl::::\t:]",
        '[text(7,1):file \a"\a&quot;\a/tmp/hello\a"\a&quot;\a {\n\a\t\a\x03\a}:\a\t\a\x03\a]',
        "[end-fcode-block:\t::3:False]",
        "[BLANK(10,1):]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>Consider this code:</p>
<p>code block here</p>
</li>
<li>
<p><strong>resource</strong>: produces a resource</p>
<pre><code class="language-mcl">file &quot;/tmp/hello&quot; {
}
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_042c() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """- Consider this code:

\tcode block here
- **resource**: produces a resource

\t```mcl
\tfile "/tmp/hello" {
\t\tcontent => "world",
\t\tmode => "o=rwx",
\t}
\t```

"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n\n\n\n\n\n\n\n]",
        "[para(1,3):]",
        "[text(1,3):Consider this code::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,5):\t]",
        "[text(3,5):code block here:]",
        "[end-para:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[emphasis(4,3):2:*]",
        "[text(4,5):resource:]",
        "[end-emphasis(4,13)::]",
        "[text(4,15):: produces a resource:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[fcode-block(6,5):`:3:mcl::::\t:]",
        '[text(7,1):file \a"\a&quot;\a/tmp/hello\a"\a&quot;\a {\n\a\t\a\x03\a\tcontent =\a>\a&gt;\a \a"\a&quot;\aworld\a"\a&quot;\a,\n\a\t\a\x03\a\tmode =\a>\a&gt;\a \a"\a&quot;\ao=rwx\a"\a&quot;\a,\n\a\t\a\x03\a}:\a\t\a\x03\a]',
        "[end-fcode-block:\t::3:False]",
        "[BLANK(12,1):]",
        "[BLANK(13,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>Consider this code:</p>
<p>code block here</p>
</li>
<li>
<p><strong>resource</strong>: produces a resource</p>
<pre><code class="language-mcl">file &quot;/tmp/hello&quot; {
\tcontent =&gt; &quot;world&quot;,
\tmode =&gt; &quot;o=rwx&quot;,
}
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_042d() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> **resource**: produces a resource

>\t```mcl
>\tfile "/tmp/hello" {
>\t\tcontent => "world",
>\t\tmode => "o=rwx",
>\t}
>\t```

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):]",
        "[emphasis(1,3):2:*]",
        "[text(1,5):resource:]",
        "[end-emphasis(1,13)::]",
        "[text(1,15):: produces a resource:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::>\n>\n>\n>\n>\n>\n]",
        "[fcode-block(3,5):`:3:mcl::::\t:]",
        '[text(4,2):file \a"\a&quot;\a/tmp/hello\a"\a&quot;\a {\n\a\t\t\a\t\acontent =\a>\a&gt;\a \a"\a&quot;\aworld\a"\a&quot;\a,\n\a\t\t\a\t\amode =\a>\a&gt;\a \a"\a&quot;\ao=rwx\a"\a&quot;\a,\n\a\t\a\x03\a}:\a\t\a\x03\a]',
        "[end-fcode-block:\t::3:False]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<p><strong>resource</strong>: produces a resource</p>
</blockquote>
<blockquote>
<pre><code class="language-mcl">file &quot;/tmp/hello&quot; {
\tcontent =&gt; &quot;world&quot;,
\tmode =&gt; &quot;o=rwx&quot;,
}
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_042x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """# test

## Example: [foo][bar]

[foo]: https://example.com
"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):test: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[atx(3,1):2:0:]",
        "[text(3,4):Example: [foo][bar]: ]",
        "[end-atx::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::foo:: :https://example.com:::::]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<h1>test</h1>
<h2>Example: [foo][bar]</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_042xx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """# test

## Example: [foo][bar]

[bar]: https://example.com
"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):test: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[atx(3,1):2:0:]",
        "[text(3,4):Example: : ]",
        "[link(3,13):full:https://example.com::::bar:foo:False::::]",
        "[text(3,14):foo:]",
        "[end-link::]",
        "[end-atx::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::bar:: :https://example.com:::::]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<h1>test</h1>
<h2>Example: <a href="https://example.com">foo</a></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_042xa() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """# test

## Example: [foo](https://example.com)

"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):test: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[atx(3,1):2:0:]",
        "[text(3,4):Example: : ]",
        "[link(3,13):inline:https://example.com:::::foo:False::::]",
        "[text(3,14):foo:]",
        "[end-link::]",
        "[end-atx::]",
        "[BLANK(4,1):]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<h1>test</h1>
<h2>Example: <a href="https://example.com">foo</a></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_042xb() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """# test

## Example: [foo]

[foo]: https://example.com
"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):test: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[atx(3,1):2:0:]",
        "[text(3,4):Example: : ]",
        "[link(3,13):shortcut:https://example.com:::::foo:False::::]",
        "[text(3,14):foo:]",
        "[end-link::]",
        "[end-atx::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::foo:: :https://example.com:::::]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<h1>test</h1>
<h2>Example: <a href="https://example.com">foo</a></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_042xc() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """# test

## Example: [foo][]

[foo]: https://example.com
"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):test: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[atx(3,1):2:0:]",
        "[text(3,4):Example: : ]",
        "[link(3,13):collapsed:https://example.com:::::foo:False::::]",
        "[text(3,14):foo:]",
        "[end-link::]",
        "[end-atx::]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::foo:: :https://example.com:::::]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<h1>test</h1>
<h2>Example: <a href="https://example.com">foo</a></h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_043x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """this \\* text * is * in italics"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this \\\b* text * is * in italics:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this * text * is * in italics</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_043a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """this &#x2a; text * is * in italics"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this \a&#x2a;\a*\a text * is * in italics:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this * text * is * in italics</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044d() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> > inner block
> > inner block
> This is text and no blank line.
> ```block
> A code block
> ```
> This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[block-quote(1,3)::> > \n> > \n> \n> ]",
        "[para(1,5):\n\n]",
        "[text(1,5):inner block\ninner block\nThis is text and no blank line.::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[para(7,3):]",
        "[text(7,3):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block
inner block
This is text and no blank line.</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044e() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> > inner block
> > inner block
> This is text and no blank line.
>
> ```block
> A code block
> ```
>
> This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> \n]",
        "[block-quote(1,3)::> > \n> > \n> \n>]",
        "[para(1,5):\n\n]",
        "[text(1,5):inner block\ninner block\nThis is text and no blank line.::\n\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[para(9,3):]",
        "[text(9,3):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block
inner block
This is text and no blank line.</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044jeb() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + > -----
>     > block
>     > abc
>     > un-block
>     > _____
>   + > more
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n\n\n]",
        "[block-quote(1,7)::> \n>     > \n>     > \n>     > \n>     > ]",
        "[tbreak(1,9):-::-----]",
        "[para(2,9):\n\n]",
        "[text(2,9):block\nabc\nun-block::\n\n]",
        "[end-para:::False]",
        "[tbreak(5,9):_::_____]",
        "[end-block-quote:::True]",
        "[li(6,5):6:  :]",
        "[block-quote(6,7)::> \n]",
        "[para(6,9):]",
        "[text(6,9):more:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<blockquote>
<hr />
<p>block
abc
un-block</p>
<hr />
</blockquote>
</li>
<li>
<blockquote>
<p>more</p>
</blockquote>
</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
@pytest.mark.skip
def test_extra_044jec() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > + > -----
>   >   > block
>   >   > abc
>   >   > un-block
>   >   > _____
>   > + > more
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::\n\n\n]",
        "[block-quote(1,5)::> \n>   > ]",
        "[para(1,7):]",
        "[text(1,7):+ \a>\a&gt;\a -----:]",
        "[end-para:::True]",
        "[block-quote(2,9)::>   >   > \n>   > \n>   >   > \n>   > \n>   >   > \n>   > \n>   >   > \n>   > \n>   >   > ]",
        "[para(2,11):\n\n]",
        "[text(2,11):block\nabc\nun-block::\n\n]",
        "[end-para:::False]",
        "[tbreak(5,11):_::_____]",
        "[ulist(6,7):+::8:]",
        "[para(6,11):]",
        "[text(6,11):more:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>block
abc
un-block</p>
<hr />
</blockquote>
</li>
<li>
<blockquote>
<p>more</p>
</blockquote>
</li>
</ul>
</blockquote>
</li>
</ul>
</blockquote>
"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mb() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """>
> > fourth block 1
"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):]",
        "[text(2,5):fourth block 1:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>fourth block 1</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_044mcxx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> +  list
>   this
> + that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::5::  ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this</li>
<li>that</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_044mcxa() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+  list
  this
+ that
"""
    expected_tokens = [
        "[ulist(1,1):+::3::\n]",
        "[para(1,4):\n  ]",
        "[text(1,4):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,1):2::]",
        "[para(3,3):]",
        "[text(3,3):that:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>list
this</li>
<li>that</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_044mca() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list
>   this
> + that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::4::  ]",
        "[para(1,5):\n]",
        "[text(1,5):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this</li>
<li>that</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcb() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> +  list
>    this
> +  that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::5::   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):5::]",
        "[para(3,6):]",
        "[text(3,6):that:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this</li>
<li>that</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcc() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> +  list
> this
> + that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::5::]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this</li>
<li>that</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_044mcd() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> +  list
>  this
> + that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::5:: ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this</li>
<li>that</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_044mce() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> +  list
>    this
> + that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::5::   ]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
this</li>
<li>that</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046a() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block
    """

    # Arrange
    source_markdown = """> + list 1
>   list 2
>   ------
>   ```block
>   A code block
>   ```
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  \n  \n  ]",
        "[setext(3,5):-:6::(1,5)]",
        "[text(1,5):list 1\nlist 2::\n]",
        "[end-setext::]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,5):-::------]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<h2>list 1
list 2</h2>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046cx() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block
    """

    # Arrange
    source_markdown = """> > inner block
> > inner block
>
> This is text and no blank line.
> ---
>
> ```block
> A code block
> ```
>
> ---
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> \n>\n> \n>\n]",
        "[block-quote(1,3)::> > \n> > \n>]",
        "[para(1,5):\n]",
        "[text(1,5):inner block\ninner block::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[end-block-quote:::True]",
        "[setext(5,3):-:3::(4,3)]",
        "[text(4,3):This is text and no blank line.:]",
        "[end-setext::]",
        "[BLANK(6,2):]",
        "[fcode-block(7,3):`:3:block:::::]",
        "[text(8,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,2):]",
        "[tbreak(11,3):-::---]",
        "[para(12,2):]",
        "[text(12,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(13,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block
inner block</p>
</blockquote>
<h2>This is text and no blank line.</h2>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046l0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_bare
    """

    # Arrange
    source_markdown = """> + list
>   ```block
>   A code block
>   ```
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  ]",
        "[para(1,5):]",
        "[text(1,5):list:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:block:::::]",
        "[text(3,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(5,3):4::]",
        "[para(5,5):]",
        "[text(5,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046l1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_bare
    """

    # Arrange
    source_markdown = """> + list
>
>   ```block
>   A code block
>   ```
>
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> \n> \n>\n> ]",
        "[ulist(1,3):+::4::\n  \n  \n  \n]",
        "[para(1,5):]",
        "[text(1,5):list:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[fcode-block(3,5):`:3:block:::::]",
        "[text(4,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,2):]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list</p>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046w0a() -> None:
    """
    TBD
    bad_fenced_block_surrounded_by_list
    """

    # Arrange
    source_markdown = """+ list
```block
A code block
```
1. another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[para(1,3):]",
        "[text(1,3):list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[fcode-block(2,1):`:3:block:::::]",
        "[text(3,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[olist(5,1):.:1:3::]",
        "[para(5,4):]",
        "[text(5,4):another list:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ul>
<li>list</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<ol>
<li>another list</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046w1() -> None:
    """
    TBD
    bad_fenced_block_surrounded_by_list
    """

    # Arrange
    source_markdown = """+ list

```block
A code block
```

1. another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::]",
        "[para(1,3):]",
        "[text(1,3):list:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[end-ulist:::True]",
        "[fcode-block(3,1):`:3:block:::::]",
        "[text(4,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
        "[olist(7,1):.:1:3::]",
        "[para(7,4):]",
        "[text(7,4):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ul>
<li>list</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<ol>
<li>another list</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046x0() -> None:
    """
    TBD
    bad_fenced_block_surrounded_by_block_quote
    """

    # Arrange
    source_markdown = """> block quote
```block
A code block
```
> block quote
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(2,1):`:3:block:::::]",
        "[text(3,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[block-quote(5,1)::> \n]",
        "[para(5,3):]",
        "[text(5,3):block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<p>block quote</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<blockquote>
<p>block quote</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046x1() -> None:
    """
    TBD
    bad_fenced_block_surrounded_by_block_quote
    """

    # Arrange
    source_markdown = """> block quote

```block
A code block
```

> block quote
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):]",
        "[text(1,3):block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[fcode-block(3,1):`:3:block:::::]",
        "[text(4,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
        "[block-quote(7,1)::> \n]",
        "[para(7,3):]",
        "[text(7,3):block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<p>block quote</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<blockquote>
<p>block quote</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047b0() -> None:
    """
    TBD
    bad_fenced_block_in_list_with_previous_inner_list
    """

    # Arrange
    source_markdown = """+ list
  + inner list
    couple of lines
  ```block
  A code block
  ```
+ another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):list:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:  :    ]",
        "[para(2,5):\n]",
        "[text(2,5):inner list\ncouple of lines::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(7,1):2::]",
        "[para(7,3):]",
        "[text(7,3):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>list
<ul>
<li>inner list
couple of lines</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>another list</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047b1() -> None:
    """
    TBD
    bad_fenced_block_in_list_with_previous_inner_list
    """

    # Arrange
    source_markdown = """+ list
  + inner list
    couple of lines

  ```block
  A code block
  ```

+ another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n\n]",
        "[para(1,3):]",
        "[text(1,3):list:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:  :    \n]",
        "[para(2,5):\n]",
        "[text(2,5):inner list\ncouple of lines::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[li(9,1):2::]",
        "[para(9,3):]",
        "[text(9,3):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>list</p>
<ul>
<li>inner list
couple of lines</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>
<p>another list</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047c0() -> None:
    """
    TBD
    bad_fenced_block_in_list_with_previous_inner_list_with_thematics
    """

    # Arrange
    source_markdown = """+ list
  + inner list
    couple of lines
  -----
  ```block
  A code block
  ```
  -----
+ another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):list:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:  :    ]",
        "[para(2,5):\n]",
        "[text(2,5):inner list\ncouple of lines::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,3):-::-----]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,3):-::-----]",
        "[li(9,1):2::]",
        "[para(9,3):]",
        "[text(9,3):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>list
<ul>
<li>inner list
couple of lines</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047c1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list
    """

    # Arrange
    source_markdown = """+ list
  + inner list
    couple of lines
  -----

  ```block
  A code block
  ```

  -----
+ another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n\n  \n  \n  \n\n  \n]",
        "[para(1,3):]",
        "[text(1,3):list:]",
        "[end-para:::True]",
        "[ulist(2,3):+::4:  :    ]",
        "[para(2,5):\n]",
        "[text(2,5):inner list\ncouple of lines::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,3):-::-----]",
        "[BLANK(5,1):]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[tbreak(10,3):-::-----]",
        "[li(11,1):2::]",
        "[para(11,3):]",
        "[text(11,3):another list:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>list</p>
<ul>
<li>inner list
couple of lines</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047f0() -> None:
    """
    TBD
    bad_fenced_block_only_after_in_block_quote_with_thematics
    """

    # Arrange
    source_markdown = """> This is text and no blank line.
> ---
> ```block
> A code block
> ```
>
> ---
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> \n>\n]",
        "[setext(2,3):-:3::(1,3)]",
        "[text(1,3):This is text and no blank line.:]",
        "[end-setext::]",
        "[fcode-block(3,3):`:3:block:::::]",
        "[text(4,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,2):]",
        "[tbreak(7,3):-::---]",
        "[para(8,2):]",
        "[text(8,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<h2>This is text and no blank line.</h2>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047f1() -> None:
    """
    TBD
    bad_fenced_block_only_before_in_block_quote_with_thematics
    """

    # Arrange
    source_markdown = """> This is text and no blank line.
> ---
> ```block
> A code block
> ```
>
> ---
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> \n>\n]",
        "[setext(2,3):-:3::(1,3)]",
        "[text(1,3):This is text and no blank line.:]",
        "[end-setext::]",
        "[fcode-block(3,3):`:3:block:::::]",
        "[text(4,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,2):]",
        "[tbreak(7,3):-::---]",
        "[para(8,2):]",
        "[text(8,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<h2>This is text and no blank line.</h2>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047f1a() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_with_previous_inner_block_with_setext
    """

    # Arrange
    source_markdown = """> > inner block
> > inner block
>
> This is text and no blank line.
> ---
> ```block
> A code block
> ```
> ---
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n>\n]",
        "[block-quote(1,3)::> > \n> > \n>]",
        "[para(1,5):\n]",
        "[text(1,5):inner block\ninner block::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[end-block-quote:::True]",
        "[setext(5,3):-:3::(4,3)]",
        "[text(4,3):This is text and no blank line.:]",
        "[end-setext::]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,3):-::---]",
        "[para(10,2):]",
        "[text(10,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block
inner block</p>
</blockquote>
<h2>This is text and no blank line.</h2>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047f2() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_with_previous_inner_block_and_para_continue_and_thematics
    """

    # Arrange
    source_markdown = """> > inner block
> > inner block
> This is text and no blank line.
> ---
> ```block
> A code block
> ```
> ---
> This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n]",
        "[block-quote(1,3)::> > \n> > \n> \n> ]",
        "[para(1,5):\n\n]",
        "[text(1,5):inner block\ninner block\nThis is text and no blank line.::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[tbreak(4,3):-::---]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,3):-::---]",
        "[para(9,3):]",
        "[text(9,3):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block
inner block
This is text and no blank line.</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047f4() -> None:
    """
    TBD
    bad_fenced_block_surrounded_by_block_quote_with_thematics
    """

    # Arrange
    source_markdown = """> block quote
---
```block
A code block
```
---
> block quote
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[tbreak(2,1):-::---]",
        "[fcode-block(3,1):`:3:block:::::]",
        "[text(4,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(6,1):-::---]",
        "[block-quote(7,1)::> \n]",
        "[para(7,3):]",
        "[text(7,3):block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<p>block quote</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<blockquote>
<p>block quote</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047f5() -> None:
    """
    TBD
    bad_fenced_block_surrounded_by_block_quote_with_setext
    """

    # Arrange
    source_markdown = """> block quote

abc
---
```block
A code block
```
abc
---
> block quote
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):]",
        "[text(1,3):block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[setext(4,1):-:3::(3,1)]",
        "[text(3,1):abc:]",
        "[end-setext::]",
        "[fcode-block(5,1):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[setext(9,1):-:3::(8,1)]",
        "[text(8,1):abc:]",
        "[end-setext::]",
        "[block-quote(10,1)::> \n]",
        "[para(10,3):]",
        "[text(10,3):block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<p>block quote</p>
</blockquote>
<h2>abc</h2>
<pre><code class="language-block">A code block
</code></pre>
<h2>abc</h2>
<blockquote>
<p>block quote</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049a0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_double_drop_with_thematics
    """

    # Arrange
    source_markdown = """1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   > ----
   > ```block
   > A code block
   > ```
   > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > \n   > \n   > \n   > \n   > \n]",
        "[ulist(1,6):+::7:]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9:  :    \n]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9:  :]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[tbreak(5,6):-::----]",
        "[fcode-block(6,6):`:3:block:::::]",
        "[text(7,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,6):-::----]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049b0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_triple_drop
    """

    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> --------
> ```block
> A code block
> ```
> --------
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n]",
        "[block-quote(1,3)::> > \n> > ]",
        "[ulist(1,5):+::6::\n\n]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[tbreak(4,3):-::--------]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,3):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_049b1a() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_triple_drop_with_thematics
    """

    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> --------
> ```block
> A code block
> ```
> --------
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n]",
        "[block-quote(1,3)::> > \n> > ]",
        "[ulist(1,5):+::6::\n\n]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[tbreak(4,3):-::--------]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,3):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_049b1b() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_triple_drop_with_thematics
    """

    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> --------
>
> ```block
> A code block
> ```
>
> --------
"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n> \n>\n> \n]",
        "[block-quote(1,3)::> > \n> > ]",
        "[ulist(1,5):+::6::\n\n]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[tbreak(4,3):-::--------]",
        "[BLANK(5,2):]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,3):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_049c0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_quad_drop
    """

    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
```block
A code block
```
--------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > ]",
        "[ulist(1,5):+::6::\n\n]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,1):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,1):-::--------]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049c1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_quad_drop_with_thematics
    """

    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
--------
```block
A code block
```
--------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > ]",
        "[ulist(1,5):+::6::\n\n]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[tbreak(4,1):-::--------]",
        "[fcode-block(5,1):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,1):-::--------]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</blockquote>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049d0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_quad_drop
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
```block
A code block
```
-----
another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,1):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,1):-::-----]",
        "[para(8,1):]",
        "[text(8,1):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049d1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_quad_drop_with_thematics
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
-----
```block
A code block
```
-----
another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[tbreak(4,1):-::-----]",
        "[fcode-block(5,1):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,1):-::-----]",
        "[para(9,1):]",
        "[text(9,1):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049e0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blockx_quad_drop
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
```block
A code block
```
-----
another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::\n\n]",
        "[block-quote(1,5)::> \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,1):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,1):-::-----]",
        "[para(8,1):]",
        "[text(8,1):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</blockquote>
</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049f0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block_quad_drop
    """

    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
```block
A code block
```
----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,6):+::7::\n\n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[fcode-block(4,1):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,1):-::----]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</blockquote>
</li>
</ol>
<pre><code class="language-block">A code block
</code></pre>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049g0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block_triple_drop
    """

    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
```block
A code block
```
----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,6):+::7::\n\n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
        "[fcode-block(4,1):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,1):-::----]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</blockquote>
</li>
</ol>
<pre><code class="language-block">A code block
</code></pre>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049h0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_quad_drop_with_thematics
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
-----
```block
A code block
```
-----
another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::\n\n]",
        "[block-quote(1,5)::> \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[tbreak(4,1):-::-----]",
        "[fcode-block(5,1):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,1):-::-----]",
        "[para(9,1):]",
        "[text(9,1):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</blockquote>
</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049j0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_quad_drop
    """

    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
```block
A code block
```
-----
another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,1):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,1):-::-----]",
        "[para(9,1):]",
        "[text(9,1):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049j1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_quad_drop_and_thematics
    """

    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
-----
```block
A code block
```
-----
another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[tbreak(5,1):-::-----]",
        "[fcode-block(6,1):`:3:block:::::]",
        "[text(7,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,1):-::-----]",
        "[para(10,1):]",
        "[text(10,1):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049k0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_triple_drop
    """

    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
------
```block
A code block
```
------
another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[tbreak(4,1):-::------]",
        "[fcode-block(5,1):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,1):-::------]",
        "[para(9,1):]",
        "[text(9,1):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<blockquote>
<p>block 2
block 3</p>
</blockquote>
</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049k1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_triple_drop_without_thematics
    """

    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
```block
A code block
```
another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,1):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[para(7,1):]",
        "[text(7,1):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<blockquote>
<p>block 2
block 3</p>
</blockquote>
</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<p>another list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049l0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_list_double_drop
    """

    # Arrange
    source_markdown = """> > + block 3
> >   block 3
> > + block 3
> ```block
> A code block
> ```
> --------
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[block-quote(1,3)::> > \n> > \n> > \n> ]",
        "[ulist(1,5):+::6::  \n]",
        "[para(1,7):\n]",
        "[text(1,7):block 3\nblock 3::\n]",
        "[end-para:::True]",
        "[li(3,5):6::]",
        "[para(3,7):]",
        "[text(3,7):block 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,3):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>block 3
block 3</li>
<li>block 3</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_049l1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_list_double_drop
    """

    # Arrange
    source_markdown = """> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> > ```block
> > A code block
> > ```
> > --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n]",
        "[block-quote(1,5)::> > >\n> > > \n> > > \n> > > \n> > ]",
        "[BLANK(1,6):]",
        "[ulist(2,7):+::8::  \n]",
        "[para(2,9):\n]",
        "[text(2,9):inner list 1\ninner list 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):inner list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::--------]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<ul>
<li>inner list 1
inner list 2</li>
<li>inner list 3</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049l2a() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> ```block
> A code block
> ```
> --------
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > >\n> > > \n> > > \n> > > \n> ]",
        "[BLANK(1,6):]",
        "[ulist(2,7):+::8::  \n]",
        "[para(2,9):\n]",
        "[text(2,9):inner list 1\ninner list 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):inner list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,3):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<ul>
<li>inner list 1
inner list 2</li>
<li>inner list 3</li>
</ul>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_049l2b() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
>
> ```block
> A code block
> ```
>
> --------
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> \n]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > >\n> > > \n> > > \n> > > \n>]",
        "[BLANK(1,6):]",
        "[ulist(2,7):+::8::  \n]",
        "[para(2,9):\n]",
        "[text(2,9):inner list 1\ninner list 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):inner list 3:]",
        "[end-para:::True]",
        "[BLANK(5,2):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,3):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<ul>
<li>inner list 1
inner list 2</li>
<li>inner list 3</li>
</ul>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_049l3a() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> ```block
> A code block
> ```
> ______
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> ]",
        "[ulist(1,5):+::6:]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,3):_::______]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049l3b() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
>
> ```block
> A code block
> ```
>
> ______
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> \n]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n>]",
        "[ulist(1,5):+::6:]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[BLANK(5,2):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,3):_::______]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049l5() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_inner_list_double_drop
    """

    # Arrange
    source_markdown = """1. > > ----
   > > + block 1
   > >   block 2
   > ```block
   > A code block
   > ```
   > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > ]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9::  \n]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,6):`:3:block:::::]",
        "[text(5,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,6):-::----]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<ul>
<li>block 1
block 2</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049l6() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_double_drop
    """

    # Arrange
    source_markdown = """1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > ```block
   > A code block
   > ```
   > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > ]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9::  \n]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9::]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,6):`:3:block:::::]",
        "[text(6,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,6):-::----]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049l7a() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_double_drop_x
    """

    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   ```block
>   A code block
>   ```
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  ]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n> ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::-----]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_049l7b() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_double_drop_x
    """

    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n\n  ]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  \n]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[BLANK(5,2):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,5):-::-----]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_049l8a() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
> ```block
> A code block
> ```
> -----
> another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n]",
        "[ulist(1,3):+::4:]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n> ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  \n]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,3):-::-----]",
        "[para(9,3):]",
        "[text(9,3):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049l8b() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>
> ```block
> A code block
> ```
>
> -----
> another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> \n]",
        "[ulist(1,3):+::4:]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  \n]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::False]",
        "[BLANK(5,2):]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,3):-::-----]",
        "[para(11,3):]",
        "[text(11,3):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_049l8c() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   >   list 3
>
> ```block
> A code block
> ```
>
> -----
> another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> \n]",
        "[ulist(1,3):+::4:]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  \n  \n]",
        "[para(2,9):\n\n]",
        "[text(2,9):list 1\nlist 2\nlist 3::\n\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::False]",
        "[BLANK(5,2):]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,3):-::-----]",
        "[para(11,3):]",
        "[text(11,3):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2
list 3</li>
</ul>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_049l9a() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """+ + > -----
    > + list 1
    >   list 2
    > + list 3
    ```block
    A code block
    ```
    -----
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :    \n    \n    \n    \n]",
        "[block-quote(1,5):    :    > \n    > \n    > \n    > ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::-----]",
        "[li(9,3):4:  :]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049l9b() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """+ + > -----
    > + list 1
    >   list 2
    > + list 3

    ```block
    A code block
    ```

    -----
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :\n    \n    \n    \n\n    \n]",
        "[block-quote(1,5):    :    > \n    > \n    > \n    > ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[tbreak(10,5):-::-----]",
        "[li(11,3):4:  :]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_049l4xa() -> None:
    """
    TBD
    preventing bad_fenced_block_in_list_in_list_in_list_with_previous_block_double_drop
    """

    # Arrange
    source_markdown = """+ + + -----
      > block 1
      > block 2
    ```block
    A code block
    ```
    -----
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :    \n    \n    \n]",
        "[ulist(1,5):+::6:    :\n\n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7):      :      > \n      > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,5):-::-----]",
        "[li(8,3):4:  :]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_049l4xb() -> None:
    """
    TBD
    preventing bad_fenced_block_in_list_in_list_in_list_with_previous_block_double_drop
    """

    # Arrange
    source_markdown = """+ + + -----
      > block 1
      > block 2

    ```block
    A code block
    ```

    -----
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :    \n    \n    \n\n    \n]",
        "[ulist(1,5):+::6:    :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7):      :      > \n      > \n]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[tbreak(9,5):-::-----]",
        "[li(10,3):4:  :]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_049l4a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ + + -----
    ```block
    A code block
    ```
    -----
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :    \n    \n    \n    \n]",
        "[ulist(1,5):+::6:    ]",
        "[tbreak(1,7):-::-----]",
        "[end-ulist:::True]",
        "[fcode-block(2,5):`:3:block:::::]",
        "[text(3,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(5,5):-::-----]",
        "[li(6,3):4:  :]",
        "[para(6,5):]",
        "[text(6,5):another list:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_extra_050a0a() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_with_previous_inner_block_double_drop
    """

    # Arrange
    source_markdown = """+ + list 1
    > block 2.1
    > block 2.2
  ```block
  A code block
  ```
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n]",
        "[ulist(1,3):+::4:  :\n\n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5):    :    > \n    > ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2.1\nblock 2.2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[para(7,3):]",
        "[text(7,3):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>list 1
<blockquote>
<p>block 2.1
block 2.2</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
another list</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_050a0b() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_with_previous_inner_block_double_drop
    """

    # Arrange
    source_markdown = """+ + list 1
    > block 2.1
    > block 2.2

  ```block
  A code block
  ```

  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n\n  \n]",
        "[ulist(1,3):+::4:  :\n\n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5):    :    > \n    > \n]",
        "[para(2,7):\n]",
        "[text(2,7):block 2.1\nblock 2.2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[para(9,3):]",
        "[text(9,3):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>list 1
<blockquote>
<p>block 2.1
block 2.2</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<p>another list</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_extra_050b0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_list_with_previous_list_double_drop
    """

    # Arrange
    source_markdown = """+ + + -----
      + list 1
        list 2
      + list 3
    ```block
    A code block
    ```
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :    \n    \n    \n]",
        "[ulist(1,5):+::6:    ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:      :        ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:      :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(8,3):4:  :]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_050b1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_list_with_previous_list_double_drop
    """

    # Arrange
    source_markdown = """+ + + -----
      + list 1
        list 2
      + list 3

    ```block
    A code block
    ```

  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :    \n    \n    \n\n]",
        "[ulist(1,5):+::6:    ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:      :        \n]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:      :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[li(10,3):4:  :]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>
<p>another list</p>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_050c0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_list_with_previous_block_triple_drop_with_thematics
    """

    # Arrange
    source_markdown = """+ + + -----
      > block 1
      > block 2
  -----
  ```block
  A code block
  ```
  -----
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n  \n  \n]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    :\n\n  ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7):      :      > \n      > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,3):-::-----]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,3):-::-----]",
        "[para(9,3):]",
        "[text(9,3):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
another list</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_050c1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_list_with_previous_block_triple_drop_with_thematics
    """

    # Arrange
    source_markdown = """+ + + -----
      > block 1
      > block 2
  -----

  ```block
  A code block
  ```

  -----
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n  \n  \n  \n\n  \n  \n]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    :\n\n  ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7):      :      > \n      > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,3):-::-----]",
        "[BLANK(5,1):]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[tbreak(10,3):-::-----]",
        "[para(11,3):]",
        "[text(11,3):another list:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_050c2() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_list_with_previous_block_quad_drop
    """

    # Arrange
    source_markdown = """+ + + -----
      > block 1
      > block 2
```block
A code block
```
-----
another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7):      :      > \n      > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,1):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,1):-::-----]",
        "[para(8,1):]",
        "[text(8,1):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_050c3() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_list_with_previous_block_quad_drop
    """

    # Arrange
    source_markdown = """+ + + -----
      > block 1
      > block 2

```block
A code block
```

-----
another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7):      :      > \n      > \n]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,1):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[tbreak(9,1):-::-----]",
        "[para(10,1):]",
        "[text(10,1):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_050d0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_double_drop
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>   ```block
>   A code block
>   ```
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  ]",
        "[ulist(1,5):+::6:  :\n\n  þ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,5):-::-----]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_050d1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_double_drop
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n\n  ]",
        "[ulist(1,5):+::6:  :\n\n\n  ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n>]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[tbreak(9,5):-::-----]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_extra_050e0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block_double_drop
    """

    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
   > ```block
   > A code block
   > ```
   > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > \n]",
        "[ulist(1,6):+::7::\n\n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > \n   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,6):`:3:block:::::]",
        "[text(5,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,6):-::----]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_extra_050e1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block_double_drop
    """

    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
   >
   > ```block
   > A code block
   > ```
   >
   > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > \n   >\n   > \n]",
        "[ulist(1,6):+::7::\n\n\n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > \n   >]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,5):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,6):`:3:block:::::]",
        "[text(6,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,5):]",
        "[tbreak(9,6):-::----]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_050f0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   ```block
   A code block
   ```
   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n   \n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7:]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9:  :    ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9:  :]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,4):`:3:block:::::]",
        "[text(6,4):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,4):-::----]",
        "[BLANK(9,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_050f1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """1. > + ----
   >   + list 1
   >     list 2
   >   + list 3

   ```block
   A code block
   ```

   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n   \n   \n   \n\n   \n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7:]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9:  :    ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9:  :]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[fcode-block(6,4):`:3:block:::::]",
        "[text(7,4):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[tbreak(10,4):-::----]",
        "[BLANK(11,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_050g0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_double_drop_with_previous_inner_block
    """

    # Arrange
    source_markdown = """> > > block 3
> > > block 3
> > > block 3
> ```block
> A code block
> ```
> text
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > > \n> > > \n> > > \n> ]",
        "[para(1,7):\n\n]",
        "[text(1,7):block 3\nblock 3\nblock 3::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[para(7,3):]",
        "[text(7,3):text:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>block 3
block 3
block 3</p>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<p>text</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_050g1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_double_drop_with_previous_inner_block
    """

    # Arrange
    source_markdown = """> > > block 3
> > > block 3
> > > block 3
>
> ```block
> A code block
> ```
>
> text
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> \n]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > > \n> > > \n> > > \n>]",
        "[para(1,7):\n\n]",
        "[text(1,7):block 3\nblock 3\nblock 3::\n\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[para(9,3):]",
        "[text(9,3):text:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>block 3
block 3
block 3</p>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<p>text</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_extra_050h0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_list_double_drop
    """

    # Arrange
    source_markdown = """> > + block 3
> >   block 3
> > + block 3
> ```block
> A code block
> ```
> --------
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[block-quote(1,3)::> > \n> > \n> > \n> ]",
        "[ulist(1,5):+::6::  \n]",
        "[para(1,7):\n]",
        "[text(1,7):block 3\nblock 3::\n]",
        "[end-para:::True]",
        "[li(3,5):6::]",
        "[para(3,7):]",
        "[text(3,7):block 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,3):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>block 3
block 3</li>
<li>block 3</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_050h1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_with_previous_inner_list_double_drop
    """

    # Arrange
    source_markdown = """> > + block 3
> >   block 3
> > + block 3
>
> ```block
> A code block
> ```
>
> --------
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> \n]",
        "[block-quote(1,3)::> > \n> > \n> > \n>]",
        "[ulist(1,5):+::6::  \n]",
        "[para(1,7):\n]",
        "[text(1,7):block 3\nblock 3::\n]",
        "[end-para:::True]",
        "[li(3,5):6::]",
        "[para(3,7):]",
        "[text(3,7):block 3:]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[tbreak(9,3):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>block 3
block 3</li>
<li>block 3</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_extra_051a0() -> None:
    """
    TBD
    bad_in_list_with_double_blanks_at_end
    """

    # Arrange
    source_markdown = """1. fred


1. barney
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):fred:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[BLANK(3,1):]",
        "[li(4,1):3::1]",
        "[para(4,4):]",
        "[text(4,4):barney:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<p>fred</p>
</li>
<li>
<p>barney</p>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051a1() -> None:
    """
    TBD
    bad_in_list_with_double_blanks_at_start
    """

    # Arrange
    source_markdown = """1.

   fred2
1. barney
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[BLANK(2,1):]",
        "[para(3,4):   ]",
        "[text(3,4):fred2:]",
        "[end-para:::True]",
        "[olist(4,1):.:1:3::]",
        "[para(4,4):]",
        "[text(4,4):barney:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<p>fred2</p>
<ol>
<li>barney</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051a2() -> None:
    """
    TBD
    bad_in_list_in_block_quote_with_double_blanks_at_start

    Note: If there was any paragraph text one line 1, the list would be held open.
          Without that, it is just text indented with 3 spaces.
    """

    # Arrange
    source_markdown = """> 1.
>
>    fred2
> 1. barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[BLANK(1,5):]",
        "[end-olist:::True]",
        "[BLANK(2,2):]",
        "[para(3,6):   ]",
        "[text(3,6):fred2:]",
        "[end-para:::True]",
        "[olist(4,3):.:1:5:]",
        "[para(4,6):]",
        "[text(4,6):barney:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li></li>
</ol>
<p>fred2</p>
<ol>
<li>barney</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051b0() -> None:
    """
    TBD
    bad_in_list_in_block_quote_with_triple_blanks_at_middle
    """

    # Arrange
    source_markdown = """> 1. fred
>
>
>
>    fred2
> 1. barney"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n>\n>\n> \n> ]",
        "[olist(1,3):.:1:5::\n\n\n   ]",
        "[para(1,6):]",
        "[text(1,6):fred:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[BLANK(3,2):]",
        "[BLANK(4,2):]",
        "[para(5,6):]",
        "[text(5,6):fred2:]",
        "[end-para:::True]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):barney:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<p>fred</p>
<p>fred2</p>
</li>
<li>
<p>barney</p>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051b1() -> None:
    """
    TBD
    bad_in_list_in_block_quote_with_triple_blanks_at_middle
    """

    # Arrange
    source_markdown = """> 1. fred
>
>    fred2
> 1. barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> ]",
        "[olist(1,3):.:1:5::\n   ]",
        "[para(1,6):]",
        "[text(1,6):fred:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[para(3,6):]",
        "[text(3,6):fred2:]",
        "[end-para:::True]",
        "[li(4,3):5::1]",
        "[para(4,6):]",
        "[text(4,6):barney:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>
<p>fred</p>
<p>fred2</p>
</li>
<li>
<p>barney</p>
</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051b2() -> None:
    """
    TBD
    md012_bad_in_list_in_block_quote_with_double_blanks_at_start
    """

    # Arrange
    source_markdown = """> 1.
>
>    fred2
> 1. barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> ]",
        "[olist(1,3):.:1:5:]",
        "[BLANK(1,5):]",
        "[end-olist:::True]",
        "[BLANK(2,2):]",
        "[para(3,6):   ]",
        "[text(3,6):fred2:]",
        "[end-para:::True]",
        "[olist(4,3):.:1:5:]",
        "[para(4,6):]",
        "[text(4,6):barney:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li></li>
</ol>
<p>fred2</p>
<ol>
<li>barney</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c0x() -> None:
    """
    TBD
    bad_in_list_in_list_with_double_blanks_at_start
    """

    # Arrange
    source_markdown = """+ 1.

     fred2
+ 1. barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n  ]",
        "[olist(1,3):.:1:5:  ]",
        "[BLANK(1,5):]",
        "[end-olist:::True]",
        "[BLANK(2,1):]",
        "[para(3,6):   ]",
        "[text(3,6):fred2:]",
        "[end-para:::True]",
        "[li(4,1):2::]",
        "[olist(4,3):.:1:5:  :]",
        "[para(4,6):]",
        "[text(4,6):barney:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li></li>
</ol>
<p>fred2</p>
</li>
<li>
<ol>
<li>barney</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c0a() -> None:
    """
    TBD
    bad_in_list_in_list_with_double_blanks_at_start
    """

    # Arrange
    source_markdown = """+ 1. abc

     fred2
+ 1. barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[olist(1,3):.:1:5:  :\n     ]",
        "[para(1,6):]",
        "[text(1,6):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,6):]",
        "[text(3,6):fred2:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(4,1):2::]",
        "[olist(4,3):.:1:5:  :]",
        "[para(4,6):]",
        "[text(4,6):barney:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ol>
<li>
<p>abc</p>
<p>fred2</p>
</li>
</ol>
</li>
<li>
<ol>
<li>barney</li>
</ol>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c1x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ +

    fred2
+ + barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n  ]",
        "[ulist(1,3):+::4:  ]",
        "[BLANK(1,4):]",
        "[end-ulist:::True]",
        "[BLANK(2,1):]",
        "[para(3,5):  ]",
        "[text(3,5):fred2:]",
        "[end-para:::True]",
        "[li(4,1):2::]",
        "[ulist(4,3):+::4:  :]",
        "[para(4,5):]",
        "[text(4,5):barney:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li></li>
</ul>
<p>fred2</p>
</li>
<li>
<ul>
<li>barney</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c1a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ + abc

    fred2
+ + barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :\n    ]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,5):]",
        "[text(3,5):fred2:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(4,1):2::]",
        "[ulist(4,3):+::4:  :]",
        "[para(4,5):]",
        "[text(4,5):barney:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<p>abc</p>
<p>fred2</p>
</li>
</ul>
</li>
<li>
<ul>
<li>barney</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c2() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> +
>
>   fred2
> + barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[BLANK(1,4):]",
        "[end-ulist:::True]",
        "[BLANK(2,2):]",
        "[para(3,5):  ]",
        "[text(3,5):fred2:]",
        "[end-para:::True]",
        "[ulist(4,3):+::4:]",
        "[para(4,5):]",
        "[text(4,5):barney:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li></li>
</ul>
<p>fred2</p>
<ul>
<li>barney</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c3x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> +

>   fred2
> + barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4:]",
        "[BLANK(1,4):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> \n> ]",
        "[para(3,5):  ]",
        "[text(3,5):fred2:]",
        "[end-para:::True]",
        "[ulist(4,3):+::4:]",
        "[para(4,5):]",
        "[text(4,5):barney:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<blockquote>
<p>fred2</p>
<ul>
<li>barney</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c3a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + abc

>   fred2
> + barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4:]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> \n> ]",
        "[para(3,5):  ]",
        "[text(3,5):fred2:]",
        "[end-para:::True]",
        "[ulist(4,3):+::4:]",
        "[para(4,5):]",
        "[text(4,5):barney:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>abc</li>
</ul>
</blockquote>
<blockquote>
<p>fred2</p>
<ul>
<li>barney</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c4x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> abc

> fred2
> barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> \n> \n]",
        "[para(3,3):\n]",
        "[text(3,3):fred2\nbarney::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
</blockquote>
<blockquote>
<p>fred2
barney</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c4a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """>

> fred2
> barney
"""
    expected_tokens = [
        "[block-quote(1,1)::>\n]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> \n> \n]",
        "[para(3,3):\n]",
        "[text(3,3):fred2\nbarney::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<blockquote>
<p>fred2
barney</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c5x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ abc

  fred2
  barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,3):\n]",
        "[text(3,3):fred2\nbarney::\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>abc</p>
<p>fred2
barney</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c5a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+

  fred2
  barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[BLANK(1,2):]",
        "[end-ulist:::True]",
        "[BLANK(2,1):]",
        "[para(3,3):  \n  ]",
        "[text(3,3):fred2\nbarney::\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ul>
<li></li>
</ul>
<p>fred2
barney</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c6x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ >

  > fred2
+ > barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n\n]",
        "[block-quote(1,3):  :  >\n]",
        "[BLANK(1,4):]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,3):  :  > ]",
        "[para(3,5):]",
        "[text(3,5):fred2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[block-quote(4,3):  :  > \n]",
        "[para(4,5):]",
        "[text(4,5):barney:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
</blockquote>
<blockquote>
<p>fred2</p>
</blockquote>
</li>
<li>
<blockquote>
<p>barney</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c6a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ > abc

  > fred2
+ > barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n\n]",
        "[block-quote(1,3):  :  > \n]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,3):  :  > ]",
        "[para(3,5):]",
        "[text(3,5):fred2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[block-quote(4,3):  :  > \n]",
        "[para(4,5):]",
        "[text(4,5):barney:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<p>abc</p>
</blockquote>
<blockquote>
<p>fred2</p>
</blockquote>
</li>
<li>
<blockquote>
<p>barney</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c7x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> >

> > fred2
> > barney
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> >\n]",
        "[BLANK(1,4):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::]",
        "[block-quote(3,3)::> > \n> > \n]",
        "[para(3,5):\n]",
        "[text(3,5):fred2\nbarney::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
</blockquote>
</blockquote>
<blockquote>
<blockquote>
<p>fred2
barney</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c7a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> > abc

> > fred2
> > barney
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::]",
        "[block-quote(3,3)::> > \n> > \n]",
        "[para(3,5):\n]",
        "[text(3,5):fred2\nbarney::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>abc</p>
</blockquote>
</blockquote>
<blockquote>
<blockquote>
<p>fred2
barney</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c8x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> > >

> > > fred2
> > > barney
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > >\n]",
        "[BLANK(1,6):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::]",
        "[block-quote(3,3)::]",
        "[block-quote(3,5)::> > > \n> > > \n]",
        "[para(3,7):\n]",
        "[text(3,7):fred2\nbarney::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
</blockquote>
<blockquote>
<blockquote>
<blockquote>
<p>fred2
barney</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c8a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> > > abc

> > > fred2
> > > barney
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > > \n]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::]",
        "[block-quote(3,3)::]",
        "[block-quote(3,5)::> > > \n> > > \n]",
        "[para(3,7):\n]",
        "[text(3,7):fred2\nbarney::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>abc</p>
</blockquote>
</blockquote>
</blockquote>
<blockquote>
<blockquote>
<blockquote>
<p>fred2
barney</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c9x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ > >

  > > fred2
+ > > barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n\n]",
        "[block-quote(1,3):  :]",
        "[block-quote(1,5):  :  > >\n]",
        "[BLANK(1,6):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,3):  :]",
        "[block-quote(3,5):  :  > > ]",
        "[para(3,7):]",
        "[text(3,7):fred2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[block-quote(4,3):  :]",
        "[block-quote(4,5):  :  > > \n]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
</blockquote>
</blockquote>
<blockquote>
<blockquote>
<p>fred2</p>
</blockquote>
</blockquote>
</li>
<li>
<blockquote>
<blockquote>
<p>barney</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051c9a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ > > abc

  > > fred2
+ > > barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n\n]",
        "[block-quote(1,3):  :]",
        "[block-quote(1,5):  :  > > \n]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,3):  :]",
        "[block-quote(3,5):  :  > > ]",
        "[para(3,7):]",
        "[text(3,7):fred2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[block-quote(4,3):  :]",
        "[block-quote(4,5):  :  > > \n]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<blockquote>
<p>abc</p>
</blockquote>
</blockquote>
<blockquote>
<blockquote>
<p>fred2</p>
</blockquote>
</blockquote>
</li>
<li>
<blockquote>
<blockquote>
<p>barney</p>
</blockquote>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cax() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ + >

    > fred2
  + > barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :\n\n\n]",
        "[block-quote(1,5):    :    >\n]",
        "[BLANK(1,6):]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,5):    :    > ]",
        "[para(3,7):]",
        "[text(3,7):fred2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(4,3):4:  :]",
        "[block-quote(4,5):    :    > \n]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
</blockquote>
<blockquote>
<p>fred2</p>
</blockquote>
</li>
<li>
<blockquote>
<p>barney</p>
</blockquote>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051caa() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ + > abc

    > fred2
  + > barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :\n\n\n]",
        "[block-quote(1,5):    :    > \n]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,5):    :    > ]",
        "[para(3,7):]",
        "[text(3,7):fred2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(4,3):4:  :]",
        "[block-quote(4,5):    :    > \n]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<p>abc</p>
</blockquote>
<blockquote>
<p>fred2</p>
</blockquote>
</li>
<li>
<blockquote>
<p>barney</p>
</blockquote>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cbx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + >

>   > fred2
> + > barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4:]",
        "[block-quote(1,5)::>\n]",
        "[BLANK(1,6):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> \n> ]",
        "[block-quote(3,5)::>   > ]",
        "[para(3,7):]",
        "[text(3,7):fred2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(4,3):+::4:]",
        "[block-quote(4,5)::> \n]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
</blockquote>
</li>
</ul>
</blockquote>
<blockquote>
<blockquote>
<p>fred2</p>
</blockquote>
<ul>
<li>
<blockquote>
<p>barney</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cba() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > abc

>   > fred2
> + > barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4:]",
        "[block-quote(1,5)::> \n]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> \n> ]",
        "[block-quote(3,5)::>   > ]",
        "[para(3,7):]",
        "[text(3,7):fred2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(4,3):+::4:]",
        "[block-quote(4,5)::> \n]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>abc</p>
</blockquote>
</li>
</ul>
</blockquote>
<blockquote>
<blockquote>
<p>fred2</p>
</blockquote>
<ul>
<li>
<blockquote>
<p>barney</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cbb() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > abc

> > fred2
> + > barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4:]",
        "[block-quote(1,5)::> \n]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> ]",
        "[block-quote(3,3)::> > ]",
        "[para(3,5):]",
        "[text(3,5):fred2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(4,3):+::4:]",
        "[block-quote(4,5)::> \n]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<p>abc</p>
</blockquote>
</li>
</ul>
</blockquote>
<blockquote>
<blockquote>
<p>fred2</p>
</blockquote>
<ul>
<li>
<blockquote>
<p>barney</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cbc() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> > fred2
> + > barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[block-quote(1,3)::> > ]",
        "[para(1,5):]",
        "[text(1,5):fred2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:]",
        "[block-quote(2,5)::> \n]",
        "[para(2,7):]",
        "[text(2,7):barney:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>fred2</p>
</blockquote>
<ul>
<li>
<blockquote>
<p>barney</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cbd() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> > fred2
>   > barney
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n>   > \n]",
        "[para(1,5):\n]",
        "[text(1,5):fred2\nbarney::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>fred2
barney</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cbe() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """>   > fred2
> + > barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[block-quote(1,5)::>   > ]",
        "[para(1,7):]",
        "[text(1,7):fred2:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(2,3):+::4:]",
        "[block-quote(2,5)::> \n]",
        "[para(2,7):]",
        "[text(2,7):barney:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>fred2</p>
</blockquote>
<ul>
<li>
<blockquote>
<p>barney</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051ccx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> > +

> >   fred2
> > + barney
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > ]",
        "[ulist(1,5):+::6:]",
        "[BLANK(1,6):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::]",
        "[block-quote(3,3)::> > \n> > ]",
        "[para(3,7):  ]",
        "[text(3,7):fred2:]",
        "[end-para:::True]",
        "[ulist(4,5):+::6:]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
</blockquote>
<blockquote>
<blockquote>
<p>fred2</p>
<ul>
<li>barney</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cca() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + abc

> >   fred2
> > + barney
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > ]",
        "[ulist(1,5):+::6:]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::]",
        "[block-quote(3,3)::> > \n> > ]",
        "[para(3,7):  ]",
        "[text(3,7):fred2:]",
        "[end-para:::True]",
        "[ulist(4,5):+::6:]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>abc</li>
</ul>
</blockquote>
</blockquote>
<blockquote>
<blockquote>
<p>fred2</p>
<ul>
<li>barney</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cdx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ > +

  >   fred2
  > + barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[block-quote(1,3):  :  > ]",
        "[ulist(1,5):+::6:]",
        "[BLANK(1,6):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,3):  :  > \n  > ]",
        "[para(3,7):  ]",
        "[text(3,7):fred2:]",
        "[end-para:::True]",
        "[ulist(4,5):+::6:]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li></li>
</ul>
</blockquote>
<blockquote>
<p>fred2</p>
<ul>
<li>barney</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cda() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ > + abc

  >   fred2
  > + barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n\n]",
        "[block-quote(1,3):  :  > ]",
        "[ulist(1,5):+::6:]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,3):  :  > \n  > ]",
        "[para(3,7):  ]",
        "[text(3,7):fred2:]",
        "[end-para:::True]",
        "[ulist(4,5):+::6:]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<blockquote>
<ul>
<li>abc</li>
</ul>
</blockquote>
<blockquote>
<p>fred2</p>
<ul>
<li>barney</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cex() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ + +

      fred2
    + barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :\n    ]",
        "[ulist(1,5):+::6:    ]",
        "[BLANK(1,6):]",
        "[end-ulist:::True]",
        "[BLANK(2,1):]",
        "[para(3,7):  ]",
        "[text(3,7):fred2:]",
        "[end-para:::True]",
        "[ulist(4,5):+::6:    :]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li></li>
</ul>
<p>fred2</p>
<ul>
<li>barney</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cea() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """+ + + abc

      fred2
    + barney
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    :\n      \n]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,7):]",
        "[text(3,7):fred2:]",
        "[end-para:::True]",
        "[li(4,5):6:    :]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<p>abc</p>
<p>fred2</p>
</li>
<li>
<p>barney</p>
</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cfx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + +

>     fred2
>   + barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  ]",
        "[BLANK(1,6):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> \n> ]",
        "[icode-block(3,7):    :]",
        "[text(3,7):fred2:]",
        "[end-icode-block:::True]",
        "[ulist(4,5):+::6:  ]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li></li>
</ul>
</li>
</ul>
</blockquote>
<blockquote>
<pre><code>fred2
</code></pre>
<ul>
<li>barney</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051cfa() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + abc

>     fred2
>   + barney
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> \n> ]",
        "[icode-block(3,7):    :]",
        "[text(3,7):fred2:]",
        "[end-icode-block:::True]",
        "[ulist(4,5):+::6:  ]",
        "[para(4,7):]",
        "[text(4,7):barney:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>abc</li>
</ul>
</li>
</ul>
</blockquote>
<blockquote>
<pre><code>fred2
</code></pre>
<ul>
<li>barney</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051d() -> None:
    """
    TBD
    bad_single_block_quote_space_bottom
    """

    # Arrange
    source_markdown = """> this is text
>
>  within a block quote
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n]",
        "[para(1,3):]",
        "[text(1,3):this is text:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[para(3,4): ]",
        "[text(3,4):within a block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text</p>
<p>within a block quote</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051e() -> None:
    """
    TBD
    bad_unordered_list_fall_off_after_fenced_open
    """

    # Arrange
    source_markdown = """+ this is text

  ```text\tdef
+ this contains\ta tab
  ```
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):this is text:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[fcode-block(3,3):`:3:text::\tdef:::]",
        "[end-fcode-block::::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):this contains\ta tab:]",
        "[end-para:::False]",
        "[fcode-block(5,3):`:3::::::]",
        "[text(6,1)::]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>this is text</p>
<pre><code class="language-text"></code></pre>
</li>
<li>
<p>this contains\ta tab</p>
<pre><code></code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051f0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_double_drop_and_thematics
    """

    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   -----
>   ```block
>   A code block
>   ```
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  þ\n  \n  \n  \n  ]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n> ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote::> :True]",
        "[tbreak(5,3):-::-----]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,5):-::-----]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051f1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_double_drop_and_thematics
    """

    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   -----
>
>   ```block
>   A code block
>   ```
>   -----
>
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> \n> \n> \n>\n> ]",
        "[ulist(1,3):+::4::  þ\n\n  \n  \n  \n  \n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n> ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote::> :True]",
        "[tbreak(5,3):-::-----]",
        "[BLANK(6,2):]",
        "[fcode-block(7,5):`:3:block:::::]",
        "[text(8,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(10,5):-::-----]",
        "[BLANK(11,2):]",
        "[li(12,3):4::]",
        "[para(12,5):]",
        "[text(12,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(13,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051g0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_triple_drop_and_thematics
    """

    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
> -----
> ```block
> A code block
> ```
> -----
> another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n> ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[tbreak(5,3):-::-----]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,3):-::-----]",
        "[para(10,3):]",
        "[text(10,3):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051g1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_triple_drop_and_thematics
    """

    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
> -----
>
> ```block
> A code block
> ```
>
> -----
> another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> \n> \n>\n> \n> \n]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n> ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[tbreak(5,3):-::-----]",
        "[BLANK(6,2):]",
        "[fcode-block(7,3):`:3:block:::::]",
        "[text(8,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,2):]",
        "[tbreak(11,3):-::-----]",
        "[para(12,3):]",
        "[text(12,3):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(13,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051h0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_triple_drop
    """

    # Arrange
    source_markdown = """> > >
> > > > fourth block 1
> > > > fourth block 2
> ```block
> A code block
> ```
> --------
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > >]",
        "[BLANK(1,6):]",
        "[block-quote(2,1)::> > > > \n> > > > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):fourth block 1\nfourth block 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,3):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<blockquote>
<p>fourth block 1
fourth block 2</p>
</blockquote>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051h1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_triple_drop
    """

    # Arrange
    source_markdown = """> > >
> > > > fourth block 1
> > > > fourth block 2
>
> ```block
> A code block
> ```
>
> --------
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> \n]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > >]",
        "[BLANK(1,6):]",
        "[block-quote(2,1)::> > > > \n> > > > \n>]",
        "[para(2,9):\n]",
        "[text(2,9):fourth block 1\nfourth block 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[tbreak(9,3):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<blockquote>
<p>fourth block 1
fourth block 2</p>
</blockquote>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051j0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_triple_drop_with_thematics
    """

    # Arrange
    source_markdown = """> > >
> > > > fourth block 1
> > > > fourth block 2
> --------
> ```block
> A code block
> ```
> --------
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > >]",
        "[BLANK(1,6):]",
        "[block-quote(2,1)::> > > > \n> > > > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):fourth block 1\nfourth block 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[tbreak(4,3):-::--------]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,3):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<blockquote>
<p>fourth block 1
fourth block 2</p>
</blockquote>
</blockquote>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_051k0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_triple_drop_with_thematics
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
> -----
> ```block
> A code block
> ```
> -----
> another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n]",
        "[ulist(1,3):+::4::\n\n]",
        "[block-quote(1,5)::> \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,3):-::-----]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,3):-::-----]",
        "[para(9,3):]",
        "[text(9,3):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</blockquote>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052a0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_double_drop
    """

    # Arrange
    source_markdown = """> > >
> > > > fourth block 1
> > > > fourth block 2
> > ```block
> > A code block
> > ```
> > --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n]",
        "[block-quote(1,5)::> > >]",
        "[BLANK(1,6):]",
        "[block-quote(2,1)::> > > > \n> > > > \n> > ]",
        "[para(2,9):\n]",
        "[text(2,9):fourth block 1\nfourth block 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,5):-::--------]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<blockquote>
<p>fourth block 1
fourth block 2</p>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052a1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_block_quote_with_previous_block_double_drop
    """

    # Arrange
    source_markdown = """> > >
> > > > fourth block 1
> > > > fourth block 2
> >
> > ```block
> > A code block
> > ```
> >
> > --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> >\n> > \n]",
        "[block-quote(1,5)::> > >]",
        "[BLANK(1,6):]",
        "[block-quote(2,1)::> > > > \n> > > > \n> >]",
        "[para(2,9):\n]",
        "[text(2,9):fourth block 1\nfourth block 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,4):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,4):]",
        "[tbreak(9,5):-::--------]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<blockquote>
<p>fourth block 1
fourth block 2</p>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052b0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_double_drop_without_thematics
    """

    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
> ```block
> A code block
> ```
> another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n]",
        "[ulist(1,3):+::4::\n\n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n> ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[para(7,3):]",
        "[text(7,3):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<blockquote>
<p>block 2
block 3</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<p>another list</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052b1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_double_drop_without_thematics
    """

    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
>
> ```block
> A code block
> ```
>
> another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> \n]",
        "[ulist(1,3):+::4::\n\n\n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n>]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[para(9,3):]",
        "[text(9,3):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<blockquote>
<p>block 2
block 3</p>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<p>another list</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052c0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_double_drop_with_thematics
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>   -----
>   ```block
>   A code block
>   ```
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  ]",
        "[ulist(1,5):+::6:  :\n\n  þ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::-----]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::-----]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052c1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_double_drop_with_thematics
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>   -----
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::\n  \n  \n  \n\n  ]",
        "[ulist(1,5):+::6:  :\n\n  þ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::-----]",
        "[BLANK(5,2):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,4):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,5):-::-----]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052d0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_triple_drop_and_thematics
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> ______
> ```block
> A code block
> ```
> ______
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> ]",
        "[ulist(1,5):+::6:]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote::> :True]",
        "[tbreak(5,3):_::______]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,3):_::______]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052d1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_triple_drop_and_thematics
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> ______
>
> ```block
> A code block
> ```
>
> ______
"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n> \n>\n> \n]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> ]",
        "[ulist(1,5):+::6:]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote::> :True]",
        "[tbreak(5,3):_::______]",
        "[BLANK(6,2):]",
        "[fcode-block(7,3):`:3:block:::::]",
        "[text(8,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,2):]",
        "[tbreak(11,3):_::______]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052e0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_double_drop_with_thematics
    """

    # Arrange
    source_markdown = """1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > ----
   > ```block
   > A code block
   > ```
   > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > ]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9::  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9::]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote::   > :True]",
        "[tbreak(5,6):-::----]",
        "[fcode-block(6,6):`:3:block:::::]",
        "[text(7,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,6):-::----]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052e1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_double_drop_with_thematics
    """

    # Arrange
    source_markdown = """1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > ----
   >
   > ```block
   > A code block
   > ```
   >
   > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :   >\n   > \n   > \n   > \n   >\n   > \n]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > ]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9::  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9::]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-block-quote::   > :True]",
        "[tbreak(5,6):-::----]",
        "[BLANK(6,5):]",
        "[fcode-block(7,6):`:3:block:::::]",
        "[text(8,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,5):]",
        "[tbreak(11,6):-::----]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052f0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_inner_list_triple_drop
    """

    # Arrange
    source_markdown = """1. > > ----
   > > + block 1
   > >   block 2
   ```block
   A code block
   ```
   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n   \n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > ]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9::  ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,4):`:3:block:::::]",
        "[text(5,4):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,4):-::----]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<ul>
<li>block 1
block 2</li>
</ul>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052f1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_inner_list_triple_drop
    """

    # Arrange
    source_markdown = """1. > > ----
   > > + block 1
   > >   block 2

   ```block
   A code block
   ```

   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n   \n   \n   \n\n   \n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > ]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9::  ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[fcode-block(5,4):`:3:block:::::]",
        "[text(6,4):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[tbreak(9,4):-::----]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<ul>
<li>block 1
block 2</li>
</ul>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052g0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block_triple_drop
    """

    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
   ```block
   A code block
   ```
   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n]",
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,6):+::7::\n\n   ]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,4):`:3:block:::::]",
        "[text(5,4):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,4):-::----]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052g1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block_triple_drop
    """

    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2

   ```block
   A code block
   ```

   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n   \n   \n   \n\n   \n]",
        "[block-quote(1,4):   :   > \n   > ]",
        "[ulist(1,6):+::7::\n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > \n]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[fcode-block(5,4):`:3:block:::::]",
        "[text(6,4):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[tbreak(9,4):-::----]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052h0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_triple_drop_with_thematics
    """

    # Arrange
    source_markdown = """1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   ----
   ```block
   A code block
   ```
   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n   \n   \n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > ]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9::  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9::]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[tbreak(5,4):-::----]",
        "[fcode-block(6,4):`:3:block:::::]",
        "[text(7,4):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,4):-::----]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052h1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_triple_drop_with_thematics
    """

    # Arrange
    source_markdown = """1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   ----

   ```block
   A code block
   ```

   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n\n   \n   \n   \n\n   \n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > ]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9::  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9::]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[tbreak(5,4):-::----]",
        "[BLANK(6,1):]",
        "[fcode-block(7,4):`:3:block:::::]",
        "[text(8,4):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,1):]",
        "[tbreak(11,4):-::----]",
        "[BLANK(12,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052j0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_triple_drop
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
> ```block
> A code block
> ```
> -----
> another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,3):-::-----]",
        "[para(8,3):]",
        "[text(8,3):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052j1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_triple_drop
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>
> ```block
> A code block
> ```
>
> -----
> another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> \n> \n]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n>]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[tbreak(9,3):-::-----]",
        "[para(10,3):]",
        "[text(10,3):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052k0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_triple_drop_with_thematics
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
> -----
> ```block
> A code block
> ```
> -----
> another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,3):-::-----]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,3):-::-----]",
        "[para(9,3):]",
        "[text(9,3):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052k1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_triple_drop_with_thematics
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
> -----
>
> ```block
> A code block
> ```
>
> -----
> another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> \n>\n> \n> \n]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,3):-::-----]",
        "[BLANK(5,2):]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,3):-::-----]",
        "[para(11,3):]",
        "[text(11,3):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052l0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_double_drop
    """

    # Arrange
    source_markdown = """> + + -----
>     + list 1
>       list 2
>     + list 3
>   ```block
>   A code block
>   ```
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  ]",
        "[ulist(1,5):+::6:  ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:    :      \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::-----]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052l1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_double_drop
    """

    # Arrange
    source_markdown = """> + + -----
>     + list 1
>       list 2
>     + list 3
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n\n  ]",
        "[ulist(1,5):+::6:  ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:    :      \n\n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[BLANK(5,2):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,5):-::-----]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052m0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_double_drop
    """

    # Arrange
    source_markdown = """> + + -----
>     + list 1
>       list 2
>     + list 3
>   -----
>   ```block
>   A code block
>   ```
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  ]",
        "[ulist(1,5):+::6:  ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:    :      \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[tbreak(5,5):-::-----]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,5):-::-----]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_extra_052m1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_double_drop
    """

    # Arrange
    source_markdown = """> + + -----
>     + list 1
>       list 2
>     + list 3
>   -----
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::\n  \n  \n  \n\n  ]",
        "[ulist(1,5):+::6:  ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:    :      \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[tbreak(5,5):-::-----]",
        "[BLANK(6,2):]",
        "[fcode-block(7,5):`:3:block:::::]",
        "[text(8,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,2):]",
        "[tbreak(11,5):-::-----]",
        "[li(12,3):4::]",
        "[para(12,5):]",
        "[text(12,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(13,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_extra_052n0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_with_previous_inner_block_double_drop_with_thematics
    """

    # Arrange
    source_markdown = """+ + list 1
    > block 2.1
    > block 2.2
  ----
  ```block
  A code block
  ```
  ----
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n  \n  \n]",
        "[ulist(1,3):+::4:  :\n\n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5):    :    > \n    > ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2.1\nblock 2.2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,3):-::----]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,3):-::----]",
        "[para(9,3):]",
        "[text(9,3):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>list 1
<blockquote>
<p>block 2.1
block 2.2</p>
</blockquote>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
another list</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052n1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_with_previous_inner_block_double_drop_with_thematics
    """

    # Arrange
    source_markdown = """+ + list 1
    > block 2.1
    > block 2.2
  ----

  ```block
  A code block
  ```

  ----
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::\n  \n  \n  \n\n  \n  \n]",
        "[ulist(1,3):+::4:  :\n\n  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5):    :    > \n    > ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2.1\nblock 2.2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,3):-::----]",
        "[BLANK(5,1):]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[tbreak(10,3):-::----]",
        "[para(11,3):]",
        "[text(11,3):another list:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>list 1
<blockquote>
<p>block 2.1
block 2.2</p>
</blockquote>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052p0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_list_with_previous_block_triple_drop
    """

    # Arrange
    source_markdown = """+ + > -----
    > > block 1
    > > block 2
  ```block
  A code block
  ```
  -----
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n  \n]",
        "[ulist(1,3):+::4:  :\n\n  ]",
        "[block-quote(1,5):    :    > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,5):    :    > > \n    > > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,3):-::-----]",
        "[para(8,3):]",
        "[text(8,3):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
another list</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052p1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_list_with_previous_block_triple_drop
    """

    # Arrange
    source_markdown = """+ + > -----
    > > block 1
    > > block 2

  ```block
  A code block
  ```

  -----
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n\n  \n  \n]",
        "[ulist(1,3):+::4:  :\n\n]",
        "[block-quote(1,5):    :    > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,5):    :    > > \n    > > \n]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[tbreak(9,3):-::-----]",
        "[para(10,3):]",
        "[text(10,3):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052q0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_list_with_previous_block_triple_drop_and_thematics
    """

    # Arrange
    source_markdown = """+ + > -----
    > > block 1
    > > block 2
  ```block
  A code block
  ```
  -----
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n  \n]",
        "[ulist(1,3):+::4:  :\n\n  ]",
        "[block-quote(1,5):    :    > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,5):    :    > > \n    > > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,3):-::-----]",
        "[para(8,3):]",
        "[text(8,3):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
another list</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052r0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """+ + > -----
    > + list 1
    >   list 2
    > + list 3
  ```block
  A code block
  ```
  -----
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n  \n]",
        "[ulist(1,3):+::4:  :  ]",
        "[block-quote(1,5):    :    > \n    > \n    > \n    > ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,3):-::-----]",
        "[para(9,3):]",
        "[text(9,3):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
another list</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_extra_052r1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """+ + > -----
    > + list 1
    >   list 2
    > + list 3

  ```block
  A code block
  ```

  -----
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n\n  \n  \n]",
        "[ulist(1,3):+::4:  :]",
        "[block-quote(1,5):    :    > \n    > \n    > \n    > ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[tbreak(10,3):-::-----]",
        "[para(11,3):]",
        "[text(11,3):another list:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052s0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list_double_drop_and_thematics
    """

    # Arrange
    source_markdown = """+ + > -----
    > + list 1
    >   list 2
    > + list 3
    -----
    ```block
    A code block
    ```
    -----
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :    \n    \n    \n    \n    \n]",
        "[block-quote(1,5):    :    > \n    > \n    > \n    > ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[tbreak(5,5):-::-----]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,5):-::-----]",
        "[li(10,3):4:  :]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052s1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list_double_drop_and_thematics
    """

    # Arrange
    source_markdown = """+ + > -----
    > + list 1
    >   list 2
    > + list 3
    -----

    ```block
    A code block
    ```

    -----
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :    \n\n    \n    \n    \n\n    \n]",
        "[block-quote(1,5):    :    > \n    > \n    > \n    > ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[tbreak(5,5):-::-----]",
        "[BLANK(6,1):]",
        "[fcode-block(7,5):`:3:block:::::]",
        "[text(8,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,1):]",
        "[tbreak(11,5):-::-----]",
        "[li(12,3):4:  :]",
        "[para(12,5):]",
        "[text(12,5):another list:]",
        "[end-para:::True]",
        "[BLANK(13,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052t0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list_triple_drop_and_thematics
    """

    # Arrange
    source_markdown = """+ + > -----
    > + list 1
    >   list 2
    > + list 3
  -----
  ```block
  A code block
  ```
  -----
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n  \n  \n]",
        "[ulist(1,3):+::4:  :  ]",
        "[block-quote(1,5):    :    > \n    > \n    > \n    > ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8::  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8::]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[tbreak(5,3):-::-----]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,3):-::-----]",
        "[para(10,3):]",
        "[text(10,3):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</blockquote>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
another list</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)
    # assert False


@pytest.mark.gfm
def test_extra_052u0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_list_with_previous_block_triple_drop
    """

    # Arrange
    source_markdown = """+ + + -----
      > block 1
      > block 2
  ```block
  A code block
  ```
  -----
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n  \n]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    :\n\n  ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7):      :      > \n      > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,3):-::-----]",
        "[para(8,3):]",
        "[text(8,3):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
another list</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)
    # assert False


@pytest.mark.gfm
def test_extra_052u1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_list_with_previous_block_triple_drop
    """

    # Arrange
    source_markdown = """+ + + -----
      > block 1
      > block 2

  ```block
  A code block
  ```

  -----
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n\n  \n  \n]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7):      :      > \n      > \n]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[tbreak(9,3):-::-----]",
        "[para(10,3):]",
        "[text(10,3):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
<p>another list</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052v0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_list_with_previous_block_double_drop_with_thematics
    """

    # Arrange
    source_markdown = """+ + + -----
      > block 1
      > block 2
    -----
    ```block
    A code block
    ```
    -----
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :    \n    \n    \n    \n]",
        "[ulist(1,5):+::6:    :\n\n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7):      :      > \n      > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::-----]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::-----]",
        "[li(9,3):4:  :]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052v1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_list_with_previous_block_double_drop_with_thematics
    """

    # Arrange
    source_markdown = """+ + + -----
      > block 1
      > block 2
    -----

    ```block
    A code block
    ```

    -----
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :\n    \n    \n    \n\n    \n]",
        "[ulist(1,5):+::6:    :\n\n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7):      :      > \n      > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::-----]",
        "[BLANK(5,1):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[tbreak(10,5):-::-----]",
        "[li(11,3):4:  :]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052w0() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_list_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """+ + + -----
      + list 1
        list 2
      + list 3
  ```block
  A code block
  ```
  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n  \n]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:      :        ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:      :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[para(8,3):]",
        "[text(8,3):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
another list</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_052w1() -> None:
    """
    TBD
    bad_fenced_block_in_list_in_list_in_list_with_previous_list_triple_drop
    """

    # Arrange
    source_markdown = """+ + + -----
      + list 1
        list 2
      + list 3

  ```block
  A code block
  ```

  another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n\n  \n]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:      :        \n]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:      :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,1):]",
        "[para(10,3):]",
        "[text(10,3):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<p>another list</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_053a0() -> None:
    """
    TBD
    issue-1302
    """

    # Arrange
    source_markdown = """## Intro to C\\#

Emits MD020 warning.
"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):Intro to C\\\b#: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):Emits MD020 warning.:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<h2>Intro to C#</h2>
<p>Emits MD020 warning.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_053a1() -> None:
    """
    TBD
    issue-1302
    """

    # Arrange
    source_markdown = """## Intro to C&#35;

Emits MD020 warning.
"""
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):Intro to C\a&#35;\a#\a: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):Emits MD020 warning.:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<h2>Intro to C#</h2>
<p>Emits MD020 warning.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_053b0() -> None:
    """
    TBD
    issue-1326
    """

    # Arrange
    source_markdown = """# z

z




<div class="grid cards" markdown>

-   z

-   z


-   z
</div>
"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):z: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):z:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
        "[BLANK(7,1):]",
        "[html-block(8,1)]",
        '[text(8,1):<div class="grid cards" markdown>:]',
        "[end-html-block:::False]",
        "[BLANK(9,1):]",
        "[ulist(10,1):-::4::\n\n]",
        "[para(10,5):]",
        "[text(10,5):z:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[li(12,1):4::]",
        "[para(12,5):]",
        "[text(12,5):z:]",
        "[end-para:::True]",
        "[BLANK(13,1):]",
        "[BLANK(14,1):]",
        "[li(15,1):4::]",
        "[para(15,5):]",
        "[text(15,5):z:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[html-block(16,1)]",
        "[text(16,1):</div>:]",
        "[end-html-block:::False]",
        "[BLANK(17,1):]",
    ]
    expected_gfm = """<h1>z</h1>
<p>z</p>
<div class="grid cards" markdown>
<ul>
<li>
<p>z</p>
</li>
<li>
<p>z</p>
</li>
<li>
<p>z</p>
</li>
</ul>
</div>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_053c0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blockx_double_drop
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   ```block
>   A code block
>   ```
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::\n\n  þ\n  \n  \n  ]",
        "[block-quote(1,5)::> \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,5):-::-----]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_extra_053c1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blockx_double_drop
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::\n\n\n  \n  \n  \n\n  ]",
        "[block-quote(1,5)::> \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,4):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[tbreak(9,5):-::-----]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_053d0() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_double_drop_with_thematics
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   -----
>   ```block
>   A code block
>   ```
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::\n\n  þ\n  \n  \n  \n  ]",
        "[block-quote(1,5)::> \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-block-quote:::True]",
        "[tbreak(4,5):-::-----]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::-----]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_053d1() -> None:
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_double_drop_with_thematics
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   -----
>
>   ```block
>   A code block
>   ```
>
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::\n\n  þ\n\n  \n  \n  \n\n  ]",
        "[block-quote(1,5)::> \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-block-quote:::True]",
        "[tbreak(4,5):-::-----]",
        "[BLANK(5,2):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,4):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,5):-::-----]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(12,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
<li>
<p>another list</p>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_054x() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item

    test_tables_extension_extra_in_block_quote_header_line_only
    """

    # Arrange
    source_markdown = """> [abc]: /url 'abc
>
> some text [abc]
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n]",
        "[para(1,3):]",
        "[text(1,3):[abc]: /url 'abc:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[para(3,3):]",
        "[text(3,3):some text [abc]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<p>[abc]: /url 'abc</p>
<p>some text [abc]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_055x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """This is text and a blank line.

+ a list
[blah]: /url
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):This is text and a blank line.:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[ulist(3,1):+::2::\n]",
        "[para(3,3):\n]",
        "[text(3,3):a list\n[blah]: /url::\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<p>This is text and a blank line.</p>
<ul>
<li>a list
[blah]: /url</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_056x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> this is a block quote
<!-- pyml disable-next-line blanks-around-lists -->
+ a list
+ still a list
<!-- pyml disable-next-line blanks-around-lists -->
+ still still a list
> this is a block quote
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):this is a block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(3,1):+::2:]",
        "[para(3,3):]",
        "[text(3,3):a list:]",
        "[end-para:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):still a list:]",
        "[end-para:::True]",
        "[li(6,1):2::]",
        "[para(6,3):]",
        "[text(6,3):still still a list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(7,1)::> \n]",
        "[para(7,3):]",
        "[text(7,3):this is a block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[pragma:2:<!-- pyml disable-next-line blanks-around-lists -->;5:<!-- pyml disable-next-line blanks-around-lists -->]",
    ]
    expected_gfm = """<blockquote>
<p>this is a block quote</p>
</blockquote>
<ul>
<li>a list</li>
<li>still a list</li>
<li>still still a list</li>
</ul>
<blockquote>
<p>this is a block quote</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_056a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> this is a block quote
<!-- pyml disable-next-line blanks-around-lists -->

+ a list
+ still a list
<!-- pyml disable-next-line blanks-around-lists -->

+ still still a list
> this is a block quote
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):]",
        "[text(1,3):this is a block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[ulist(4,1):+::2::]",
        "[para(4,3):]",
        "[text(4,3):a list:]",
        "[end-para:::True]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):still a list:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[li(8,1):2::]",
        "[para(8,3):]",
        "[text(8,3):still still a list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(9,1)::> \n]",
        "[para(9,3):]",
        "[text(9,3):this is a block quote:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
        "[pragma:2:<!-- pyml disable-next-line blanks-around-lists -->;6:<!-- pyml disable-next-line blanks-around-lists -->]",
    ]
    expected_gfm = """<blockquote>
<p>this is a block quote</p>
</blockquote>
<ul>
<li>
<p>a list</p>
</li>
<li>
<p>still a list</p>
</li>
<li>
<p>still still a list</p>
</li>
</ul>
<blockquote>
<p>this is a block quote</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_057xx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """This is a paragraph with an image embedded
<!-- pyml disable-next-line no-inline-html -->
in something other <img src="fred"> than the first line.
"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):This is a paragraph with an image embedded\nin something other ::\n]",
        '[raw-html(3,20):img src="fred"]',
        "[text(3,36): than the first line.:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[pragma:2:<!-- pyml disable-next-line no-inline-html -->]",
    ]
    expected_gfm = """<p>This is a paragraph with an image embedded
in something other <img src="fred"> than the first line.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_057xa() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """This is a paragraph with an image embedded
<!-- pyml disable-next-line no-inline-html -->
in something other <img
<!-- pyml disable-next-line no-inline-html -->
src="fred"> than the first line.
"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):This is a paragraph with an image embedded\nin something other ::\n]",
        '[raw-html(3,20):img\nsrc="fred"]',
        "[text(5,12): than the first line.:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[pragma:2:<!-- pyml disable-next-line no-inline-html -->;4:<!-- pyml disable-next-line no-inline-html -->]",
    ]
    expected_gfm = """<p>This is a paragraph with an image embedded
in something other <img
src="fred"> than the first line.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_057a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """This is a paragraph with a code span
<!-- pyml disable-next-line no-inline-html -->
in something other `than the` than the first line.
"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):This is a paragraph with a code span\nin something other ::\n]",
        "[icode-span(3,20):than the:`::]",
        "[text(3,30): than the first line.:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[pragma:2:<!-- pyml disable-next-line no-inline-html -->]",
    ]
    expected_gfm = """<p>This is a paragraph with a code span
in something other <code>than the</code> than the first line.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_057b() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """```shell
<!-- pyml disable-next-line commands-show-output -->
$ ls /my/dir
$ cat /my/dir/file
```
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:shell:::::]",
        "[text(3,1):$ ls /my/dir\n$ cat /my/dir/file:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
        "[pragma:2:<!-- pyml disable-next-line commands-show-output -->]",
    ]
    expected_gfm = """<pre><code class="language-shell">$ ls /my/dir
$ cat /my/dir/file
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_057c() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """This is a paragraph with emphasis
<!-- pyml disable-next-line no-inline-html -->
in something other *than the* than the first line.
"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):This is a paragraph with emphasis\nin something other ::\n]",
        "[emphasis(3,20):1:*]",
        "[text(3,21):than the:]",
        "[end-emphasis(3,29)::]",
        "[text(3,30): than the first line.:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[pragma:2:<!-- pyml disable-next-line no-inline-html -->]",
    ]
    expected_gfm = """<p>This is a paragraph with emphasis
in something other <em>than the</em> than the first line.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_057d() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """This is a paragraph with emphasis
<!-- pyml disable-next-line no-inline-html -->
in something other *than
<!-- pyml disable-next-line no-inline-html -->
the* than the first line.
"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):This is a paragraph with emphasis\nin something other ::\n]",
        "[emphasis(3,20):1:*]",
        "[text(3,21):than\nthe::\n]",
        "[end-emphasis(5,4)::]",
        "[text(5,5): than the first line.:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[pragma:2:<!-- pyml disable-next-line no-inline-html -->;4:<!-- pyml disable-next-line no-inline-html -->]",
    ]
    expected_gfm = """<p>This is a paragraph with emphasis
in something other <em>than
the</em> than the first line.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_057e() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """This is a paragraph with link
<!-- pyml disable-next-line no-inline-html -->
in something other [than the](/url) than the first line.
"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):This is a paragraph with link\nin something other ::\n]",
        "[link(3,20):inline:/url:::::than the:False::::]",
        "[text(3,21):than the:]",
        "[end-link::]",
        "[text(3,36): than the first line.:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[pragma:2:<!-- pyml disable-next-line no-inline-html -->]",
    ]
    expected_gfm = """<p>This is a paragraph with link
in something other <a href="/url">than the</a> than the first line.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_057f() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """This is a paragraph with link
<!-- pyml disable-next-line no-inline-html -->
in something other [than
<!-- pyml disable-next-line no-inline-html -->
the](/url) than the first line.
"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):This is a paragraph with link\nin something other ::\n]",
        "[link(3,20):inline:/url:::::than\nthe:False::::]",
        "[text(3,21):than\nthe::\n]",
        "[end-link::]",
        "[text(5,11): than the first line.:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[pragma:2:<!-- pyml disable-next-line no-inline-html -->;4:<!-- pyml disable-next-line no-inline-html -->]",
    ]
    expected_gfm = """<p>This is a paragraph with link
in something other <a href="/url">than
the</a> than the first line.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_057g() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """This is a paragraph with link
<!-- pyml disable-next-line no-inline-html -->
in something other [than the](/url "my
<!-- pyml disable-next-line no-inline-html -->
title") than the first line.
"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):This is a paragraph with link\nin something other ::\n]",
        '[link(3,20):inline:/url:my\ntitle::::than the:False:":: :]',
        "[text(3,21):than the:]",
        "[end-link::]",
        "[text(5,8): than the first line.:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[pragma:2:<!-- pyml disable-next-line no-inline-html -->;4:<!-- pyml disable-next-line no-inline-html -->]",
    ]
    expected_gfm = """<p>This is a paragraph with link
in something other <a href="/url" title="my
title">than the</a> than the first line.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_057h() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """```shell
<!-- pyml disable-next-line commands-show-output -->
$ ls /my/dir
$ cat /my/dir/file
```
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:shell:::::]",
        "[text(3,1):$ ls /my/dir\n$ cat /my/dir/file:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
        "[pragma:2:<!-- pyml disable-next-line commands-show-output -->]",
    ]
    expected_gfm = """<pre><code class="language-shell">$ ls /my/dir
$ cat /my/dir/file
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_058x() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. still still a list
[lrd]: /url
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[para(1,4):\n]",
        "[text(1,4):still still a list\n[lrd]: /url::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>still still a list
[lrd]: /url</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_058a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """[lrd]: /url
1. still still a list
[lrd]: /url
"""
    expected_tokens = [
        "[link-ref-def(1,1):True::lrd:: :/url:::::]",
        "[olist(2,1):.:1:3::\n]",
        "[para(2,4):\n]",
        "[text(2,4):still still a list\n::\n]",
        "[link(3,1):shortcut:/url:::::lrd:False::::]",
        "[text(3,2):lrd:]",
        "[end-link::]",
        "[text(3,6):: /url:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>still still a list
<a href="/url">lrd</a>: /url</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_058b() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
1. still still a list
"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1):::True:| --- | --- |]",
        "[table-header-item(1,3): :]",
        "[text(1,3):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,9): :]",
        "[text(1,9):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[end-table:::False]",
        "[olist(3,1):.:1:3::]",
        "[para(3,4):]",
        "[text(3,4):still still a list:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
</table>
<ol>
<li>still still a list</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=tables_config_map
    )


@pytest.mark.gfm
def test_extra_058cx() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
1. still still a list
| abc | def |
| --- | --- |
"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1):::True:| --- | --- |]",
        "[table-header-item(1,3): :]",
        "[text(1,3):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,9): :]",
        "[text(1,9):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[end-table:::False]",
        "[olist(3,1):.:1:3::\n\n]",
        "[para(3,4):\n\n]",
        "[text(3,4):still still a list\n| abc | def |\n| --- | --- |::\n\n]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
</table>
<ol>
<li>still still a list
| abc | def |
| --- | --- |</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=tables_config_map
    )


@pytest.mark.gfm
def test_extra_058ca() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """  |  abc | def |\a
 |  --- | :---: |\a
  |  abc  | def |\a
1. still still a list

| abc | def |
| --- | --- |
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[table(1,3)]",
        "[table-header(1,3):  : :True: |  --- | :---: | ]",
        "[table-header-item(1,6):  :]",
        "[text(1,6):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,12): :center]",
        "[text(1,12):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,1)]",
        "[table-row(3,3):  : :True:0]",
        "[table-row-item(3,4):  :]",
        "[text(3,4):abc:]",
        "[end-table-row-item:  |::False]",
        "[table-row-item(3,11): :center]",
        "[text(3,11):def:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[olist(4,1):.:1:3::]",
        "[para(4,4):]",
        "[text(4,4):still still a list:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[table(6,1)]",
        "[table-header(6,1):::True:| --- | --- |]",
        "[table-header-item(6,3): :]",
        "[text(6,3):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(6,9): :]",
        "[text(6,9):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[end-table:::False]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th align="center">def</th>
</tr>
</thead>
<tbody>
<tr>
<td>abc</td>
<td align="center">def</td>
</tr>
</tbody>
</table>
<ol>
<li>still still a list</li>
</ol><table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=tables_config_map
    )


@pytest.mark.gfm
def test_extra_058d() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. a list
1. still a list
   <script>
<!-- pyml disable-next-line blanks-around-lists -->

   </script>
<script>
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n\n   ]",
        "[para(1,4):]",
        "[text(1,4):a list:]",
        "[end-para:::True]",
        "[li(2,1):3::1]",
        "[para(2,4):]",
        "[text(2,4):still a list:]",
        "[end-para:::False]",
        "[html-block(3,4)]",
        "[text(3,4):<script>:]",
        "[BLANK(5,1):]",
        "[text(6,4):</script>:]",
        "[end-html-block:::False]",
        "[end-olist:::True]",
        "[html-block(7,1)]",
        "[text(7,1):<script>\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(9,1):]",
        "[pragma:4:<!-- pyml disable-next-line blanks-around-lists -->]",
    ]
    expected_gfm = """<ol>
<li>a list</li>
<li>still a list
<script>

</script>
</li>
</ol>
<script>
</script>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=tables_config_map
    )


@pytest.mark.gfm
def test_extra_058e() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """<!-- pyml disable-next-line proper-names -->

[lrd with a paragraph]: http://www.google.com "a
<!-- pyml disable-next-line proper-names -->

paragraph"
LRD.
"""
    expected_tokens = [
        "[BLANK(2,1):]",
        "[para(3,1):]",
        '[text(3,1):[lrd with a paragraph]: http://www.google.com \a"\a&quot;\aa:]',
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[para(6,1):\n]",
        '[text(6,1):paragraph\a"\a&quot;\a\nLRD.::\n]',
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[pragma:1:<!-- pyml disable-next-line proper-names -->;4:<!-- pyml disable-next-line proper-names -->]",
    ]
    expected_gfm = """<p>[lrd with a paragraph]: http://www.google.com &quot;a</p>
<p>paragraph&quot;
LRD.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=tables_config_map
    )


@pytest.mark.gfm
def test_extra_058f() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """<!-- pyml disable-next-line proper-names -->

[lrd with a paragraph]: http://www.google.com "a
<!-- pyml disable-next-line line-length -->
<!-- pyml disable-next-line proper-names -->

paragraph"
LRD.
"""
    expected_tokens = [
        "[BLANK(2,1):]",
        "[para(3,1):]",
        '[text(3,1):[lrd with a paragraph]: http://www.google.com \a"\a&quot;\aa:]',
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[para(7,1):\n]",
        '[text(7,1):paragraph\a"\a&quot;\a\nLRD.::\n]',
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[pragma:1:<!-- pyml disable-next-line proper-names -->;4:<!-- pyml disable-next-line line-length -->;5:<!-- pyml disable-next-line proper-names -->]",
    ]
    expected_gfm = """<p>[lrd with a paragraph]: http://www.google.com &quot;a</p>
<p>paragraph&quot;
LRD.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=tables_config_map
    )


@pytest.mark.gfm
def test_extra_058g() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """<!-- pyml disable-next-line proper-names -->

[lrd with a paragraph]: http://www.google.com "a
<!-- pyml disable-next-line line-length -->
<!-- pyml disable-next-line proper-names -->
" xx
paragraph"
LRD.
"""
    expected_tokens = [
        "[BLANK(2,1):]",
        "[para(3,1):\n\n\n]",
        '[text(3,1):[lrd with a paragraph]: http://www.google.com \a"\a&quot;\aa\n\a"\a&quot;\a xx\nparagraph\a"\a&quot;\a\nLRD.::\n\n\n]',
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[pragma:1:<!-- pyml disable-next-line proper-names -->;4:<!-- pyml disable-next-line line-length -->;5:<!-- pyml disable-next-line proper-names -->]",
    ]
    expected_gfm = """<p>[lrd with a paragraph]: http://www.google.com &quot;a
&quot; xx
paragraph&quot;
LRD.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=tables_config_map
    )


@pytest.mark.gfm
def test_extra_058h() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """<!-- pyml disable-next-line proper-names -->

[lrd with a paragraph]: http://www.google.com "a
<!-- pyml disable-next-line line-length -->
abc
<!-- pyml disable-next-line proper-names -->
" xx
paragraph"
LRD.
"""
    expected_tokens = [
        "[BLANK(2,1):]",
        "[para(3,1):\n\n\n\n]",
        '[text(3,1):[lrd with a paragraph]: http://www.google.com \a"\a&quot;\aa\nabc\n\a"\a&quot;\a xx\nparagraph\a"\a&quot;\a\nLRD.::\n\n\n\n]',
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[pragma:1:<!-- pyml disable-next-line proper-names -->;4:<!-- pyml disable-next-line line-length -->;6:<!-- pyml disable-next-line proper-names -->]",
    ]
    expected_gfm = """<p>[lrd with a paragraph]: http://www.google.com &quot;a
abc
&quot; xx
paragraph&quot;
LRD.</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=tables_config_map
    )


@pytest.mark.gfm
def test_extra_999() -> None:
    """
    Temporary test to keep coverage up while consistency checks disabled.
    """

    new_position = PositionMarker(1, 0, "text")

    new_block_quote = BlockQuoteMarkdownToken("", new_position)
    ex_ws = new_block_quote.extracted_whitespace
    assert not ex_ws

    new_front_matter = FrontMatterMarkdownToken("--", "--", ["a: b"], {}, new_position)
    new_value = new_front_matter.calculate_block_token_height(new_front_matter)
    assert new_value != 999
    new_value, _ = new_front_matter.calculate_initial_whitespace()
    assert new_value != 999
    assert new_front_matter.is_extension

    ParserHelper.count_newlines_in_texts("text")


# FOOBAR1 bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_triple_drop_and_thematics
# Expected:> > + ______\n> >   + list 1\n> >     list 2\n> >   + list 3\n> ______\n>\n> ```block\n> A code block\n> ```\n>\n> ______\n:
#   Actual:> > + ______\n> >   + list 1\n> >     list 2\n> >   + list 3\n> ______\n> \n>```block\n> A code block\n> ```\n> \n>______\n:
# -> bq and list

# FOOBAR3 bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_double_drop_with_thematics
# Expected:1. > > ----\n   > > + list 1\n   > >   list 2\n   > > + list 3\n   > ----\n   >\n   > ```block\n   > A code block\n   > ```\n   >\n   > ----\n:
#   Actual:1. > > ----\n   > > + list 1\n   > >   list 2\n   > > + list 3\n   > ----\n   > \n   >```block\n   > A code block\n   > ```\n   > \n   >----\n:

# FOOBAR4 bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_triple_drop_with_thematics
# Expected:1. > > ----\n   > > + list 1\n   > >   list 2\n   > > + list 3\n   ----\n\n   ```block\n   A code block\n   ```\n\n   ----\n:
#   Actual:1. > > ----\n   > > + list 1\n   > >   list 2\n   > > + list 3\n   ----\n   \n```block\n   A code block\n   ```\n   \n----\n:

# FOOBAR5
# bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_list_double_drop_and_thematics
# Expected:> + > -----\n>   > + list 1\n>   >   list 2\n>   > + list 3\n>   -----\n>\n>   ```block\n>   A code block\n>   ```\n>\n>   -----\n> + another list\n:
#   Actual:> + > -----\n>   > + list 1\n>   >   list 2\n>   > + list 3\n>   -----\n> \n>  ```block\n>   A code block\n>   ```\n> \n>  -----\n> + another list\n:

# FOOBAR6
# bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_double_drop_with_thematics
# Expected:> + + -----\n>     > block 1\n>     > block 2\n>   -----\n>\n>   ```block\n>   A code block\n>   ```\n>\n>   -----\n> + another list\n:
#   Actual:> + + -----\n>     > block 1\n>     > block 2\n>   -----\n> \n>```block\n> A code block\n> ```\n>\n> -----\n> + another list\n:

# FOOBAR7
# bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_triple_drop_with_thematics
# Expected:> + + -----\n>     > block 1\n>     > block 2\n> -----\n>\n> ```block\n> A code block\n> ```\n>\n> -----\n> another list\n:
#   Actual:> + + -----\n>     > block 1\n>     > block 2\n> -----\n> \n>```block\n> A code block\n> ```\n> \n>-----\n> another list\n:

# FOOBAR8
# bad_fenced_block_in_list_in_list_with_previous_inner_block_double_drop
# Expected:+ + list 1\n    > block 2.1\n    > block 2.2\n\n  ```block\n  A code block\n  ```\n\n  another list\n:
#   Actual:+ + list 1\n    > block 2.1\n    > block 2.2\n\n  ```block\n  A code block\n```\n  \nanother list\n:

# FOOBAR9
# bad_fenced_block_in_block_quote_in_list_in_list_with_previous_list_double_drop_and_thematics
# Expected:+ + > -----\n    > + list 1\n    >   list 2\n    > + list 3\n    -----\n\n    ```block\n    A code block\n    ```\n\n    -----\n  + another list\n:
#   Actual:+ + > -----\n    > + list 1\n    >   list 2\n    > + list 3\n    -----\n    \n```block\n    A code block\n    ```\n    \n-----\n  + another list\n:

# FOOBAR10
# bad_fenced_block_in_list_in_list_in_list_with_previous_block_double_drop
# Expected:+ + + -----\n      > block 1\n      > block 2\n\n    ```block\n    A code block\n    ```\n\n    -----\n  + another list\n:
#   Actual:+ + + -----\n      > block 1\n      > block 2\n\n    ```block\n    A code block\n```\n    \n-----\n  + another list\n:

# FOOBAR11
# bad_fenced_block_in_list_in_list_in_list_with_previous_block_triple_drop
# Expected:+ + + -----\n      > block 1\n      > block 2\n\n  ```block\n  A code block\n  ```\n\n  -----\n  another list\n:
#   Actual:+ + + -----\n      > block 1\n      > block 2\n\n  ```block\n  A code block\n```\n  \n  -----\nanother list\n:

# FOOBAR12
# bad_fenced_block_in_list_in_list_in_list_with_previous_list_double_drop
# Expected:+ + + -----\n      + list 1\n        list 2\n      + list 3\n\n    ```block\n    A code block\n    ```\n\n  + another list\n:
#   Actual:+ + + -----\n      + list 1\n        list 2\n      + list 3\n\n    ```block\n    A code block\n```\n    \n  + another list\n:

# FOOBAR13
# bad_fenced_block_in_list_in_list_in_list_with_previous_list_triple_drop
# Expected:+ + + -----\n      + list 1\n        list 2\n      + list 3\n\n  ```block\n  A code block\n  ```\n\n  another list\n:
#   Actual:+ + + -----\n      + list 1\n        list 2\n      + list 3\n\n  ```block\n  A code block\n```\n  \n  another list\n:

# FOOBAR14
# # bad_fenced_block_in_block_quote_in_list_with_previous_inner_list_double_drop
# Expected:1. > +\n   >   list 3\n   > + list 3\n\n   ```block\n   A code block\n   ```\n\n   --------\n:
#   Actual:1. > +\n   >   list 3\n   > + list 3\n   \n   ```block\nA code block\n   ```\n   \n--------\n:

# SNAFU2
# bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blockx_double_drop
#   File "c:\enlistments\pymarkdown\pymarkdown\block_quotes\block_quote_processor.py", line 698, in __handle_existing_block_quote_fenced_special_part_two
#     assert sd == ">"
#            ^^^^^^^^^
# AssertionError

# SNAFU9
# bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block_double_drop
#   File "c:\enlistments\pymarkdown\pymarkdown\transform_markdown\transform_list_block.py", line 773, in __rehydrate_list_start_deep
#     block_quote_leading_space = split_leading_spaces[line_number_delta]
