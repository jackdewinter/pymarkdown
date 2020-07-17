"""
https://github.github.com/gfm/#links
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    assert_if_lists_different,
    assert_if_strings_different,
    assert_token_consistency,
)


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_reference_links_535():
    """
    Test case 535:  Here is a simple example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo][bar]

[bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:full:/url:title:::bar:foo]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_536():
    """
    Test case 536:  (part 1) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link [foo [bar]]][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:full:/uri::::ref:link [foo [bar]]]",
        "[text:link :]",
        "[text:[:]",
        "[text:foo :]",
        "[text:[:]",
        "[text:bar:]",
        "[text:]:]",
        "[text:]:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri">link [foo [bar]]</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_537():
    """
    Test case 537:  (part 2) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link \\[bar][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:full:/uri::::ref:link \\\\\b[bar]",
        "[text:link \\\b[bar:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri">link [bar</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_538():
    """
    Test case 538:  (part 1) The link text may contain inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link *foo **bar** `#`*][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:full:/uri::::ref:link *foo **bar** #*]",
        "[text:link :]",
        "[emphasis:1]",
        "[text:foo :]",
        "[emphasis:2]",
        "[text:bar:]",
        "[end-emphasis::2]",
        "[text: :]",
        "[icode-span:#]",
        "[end-emphasis::1]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri">link <em>foo <strong>bar</strong> <code>#</code></em></a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_539():
    """
    Test case 539:  (part 2) The link text may contain inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[![moon](moon.jpg)][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:full:/uri::::ref:moon]",
        "[image:inline:moon.jpg::moon::::moon]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri"><img src="moon.jpg" alt="moon" /></a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_540():
    """
    Test case 540:  (part 1) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo [bar](/uri)][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo :]",
        "[link:inline:/uri:::::bar]",
        "[text:bar:]",
        "[end-link::]",
        "[text:]:]",
        "[link:shortcut:/uri:::::ref]",
        "[text:ref:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p>[foo <a href="/uri">bar</a>]<a href="/uri">ref</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_541():
    """
    Test case 541:  (part 2) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo *bar [baz][ref]*][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo :]",
        "[emphasis:1]",
        "[text:bar :]",
        "[link:full:/uri::::ref:baz]",
        "[text:baz:]",
        "[end-link::]",
        "[end-emphasis::1]",
        "[text:]:]",
        "[link:shortcut:/uri:::::ref]",
        "[text:ref:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = (
        """<p>[foo <em>bar <a href="/uri">baz</a></em>]<a href="/uri">ref</a></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_542():
    """
    Test case 542:  (part 1) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*[foo*][ref]

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:*:]",
        "[link:full:/uri::::ref:foo*]",
        "[text:foo:]",
        "[text:*:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p>*<a href="/uri">foo*</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_543():
    """
    Test case 543:  (part 2) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo *bar][ref]*

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:full:/uri::::ref:foo *bar]",
        "[text:foo :]",
        "[text:*:]",
        "[text:bar:]",
        "[end-link::]",
        "[text:*:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri">foo *bar</a>*</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_544():
    """
    Test case 544:  (part 1) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo <bar attr="][ref]">

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo :]",
        '[raw-html:bar attr="][ref]"]',
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p>[foo <bar attr="][ref]"></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_545():
    """
    Test case 545:  (part 2) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo`][ref]`

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[icode-span:][ref]]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p>[foo<code>][ref]</code></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_546():
    """
    Test case 546:  (part 3) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo<http://example.com/?search=][ref]>

[ref]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[uri-autolink:http://example.com/?search=][ref]]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref:: :/uri:::::]",
    ]
    expected_gfm = """<p>[foo<a href="http://example.com/?search=%5D%5Bref%5D">http://example.com/?search=][ref]</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_547():
    """
    Test case 547:  Matching is case-insensitive:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo][BaR]

[bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:full:/url:title:::BaR:foo]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_548():
    """
    Test case 548:  Unicode case fold is used:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[ẞ]

[SS]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:shortcut:/url:::::ẞ]",
        "[text:ẞ:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ss:SS: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">ẞ</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_549():
    """
    Test case 549:  Consecutive internal whitespace is treated as one space for purposes of determining matching:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[Foo
  bar]: /url

[Baz][Foo bar]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo bar:Foo\n  bar: :/url:::::]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[link:full:/url::::Foo bar:Baz]",
        "[text:Baz:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/url">Baz</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_550():
    """
    Test case 550:  (part 1) No whitespace is allowed between the link text and the link label:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo] [bar]

[bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[text: :]",
        "[link:shortcut:/url:title::::bar]",
        "[text:bar:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>[foo] <a href="/url" title="title">bar</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_551():
    """
    Test case 551:  (part 2) No whitespace is allowed between the link text and the link label:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]
[bar]

[bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[text:\n::\n]",
        "[link:shortcut:/url:title::::bar]",
        "[text:bar:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(3,1):]",
        '[link-ref-def(4,1):True::bar:: :/url:: :title:"title":]',
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<p>[foo]
<a href="/url" title="title">bar</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_552():
    """
    Test case 552:  When there are multiple matching link reference definitions, the first is used:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]: /url1

[foo]: /url2

[bar][foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url1:::::]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):False::foo:: :/url2:::::]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[link:full:/url1::::foo:bar]",
        "[text:bar:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/url1">bar</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_553():
    """
    Test case 553:  Note that matching is performed on normalized strings, not parsed inline content. So the following does not match, even though the labels define equivalent inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[bar][foo\\!]

[foo!]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:bar:]",
        "[text:]:]",
        "[text:[:]",
        "[text:foo\\\b!:]",
        "[text:]:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo!:: :/url:::::]",
    ]
    expected_gfm = """<p>[bar][foo!]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_554():
    """
    Test case 554:  (part 1) Link labels cannot contain brackets, unless they are backslash-escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo][ref[]

[ref[]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[text:[:]",
        "[text:ref:]",
        "[text:[:]",
        "[text:]:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:[:]",
        "[text:ref:]",
        "[text:[:]",
        "[text:]:]",
        "[text:: /uri:]",
        "[end-para]",
    ]
    expected_gfm = """<p>[foo][ref[]</p>
<p>[ref[]: /uri</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_555():
    """
    Test case 555:  (part 2) Link labels cannot contain brackets, unless they are backslash-escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo][ref[bar]]

[ref[bar]]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[text:[:]",
        "[text:ref:]",
        "[text:[:]",
        "[text:bar:]",
        "[text:]:]",
        "[text:]:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:[:]",
        "[text:ref:]",
        "[text:[:]",
        "[text:bar:]",
        "[text:]:]",
        "[text:]:]",
        "[text:: /uri:]",
        "[end-para]",
    ]
    expected_gfm = """<p>[foo][ref[bar]]</p>
<p>[ref[bar]]: /uri</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_556():
    """
    Test case 556:  (part 3) Link labels cannot contain brackets, unless they are backslash-escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[[[foo]]]

[[[foo]]]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:[:]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[text:]:]",
        "[text:]:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:[:]",
        "[text:[:]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[text:]:]",
        "[text:]:]",
        "[text:: /url:]",
        "[end-para]",
    ]
    expected_gfm = """<p>[[[foo]]]</p>
<p>[[[foo]]]: /url</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_557():
    """
    Test case 557:  (part 4) Link labels cannot contain brackets, unless they are backslash-escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo][ref\\[]

[ref\\[]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:full:/uri::::ref\\[:foo]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::ref\\[:: :/uri:::::]",
    ]
    expected_gfm = """<p><a href="/uri">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_558():
    """
    Test case 558:  Note that in this example ] is not backslash-escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[bar\\\\]: /uri

[bar\\\\]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::bar\\\\:: :/uri:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link:shortcut:/uri:::::bar\\\\\b\\]",
        "[text:bar\\\b\\:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/uri">bar\\</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_559():
    """
    Test case 559:  (part 1) A link label must contain at least one non-whitespace character:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[]

[]: /uri"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:]:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:[:]",
        "[text:]:]",
        "[text:: /uri:]",
        "[end-para]",
    ]
    expected_gfm = """<p>[]</p>
