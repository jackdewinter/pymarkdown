"""
https://github.github.com/gfm/#task-list-items-extension-
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_task_list_items_279():
    """
    Test case 279:  If the character between the brackets is a whitespace character, the checkbox is unchecked. Otherwise, the checkbox is checked.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- [ ] foo
- [x] bar"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_task_list_items_280():
    """
    Test case 280:  Task lists can be arbitrarily nested:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- [x] foo
  - [ ] bar
  - [x] baz
- [ ] bim"""
    expected_tokens = [
        "[block-quote:]",
        "[atx:1:Foo:: ::]",
        "[para:]",
        "[text:bar:]",
        "[text:baz:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
