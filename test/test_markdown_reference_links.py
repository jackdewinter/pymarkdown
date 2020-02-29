"""
https://github.github.com/gfm/#links
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


# pylint: disable=too-many-lines
@pytest.mark.skip
def test_reference_links_535():
    """
    Test case 535:  Here is a simple example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo][bar]

[bar]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_536():
    """
    Test case 536:  (part 1) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link [foo [bar]]][ref]

[ref]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_537():
    """
    Test case 537:  (part 2) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link \\[bar][ref]

[ref]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_538():
    """
    Test case 538:  (part 1) The link text may contain inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link *foo **bar** `#`*][ref]

[ref]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_539():
    """
    Test case 539:  (part 2) The link text may contain inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[![moon](moon.jpg)][ref]

[ref]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_540():
    """
    Test case 540:  (part 1) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo [bar](/uri)][ref]

[ref]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_541():
    """
    Test case 541:  (part 2) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo *bar [baz][ref]*][ref]

[ref]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_542():
    """
    Test case 542:  (part 1) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*[foo*][ref]

[ref]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_543():
    """
    Test case 543:  (part 2) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo *bar][ref]*

[ref]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_544():
    """
    Test case 544:  (part 1) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo <bar attr="][ref]">

[ref]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_545():
    """
    Test case 545:  (part 2) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo`][ref]`

[ref]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_546():
    """
    Test case 546:  (part 3) The following cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo<http://example.com/?search=][ref]>

[ref]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_547():
    """
    Test case 547:  Matching is case-insensitive:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo][BaR]

[bar]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_548():
    """
    Test case 548:  Unicode case fold is used:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[ẞ]

[SS]: /url"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_549():
    """
    Test case 549:  Consecutive internal whitespace is treated as one space for purposes of determining matching:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[Foo
  bar]: /url

[Baz][Foo bar]"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_550():
    """
    Test case 550:  (part 1) No whitespace is allowed between the link text and the link label:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo] [bar]

[bar]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_551():
    """
    Test case 551:  (part 2) No whitespace is allowed between the link text and the link label:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo]
[bar]

[bar]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_552():
    """
    Test case 552:  When there are multiple matching link reference definitions, the first is used:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo]: /url1

[foo]: /url2

[bar][foo]"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_553():
    """
    Test case 553:  Note that matching is performed on normalized strings, not parsed inline content. So the following does not match, even though the labels define equivalent inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[bar][foo\\!]

[foo!]: /url"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_554():
    """
    Test case 554:  (part 1) Link labels cannot contain brackets, unless they are backslash-escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo][ref[]

[ref[]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_555():
    """
    Test case 555:  (part 2) Link labels cannot contain brackets, unless they are backslash-escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo][ref[bar]]

[ref[bar]]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_556():
    """
    Test case 556:  (part 3) Link labels cannot contain brackets, unless they are backslash-escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[[[foo]]]

[[[foo]]]: /url"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_557():
    """
    Test case 557:  (part 4) Link labels cannot contain brackets, unless they are backslash-escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo][ref\\[]

[ref\\[]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_558():
    """
    Test case 558:  Note that in this example ] is not backslash-escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[bar\\]: /uri

[bar\\]"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_559():
    """
    Test case 559:  (part 1) A link label must contain at least one non-whitespace character:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[]

[]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_560():
    """
    Test case 560:  (part 2) A link label must contain at least one non-whitespace character:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[
 ]

[
 ]: /uri"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_561():
    """
    Test case 561:  (part 1) Thus, [foo][] is equivalent to [foo][foo].
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo][]

[foo]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_562():
    """
    Test case 562:  (part 2) Thus, [foo][] is equivalent to [foo][foo].
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[*foo* bar][]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_563():
    """
    Test case 563:  The link labels are case-insensitive:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[Foo][]

[foo]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_564():
    """
    Test case 564:  As with full reference links, whitespace is not allowed between the two sets of brackets:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo]\a
[]

[foo]: /url "title"
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_565():
    """
    Test case 565:  (part 1) A shortcut reference link consists of a link label that matches a link reference definition elsewhere in the document and is not followed by [] or a link label.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_566():
    """
    Test case 566:  (part 2) A shortcut reference link consists of a link label that matches a link reference definition elsewhere in the document and is not followed by [] or a link label.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[*foo* bar]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_567():
    """
    Test case 567:  (part 3) A shortcut reference link consists of a link label that matches a link reference definition elsewhere in the document and is not followed by [] or a link label.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[[*foo* bar]]

[*foo* bar]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_568():
    """
    Test case 568:  (part 4) A shortcut reference link consists of a link label that matches a link reference definition elsewhere in the document and is not followed by [] or a link label.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[[bar [foo]

[foo]: /url"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_569():
    """
    Test case 569:  The link labels are case-insensitive:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[Foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_570():
    """
    Test case 570:  A space after the link text should be preserved:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo] bar

[foo]: /url"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_571():
    """
    Test case 571:  If you just want bracketed text, you can backslash-escape the opening bracket to avoid links
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """\\[foo]

[foo]: /url "title"
"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_572():
    """
    Test case 572:  Note that this is a link, because a link label ends with the first following closing bracket:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo*]: /url

*[foo*]"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_573():
    """
    Test case 573:  (part 1) Full and compact references take precedence over shortcut references:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo][bar]

[foo]: /url1
[bar]: /url2"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_574():
    """
    Test case 574:  (part 2) Full and compact references take precedence over shortcut references:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo][]

[foo]: /url1"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_575():
    """
    Test case 575:  (part 1) Inline links also take precedence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo]()

[foo]: /url1"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_576():
    """
    Test case 576:  (part 2) Inline links also take precedence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo]()
[foo](not a link)

[foo]: /url1"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_577():
    """
    Test case 577:  In the following case [bar][baz] is parsed as a reference, [foo] as normal text:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo][bar][baz]

[baz]: /url"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_578():
    """
    Test case 578:  Here, though, [foo][bar] is parsed as a reference, since [bar] is defined:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo][bar][baz]

[baz]: /url1
[bar]: /url2"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_reference_links_579():
    """
    Test case 579:  Here [foo] is not parsed as a shortcut reference, because it is followed by a link label (even though [bar] is not defined):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo][bar][baz]

[baz]: /url1
[foo]: /url2"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
