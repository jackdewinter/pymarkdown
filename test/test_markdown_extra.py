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


@pytest.mark.gfm
def test_extra_001():
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
def test_extra_002():
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
def test_extra_003():
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
def test_extra_004():
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
def test_extra_005():
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
def test_extra_006():
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
        "[olist(5,3):.:1:5::]",
        "[para(5,6):]",
        "[text(5,6):another list:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_007a():
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
def test_extra_007b():
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
def test_extra_007cx():
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
def test_extra_007ca():
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
def test_extra_007d():
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
def test_extra_007e():
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
def test_extra_008x():
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
        "[ulist(3,7):*::8:    :]",
        "[para(3,9):]",
        "[text(3,9):this is level 3:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_008a():
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
def test_extra_009x():
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
def test_extra_009a():
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
def test_extra_009b():
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
def test_extra_009c():
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
def test_extra_010x():
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
def test_extra_010a():
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
def test_extra_010b():
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
def test_extra_011x():
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
def test_extra_011a():
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
def test_extra_011b():
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
def test_extra_012():
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
def test_extra_013x():
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
def test_extra_013a():
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
def test_extra_014x():
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
        "[olist(1,3):.:1:5::   \n   \n\n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[tbreak(3,6):*::*****]",
        "[li(4,3):5::1]",
        "[para(4,6):]",
        "[text(4,6):that:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_014a():
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
        "[olist(1,3):.:1:5::   \n   \n\n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[tbreak(3,7):*: :*****]",
        "[li(4,3):5::1]",
        "[para(4,6):]",
        "[text(4,6):that:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_014bx():
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
        "[olist(1,3):.:1:5::   \n   \n   \n\n]",
        "[tbreak(1,6):*::*****]",
        "[para(2,6):\n]",
        "[text(2,6):list\nthis::\n]",
        "[end-para:::False]",
        "[tbreak(4,6):*::*****]",
        "[li(5,3):5::1]",
        "[para(5,6):]",
        "[text(5,6):that:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_014ba():
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
def test_extra_014bb():
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
def test_extra_015():
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
        "[olist(1,3):.:1:5::   \n   \n\n]",
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
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_015a():
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
        "[olist(1,3):.:1:5::   \n   \n\n]",
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
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_016():
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
        "[olist(1,3):.:1:5::   \n\n   \n   \n]",
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
        "[BLANK(7,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_016a():
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
        "[olist(1,3):.:1:5::   \n\n   \n   \n\n]",
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
        "[BLANK(7,1):]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_017():
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
        "[olist(1,3):.:1:5::   \n\n   \n   \n]",
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
        "[BLANK(7,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_018x():
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
        "[olist(1,3):.:1:5::   \n   \n   \n   \n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[fcode-block(3,6):`:3:html:::::]",
        "[text(4,4):\a<\a&lt;\ahtml\a>\a&gt;\a:]",
        "[end-fcode-block:::3:False]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_018a():
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
        "[olist(1,3):.:1:5::   \n   \n   \n   \n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[fcode-block(3,7):`:3:html:::: :]",
        "[text(4,4):\a<\a&lt;\ahtml\a>\a&gt;\a:]",
        "[end-fcode-block:::3:False]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_018b():
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
        "[olist(1,3):.:1:5::   \n   \n   \n   \n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[fcode-block(3,6):`:3:html:::::]",
        "[text(4,4):\a<\a&lt;\ahtml\a>\a&gt;\a: ]",
        "[end-fcode-block:::3:False]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_018c():
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
        "[olist(1,3):.:1:5::   \n   \n   \n   \n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::False]",
        "[fcode-block(3,6):`:3:html:::::]",
        "[text(4,4):\a<\a&lt;\ahtml\a>\a&gt;\a:]",
        "[end-fcode-block: ::3:False]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_019x():
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
        "[olist(1,3):.:1:5::   \n   \n]",
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
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_019a():
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
        "[olist(1,3):.:1:5::   \n   \n]",
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
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_019b():
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
        "[olist(1,3):.:1:5::   \n   \n   \n]",
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
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_020x():
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
        "[olist(1,3):.:1:5::   \n\n   \n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[link-ref-def(4,6):True::abc:: :/url:::::]",
        "[li(5,3):5::1]",
        "[para(5,6):]",
        "[text(5,6):that:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_020a():
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
        "[olist(1,3):.:1:5::   \n\n   \n   \n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[link-ref-def(4,6):True::abc::\n :/url:::::]",
        "[li(6,3):5::1]",
        "[para(6,6):]",
        "[text(6,6):that:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_020b():
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
        "[olist(1,3):.:1:5::   \n\n   \n   \n   \n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        '[link-ref-def(4,6):True::abc::\n :/url::\n  :title:"title":]',
        "[li(7,3):5::1]",
        "[para(7,6):]",
        "[text(7,6):that:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_020c():
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
        "[olist(1,3):.:1:5::   \n\n   \n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[BLANK(3,3):\x0c]",
        "[link-ref-def(4,6):True::abc:: :/url:::::]",
        "[li(5,3):5::1]",
        "[para(5,6):]",
        "[text(5,6):that:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_020d():
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
        "[olist(1,3):.:1:5::   \n\n   \n]",
        "[para(1,6):\n\n\n]",
        "[text(1,6):list\nthis\n\u00a0\n[abc]: /url::\n\n\n]",
        "[end-para:::True]",
        "[li(5,3):5::1]",
        "[para(5,6):]",
        "[text(5,6):that:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_021x():
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
def test_extra_021a():
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
def test_extra_021b():
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
        "[ulist(1,4):+::5: :   \n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_021c():
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
        "[ulist(5,8):*::9:     :]",
        "[para(5,10):]",
        "[text(5,10):this is level 3:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_022():
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
def test_extra_023xx():
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
def test_extra_023xa():
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
def test_extra_023xb():
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
def test_extra_023xc():
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
def test_extra_023ax():
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
def test_extra_023aa():
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
def test_extra_023ab():
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
def test_extra_024x():
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
        "[ulist(5,6):*::7:   :]",
        "[para(5,8):]",
        "[text(5,8):Item 2a:]",
        "[end-para:::True]",
        "[li(6,6):7:   :]",
        "[para(6,8):]",
        "[text(6,8):Item 2b:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_024a():
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
        "[ulist(5,6):*::7:   :]",
        "[para(5,8):]",
        "[text(5,8):Item 2a:]",
        "[end-para:::True]",
        "[li(6,6):7:   :]",
        "[para(6,8):]",
        "[text(6,8):Item 2b:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_025xx():
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
        "[ulist(1,3):+::4::  \n\n\n]",
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
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_025xa():
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
        "[ulist(1,3):+::4::  \n\n\n  \u00fe\n]",
        "[para(1,5):\n]",
        "[text(1,5):list\nthis::\n]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n>   > \n> \n]",
        "[para(3,8): \n\n]",
        "[text(3,8):good\nitem\nthat::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_025ax():
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
        "[ulist(1,3):+::4::  \n\n\n]",
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
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_025aa():
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
        "[ulist(1,3):+::4::  \n\n\n  þ\n]",
        "[para(1,5):\n]",
        "[text(1,5):list\nthis::\n]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n>   > \n> \n]",
        "[para(3,7):\n\n]",
        "[text(3,7):good\nitem\nthat::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_025bx():
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
        "[ulist(1,3):+::4::  \n\n]",
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
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_025ba():
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
        "[ulist(1,3):+::4::  \n\n  þ\n]",
        "[para(1,5):\n]",
        "[text(1,5):list\nthis::\n]",
        "[end-para:::True]",
        "[block-quote(3,5)::> \n> \n]",
        "[para(3,7):\n]",
        "[text(3,7):item\nthat::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_025cxx():
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
        "[ulist(1,3):+::4::\n\n]",
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
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_025cxb():
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
        "[olist(1,3):.:1:5::\n\n]",
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
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_025cxc():
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
        "[olist(1,3):.:1:5::\n]",
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
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_025cxd():
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. list
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[olist(1,3):.:1:5::]",
        "[para(1,6):]",
        "[text(1,6):list:]",
        "[end-para:::True]",
        "[li(2,3):5::1]",
        "[para(2,6):]",
        "[text(2,6):that:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_025cxe():
    """
    TBD
    """

    # Arrange
    source_markdown = """> 1. > list
> 1. that
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[olist(1,3):.:1:5::]",
        "[block-quote(1,6)::> \n> ]",
        "[para(1,8):]",
        "[text(1,8):list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(2,3):5::1]",
        "[para(2,6):]",
        "[text(2,6):that:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
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
<li>that</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_025cxf():
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
        "[olist(1,3):.:1:5::\n]",
        "[block-quote(1,6)::> \n>    > \n> ]",
        "[para(1,8):\n]",
        "[text(1,8):list\nis::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(3,3):5::1]",
        "[para(3,6):]",
        "[text(3,6):that:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_025cxg():
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
        "[ulist(1,3):+::4::\n]",
        "[block-quote(1,5)::> \n>   > \n> ]",
        "[para(1,7):\n]",
        "[text(1,7):list\nis::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_025cxz():
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
def test_extra_025ca():
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
        "[ulist(1,3):+::4::\n\n  þ\n]",
        "[para(1,5):]",
        "[text(1,5):list:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n> \n]",
        "[para(2,7):\n\n]",
        "[text(2,7):good\nitem\nthat::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_026x():
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
def test_extra_026a():
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
def test_extra_026b():
    """
    TBD
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
def test_extra_026cx():
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
def test_extra_026ca():
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
def test_extra_026cb():
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
def test_extra_026cc():
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
def test_extra_026cd():
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
def test_extra_027x():
    """
    TBD
    """

    # Arrange
    source_markdown = """   1.    >    +
   1.    >    + item"""
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
        "[para(2,17):]",
        "[text(2,17):item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
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
<li>item</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_027a():
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
def test_extra_028():
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
def test_extra_028a():
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
def test_extra_029x():
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
def test_extra_029a():
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
def test_extra_029b():
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
def test_extra_029c():
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
def test_extra_029d():
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
def test_extra_029e():
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
def test_extra_029f():
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
def test_extra_029g():
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
def test_extra_029h():
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
def test_extra_030xx():
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
def test_extra_030xa():
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
def test_extra_030ax():
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
def test_extra_030aa():
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
def test_extra_030bx():
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
def test_extra_030ba():
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
def test_extra_031x():
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
def test_extra_032():
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
def test_extra_033x():
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
def test_extra_033a():
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
def test_extra_034d():
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
def test_extra_034e():
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
def test_extra_035x():
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
def test_extra_035a():
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
def test_extra_036():
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
def test_extra_037():
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
def test_extra_038x():
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
def test_extra_038a():
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
def test_extra_038bx():
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
def test_extra_038ba():
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
def test_extra_038bb():
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
def test_extra_038bc():
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
def test_extra_038bd():
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
def test_extra_038be():
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
def test_extra_038cx():
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
def test_extra_038ca():
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
def test_extra_038dx():
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
def test_extra_038da():
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
def test_extra_039x():
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
def test_extra_039a():
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
def test_extra_040x():
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
def test_extra_040a():
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
def test_extra_040b():
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
def test_extra_040c():
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
def test_extra_040d():
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
def test_extra_040e():
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
def test_extra_041x():
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
def test_extra_041a():
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
def test_extra_042b():
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
def test_extra_042c():
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
def test_extra_042d():
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
def test_extra_042x():
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
def test_extra_042xx():
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
def test_extra_042xa():
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
def test_extra_042xb():
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
def test_extra_042xc():
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
def test_extra_043x():
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
def test_extra_043a():
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
def test_extra_044x():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > > block 3
> > > block 3
> > > block 3
> > --------
> > ```block
> > A code block
> > ```
> > --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n]",
        "[block-quote(1,5)::> > > \n> > > \n> > > \n> > ]",
        "[para(1,7):\n\n]",
        "[text(1,7):block 3\nblock 3\nblock 3::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[tbreak(4,5):-::--------]",
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
<p>block 3
block 3
block 3</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044a():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > > block 3
> > > block 3
> > > block 3
> > --------
> >
> > ```block
> > A code block
> > ```
> >
> > --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> >\n> > \n> > \n> > \n> >\n> > \n]",
        "[block-quote(1,5)::> > > \n> > > \n> > > \n> > ]",
        "[para(1,7):\n\n]",
        "[text(1,7):block 3\nblock 3\nblock 3::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[tbreak(4,5):-::--------]",
        "[BLANK(5,4):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,4):]",
        "[tbreak(10,5):-::--------]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>block 3
