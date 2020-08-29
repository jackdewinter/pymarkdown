"""
https://github.github.com/gfm/#task-list-items-extension-
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different, assert_token_consistency


def test_task_list_items_279():
    """
    Test case 279:  If the character between the brackets is a whitespace character, the checkbox is unchecked. Otherwise, the checkbox is checked.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- [ ] foo
- [x] bar"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):[:]",
        "[text(1,4): :]",
        "[text(1,5):]:]",
        "[text(1,6): foo:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):[:]",
        "[text(2,4):x:]",
        "[text(2,5):]:]",
        "[text(2,6): bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO revisit at end, not in back CommonMark spec
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_token_consistency(source_markdown, actual_tokens)


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
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):[:]",
        "[text(1,4):x:]",
        "[text(1,5):]:]",
        "[text(1,6): foo:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):[:]",
        "[text(2,6): :]",
        "[text(2,7):]:]",
        "[text(2,8): bar:]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text(3,5):[:]",
        "[text(3,6):x:]",
        "[text(3,7):]:]",
        "[text(3,8): baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):[:]",
        "[text(4,4): :]",
        "[text(4,5):]:]",
        "[text(4,6): bim:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO revisit at end, not in back CommonMark spec
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_token_consistency(source_markdown, actual_tokens)
