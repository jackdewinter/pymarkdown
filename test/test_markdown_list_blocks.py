# pylint: disable=too-many-lines
"""
https://github.github.com/gfm/#lists
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_list_blocks_231():
    """
    Test case 231:  If the list item is ordered, then it is also assigned a start number, based on the ordered list marker.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """A paragraph
with two lines.

    indented code

> A block quote."""
    expected_tokens = [
        "[para:\n]",
        "[text:A paragraph\nwith two lines.:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK:]",
        "[block-quote:]",
        "[para:]",
        "[text:A block quote.:]",
        "[end-para]",
        "[end-block-quote]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_232():
    """
    Test case 232:  And let M be the marker 1., and N = 2. Then rule #1 says that the following is an ordered list item with start number 1, and the same contents as Ls:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1.  A paragraph
    with two lines.

        indented code

    > A block quote."""
    expected_tokens = [
        "[olist:.:1:4:]",
        "[para:\n]",
        "[text:A paragraph\nwith two lines.:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK:]",
        "[block-quote:    ]",
        "[para:]",
        "[text:A block quote.:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_233():
    """
    Test case 233:  (part 1) Here are some examples showing how far content must be indented to be put under the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- one

 two"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:one:]",
        "[end-para]",
        "[BLANK:]",
        "[end-ulist]",
        "[para: ]",
        "[text:two:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_234():
    """
    Test case 234:  (part 2) Here are some examples showing how far content must be indented to be put under the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- one

  two"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:one:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:two:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_235():
    """
    Test case 235:  (part 3) Here are some examples showing how far content must be indented to be put under the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """ -    one

     two"""
    expected_tokens = [
        "[ulist:-::6: ]",
        "[para:]",
        "[text:one:]",
        "[end-para]",
        "[BLANK:]",
        "[end-ulist]",
        "[icode-block:     ]",
        "[text:two: ]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_236():
    """
    Test case 236:  (part 4) Here are some examples showing how far content must be indented to be put under the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """ -    one

      two"""
    expected_tokens = [
        "[ulist:-::6: ]",
        "[para:]",
        "[text:one:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:two:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_list_blocks_237():
    """
    Test case 237:  The spaces after the list marker determine how much relative indentation is needed. Which column this indentation reaches will depend on how the list item is embedded in other constructions, as shown by this example:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """   > > 1.  one
>>
>>     two"""
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


@pytest.mark.skip
def test_list_blocks_238():
    """
    Test case 238:  The converse is also possible. In the following example, the word two occurs far to the right of the initial text of the list item, one, but it is not considered part of the list item, because it is not indented far enough past the blockquote marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """>>- one
>>
  >  > two"""
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


def test_list_blocks_239():
    """
    Test case 239:  Note that at least one space is needed between the list marker and any following content, so these are not list items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """-one

2.two"""
    expected_tokens = [
        "[para:]",
        "[text:-one:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:2.two:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_240():
    """
    Test case 240:  A list item may contain blocks that are separated by more than one blank line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo


  bar"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
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


def test_list_blocks_241():
    """
    Test case 241:  A list item may contain any kind of block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1.  foo

    ```
    bar
    ```

    baz

    > bam"""
    expected_tokens = [
        "[olist:.:1:4:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
        "[fcode-block:`:3::::]",
        "[text:bar:]",
        "[end-fcode-block]",
        "[BLANK:]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
        "[BLANK:]",
        "[block-quote:    ]",
        "[para:]",
        "[text:bam:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_242():
    """
    Test case 242:  A list item that contains an indented code block will preserve empty lines within the code block verbatim.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- Foo

      bar


      baz"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:Foo:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:bar\n\n\nbaz:]",
        "[end-icode-block]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_243():
    """
    Test case 243:  (part 1) Note that ordered list start numbers must be nine digits or less:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """123456789. ok"""
    expected_tokens = [
        "[olist:.:123456789:11:]",
        "[para:]",
        "[text:ok:]",
        "[end-para]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_244():
    """
    Test case 244:  (part 2) Note that ordered list start numbers must be nine digits or less:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1234567890. not ok"""
    expected_tokens = ["[para:]", "[text:1234567890. not ok:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_245():
    """
    Test case 245:  (part 1) A start number may begin with 0s:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """0. ok"""
    expected_tokens = [
        "[olist:.:0:3:]",
        "[para:]",
        "[text:ok:]",
        "[end-para]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_246():
    """
    Test case 246:  (part 2) A start number may begin with 0s:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """003. ok"""
    expected_tokens = [
        "[olist:.:003:5:]",
        "[para:]",
        "[text:ok:]",
        "[end-para]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_247():
    """
    Test case 247:  A start number may not be negative:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """-1. not ok"""
    expected_tokens = ["[para:]", "[text:-1. not ok:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_248():
    """
    Test case 248:  An indented code block will have to be indented four spaces beyond the edge of the region where text will be included in the list item. In the following case that is 6 spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo

      bar"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:bar:]",
        "[end-icode-block]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_249():
    """
    Test case 249:  And in this case it is 11 spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """  10.  foo

           bar"""
    expected_tokens = [
        "[olist:.:10:7:  ]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:bar:]",
        "[end-icode-block]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_250():
    """
    Test case 250:  (part 1) If the first block in the list item is an indented code block, then by rule #2, the contents must be indented one space after the list marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    indented code

paragraph

    more code"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK:]",
        "[para:]",
        "[text:paragraph:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:more code:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_251():
    """
    Test case 251:  (part 2) If the first block in the list item is an indented code block, then by rule #2, the contents must be indented one space after the list marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1.     indented code

   paragraph

       more code"""
    expected_tokens = [
        "[olist:.:1:3:]",
        "[icode-block:    ]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK:]",
        "[para:]",
        "[text:paragraph:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:more code:]",
        "[end-icode-block]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_252():
    """
    Test case 252:  (part 2) If the first block in the list item is an indented code block, then by rule #2, the contents must be indented one space after the list marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1.      indented code

   paragraph

       more code"""
    expected_tokens = [
        "[olist:.:1:3:]",
        "[icode-block:     ]",
        "[text:indented code: ]",
        "[end-icode-block]",
        "[BLANK:]",
        "[para:]",
        "[text:paragraph:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:more code:]",
        "[end-icode-block]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_253():
    """
    Test case 253:  (part 1) Note that rules #1 and #2 only apply to two cases: (a) cases in which the lines to be included in a list item begin with a non-whitespace character, and (b) cases in which they begin with an indented code block. In a case like the following, where the first block begins with a three-space indent, the rules do not allow us to form a list item by indenting the whole thing and prepending a list marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """   foo

bar"""
    expected_tokens = [
        "[para:   ]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_254():
    """
    Test case 254:  (part 2) Note that rules #1 and #2 only apply to two cases: (a) cases in which the lines to be included in a list item begin with a non-whitespace character, and (b) cases in which they begin with an indented code block. In a case like the following, where the first block begins with a three-space indent, the rules do not allow us to form a list item by indenting the whole thing and prepending a list marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """-    foo

  bar"""
    expected_tokens = [
        "[ulist:-::5:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
        "[end-ulist]",
        "[para:  ]",
        "[text:bar:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_255():
    """
    Test case 255:  This is not a significant restriction, because when a block begins with 1-3 spaces indent, the indentation can always be removed without a change in interpretation, allowing rule #1 to be applied. So, in the above case:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """-  foo

   bar"""
    expected_tokens = [
        "[ulist:-::3:]",
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


def test_list_blocks_256():
    """
    Test case 256:  Here are some list items that start with a blank line but are not empty:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """-
  foo
-
  ```
  bar
  ```
-
      baz"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[BLANK:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[li:2]",
        "[BLANK:]",
        "[fcode-block:`:3::::]",
        "[text:bar:]",
        "[end-fcode-block]",
        "[li:2]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:baz:]",
        "[end-icode-block]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_257():
    """
    Test case 257:  When the list item starts with a blank line, the number of spaces following the list marker doesn’t change the required indentation:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """-\a\a\a
  foo""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[ulist:-::2:]",
        "[BLANK:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_258():
    """
    Test case 258:  A list item can begin with at most one blank line. In the following example, foo is not part of the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """-

  foo"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[BLANK:]",
        "[end-ulist]",
        "[BLANK:]",
        "[para:  ]",
        "[text:foo:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_259():
    """
    Test case 259:  Here is an empty bullet list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo
-
- bar"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[li:2]",
        "[BLANK:]",
        "[li:2]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_260():
    """
    Test case 260:  It does not matter whether there are spaces following the list marker:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo
-   
- bar"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[li:2]",
        "[BLANK:]",
        "[li:2]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_261():
    """
    Test case 261:  Here is an empty ordered list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1. foo
2.
3. bar"""
    expected_tokens = [
        "[olist:.:1:3:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[li:3]",
        "[BLANK:]",
        "[li:3]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_262():
    """
    Test case 262:  A list may start or end with an empty list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """*"""
    expected_tokens = ["[ulist:*::2:]", "[BLANK:]", "[end-ulist]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_263():
    """
    Test case 263:  However, an empty list item cannot interrupt a paragraph:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo
*

foo
1."""
    expected_tokens = [
        "[para:\n]",
        "[text:foo\n*:]",
        "[end-para]",
        "[BLANK:]",
        "[para:\n]",
        "[text:foo\n1.:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_264():
    """
    Test case 264:  Indented one space:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """ 1.  A paragraph
     with two lines.

         indented code

     > A block quote."""
    expected_tokens = [
        "[olist:.:1:5: ]",
        "[para:\n]",
        "[text:A paragraph\nwith two lines.:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK:]",
        "[block-quote:     ]",
        "[para:]",
        "[text:A block quote.:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_265():
    """
    Test case 265:  Indented two spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """  1.  A paragraph
      with two lines.

          indented code

      > A block quote."""
    expected_tokens = [
        "[olist:.:1:6:  ]",
        "[para:\n]",
        "[text:A paragraph\nwith two lines.:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK:]",
        "[block-quote:      ]",
        "[para:]",
        "[text:A block quote.:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_266():
    """
    Test case 266:  Indented three spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """   1.  A paragraph
       with two lines.

           indented code

       > A block quote."""
    expected_tokens = [
        "[olist:.:1:7:   ]",
        "[para:\n]",
        "[text:A paragraph\nwith two lines.:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK:]",
        "[block-quote:       ]",
        "[para:]",
        "[text:A block quote.:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_267():
    """
    Test case 267:  Four spaces indent gives a code block
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    1.  A paragraph
        with two lines.

            indented code

        > A block quote."""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:1.  A paragraph\n    with two lines.\n\n        indented code\n\n    &gt; A block quote.:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_268():
    """
    Test case 268:  Here is an example with lazy continuation lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """  1.  A paragraph
with two lines.

          indented code

      > A block quote."""
    expected_tokens = [
        "[olist:.:1:6:  ]",
        "[para:\n]",
        "[text:A paragraph\nwith two lines.:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:indented code:]",
        "[end-icode-block]",
        "[BLANK:]",
        "[block-quote:      ]",
        "[para:]",
        "[text:A block quote.:]",
        "[end-para]",
        "[end-block-quote]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_269():
    """
    Test case 269:  Indentation can be partially deleted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """  1.  A paragraph
    with two lines."""
    expected_tokens = [
        "[olist:.:1:6:  ]",
        "[para:\n]",
        "[text:A paragraph\nwith two lines.:]",
        "[end-para]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


@pytest.mark.skip
def test_list_blocks_270():
    """
    Test case 270:  (part 1) These examples show how laziness can work in nested structures:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> 1. > Blockquote
continued here."""
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


@pytest.mark.skip
def test_list_blocks_271():
    """
    Test case 271:  (part 2) These examples show how laziness can work in nested structures:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> 1. > Blockquote
> continued here."""
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


def test_list_blocks_272():
    """
    Test case 272:  So, in this case we need two spaces indent:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo
  - bar
    - baz
      - boo"""
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
        "[ulist:-::8:      ]",
        "[para:]",
        "[text:boo:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
        "[end-ulist]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_273():
    """
    Test case 273:  One is not enough:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- foo
 - bar
  - baz
   - boo"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[li:3]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[li:4]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
        "[li:5]",
        "[para:]",
        "[text:boo:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_274():
    """
    Test case 274:  Here we need four, because the list marker is wider:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """10) foo
    - bar"""
    expected_tokens = [
        "[olist:):10:4:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[ulist:-::6:    ]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_275():
    """
    Test case 275:  Three is not enough:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """10) foo
   - bar"""
    expected_tokens = [
        "[olist:):10:4:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[end-olist]",
        "[ulist:-::5:   ]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_276():
    """
    Test case 276:  (part 1) A list may be the first block in a list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- - foo"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[ulist:-::4:  ]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_277():
    """
    Test case 277:  (part 2) A list may be the first block in a list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """1. - 2. foo"""
    expected_tokens = [
        "[olist:.:1:3:]",
        "[ulist:-::5:   ]",
        "[olist:.:2:8:     ]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[end-olist]",
        "[end-ulist]",
        "[end-olist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_list_blocks_278():
    """
    Test case 278:  A list item can contain a heading:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- # Foo
- Bar
  ---
  baz"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[atx:1:0:]",
        "[text:Foo: ]",
        "[end-atx::]",
        "[li:2]",
        "[setext:-:]",
        "[text:Bar:]",
        "[end-setext::]",
        "[para:]",
        "[text:baz:]",
        "[end-para]",
        "[end-ulist]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
