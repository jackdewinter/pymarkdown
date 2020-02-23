"""
https://github.github.com/gfm/#hard-line-breaks
"""

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_hard_line_breaks_654():
    """
    Test case 654:  A line break (not in a code span or HTML tag) that is preceded by two or more spaces and does not occur at the end of a block is parsed as a hard line break (rendered in HTML as a <br /> tag):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo\a\a
baz""".replace("\a", " ")
    expected_tokens = ['[para:\n]', '[text:foo:]', '[hard-break]', '[text:\nbaz::  \n]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_hard_line_breaks_655():
    """
    Test case 655:  For a more visible alternative, a backslash before the line ending may be used instead of two spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo\\
baz"""
    expected_tokens = ['[para:\n]', '[text:foo:]', '[hard-break]', '[text:\nbaz:]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_hard_line_breaks_656():
    """
    Test case 656:  More than two spaces can be used:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo\a\a\a\a\a\a\a
baz""".replace("\a", " ")
    expected_tokens = ['[para:\n]', '[text:foo:]', '[hard-break]', '[text:\nbaz::       \n]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_hard_line_breaks_657():
    """
    Test case 657:  (part 1) Leading spaces at the beginning of the next line are ignored:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo\a\a
     bar""".replace("\a", " ")
    expected_tokens = ['[para:\n     ]', '[text:foo:]', '[hard-break]', '[text:\nbar::  \n]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_hard_line_breaks_658():
    """
    Test case 658:  (part 2) Leading spaces at the beginning of the next line are ignored:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo\\
     bar"""
    expected_tokens = ['[para:\n     ]', '[text:foo:]', '[hard-break]', '[text:\nbar:]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_hard_line_breaks_659():
    """
    Test case 659:  (part 1) Line breaks can occur inside emphasis, links, and other constructs that allow inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*foo\a\a
bar*""".replace("\a", " ")
    expected_tokens = ['[para:\n]', '[text:*foo:]', '[hard-break]', '[text:\nbar*::  \n]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_hard_line_breaks_660():
    """
    Test case 660:  (part 2) Line breaks can occur inside emphasis, links, and other constructs that allow inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*foo\\
bar*""".replace("\a", " ")
    expected_tokens = ['[para:\n]', '[text:*foo:]', '[hard-break]', '[text:\nbar*:]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_hard_line_breaks_661():
    """
    Test case 661:  (part 1) Line breaks do not occur inside code spans
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`code\a\a
span`""".replace("\a", " ")
    expected_tokens = ['[para:\n]', '[icode-span:code   span]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_hard_line_breaks_662():
    """
    Test case 662:  (part 2) Line breaks do not occur inside code spans
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`code\\
span`"""
    expected_tokens = ['[para:\n]', '[icode-span:code\\ span]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_hard_line_breaks_663():
    """
    Test case 663:  (part 1) or HTML tags:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<a href="foo  
bar">""".replace("\a", " ")
    expected_tokens = ['[para:\n]', '[text:&lt;a href=&quot;foo:]', '[hard-break]', '[text:\nbar&quot;&gt;::  \n]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO will change when raw html implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_hard_line_breaks_664():
    """
    Test case 664:  (part 2) or HTML tags:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<a href="foo\\
bar">"""
    expected_tokens = ['[para:\n]', '[text:&lt;a href=&quot;foo:]', '[hard-break]', '[text:\nbar&quot;&gt;:]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO will change when raw html implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_hard_line_breaks_665():
    """
    Test case 665:  (part 1) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo\\"""
    expected_tokens = ['[para:]', '[text:foo\\:]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_hard_line_breaks_666():
    """
    Test case 666:  (part 2) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo  """
    expected_tokens =  ['[para::  ]', '[text:foo:]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_hard_line_breaks_667():
    """
    Test case 667:  (part 3) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """### foo\\"""
    expected_tokens = ['[atx:3:0:]', '[text:foo\\: ]', '[end-atx::]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

def test_hard_line_breaks_668():
    """
    Test case 668:  (part 4) Neither syntax for hard line breaks works at the end of a paragraph or other block element:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """### foo  """
    expected_tokens = ['[atx:3:0:]', '[text:foo: ]', '[end-atx:  :]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)

