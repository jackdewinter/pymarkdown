"""
https://github.github.com/gfm/#precedence
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_tabs_001():
    """
    Test case 001:  (part a) a tab can be used instead of four spaces in an indented code block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """\tfoo\tbaz\t\tbim"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:foo    baz        bim:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_002():
    """
    Test case 002:  (part b) a tab can be used instead of four spaces in an indented code block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """  \tfoo\tbaz\t\tbim"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:foo    baz        bim:  ]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_003():
    """
    Test case 003:  (part c) a tab can be used instead of four spaces in an indented code block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    a\ta
    ὐ\ta"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:a    a\n    ὐ    a:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_004():
    """
    Test case 004:  (part a) a continuation paragraph of a list item is indented with a tab; this has exactly the same effect as indentation with four spaces would
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """  - foo

\tbar"""  # noqa: E101,W191
    # noqa: E101,W191
    expected_tokens = [
        "[ulist:-::4:  ]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_005():
    """
    Test case 005:  (part b) a continuation paragraph of a list item is indented with a tab; this has exactly the same effect as indentation with four spaces would
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo

\t\tbar"""  # noqa: E101,W191
    # noqa: E101,W191
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:bar:  ]",
        "[end-icode-block]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_006():
    """
    Test case 006:  case > is followed by a tab, which is treated as if it were expanded into three spaces.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """>\t\tfoo"""
    expected_tokens = [
        "[block-quote:]",
        "[icode-block:    ]",
        "[text:foo:   ]",
        "[end-icode-block]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_007():
    """
    Test case 007:  none
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """-\t\tfoo"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[icode-block:    ]",
        "[text:foo:   ]",
        "[end-icode-block]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_008():
    """
    Test case 008:  none
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    foo
\tbar"""  # noqa: E101,W191
    # noqa: E101
    expected_tokens = [
        "[icode-block:    ]",
        "[text:foo\n    bar:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_009():
    """
    Test case 009:  none
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """ - foo
   - bar
\t - baz"""  # noqa: E101,W191
    # noqa: E101
    expected_tokens = [
        "[ulist:-::3: ]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[ulist:-::5:   ]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[ulist:-::7:     ]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_010():
    """
    Test case 010:  none
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """#\tFoo"""
    expected_tokens = ["[atx:1:Foo::    ::]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_011():
    """
    Test case 011:  none
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*\t*\t*\t"""
    expected_tokens = ["[tbreak:*::*    *    *    ]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