block 3
block 3</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044b():
    """
    TBD
    """

    # Arrange
    source_markdown = """+ + list 1
+ + + list 2.1
      list 2.2

    ```block
    A code block
    ```

  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,1):2::]",
        "[ulist(2,3):+::4:  :    \n    \n    \n\n]",
        "[ulist(2,5):+::6:    :      \n]",
        "[para(2,7):\n]",
        "[text(2,7):list 2.1\nlist 2.2::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
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
<li>list 1</li>
</ul>
</li>
<li>
<ul>
<li>
<ul>
<li>list 2.1
list 2.2</li>
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044cx():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list 1
>   + list 2
>     list 3
>   ------
>   ```block
>   A code block
>   ```
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :    \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::------]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::------]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<ul>
<li>list 2
list 3</li>
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ca():
    """
    TBD
    BLAH-E
    """

    # Arrange
    source_markdown = """> + list 1
>   + list 2
>     list 3
>   ------
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::\n  \n  \n  \n\n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :    \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::------]",
        "[BLANK(5,2):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,5):-::------]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<ul>
<li>list 2
list 3</li>
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044d():
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
def test_extra_044e():
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
def test_extra_044fxx():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > abc
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::False]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[text(4,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(6,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>abc</p>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044fxa():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > abc
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   >\n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[BLANK(3,6):]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(7,6):]",
        "[tbreak(8,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>abc</p>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044fa():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::]",
        "[block-quote(1,5)::> ]",
        "[tbreak(1,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(2,3):4::]",
        "[para(2,5):]",
        "[text(2,5):another list:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044fb():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > abc
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::\n]",
        "[block-quote(1,5)::> \n>   > \n> ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):another list:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>abc</p>
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044fc():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > ```block
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n]",
        "[block-quote(1,5)::> \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[fcode-block(2,7):`:3:block:::::]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):another list:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block"></code></pre>
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044fd():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > ```block
>   > abc
>   > ```
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > ]",
        "[fcode-block(1,7):`:3:block:::::]",
        "[text(2,7):abc:]",
        "[end-fcode-block:::3:False]",
        "[end-block-quote:::True]",
        "[li(4,3):4::]",
        "[para(4,5):]",
        "[text(4,5):another list:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<pre><code class="language-block">abc
</code></pre>
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044fe():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > ```block
>   > ```
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n]",
        "[block-quote(1,5)::> \n>   > ]",
        "[fcode-block(1,7):`:3:block:::::]",
        "[end-fcode-block:::3:False]",
        "[end-block-quote:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):another list:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<pre><code class="language-block"></code></pre>
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044gx():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > > -----
> > > abc
> > > ```block
> > > A code block
> > > ```
> > > -----
> > another list
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n]",
        "[block-quote(1,5)::> > > \n> > > \n> > > \n> > > \n> > > \n> > > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::False]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[text(4,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(6,7):-::-----]",
        "[end-block-quote:::True]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<hr />
<p>abc</p>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
<p>another list</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ga():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > > -----
> > > abc
> > > 
> > > ```block
> > > A code block
> > > ```
> > > 
> > > -----
> > another list
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n]",
        "[block-quote(1,5)::> > > \n> > > \n> > > \n> > > \n> > > \n> > > \n> > > \n> > > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[BLANK(3,7):]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(7,7):]",
        "[tbreak(8,7):-::-----]",
        "[end-block-quote:::True]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<hr />
<p>abc</p>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
<p>another list</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044h():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   >\n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,6):]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[text(4,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,6):]",
        "[tbreak(7,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044i():
    """
    TBD
    """

    # Arrange
    source_markdown = """1. > > ----
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
1. Another
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > >\n   > > \n   > > \n   > > \n   > >\n   > > ]",
        "[tbreak(1,8):-::----]",
        "[BLANK(2,7):]",
        "[fcode-block(3,8):`:3:block:::::]",
        "[text(4,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,7):]",
        "[tbreak(7,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[li(8,1):3::1]",
        "[para(8,4):]",
        "[text(8,4):Another:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
<li>Another</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044jxx():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > ```block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[fcode-block(2,7):`:3:block:::::]",
        "[end-fcode-block:::3:False]",
        "[tbreak(4,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(5,3):4::]",
        "[para(5,5):]",
        "[text(5,5):another list:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block"></code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044jxa():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   >    
>   > ```block
>   > ```
>   >
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,7):   ]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,6):]",
        "[tbreak(6,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block"></code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044jax():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > ```block
>   > abc
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[fcode-block(2,7):`:3:block:::::]",
        "[text(3,7):abc:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(5,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(6,3):4::]",
        "[para(6,5):]",
        "[text(6,5):another list:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block">abc
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044jaa():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   >
>   > ```block
>   > abc
>   > ```
>   >
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   >\n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,6):]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[text(4,6):abc:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,6):]",
        "[tbreak(7,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block">abc
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044jbx():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > def
>   > ```block
>   > abc
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[text(4,7):abc:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(6,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>def</p>
<pre><code class="language-block">abc
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044jba():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > def
>   >
>   > ```block
>   > abc
>   > ```
>   >
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   >\n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[BLANK(3,6):]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):abc:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(7,6):]",
        "[tbreak(8,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>def</p>
<pre><code class="language-block">abc
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044jcx():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > ```block
>   > abc
>   > ```
>   > def
>   > _____
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[fcode-block(2,7):`:3:block:::::]",
        "[text(3,7):abc:]",
        "[end-fcode-block:::3:False]",
        "[para(5,7):]",
        "[text(5,7):def:]",
        "[end-para:::False]",
        "[tbreak(6,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block">abc
</code></pre>
<p>def</p>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044jca():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   >
>   > ```block
>   > abc
>   > ```
>   >
>   > def
>   > _____
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   >\n>   > \n>   > \n>   > \n>   >\n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,6):]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[text(4,6):abc:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,6):]",
        "[para(7,7):]",
        "[text(7,7):def:]",
        "[end-para:::False]",
        "[tbreak(8,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block">abc
</code></pre>
<p>def</p>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044jd():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > ```block
>   > abc
>   > def
>   > ```
>   > _____
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[fcode-block(2,7):`:3:block:::::]",
        "[text(3,7):abc\ndef:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(6,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<pre><code class="language-block">abc
def
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044jex():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > block
>   > abc
>   > un-block
>   > _____
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):\n\n]",
        "[text(2,7):block\nabc\nun-block::\n\n]",
        "[end-para:::False]",
        "[tbreak(5,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(6,3):4::]",
        "[para(6,5):]",
        "[text(6,5):another list:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
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
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044jea():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > block
>   > abc
>   > un-block
>   > _____
>   > more
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > \n]",
        "[tbreak(1,7):-::-----]",
        "[para(2,7):\n\n]",
        "[text(2,7):block\nabc\nun-block::\n\n]",
        "[end-para:::False]",
        "[tbreak(5,7):_::_____]",
        "[para(6,7):]",
        "[text(6,7):more:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<p>block
abc
un-block</p>
<hr />
<p>more</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044jeb():
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
        "[ulist(1,5):+::6:  :\n\n\n\n\n]",
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
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_044jec():
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
        "[ulist(6,7):+::8::]",
        "[para(6,11):]",
        "[text(6,11):more:]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_044kx():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > 
>   > block
>   > abc
>   > un-block
>   > 
>   > _____
> + more
>   this is more
> + some
>   > more
> + more
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n  \n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,7):]",
        "[para(3,7):\n\n]",
        "[text(3,7):block\nabc\nun-block::\n\n]",
        "[end-para:::True]",
        "[BLANK(6,7):]",
        "[tbreak(7,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(8,3):4::]",
        "[para(8,5):\n]",
        "[text(8,5):more\nthis is more::\n]",
        "[end-para:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):some:]",
        "[end-para:::True]",
        "[block-quote(11,5)::> \n> ]",
        "[para(11,7):]",
        "[text(11,7):more:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(12,3):4::]",
        "[para(12,5):]",
        "[text(12,5):more:]",
        "[end-para:::True]",
        "[BLANK(13,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
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
<li>more
this is more</li>
<li>some
<blockquote>
<p>more</p>
</blockquote>
</li>
<li>more</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044k0():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > 
>   > block
>   > abc
>   > un-block
>   > 
>   > _____
> + more
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,7):]",
        "[para(3,7):\n\n]",
        "[text(3,7):block\nabc\nun-block::\n\n]",
        "[end-para:::True]",
        "[BLANK(6,7):]",
        "[tbreak(7,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):more:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
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
<li>more</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044k1():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > 
>   > _____
> + more
>   this is more
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[ulist(1,3):+::4::\n\n  \n]",
        "[block-quote(1,5)::> \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,7):]",
        "[tbreak(3,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(4,3):4::]",
        "[para(4,5):\n]",
        "[text(4,5):more\nthis is more::\n]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<hr />
</blockquote>
</li>
<li>more
this is more</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044k2():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > 
>   > _____
> + > more
>   > this is more
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[BLANK(2,7):]",
        "[tbreak(3,7):_::_____]",
        "[end-block-quote:::True]",
        "[li(4,3):4::]",
        "[block-quote(4,5)::> \n>   > \n]",
        "[para(4,7):\n]",
        "[text(4,7):more\nthis is more::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<hr />
</blockquote>
</li>
<li>
<blockquote>
<p>more
this is more</p>
</blockquote>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lx():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + block 3
> >   block 3
> > + block 3
> > --------
> > ```block
> > A code block
> > ```
> > --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n]",
        "[ulist(1,5):+::6::  \n]",
        "[para(1,7):\n]",
        "[text(1,7):block 3\nblock 3::\n]",
        "[end-para:::True]",
        "[li(3,5):6::]",
        "[para(3,7):]",
        "[text(3,7):block 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::--------]",
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
<ul>
<li>block 3
block 3</li>
<li>block 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044la0():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
>   ------
>   ```block
>   A code block
>   ```
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::\n\n  þ\n  \n  \n  \n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n> ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[tbreak(4,5):-::------]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::------]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<blockquote>
<p>block 2
block 3</p>
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044la1():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
>   ------
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::\n\n  þ\n\n  \n  \n  \n\n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n> ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[tbreak(4,5):-::------]",
        "[BLANK(5,2):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,5):-::------]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<blockquote>
<p>block 2
block 3</p>
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lb():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
>   # xxx
>   ```block
>   A code block
>   ```
>   # xxx
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::\n\n  þ\n  \n  \n  \n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n> ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[atx(4,5):1:0:]",
        "[text(4,7):xxx: ]",
        "[end-atx::]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[atx(8,5):1:0:]",
        "[text(8,7):xxx: ]",
        "[end-atx::]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<blockquote>
<p>block 2
block 3</p>
</blockquote>
<h1>xxx</h1>
<pre><code class="language-block">A code block
</code></pre>
<h1>xxx</h1>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lc():
    """
    TBD
    """

    # Arrange
    source_markdown = """+ + > -----
    > > block 1
    > > block 2
    > -----
    > ```block
    > A code block
    > ```
    > -----
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :\n\n\n\n\n\n\n]",
        "[block-quote(1,5):    :    > \n    > \n    > \n    > \n    > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,5):    :    > > \n    > > \n    > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::    > :True]",
        "[tbreak(4,7):-::-----]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-block-quote:::True]",
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
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ldx():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>     -----
>     ```block
>     A code block
>     ```
>     -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::]",
        "[ulist(1,5):+::6:  :\n\n  þ\n    \n    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   :True]",
        "[tbreak(4,7):-::-----]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-ulist:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lda():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>
