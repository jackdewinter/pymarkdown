"""
https://github.github.com/gfm/#links
"""
from test.utils import act_and_assert

import pytest


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_inline_links_493x():
    """
    Test case 493:  Here is a simple inline link:
    """

    # Arrange
    source_markdown = """[link](/uri "title")"""
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/uri:title::::link:False:":: :]',
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri" title="title">link</a></p>"""

    # Act & Assert
    #
    # NOTE: The `show_debug` is present to allow for extra coverage of the link_helper module.
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=True)


@pytest.mark.gfm
def test_inline_links_493a():
    """
    Test case 493a:  variation of 493 with space after
    """

    # Arrange
    source_markdown = """[link](/uri "title") """
    expected_tokens = [
        "[para(1,1):: ]",
        '[link(1,1):inline:/uri:title::::link:False:":: :]',
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri" title="title">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_493b():
    """
    Test case 493b:  variation of 493 with space and text after
    """

    # Arrange
    source_markdown = """[link](/uri "title") abc"""
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/uri:title::::link:False:":: :]',
        "[text(1,2):link:]",
        "[end-link::]",
        "[text(1,21): abc:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri" title="title">link</a> abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_494():
    """
    Test case 494:  The title may be omitted:
    """

    # Arrange
    source_markdown = """[link](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/uri:::::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_495():
    """
    Test case 495:  (part 1) Both the title and the destination may be omitted:
    """

    # Arrange
    source_markdown = """[link]()"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline::::::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_496():
    """
    Test case 496:  (part 2) Both the title and the destination may be omitted:
    """

    # Arrange
    source_markdown = """[link](<>)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline::::::link:True::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_497():
    """
    Test case 497:  (part 1) The destination can only contain spaces if it is enclosed in pointy brackets
    """

    # Arrange
    source_markdown = """[link](/my uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):link:]",
        "[text(1,6):]:]",
        "[text(1,7):(/my uri):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[link](/my uri)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_497a():
    """
    Test case 497a:  variation of 497 with no inline close and
        defined reference
    """

    # Arrange
    source_markdown = """[link](
        
[link]: /url 'title'"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:title::::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[text(1,7):(:]",
        "[end-para:::True]",
        "[BLANK(2,1):        ]",
        "[link-ref-def(3,1):True::link:: :/url:: :title:'title':]",
    ]
    expected_gfm = """<p><a href="/url" title="title">link</a>(</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_498():
    """
    Test case 498:  (part 2) The destination can only contain spaces if it is enclosed in pointy brackets
    """

    # Arrange
    source_markdown = """[link](</my uri>)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/my%20uri::/my uri:::link:True::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/my%20uri">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_499():
    """
    Test case 499:  (part 1) The destination cannot contain line breaks, even if enclosed in pointy brackets:
    """

    # Arrange
    source_markdown = """[link](foo
bar)"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):[:]",
        "[text(1,2):link:]",
        "[text(1,6):]:]",
        "[text(1,7):(foo\nbar)::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[link](foo
bar)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_500():
    """
    Test case 500:  (part 2) The destination cannot contain line breaks, even if enclosed in pointy brackets:
    """

    # Arrange
    source_markdown = """[link](<foo
bar>)"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):[:]",
        "[text(1,2):link:]",
        "[text(1,6):]:]",
        "[text(1,7):(:]",
        "[raw-html(1,8):foo\nbar]",
        "[text(2,5):):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[link](<foo
bar>)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_501():
    """
    Test case 501:  The destination can contain ) if it is enclosed in pointy brackets:
    """

    # Arrange
    source_markdown = """[a](<b)c>)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:b)c:::::a:True::::]",
        "[text(1,2):a:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="b)c">a</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_502():
    """
    Test case 502:  Pointy brackets that enclose links must be unescaped:
    """

    # Arrange
    source_markdown = """[link](<foo\\>)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):link:]",
        "[text(1,6):]:]",
        "[text(1,7):(\a<\a&lt;\afoo\\\b\a>\a&gt;\a):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[link](&lt;foo&gt;)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_503():
    """
    Test case 503:  These are not links, because the opening pointy bracket is not matched properly:
    """

    # Arrange
    source_markdown = """[a](<b)c
