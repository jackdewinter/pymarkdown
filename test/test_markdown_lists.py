"""
https://github.github.com/gfm/#lists
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_list_items_281():
    """
    Test case 281:  (part 1) Changing the bullet or ordered list delimiter starts a new list:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo
- bar
+ baz"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[li:2]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
        "[ulist:+::2:]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_282():
    """
    Test case 282:  (part 2) Changing the bullet or ordered list delimiter starts a new list:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1. foo
2. bar
3) baz"""
    expected_tokens = [
        "[olist:.:1:3:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[li:3]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-olist]",
        "[olist:):3:3:]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_283():
    """
    Test case 283:  In CommonMark, a list can interrupt a paragraph. That is, no blank line is needed to separate a paragraph from a following list:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo
- bar
- baz"""
    expected_tokens = [
        "[para:]",
        "[text:Foo:]",
        "[end-para]",
        "[ulist:-::2:]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[li:2]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_284():
    """
    Test case 284:  In order to solve of unwanted lists in paragraphs with hard-wrapped numerals, we allow only lists starting with 1 to interrupt paragraphs. Thus,
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """The number of windows in my house is
14.  The number of doors is 6."""
    expected_tokens = [
        "[para:]",
        "[text:The number of windows in my house is:]",
        "[text:14.  The number of doors is 6.:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_285():
    """
    Test case 285:  We may still get an unintended result in cases like
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """The number of windows in my house is
1.  The number of doors is 6."""
    expected_tokens = [
        "[para:]",
        "[text:The number of windows in my house is:]",
        "[end-para]",
        "[olist:.:1:4:]",
        "[para:]",
        "[text:The number of doors is 6.:]",
        "[end-para]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_286():
    """
    Test case 286:  (part 1) There can be any number of blank lines between items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo

- bar


- baz"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
        "[li:2]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[BLANK:]",
        "[BLANK:]",
        "[li:2]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_287():
    """
    Test case 287:  (part 2) There can be any number of blank lines between items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo
  - bar
    - baz


      bim"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[ulist:-::4:  ]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[ulist:-::6:    ]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
        "[BLANK:]",
        "[BLANK:]",
        "[para:]",
        "[text:bim:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_288():
    """
    Test case 288:  (part 1) To separate consecutive lists of the same type, or to separate a list from an indented code block that would otherwise be parsed as a subparagraph of the final list item, you can insert a blank HTML comment:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo
- bar

<!-- -->

- baz
- bim"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[li:2]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[BLANK:]",
        "[end-ulist]",
        "[html-block]",
        "[text:<!-- -->:]",
        "[end-html-block]",
        "[BLANK:]",
        "[ulist:-::2:]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
        "[li:2]",
        "[para:]",
        "[text:bim:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_289():
    """
    Test case 289:  (part 2) To separate consecutive lists of the same type, or to separate a list from an indented code block that would otherwise be parsed as a subparagraph of the final list item, you can insert a blank HTML comment:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """-   foo

    notcode

-   foo

<!-- -->

    code"""
    expected_tokens = [
        "[ulist:-::4:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:notcode:]",
        "[end-para]",
        "[BLANK:]",
        "[li:4]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
        "[end-ulist]",
        "[html-block]",
        "[text:<!-- -->:]",
        "[end-html-block]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:code:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_290():
    """
    Test case 290:  (part 1) List items need not be indented to the same level. The following list items will be treated as items at the same list level, since none is indented enough to belong to the previous list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
 - b
  - c
   - d
  - e
 - f
- g"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[li:3]",
        "[para:]",
        "[text:b:]",
        "[end-para]",
        "[li:4]",
        "[para:]",
        "[text:c:]",
        "[end-para]",
        "[li:5]",
        "[para:]",
        "[text:d:]",
        "[end-para]",
        "[li:4]",
        "[para:]",
        "[text:e:]",
        "[end-para]",
        "[li:3]",
        "[para:]",
        "[text:f:]",
        "[end-para]",
        "[li:2]",
        "[para:]",
        "[text:g:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_291():
    """
    Test case 291:  (part 2) List items need not be indented to the same level. The following list items will be treated as items at the same list level, since none is indented enough to belong to the previous list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1. a

  2. b

   3. c"""
    expected_tokens = [
        "[olist:.:1:3:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[BLANK:]",
        "[li:5]",
        "[para:]",
        "[text:b:]",
        "[end-para]",
        "[BLANK:]",
        "[li:6]",
        "[para:]",
        "[text:c:]",
        "[end-para]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_292():
    """
    Test case 292:  Note, however, that list items may not be indented more than three spaces. Here - e is treated as a paragraph continuation line, because it is indented more than three spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
 - b
  - c
   - d
    - e"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[li:3]",
        "[para:]",
        "[text:b:]",
        "[end-para]",
        "[li:4]",
        "[para:]",
        "[text:c:]",
        "[end-para]",
        "[li:5]",
        "[para:]",
        "[text:d:]",
        "[text:- e:  ]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_293():
    """
    Test case 293:  And here, 3. c is treated as in indented code block, because it is indented four spaces and preceded by a blank line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1. a

  2. b

    3. c"""
    expected_tokens = [
        "[olist:.:1:3:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[BLANK:]",
        "[li:5]",
        "[para:]",
        "[text:b:]",
        "[end-para]",
        "[BLANK:]",
        "[end-olist]",
        "[icode-block:    ]",
        "[text:3. c:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_294():
    """
    Test case 294:  This is a loose list, because there is a blank line between two of the list items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
- b

- c"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[li:2]",
        "[para:]",
        "[text:b:]",
        "[end-para]",
        "[BLANK:]",
        "[li:2]",
        "[para:]",
        "[text:c:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_295():
    """
    Test case 295:  So is this, with a empty second item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """* a
*

* c"""
    expected_tokens = [
        "[ulist:*::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[li:2]",
        "[BLANK:]",
        "[BLANK:]",
        "[li:2]",
        "[para:]",
        "[text:c:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_296():
    """
    Test case 296:  (part 1) These are loose lists, even though there is no space between the items, because one of the items directly contains two block-level elements with a blank line between them:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
- b

  c
- d"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[li:2]",
        "[para:]",
        "[text:b:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:c:]",
        "[end-para]",
        "[li:2]",
        "[para:]",
        "[text:d:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_297():
    """
    Test case 297:  (part 2) These are loose lists, even though there is no space between the items, because one of the items directly contains two block-level elements with a blank line between them:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
- b

  [ref]: /url
- d"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[li:2]",
        "[para:]",
        "[text:b:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:[ref]: /url:]",
        "[end-para]",
        "[li:2]",
        "[para:]",
        "[text:d:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_298():
    """
    Test case 298:  This is a tight list, because the blank lines are in a code block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
- ```
  b


  ```
- c"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[li:2]",
        "[fcode-block:`:3::::]",
        "[text:b:]",
        "[BLANK:]",
        "[BLANK:]",
        "[end-fcode-block]",
        "[li:2]",
        "[para:]",
        "[text:c:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_299():
    """
    Test case 299:  This is a tight list, because the blank line is between two paragraphs of a sublist. So the sublist is loose while the outer list is tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
  - b

    c
- d"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[ulist:-::4:  ]",
        "[para:]",
        "[text:b:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:c:]",
        "[end-para]",
        "[end-ulist]",
        "[li:2]",
        "[para:]",
        "[text:d:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_300():
    """
    Test case 300:  This is a tight list, because the blank line is inside the block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """* a
  > b
  >
* c"""
    expected_tokens = [
        "[ulist:*::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[block-quote:  ]",
        "[para:]",
        "[text:b:]",
        "[end-para]",
        "[BLANK:]",
        "[end-block-quote]",
        "[li:2]",
        "[para:]",
        "[text:c:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_301():
    """
    Test case 301:  This list is tight, because the consecutive block elements are not separated by blank lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
  > b
  ```
  c
  ```
- d"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[block-quote:  ]",
        "[para:]",
        "[text:b:]",
        "[end-para]",
        "[end-block-quote]",
        "[fcode-block:`:3::::]",
        "[text:c:]",
        "[end-fcode-block]",
        "[li:2]",
        "[para:]",
        "[text:d:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_302():
    """
    Test case 302:  (part 1) A single-paragraph list is tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_303():
    """
    Test case 303:  (part 2) A single-paragraph list is tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
  - b"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[ulist:-::4:  ]",
        "[para:]",
        "[text:b:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_304():
    """
    Test case 304:  This list is loose, because of the blank line between the two block elements in the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1. ```
   foo
   ```

   bar"""
    expected_tokens = [
        "[olist:.:1:3:]",
        "[fcode-block:`:3::::]",
        "[text:foo:]",
        "[end-fcode-block]",
        "[BLANK:]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_305():
    """
    Test case 305:  (part 1) Here the outer list is loose, the inner list tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """* foo
  * bar

  baz"""
    expected_tokens = [
        "[ulist:*::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[ulist:*::4:  ]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[BLANK:]",
        "[end-ulist]",
        "[para:  ]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_items_306():
    """
    Test case 306:  (part 2) Here the outer list is loose, the inner list tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- a
  - b
  - c

- d
  - e
  - f"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[ulist:-::4:  ]",
        "[para:]",
        "[text:b:]",
        "[end-para]",
        "[li:4]",
        "[para:]",
        "[text:c:]",
        "[end-para]",
        "[BLANK:]",
        "[end-ulist]",
        "[li:2]",
        "[para:]",
        "[text:d:]",
        "[end-para]",
        "[ulist:-::4:  ]",
        "[para:]",
        "[text:e:]",
        "[end-para]",
        "[li:4]",
        "[para:]",
        "[text:f:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


# TODO '* foo\n  * bar\n+ baz'
# TODO '- a\n - b\n  - c\n- d'
# TODO block quotes that start and stop i.e. > then >> then > then >>>, etc
# TODO 300 with different list following
# TODO 300 with extra indent on following item
# TODO 301, but with extra levels of block quotes
# TODO 301, with indented code blocks
# TODO 270 and check for indent levels after