>     -----
>     ```block
>     A code block
>     ```
>     -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::]",
        "[ulist(1,5):+::6:  :\n\n\n    \n    \n    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n>]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-block-quote:::True]",
        "[tbreak(5,7):-::-----]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::-----]",
        "[end-ulist:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ldb0():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>     # before
>     ```block
>     A code block
>     ```
>     # after
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::]",
        "[ulist(1,5):+::6:  :\n\n  þ\n    \n    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   :True]",
        "[atx(4,7):1:0:]",
        "[text(4,9):before: ]",
        "[end-atx::]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[atx(8,7):1:0:]",
        "[text(8,9):after: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<h1>before</h1>
<pre><code class="language-block">A code block
</code></pre>
<h1>after</h1>
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ldb1():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>     <!-- before -->
>     ```block
>     A code block
>     ```
>     <!-- after -->
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::]",
        "[ulist(1,5):+::6:  :\n\n  þ\n    \n    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   :True]",
        "[html-block(4,7)]",
        "[text(4,7):<!-- before -->:]",
        "[end-html-block:::False]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[html-block(8,7)]",
        "[text(8,7):<!-- after -->:]",
        "[end-html-block:::False]",
        "[end-ulist:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<!-- before -->
<pre><code class="language-block">A code block
</code></pre>
<!-- after -->
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ldb1a():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>    <!-- before -->
>    ```block
>    A code block
>    ```
>    <!-- after -->
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  \n]",
        "[ulist(1,5):+::6:  :\n\n  þ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[html-block(4,5)]",
        "[text(4,6):<!-- before -->: ]",
        "[end-html-block:::False]",
        "[fcode-block(5,6):`:3:block:::: :]",
        "[text(6,3):A code block:\a \a\x03\a]",
        "[end-fcode-block: ::3:False]",
        "[html-block(8,5)]",
        "[text(8,6):<!-- after -->: ]",
        "[end-html-block:::False]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
 <!-- before -->
<pre><code class="language-block">A code block
</code></pre>
 <!-- after -->
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ldb1b():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>    <!-- before -->
>    ```block
>    A code block
>    ```
>    <!-- after -->
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  \n]",
        "[ulist(1,5):+::6:  :\n\n  þ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[html-block(4,5)]",
        "[text(4,6):<!-- before -->: ]",
        "[end-html-block:::False]",
        "[fcode-block(5,6):`:3:block:::: :]",
        "[text(6,3):A code block:\a \a\x03\a]",
        "[end-fcode-block: ::3:False]",
        "[html-block(8,5)]",
        "[text(8,6):<!-- after -->: ]",
        "[end-html-block:::False]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
 <!-- before -->
<pre><code class="language-block">A code block
</code></pre>
 <!-- after -->
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ldb1c():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>   <!-- before -->
>   ```block
>   A code block
>   ```
>   <!-- after -->
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  \n]",
        "[ulist(1,5):+::6:  :\n\n  þ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[html-block(4,5)]",
        "[text(4,5):<!-- before -->:]",
        "[end-html-block:::False]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[html-block(8,5)]",
        "[text(8,5):<!-- after -->:]",
        "[end-html-block:::False]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<!-- before -->
<pre><code class="language-block">A code block
</code></pre>
<!-- after -->
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ldb1d():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>  <!-- before -->
>  ```block
>  A code block
>  ```
>  <!-- after -->
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
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
        "[html-block(4,3)]",
        "[text(4,4):<!-- before -->: ]",
        "[end-html-block:::False]",
        "[fcode-block(5,4):`:3:block:::: :]",
        "[text(6,3):A code block:\a \a\x03\a]",
        "[end-fcode-block: ::3:False]",
        "[html-block(8,3)]",
        "[text(8,4):<!-- after -->: ]",
        "[end-html-block:::False]",
        "[ulist(9,3):+::4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
 <!-- before -->
<pre><code class="language-block">A code block
</code></pre>
 <!-- after -->
<ul>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ldb1e():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
> <!-- before -->
> ```block
> A code block
> ```
> <!-- after -->
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
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
        "[html-block(4,3)]",
        "[text(4,3):<!-- before -->:]",
        "[end-html-block:::False]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[html-block(8,3)]",
        "[text(8,3):<!-- after -->:]",
        "[end-html-block:::False]",
        "[ulist(9,3):+::4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<!-- before -->
