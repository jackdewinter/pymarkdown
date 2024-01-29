"""
https://github.github.com/gfm/#links
"""

from test.utils import act_and_assert

import pytest


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_reference_links_535():
    """
    Test case 535:  Here is a simple example:
    """

    # Arrange
    source_markdown = """[foo][bar]

[bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/url:title:::bar:foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_535a():
    """
    Test case 535a:  variation of 535 with trailing space
    """

    # Arrange
    source_markdown = """[foo][bar]\a

[bar]: /url "title"
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):: ]",
        "[link(1,1):full:/url:title:::bar:foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_535b():
    """
    Test case 535b:  variation of 535 with trailing space and text
    """

    # Arrange
    source_markdown = """[foo][bar] abc

[bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/url:title:::bar:foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[text(1,11): abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a> abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_536():
    """
    Test case 536:  (part 1) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    source_markdown = """[link [foo [bar]]][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/uri::::ref:link [foo [bar]]:False::::]",
        "[text(1,2):link :]",
        "[text(1,7):[:]",
        "[text(1,8):foo :]",
        "[text(1,12):[:]",
        "[text(1,13):bar:]",
        "[text(1,16):]:]",
        "[text(1,17):]:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri">link [foo [bar]]</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_537():
    """
    Test case 537:  (part 2) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    source_markdown = """[link \\[bar][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/uri::::ref:link \\[bar:False::::]",
        "[text(1,2):link \\\b[bar:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri">link [bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_538():
    """
    Test case 538:  (part 1) The link text may contain inline content:
    """

    # Arrange
    source_markdown = """[link *foo **bar** `#`*][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/uri::::ref:link *foo **bar** `#`*:False::::]",
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
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri">link <em>foo <strong>bar</strong> <code>#</code></em></a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_539():
    """
    Test case 539:  (part 2) The link text may contain inline content:
    """

    # Arrange
    source_markdown = """[![moon](moon.jpg)][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/uri::::ref:![moon](moon.jpg):False::::]",
        "[image(1,2):inline:moon.jpg::moon::::moon:False::::]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri"><img src="moon.jpg" alt="moon" /></a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_540():
    """
    Test case 540:  (part 1) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    source_markdown = """[foo [bar](/uri)][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo :]",
        "[link(1,6):inline:/uri:::::bar:False::::]",
        "[text(1,7):bar:]",
        "[end-link::]",
        "[text(1,17):]:]",
        "[link(1,18):shortcut:/uri:::::ref:False::::]",
        "[text(1,19):ref:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p>[foo <a href="/uri">bar</a>]<a href="/uri">ref</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_541():
    """
    Test case 541:  (part 2) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    source_markdown = """[foo *bar [baz][ref]*][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo :]",
        "[emphasis(1,6):1:*]",
        "[text(1,7):bar :]",
        "[link(1,11):full:/uri::::ref:baz:False::::]",
        "[text(1,12):baz:]",
        "[end-link::]",
        "[end-emphasis(1,21)::]",
        "[text(1,22):]:]",
        "[link(1,23):shortcut:/uri:::::ref:False::::]",
        "[text(1,24):ref:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = (
        """<p>[foo <em>bar <a href="/uri">baz</a></em>]<a href="/uri">ref</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_542():
    """
    Test case 542:  (part 1) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    source_markdown = """*[foo*][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):*:]",
        "[link(1,2):full:/uri::::ref:foo*:False::::]",
        "[text(1,3):foo:]",
        "[text(1,6):*:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p>*<a href="/uri">foo*</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_543():
    """
    Test case 543:  (part 2) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    source_markdown = """[foo *bar][ref]*

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/uri::::ref:foo *bar:False::::]",
        "[text(1,2):foo :]",
        "[text(1,6):*:]",
        "[text(1,7):bar:]",
        "[end-link::]",
        "[text(1,16):*:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri">foo *bar</a>*</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_544():
    """
    Test case 544:  (part 1) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    source_markdown = """[foo <bar attr="][ref]">

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo :]",
        '[raw-html(1,6):bar attr="][ref]"]',
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p>[foo <bar attr="][ref]"></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_545():
    """
    Test case 545:  (part 2) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    source_markdown = """[foo`][ref]`

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[icode-span(1,5):][ref]:`::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p>[foo<code>][ref]</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_546():
    """
    Test case 546:  (part 3) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    source_markdown = """[foo<http://example.com/?search=][ref]>

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[uri-autolink(1,5):http://example.com/?search=][ref]]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p>[foo<a href="http://example.com/?search=%5D%5Bref%5D">http://example.com/?search=][ref]</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_547():
    """
    Test case 547:  Matching is case-insensitive:
    """

    # Arrange
    source_markdown = """[foo][BaR]

[bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/url:title:::BaR:foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_548():
    """
    Test case 548:  Unicode case fold is used:
    """

    # Arrange
    source_markdown = """[ẞ]

[SS]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::ẞ:False::::]",
        "[text(1,2):ẞ:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ss:SS: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">ẞ</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_549():
    """
    Test case 549:  Consecutive internal whitespace is treated as one space for purposes of determining matching:
    """

    # Arrange
    source_markdown = """[Foo
  bar]: /url

[Baz][Foo bar]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo bar:Foo\n  bar: :/url:::::]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[link(4,1):full:/url::::Foo bar:Baz:False::::]",
        "[text(4,2):Baz:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">Baz</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_549ax():
    """
    Test case 549:  variant
    """

    # Arrange
    source_markdown = """[ Foo  bar ]: /url

[Baz][Foo bar]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo bar: Foo  bar : :/url:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):full:/url::::Foo bar:Baz:False::::]",
        "[text(3,2):Baz:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">Baz</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_549aa():
    """
    Test case 549:  variant
    """

    # Arrange
    source_markdown = """[\x0cFoo\x0c\x0cbar\x0c]: /url

[Baz][Foo bar]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo bar:\x0cFoo\x0c\x0cbar\x0c: :/url:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):full:/url::::Foo bar:Baz:False::::]",
        "[text(3,2):Baz:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">Baz</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_549bx():
    """
    Test case 549:  variant
    """

    # Arrange
    source_markdown = """[Foo bar]: /url

[Baz][ Foo  bar ]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo bar:Foo bar: :/url:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):full:/url:::: Foo  bar :Baz:False::::]",
        "[text(3,2):Baz:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">Baz</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_549ba():
    """
    Test case 549:  variant
    """

    # Arrange
    source_markdown = """[Foo bar]: /url

[Baz][\x0cFoo\x0c\x0cbar\x0c]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo bar:Foo bar: :/url:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):full:/url::::\x0cFoo\x0c\x0cbar\x0c:Baz:False::::]",
        "[text(3,2):Baz:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">Baz</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_549c():
    """
    Test case 549:  variant
    """

    # Arrange
    source_markdown = """[Foo bar]: /url

[Baz][\u00a0Foo  bar ]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo bar:Foo bar: :/url:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):Baz:]",
        "[text(3,5):]:]",
        "[text(3,6):[:]",
        "[text(3,7):\u00a0Foo  bar :]",
        "[text(3,17):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[Baz][\u00a0Foo  bar ]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_549d():
    """
    Test case 549:  variant
    """

    # Arrange
    source_markdown = """[Foo bar]: /url

[Baz][ Foo  bar\u00a0]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo bar:Foo bar: :/url:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):Baz:]",
        "[text(3,5):]:]",
        "[text(3,6):[:]",
        "[text(3,7): Foo  bar\u00a0:]",
        "[text(3,17):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[Baz][ Foo  bar\u00a0]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_549e():
    """
    Test case 549:  variant
    """

    # Arrange
    source_markdown = """[Foo bar]: /url

[Baz][ Foo\u00a0\u00a0bar ]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo bar:Foo bar: :/url:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):Baz:]",
        "[text(3,5):]:]",
        "[text(3,6):[:]",
        "[text(3,7): Foo\u00a0\u00a0bar :]",
        "[text(3,17):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[Baz][ Foo\u00a0\u00a0bar ]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_550():
    """
    Test case 550:  (part 1) No whitespace is allowed between the link text and the link label:
    """

    # Arrange
    source_markdown = """[foo] [bar]

[bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        "[text(1,6): :]",
        "[link(1,7):shortcut:/url:title::::bar:False::::]",
        "[text(1,8):bar:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>[foo] <a href="/url" title="title">bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_551():
    """
    Test case 551:  (part 2) No whitespace is allowed between the link text and the link label:
    """

    # Arrange
    source_markdown = """[foo]
[bar]

[bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        "[text(1,6):\n::\n]",
        "[link(2,1):shortcut:/url:title::::bar:False::::]",
        "[text(2,2):bar:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        '[link-ref-def(4,1):True::bar:: :/url:: :title:"title":]',
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<p>[foo]
<a href="/url" title="title">bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_552():
    """
    Test case 552:  When there are multiple matching link reference definitions, the first is used:
    """

    # Arrange
    source_markdown = """[foo]: /url1

[foo]: /url2

[bar][foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url1:::::]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):False::foo:: :/url2:::::]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[link(5,1):full:/url1::::foo:bar:False::::]",
        "[text(5,2):bar:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url1">bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_553():
    """
    Test case 553:  Note that matching is performed on normalized strings, not parsed inline content. So the following does not match, even though the labels define equivalent inline content:
    """

    # Arrange
    source_markdown = """[bar][foo\\!]

[foo!]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):bar:]",
        "[text(1,5):]:]",
        "[text(1,6):[:]",
        "[text(1,7):foo\\\b!:]",
        "[text(1,12):]:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo!:: :/url:::::]",
    ]
    expected_gfm = """<p>[bar][foo!]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_554():
    """
    Test case 554:  (part 1) Link labels cannot contain brackets, unless they are backslash-escaped:
    """

    # Arrange
    source_markdown = """[foo][ref[]

[ref[]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        "[text(1,6):[:]",
        "[text(1,7):ref:]",
        "[text(1,10):[:]",
        "[text(1,11):]:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):ref:]",
        "[text(3,5):[:]",
        "[text(3,6):]:]",
        "[text(3,7):: /uri:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo][ref[]</p>
<p>[ref[]: /uri</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_555():
    """
    Test case 555:  (part 2) Link labels cannot contain brackets, unless they are backslash-escaped:
    """

    # Arrange
    source_markdown = """[foo][ref[bar]]

[ref[bar]]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        "[text(1,6):[:]",
        "[text(1,7):ref:]",
        "[text(1,10):[:]",
        "[text(1,11):bar:]",
        "[text(1,14):]:]",
        "[text(1,15):]:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):ref:]",
        "[text(3,5):[:]",
        "[text(3,6):bar:]",
        "[text(3,9):]:]",
        "[text(3,10):]:]",
        "[text(3,11):: /uri:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo][ref[bar]]</p>
<p>[ref[bar]]: /uri</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_556():
    """
    Test case 556:  (part 3) Link labels cannot contain brackets, unless they are backslash-escaped:
    """

    # Arrange
    source_markdown = """[[[foo]]]

[[[foo]]]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):[:]",
        "[text(1,3):[:]",
        "[text(1,4):foo:]",
        "[text(1,7):]:]",
        "[text(1,8):]:]",
        "[text(1,9):]:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):[:]",
        "[text(3,3):[:]",
        "[text(3,4):foo:]",
        "[text(3,7):]:]",
        "[text(3,8):]:]",
        "[text(3,9):]:]",
        "[text(3,10):: /url:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[[[foo]]]</p>
<p>[[[foo]]]: /url</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_557():
    """
    Test case 557:  (part 4) Link labels cannot contain brackets, unless they are backslash-escaped:
    """

    # Arrange
    source_markdown = """[foo][ref\\[]

[ref\\[]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/uri::::ref\\[:foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref\\[:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_558():
    """
    Test case 558:  Note that in this example ] is not backslash-escaped:
    """

    # Arrange
    source_markdown = """[bar\\\\]: /uri

[bar\\\\]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar\\\\:: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/uri:::::bar\\\\:False::::]",
        "[text(3,2):bar\\\b\\:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar\\</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_558a():
    """
    Test case 558a:  variation of 558 with reference
    """

    # Arrange
    source_markdown = """[bar&#x5C;]: /uri

[bar&#x5C;]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar&#x5c;:bar&#x5C;: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/uri:::::bar&#x5C;:False::::]",
        "[text(3,2):bar\a&#x5C;\a\\\a:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar\\</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_558b():
    """
    Test case 558b:  variation of 558 with reference
    """

    # Arrange
    source_markdown = """[bar&beta;]: /uri

[bar&beta;]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar&beta;:: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/uri:::::bar&beta;:False::::]",
        "[text(3,2):bar\a&beta;\aβ\a:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">barβ</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_559():
    """
    Test case 559:  (part 1) A link label must contain at least one non-whitespace character:
    """

    # Arrange
    source_markdown = """[]

[]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):]:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):]:]",
        "[text(3,3):: /uri:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[]</p>
<p>[]: /uri</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_560():
    """
    Test case 560:  (part 2) A link label must contain at least one non-whitespace character:
    """

    # Arrange
    source_markdown = """[
 ]

[
 ]: /uri"""
    expected_tokens = [
        "[para(1,1):\n ]",
        "[text(1,1):[:]",
        "[text(1,2):\n::\n]",
        "[text(2,2):]:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):\n ]",
        "[text(4,1):[:]",
        "[text(4,2):\n::\n]",
        "[text(5,2):]:]",
        "[text(5,3):: /uri:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[
]</p>
<p>[
]: /uri</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_561():
    """
    Test case 561:  (part 1) Thus, [foo][] is equivalent to [foo][foo].
    """

    # Arrange
    source_markdown = """[foo][]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):collapsed:/url:title::::foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_562():
    """
    Test case 562:  (part 2) Thus, [foo][] is equivalent to [foo][foo].
    """

    # Arrange
    source_markdown = """[*foo* bar][]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):collapsed:/url:title::::*foo* bar:False::::]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):foo:]",
        "[end-emphasis(1,6)::]",
        "[text(1,7): bar:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::*foo* bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title"><em>foo</em> bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_563():
    """
    Test case 563:  The link labels are case-insensitive:
    """

    # Arrange
    source_markdown = """[Foo][]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):collapsed:/url:title::::Foo:False::::]",
        "[text(1,2):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_564():
    """
    Test case 564:  As with full reference links, whitespace is not allowed between the two sets of brackets:
    """

    # Arrange
    source_markdown = """[foo]\a
[]

[foo]: /url "title"
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[link(1,1):shortcut:/url:title::::foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[text(1,6):\n:: \n]",
        "[text(2,1):[:]",
        "[text(2,2):]:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        '[link-ref-def(4,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a> 
[]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_565():
    """
    Test case 565:  (part 1) A shortcut reference link consists of a link label that matches a link reference definition elsewhere in the document and is not followed by [] or a link label.
    """

    # Arrange
    source_markdown = """[foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:title::::foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_566():
    """
    Test case 566:  (part 2) A shortcut reference link consists of a link label that matches a link reference definition elsewhere in the document and is not followed by [] or a link label.
    """

    # Arrange
    source_markdown = """[*foo* bar]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:title::::*foo* bar:False::::]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):foo:]",
        "[end-emphasis(1,6)::]",
        "[text(1,7): bar:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::*foo* bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title"><em>foo</em> bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_567():
    """
    Test case 567:  (part 3) A shortcut reference link consists of a link label that matches a link reference definition elsewhere in the document and is not followed by [] or a link label.
    """

    # Arrange
    source_markdown = """[[*foo* bar]]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[link(1,2):shortcut:/url:title::::*foo* bar:False::::]",
        "[emphasis(1,3):1:*]",
        "[text(1,4):foo:]",
        "[end-emphasis(1,7)::]",
        "[text(1,8): bar:]",
        "[end-link::]",
        "[text(1,13):]:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::*foo* bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>[<a href="/url" title="title"><em>foo</em> bar</a>]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_568():
    """
    Test case 568:  (part 4) A shortcut reference link consists of a link label that matches a link reference definition elsewhere in the document and is not followed by [] or a link label.
    """

    # Arrange
    source_markdown = """[[bar [foo]

[foo]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):[:]",
        "[text(1,3):bar :]",
        "[link(1,7):shortcut:/url:::::foo:False::::]",
        "[text(1,8):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :/url:::::]",
    ]
    expected_gfm = """<p>[[bar <a href="/url">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_569():
    """
    Test case 569:  The link labels are case-insensitive:
    """

    # Arrange
    source_markdown = """[Foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:title::::Foo:False::::]",
        "[text(1,2):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_570():
    """
    Test case 570:  A space after the link text should be preserved:
    """

    # Arrange
    source_markdown = """[foo] bar

[foo]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[text(1,6): bar:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">foo</a> bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_570a():
    """
    Test case 570a:  variation of 570 to show how link inside of link doesn't work.
    """

    # Arrange
    source_markdown = """[foo[foo]]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[link(1,5):shortcut:/url:title::::foo:False::::]",
        "[text(1,6):foo:]",
        "[end-link::]",
        "[text(1,10):]:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>[foo<a href=\"/url\" title=\"title\">foo</a>]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_571():
    """
    Test case 571:  If you just want bracketed text, you can backslash-escape the opening bracket to avoid links
    """

    # Arrange
    source_markdown = """\\[foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b[foo:]",
        "[text(1,6):]:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_572():
    """
    Test case 572:  Note that this is a link, because a link label ends with the first following closing bracket:
    """

    # Arrange
    source_markdown = """[foo*]: /url

*[foo*]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo*:: :/url:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):*:]",
        "[link(3,2):shortcut:/url:::::foo*:False::::]",
        "[text(3,3):foo:]",
        "[text(3,6):*:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*<a href="/url">foo*</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_573():
    """
    Test case 573:  (part 1) Full and compact references take precedence over shortcut references:
    """

    # Arrange
    source_markdown = """[foo][bar]

[foo]: /url1
[bar]: /url2"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/url2::::bar:foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :/url1:::::]",
        "[link-ref-def(4,1):True::bar:: :/url2:::::]",
    ]
    expected_gfm = """<p><a href="/url2">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_574():
    """
    Test case 574:  (part 2) Full and compact references take precedence over shortcut references:
    """

    # Arrange
    source_markdown = """[foo][]

[foo]: /url1"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):collapsed:/url1:::::foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :/url1:::::]",
    ]
    expected_gfm = """<p><a href="/url1">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_575():
    """
    Test case 575:  (part 1) Inline links also take precedence:
    """

    # Arrange
    source_markdown = """[foo]()

[foo]: /url1"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline::::::foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :/url1:::::]",
    ]
    expected_gfm = """<p><a href="">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_576():
    """
    Test case 576:  (part 2) Inline links also take precedence:
    """

    # Arrange
    source_markdown = """[foo](not a link)

[foo]: /url1"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url1:::::foo:False::: :]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[text(1,6):(not a link):]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :/url1:::::]",
    ]
    expected_gfm = """<p><a href="/url1">foo</a>(not a link)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_577():
    """
    Test case 577:  In the following case [bar][baz] is parsed as a reference, [foo] as normal text:
    """

    # Arrange
    source_markdown = """[foo][bar][baz]

[baz]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        "[link(1,6):full:/url::::baz:bar:False::::]",
        "[text(1,7):bar:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::baz:: :/url:::::]",
    ]
    expected_gfm = """<p>[foo]<a href="/url">bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_578():
    """
    Test case 578:  Here, though, [foo][bar] is parsed as a reference, since [bar] is defined:
    """

    # Arrange
    source_markdown = """[foo][bar][baz]

[baz]: /url1
[bar]: /url2"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/url2::::bar:foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[link(1,11):shortcut:/url1:::::baz:False::::]",
        "[text(1,12):baz:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::baz:: :/url1:::::]",
        "[link-ref-def(4,1):True::bar:: :/url2:::::]",
    ]
    expected_gfm = """<p><a href="/url2">foo</a><a href="/url1">baz</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_579():
    """
    Test case 579:  Here [foo] is not parsed as a shortcut reference, because it is followed by a link label (even though [bar] is not defined):
    """

    # Arrange
    source_markdown = """[foo][bar][baz]

[baz]: /url1
[foo]: /url2"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        "[link(1,6):full:/url1::::baz:bar:False::::]",
        "[text(1,7):bar:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::baz:: :/url1:::::]",
        "[link-ref-def(4,1):True::foo:: :/url2:::::]",
    ]
    expected_gfm = """<p>[foo]<a href="/url1">bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_01():
    """
    Test case extra 01:  variation on 644
    """

    # Arrange
    source_markdown = """[foo <!-- this is a
comment - with hyphen --> bar]: /uri

[foo <!-- this is a
comment - with hyphen --> bar]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo <!-- this is a comment - with hyphen --> bar:foo <!-- this is a\ncomment - with hyphen --> bar: :/uri:::::]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[link(4,1):shortcut:/uri:::::foo <!-- this is a\ncomment - with hyphen --> bar:False::::]",
        "[text(4,2):foo :]",
        "[raw-html(4,6):!-- this is a\ncomment - with hyphen --]",
        "[text(5,26): bar:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">foo <!-- this is a
comment - with hyphen --> bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_02():
    """
    Test case extra 02:  variation on 345
    """

    # Arrange
    source_markdown = """[foo ``
foo
bar\a\a
baz
`` bar]: /uri

[foo ``
foo
bar\a\a
baz
`` bar]""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[link-ref-def(1,1):True::foo `` foo bar baz `` bar:foo ``\nfoo\nbar  \nbaz\n`` bar: :/uri:::::]",
        "[BLANK(6,1):]",
        "[para(7,1):\n\n\n\n]",
        "[link(7,1):shortcut:/uri:::::foo ``\nfoo\nbar  \nbaz\n`` bar:False::::]",
        "[text(7,2):foo :]",
        "[icode-span(7,6):foo\a\n\a \abar  \a\n\a \abaz:``:\a\n\a \a:\a\n\a \a]",
        "[text(11,3): bar:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">foo <code>foo bar   baz</code> bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03x():
    """
    Test case extra 03x:  variation on 558
    """

    # Arrange
    source_markdown = """[bar\\foo]: /uri

[bar\\foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar\\foo:: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/uri:::::bar\\foo:False::::]",
        "[text(3,2):bar\\foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar\\foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03xa():
    """
    Test case extra 03xa:  variation of 3 with extra text in label
    """

    # Arrange
    source_markdown = """[xx[bar\\foo]yy](/uri)

[bar\\foo]: /uri1"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):xx:]",
        "[link(1,4):shortcut:/uri1:::::bar\\foo:False::::]",
        "[text(1,5):bar\\foo:]",
        "[end-link::]",
        "[text(1,13):yy:]",
        "[text(1,15):]:]",
        "[text(1,16):(/uri):]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar\\foo:: :/uri1:::::]",
    ]
    expected_gfm = """<p>[xx<a href="/uri1">bar\\foo</a>yy](/uri)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03xb():
    """
    Test case extra 03xb:  variation of 3xa as image
    """

    # Arrange
    source_markdown = """![xx[bar\\foo]yy](/uri)

[bar\\foo]: /uri1"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:/uri::xxbar\\fooyy::::xx[bar\\foo]yy:False::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar\\foo:: :/uri1:::::]",
    ]
    expected_gfm = """<p><img src="/uri" alt="xxbar\\fooyy" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03xc():
    """
    Test case extra 03xc:  variation of 3xa with inner as image
    """

    # Arrange
    source_markdown = """[xx![bar\\foo]yy](/uri)

[bar\\foo]: /uri1"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/uri:::::xx![bar\\foo]yy:False::::]",
        "[text(1,2):xx:]",
        "[image(1,4):shortcut:/uri1::bar\\foo::::bar\\foo:False::::]",
        "[text(1,14):yy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar\\foo:: :/uri1:::::]",
    ]
    expected_gfm = (
        """<p><a href="/uri">xx<img src="/uri1" alt="bar\\foo" />yy</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03a():
    """
    Test case extra 03a:  variation of 3 with reference
    """

    # Arrange
    source_markdown = """[bar&amp;foo]: /uri

[bar&amp;foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar&amp;foo:: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/uri:::::bar&amp;foo:False::::]",
        "[text(3,2):bar\a&amp;\a\a&\a&amp;\a\afoo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar&amp;foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03aa():
    """
    Test case extra 03aa:  variation of 3a with extra text
    """

    # Arrange
    source_markdown = """[xx[bar&amp;foo]yy](/uri1)

[bar&amp;foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):xx:]",
        "[link(1,4):shortcut:/uri:::::bar&amp;foo:False::::]",
        "[text(1,5):bar\a&amp;\a\a&\a&amp;\a\afoo:]",
        "[end-link::]",
        "[text(1,17):yy:]",
        "[text(1,19):]:]",
        "[text(1,20):(/uri1):]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar&amp;foo:: :/uri:::::]",
    ]
    expected_gfm = """<p>[xx<a href="/uri">bar&amp;foo</a>yy](/uri1)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03ab():
    """
    Test case extra 03ab:  variation of 3a with outer image
    """

    # Arrange
    source_markdown = """![xx[bar&amp;foo]yy](/uri1)

[bar&amp;foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:/uri1::xxbar&amp;fooyy::::xx[bar&amp;foo]yy:False::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar&amp;foo:: :/uri:::::]",
    ]
    expected_gfm = """<p><img src="/uri1" alt="xxbar&amp;fooyy" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03ac():
    """
    Test case extra 03ac:  variation of 3a with inner image
    """

    # Arrange
    source_markdown = """[xx![bar&lt;&amp;&gt;foo]yy](/uri1)

[bar&lt;&amp;&gt;foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/uri1:::::xx![bar&lt;&amp;&gt;foo]yy:False::::]",
        "[text(1,2):xx:]",
        "[image(1,4):shortcut:/uri::bar&lt;&amp;&gt;foo::::bar&lt;&amp;&gt;foo:False::::]",
        "[text(1,26):yy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar&lt;&amp;&gt;foo:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri1">xx<img src="/uri" alt="bar&lt;&amp;&gt;foo" />yy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03b():
    """
    Test case extra 03b:  variation of 3 with copyright
    """

    # Arrange
    source_markdown = """[bar&copy;foo]: /uri

[bar&copy;foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar&copy;foo:: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/uri:::::bar&copy;foo:False::::]",
        "[text(3,2):bar\a&copy;\a©\afoo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar©foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03ba():
    """
    Test case extra 03ba:  variation of 3b with text
    """

    # Arrange
    source_markdown = """[bar&copy;foo]: /uri

[xx[bar&copy;foo]yy](/uri1)"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar&copy;foo:: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):xx:]",
        "[link(3,4):shortcut:/uri:::::bar&copy;foo:False::::]",
        "[text(3,5):bar\a&copy;\a©\afoo:]",
        "[end-link::]",
        "[text(3,18):yy:]",
        "[text(3,20):]:]",
        "[text(3,21):(/uri1):]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[xx<a href="/uri">bar©foo</a>yy](/uri1)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03bb():
    """
    Test case extra 03bb:  variation of 3b with outer image
    """

    # Arrange
    source_markdown = """[bar&copy;foo]: /uri

![xx[bar&copy;foo]yy](/uri1)"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar&copy;foo:: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[image(3,1):inline:/uri1::xxbar©fooyy::::xx[bar&copy;foo]yy:False::::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><img src="/uri1" alt="xxbar©fooyy" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03bc():
    """
    Test case extra 03bc:  variation of 3b with inner image
    """

    # Arrange
    source_markdown = """[bar&copy;foo]: /uri

[xx![bar&copy;foo]yy](/uri1)"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar&copy;foo:: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):inline:/uri1:::::xx![bar&copy;foo]yy:False::::]",
        "[text(3,2):xx:]",
        "[image(3,4):shortcut:/uri::bar©foo::::bar&copy;foo:False::::]",
        "[text(3,19):yy:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri1">xx<img src="/uri" alt="bar©foo" />yy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03c():
    """
    Test case extra 03c:  variation of 3 with code span
    """

    # Arrange
    source_markdown = """[bar` span `foo]: /uri

[bar` span `foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar` span `foo:: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/uri:::::bar` span `foo:False::::]",
        "[text(3,2):bar:]",
        "[icode-span(3,5):span:`: : ]",
        "[text(3,13):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar<code>span</code>foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03ca():
    """
    Test case extra 03ca:  variation of 3c with text
    """

    # Arrange
    source_markdown = """[xx[bar` span `foo]yy](/uri1)

[bar` span `foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):xx:]",
        "[link(1,4):shortcut:/uri:::::bar` span `foo:False::::]",
        "[text(1,5):bar:]",
        "[icode-span(1,8):span:`: : ]",
        "[text(1,16):foo:]",
        "[end-link::]",
        "[text(1,20):yy:]",
        "[text(1,22):]:]",
        "[text(1,23):(/uri1):]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar` span `foo:: :/uri:::::]",
    ]
    expected_gfm = """<p>[xx<a href="/uri">bar<code>span</code>foo</a>yy](/uri1)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03cb():
    """
    Test case extra 03cb:  variation of 3c with outer image
    """

    # Arrange
    source_markdown = """![xx[bar` span `foo]yy](/uri1)

[bar` span `foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:/uri1::xxbarspanfooyy::::xx[bar` span `foo]yy:False::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar` span `foo:: :/uri:::::]",
    ]
    expected_gfm = """<p><img src="/uri1" alt="xxbarspanfooyy" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03cc():
    """
    Test case extra 03cc:  variation of 3c with inner image
    """

    # Arrange
    source_markdown = """[xx![bar` span `foo]yy](/uri1)

[bar` span `foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/uri1:::::xx![bar` span `foo]yy:False::::]",
        "[text(1,2):xx:]",
        "[image(1,4):shortcut:/uri::barspanfoo::::bar` span `foo:False::::]",
        "[text(1,21):yy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar` span `foo:: :/uri:::::]",
    ]
    expected_gfm = (
        """<p><a href="/uri1">xx<img src="/uri" alt="barspanfoo" />yy</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03d():
    """
    Test case extra 03d:  variation of 3 with emphasis
    """

    # Arrange
    source_markdown = """[bar*span*foo]: /uri

[bar*span*foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar*span*foo:: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/uri:::::bar*span*foo:False::::]",
        "[text(3,2):bar:]",
        "[emphasis(3,5):1:*]",
        "[text(3,6):span:]",
        "[end-emphasis(3,10)::]",
        "[text(3,11):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar<em>span</em>foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03da():
    """
    Test case extra 03da:  variation of 3d with text
    """

    # Arrange
    source_markdown = """[xx[bar*span*foo]yy](/uri1)

[bar*span*foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):xx:]",
        "[link(1,4):shortcut:/uri:::::bar*span*foo:False::::]",
        "[text(1,5):bar:]",
        "[emphasis(1,8):1:*]",
        "[text(1,9):span:]",
        "[end-emphasis(1,13)::]",
        "[text(1,14):foo:]",
        "[end-link::]",
        "[text(1,18):yy:]",
        "[text(1,20):]:]",
        "[text(1,21):(/uri1):]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar*span*foo:: :/uri:::::]",
    ]
    expected_gfm = """<p>[xx<a href="/uri">bar<em>span</em>foo</a>yy](/uri1)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03db():
    """
    Test case extra 03db:  variation of 3d with outer image
    """

    # Arrange
    source_markdown = """![xx[bar*span*foo]yy](/uri1)

