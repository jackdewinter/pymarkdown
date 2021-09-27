"""
Extra tests.
"""
import pytest

from .utils import act_and_assert


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
        "[link(1,1):inline:!%22#$%25&amp;'()*+,-./0123456789:;%3C=%3E?@A-Z%5B%5C%5D%5E_%60a-z%7B%7C%7D~::!\"#$%&'\\(\\)*+,-./0123456789:;<=>?@A-Z[\\\\]^_`a-z{|}~:::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = '<p><a href="!%22#$%25&amp;\'()*+,-./0123456789:;%3C=%3E?@A-Z%5B%5C%5D%5E_%60a-z%7B%7C%7D~">link</a></p>'

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
        "[link(1,1):inline:!%22#$%12&amp;'()*+,-./0123456789:;%3C=%3E?@A-Z%5B%5C%5D%5E_%60a-z%7B%7C%7D~::!\"#$%12&'\\(\\)*+,-./0123456789:;<=>?@A-Z[\\\\]^_`a-z{|}~:::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = '<p><a href="!%22#$%12&amp;\'()*+,-./0123456789:;%3C=%3E?@A-Z%5B%5C%5D%5E_%60a-z%7B%7C%7D~">link</a></p>'

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
    When encoding link characters, special attention is used for the % characters as
    the CommonMark parser treats "%<hex-char><hex-char>" as non-encodable.  Make sure
    this is tested at the end of the link.
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
        "[ulist(1,3):+::4:  ]",
        "[para(1,5):]",
        "[text(1,5):list:]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[fcode-block(2,3):`:3:block:::::]",
        "[text(3,3):A code block:]",
        "[end-fcode-block::3:False]",
        "[olist(5,3):.:1:5:  ]",
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
    When encoding link characters, special attention is used for the % characters as
    the CommonMark parser treats "%<hex-char><hex-char>" as non-encodable.  Make sure
    this is tested at the end of the link.
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
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        show_debug=False,
        disable_consistency_checks=True,
    )


@pytest.mark.gfm
def test_extra_007b():
    """
    When encoding link characters, special attention is used for the % characters as
    the CommonMark parser treats "%<hex-char><hex-char>" as non-encodable.  Make sure
    this is tested at the end of the link.
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
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        show_debug=True,
        disable_consistency_checks=True,
    )


@pytest.mark.gfm
def test_extra_007c():
    """
    When encoding link characters, special attention is used for the % characters as
    the CommonMark parser treats "%<hex-char><hex-char>" as non-encodable.  Make sure
    this is tested at the end of the link.
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
title">a
not
so simple</a>
a real test</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_extra_007d():
    """
    When encoding link characters, special attention is used for the % characters as
    the CommonMark parser treats "%<hex-char><hex-char>" as non-encodable.  Make sure
    this is tested at the end of the link.
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
title">a
not
so simple</a>
a real test</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )


@pytest.mark.gfm
def test_extra_007e():
    """
    When encoding link characters, special attention is used for the % characters as
    the CommonMark parser treats "%<hex-char><hex-char>" as non-encodable.  Make sure
    this is tested at the end of the link.
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
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, disable_consistency_checks=True
    )