<pre><code class="language-block">A code block
</code></pre>
<!-- after -->
<ul>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ldc():
    """
    TBD
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
        "[ulist(1,3):+::4::  \n  \n  \n  \n]",
        "[ulist(1,5):+::6:  :\n\n  \u00fe]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::-----]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::-----]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lddx():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(4,7):-::-----]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ldd1():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > >block 1
>   > >block 2
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > >\n>   > >\n>   > ]",
        "[para(2,8):\n]",
        "[text(2,8):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(4,7):-::-----]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lde():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > ]",
        "[para(2,9):]",
        "[text(2,9):block 1:]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(3,7):-::-----]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ldf():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > -----
>   > > block 1
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > ]",
        "[para(2,9):]",
        "[text(2,9):block 1:]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(3,7):-::-----]",
        "[block-quote(4,7)::>   > > \n>   > ]",
        "[para(4,9):]",
        "[text(4,9):block 1:]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(5,7):-::-----]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<blockquote>
<p>block 1</p>
</blockquote>
<hr />
<blockquote>
<p>block 1</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ldg():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > + block 1
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:]",
        "[para(2,9):]",
        "[text(2,9):block 1:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(3,7):-::-----]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<blockquote>
<hr />
<ul>
<li>block 1</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lex1():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_and_thematics
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >   ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  \n  \n]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):_::______]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):_::______]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lex1a():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list_and_thematics
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >   ______
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> >\n> > \n> > \n> > \n> >\n> > ]",
        "[ulist(1,5):+::6::\n  \n  \n  \n\n  \n]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):_::______]",
        "[BLANK(6,4):]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,4):]",
        "[tbreak(11,7):_::______]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lex2():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >  ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n]",
        "[ulist(1,5):+::6:]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[tbreak(5,6):_: :______]",
        "[fcode-block(6,7):`:3:block::::  :]",
        "[text(7,5):A code block:\a  \a\x03\a]",
        "[end-fcode-block:  ::3:False]",
        "[tbreak(9,7):_:  :______]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lex3():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> > ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n]",
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
        "[tbreak(5,5):_::______]",
        "[fcode-block(6,7):`:3:block::::  :]",
        "[text(7,5):A code block:\a  \a\x03\a]",
        "[end-fcode-block:  ::3:False]",
        "[tbreak(9,7):_:  :______]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lex3a():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> > # head 1
> >   ```block
> >   A code block
> >   ```
> >   # head 2
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n]",
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
        "[atx(5,5):1:0:]",
        "[text(5,7):head 1: ]",
        "[end-atx::]",
        "[fcode-block(6,7):`:3:block::::  :]",
        "[text(7,5):A code block:\a  \a\x03\a]",
        "[end-fcode-block:  ::3:False]",
        "[atx(9,7):1:0:  ]",
        "[text(9,9):head 2: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
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
<h1>head 1</h1>
<pre><code class="language-block">A code block
</code></pre>
<h1>head 2</h1>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lex3b():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> > <!-- html 1 -->
> >   ```block
> >   A code block
> >   ```
> >   <!-- html 2 -->
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n]",
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
        "[html-block(5,5)]",
        "[text(5,5):<!-- html 1 -->:]",
        "[end-html-block:::False]",
        "[fcode-block(6,7):`:3:block::::  :]",
        "[text(7,5):A code block:\a  \a\x03\a]",
        "[end-fcode-block:  ::3:False]",
        "[html-block(9,5)]",
        "[text(9,7):<!-- html 2 -->:  ]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
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
<!-- html 1 -->
<pre><code class="language-block">A code block
</code></pre>
  <!-- html 2 -->
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lex4():
    """
    TBD
    BLAH-F
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >    ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  \n  \n]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n   ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,8):_: :______]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):_::______]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lex5x():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >     ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  \n]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n    \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[tbreak(5,9):_::______]",
        "[end-ulist:::True]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):_::______]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2</li>
<li>list 3
<hr />
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lex5a():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >     ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  \n]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n    \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::False]",
        "[tbreak(4,9):_::______]",
        "[end-ulist:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):_::______]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
list 2
<hr />
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lex5b():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  \n]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n  ]",
        "[para(2,9):]",
        "[text(2,9):list 1:]",
        "[end-para:::False]",
        "[tbreak(3,9):_::______]",
        "[end-ulist:::True]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,7):_::______]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<ul>
<li>list 1
<hr />
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lex5c():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + ______
> >     ______
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  \n  \n  \n]",
        "[tbreak(1,7):_::______]",
        "[tbreak(2,9):_:  :______]",
        "[fcode-block(3,7):`:3:block:::::]",
        "[text(4,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(6,7):_::______]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ul>
<li>
<hr />
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044lea():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + ______
>     + list 1
>       list 2
>     + list 3
>     ______
>     ```block
>     A code block
>     ```
>     ______
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :    \n    \n    \n    \n]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:    :      \n    ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):_::______]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):_::______]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mx1():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_block
    """

    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
   >   ```block
   >   A code block
   >   ```
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::\n\n  þ\n  \n  \n  \n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > \n   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[fcode-block(4,8):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,8):-::----]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mx2():
    """
    TBD
    """

    # Arrange
    source_markdown = """1. > + ----
   >   ```block
   >   A code block
   >   ```
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::  \n  \n  \n  \n]",
        "[tbreak(1,8):-::----]",
        "[fcode-block(2,8):`:3:block:::::]",
        "[text(3,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(5,8):-::----]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mx30():
    """
    TBD

    Note: In commonmark java 0.13.0 and commonmark.js 0.28.1, both
    report that the `A code block` should be in a paragraph, hinting
    that it is loose.  There are no blank lines, hence, cannot be loose.
    """

    # Arrange
    source_markdown = """1. > + ----
       first list item    
     + next list item    
   >   > block 1
   >   > block 2
   >   # header
   >   A code block
   >   # header
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :   > ]",
        "[ulist(1,6):+::7:]",
        "[tbreak(1,8):-::----]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[icode-block(2,8):    :]",
        "[text(2,8):first list item    :]",
        "[end-icode-block:::True]",
        "[ulist(3,6):+::7:     ]",
        "[para(3,8)::    ]",
        "[text(3,8):next list item:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(4,4):   :   > \n   > \n   > \n   > \n]",
        "[block-quote(4,8)::   >   > \n   >   > \n   > ]",
        "[para(4,10):\n]",
        "[text(4,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[atx(6,8):1:0:  ]",
        "[text(6,10):header: ]",
        "[end-atx::]",
        "[para(7,8):  ]",
        "[text(7,8):A code block:]",
        "[end-para:::False]",
        "[atx(8,8):1:0:  ]",
        "[text(8,10):header: ]",
        "[end-atx::]",
        "[tbreak(9,8):-:  :----]",
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
</li>
</ul>
</blockquote>
<pre><code>first list item    
</code></pre>
<ul>
<li>next list item</li>
</ul>
<blockquote>
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<h1>header</h1>
A code block
<h1>header</h1>
<hr />
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mx31():
    """
    TBD
    """

    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
   >   # header
   >   A code block
   >   # header
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::\n\n  þ\n  \n  \n  \n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > \n   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[atx(4,8):1:0:]",
        "[text(4,10):header: ]",
        "[end-atx::]",
        "[para(5,8):]",
        "[text(5,8):A code block:]",
        "[end-para:::False]",
        "[atx(6,8):1:0:]",
        "[text(6,10):header: ]",
        "[end-atx::]",
        "[tbreak(7,8):-::----]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<h1>header</h1>
A code block
<h1>header</h1>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mx4():
    """
    TBD
    """

    # Arrange
    source_markdown = """1. > + ----
   >   # header
   >   A code block
   >   # header
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::  \n  \n  \n  \n]",
        "[tbreak(1,8):-::----]",
        "[atx(2,8):1:0:]",
        "[text(2,10):header: ]",
        "[end-atx::]",
        "[para(3,8):]",
        "[text(3,8):A code block:]",
        "[end-para:::False]",
        "[atx(4,8):1:0:]",
        "[text(4,10):header: ]",
        "[end-atx::]",
        "[tbreak(5,8):-::----]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<ul>
<li>
<hr />
<h1>header</h1>
A code block
<h1>header</h1>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mx50():
    """
    TBD
    """

    # Arrange
    source_markdown = """1. > + _____
   >   > block 1
   >   > block 2
   >   _____
   >   A code block
   >   _____
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::\n\n  þ\n  \n  \n]",
        "[tbreak(1,8):_::_____]",
        "[block-quote(2,8)::> \n   >   > \n   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[tbreak(4,8):_::_____]",
        "[para(5,8):]",
        "[text(5,8):A code block:]",
        "[end-para:::False]",
        "[tbreak(6,8):_::_____]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
A code block
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mx60():
    """
    TBD
    """

    # Arrange
    source_markdown = """1. > + _____
   >   > block 1
   >   > block 2
   >   <!--
   >   A code block
   >   -->
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::\n\n  þ\n  \n  \n]",
        "[tbreak(1,8):_::_____]",
        "[block-quote(2,8)::> \n   >   > \n   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[html-block(4,8)]",
        "[text(4,8):<!--\nA code block\n-->:]",
        "[end-html-block:::False]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<!--
