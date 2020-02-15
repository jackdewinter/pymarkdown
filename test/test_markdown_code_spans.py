"""
https://github.github.com/gfm/#code-spans
"""

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_code_spans_338():
    """
    Test case 338:  This is a simple code span:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`foo`"""
    expected_tokens = [
        "[para:]",
        "[icode-span:foo]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_339():
    """
    Test case 339:  Here two backticks are used, because the code contains a backtick. This example also illustrates stripping of a single leading and trailing space:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`` foo ` bar ``"""
    expected_tokens = [
        "[para:]",
        "[icode-span:foo ` bar]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_340():
    """
    Test case 340:  This example shows the motivation for stripping leading and trailing spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`  ``  `"""
    expected_tokens = [
        "[para:]",
        "[icode-span: `` ]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_341():
    """
    Test case 341:  Note that only one space is stripped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`  ``  `"""
    expected_tokens = [
        "[para:]",
        "[icode-span: `` ]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_342():
    """
    Test case 342:  The stripping only happens if the space is on both sides of the string:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """` a`"""
    expected_tokens = [
        "[para:]",
        "[icode-span: a]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_343():
    """
    Test case 343:  Only spaces, and not unicode whitespace in general, are stripped in this way:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`\u00A0b\u00A0`"""
    expected_tokens = [
        "[para:]",
        "[icode-span:\u00A0b\u00A0]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_344():
    """
    Test case 344:  No stripping occurs if the code span contains only spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """` `
`  `"""
    expected_tokens = [
        "[para:]",
        "[icode-span: ]",
        """[text:
:]""",
        "[icode-span:  ]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_344a():
    """
    Test case 344a:  Extension of 344 with a whitespace string that is longer than 2.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`   `"""
    expected_tokens = [
        "[para:]",
        "[icode-span:   ]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_345():
    """
    Test case 345:  (part 1) Line endings are treated like spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """``
foo
bar  
baz
``"""
    expected_tokens = [
        "[para:]",
        "[icode-span:foo bar   baz]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_346():
    """
    Test case 346:  (part 2) Line endings are treated like spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """``
foo 
``"""
    expected_tokens = [
        "[para:]",
        "[icode-span:foo ]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_347():
    """
    Test case 347:  Interior spaces are not collapsed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    # pylint: disable=trailing-whitespace
    source_markdown = """`foo   bar 
baz`"""
    # pylint: enable=trailing-whitespace
    expected_tokens = [
        "[para:]",
        "[icode-span:foo   bar  baz]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_348():
    """
    Test case 348:  Note that backslash escapes do not work in code spans. All backslashes are treated literally:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`foo\\`bar`"""
    expected_tokens = [
        "[para:]",
        "[icode-span:foo\\]",
        "[text:bar`:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_349():
    """
    Test case 349:  (part 1) Backslash escapes are never needed, because one can always choose a string of n backtick characters as delimiters, where the code does not contain any strings of exactly n backtick characters.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """``foo`bar``"""
    expected_tokens = [
        "[para:]",
        "[icode-span:foo`bar]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_350():
    """
    Test case 350:  (part 2) Backslash escapes are never needed, because one can always choose a string of n backtick characters as delimiters, where the code does not contain any strings of exactly n backtick characters.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """` foo `` bar `"""
    expected_tokens = [
        "[para:]",
        "[icode-span:foo `` bar]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_351():
    """
    Test case 351:  Code span backticks have higher precedence than any other inline constructs except HTML tags and autolinks.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*foo`*`"""
    expected_tokens = [
        "[para:]",
        "[text:*foo:]",
        "[icode-span:*]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_352():
    """
    Test case 352:  And this is not parsed as a link:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[not a `link](/foo`)"""
    expected_tokens = [
        "[para:]",
        "[text:[not a :]",
        "[icode-span:link](/foo]",
        "[text:):]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_353():
    """
    Test case 353:  Code spans, HTML tags, and autolinks have the same precedence. Thus, this is code:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`<a href="`">`"""
    expected_tokens = [
        "[para:]",
        "[icode-span:&lt;a href=&quot;]",
        "[text:&quot;&gt;`:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_354():
    """
    Test case 354:  But this is an HTML tag:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<a href="`">`"""
    expected_tokens = [
        "[para:]",
        "[text:&lt;a href=&quot;:]",
        "[icode-span:&quot;&gt;]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO will fail when raw html
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_355():
    """
    Test case 355:  And this is code:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`<http://foo.bar.`baz>`"""
    expected_tokens = [
        "[para:]",
        "[icode-span:&lt;http://foo.bar.]",
        "[text:baz&gt;`:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_356():
    """
    Test case 356:  But this is an autolink:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<http://foo.bar.`baz>`"""
    expected_tokens = [
        "[para:]",
        "[text:&lt;http://foo.bar.:]",
        "[icode-span:baz&gt;]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO will fail when autolinks
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_357():
    """
    Test case 357:  (part 1) When a backtick string is not closed by a matching backtick string, we just have literal backticks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """```foo``"""
    expected_tokens = [
        "[para:]",
        "[text:```foo``:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_358():
    """
    Test case 358:  (part 2) When a backtick string is not closed by a matching backtick string, we just have literal backticks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`foo"""
    expected_tokens = [
        "[para:]",
        "[text:`foo:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_code_spans_359():
    """
    Test case 359:  The following case also illustrates the need for opening and closing backtick strings to be equal in length:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`foo``bar``"""
    expected_tokens = [
        "[para:]",
        "[text:`foo:]",
        "[icode-span:bar]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
