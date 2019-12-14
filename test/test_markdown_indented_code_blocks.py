"""
https://github.github.com/gfm/#indented-code-blocks
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_indented_code_blocks_077():
    """
    Test case 077:  Simple examples:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    a simple
      indented code block"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:a simple:]",
        "[text:indented code block:      ]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_indented_code_blocks_078():
    """
    Test case 078:  (part a) If there is any ambiguity between an interpretation of indentation as a code block and as indicating that material belongs to a list item, the list item interpretation takes precedence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """  - foo

    bar"""
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


def test_indented_code_blocks_079():
    """
    Test case 079:  (part b) If there is any ambiguity between an interpretation of indentation as a code block and as indicating that material belongs to a list item, the list item interpretation takes precedence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1.  foo

    - bar"""
    expected_tokens = [
        "[para:]",
        "[text:1.  foo:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:- bar:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when list blocks implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_indented_code_blocks_080():
    """
    Test case 080:  The contents of a code block are literal text, and do not get parsed as Markdown:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    <a/>
    *hi*

    - one"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:<a/>:]",
        "[text:*hi*:    ]",
        "[BLANK:]",
        "[text:- one:    ]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_indented_code_blocks_081():
    """
    Test case 081:  Here we have three chunks separated by blank lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    chunk1

    chunk2
  
 
 
    chunk3"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:chunk1:]",
        "[BLANK:]",
        "[text:chunk2:    ]",
        "[BLANK:  ]",
        "[BLANK: ]",
        "[BLANK: ]",
        "[text:chunk3:    ]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_indented_code_blocks_082():
    """
    Test case 082:  Any initial spaces beyond four will be included in the content, even in interior blank lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    chunk1
      
      chunk2"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:chunk1:]",
        "[BLANK:      ]",
        "[text:chunk2:      ]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_indented_code_blocks_083():
    """
    Test case 083:  An indented code block cannot interrupt a paragraph. (This allows hanging indents and the like.)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo
    bar"""
    expected_tokens = ["[para:]", "[text:Foo:]", "[text:bar:    ]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_indented_code_blocks_084():
    """
    Test case 084:  However, any non-blank line with fewer than four leading spaces ends the code block immediately. So a paragraph may occur immediately after indented code:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    foo
bar"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_indented_code_blocks_085():
    """
    Test case 085:  And indented code can occur immediately before and after other kinds of blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """# Heading
    foo
Heading
------
    foo
----"""
    expected_tokens = [
        "[atx:1:Heading:: ::]",
        "[icode-block:    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[setext:-:]",
        "[text:Heading:]",
        "[end-setext::]",
        "[icode-block:    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[tbreak:-::----]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_indented_code_blocks_086():
    """
    Test case 086:  The first line can be indented more than four spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """        foo
    bar"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:foo:    ]",
        "[text:bar:    ]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_indented_code_blocks_087():
    """
    Test case 087:  Blank lines preceding or following an indented code block are not included in it:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """
    
    foo
    """
    expected_tokens = [
        "[BLANK:]",
        "[BLANK:    ]",
        "[icode-block:    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[BLANK:    ]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_indented_code_blocks_087a():
    """
    ADDED:
    Test case 087a:  Copied from 84 with extra lines inserted to verify trailing blanks are not part of section.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    foo


bar"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:foo:]",
        "[end-icode-block]",
        "[BLANK:]",
        "[BLANK:]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_indented_code_blocks_088():
    """
    Test case 088:  Trailing spaces are included in the code block’s content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    foo  """
    expected_tokens = ["[icode-block:    ]", "[text:foo  :]", "[end-icode-block]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