[bar*span*foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:/uri1::xxbarspanfooyy::::xx[bar*span*foo]yy:False::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar*span*foo:: :/uri:::::]",
    ]
    expected_gfm = """<p><img src="/uri1" alt="xxbarspanfooyy" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03dc():
    """
    Test case extra 03dc:  variation of 3d with inner image
    """

    # Arrange
    source_markdown = """[xx![bar*span*foo]yy](/uri1)

[bar*span*foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/uri1:::::xx![bar*span*foo]yy:False::::]",
        "[text(1,2):xx:]",
        "[image(1,4):shortcut:/uri::barspanfoo::::bar*span*foo:False::::]",
        "[text(1,19):yy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar*span*foo:: :/uri:::::]",
    ]
    expected_gfm = (
        """<p><a href="/uri1">xx<img src="/uri" alt="barspanfoo" />yy</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03e():
    """
    Test case extra 03e:  variation of 3 with autolink
    """

    # Arrange
    source_markdown = """[bar<http://autolink.com>foo]: /uri

[bar<http://autolink.com>foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar<http://autolink.com>foo:: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/uri:::::bar<http://autolink.com>foo:False::::]",
        "[text(3,2):bar:]",
        "[uri-autolink(3,5):http://autolink.com]",
        "[text(3,26):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar<a href="http://autolink.com">http://autolink.com</a>foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03ea():
    """
    Test case extra 03ea:  variation of 3e with text
    """

    # Arrange
    source_markdown = """[xx[bar<http://autolink.com>foo]yy](/uri1)

[bar<http://autolink.com>foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):xx:]",
        "[link(1,4):shortcut:/uri:::::bar<http://autolink.com>foo:False::::]",
        "[text(1,5):bar:]",
        "[uri-autolink(1,8):http://autolink.com]",
        "[text(1,29):foo:]",
        "[end-link::]",
        "[text(1,33):yy:]",
        "[text(1,35):]:]",
        "[text(1,36):(/uri1):]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar<http://autolink.com>foo:: :/uri:::::]",
    ]
    expected_gfm = """<p>[xx<a href="/uri">bar<a href="http://autolink.com">http://autolink.com</a>foo</a>yy](/uri1)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03eb():
    """
    Test case extra 03eb:  variation of 3e with outer image
    """

    # Arrange
    source_markdown = """![xx[bar<http://autolink.com>foo]yy](/uri1)

[bar<http://autolink.com>foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[image(1,1):inline:/uri1::xxbarhttp://autolink.comfooyy::::xx[bar<http://autolink.com>foo]yy:False::::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar<http://autolink.com>foo:: :/uri:::::]",
    ]
    expected_gfm = """<p><img src="/uri1" alt="xxbarhttp://autolink.comfooyy" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03ec():
    """
    Test case extra 03ec:  variation of 3e with inner image
    """

    # Arrange
    source_markdown = """[xx![bar<http://autolink.com>foo]yy](/uri1)

[bar<http://autolink.com>foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):inline:/uri1:::::xx![bar<http://autolink.com>foo]yy:False::::]",
        "[text(1,2):xx:]",
        "[image(1,4):shortcut:/uri::barhttp://autolink.comfoo::::bar<http://autolink.com>foo:False::::]",
        "[text(1,34):yy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::bar<http://autolink.com>foo:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri1">xx<img src="/uri" alt="barhttp://autolink.comfoo" />yy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03f():
    """
    Test case extra 03f:  variation of 3 with raw html
    """

    # Arrange
    source_markdown = """[bar<image src="xx">foo]: /uri

[bar<image src="xx">foo]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::bar<image src="xx">foo:: :/uri:::::]',
        "[BLANK(2,1):]",
        "[para(3,1):]",
        '[link(3,1):shortcut:/uri:::::bar<image src="xx">foo:False::::]',
        "[text(3,2):bar:]",
        '[raw-html(3,5):image src="xx"]',
        "[text(3,21):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar<image src="xx">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03fa():
    """
    Test case extra 03fa:  variation of 3f with text
    """

    # Arrange
    source_markdown = """[xx[bar<image src="xx">foo]yy](/uri1)

[bar<image src="xx">foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):xx:]",
        '[link(1,4):shortcut:/uri:::::bar<image src="xx">foo:False::::]',
        "[text(1,5):bar:]",
        '[raw-html(1,8):image src="xx"]',
        "[text(1,24):foo:]",
        "[end-link::]",
        "[text(1,28):yy:]",
        "[text(1,30):]:]",
        "[text(1,31):(/uri1):]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::bar<image src="xx">foo:: :/uri:::::]',
    ]
    expected_gfm = """<p>[xx<a href="/uri">bar<image src="xx">foo</a>yy](/uri1)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03fb():
    """
    Test case extra 03fb:  variation of 3f with outer image
    """

    # Arrange
    source_markdown = """![xx[bar<image src="xx">foo]yy](/uri1)

[bar<image src="xx">foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        '[image(1,1):inline:/uri1::xxbar<image src="xx">fooyy::::xx[bar<image src="xx">foo]yy:False::::]',
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::bar<image src="xx">foo:: :/uri:::::]',
    ]
    expected_gfm = """<p><img src="/uri1" alt="xxbar<image src="xx">fooyy" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03fc():
    """
    Test case extra 03fc:  variation of 3f with inner iage
    """

    # Arrange
    source_markdown = """[xx![bar<image src="xx">foo]yy](/uri1)

[bar<image src="xx">foo]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/uri1:::::xx![bar<image src="xx">foo]yy:False::::]',
        "[text(1,2):xx:]",
        '[image(1,4):shortcut:/uri::bar<image src="xx">foo::::bar<image src="xx">foo:False::::]',
        "[text(1,29):yy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::bar<image src="xx">foo:: :/uri:::::]',
    ]
    expected_gfm = """<p><a href="/uri1">xx<img src="/uri" alt="bar<image src="xx">foo" />yy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03g():
    """
    Test case extra 03g:  variation of 3 with newline
    """

    # Arrange
    source_markdown = """[bar
foo]: /uri

[bar\nfoo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar foo:bar\nfoo: :/uri:::::]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[link(4,1):shortcut:/uri:::::bar\nfoo:False::::]",
        "[text(4,2):bar\nfoo::\n]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar
foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03ga():
    """
    Test case extra 03ga:  variation of 3g with text
    """

    # Arrange
    source_markdown = """[xx[bar
foo]yy](/uri1)

[bar
foo]: /uri
"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):[:]",
        "[text(1,2):xx:]",
        "[link(1,4):shortcut:/uri:::::bar\nfoo:False::::]",
        "[text(1,5):bar\nfoo::\n]",
        "[end-link::]",
        "[text(2,5):yy:]",
        "[text(2,7):]:]",
        "[text(2,8):(/uri1):]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar foo:bar\nfoo: :/uri:::::]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<p>[xx<a href="/uri">bar
foo</a>yy](/uri1)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03gb():
    """
    Test case extra 03gb:  variation of 3g with outer image
    """

    # Arrange
    source_markdown = """![xx[bar
foo]yy](/uri1)

[bar
foo]: /uri
"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[image(1,1):inline:/uri1::xxbar\nfooyy::::xx[bar\nfoo]yy:False::::]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar foo:bar\nfoo: :/uri:::::]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<p><img src="/uri1" alt="xxbar
fooyy" /></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03gc():
    """
    Test case extra 03gc:  variation of 3g with inner image
    """

    # Arrange
    source_markdown = """[xx![bar
foo]yy](/uri1)

[bar
foo]: /uri"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[link(1,1):inline:/uri1:::::xx![bar\nfoo]yy:False::::]",
        "[text(1,2):xx:]",
        "[image(1,4):shortcut:/uri::bar\nfoo::::bar\nfoo:False::::]",
        "[text(2,5):yy:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,1):True::bar foo:bar\nfoo: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri1">xx<img src="/uri" alt="bar
foo" />yy</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03hx():
    """
    Test case extra 03h:  variation of 3 with backslash
    """

    # Arrange
    source_markdown = """[bar\\
foo]: /uri

[bar\\
foo]"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):[:]",
        "[text(1,2):bar:]",
        "[hard-break(1,5):\\:\n]",
        "[text(2,1):foo:]",
        "[text(2,4):]:]",
        "[text(2,5):: /uri:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):[:]",
        "[text(4,2):bar:]",
        "[hard-break(4,5):\\:\n]",
        "[text(5,1):foo:]",
        "[text(5,4):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[bar<br />
foo]: /uri</p>
<p>[bar<br />
foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03hxa():
    """
    Test case extra 03hxa:  variation of 3h with newline
    """

    # Arrange
    source_markdown = """[\\
foo]: /uri

[\\
foo]"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):[:]",
        "[hard-break(1,2):\\:\n]",
        "[text(2,1):foo:]",
        "[text(2,4):]:]",
        "[text(2,5):: /uri:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):[:]",
        "[hard-break(4,2):\\:\n]",
        "[text(5,1):foo:]",
        "[text(5,4):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[<br />
foo]: /uri</p>
<p>[<br />
foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03hy():
    """
    Test case extra 03hy:  variation of 3h with multiple backslashes
    """

    # Arrange
    source_markdown = """[b\\ar\\
foo]: /uri

[b\\ar\\
foo]"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):[:]",
        "[text(1,2):b\\ar:]",
        "[hard-break(1,6):\\:\n]",
        "[text(2,1):foo:]",
        "[text(2,4):]:]",
        "[text(2,5):: /uri:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):[:]",
        "[text(4,2):b\\ar:]",
        "[hard-break(4,6):\\:\n]",
        "[text(5,1):foo:]",
        "[text(5,4):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[b\\ar<br />
foo]: /uri</p>
<p>[b\\ar<br />
foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03hz():
    """
    Test case extra 03hz:  variation of 3h with double backslash
    """

    # Arrange
    source_markdown = """[bar\\\\
foo]: /uri

[bar\\\\
foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar\\\\ foo:bar\\\\\nfoo: :/uri:::::]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[link(4,1):shortcut:/uri:::::bar\\\\\nfoo:False::::]",
        "[text(4,2):bar\\\b\\\nfoo::\n]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar\\
foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03ha():
    """
    Test case extra 03ha:  variation of 3h with text
    """

    # Arrange
    source_markdown = """[bar\\
foo]: /uri

[xx[bar\\
foo]yy]"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):[:]",
        "[text(1,2):bar:]",
        "[hard-break(1,5):\\:\n]",
        "[text(2,1):foo:]",
        "[text(2,4):]:]",
        "[text(2,5):: /uri:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):[:]",
        "[text(4,2):xx:]",
        "[text(4,4):[:]",
        "[text(4,5):bar:]",
        "[hard-break(4,8):\\:\n]",
        "[text(5,1):foo:]",
        "[text(5,4):]:]",
        "[text(5,5):yy:]",
        "[text(5,7):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[bar<br />
foo]: /uri</p>
<p>[xx[bar<br />
foo]yy]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03hb():
    """
    Test case extra 03hb:  variation of 3h with outer image
    """

    # Arrange
    source_markdown = """[bar\\
foo]: /uri

![xx[bar\\
foo]yy]"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):[:]",
        "[text(1,2):bar:]",
        "[hard-break(1,5):\\:\n]",
        "[text(2,1):foo:]",
        "[text(2,4):]:]",
        "[text(2,5):: /uri:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):![:]",
        "[text(4,3):xx:]",
        "[text(4,5):[:]",
        "[text(4,6):bar:]",
        "[hard-break(4,9):\\:\n]",
        "[text(5,1):foo:]",
        "[text(5,4):]:]",
        "[text(5,5):yy:]",
        "[text(5,7):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[bar<br />
foo]: /uri</p>
<p>![xx[bar<br />
foo]yy]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03hc():
    """
    Test case extra 03hc:  variation of 3h with inner image
    """

    # Arrange
    source_markdown = """[bar\\
foo]: /uri

[xx![bar\\
foo]yy]"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):[:]",
        "[text(1,2):bar:]",
        "[hard-break(1,5):\\:\n]",
        "[text(2,1):foo:]",
        "[text(2,4):]:]",
        "[text(2,5):: /uri:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):[:]",
        "[text(4,2):xx:]",
        "[text(4,4):![:]",
        "[text(4,6):bar:]",
        "[hard-break(4,9):\\:\n]",
        "[text(5,1):foo:]",
        "[text(5,4):]:]",
        "[text(5,5):yy:]",
        "[text(5,7):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[bar<br />
foo]: /uri</p>
<p>[xx![bar<br />
foo]yy]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03i():
    """
    Test case extra 03i:  variation of 3 with double space
    """

    # Arrange
    source_markdown = """[bar\a\a
foo]: /uri

[bar\a\a
foo]""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[link-ref-def(1,1):True::bar foo:bar  \nfoo: :/uri:::::]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[link(4,1):shortcut:/uri:::::bar  \nfoo:False::::]",
        "[text(4,2):bar:]",
        "[hard-break(4,5):  :\n]",
        "[text(5,1):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar<br />
foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03ia():
    """
    Test case extra 03ia:  variation of 3i with text
    """

    # Arrange
    source_markdown = """[bar\a\a
foo]: /uri

[xx[bar\a\a
foo]yy]""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[link-ref-def(1,1):True::bar foo:bar  \nfoo: :/uri:::::]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):[:]",
        "[text(4,2):xx:]",
        "[link(4,4):shortcut:/uri:::::bar  \nfoo:False::::]",
        "[text(4,5):bar:]",
        "[hard-break(4,8):  :\n]",
        "[text(5,1):foo:]",
        "[end-link::]",
        "[text(5,5):yy:]",
        "[text(5,7):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[xx<a href="/uri">bar<br />
foo</a>yy]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03ib():
    """
    Test case extra 03ib:  variation of 3i with outer image
    """

    # Arrange
    source_markdown = """[bar\a\a
foo]: /uri

![xx[bar\a\a
foo]yy]""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[link-ref-def(1,1):True::bar foo:bar  \nfoo: :/uri:::::]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):![:]",
        "[text(4,3):xx:]",
        "[link(4,5):shortcut:/uri:::::bar  \nfoo:False::::]",
        "[text(4,6):bar:]",
        "[hard-break(4,9):  :\n]",
        "[text(5,1):foo:]",
        "[end-link::]",
        "[text(5,5):yy:]",
        "[text(5,7):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>![xx<a href="/uri">bar<br />
