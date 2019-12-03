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
    source_markdown = """	foo	baz		bim"""
    expected_tokens = [
        "[icode-block:\t]",
        "[text:foo\tbaz\t\tbim:]",
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
    source_markdown = """  	foo	baz		bim"""
    expected_tokens = [
        "[icode-block:  \t]",
        "[text:foo\tbaz\t\tbim:]",
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
    source_markdown = """    a	a
    ὐ	a"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:a\ta:]",
        "[text:ὐ\ta:    ]",
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

	bar"""  # noqa: E101,W191
    # noqa: E101,W191
    expected_tokens = [
        "[para:  ]",
        "[text:- foo:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:\t]",
        "[text:bar:]",
        "[end-icode-block]",
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

		bar"""  # noqa: E101,W191
    # noqa: E101,W191
    expected_tokens = [
        "[para:]",
        "[text:- foo:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:\t\t]",
        "[text:bar:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when list blocks implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_006():
    """
    Test case 006:  case > is followed by a tab, which is treated as if it were expanded into three spaces.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """>		foo"""
    expected_tokens = ["[para:]", "[text:>\t\tfoo:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when block quotes implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_007():
    """
    Test case 007:  none
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """-		foo"""
    expected_tokens = ["[para:]", "[text:-\t\tfoo:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when list blocks implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_008():
    """
    Test case 008:  none
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    foo
	bar"""  # noqa: E101,W191
    # noqa: E101
    expected_tokens = [
        "[icode-block:    ]",
        "[text:foo:]",
        "[text:bar:\t]",
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
	- baz"""  # noqa: E101,W191
    # noqa: E101
    expected_tokens = [
        "[para: ]",
        "[text:- foo:]",
        "[text:- bar:   ]",
        "[text:- baz:\t]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when list blocks implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_tabs_010():
    """
    Test case 010:  none
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """#	Foo"""
    expected_tokens = ["[atx:1:Foo::\t::]"]

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
    source_markdown = """*	*	*	"""
    expected_tokens = ["[tbreak:*::*\t*\t*\t]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
