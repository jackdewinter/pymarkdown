"""
https://github.github.com/gfm/#tables-extension-
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different, assert_token_consistency


def test_tables_extension_198():
    """
    Test case 198:  The delimiter row consists of cells whose only content are hyphens (-), and optionally, a leading or trailing colon (:), or both, to indicate left, right, or center alignment respectively.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """| foo | bar |
| --- | --- |
| baz | bim |"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| foo | bar |\n| --- | --- |\n| baz | bim |::\n\n]",
        "[end-para:::True]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when tables are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_token_consistency(source_markdown, actual_tokens)


def test_tables_extension_199():
    """
    Test case 199:  Cells in one column don’t need to match length, though it’s easier to read if they are. Likewise, use of leading and trailing pipes may be inconsistent:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """| abc | defghi |
:-: | -----------:
bar | baz"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| abc | defghi |\n:-: | -----------:\nbar | baz::\n\n]",
        "[end-para:::True]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when tables are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_token_consistency(source_markdown, actual_tokens)


def test_tables_extension_200():
    """
    Test case 200:  Include a pipe in a cell’s content by escaping it, including inside other inline spans:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """| f\\|oo  |
| ------ |
| b `\\|` az |
| b **\\|** im |"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):| f\\\b|oo  |\n| ------ |\n| b ::\n\n]",
        "[icode-span(3,5):\\|:`::]",
        "[text(3,9): az |\n| b ::\n]",
        "[emphasis(4,5):2:*]",
        "[text(4,7):\\\b|:]",
        "[end-emphasis(4,9)::2:*:False]",
        "[text(4,11): im |:]",
        "[end-para:::True]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when tables are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_token_consistency(source_markdown, actual_tokens)


def test_tables_extension_201():
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
> bar"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| abc | def |\n| --- | --- |\n| bar | baz |::\n\n]",
        "[end-para:::True]",
        "[block-quote(4,1)::> ]",
        "[para(4,3):]",
        "[text(4,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when tables are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_token_consistency(source_markdown, actual_tokens)


def test_tables_extension_202():
    """
    Test case 202:  (part 2) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
bar

bar"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):| abc | def |\n| --- | --- |\n| bar | baz |\nbar::\n\n\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[para(6,1):]",
        "[text(6,1):bar:]",
        "[end-para:::True]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when tables are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_token_consistency(source_markdown, actual_tokens)


def test_tables_extension_203():
    """
    Test case 203:  The header row must match the delimiter row in the number of cells. If not, a table will not be recognized:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """| abc | def |
| --- |
| bar |"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| abc | def |\n| --- |\n| bar |::\n\n]",
        "[end-para:::True]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when tables are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_token_consistency(source_markdown, actual_tokens)


def test_tables_extension_204():
    """
    Test case 204:  The remainder of the table’s rows may vary in the number of cells. If there are a number of cells fewer than the number of cells in the header row, empty cells are inserted. If there are greater, the excess is ignored:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """| abc | def |
| --- | --- |
| bar |
| bar | baz | boo |"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):| abc | def |\n| --- | --- |\n| bar |\n| bar | baz | boo |::\n\n\n]",
        "[end-para:::True]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when tables are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_token_consistency(source_markdown, actual_tokens)


def test_tables_extension_205():
    """
    Test case 205:  If there are no rows in the body, no <tbody> is generated in HTML output:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """| abc | def |
| --- | --- |"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):| abc | def |\n| --- | --- |::\n]",
        "[end-para:::True]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when tables are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_token_consistency(source_markdown, actual_tokens)
