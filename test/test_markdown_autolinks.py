"""
https://github.github.com/gfm/#autolinks
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_autolinks_602():
    """
    Test case 602:  (part 1) Here are some valid autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<http://foo.bar.baz>"""
    expected_tokens = ["[para:]", "[uri-autolink:http://foo.bar.baz]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_603():
    """
    Test case 603:  (part 2) Here are some valid autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<http://foo.bar.baz/test?q=hello&id=22&boolean>"""
    expected_tokens = [
        "[para:]",
        "[uri-autolink:http://foo.bar.baz/test?q=hello&id=22&boolean]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_604():
    """
    Test case 604:  (part 3) Here are some valid autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<irc://foo.bar:2233/baz>"""
    expected_tokens = ["[para:]", "[uri-autolink:irc://foo.bar:2233/baz]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_605():
    """
    Test case 605:  Uppercase is also fine
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<MAILTO:FOO@BAR.BAZ>"""
    expected_tokens = ["[para:]", "[uri-autolink:MAILTO:FOO@BAR.BAZ]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_606():
    """
    Test case 606:  (part 1) Note that many strings that count as absolute URIs for purposes of this spec are not valid URIs, because their schemes are not registered or because of other problems with their syntax:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<a+b+c:d>"""
    expected_tokens = ["[para:]", "[uri-autolink:a+b+c:d]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_607():
    """
    Test case 607:  (part 2) Note that many strings that count as absolute URIs for purposes of this spec are not valid URIs, because their schemes are not registered or because of other problems with their syntax:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<made-up-scheme://foo,bar>"""
    expected_tokens = [
        "[para:]",
        "[uri-autolink:made-up-scheme://foo,bar]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_608():
    """
    Test case 608:  (part 3) Note that many strings that count as absolute URIs for purposes of this spec are not valid URIs, because their schemes are not registered or because of other problems with their syntax:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<http://../>"""
    expected_tokens = ["[para:]", "[uri-autolink:http://../]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_609():
    """
    Test case 609:  (part 4) Note that many strings that count as absolute URIs for purposes of this spec are not valid URIs, because their schemes are not registered or because of other problems with their syntax:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<localhost:5001/foo>"""
    expected_tokens = ["[para:]", "[uri-autolink:localhost:5001/foo]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_610():
    """
    Test case 610:  Spaces are not allowed in autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<http://foo.bar/baz bim>"""
    expected_tokens = [
        "[para:]",
        "[text:&lt;http://foo.bar/baz bim&gt;:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_611():
    """
    Test case 611:  Backslash-escapes do not work inside autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<http://example.com/\\[\\>"""
    expected_tokens = [
        "[para:]",
        "[uri-autolink:http://example.com/\\[\\]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_612():
    """
    Test case 612:  (part 1) Examples of email autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<foo@bar.example.com>"""
    expected_tokens = ["[para:]", "[email-autolink:foo@bar.example.com]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_613():
    """
    Test case 613:  (part 2) Examples of email autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<foo+special@Bar.baz-bar0.com>"""
    expected_tokens = [
        "[para:]",
        "[email-autolink:foo+special@Bar.baz-bar0.com]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_614():
    """
    Test case 614:  Backslash-escapes do not work inside email autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<foo\\+@bar.example.com>"""
    expected_tokens = ["[para:]", "[text:&lt;foo+@bar.example.com&gt;:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_615():
    """
    Test case 615:  (part 1) These are not autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<>"""
    expected_tokens = ["[para:]", "[text:&lt;&gt;:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_616():
    """
    Test case 616:  (part 2) These are not autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """< http://foo.bar >"""
    expected_tokens = ["[para:]", "[text:&lt; http://foo.bar &gt;:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_617():
    """
    Test case 617:  (part 3) These are not autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<m:abc>"""
    expected_tokens = ["[para:]", "[text:&lt;m:abc&gt;:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_618():
    """
    Test case 618:  (part 4) These are not autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<foo.bar.baz>"""
    expected_tokens = ["[para:]", "[text:&lt;foo.bar.baz&gt;:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_619():
    """
    Test case 619:  (part 5) These are not autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """http://example.com"""
    expected_tokens = ["[para:]", "[text:http://example.com:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_autolinks_620():
    """
    Test case 620:  (part 6) These are not autolinks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo@bar.example.com"""
    expected_tokens = ["[para:]", "[text:foo@bar.example.com:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
