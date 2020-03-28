"""
https://github.github.com/gfm/#lists
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_list_items_281():
    """
    Test case 281:  (part 1) Changing the bullet or ordered list delimiter starts a new list:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>foo</li>
<li>bar</li>
</ul>
<ul>
<li>baz</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_282():
    """
    Test case 282:  (part 2) Changing the bullet or ordered list delimiter starts a new list:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ol>
<li>foo</li>
<li>bar</li>
</ol>
<ol start="3">
<li>baz</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_283():
    """
    Test case 283:  In CommonMark, a list can interrupt a paragraph. That is, no blank line is needed to separate a paragraph from a following list:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<p>Foo</p>
<ul>
<li>bar</li>
<li>baz</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_284():
    """
    Test case 284:  In order to solve of unwanted lists in paragraphs with hard-wrapped numerals, we allow only lists starting with 1 to interrupt paragraphs. Thus,
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """The number of windows in my house is
14.  The number of doors is 6."""
    expected_tokens = [
        "[para:\n]",
        "[text:The number of windows in my house is\n14.  The number of doors is 6.::\n]",
        "[end-para]",
    ]
    expected_gfm = """<p>The number of windows in my house is
14.  The number of doors is 6.</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_285():
    """
    Test case 285:  We may still get an unintended result in cases like
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<p>The number of windows in my house is</p>
<ol>
<li>The number of doors is 6.</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_286():
    """
    Test case 286:  (part 1) There can be any number of blank lines between items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>
<p>foo</p>
</li>
<li>
<p>bar</p>
</li>
<li>
<p>baz</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_287():
    """
    Test case 287:  (part 2) There can be any number of blank lines between items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar
<ul>
<li>
<p>baz</p>
<p>bim</p>
</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_288():
    """
    Test case 288:  (part 1) To separate consecutive lists of the same type, or to separate a list from an indented code block that would otherwise be parsed as a subparagraph of the final list item, you can insert a blank HTML comment:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>foo</li>
<li>bar</li>
</ul>
<!-- -->
<ul>
<li>baz</li>
<li>bim</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_289():
    """
    Test case 289:  (part 2) To separate consecutive lists of the same type, or to separate a list from an indented code block that would otherwise be parsed as a subparagraph of the final list item, you can insert a blank HTML comment:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>
<p>foo</p>
<p>notcode</p>
</li>
<li>
<p>foo</p>
</li>
</ul>
<!-- -->
<pre><code>code
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_290():
    """
    Test case 290:  (part 1) List items need not be indented to the same level. The following list items will be treated as items at the same list level, since none is indented enough to belong to the previous list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>a</li>
<li>b</li>
<li>c</li>
<li>d</li>
<li>e</li>
<li>f</li>
<li>g</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_291():
    """
    Test case 291:  (part 2) List items need not be indented to the same level. The following list items will be treated as items at the same list level, since none is indented enough to belong to the previous list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ol>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
</li>
<li>
<p>c</p>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_292():
    """
    Test case 292:  Note, however, that list items may not be indented more than three spaces. Here - e is treated as a paragraph continuation line, because it is indented more than three spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
        "[para:\n  ]",
        "[text:d\n- e::\n]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>a</li>
<li>b</li>
<li>c</li>
<li>d
- e</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_293():
    """
    Test case 293:  And here, 3. c is treated as in indented code block, because it is indented four spaces and preceded by a blank line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ol>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
</li>
</ol>
<pre><code>3. c
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_294():
    """
    Test case 294:  This is a loose list, because there is a blank line between two of the list items:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
</li>
<li>
<p>c</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_295():
    """
    Test case 295:  So is this, with a empty second item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li></li>
<li>
<p>c</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_296():
    """
    Test case 296:  (part 1) These are loose lists, even though there is no space between the items, because one of the items directly contains two block-level elements with a blank line between them:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
<p>c</p>
</li>
<li>
<p>d</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_297():
    """
    Test case 297:  (part 2) These are loose lists, even though there is no space between the items, because one of the items directly contains two block-level elements with a blank line between them:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
        "[li:2]",
        "[para:]",
        "[text:d:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
</li>
<li>
<p>d</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_298():
    """
    Test case 298:  This is a tight list, because the blank lines are in a code block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
        "[text:b\n\n:]",
        "[end-fcode-block]",
        "[li:2]",
        "[para:]",
        "[text:c:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>a</li>