A code block
-->
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044ma():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > >
> > > > fourth block 1
> > > > fourth block 2
> > > --------
> > > ```block
> > > A code block
> > > ```
> > > --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > >\n> > > \n> > > \n> > > \n> > > \n]",
        "[BLANK(1,6):]",
        "[block-quote(2,1)::> > > > \n> > > > \n> > > ]",
        "[para(2,9):\n]",
        "[text(2,9):fourth block 1\nfourth block 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> > > :True]",
        "[tbreak(4,7):-::--------]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::--------]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mb():
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcxx():
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
        "[ulist(1,3):+::5::  \n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_044mcxa():
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
def test_extra_044mca():
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
        "[ulist(1,3):+::4::  \n]",
        "[para(1,5):\n]",
        "[text(1,5):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_044mcb():
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
        "[ulist(1,3):+::5::   \n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):5::]",
        "[para(3,6):]",
        "[text(3,6):that:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_044mcc():
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
        "[ulist(1,3):+::5::\n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_044mcd():
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
        "[ulist(1,3):+::5:: \n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_044mce():
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
        "[ulist(1,3):+::5::   \n]",
        "[para(1,6):\n]",
        "[text(1,6):list\nthis::\n]",
        "[end-para:::True]",
        "[li(3,3):4::]",
        "[para(3,5):]",
        "[text(3,5):that:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_044mcm():
    """
    TBD
    """

    source_markdown = """   >    >    1. list
   >    >    item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[olist(1,14):.:1:16:   :   ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcn():
    """
    TBD
    """

    source_markdown = """   >    >    1. list
   >    >   item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[olist(1,14):.:1:16:   :  ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mco():
    """
    TBD
    """

    source_markdown = """   >    >    1. list
   >    >  item"""
    expected_tokens = [
        "[block-quote(1,4):   :   > ]",
        "[block-quote(1,9)::   >    > \n   >    > ]",
        "[olist(1,14):.:1:16:   : ]",
        "[para(1,17):\n]",
        "[text(1,17):list\nitem::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<ol>
<li>list
item</li>
</ol>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcp():
    """
    TBD
    BLAH-G
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
def test_extra_044mcq0():
    """
    TBD
    """

    # Arrange
    source_markdown = """+ + + -----
      + list 1
        list 2
      + list 3
      -----
      ```block
      A code block
      ```
      -----
  + another list"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    :      \n      \n      \n      \n      ]",
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
        "[tbreak(5,7):-::-----]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::-----]",
        "[end-ulist:::True]",
        "[li(10,3):4:  :]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcq1():
    """
    TBD
    """

    # Arrange
    source_markdown = """+ + + -----
      + list 1
        list 2
      + list 3
      -----

      ```block
      A code block
      ```

      -----
  + another list"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[ulist(1,5):+::6:    :      \n\n      \n      \n      \n\n      ]",
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
        "[tbreak(5,7):-::-----]",
        "[BLANK(6,1):]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,1):]",
        "[tbreak(11,7):-::-----]",
        "[end-ulist:::True]",
        "[li(12,3):4:  :]",
        "[para(12,5):]",
        "[text(12,5):another list:]",
        "[end-para:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcr0():
    """
    TBD
    """

    # Arrange
    source_markdown = """+ + list 1
    > block 2.1
    > block 2.2
    ```block
    A code block
    ```
  + another list"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :\n\n    \n    \n    ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5):    :    > \n    > ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2.1\nblock 2.2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(7,3):4:  :]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcr1():
    """
    TBD
    """

    # Arrange
    source_markdown = """+ + list 1
    > block 2.1
    > block 2.2

    ```block
    A code block
    ```

  + another list"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  :\n\n\n    \n    \n    \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5):    :    > \n    > \n]",
        "[para(2,7):\n]",
        "[text(2,7):block 2.1\nblock 2.2::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
        "[li(9,3):4:  :]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>
<p>list 1</p>
<blockquote>
<p>block 2.1
block 2.2</p>
</blockquote>
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcs0():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     + list 1
>       list 2
>     + list 3
>     -----
>     ```block
>     A code block
>     ```
>     -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :    \n    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:    :      \n    ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):-::-----]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::-----]",
        "[end-ulist:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcs1():
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_and_thematics
    """

    # Arrange
    source_markdown = """> + + -----
>     + list 1
>       list 2
>     + list 3
>     -----
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n    \n    \n    \n\n    ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:    :      \n    ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,7):-::-----]",
        "[BLANK(6,2):]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,2):]",
        "[tbreak(11,7):-::-----]",
        "[end-ulist:::True]",
        "[li(12,3):4::]",
        "[para(12,5):]",
        "[text(12,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mct0():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>     -----
>     ```block
>     A code block
>     ```
>     -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n  þ\n    \n    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   :True]",
        "[tbreak(4,7):-::-----]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-ulist:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mct1():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>     -----
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n  þ\n\n    \n    \n    \n\n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   :True]",
        "[tbreak(4,7):-::-----]",
        "[BLANK(5,2):]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,7):-::-----]",
        "[end-ulist:::True]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcu0():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > \n>   > ]",
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
        "[tbreak(5,7):-::-----]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcu1():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + > -----
>   > + list 1
>   >   list 2
>   > + list 3
>   > -----
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   >\n>   > \n>   > \n>   > \n>   >\n>   > ]",
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
        "[tbreak(5,7):-::-----]",
        "[BLANK(6,6):]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,6):]",
        "[tbreak(11,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(12,3):4::]",
        "[para(12,5):]",
        "[text(12,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcv0():
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_with_thematics
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(4,7):-::-----]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcv1():
    """
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block_with_thematics
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   >\n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(4,7):-::-----]",
        "[BLANK(5,6):]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,6):]",
        "[tbreak(10,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcw0():
    """
    TBD
    """

    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
   >   ```block
   >   A code block
   >   ```
   >   ----"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::\n\n  þ\n  \n  \n  ]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > \n   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[fcode-block(4,8):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,8):-::----]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcw1():
    """
    TBD
    """

    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   ----"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > \n   >\n   > ]",
        "[ulist(1,6):+::7::\n\n\n  \n  \n  \n\n  ]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > \n   >]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,5):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,8):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,5):]",
        "[tbreak(9,8):-::----]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcw2():
    """
    TBD
    """

    # Arrange
    source_markdown = """1. > + ----
   >   > block 1
   >   > block 2
   >   # header 1
   >   ```block
   >   A code block
   >   ```
   >   # header 2
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::\n\n  þ\n  \n  \n  \n  \n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,8)::> \n   >   > \n   > ]",
        "[para(2,10):\n]",
        "[text(2,10):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[atx(4,8):1:0:]",
        "[text(4,10):header 1: ]",
        "[end-atx::]",
        "[fcode-block(5,8):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[atx(8,8):1:0:]",
        "[text(8,10):header 2: ]",
        "[end-atx::]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<h1>header 1</h1>
<pre><code class="language-block">A code block
</code></pre>
<h1>header 2</h1>
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcx0():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> >   --------
> >   ```block
> >   A code block
> >   ```
> >   --------"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::\n\n  þ\n  \n  \n  \n  ]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[tbreak(4,7):-::--------]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::--------]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcx1():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> >   --------
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   --------"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> >\n> > \n> > \n> > \n> >\n> > ]",
        "[ulist(1,5):+::6::\n\n  þ\n\n  \n  \n  \n\n  ]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[tbreak(4,7):-::--------]",
        "[BLANK(5,4):]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,4):]",
        "[tbreak(10,7):-::--------]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcy0():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> > > --------
> > > ```block
> > > A code block
> > > ```
> > > --------"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > >\n> > > \n> > > \n> > > \n> > > \n> > > \n> > > \n> > > \n> > > ]",
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
        "[tbreak(5,7):-::--------]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::--------]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<ul>
<li>inner list 1
inner list 2</li>
<li>inner list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcy1():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > >
> > > + inner list 1
> > >   inner list 2
> > > + inner list 3
> > > --------
> > >
> > > ```block
> > > A code block
> > > ```
> > >
> > > --------"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::]",
        "[block-quote(1,5)::> > >\n> > > \n> > > \n> > > \n> > > \n> > >\n> > > \n> > > \n> > > \n> > >\n> > > ]",
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
        "[tbreak(5,7):-::--------]",
        "[BLANK(6,6):]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,6):]",
        "[tbreak(11,7):-::--------]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<ul>
<li>inner list 1
inner list 2</li>
<li>inner list 3</li>
</ul>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcz0x():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>     ```block
>     A code block
>     ```
>     -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n  þ\n    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n> ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   :True]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,7):-::-----]",
        "[end-ulist:::True]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcz0a():
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_block
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n\n    \n    \n    \n\n    ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n>]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[tbreak(9,7):-::-----]",
        "[end-ulist:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcz1():
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcz2():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>    ```block
>    A code block
>    ```
>    -----
> + another list"""
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
        "[fcode-block(4,6):`:3:block:::: :]",
        "[text(5,3):A code block:\a \a\x03\a]",
        "[end-fcode-block: ::3:False]",
        "[tbreak(7,6):-: :-----]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcz3():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>   ```block
>   A code block
>   ```
>   -----
> + another list"""
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
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,5):-::-----]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcz4():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>  ```block
>  A code block
>  ```
>  -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
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
        "[fcode-block(4,4):`:3:block:::: :]",
        "[text(5,3):A code block:\a \a\x03\a]",
        "[end-fcode-block: ::3:False]",
        "[tbreak(7,4):-: :-----]",
        "[ulist(8,3):+::4:]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<ul>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcz5():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
> ```block
> A code block
> ```
> -----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
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
        "[ulist(8,3):+::4:]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<ul>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_044mcz6():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + + -----
>     > block 1
>     > block 2
>```block
>A code block
>```
>-----
> + another list"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>\n>\n> ]",
        "[ulist(1,3):+::4:]",
        "[ulist(1,5):+::6:  :\n\n]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>     > \n>     > \n>]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,2):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,2):-::-----]",
        "[ulist(8,3):+::4:]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<ul>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_045x():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> >\a
> >  ```block
> >   A code block
> >   ```
> >\a
> >  --------
> >\a
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > \n]",
        "[ulist(1,5):+::6::\n\n\n ]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,5):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,6):`:3:block:::: :]",
        "[text(6,5):A code block:\a \a\x03\a ]",
        "[end-fcode-block:  ::3:False]",
        "[BLANK(8,5):]",
        "[tbreak(9,6):-: :--------]",
        "[BLANK(10,5):]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block"> A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_045a():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> >
> >  ```block
> >   A code block
> >   ```
> >
> >  --------
> >
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> >\n> > \n> >\n]",
        "[ulist(1,5):+::6::\n\n\n ]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> >]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,4):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[fcode-block(5,6):`:3:block:::: :]",
        "[text(6,5):A code block:\a \a\x03\a ]",
        "[end-fcode-block:  ::3:False]",
        "[BLANK(8,4):]",
        "[tbreak(9,6):-: :--------]",
        "[BLANK(10,4):]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block"> A code block
</code></pre>
<hr />
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046x():
    """
    TBD
    test_extra_046x
    """

    # Arrange
    source_markdown = """> + list 1
>   + list 2
>   list 3
>   ------
>   ```block
>   A code block
>   ```
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :  \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::------]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::------]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<ul>
<li>list 2
list 3</li>
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046a():
    """
    TBD
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
        "[ulist(1,3):+::4::  \n  \n  \n  \n  \n  \n]",
        "[setext(3,5):-:6::(1,5)]",
        "[text(1,5):list 1\nlist 2::\n]",
        "[end-setext::]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,5):-::------]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_046b():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_with_thematics_sub3
    """

    # Arrange
    source_markdown = """> + list 1
>   + list 2
>   + list 3
>   _____
>
>   ```block
>   A code block
>   ```
>
>   _____
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::\n  \n  \n  \n\n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :  ]",
        "[para(2,7):]",
        "[text(2,7):list 2:]",
        "[end-para:::True]",
        "[li(3,5):6:  :]",
        "[para(3,7):]",
        "[text(3,7):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):_::_____]",
        "[BLANK(5,2):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,5):_::_____]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<ul>
<li>list 2</li>
<li>list 3</li>
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046cx():
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
def test_extra_046ca():
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_block
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>   >\n>   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,6):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,6):]",
        "[tbreak(9,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046cc0():
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list
    """

    # Arrange
    source_markdown = """> + + -----
>     + list 1
>       list 2
>     + list 3
>     ```block
>     A code block
>     ```
>     -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::]",
        "[ulist(1,5):+::6:  :    \n    \n    ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:    :      \n    ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-ulist:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046cc1():
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list
    """

    # Arrange
    source_markdown = """> + + -----