[a](<b)c>
[a](<b>c)"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):[:]",
        "[text(1,2):a:]",
        "[text(1,3):]:]",
        "[text(1,4):(\a<\a&lt;\ab)c\n::\n]",
        "[text(2,1):[:]",
        "[text(2,2):a:]",
        "[text(2,3):]:]",
        "[text(2,4):(\a<\a&lt;\ab)c\a>\a&gt;\a\n::\n]",
        "[text(3,1):[:]",
        "[text(3,2):a:]",
        "[text(3,3):]:]",
        "[text(3,4):(:]",
        "[raw-html(3,5):b]",
        "[text(3,8):c):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[a](&lt;b)c
[a](&lt;b)c&gt;
[a](<b>c)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_504():
    """
    Test case 504:  Parentheses inside the link destination may be escaped:
    """

    # Arrange
    source_markdown = """[link](\\(foo\\))"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:(foo)::\\(foo\\):::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="(foo)">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_505():
    """
    Test case 505:  Any number of parentheses are allowed without escaping, as long as they are balanced:
    """

    # Arrange
    source_markdown = """[link](foo(and(bar)))"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:foo(and(bar)):::::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="foo(and(bar))">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_506():
    """
    Test case 506:  (part 1) However, if you have unbalanced parentheses, you need to escape or use the <...> form:
    """

    # Arrange
    source_markdown = """[link](foo\\(and\\(bar\\))"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:foo(and(bar)::foo\\(and\\(bar\\):::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="foo(and(bar)">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_507():
    """
    Test case 507:  (part 2) However, if you have unbalanced parentheses, you need to escape or use the <...> form:
    """

    # Arrange
    source_markdown = """[link](<foo(and(bar)>)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:foo(and(bar):::::link:True::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="foo(and(bar)">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_507b():
    """
    Test case 507b:  variation of 507 without the angle brackets.
    """

    # Arrange
    source_markdown = """[link](foo(and(bar))"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):link:]",
        "[text(1,6):]:]",
        "[text(1,7):(foo(and(bar)):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[link](foo(and(bar))</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_507c():
    """
    Test case 507c:  variation of 507 without the angle brackets, and more open
    """

    # Arrange
    source_markdown = """[link](foo(and(b(ar))"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):link:]",
        "[text(1,6):]:]",
        "[text(1,7):(foo(and(b(ar)):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[link](foo(and(b(ar))</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_508():
    """
    Test case 508:  Parentheses and other symbols can also be escaped, as usual in Markdown:
    """

    # Arrange
    source_markdown = """[link](foo\\)\\:)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:foo):::foo\\)\\::::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="foo):">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_509():
    """
    Test case 509:  A link can contain fragment identifiers and queries:
    """

    # Arrange
    source_markdown = """[link](#fragment)

[link](http://example.com#fragment)

[link](http://example.com?foo=3#frag)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:#fragment:::::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):inline:http://example.com#fragment:::::link:False::::]",
        "[text(3,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[link(5,1):inline:http://example.com?foo=3#frag:::::link:False::::]",
        "[text(5,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="#fragment">link</a></p>
<p><a href="http://example.com#fragment">link</a></p>
<p><a href="http://example.com?foo=3#frag">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_510():
    """
    Test case 510:  Note that a backslash before a non-escapable character is just a backslash:
    """

    # Arrange
    source_markdown = """[link](foo\\bar)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:foo%5Cbar::foo\\bar:::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="foo%5Cbar">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_511():
    """
    Test case 511:  URL-escaping should be left alone inside the destination
    """

    # Arrange
    source_markdown = """[link](foo%20b&auml;)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:foo%20b%C3%A4::foo%20b&auml;:::link:False::::]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="foo%20b%C3%A4">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_512():
    """
    Test case 512:  Note that, because titles can often be parsed as destinations,
                    if you try to omit the destination and keep the title, you’ll
                    get unexpected results:
    """

    # Arrange
    source_markdown = """[link]("title")"""
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:%22title%22::"title":::link:False::::]',
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="%22title%22">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_513():
    """
    Test case 513:  Titles may be in single quotes, double quotes, or parentheses:
    """

    # Arrange
    source_markdown = """[link](/url "title")
[link](/url 'title')
[link](/url (title))"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        '[link(1,1):inline:/url:title::::link:False:":: :]',
        "[text(1,2):link:]",
        "[end-link::]",
        "[text(1,21):\n::\n]",
        "[link(2,1):inline:/url:title::::link:False:':: :]",
        "[text(2,2):link:]",
        "[end-link::]",
        "[text(2,21):\n::\n]",
        "[link(3,1):inline:/url:title::::link:False:(:: :]",
        "[text(3,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">link</a>
<a href="/url" title="title">link</a>
<a href="/url" title="title">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_514():
    """
    Test case 514:  Backslash escapes and entity and numeric character references may be used in titles:
    """

    # Arrange
    source_markdown = """[link](/url "title \\"&quot;")"""
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/url:title &quot;&quot;::title \\"&quot;::link:False:":: :]',
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title &quot;&quot;">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_515():
    """
    Test case 515:  Titles must be separated from the link using a whitespace.
                    Other Unicode whitespace like non-breaking space doesn’t work.
    """

    # Arrange
    source_markdown = """[link](/url\u00A0"title")"""
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/url%C2%A0%22title%22::/url\u00A0"title":::link:False::::]',
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url%C2%A0%22title%22">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_515b():
    """
    Test case 515b:  variation of 515 to use normal space and remove closing quotes.
    """

    # Arrange
    source_markdown = """[link](/url "title)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):link:]",
        "[text(1,6):]:]",
        '[text(1,7):(/url \a"\a&quot;\atitle):]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[link](/url &quot;title)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_515c():
    """
    Test case 515c:  variation of 515 to use normal space and remove closing quotes.
    """

    # Arrange
    source_markdown = """[link](/url (title))"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title::::link:False:(:: :]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_515d():
    """
    Test case 515d:  variation of 515 to use normal space and remove closing quotes.
    """

    # Arrange
    source_markdown = """[link](/url (title)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):link:]",
        "[text(1,6):]:]",
        "[text(1,7):(/url (title):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[link](/url (title)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_515e():
    """
    Test case 515e:  variation of 515 to use normal space and remove closing quotes.
    """

    # Arrange
    source_markdown = """[link](/url (title(other)line))"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title(other)line::::link:False:(:: :]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title(other)line">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_515f():
    """
    Test case 515e:  variation of 515 to use normal space and remove closing quotes.
    """

    # Arrange
    source_markdown = """[link](/url (title(other)line)) abc"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/url:title(other)line::::link:False:(:: :]",
        "[text(1,2):link:]",
        "[end-link::]",
        "[text(1,32): abc:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title(other)line">link</a> abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_515g():
    """
    Test case 515e:  variation of 515 to use normal space and remove closing quotes.
    """

    # Arrange
    source_markdown = """[link](/url (title(otherline) abc"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):link:]",
        "[text(1,6):]:]",
        "[text(1,7):(/url (title(otherline) abc:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[link](/url (title(otherline) abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_516():
    """
    Test case 516:  Nested balanced quotes are not allowed without escaping:
    """

    # Arrange
    source_markdown = """[link](/url "title "and" title")"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):link:]",
        "[text(1,6):]:]",
        '[text(1,7):(/url \a"\a&quot;\atitle \a"\a&quot;\aand\a"\a&quot;\a title\a"\a&quot;\a):]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[link](/url &quot;title &quot;and&quot; title&quot;)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_517():
    """
    Test case 517:  But it is easy to work around this by using a different quote type:
    """

    # Arrange
    source_markdown = """[link](/url 'title "and" title')"""
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/url:title &quot;and&quot; title::title "and" title::link:False:\':: :]',
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="/url" title="title &quot;and&quot; title">link</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_518():
    """
    Test case 518:  Whitespace is allowed around the destination and title:
    """

    # Arrange
    source_markdown = """[link](   /uri
  "title"  )"""
    expected_tokens = [
        "[para(1,1):\n  ]",
        '[link(1,1):inline:/uri:title::::link:False:":   :\n:  ]',
        "[text(1,2):link:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri" title="title">link</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_519():
    """
    Test case 519:  But it is not allowed between the link text and the following parenthesis:
    """

    # Arrange
    source_markdown = """[link] (/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):link:]",
        "[text(1,6):]:]",
        "[text(1,7): (/uri):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[link] (/uri)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_520():
    """
    Test case 520:  (part 1) The link text may contain balanced brackets, but not
                    unbalanced ones, unless they are escaped:
    """

    # Arrange
    source_markdown = """[link [foo [bar]]](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/uri:::::link [foo [bar]]:False::::]",
        "[text(1,2):link :]",
        "[text(1,7):[:]",
        "[text(1,8):foo :]",
        "[text(1,12):[:]",
        "[text(1,13):bar:]",
        "[text(1,16):]:]",
        "[text(1,17):]:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">link [foo [bar]]</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_521():
    """
    Test case 521:  (part 2) The link text may contain balanced brackets, but not
                    unbalanced ones, unless they are escaped:
    """

    # Arrange
    source_markdown = """[link] bar](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):link:]",
        "[text(1,6):]:]",
        "[text(1,7): bar:]",
        "[text(1,11):]:]",
        "[text(1,12):(/uri):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[link] bar](/uri)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_522():
    """
    Test case 522:  (part 3) The link text may contain balanced brackets, but not
                    unbalanced ones, unless they are escaped:
    """

    # Arrange
    source_markdown = """[link [bar](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):link :]",
        "[link(1,7):inline:/uri:::::bar:False::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[link <a href="/uri">bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_523():
    """
    Test case 523:  (part 4) The link text may contain balanced brackets, but not
                    unbalanced ones, unless they are escaped:
    """

    # Arrange
    source_markdown = """[link \\[bar](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/uri:::::link \\[bar:False::::]",
        "[text(1,2):link \\\b[bar:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">link [bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_524():
    """
    Test case 524:  (part 1) The link text may contain inline content:
    """

    # Arrange
    source_markdown = """[link *foo **bar** `#`*](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/uri:::::link *foo **bar** `#`*:False::::]",
        "[text(1,2):link :]",
        "[emphasis(1,7):1:*]",
        "[text(1,8):foo :]",
        "[emphasis(1,12):2:*]",
        "[text(1,14):bar:]",
        "[end-emphasis(1,17)::]",
        "[text(1,19): :]",
        "[icode-span(1,20):#:`::]",
        "[end-emphasis(1,23)::]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">link <em>foo <strong>bar</strong> <code>#</code></em></a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_525():
    """
    Test case 525:  (part 2) The link text may contain inline content:
    """

    # Arrange
    source_markdown = """[![moon](moon.jpg)](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/uri:::::![moon](moon.jpg):False::::]",
        "[image(1,2):inline:moon.jpg::moon::::moon:False::::]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri"><img src="moon.jpg" alt="moon" /></a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_526():
    """
    Test case 526:  (part 1) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    source_markdown = """[foo [bar](/uri)](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo :]",
        "[link(1,6):inline:/uri:::::bar:False::::]",
        "[text(1,7):bar:]",
        "[end-link::]",
        "[text(1,17):]:]",
        "[text(1,18):(/uri):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo <a href="/uri">bar</a>](/uri)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_526a():
    """
    Test case 526a:  variation of 526 to switch uris
    """

    # Arrange
    source_markdown = """[foo [bar](/uri1)](/uri2)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo :]",
        "[link(1,6):inline:/uri1:::::bar:False::::]",
        "[text(1,7):bar:]",
        "[end-link::]",
        "[text(1,18):]:]",
        "[text(1,19):(/uri2):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo <a href="/uri1">bar</a>](/uri2)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_527():
    """
    Test case 527:  (part 2) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    source_markdown = """[foo *[bar [baz](/uri)](/uri)*](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo :]",
        "[emphasis(1,6):1:*]",
        "[text(1,7):[:]",
        "[text(1,8):bar :]",
        "[link(1,12):inline:/uri:::::baz:False::::]",
        "[text(1,13):baz:]",
        "[end-link::]",
        "[text(1,23):]:]",
        "[text(1,24):(/uri):]",
        "[end-emphasis(1,30)::]",
        "[text(1,31):]:]",
        "[text(1,32):(/uri):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo <em>[bar <a href="/uri">baz</a>](/uri)</em>](/uri)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_527a():
    """
    Test case 527a:  variation of 527 to have multiple uris instead of one
    """

    # Arrange
    source_markdown = """[foo *[bar [baz](/uri1)](/uri2)*](/uri3)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo :]",
        "[emphasis(1,6):1:*]",
        "[text(1,7):[:]",
        "[text(1,8):bar :]",
        "[link(1,12):inline:/uri1:::::baz:False::::]",
        "[text(1,13):baz:]",
        "[end-link::]",
        "[text(1,24):]:]",
        "[text(1,25):(/uri2):]",
        "[end-emphasis(1,32)::]",
        "[text(1,33):]:]",
        "[text(1,34):(/uri3):]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>[foo <em>[bar <a href="/uri1">baz</a>](/uri2)</em>](/uri3)</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_528():
    """
    Test case 528:  (part 3) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    source_markdown = """![[[foo](uri1)](uri2)](uri3)"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:uri3::[foo](uri2)::::[[foo](uri1)](uri2):False::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="uri3" alt="[foo](uri2)" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_528a():
    """
    Test case 528a:  variation of 528 to have multuple uris instead of one
    """

    # Arrange
    source_markdown = """![[foo](uri2)](uri3)"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:uri3::foo::::[foo](uri2):False::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="uri3" alt="foo" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_528b():
    """
    Test case 528b:  variation of 528 to have a slightly different format
    """

    # Arrange
    source_markdown = """![[foo](uri2 "bar")](uri3)"""
    expected_tokens = [
        "[para(1,1):]",
        '[image(1,1):inline:uri3::foo::::[foo](uri2 "bar"):False::::]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="uri3" alt="foo" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_528c():
    """
    Test case 528c:  variation of 528 to have a slightly different format
    """

    # Arrange
    source_markdown = """![![[foo](uri1)](uri2)](uri3)"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:uri3::foo::::![[foo](uri1)](uri2):False::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="uri3" alt="foo" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_529():
    """
    Test case 529:  (part 1) These cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    source_markdown = """*[foo*](/uri)"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*:]",
        "[link(1,2):inline:/uri:::::foo*:False::::]",
        "[text(1,3):foo:]",
        "[text(1,6):*:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*<a href="/uri">foo*</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_530():
    """
    Test case 530:  (part 2) These cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    source_markdown = """[foo *bar](baz*)"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:baz*:::::foo *bar:False::::]",
        "[text(1,2):foo :]",
        "[text(1,6):*:]",
        "[text(1,7):bar:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="baz*">foo *bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_531():
    """
    Test case 531:  Note that brackets that aren’t part of links do not take precedence:
    """

    # Arrange
    source_markdown = """*foo [bar* baz]"""
    expected_tokens = [
        "[para(1,1):]",
        "[emphasis(1,1):1:*]",
        "[text(1,2):foo :]",
        "[text(1,6):[:]",
        "[text(1,7):bar:]",
        "[end-emphasis(1,10)::]",
        "[text(1,11): baz:]",
        "[text(1,15):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>foo [bar</em> baz]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_532():
    """
    Test case 532:  (part 1) These cases illustrate the precedence of HTML tags,
                    code spans, and autolinks over link grouping:
    """

    # Arrange
    source_markdown = """[foo <bar attr="](baz)">"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo :]",
        '[raw-html(1,6):bar attr="](baz)"]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo <bar attr="](baz)"></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_533():
    """
    Test case 533:  (part 2) These cases illustrate the precedence of HTML tags,
                    code spans, and autolinks over link grouping:
    """

    # Arrange
    source_markdown = """[foo`](/uri)`"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[icode-span(1,5):](/uri):`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo<code>](/uri)</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_534():
    """
    Test case 534:  (part 3) These cases illustrate the precedence of HTML tags,
                    code spans, and autolinks over link grouping:
    """

    # Arrange
    source_markdown = """[foo<http://example.com/?search=](uri)>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[uri-autolink(1,5):http://example.com/?search=](uri)]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo<a href="http://example.com/?search=%5D(uri)">http://example.com/?search=](uri)</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_extra_01():
    """
    Test case extra 01:  variation on 644
    """

    # Arrange
    source_markdown = """[foo <!-- this is a
comment - with hyphen --> bar](uri)"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[link(1,1):inline:uri:::::foo <!-- this is a\ncomment - with hyphen --> bar:False::::]",
        "[text(1,2):foo :]",
        "[raw-html(1,6):!-- this is a\ncomment - with hyphen --]",
        "[text(2,26): bar:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="uri">foo <!-- this is a
comment - with hyphen --> bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_extra_02():
    """
    Test case extra 02:  variation on 345
    """

    # Arrange
    source_markdown = """[foo ``
foo
bar\a\a
baz
`` bar](uri)""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n\n\n\n]",
        "[link(1,1):inline:uri:::::foo ``\nfoo\nbar  \nbaz\n`` bar:False::::]",
        "[text(1,2):foo :]",
        "[icode-span(1,6):foo\a\n\a \abar  \a\n\a \abaz:``:\a\n\a \a:\a\n\a \a]",
        "[text(5,3): bar:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="uri">foo <code>foo bar   baz</code> bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_extra_03x():
    """
    Test case extra 03:  from https://github.com/jackdewinter/pymarkdown/issues/634
    """

    # Arrange
    source_markdown = """1.  [Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture
    models](https://scikit-learn.org/stable/modules/mixture.html)"""
    expected_tokens = [
        "[olist(1,1):.:1:4::    ]",
        "[para(1,5):\n]",
        "[link(1,5):inline:https://scikit-learn.org/stable/modules/mixture.html:::::Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture\nmodels:False::::]",
        "[text(1,6):Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture\nmodels::\n]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li><a href="https://scikit-learn.org/stable/modules/mixture.html">Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture
models</a></li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_extra_03a():
    """
    Test case extra 03:  from https://github.com/jackdewinter/pymarkdown/issues/634
    """

    # Arrange
    source_markdown = """1.  Reference [Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture
    models](https://scikit-learn.org/stable/modules/mixture.html)"""
    expected_tokens = [
        "[olist(1,1):.:1:4::    ]",
        "[para(1,5):\n]",
        "[text(1,5):Reference :]",
        "[link(1,15):inline:https://scikit-learn.org/stable/modules/mixture.html:::::Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture\nmodels:False::::]",
        "[text(1,16):Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture\nmodels::\n]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Reference <a href="https://scikit-learn.org/stable/modules/mixture.html">Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture
models</a></li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_extra_03b():
    """
    Test case extra 03:  from https://github.com/jackdewinter/pymarkdown/issues/634
    """

    # Arrange
    source_markdown = """- [Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture
    models](https://scikit-learn.org/stable/modules/mixture.html)"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n  ]",
        "[link(1,3):inline:https://scikit-learn.org/stable/modules/mixture.html:::::Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture\nmodels:False::::]",
        "[text(1,4):Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture\nmodels::\n]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><a href="https://scikit-learn.org/stable/modules/mixture.html">Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture
models</a></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_extra_03c():
    """
    Test case extra 03:  from https://github.com/jackdewinter/pymarkdown/issues/634
    """

    # Arrange
    source_markdown = """1.  [Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture
    models](https://scikit-learn.org/stable/modules/mixture.html)
2.  [Bishop - Pattern Recognition and Machine Learning,
    p. 474ff.](http://users.isr.ist.utl.pt/~wurmd/Livros/school/Bishop%20-%20Pattern%20Recognition%20And%20Machine%20Learning%20-%20Springer%20%202006.pdf)"""
    expected_tokens = [
        "[olist(1,1):.:1:4::    \n    \n    ]",
        "[para(1,5):\n]",
        "[link(1,5):inline:https://scikit-learn.org/stable/modules/mixture.html:::::Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture\nmodels:False::::]",
        "[text(1,6):Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture\nmodels::\n]",
        "[end-link::]",
        "[end-para:::True]",
        "[li(3,1):4::2]",
        "[para(3,5):\n]",
        "[link(3,5):inline:http://users.isr.ist.utl.pt/~wurmd/Livros/school/Bishop%20-%20Pattern%20Recognition%20And%20Machine%20Learning%20-%20Springer%20%202006.pdf:::::Bishop - Pattern Recognition and Machine Learning,\np. 474ff.:False::::]",
        "[text(3,6):Bishop - Pattern Recognition and Machine Learning,\np. 474ff.::\n]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li><a href="https://scikit-learn.org/stable/modules/mixture.html">Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture
models</a></li>
<li><a href="http://users.isr.ist.utl.pt/~wurmd/Livros/school/Bishop%20-%20Pattern%20Recognition%20And%20Machine%20Learning%20-%20Springer%20%202006.pdf">Bishop - Pattern Recognition and Machine Learning,
p. 474ff.</a></li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_extra_03d():
    """
    Test case extra 03:  from https://github.com/jackdewinter/pymarkdown/issues/634
    """

    # Arrange
    source_markdown = """- [Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture
    models](https://scikit-learn.org/stable/modules/mixture.html)
- [Bishop - Pattern Recognition and Machine Learning,
  p. 474ff.](http://users.isr.ist.utl.pt/~wurmd/Livros/school/Bishop%20-%20Pattern%20Recognition%20And%20Machine%20Learning%20-%20Springer%20%202006.pdf)"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[para(1,3):\n  ]",
        "[link(1,3):inline:https://scikit-learn.org/stable/modules/mixture.html:::::Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture\nmodels:False::::]",
        "[text(1,4):Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture\nmodels::\n]",
        "[end-link::]",
        "[end-para:::True]",
        "[li(3,1):2::]",
        "[para(3,3):\n]",
        "[link(3,3):inline:http://users.isr.ist.utl.pt/~wurmd/Livros/school/Bishop%20-%20Pattern%20Recognition%20And%20Machine%20Learning%20-%20Springer%20%202006.pdf:::::Bishop - Pattern Recognition and Machine Learning,\np. 474ff.:False::::]",
        "[text(3,4):Bishop - Pattern Recognition and Machine Learning,\np. 474ff.::\n]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><a href="https://scikit-learn.org/stable/modules/mixture.html">Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture
models</a></li>
<li><a href="http://users.isr.ist.utl.pt/~wurmd/Livros/school/Bishop%20-%20Pattern%20Recognition%20And%20Machine%20Learning%20-%20Springer%20%202006.pdf">Bishop - Pattern Recognition and Machine Learning,
p. 474ff.</a></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_inline_links_extra_03e():
    """
    Test case extra 03:  from https://github.com/jackdewinter/pymarkdown/issues/634
    """

    # Arrange
    source_markdown = """- [Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture
    models](https://scikit-learn.org/stable/modules/mixture.html) ref
- [Bishop - Pattern Recognition and Machine Learning,
  p. 474ff.](http://users.isr.ist.utl.pt/~wurmd/Livros/school/Bishop%20-%20Pattern%20Recognition%20And%20Machine%20Learning%20-%20Springer%20%202006.pdf)"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[para(1,3):\n  ]",
        "[link(1,3):inline:https://scikit-learn.org/stable/modules/mixture.html:::::Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture\nmodels:False::::]",
        "[text(1,4):Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture\nmodels::\n]",
        "[end-link::]",
        "[text(2,64): ref:]",
        "[end-para:::True]",
        "[li(3,1):2::]",
        "[para(3,3):\n]",
        "[link(3,3):inline:http://users.isr.ist.utl.pt/~wurmd/Livros/school/Bishop%20-%20Pattern%20Recognition%20And%20Machine%20Learning%20-%20Springer%20%202006.pdf:::::Bishop - Pattern Recognition and Machine Learning,\np. 474ff.:False::::]",
        "[text(3,4):Bishop - Pattern Recognition and Machine Learning,\np. 474ff.::\n]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><a href="https://scikit-learn.org/stable/modules/mixture.html">Scikit-learn: Machine Learning in {P}ython} - Gaussian mixture
models</a> ref</li>
<li><a href="http://users.isr.ist.utl.pt/~wurmd/Livros/school/Bishop%20-%20Pattern%20Recognition%20And%20Machine%20Learning%20-%20Springer%20%202006.pdf">Bishop - Pattern Recognition and Machine Learning,
p. 474ff.</a></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
