"""
https://github.github.com/gfm/#links
"""
import pytest

from .utils import (
    act_and_assert
)


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
        "[link(1,1):full:/url:title:::bar:foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
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
    Test case 535:  Here is a simple example:
    """

    # Arrange
    source_markdown = """[foo][bar]\a

[bar]: /url "title"
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):: ]",
        "[link(1,1):full:/url:title:::bar:foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
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
    Test case 535:  Here is a simple example:
    """

    # Arrange
    source_markdown = """[foo][bar] abc

[bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):full:/url:title:::bar:foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
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
        "[link(1,1):full:/uri::::ref:link [foo [bar]]:::::]",
        "[text(1,2):link :]",
        "[text(1,7):[:]",
        "[text(1,8):foo :]",
        "[text(1,12):[:]",
        "[text(1,13):bar:]",
        "[text(1,16):]:]",
        "[text(1,17):]:]",
        "[end-link:::False]",
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
        "[link(1,1):full:/uri::::ref:link \\[bar:::::]",
        "[text(1,2):link \\\b[bar:]",
        "[end-link:::False]",
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
        "[link(1,1):full:/uri::::ref:link *foo **bar** `#`*:::::]",
        "[text(1,2):link :]",
        "[emphasis(1,7):1:*]",
        "[text(1,8):foo :]",
        "[emphasis(1,12):2:*]",
        "[text(1,14):bar:]",
        "[end-emphasis(1,17)::2:*:False]",
        "[text(1,19): :]",
        "[icode-span(1,20):#:`::]",
        "[end-emphasis(1,23)::1:*:False]",
        "[end-link:::False]",
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
        "[link(1,1):full:/uri::::ref:![moon](moon.jpg):::::]",
        "[image(1,2):inline:moon.jpg::moon::::moon:False::::]",
        "[end-link:::False]",
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
        "[end-link:::False]",
        "[text(1,17):]:]",
        "[link(1,18):shortcut:/uri:::::ref:::::]",
        "[text(1,19):ref:]",
        "[end-link:::False]",
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
        "[link(1,11):full:/uri::::ref:baz:::::]",
        "[text(1,12):baz:]",
        "[end-link:::False]",
        "[end-emphasis(1,21)::1:*:False]",
        "[text(1,22):]:]",
        "[link(1,23):shortcut:/uri:::::ref:::::]",
        "[text(1,24):ref:]",
        "[end-link:::False]",
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
        "[link(1,2):full:/uri::::ref:foo*:::::]",
        "[text(1,3):foo:]",
        "[text(1,6):*:]",
        "[end-link:::False]",
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
        "[link(1,1):full:/uri::::ref:foo *bar:::::]",
        "[text(1,2):foo :]",
        "[text(1,6):*:]",
        "[text(1,7):bar:]",
        "[end-link:::False]",
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
        "[link(1,1):full:/url:title:::BaR:foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
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
        "[link(1,1):shortcut:/url:::::ẞ:::::]",
        "[text(1,2):ẞ:]",
        "[end-link:::False]",
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
        "[link(4,1):full:/url::::Foo bar:Baz:::::]",
        "[text(4,2):Baz:]",
        "[end-link:::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">Baz</a></p>"""

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
        "[link(1,7):shortcut:/url:title::::bar:::::]",
        "[text(1,8):bar:]",
        "[end-link:::False]",
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
        "[link(2,1):shortcut:/url:title::::bar:::::]",
        "[text(2,2):bar:]",
        "[end-link:::False]",
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
        "[link(5,1):full:/url1::::foo:bar:::::]",
        "[text(5,2):bar:]",
        "[end-link:::False]",
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
        "[link(1,1):full:/uri::::ref\\[:foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
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
        "[link(3,1):shortcut:/uri:::::bar\\\\:::::]",
        "[text(3,2):bar\\\b\\:]",
        "[end-link:::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar\\</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_558a():
    """
    Test case 558a:  variation
    """

    # Arrange
    source_markdown = """[bar&#x5C;]: /uri

[bar&#x5C;]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar&#x5c;:bar&#x5C;: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/uri:::::bar&#x5C;:::::]",
        "[text(3,2):bar\a&#x5C;\a\\\a:]",
        "[end-link:::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/uri">bar\\</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_reference_links_558b():
    """
    Test case 558a:  variation
    """

    # Arrange
    source_markdown = """[bar&beta;]: /uri

[bar&beta;]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar&beta;:: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/uri:::::bar&beta;:::::]",
        "[text(3,2):bar\a&beta;\aβ\a:]",
        "[end-link:::False]",
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
        "[link(1,1):collapsed:/url:title::::foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
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
        "[link(1,1):collapsed:/url:title::::*foo* bar:::::]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):foo:]",
        "[end-emphasis(1,6)::1:*:False]",
        "[text(1,7): bar:]",
        "[end-link:::False]",
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
        "[link(1,1):collapsed:/url:title::::Foo:::::]",
        "[text(1,2):Foo:]",
        "[end-link:::False]",
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
        "[link(1,1):shortcut:/url:title::::foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
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
        "[link(1,1):shortcut:/url:title::::foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
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
        "[link(1,1):shortcut:/url:title::::*foo* bar:::::]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):foo:]",
        "[end-emphasis(1,6)::1:*:False]",
        "[text(1,7): bar:]",
        "[end-link:::False]",
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
        "[link(1,2):shortcut:/url:title::::*foo* bar:::::]",
        "[emphasis(1,3):1:*]",
        "[text(1,4):foo:]",
        "[end-emphasis(1,7)::1:*:False]",
        "[text(1,8): bar:]",
        "[end-link:::False]",
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
        "[link(1,7):shortcut:/url:::::foo:::::]",
        "[text(1,8):foo:]",
        "[end-link:::False]",
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
        "[link(1,1):shortcut:/url:title::::Foo:::::]",
        "[text(1,2):Foo:]",
        "[end-link:::False]",
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
        "[link(1,1):shortcut:/url:::::foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
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
    Test case 570a:  Variation of 570 to show how link inside of link doesn't work.
    """

    # Arrange
    source_markdown = """[foo[foo]]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[link(1,5):shortcut:/url:title::::foo:::::]",
        "[text(1,6):foo:]",
        "[end-link:::False]",
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
        "[link(3,2):shortcut:/url:::::foo*:::::]",
        "[text(3,3):foo:]",
        "[text(3,6):*:]",
        "[end-link:::False]",
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
        "[link(1,1):full:/url2::::bar:foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
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
        "[link(1,1):collapsed:/url1:::::foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
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
        "[link(1,1):inline::::::foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
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
        "[end-link:::False]",
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
        "[link(1,6):full:/url::::baz:bar:::::]",
        "[text(1,7):bar:]",
        "[end-link:::False]",
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
        "[link(1,1):full:/url2::::bar:foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
        "[link(1,11):shortcut:/url1:::::baz:::::]",
        "[text(1,12):baz:]",
        "[end-link:::False]",
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
        "[link(1,6):full:/url1::::baz:bar:::::]",
        "[text(1,7):bar:]",
        "[end-link:::False]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::baz:: :/url1:::::]",
        "[link-ref-def(4,1):True::foo:: :/url2:::::]",
    ]
    expected_gfm = """<p>[foo]<a href="/url1">bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
