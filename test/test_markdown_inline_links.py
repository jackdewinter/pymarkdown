"""
https://github.github.com/gfm/#links
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_inline_links_493():
    """
    Test case 493:  Here is a simple inline link:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/uri "title")"""
    expected_tokens = [
        "[para:]",
        "[link:/uri:title]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/uri" title="title">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_494():
    """
    Test case 494:  The title may be omitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/uri)"""
    expected_tokens = [
        "[para:]",
        "[link:/uri:]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/uri">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_495():
    """
    Test case 495:  (part 1) Both the title and the destination may be omitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link]()"""
    expected_tokens = [
        "[para:]",
        "[link::]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_496():
    """
    Test case 496:  (part 2) Both the title and the destination may be omitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](<>)"""
    expected_tokens = [
        "[para:]",
        "[link::]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_497():
    """
    Test case 497:  (part 1) The destination can only contain spaces if it is enclosed in pointy brackets
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/my uri)"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text:(/my uri):]",
        "[end-para]",
    ]
    expected_gfm = """<p>[link](/my uri)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_498():
    """
    Test case 498:  (part 2) The destination can only contain spaces if it is enclosed in pointy brackets
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](</my uri>)"""
    expected_tokens = [
        "[para:]",
        "[link:/my%20uri:]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/my%20uri">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_499():
    """
    Test case 499:  (part 1) The destination cannot contain line breaks, even if enclosed in pointy brackets:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<p>[link](foo
bar)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_500():
    """
    Test case 500:  (part 2) The destination cannot contain line breaks, even if enclosed in pointy brackets:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<p>[link](<foo
bar>)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_501():
    """
    Test case 501:  The destination can contain ) if it is enclosed in pointy brackets:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[a](<b)c>)"""
    expected_tokens = [
        "[para:]",
        "[link:b)c:]",
        "[text:a:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="b)c">a</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_502():
    """
    Test case 502:  Pointy brackets that enclose links must be unescaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](<foo\\>)"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text:(&lt;foo&gt;):]",
        "[end-para]",
    ]
    expected_gfm = """<p>[link](&lt;foo&gt;)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_503():
    """
    Test case 503:  These are not links, because the opening pointy bracket is not matched properly:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[a](<b)c
[a](<b)c>
[a](<b>c)"""
    expected_tokens = [
        "[para:\n\n]",
        "[text:[:]",
        "[text:a:]",
        "[text:]:]",
        "[text:(&lt;b)c\n::\n]",
        "[text:[:]",
        "[text:a:]",
        "[text:]:]",
        "[text:(&lt;b)c&gt;\n::\n]",
        "[text:[:]",
        "[text:a:]",
        "[text:]:]",
        "[text:(:]",
        "[raw-html:b]",
        "[text:c):]",
        "[end-para]",
    ]
    expected_gfm = """<p>[a](&lt;b)c