<p>[]: /uri</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    # assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_560():
    """
    Test case 560:  (part 2) A link label must contain at least one non-whitespace character:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[
 ]

[
 ]: /uri"""
    expected_tokens = [
        "[para(1,1):\n ]",
        "[text:[:]",
        "[text:\n::\n]",
        "[text:]:]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[para(4,1):\n ]",
        "[text:[:]",
        "[text:\n::\n]",
        "[text:]:]",
        "[text:: /uri:]",
        "[end-para]",
    ]
    expected_gfm = """<p>[
]</p>
<p>[
]: /uri</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    # assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_561():
    """
    Test case 561:  (part 1) Thus, [foo][] is equivalent to [foo][foo].
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo][]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:collapsed:/url:title::::foo]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_562():
    """
    Test case 562:  (part 2) Thus, [foo][] is equivalent to [foo][foo].
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[*foo* bar][]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:collapsed:/url:title::::*foo* bar]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[text: bar:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::*foo* bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title"><em>foo</em> bar</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_563():
    """
    Test case 563:  The link labels are case-insensitive:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[Foo][]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:collapsed:/url:title::::Foo]",
        "[text:Foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">Foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_564():
    """
    Test case 564:  As with full reference links, whitespace is not allowed between the two sets of brackets:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]\a
[]

[foo]: /url "title"
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,1):\n]",
        "[link:shortcut:/url:title::::foo]",
        "[text:foo:]",
        "[end-link::]",
        "[text:\n:: \n]",
        "[text:[:]",
        "[text:]:]",
        "[end-para]",
        "[BLANK(3,1):]",
        '[link-ref-def(4,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a>
[]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_565():
    """
    Test case 565:  (part 1) A shortcut reference link consists of a link label that matches a link reference definition elsewhere in the document and is not followed by [] or a link label.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:shortcut:/url:title::::foo]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_566():
    """
    Test case 566:  (part 2) A shortcut reference link consists of a link label that matches a link reference definition elsewhere in the document and is not followed by [] or a link label.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[*foo* bar]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:shortcut:/url:title::::*foo* bar]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[text: bar:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::*foo* bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title"><em>foo</em> bar</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_567():
    """
    Test case 567:  (part 3) A shortcut reference link consists of a link label that matches a link reference definition elsewhere in the document and is not followed by [] or a link label.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[[*foo* bar]]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[link:shortcut:/url:title::::*foo* bar]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[text: bar:]",
        "[end-link::]",
        "[text:]:]",
        "[end-para]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::*foo* bar:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>[<a href="/url" title="title"><em>foo</em> bar</a>]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_568():
    """
    Test case 568:  (part 4) A shortcut reference link consists of a link label that matches a link reference definition elsewhere in the document and is not followed by [] or a link label.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[[bar [foo]

[foo]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:[:]",
        "[text:bar :]",
        "[link:shortcut:/url:::::foo]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :/url:::::]",
    ]
    expected_gfm = """<p>[[bar <a href="/url">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_569():
    """
    Test case 569:  The link labels are case-insensitive:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[Foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:shortcut:/url:title::::Foo]",
        "[text:Foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/url" title="title">Foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_570():
    """
    Test case 570:  A space after the link text should be preserved:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo] bar

[foo]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:shortcut:/url:::::foo]",
        "[text:foo:]",
        "[end-link::]",
        "[text: bar:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :/url:::::]",
    ]
    expected_gfm = """<p><a href="/url">foo</a> bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_570a():
    """
    Test case 570a:  Variation of 570 to show how link inside of link doesn't work.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo[foo]]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[link:shortcut:/url:title::::foo]",
        "[text:foo:]",
        "[end-link::]",
        "[text:]:]",
        "[end-para]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>[foo<a href=\"/url\" title=\"title\">foo</a>]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_571():
    """
    Test case 571:  If you just want bracketed text, you can backslash-escape the opening bracket to avoid links
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\[foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:\\\b[foo:]",
        "[text:]:]",
        "[end-para]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>[foo]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_572():
    """
    Test case 572:  Note that this is a link, because a link label ends with the first following closing bracket:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo*]: /url

*[foo*]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo*:: :/url:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:*:]",
        "[link:shortcut:/url:::::foo*]",
        "[text:foo:]",
        "[text:*:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p>*<a href="/url">foo*</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_573():
    """
    Test case 573:  (part 1) Full and compact references take precedence over shortcut references:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo][bar]

[foo]: /url1
[bar]: /url2"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:full:/url2::::bar:foo]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :/url1:::::]",
        "[link-ref-def(4,1):True::bar:: :/url2:::::]",
    ]
    expected_gfm = """<p><a href="/url2">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_574():
    """
    Test case 574:  (part 2) Full and compact references take precedence over shortcut references:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo][]

[foo]: /url1"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:collapsed:/url1:::::foo]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :/url1:::::]",
    ]
    expected_gfm = """<p><a href="/url1">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_575():
    """
    Test case 575:  (part 1) Inline links also take precedence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]()

[foo]: /url1"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:inline::::::foo]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :/url1:::::]",
    ]
    expected_gfm = """<p><a href="">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_576():
    """
    Test case 576:  (part 2) Inline links also take precedence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo](not a link)

[foo]: /url1"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:shortcut:/url1:::::foo]",
        "[text:foo:]",
        "[end-link::]",
        "[text:(not a link):]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :/url1:::::]",
    ]
    expected_gfm = """<p><a href="/url1">foo</a>(not a link)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_577():
    """
    Test case 577:  In the following case [bar][baz] is parsed as a reference, [foo] as normal text:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo][bar][baz]

[baz]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[link:full:/url::::baz:bar]",
        "[text:bar:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::baz:: :/url:::::]",
    ]
    expected_gfm = """<p>[foo]<a href="/url">bar</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_578():
    """
    Test case 578:  Here, though, [foo][bar] is parsed as a reference, since [bar] is defined:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo][bar][baz]

[baz]: /url1
[bar]: /url2"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:full:/url2::::bar:foo]",
        "[text:foo:]",
        "[end-link::]",
        "[link:shortcut:/url1:::::baz]",
        "[text:baz:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::baz:: :/url1:::::]",
        "[link-ref-def(4,1):True::bar:: :/url2:::::]",
    ]
    expected_gfm = """<p><a href="/url2">foo</a><a href="/url1">baz</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_reference_links_579():
    """
    Test case 579:  Here [foo] is not parsed as a shortcut reference, because it is followed by a link label (even though [bar] is not defined):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo][bar][baz]

[baz]: /url1
[foo]: /url2"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[link:full:/url1::::baz:bar]",
        "[text:bar:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::baz:: :/url1:::::]",
        "[link-ref-def(4,1):True::foo:: :/url2:::::]",
    ]
    expected_gfm = """<p>[foo]<a href="/url1">bar</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