>     + list 1
>       list 2
>     + list 3
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::]",
        "[ulist(1,5):+::6:  :    \n    \n\n    ]",
        "[tbreak(1,7):-::-----]",
        "[ulist(2,7):+::8:    :      \n\n    ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:    :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[BLANK(5,2):]",
        "[end-ulist:::True]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,7):-::-----]",
        "[end-ulist:::True]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046cc2():
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_sub1
    """

    # Arrange
    source_markdown = """> +
>   + -----
>     + list 1
>       list 2
>     + list 3
>     ```block
>     A code block
>     ```
>     -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::]",
        "[BLANK(1,4):]",
        "[ulist(2,5):+::6:  :    \n    \n    ]",
        "[tbreak(2,7):-::-----]",
        "[ulist(3,7):+::8:    :      \n    ]",
        "[para(3,9):\n]",
        "[text(3,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(5,7):8:    :]",
        "[para(5,9):]",
        "[text(5,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,7):-::-----]",
        "[end-ulist:::True]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_extra_046cc3():
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_sub1
    """

    # Arrange
    source_markdown = """> +
>   + -----
>     + list 1
>       list 2
>     + list 3
>
>     ```block
>     A code block
>     ```
>
>     -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::]",
        "[BLANK(1,4):]",
        "[ulist(2,5):+::6:  :    \n    \n\n    ]",
        "[tbreak(2,7):-::-----]",
        "[ulist(3,7):+::8:    :      \n\n    ]",
        "[para(3,9):\n]",
        "[text(3,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(5,7):8:    :]",
        "[para(5,9):]",
        "[text(5,9):list 3:]",
        "[end-para:::True]",
        "[BLANK(6,2):]",
        "[end-ulist:::True]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,2):]",
        "[tbreak(11,7):-::-----]",
        "[end-ulist:::True]",
        "[li(12,3):4::]",
        "[para(12,5):]",
        "[text(12,5):another list:]",
        "[end-para:::True]",
        "[BLANK(13,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_extra_046cc4():
    """
    TBD
    bad_fenced_block_in_list_in_list_in_block_quote_with_previous_list_sub2
    """

    # Arrange
    source_markdown = """> +
>   + -----
>     + list 1
>       list 2
>     ```block
>     A code block
>     ```
>     -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::]",
        "[BLANK(1,4):]",
        "[ulist(2,5):+::6:  :    \n    \n    ]",
        "[tbreak(2,7):-::-----]",
        "[ulist(3,7):+::8:    :      \n    ]",
        "[para(3,9):\n]",
        "[text(3,9):list 1\nlist 2::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::-----]",
        "[end-ulist:::True]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
</ul>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046cc5():
    """
    TBD
    """

    # Arrange
    source_markdown = """> +
>   + list 1
>     list 2
>   + list 3
>   ```block
>   A code block
>   ```
>   -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n]",
        "[BLANK(1,4):]",
        "[ulist(2,5):+::6:  :    \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,5):6:  :]",
        "[para(4,7):]",
        "[text(4,7):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):-::-----]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<ul>
<li>list 1
list 2</li>
<li>list 3</li>
</ul>
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
def test_extra_046dx():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_and_para_continue_with_thematics
    """

    # Arrange
    source_markdown = """> + list 1
>   + list 2
>   list 3
>   ------
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::\n  \n  \n  \n\n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :  \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):-::------]",
        "[BLANK(5,2):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,5):-::------]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<ul>
<li>list 2
list 3</li>
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046da():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_and_para_continue
    """

    # Arrange
    source_markdown = """> + list 1
>   + list 2
>   list 3
>   ```block
>   A code block
>   ```
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :  \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,5):-::------]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<ul>
<li>list 2
list 3</li>
</ul>
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
def test_extra_046db():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_and_para_continue
    """

    # Arrange
    source_markdown = """> + list 1
>   + list 2
>   list 3
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n\n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :  \n\n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-ulist:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[tbreak(9,5):-::------]",
        "[li(10,3):4::]",
        "[para(10,5):]",
        "[text(10,5):another list:]",
        "[end-para:::True]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<ul>
<li>list 2
list 3</li>
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046e0():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_with_thematics_sub3
    """

    # Arrange
    source_markdown = """> + list 1
>   + list 2
>   + list 3
>   _____
>   ```block
>   A code block
>   ```
>   _____
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n  \n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :  ]",
        "[para(2,7):]",
        "[text(2,7):list 2:]",
        "[end-para:::True]",
        "[li(3,5):6:  :]",
        "[para(3,7):]",
        "[text(3,7):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):_::_____]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,5):_::_____]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<ul>
<li>list 2</li>
<li>list 3</li>
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046e1():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_list_with_thematics_sub3
    """

    # Arrange
    source_markdown = """> + list 1
>   + list 2
>   + list 3
>   _____
>
>   ```block
>   A code block
>   ```
>
>   ------
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n> \n> \n>\n> \n> ]",
        "[ulist(1,3):+::4::\n  \n  \n  \n\n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :  ]",
        "[para(2,7):]",
        "[text(2,7):list 2:]",
        "[end-para:::True]",
        "[li(3,5):6:  :]",
        "[para(3,7):]",
        "[text(3,7):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(4,5):_::_____]",
        "[BLANK(5,2):]",
        "[fcode-block(6,5):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,2):]",
        "[tbreak(10,5):-::------]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<ul>
<li>list 2</li>
<li>list 3</li>
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046f0():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_list
    """

    # Arrange
    source_markdown = """> + list 1
>   + list 2
>     list 3
>   ```block
>   A code block
>   ```
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::  \n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :    \n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<ul>
<li>list 2
list 3</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046f0a():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list 1
>   + list 2
>     list 3
> ```block
> A code block
> ```
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4:]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :    \n]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,3):`:3:block:::::]",
        "[text(5,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[ulist(7,3):+::4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<ul>
<li>list 2
list 3</li>
</ul>
</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
<ul>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046f1():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_list
    """

    # Arrange
    source_markdown = """> + list 1
>   + list 2
>     list 3
>
>   ```block
>   A code block
>   ```
>
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> \n> \n> \n>\n> ]",
        "[ulist(1,3):+::4::  \n  \n\n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[ulist(2,5):+::6:  :    \n\n  ]",
        "[para(2,7):\n]",
        "[text(2,7):list 2\nlist 3::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-ulist:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<ul>
<li>list 2
list 3</li>
</ul>
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
def test_extra_046g0():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_0_without_thematics
    """

    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
>   ```block
>   A code block
>   ```
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[ulist(1,3):+::4::\n\n  þ\n  \n  \n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n> ]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>list 1
<blockquote>
<p>block 2
block 3</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046g1():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_with_previous_inner_block_0_without_thematics
    """

    # Arrange
    source_markdown = """> + list 1
>   > block 2
>   > block 3
>
>   ```block
>   A code block
>   ```
>
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> ]",
        "[ulist(1,3):+::4::\n\n\n  \n  \n  \n\n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>   > \n>]",
        "[para(2,7):\n]",
        "[text(2,7):block 2\nblock 3::\n]",
        "[end-para:::True]",
        "[BLANK(4,2):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,2):]",
        "[li(9,3):4::]",
        "[para(9,5):]",
        "[text(9,5):another list:]",
        "[end-para:::True]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<blockquote>
<p>block 2
block 3</p>
</blockquote>
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
def test_extra_046g2():
    """
    TBD
    """

    # Arrange
    source_markdown = """> + list 1
>   > block 2
>
>   ```block
>   A code block
>   ```
>
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n>\n> ]",
        "[ulist(1,3):+::4::\n\n  \n  \n  \n\n]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[block-quote(2,5)::> \n>]",
        "[para(2,7):]",
        "[text(2,7):block 2:]",
        "[end-para:::True]",
        "[BLANK(3,2):]",
        "[end-block-quote:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(7,2):]",
        "[li(8,3):4::]",
        "[para(8,5):]",
        "[text(8,5):another list:]",
        "[end-para:::True]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>
<p>list 1</p>
<blockquote>
<p>block 2</p>
</blockquote>
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
def test_extra_046h0():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_with_thematics
    """

    # Arrange
    source_markdown = """1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > > ----
   > > ```block
   > > A code block
   > > ```
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n]",
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
        "[tbreak(5,8):-::----]",
        "[fcode-block(6,8):`:3:block:::::]",
        "[text(7,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,8):-::----]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046h1():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list_with_thematics
    """

    # Arrange
    source_markdown = """1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > > ----
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > > \n   > >\n   > > \n   > > \n   > > \n   > >\n   > > \n]",
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
        "[tbreak(5,8):-::----]",
        "[BLANK(6,7):]",
        "[fcode-block(7,8):`:3:block:::::]",
        "[text(8,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,7):]",
        "[tbreak(11,8):-::----]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046j0():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list
    """

    # Arrange
    source_markdown = """1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > > ```block
   > > A code block
   > > ```
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n   > > \n]",
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
        "[fcode-block(5,8):`:3:block:::::]",
        "[text(6,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,8):-::----]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046j1():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_list
    """

    # Arrange
    source_markdown = """1. > > ----
   > > + list 1
   > >   list 2
   > > + list 3
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > >\n   > > \n   > > \n   > > \n   > >\n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9::  \n\n]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9::]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::True]",
        "[BLANK(5,7):]",
        "[end-ulist:::True]",
        "[fcode-block(6,8):`:3:block:::::]",
        "[text(7,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,7):]",
        "[tbreak(10,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046k0():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block_with_thematics
    """

    # Arrange
    source_markdown = """1. > > ----
   > > > inner block 1
   > > > inner block 2
   > > ----
   > > ```block
   > > A code block
   > > ```
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,4):   :   > > > \n   > > > \n   > > ]",
        "[para(2,10):\n]",
        "[text(2,10):inner block 1\ninner block 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > > :True]",
        "[tbreak(4,8):-::----]",
        "[fcode-block(5,8):`:3:block:::::]",
        "[text(6,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<blockquote>
