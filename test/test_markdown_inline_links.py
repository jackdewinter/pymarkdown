"""
https://github.github.com/gfm/#links
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


@pytest.mark.skip
def test_inline_links_493():
    """
    Test case 493:  Here is a simple inline link:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](/uri "title")"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_494():
    """
    Test case 494:  The title may be omitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](/uri)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_495():
    """
    Test case 495:  (part 1) Both the title and the destination may be omitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link]()"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_496():
    """
    Test case 496:  (part 2) Both the title and the destination may be omitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](<>)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_inline_links_497():
    """
    Test case 497:  (part 1) The destination can only contain spaces if it is enclosed in pointy brackets
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](/my uri)"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text:(/my uri):]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_498():
    """
    Test case 498:  (part 2) The destination can only contain spaces if it is enclosed in pointy brackets
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](</my uri>)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_inline_links_499():
    """
    Test case 499:  (part 1) The destination cannot contain line breaks, even if enclosed in pointy brackets:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](foo
bar)"""
    expected_tokens = [
        "[para:\n]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text:(foo\nbar)::\n]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_inline_links_500():
    """
    Test case 500:  (part 2) The destination cannot contain line breaks, even if enclosed in pointy brackets:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](<foo
bar>)"""
    expected_tokens = [
        "[para:\n]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text:(:]",
        "[raw-html:foo\nbar]",
        "[text:):]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_501():
    """
    Test case 501:  The destination can contain ) if it is enclosed in pointy brackets:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[a](<b)c>)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_inline_links_502():
    """
    Test case 502:  Pointy brackets that enclose links must be unescaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](<foo\\>)"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text:(&lt;foo&gt;):]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_503():
    """
    Test case 503:  These are not links, because the opening pointy bracket is not matched properly:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[a](<b)c
[a](<b)c>
[a](<b>c)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_504():
    """
    Test case 504:  Parentheses inside the link destination may be escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](\\(foo\\))"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_505():
    """
    Test case 505:  Any number of parentheses are allowed without escaping, as long as they are balanced:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](foo(and(bar)))"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_506():
    """
    Test case 506:  (part 1) However, if you have unbalanced parentheses, you need to escape or use the <...> form:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](foo\\(and\\(bar\\))"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_507():
    """
    Test case 506:  (part 2) However, if you have unbalanced parentheses, you need to escape or use the <...> form:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](<foo(and(bar)>)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_508():
    """
    Test case 508:  Parentheses and other symbols can also be escaped, as usual in Markdown:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](foo\\)\\:)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_509():
    """
    Test case 509:  A link can contain fragment identifiers and queries:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](#fragment)

[link](http://example.com#fragment)

[link](http://example.com?foo=3#frag)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_510():
    """
    Test case 510:  Note that a backslash before a non-escapable character is just a backslash:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](foo\\bar)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_511():
    """
    Test case 511:  URL-escaping should be left alone inside the destination
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](foo%20b&auml;)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_512():
    """
    Test case 512:  Note that, because titles can often be parsed as destinations, if you try to omit the destination and keep the title, you’ll get unexpected results:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link]("title")"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_513():
    """
    Test case 513:  Titles may be in single quotes, double quotes, or parentheses:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](/url "title")
[link](/url 'title')
[link](/url (title))"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_514():
    """
    Test case 514:  Backslash escapes and entity and numeric character references may be used in titles:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](/url "title \"&quot;")"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_515():
    """
    Test case 515:  Titles must be separated from the link using a whitespace. Other Unicode whitespace like non-breaking space doesn’t work.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](/url "title")"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_inline_links_516():
    """
    Test case 516:  Nested balanced quotes are not allowed without escaping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](/url "title "and" title")"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text:(/url &quot;title &quot;and&quot; title&quot;):]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_517():
    """
    Test case 517:  But it is easy to work around this by using a different quote type:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](/url 'title "and" title')"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_518():
    """
    Test case 518:  Whitespace is allowed around the destination and title:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link](   /uri
  "title"  )"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_inline_links_519():
    """
    Test case 519:  But it is not allowed between the link text and the following parenthesis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link] (/uri)"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text: (/uri):]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_520():
    """
    Test case 520:  (part 1) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link [foo [bar]]](/uri)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_inline_links_521():
    """
    Test case 521:  (part 2) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link] bar](/uri)"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text: bar:]",
        "[text:]:]",
        "[text:(/uri):]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_522():
    """
    Test case 522:  (part 3) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link [bar](/uri)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_523():
    """
    Test case 523:  (part 4) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link \\[bar](/uri)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_524():
    """
    Test case 524:  (part 1) The link text may contain inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[link *foo **bar** `#`*](/uri)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_525():
    """
    Test case 525:  (part 2) The link text may contain inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[![moon](moon.jpg)](/uri)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_526():
    """
    Test case 526:  (part 1) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo [bar](/uri)](/uri)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_527():
    """
    Test case 527:  (part 2) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo *[bar [baz](/uri)](/uri)*](/uri)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_528():
    """
    Test case 528:  (part 3) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """![[[foo](uri1)](uri2)](uri3)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_529():
    """
    Test case 529:  (part 1) These cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*[foo*](/uri)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_530():
    """
    Test case 530:  (part 2) These cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo *bar](baz*)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_inline_links_531():
    """
    Test case 531:  Note that brackets that aren’t part of links do not take precedence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*foo [bar* baz]"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_inline_links_532():
    """
    Test case 532:  (part 1) These cases illustrate the precedence of HTML tags, code spans, and autolinks over link grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo <bar attr="](baz)">"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:foo :]",
        '[raw-html:bar attr="](baz)"]',
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_inline_links_533():
    """
    Test case 533:  (part 2) These cases illustrate the precedence of HTML tags, code spans, and autolinks over link grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo`](/uri)`"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:foo:]",
        "[icode-span:](/uri)]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_inline_links_534():
    """
    Test case 534:  (part 3) These cases illustrate the precedence of HTML tags, code spans, and autolinks over link grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo<http://example.com/?search=](uri)>"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:foo:]",
        "[uri-autolink:http://example.com/?search=](uri)]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