foo</a>yy]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03ic():
    """
    Test case extra 03ic:  variation of 03 with inner image
    """

    # Arrange
    source_markdown = """[bar\a\a
foo]: /uri

[xx![bar\a\a
foo]yy]""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[link-ref-def(1,1):True::bar foo:bar  \nfoo: :/uri:::::]",
        "[BLANK(3,1):]",
        "[para(4,1):\n]",
        "[text(4,1):[:]",
        "[text(4,2):xx:]",
        "[image(4,4):shortcut:/uri::bar\nfoo::::bar  \nfoo:False::::]",
        "[text(5,5):yy:]",
        "[text(5,7):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[xx<img src="/uri" alt="bar
foo" />yy]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03jx():
    """
    Test case extra 03j:  variation of 3 with double backslash
    """

    # Arrange
    source_markdown = """[bar\\\\
foo]: /uri

abc
[bar\\\\
foo]
abc"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar\\\\ foo:bar\\\\\nfoo: :/uri:::::]",
        "[BLANK(3,1):]",
        "[para(4,1):\n\n\n]",
        "[text(4,1):abc\n::\n]",
        "[link(5,1):shortcut:/uri:::::bar\\\\\nfoo:False::::]",
        "[text(5,2):bar\\\b\\\nfoo::\n]",
        "[end-link::]",
        "[text(6,5):\nabc::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
<a href="/uri">bar\\
foo</a>
abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_extra_03ja():
    """
    Test case extra 03ja:  variation of 3 with text
    """

    # Arrange
    source_markdown = """[bar\\\\
foo]: /uri

abc
[bar\\\\
foo][]
abc"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar\\\\ foo:bar\\\\\nfoo: :/uri:::::]",
        "[BLANK(3,1):]",
        "[para(4,1):\n\n\n]",
        "[text(4,1):abc\n::\n]",
        "[link(5,1):collapsed:/uri:::::bar\\\\\nfoo:False::::]",
        "[text(5,2):bar\\\b\\\nfoo::\n]",
        "[end-link::]",
        "[text(6,7):\nabc::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
<a href="/uri">bar\\
foo</a>
abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