<p>inner block 1
inner block 2</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046k1():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block_with_thematics
    """

    # Arrange
    source_markdown = """1. > > ----
   > > > inner block 1
   > > > inner block 2
   > > ----
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > >\n   > > \n   > > \n   > > \n   > >\n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,4):   :   > > > \n   > > > \n   > > ]",
        "[para(2,10):\n]",
        "[text(2,10):inner block 1\ninner block 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > > :True]",
        "[tbreak(4,8):-::----]",
        "[BLANK(5,7):]",
        "[fcode-block(6,8):`:3:block:::::]",
        "[text(7,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,7):]",
        "[tbreak(10,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<blockquote>
<p>inner block 1
inner block 2</p>
</blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046l0():
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
        "[ulist(1,3):+::4::  \n  \n  \n]",
        "[para(1,5):]",
        "[text(1,5):list:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:block:::::]",
        "[text(3,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(5,3):4::]",
        "[para(5,5):]",
        "[text(5,5):another list:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_046l1():
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
        "[ulist(1,3):+::4::\n  \n  \n  \n\n]",
        "[para(1,5):]",
        "[text(1,5):list:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[fcode-block(3,5):`:3:block:::::]",
        "[text(4,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,2):]",
        "[li(7,3):4::]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
def test_extra_046m0():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block
    """

    # Arrange
    source_markdown = """1. > > ----
   > > > inner block 1
   > > > inner block 2
   > > ```block
   > > A code block
   > > ```
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,4):   :   > > > \n   > > > \n   > > ]",
        "[para(2,10):\n]",
        "[text(2,10):inner block 1\ninner block 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > > :True]",
        "[fcode-block(4,8):`:3:block:::::]",
        "[text(5,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<blockquote>
<p>inner block 1
inner block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046m1():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_with_previous_block
    """

    # Arrange
    source_markdown = """1. > > ----
   > > > inner block 1
   > > > inner block 2
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > >\n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[block-quote(2,4):   :   > > > \n   > > > \n   > >]",
        "[para(2,10):\n]",
        "[text(2,10):inner block 1\ninner block 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,7):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,8):`:3:block:::::]",
        "[text(6,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,7):]",
        "[tbreak(9,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<blockquote>
<p>inner block 1
inner block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046n0():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_with_thematics
    """

    # Arrange
    source_markdown = """1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >   ----
   >   ```block
   >   A code block
   >   ```
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::  \n  \n  \n  \n]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9:  :    \n  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9:  :]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,8):-::----]",
        "[fcode-block(6,8):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,8):-::----]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046n1():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list_with_thematics
    """

    # Arrange
    source_markdown = """1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >   ----
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > \n   >\n   > \n   > \n   > \n   >\n   > ]",
        "[ulist(1,6):+::7::\n  \n  \n  \n\n  \n]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9:  :    \n  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9:  :]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[tbreak(5,8):-::----]",
        "[BLANK(6,5):]",
        "[fcode-block(7,8):`:3:block:::::]",
        "[text(8,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,5):]",
        "[tbreak(11,8):-::----]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046p0():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list
    """

    # Arrange
    source_markdown = """1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >   ```block
   >   A code block
   >   ```
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   > \n   > \n   > \n   > ]",
        "[ulist(1,6):+::7::  \n  \n  \n]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9:  :    \n  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9:  :]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(5,8):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,8):-::----]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046p1():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_list_with_previous_list
    """

    # Arrange
    source_markdown = """1. > + ----
   >   + list 1
   >     list 2
   >   + list 3
   >
   >   ```block
   >   A code block
   >   ```
   >
   >   ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   > \n   >\n   > \n   > \n   > \n   >\n   > ]",
        "[ulist(1,6):+::7::  \n  \n\n  \n]",
        "[tbreak(1,8):-::----]",
        "[ulist(2,8):+::9:  :    \n\n  ]",
        "[para(2,10):\n]",
        "[text(2,10):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,8):9:  :]",
        "[para(4,10):]",
        "[text(4,10):list 3:]",
        "[end-para:::True]",
        "[BLANK(5,5):]",
        "[end-ulist:::True]",
        "[fcode-block(6,8):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,5):]",
        "[tbreak(10,8):-::----]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046q0():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_empty
    """

    # Arrange
    source_markdown = """1. > > ----
   > > ```block
   > > ```
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[fcode-block(2,8):`:3:block:::::]",
        "[end-fcode-block:::3:False]",
        "[tbreak(4,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<pre><code class="language-block"></code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046q1():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list_empty
    """

    # Arrange
    source_markdown = """1. > > ----
   > >
   > > ```block
   > > ```
   > >
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > >\n   > > \n   > > \n   > >\n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[BLANK(2,7):]",
        "[fcode-block(3,8):`:3:block:::::]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,7):]",
        "[tbreak(6,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<pre><code class="language-block"></code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046r0():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list
    """

    # Arrange
    source_markdown = """1. > > ----
   > > ```block
   > > A code block
   > > ```
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > > \n   > > \n   > > \n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[fcode-block(2,8):`:3:block:::::]",
        "[text(3,8):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(5,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046r1():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list
    """

    # Arrange
    source_markdown = """1. > > ----
   > >
   > > ```block
   > > A code block
   > > ```
   > >
   > > ----
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :]",
        "[block-quote(1,6):   :   > > \n   > >\n   > > \n   > > \n   > > \n   > >\n   > > \n]",
        "[tbreak(1,8):-::----]",
        "[BLANK(2,7):]",
        "[fcode-block(3,8):`:3:block:::::]",
        "[text(4,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,7):]",
        "[tbreak(7,8):-::----]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</blockquote>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046s0():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list
    """

    # Arrange
    source_markdown = """1. > >
   > > block 3
   > block 3
   > ```block
   > A code block
   > ```
   > --------
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n]",
        "[block-quote(1,6):   :   > >\n   > > \n   > \n   > ]",
        "[BLANK(1,7):]",
        "[para(2,8):\n]",
        "[text(2,8):block 3\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[fcode-block(4,6):`:3:block:::::]",
        "[text(5,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,6):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>block 3
block 3</p>
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
def test_extra_046s1():
    """
    TBD
    bad_fenced_block_in_block_quote_in_block_quote_in_list
    """

    # Arrange
    source_markdown = """1. > >
   > > block 3
   > block 3
   >
   > ```block
   > A code block
   > ```
   >
   > --------
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n   >\n   > \n]",
        "[block-quote(1,6):   :   > >\n   > > \n   > \n   >]",
        "[BLANK(1,7):]",
        "[para(2,8):\n]",
        "[text(2,8):block 3\nblock 3::\n]",
        "[end-para:::True]",
        "[BLANK(4,5):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,6):`:3:block:::::]",
        "[text(6,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,5):]",
        "[tbreak(9,6):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(10,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>block 3
block 3</p>
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
def test_extra_046t0():
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_with_previous_inner_block
    """

    # Arrange
    source_markdown = """1. > >
   > > block 3
   > > block 3
   > ```block
   > A code block
   > ```
   > --------
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n]",
        "[block-quote(1,6):   :   > >\n   > > \n   > > \n   > ]",
        "[BLANK(1,7):]",
        "[para(2,8):\n]",
        "[text(2,8):block 3\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[fcode-block(4,6):`:3:block:::::]",
        "[text(5,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,6):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>block 3
block 3</p>
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
def test_extra_046t1():
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_with_previous_inner_block
    """

    # Arrange
    source_markdown = """1. > >
   > > block 3
   > > block 3
   > ```block
   > A code block
   > ```
   > --------
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n\n\n\n]",
        "[block-quote(1,4):   :   > \n   > \n   > \n]",
        "[block-quote(1,6):   :   > >\n   > > \n   > > \n   > ]",
        "[BLANK(1,7):]",
        "[para(2,8):\n]",
        "[text(2,8):block 3\nblock 3::\n]",
        "[end-para:::False]",
        "[end-block-quote::   > :True]",
        "[fcode-block(4,6):`:3:block:::::]",
        "[text(5,6):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,6):-::--------]",
        "[end-block-quote:::True]",
        "[BLANK(8,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<blockquote>
<blockquote>
<p>block 3
block 3</p>
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
def test_extra_046u0():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >   ```block
> >   A code block
> >   ```
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::  \n  \n  \n]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):_::______]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046u1():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_list
    """

    # Arrange
    source_markdown = """> > + ______
> >   + list 1
> >     list 2
> >   + list 3
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   ______
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> >\n> > \n> > \n> > \n> >\n> > ]",
        "[ulist(1,5):+::6::  \n  \n\n  \n]",
        "[tbreak(1,7):_::______]",
        "[ulist(2,7):+::8:  :    \n\n  ]",
        "[para(2,9):\n]",
        "[text(2,9):list 1\nlist 2::\n]",
        "[end-para:::True]",
        "[li(4,7):8:  :]",
        "[para(4,9):]",
        "[text(4,9):list 3:]",
        "[end-para:::True]",
        "[BLANK(5,4):]",
        "[end-ulist:::True]",
        "[fcode-block(6,7):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(9,4):]",
        "[tbreak(10,7):_::______]",
        "[BLANK(11,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046v0():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block
    """

    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> >   ```block
> >   A code block
> >   ```
> >   --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::\n\n  þ\n  \n  \n  \n]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[fcode-block(4,7):`:3:block:::::]",
        "[text(5,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(7,7):-::--------]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046v1():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block
    """

    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> >
> >   ```block
> >   A code block
> >   ```
> >
> >   --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> >\n> > ]",
        "[ulist(1,5):+::6::\n\n\n  \n  \n  \n\n  \n]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> >]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(4,4):]",
        "[end-block-quote:::True]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,4):]",
        "[tbreak(9,7):-::--------]",
        "[BLANK(10,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_046w0a():
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
def test_extra_046w1():
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
def test_extra_046x0():
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
def test_extra_046x1():
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
def test_extra_047a0():
    """
    TBD
    bad_fenced_block_in_list_in_list_with_previous_inner_list
    """

    # Arrange
    source_markdown = """+ + list 1
+ + + list 2.1
      list 2.2
    ```block
    A code block
    ```
  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,1):2::]",
        "[ulist(2,3):+::4:  :    \n    \n    \n]",
        "[ulist(2,5):+::6:    :      \n]",
        "[para(2,7):\n]",
        "[text(2,7):list 2.1\nlist 2.2::\n]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(4,5):`:3:block:::::]",
        "[text(5,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[li(7,3):4:  :]",
        "[para(7,5):]",
        "[text(7,5):another list:]",
        "[end-para:::True]",
        "[BLANK(8,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>list 1</li>