[a](&lt;b)c&gt;
[a](<b>c)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_504():
    """
    Test case 504:  Parentheses inside the link destination may be escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](\\(foo\\))"""
    expected_tokens = [
        "[para:]",
        "[link:(foo):]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="(foo)">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_505():
    """
    Test case 505:  Any number of parentheses are allowed without escaping, as long as they are balanced:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](foo(and(bar)))"""
    expected_tokens = [
        "[para:]",
        "[link:foo(and(bar)):]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="foo(and(bar))">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_506():
    """
    Test case 506:  (part 1) However, if you have unbalanced parentheses, you need to escape or use the <...> form:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](foo\\(and\\(bar\\))"""
    expected_tokens = [
        "[para:]",
        "[link:foo(and(bar):]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="foo(and(bar)">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_507():
    """
    Test case 507:  (part 2) However, if you have unbalanced parentheses, you need to escape or use the <...> form:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](<foo(and(bar)>)"""
    expected_tokens = [
        "[para:]",
        "[link:foo(and(bar):]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="foo(and(bar)">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_507b():
    """
    Test case 507b:  Modification of 507 without the angle brackets.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](foo(and(bar))"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text:(foo(and(bar)):]",
        "[end-para]",
    ]
    expected_gfm = """<p>[link](foo(and(bar))</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_507c():
    """
    Test case 507c:  Modification of 507 without the angle brackets, and more open
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](foo(and(b(ar))"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text:(foo(and(b(ar)):]",
        "[end-para]",
    ]
    expected_gfm = """<p>[link](foo(and(b(ar))</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_508():
    """
    Test case 508:  Parentheses and other symbols can also be escaped, as usual in Markdown:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](foo\\)\\:)"""
    expected_tokens = [
        "[para:]",
        "[link:foo)::]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="foo):">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_509():
    """
    Test case 509:  A link can contain fragment identifiers and queries:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](#fragment)

[link](http://example.com#fragment)

[link](http://example.com?foo=3#frag)"""
    expected_tokens = [
        "[para:]",
        "[link:#fragment:]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[link:http://example.com#fragment:]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[link:http://example.com?foo=3#frag:]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="#fragment">link</a></p>
<p><a href="http://example.com#fragment">link</a></p>
<p><a href="http://example.com?foo=3#frag">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_510():
    """
    Test case 510:  Note that a backslash before a non-escapable character is just a backslash:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](foo\\bar)"""
    expected_tokens = [
        "[para:]",
        "[link:foo%5Cbar:]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="foo%5Cbar">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_511():
    """
    Test case 511:  URL-escaping should be left alone inside the destination
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](foo%20b&auml;)"""
    expected_tokens = [
        "[para:]",
        "[link:foo%20b%C3%A4:]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="foo%20b%C3%A4">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_512():
    """
    Test case 512:  Note that, because titles can often be parsed as destinations, if you try to omit the destination and keep the title, you’ll get unexpected results:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link]("title")"""
    expected_tokens = [
        "[para:]",
        "[link:%22title%22:]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="%22title%22">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_513():
    """
    Test case 513:  Titles may be in single quotes, double quotes, or parentheses:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/url "title")
[link](/url 'title')
[link](/url (title))"""
    expected_tokens = [
        "[para:\n\n]",
        "[link:/url:title]",
        "[text:link:]",
        "[end-link::]",
        "[text:\n::\n]",
        "[link:/url:title]",
        "[text:link:]",
        "[end-link::]",
        "[text:\n::\n]",
        "[link:/url:title]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/url" title="title">link</a>
<a href="/url" title="title">link</a>
<a href="/url" title="title">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_514():
    """
    Test case 514:  Backslash escapes and entity and numeric character references may be used in titles:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/url "title \\"&quot;")"""
    expected_tokens = [
        "[para:]",
        "[link:/url:title &quot;&quot;]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/url" title="title &quot;&quot;">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_515():
    """
    Test case 515:  Titles must be separated from the link using a whitespace. Other Unicode whitespace like non-breaking space doesn’t work.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/url\u00A0"title")"""
    expected_tokens = [
        "[para:]",
        "[link:/url%C2%A0%22title%22:]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/url%C2%A0%22title%22">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_515b():
    """
    Test case 515b:  Modification of 515 to use normal space and remove closing quotes.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/url "title)"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text:(/url &quot;title):]",
        "[end-para]",
    ]
    expected_gfm = """<p>[link](/url &quot;title)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_515c():
    """
    Test case 515c:  Modification of 515 to use normal space and remove closing quotes.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/url (title))"""
    expected_tokens = [
        "[para:]",
        "[link:/url:title]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/url" title="title">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_515d():
    """
    Test case 515d:  Modification of 515 to use normal space and remove closing quotes.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/url (title)"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text:(/url (title):]",
        "[end-para]",
    ]
    expected_gfm = """<p>[link](/url (title)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_515e():
    """
    Test case 515e:  Modification of 515 to use normal space and remove closing quotes.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/url (title(other)line))"""
    expected_tokens = [
        "[para:]",
        "[link:/url:title(other)line]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/url" title="title(other)line">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_515f():
    """
    Test case 515e:  Modification of 515 to use normal space and remove closing quotes.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/url (title(other)line)) abc"""
    expected_tokens = [
        "[para:]",
        "[link:/url:title(other)line]",
        "[text:link:]",
        "[end-link::]",
        "[text: abc:]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/url" title="title(other)line">link</a> abc</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_515g():
    """
    Test case 515e:  Modification of 515 to use normal space and remove closing quotes.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/url (title(otherline) abc"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text:(/url (title(otherline) abc:]",
        "[end-para]",
    ]
    expected_gfm = """<p>[link](/url (title(otherline) abc</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_516():
    """
    Test case 516:  Nested balanced quotes are not allowed without escaping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/url "title "and" title")"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text:(/url &quot;title &quot;and&quot; title&quot;):]",
        "[end-para]",
    ]
    expected_gfm = """<p>[link](/url &quot;title &quot;and&quot; title&quot;)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_517():
    """
    Test case 517:  But it is easy to work around this by using a different quote type:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](/url 'title "and" title')"""
    expected_tokens = [
        "[para:]",
        "[link:/url:title &quot;and&quot; title]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = (
        """<p><a href="/url" title="title &quot;and&quot; title">link</a></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_518():
    """
    Test case 518:  Whitespace is allowed around the destination and title:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link](   /uri
  "title"  )"""
    expected_tokens = [
        "[para:\n  ]",
        "[link:/uri:title]",
        "[text:link:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/uri" title="title">link</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_519():
    """
    Test case 519:  But it is not allowed between the link text and the following parenthesis:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link] (/uri)"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link:]",
        "[text:]:]",
        "[text: (/uri):]",
        "[end-para]",
    ]
    expected_gfm = """<p>[link] (/uri)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_520():
    """
    Test case 520:  (part 1) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link [foo [bar]]](/uri)"""
    expected_tokens = [
        "[para:]",
        "[link:/uri:]",
        "[text:link :]",
        "[text:[:]",
        "[text:foo :]",
        "[text:[:]",
        "[text:bar:]",
        "[text:]:]",
        "[text:]:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/uri">link [foo [bar]]</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_521():
    """
    Test case 521:  (part 2) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<p>[link] bar](/uri)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_522():
    """
    Test case 522:  (part 3) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link [bar](/uri)"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:link :]",
        "[link:/uri:]",
        "[text:bar:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p>[link <a href="/uri">bar</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_523():
    """
    Test case 523:  (part 4) The link text may contain balanced brackets, but not unbalanced ones, unless they are escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link \\[bar](/uri)"""
    expected_tokens = [
        "[para:]",
        "[link:/uri:]",
        "[text:link [bar:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/uri">link [bar</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_524():
    """
    Test case 524:  (part 1) The link text may contain inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[link *foo **bar** `#`*](/uri)"""
    expected_tokens = [
        "[para:]",
        "[link:/uri:]",
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
    ]
    expected_gfm = """<p><a href="/uri">link <em>foo <strong>bar</strong> <code>#</code></em></a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.skip
@pytest.mark.gfm
def test_inline_links_525():
    """
    Test case 525:  (part 2) The link text may contain inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[![moon](moon.jpg)](/uri)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]
    expected_gfm = """<p><a href="/uri"><img src="moon.jpg" alt="moon" /></a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_526():
    """
    Test case 526:  (part 1) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo [bar](/uri)](/uri)"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:foo :]",
        "[link:/uri:]",
        "[text:bar:]",
        "[end-link::]",
        "[text:]:]",
        "[text:(/uri):]",
        "[end-para]",
    ]
    expected_gfm = """<p>[foo <a href="/uri">bar</a>](/uri)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_527():
    """
    Test case 527:  (part 2) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo *[bar [baz](/uri)](/uri)*](/uri)"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:foo :]",
        "[emphasis:1]",
        "[text:[:]",
        "[text:bar :]",
        "[link:/uri:]",
        "[text:baz:]",
        "[end-link::]",
        "[text:]:]",
        "[text:(/uri):]",
        "[end-emphasis::1]",
        "[text:]:]",
        "[text:(/uri):]",
        "[end-para]",
    ]
    expected_gfm = """<p>[foo <em>[bar <a href="/uri">baz</a>](/uri)</em>](/uri)</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.skip
@pytest.mark.gfm
def test_inline_links_528():
    """
    Test case 528:  (part 3) However, links may not contain other links, at any level of nesting.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """![[[foo](uri1)](uri2)](uri3)"""
    expected_tokens = [
        "[ulist:-::2:]",
    ]
    expected_gfm = """<p><img src="uri3" alt="[foo](uri2)" /></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_529():
    """
    Test case 529:  (part 1) These cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*[foo*](/uri)"""
    expected_tokens = [
        "[para:]",
        "[text:*:]",
        "[link:/uri:]",
        "[text:foo:]",
        "[text:*:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p>*<a href="/uri">foo*</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_530():
    """
    Test case 530:  (part 2) These cases illustrate the precedence of link text grouping over emphasis grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo *bar](baz*)"""
    expected_tokens = [
        "[para:]",
        "[link:baz*:]",
        "[text:foo :]",
        "[text:*:]",
        "[text:bar:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="baz*">foo *bar</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_531():
    """
    Test case 531:  Note that brackets that aren’t part of links do not take precedence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """*foo [bar* baz]"""
    expected_tokens = [
        "[para:]",
        "[emphasis:1]",
        "[text:foo :]",
        "[text:[:]",
        "[text:bar:]",
        "[end-emphasis::1]",
        "[text: baz:]",
        "[text:]:]",
        "[end-para]",
    ]
    expected_gfm = """<p><em>foo [bar</em> baz]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_532():
    """
    Test case 532:  (part 1) These cases illustrate the precedence of HTML tags, code spans, and autolinks over link grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo <bar attr="](baz)">"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:foo :]",
        '[raw-html:bar attr="](baz)"]',
        "[end-para]",
    ]
    expected_gfm = """<p>[foo <bar attr="](baz)"></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_533():
    """
    Test case 533:  (part 2) These cases illustrate the precedence of HTML tags, code spans, and autolinks over link grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo`](/uri)`"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:foo:]",
        "[icode-span:](/uri)]",
        "[end-para]",
    ]
    expected_gfm = """<p>[foo<code>](/uri)</code></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_inline_links_534():
    """
    Test case 534:  (part 3) These cases illustrate the precedence of HTML tags, code spans, and autolinks over link grouping:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo<http://example.com/?search=](uri)>"""
    expected_tokens = [
        "[para:]",
        "[text:[:]",
        "[text:foo:]",
        "[uri-autolink:http://example.com/?search=](uri)]",
        "[end-para]",
    ]
    expected_gfm = """<p>[foo<a href="http://example.com/?search=%5D(uri)">http://example.com/?search=](uri)</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
