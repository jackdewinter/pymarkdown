"""
https://github.github.com/gfm/#autolinks
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    assert_if_lists_different,
    assert_if_strings_different,
    assert_token_consistency,
)


@pytest.mark.gfm
def test_autolinks_602():
    """
    Test case 602:  (part 1) Here are some valid autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<http://foo.bar.baz>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink:http://foo.bar.baz]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="http://foo.bar.baz">http://foo.bar.baz</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_603():
    """
    Test case 603:  (part 2) Here are some valid autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<http://foo.bar.baz/test?q=hello&id=22&boolean>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink:http://foo.bar.baz/test?q=hello&id=22&boolean]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="http://foo.bar.baz/test?q=hello&amp;id=22&amp;boolean">http://foo.bar.baz/test?q=hello&amp;id=22&amp;boolean</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_604():
    """
    Test case 604:  (part 3) Here are some valid autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<irc://foo.bar:2233/baz>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink:irc://foo.bar:2233/baz]",
        "[end-para]",
    ]
    expected_gfm = (
        """<p><a href="irc://foo.bar:2233/baz">irc://foo.bar:2233/baz</a></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_605():
    """
    Test case 605:  Uppercase is also fine
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<MAILTO:FOO@BAR.BAZ>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink:MAILTO:FOO@BAR.BAZ]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="MAILTO:FOO@BAR.BAZ">MAILTO:FOO@BAR.BAZ</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_606():
    """
    Test case 606:  (part 1) Note that many strings that count as absolute URIs for purposes of this spec are not valid URIs, because their schemes are not registered or because of other problems with their syntax:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a+b+c:d>"""
    expected_tokens = ["[para(1,1):]", "[uri-autolink:a+b+c:d]", "[end-para]"]
    expected_gfm = """<p><a href="a+b+c:d">a+b+c:d</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_607():
    """
    Test case 607:  (part 2) Note that many strings that count as absolute URIs for purposes of this spec are not valid URIs, because their schemes are not registered or because of other problems with their syntax:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<made-up-scheme://foo,bar>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink:made-up-scheme://foo,bar]",
        "[end-para]",
    ]
    expected_gfm = (
        """<p><a href="made-up-scheme://foo,bar">made-up-scheme://foo,bar</a></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_608():
    """
    Test case 608:  (part 3) Note that many strings that count as absolute URIs for purposes of this spec are not valid URIs, because their schemes are not registered or because of other problems with their syntax:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<http://../>"""
    expected_tokens = ["[para(1,1):]", "[uri-autolink:http://../]", "[end-para]"]
    expected_gfm = """<p><a href="http://../">http://../</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_609():
    """
    Test case 609:  (part 4) Note that many strings that count as absolute URIs for purposes of this spec are not valid URIs, because their schemes are not registered or because of other problems with their syntax:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<localhost:5001/foo>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink:localhost:5001/foo]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="localhost:5001/foo">localhost:5001/foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_610():
    """
    Test case 610:  Spaces are not allowed in autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<http://foo.bar/baz bim>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:&lt;http://foo.bar/baz bim&gt;:]",
        "[end-para]",
    ]
    expected_gfm = """<p>&lt;http://foo.bar/baz bim&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_611prime():
    """
    Test case 611:  Backslash-escapes do not work inside autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<http://example.com/\\[\\>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink:http://example.com/\\[\\]",
        "[end-para]",
    ]
    expected_gfm = (
        """<p><a href="http://example.com/%5C%5B%5C">http://example.com/\\[\\</a></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_611a():
    """
    Test case 611a:  Backslash-escapes do not work inside autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<http://example.com/\u2122\u20AC>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink:http://example.com/™€]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="http://example.com/%E2%84%A2%E2%82%AC">http://example.com/™€</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_611b():
    """
    Test case 611b:  Backslash-escapes do not work inside autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<http://abcdefjhijklmnopqrstuvwxyz!"#$%&'()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`{}|~ABC>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink:http://abcdefjhijklmnopqrstuvwxyz!\"#$%&'()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`{}|~ABC]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="http://abcdefjhijklmnopqrstuvwxyz!%22#$%25&amp;'()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ%5B%5C%5D%5E_%60%7B%7D%7C~ABC">http://abcdefjhijklmnopqrstuvwxyz!&quot;#$%&amp;'()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`{}|~ABC</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_612():
    """
    Test case 612:  (part 1) Examples of email autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<foo@bar.example.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink:foo@bar.example.com]",
        "[end-para]",
    ]
    expected_gfm = (
        """<p><a href="mailto:foo@bar.example.com">foo@bar.example.com</a></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_613():
    """
    Test case 613:  (part 2) Examples of email autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<foo+special@Bar.baz-bar0.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[email-autolink:foo+special@Bar.baz-bar0.com]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="mailto:foo+special@Bar.baz-bar0.com">foo+special@Bar.baz-bar0.com</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_614():
    """
    Test case 614:  Backslash-escapes do not work inside email autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<foo\\+@bar.example.com>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:&lt;foo+@bar.example.com&gt;:]",
        "[end-para]",
    ]
    expected_gfm = """<p>&lt;foo+@bar.example.com&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_615():
    """
    Test case 615:  (part 1) These are not autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<>"""
    expected_tokens = ["[para(1,1):]", "[text:&lt;&gt;:]", "[end-para]"]
    expected_gfm = """<p>&lt;&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_616():
    """
    Test case 616:  (part 2) These are not autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """< http://foo.bar >"""
    expected_tokens = ["[para(1,1):]", "[text:&lt; http://foo.bar &gt;:]", "[end-para]"]
    expected_gfm = """<p>&lt; http://foo.bar &gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_617():
    """
    Test case 617:  (part 3) These are not autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<m:abc>"""
    expected_tokens = ["[para(1,1):]", "[text:&lt;m:abc&gt;:]", "[end-para]"]
    expected_gfm = """<p>&lt;m:abc&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_618():
    """
    Test case 618:  (part 4) These are not autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<foo.bar.baz>"""
    expected_tokens = ["[para(1,1):]", "[text:&lt;foo.bar.baz&gt;:]", "[end-para]"]
    expected_gfm = """<p>&lt;foo.bar.baz&gt;</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_619():
    """
    Test case 619:  (part 5) These are not autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """http://example.com"""
    expected_tokens = ["[para(1,1):]", "[text:http://example.com:]", "[end-para]"]
    expected_gfm = """<p>http://example.com</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_autolinks_620():
    """
    Test case 620:  (part 6) These are not autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo@bar.example.com"""
    expected_tokens = ["[para(1,1):]", "[text:foo@bar.example.com:]", "[end-para]"]
    expected_gfm = """<p>foo@bar.example.com</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