</ul>
</li>
<li>
<ul>
<li>
<ul>
<li>list 2.1
list 2.2</li>
</ul>
<pre><code class="language-block">A code block
</code></pre>
</li>
<li>another list</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047a1():
    """
    TBD
    bad_fenced_block_in_list_in_list_with_previous_inner_list
    """

    # Arrange
    source_markdown = """+ + list 1
+ + + list 2.1
      list 2.2

    ```block
    A code block
    ```

  + another list
"""
    expected_tokens = [
        "[ulist(1,1):+::2:]",
        "[ulist(1,3):+::4:  ]",
        "[para(1,5):]",
        "[text(1,5):list 1:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(2,1):2::]",
        "[ulist(2,3):+::4:  :    \n    \n    \n\n]",
        "[ulist(2,5):+::6:    :      \n]",
        "[para(2,7):\n]",
        "[text(2,7):list 2.1\nlist 2.2::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(8,1):]",
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
<li>list 1</li>
</ul>
</li>
<li>
<ul>
<li>
<ul>
<li>list 2.1
list 2.2</li>
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
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047b0():
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
def test_extra_047b1():
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
def test_extra_047c0():
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
def test_extra_047c1():
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
        "[text(7,1):A code block:]",
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
def test_extra_047d0():
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blocks
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   > > block 1
>   > > block 2
>   > ```block
>   > A code block
>   > ```
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(4,7):-::-----]",
        "[block-quote(5,7)::>   > > \n>   > > \n>   > ]",
        "[para(5,9):\n]",
        "[text(5,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[fcode-block(7,7):`:3:block:::::]",
        "[text(8,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(10,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(11,3):4::]",
        "[para(11,5):]",
        "[text(11,5):another list:]",
        "[end-para:::True]",
        "[BLANK(12,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047d1():
    """
    TBD
    bad_fenced_block_in_block_quote_in_list_in_block_quote_with_previous_blocks
    """

    # Arrange
    source_markdown = """> + > -----
>   > > block 1
>   > > block 2
>   > -----
>   > > block 1
>   > > block 2
>   >
>   > ```block
>   > A code block
>   > ```
>   >
>   > -----
> + another list
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[ulist(1,3):+::4::\n\n\n\n\n\n\n\n\n\n\n]",
        "[block-quote(1,5)::> \n>   > \n>   > \n>   > \n>   > \n>   >\n>   > ]",
        "[tbreak(1,7):-::-----]",
        "[block-quote(2,7)::>   > > \n>   > > \n>   > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::>   > :True]",
        "[tbreak(4,7):-::-----]",
        "[block-quote(5,7)::>   > > \n>   > > \n>   >\n>   > ]",
        "[para(5,9):\n]",
        "[text(5,9):block 1\nblock 2::\n]",
        "[end-para:::True]",
        "[BLANK(7,6):]",
        "[end-block-quote:::True]",
        "[fcode-block(8,7):`:3:block:::::]",
        "[text(9,7):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(11,6):]",
        "[tbreak(12,7):-::-----]",
        "[end-block-quote:::True]",
        "[li(13,3):4::]",
        "[para(13,5):]",
        "[text(13,5):another list:]",
        "[end-para:::True]",
        "[BLANK(14,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
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
<hr />
<blockquote>
<p>block 1
block 2</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<hr />
</blockquote>
</li>
<li>another list</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047e0():
    """
    TBD
    bad_fenced_block_in_list_in_block_quote_in_block_quote_with_previous_block_with_thematics
    """

    # Arrange
    source_markdown = """> > + --------
> >   > block 1
> >   > block 2
> >   --------
> >   ```block
> >   A code block
> >   ```
> >   --------
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n> > \n> > \n> > \n> > ]",
        "[ulist(1,5):+::6::\n\n  \u00fe\n  \n  \n  \n  \n]",
        "[tbreak(1,7):-::--------]",
        "[block-quote(2,7)::> \n> >   > \n> > ]",
        "[para(2,9):\n]",
        "[text(2,9):block 1\nblock 2::\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[tbreak(4,7):-::--------]",
        "[fcode-block(5,7):`:3:block:::::]",
        "[text(6,1):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(8,7):-::--------]",
        "[BLANK(9,1):]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
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
<hr />
<pre><code class="language-block">A code block
</code></pre>
<hr />
</li>
</ul>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047f0():
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
def test_extra_047f1():
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
def test_extra_047f1a():
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
def test_extra_047f2():
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
def test_extra_047f3():
    """
    TBD
    bad_fenced_block_in_block_quote_with_previous_inner_blocks_with_thematics
    """

    # Arrange
    source_markdown = """> > inner block
> > > innermost block
> > > innermost block
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
        "[block-quote(1,3)::> > ]",
        "[para(1,5):]",
        "[text(1,5):inner block:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > > \n> > > \n> > \n>]",
        "[para(2,7):\n\n]",
        "[text(2,7):innermost block\ninnermost block\ninner block::\n\n]",
        "[end-para:::True]",
        "[BLANK(5,2):]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[setext(7,3):-:3::(6,3)]",
        "[text(6,3):This is text and no blank line.:]",
        "[end-setext::]",
        "[fcode-block(8,3):`:3:block:::::]",
        "[text(9,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(11,3):-::---]",
        "[para(12,2):]",
        "[text(12,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(13,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block</p>
<blockquote>
<p>innermost block
innermost block
inner block</p>
</blockquote>
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
def test_extra_047f4():
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
def test_extra_047f5():
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
def test_extra_047f6x():  # https://github.com/jackdewinter/pymarkdown/issues/1213
    """
    TBD
    bad_fenced_block_in_block_quote_with_previous_inner_blocks

    Note: temporary fix in __abcd_final( in transform containers.
    """

    # Arrange
    source_markdown = """> > inner block
> > > innermost block
> > > innermost block
> > inner block
> ```block
> A code block
> ```
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n]",
        "[block-quote(1,3)::> > ]",
        "[para(1,5):]",
        "[text(1,5):inner block:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > > \n> > > \n> > \n> ]",
        "[para(2,7):\n\n]",
        "[text(2,7):innermost block\ninnermost block\ninner block::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-block-quote:::True]",
        "[fcode-block(5,3):`:3:block:::::]",
        "[text(6,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[para(8,2):]",
        "[text(8,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block</p>
<blockquote>
<p>innermost block
innermost block
inner block</p>
</blockquote>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047f6a():
    """
    TBD
    """

    # Arrange
    source_markdown = """> > inner block
> > > innermost block
> > > innermost block
> > inner block
> > ```block
> > A code block
> > ```
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::>\n]",
        "[block-quote(1,3)::> > \n> > \n> > ]",
        "[para(1,5):]",
        "[text(1,5):inner block:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > > \n> > > \n> > \n> > ]",
        "[para(2,7):\n\n]",
        "[text(2,7):innermost block\ninnermost block\ninner block::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> > :True]",
        "[fcode-block(5,5):`:3:block:::::]",
        "[text(6,5):A code block:]",
        "[end-fcode-block:::3:False]",
        "[end-block-quote:::True]",
        "[para(8,2):]",
        "[text(8,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block</p>
<blockquote>
<p>innermost block
innermost block
inner block</p>
</blockquote>
<pre><code class="language-block">A code block
</code></pre>
</blockquote>
<p>This is a blank line and some text.</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_extra_047f6b():
    """
    TBD
    bad_fenced_block_in_block_quote_with_previous_inner_blocks_with_thematics
    """

    # Arrange
    source_markdown = """> > inner block
> > > innermost block
> > > innermost block
> > inner block
> ___
> ```block
> A code block
> ```
> ___
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n]",
        "[block-quote(1,3)::> > ]",
        "[para(1,5):]",
        "[text(1,5):inner block:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > > \n> > > \n> > \n> ]",
        "[para(2,7):\n\n]",
        "[text(2,7):innermost block\ninnermost block\ninner block::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-block-quote:::True]",
        "[tbreak(5,3):_::___]",
        "[fcode-block(6,3):`:3:block:::::]",
        "[text(7,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[tbreak(9,3):_::___]",
        "[para(10,2):]",
        "[text(10,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block</p>
<blockquote>
<p>innermost block
innermost block
inner block</p>
</blockquote>
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
def test_extra_047f6c():
    """
    TBD
    bad_fenced_block_in_block_quote_with_previous_inner_blocks_with_thematics
    """

    # Arrange
    source_markdown = """> > inner block
> > > innermost block
> > > innermost block
> > inner block
> ___
>
> ```block
> A code block
> ```
>
> ___
>This is a blank line and some text.
"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> \n> \n>\n> \n>\n]",
        "[block-quote(1,3)::> > ]",
        "[para(1,5):]",
        "[text(1,5):inner block:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > > \n> > > \n> > \n> ]",
        "[para(2,7):\n\n]",
        "[text(2,7):innermost block\ninnermost block\ninner block::\n\n]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[end-block-quote:::True]",
        "[tbreak(5,3):_::___]",
        "[BLANK(6,2):]",
        "[fcode-block(7,3):`:3:block:::::]",
        "[text(8,3):A code block:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(10,2):]",
        "[tbreak(11,3):_::___]",
        "[para(12,2):]",
        "[text(12,2):This is a blank line and some text.:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(13,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>inner block</p>
<blockquote>
<p>innermost block
innermost block
inner block</p>
</blockquote>
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
def test_extra_999():
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
    new_value = new_front_matter.calculate_initial_whitespace()
    assert new_value != 999
    assert new_front_matter.is_extension

    ParserHelper.count_newlines_in_texts("text")