<li>
<pre><code>b


</code></pre>
</li>
<li>c</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_299():
    """
    Test case 299:  This is a tight list, because the blank line is between two paragraphs of a sublist. So the sublist is loose while the outer list is tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>a
<ul>
<li>
<p>b</p>
<p>c</p>
</li>
</ul>
</li>
<li>d</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_300():
    """
    Test case 300:  This is a tight list, because the blank line is inside the block quote:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>a
<blockquote>
<p>b</p>
</blockquote>
</li>
<li>c</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_301():
    """
    Test case 301:  This list is tight, because the consecutive block elements are not separated by blank lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>a
<blockquote>
<p>b</p>
</blockquote>
<pre><code>c
</code></pre>
</li>
<li>d</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_302():
    """
    Test case 302:  (part 1) A single-paragraph list is tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- a"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[para:]",
        "[text:a:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>a</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_303():
    """
    Test case 303:  (part 2) A single-paragraph list is tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>a
<ul>
<li>b</li>
</ul>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_304():
    """
    Test case 304:  This list is loose, because of the blank line between the two block elements in the list item:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ol>
<li>
<pre><code>foo
</code></pre>
<p>bar</p>
</li>
</ol>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_305():
    """
    Test case 305:  (part 1) Here the outer list is loose, the inner list tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>
<p>foo</p>
<ul>
<li>bar</li>
</ul>
<p>baz</p>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_list_items_306():
    """
    Test case 306:  (part 2) Here the outer list is loose, the inner list tight:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
    expected_gfm = """<ul>
<li>
<p>a</p>
<ul>
<li>b</li>
<li>c</li>
</ul>
</li>
<li>
<p>d</p>
<ul>
<li>e</li>
<li>f</li>
</ul>
</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


# TODO go through each use of extract_whitespace and validate whether it should
#    be e_space or e_whitespace
# TODO '* foo\n  * bar\n+ baz'
# TODO '- a\n - b\n  - c\n- d'
# TODO block quotes that start and stop i.e. > then >> then > then >>>, etc
# TODO 300 with different list following
# TODO 300 with extra indent on following item
# TODO 301, but with extra levels of block quotes
# TODO 301, with indented code blocks
# TODO 270 and check for indent levels after
# TODO 670 - hard/soft line break with code span
# TODO 620 - more bad cases, like <
# TODO 603 - href? doesn't look right

# TODO go through any case that uses lazy and do un-lazy example
# TODO Verify correct parsing
#       - 118 (html)
# TODO - foo \, what happens

# DONE?
# TODO - linking text blocks properly if not in paragraph block. DONE?
# TODO - [BLANK] and folding lines. DONE?

# TODO Expect this to fail when proper paragraph handling with breaks and trimming
# - 052
# - 059
# TODO "aaa" should not have 2 spaces in front of it
# - 098
# TODO removed spaces inconsistent
# - 101
# - 103
# TODO 144 as two separate and make sure still works
# TODO recheck after resetting tabs back
# - 006
# - 007
# TODO Is the example for this wrong?
# - 002
# TODO blank line ending a list is parsed wrong into tokens
# >>stack_count>>1>>#8:[BLANK:]
# >>stack_count>>0>>#9:[end-ulist]
# - should be end and then blank, as the blank is outside of the list
# TODO scan GFM and ensure Unicode whitespace uses actual unicode whitespace, not just whitespace
# TODO inline link ( without any extra info
# TODO why does GFM not specify that between [ and ] for a lrd, no blanks are allowed?
# -- maybe expound on 166 a bit?
# TODO what if bad link followed by good link?
# TODO collect_until_one_of_characters with backslashes?
# TODO what if bad link definition discovered multiple lines down, how to back track?
# TODO split up link definition within a block quote or list?
# TODO link ref def with empty link label, like 560?
# TODO full reference link with empty link label, like 560?
# TODO samples that end without a blank line, and add a blank line?
# TODO 553 with other inlines?

# TODO can we generate Markdown from tokens? do we have enough info?
# TODO token for LRDs, even though consumed?
# TODO specific types of links for the 3 types?
# TODO more testing to determine what inlines are stripped within image links i.e. code spans?
