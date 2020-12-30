"""
https://github.github.com/gfm/#lists
"""
import pytest

from .utils import (
    act_and_assert,
)


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_list_items_281():
    """
    Test case 281:  (part 1) Changing the bullet or ordered list delimiter starts a new list:
    """

    # Arrange
    source_markdown = """- foo
- bar
+ baz"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[ulist(3,1):+::2:]",
        "[para(3,3):]",
        "[text(3,3):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
<li>bar</li>
</ul>
<ul>
<li>baz</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_281a():
    """
    Test case 281a:  variation on 281 with second item indented
    """

    # Arrange
    source_markdown = """* foo
  * bar
* baz"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text(2,5):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(3,1):2::]",
        "[para(3,3):]",
        "[text(3,3):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar</li>
</ul>
</li>
<li>baz</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_281b():
    """
    Test case 281b:  variation on 281 with second item indented and third with different list start
    """

    # Arrange
    source_markdown = """* foo
  * bar
+ baz"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text(2,5):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[ulist(3,1):+::2:]",
        "[para(3,3):]",
        "[text(3,3):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar</li>
</ul>
</li>
</ul>
<ul>
<li>baz</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_281c():
    """
    Test case 281c:  variation on 281b with third item indented, and a following list item for the parent
    """

    # Arrange
    source_markdown = """* foo
  * bar
  + baz
* boffo"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text(2,5):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[ulist(3,3):+::4:  ]",
        "[para(3,5):]",
        "[text(3,5):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):boffo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar</li>
</ul>
<ul>
<li>baz</li>
</ul>
</li>
<li>boffo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_281d():
    """
    Test case 281d:  variation on 281
    """

    # Arrange
    source_markdown = """* foo
  * bar
    * boffo
  + baz"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text(2,5):bar:]",
        "[end-para:::True]",
        "[ulist(3,5):*::6:    ]",
        "[para(3,7):]",
        "[text(3,7):boffo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[ulist(4,3):+::4:  ]",
        "[para(4,5):]",
        "[text(4,5):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar
<ul>
<li>boffo</li>
</ul>
</li>
</ul>
<ul>
<li>baz</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_281e():
    """
    Test case 281e:  variation on 281
    """

    # Arrange
    source_markdown = """* foo
  * bar
    * boffo
+ baz"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text(2,5):bar:]",
        "[end-para:::True]",
        "[ulist(3,5):*::6:    ]",
        "[para(3,7):]",
        "[text(3,7):boffo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[ulist(4,1):+::2:]",
        "[para(4,3):]",
        "[text(4,3):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo
<ul>
<li>bar
<ul>
<li>boffo</li>
</ul>
</li>
</ul>
</li>
</ul>
<ul>
<li>baz</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_282():
    """
    Test case 282:  (part 2) Changing the bullet or ordered list delimiter starts a new list:
    """

    # Arrange
    source_markdown = """1. foo
2. bar
3) baz"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):foo:]",
        "[end-para:::True]",
        "[li(2,1):3::2]",
        "[para(2,4):]",
        "[text(2,4):bar:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[olist(3,1):):3:3:]",
        "[para(3,4):]",
        "[text(3,4):baz:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
<li>bar</li>
</ol>
<ol start="3">
<li>baz</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_282a():
    """
    Test case 282a:  variation
    """

    # Arrange
    source_markdown = """1. foo
2. bar
 3) baz"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):foo:]",
        "[end-para:::True]",
        "[li(2,1):3::2]",
        "[para(2,4):]",
        "[text(2,4):bar:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[olist(3,2):):3:4: ]",
        "[para(3,5):]",
        "[text(3,5):baz:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
<li>bar</li>
</ol>
<ol start="3">
<li>baz</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_282b():
    """
    Test case 282b:  variation
    """

    # Arrange
    source_markdown = """1. foo
2. bar
  3) baz"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):foo:]",
        "[end-para:::True]",
        "[li(2,1):3::2]",
        "[para(2,4):]",
        "[text(2,4):bar:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[olist(3,3):):3:5:  ]",
        "[para(3,6):]",
        "[text(3,6):baz:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
<li>bar</li>
</ol>
<ol start="3">
<li>baz</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_282c():
    """
    Test case 282c:  variation
    """

    # Arrange
    source_markdown = """1. foo
2. bar
   3) baz"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):foo:]",
        "[end-para:::True]",
        "[li(2,1):3::2]",
        "[para(2,4):\n]",
        "[text(2,4):bar\n3) baz::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>foo</li>
<li>bar
3) baz</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_282d():
    """
    Test case 282d:  variation
    """

    # Arrange
    source_markdown = """1. foo
2. bar

   3) baz"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):foo:]",
        "[end-para:::True]",
        "[li(2,1):3::2]",
        "[para(2,4):]",
        "[text(2,4):bar:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[olist(4,4):):3:6:   ]",
        "[para(4,7):]",
        "[text(4,7):baz:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<p>foo</p>
</li>
<li>
<p>bar</p>
<ol start="3">
<li>baz</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_283():
    """
    Test case 283:  In CommonMark, a list can interrupt a paragraph. That is, no blank line is needed to separate a paragraph from a following list:
    """

    # Arrange
    source_markdown = """Foo
- bar
- baz"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):Foo:]",
        "[end-para:::True]",
        "[ulist(2,1):-::2:]",
        "[para(2,3):]",
        "[text(2,3):bar:]",
        "[end-para:::True]",
        "[li(3,1):2::]",
        "[para(3,3):]",
        "[text(3,3):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<p>Foo</p>
<ul>
<li>bar</li>
<li>baz</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_284():
    """
    Test case 284:  In order to solve of unwanted lists in paragraphs with hard-wrapped numerals, we allow only lists starting with 1 to interrupt paragraphs. Thus,
    """

    # Arrange
    source_markdown = """The number of windows in my house is
14.  The number of doors is 6."""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):The number of windows in my house is\n14.  The number of doors is 6.::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>The number of windows in my house is
14.  The number of doors is 6.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_285():
    """
    Test case 285:  We may still get an unintended result in cases like
    """

    # Arrange
    source_markdown = """The number of windows in my house is
1.  The number of doors is 6."""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):The number of windows in my house is:]",
        "[end-para:::True]",
        "[olist(2,1):.:1:4:]",
        "[para(2,5):]",
        "[text(2,5):The number of doors is 6.:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<p>The number of windows in my house is</p>
<ol>
<li>The number of doors is 6.</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_286():
    """
    Test case 286:  (part 1) There can be any number of blank lines between items:
    """

    # Arrange
    source_markdown = """- foo

- bar


- baz"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[li(3,1):2::]",
        "[para(3,3):]",
        "[text(3,3):bar:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[BLANK(5,1):]",
        "[li(6,1):2::]",
        "[para(6,3):]",
        "[text(6,3):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_287():
    """
    Test case 287:  (part 2) There can be any number of blank lines between items:
    """

    # Arrange
    source_markdown = """- foo
  - bar
    - baz


      bim"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):bar:]",
        "[end-para:::True]",
        "[ulist(3,5):-::6:    :      ]",
        "[para(3,7):]",
        "[text(3,7):baz:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[BLANK(5,1):]",
        "[para(6,7):]",
        "[text(6,7):bim:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_288():
    """
    Test case 288:  (part 1) To separate consecutive lists of the same type, or to separate a list from an indented code block that would otherwise be parsed as a subparagraph of the final list item, you can insert a blank HTML comment:
    """

    # Arrange
    source_markdown = """- foo
- bar

<!-- -->

- baz
- bim"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):bar:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
        "[html-block(4,1)]",
        "[text(4,1):<!-- -->:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
        "[ulist(6,1):-::2:]",
        "[para(6,3):]",
        "[text(6,3):baz:]",
        "[end-para:::True]",
        "[li(7,1):2::]",
        "[para(7,3):]",
        "[text(7,3):bim:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_289():
    """
    Test case 289:  (part 2) To separate consecutive lists of the same type, or to separate a list from an indented code block that would otherwise be parsed as a subparagraph of the final list item, you can insert a blank HTML comment:
    """

    # Arrange
    source_markdown = """-   foo

    notcode

-   foo

<!-- -->

    code"""
    expected_tokens = [
        "[ulist(1,1):-::4::    ]",
        "[para(1,5):]",
        "[text(1,5):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,5):]",
        "[text(3,5):notcode:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[li(5,1):4::]",
        "[para(5,5):]",
        "[text(5,5):foo:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[html-block(7,1)]",
        "[text(7,1):<!-- -->:]",
        "[end-html-block:::False]",
        "[BLANK(8,1):]",
        "[icode-block(9,5):    :]",
        "[text(9,5):code:]",
        "[end-icode-block:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_290():
    """
    Test case 290:  (part 1) List items need not be indented to the same level. The following list items will be treated as items at the same list level, since none is indented enough to belong to the previous list item:
    """

    # Arrange
    source_markdown = """- a
 - b
  - c
   - d
  - e
 - f
- g"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,2):3: :]",
        "[para(2,4):]",
        "[text(2,4):b:]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text(3,5):c:]",
        "[end-para:::True]",
        "[li(4,4):5:   :]",
        "[para(4,6):]",
        "[text(4,6):d:]",
        "[end-para:::True]",
        "[li(5,3):4:  :]",
        "[para(5,5):]",
        "[text(5,5):e:]",
        "[end-para:::True]",
        "[li(6,2):3: :]",
        "[para(6,4):]",
        "[text(6,4):f:]",
        "[end-para:::True]",
        "[li(7,1):2::]",
        "[para(7,3):]",
        "[text(7,3):g:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_291():
    """
    Test case 291:  (part 2) List items need not be indented to the same level. The following list items will be treated as items at the same list level, since none is indented enough to belong to the previous list item:
    """

    # Arrange
    source_markdown = """1. a

  2. b

   3. c"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[li(3,3):5:  :2]",
        "[para(3,6):]",
        "[text(3,6):b:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[li(5,4):6:   :3]",
        "[para(5,7):]",
        "[text(5,7):c:]",
        "[end-para:::True]",
        "[end-olist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_292x():
    """
    Test case 292x:  Note, however, that list items may not be indented more than three spaces. Here - e is treated as a paragraph continuation line, because it is indented more than three spaces:
    """

    # Arrange
    source_markdown = """- a
 - b
  - c
   - d
    - e"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,2):3: :]",
        "[para(2,4):]",
        "[text(2,4):b:]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text(3,5):c:]",
        "[end-para:::True]",
        "[li(4,4):5:   :]",
        "[para(4,6):\n\x04]",
        "[text(4,6):d\n- e::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a</li>
<li>b</li>
<li>c</li>
<li>d
- e</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_292xa():
    """
    Test case 292xa:  variation, indent by 2 instead of 1
    """

    # Arrange
    source_markdown = """- a
  - b
    - c
      - d
        - e"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):b:]",
        "[end-para:::True]",
        "[ulist(3,5):-::6:    ]",
        "[para(3,7):]",
        "[text(3,7):c:]",
        "[end-para:::True]",
        "[ulist(4,7):-::8:      ]",
        "[para(4,9):]",
        "[text(4,9):d:]",
        "[end-para:::True]",
        "[ulist(5,9):-::10:        ]",
        "[para(5,11):]",
        "[text(5,11):e:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<ul>
<li>b
<ul>
<li>c
<ul>
<li>d
<ul>
<li>e</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_292a():
    """
    Test case 292a:  Variation on 292
    """

    # Arrange
    source_markdown = """- a
 - b
  - c
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,2):3: :]",
        "[para(2,4):]",
        "[text(2,4):b:]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text(3,5):c:]",
        "[end-para:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a</li>
<li>b</li>
<li>c</li>
<li>d</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_292b():
    """
    Test case 292b:  Variation on 292
    """

    # Arrange
    source_markdown = """- a
 - b
  - c
   - d
- e"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,2):3: :]",
        "[para(2,4):]",
        "[text(2,4):b:]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text(3,5):c:]",
        "[end-para:::True]",
        "[li(4,4):5:   :]",
        "[para(4,6):]",
        "[text(4,6):d:]",
        "[end-para:::True]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):e:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a</li>
<li>b</li>
<li>c</li>
<li>d</li>
<li>e</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_292c():
    """
    Test case 292c:  variations
    """

    # Arrange
    source_markdown = """1. a
 1. b
  1. c
   1. d
    1. e"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):a:]",
        "[end-para:::True]",
        "[li(2,2):4: :1]",
        "[para(2,5):]",
        "[text(2,5):b:]",
        "[end-para:::True]",
        "[li(3,3):5:  :1]",
        "[para(3,6):]",
        "[text(3,6):c:]",
        "[end-para:::True]",
        "[li(4,4):6:   :1]",
        "[para(4,7):\n\x04\x04]",
        "[text(4,7):d\n1. e::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>a</li>
<li>b</li>
<li>c</li>
<li>d
1. e</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_292d():
    """
    Test case 292a:  Variation on 292
    """

    # Arrange
    source_markdown = """1. a
 1. b
  1. c
1. d"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):a:]",
        "[end-para:::True]",
        "[li(2,2):4: :1]",
        "[para(2,5):]",
        "[text(2,5):b:]",
        "[end-para:::True]",
        "[li(3,3):5:  :1]",
        "[para(3,6):]",
        "[text(3,6):c:]",
        "[end-para:::True]",
        "[li(4,1):3::1]",
        "[para(4,4):]",
        "[text(4,4):d:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>a</li>
<li>b</li>
<li>c</li>
<li>d</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_292e():
    """
    Test case 292b:  Variation on 292
    """

    # Arrange
    source_markdown = """1. a
 1. b
  1. c
   1. d
1. e"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):a:]",
        "[end-para:::True]",
        "[li(2,2):4: :1]",
        "[para(2,5):]",
        "[text(2,5):b:]",
        "[end-para:::True]",
        "[li(3,3):5:  :1]",
        "[para(3,6):]",
        "[text(3,6):c:]",
        "[end-para:::True]",
        "[li(4,4):6:   :1]",
        "[para(4,7):]",
        "[text(4,7):d:]",
        "[end-para:::True]",
        "[li(5,1):3::1]",
        "[para(5,4):]",
        "[text(5,4):e:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>a</li>
<li>b</li>
<li>c</li>
<li>d</li>
<li>e</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_293():
    """
    Test case 293:  And here, 3. c is treated as in indented code block, because it is indented four spaces and preceded by a blank line.
    """

    # Arrange
    source_markdown = """1. a

  2. b

    3. c"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[li(3,3):5:  :2]",
        "[para(3,6):]",
        "[text(3,6):b:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-olist:::True]",
        "[icode-block(5,5):    :]",
        "[text(5,5):3. c:]",
        "[end-icode-block:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_293a():
    """
    Test case 293a:  variation on 293
    """

    # Arrange
    source_markdown = """1. a
  1. b
    1. c"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):a:]",
        "[end-para:::True]",
        "[li(2,3):5:  :1]",
        "[para(2,6):\n\x04]",
        "[text(2,6):b\n1. c::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>a</li>
<li>b
1. c</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_293b():
    """
    Test case 293b:  variation on 293
    """

    # Arrange
    source_markdown = """1. a
   1. b
1. c"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):a:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):b:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(3,1):3::1]",
        "[para(3,4):]",
        "[text(3,4):c:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>a
<ol>
<li>b</li>
</ol>
</li>
<li>c</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_293c():
    """
    Test case 293c:  variation on 293
    """

    # Arrange
    source_markdown = """1. a
   1. b
1) c"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):a:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):b:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[olist(3,1):):1:3:]",
        "[para(3,4):]",
        "[text(3,4):c:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>a
<ol>
<li>b</li>
</ol>
</li>
</ol>
<ol>
<li>c</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_293d():
    """
    Test case 293d:  variation on 293
    """

    # Arrange
    source_markdown = """1. a
   1. b
   1) c
1. d"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):a:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):b:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[olist(3,4):):1:6:   ]",
        "[para(3,7):]",
        "[text(3,7):c:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[li(4,1):3::1]",
        "[para(4,4):]",
        "[text(4,4):d:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>a
<ol>
<li>b</li>
</ol>
<ol>
<li>c</li>
</ol>
</li>
<li>d</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_293e():
    """
    Test case 293e:  variation on 293
    """

    # Arrange
    source_markdown = """1. a
   1. b
      1. c
   1) d"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):a:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):b:]",
        "[end-para:::True]",
        "[olist(3,7):.:1:9:      ]",
        "[para(3,10):]",
        "[text(3,10):c:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[olist(4,4):):1:6:   ]",
        "[para(4,7):]",
        "[text(4,7):d:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>a
<ol>
<li>b
<ol>
<li>c</li>
</ol>
</li>
</ol>
<ol>
<li>d</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_293f():
    """
    Test case 293f:  variation on 293
    """

    # Arrange
    source_markdown = """1. a
   1. b
      1. c
1) d"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):a:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):b:]",
        "[end-para:::True]",
        "[olist(3,7):.:1:9:      ]",
        "[para(3,10):]",
        "[text(3,10):c:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[olist(4,1):):1:3:]",
        "[para(4,4):]",
        "[text(4,4):d:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>a
<ol>
<li>b
<ol>
<li>c</li>
</ol>
</li>
</ol>
</li>
</ol>
<ol>
<li>d</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_294():
    """
    Test case 294:  This is a loose list, because there is a blank line between two of the list items:
    """

    # Arrange
    source_markdown = """- a
- b

- c"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):b:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):c:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_295():
    """
    Test case 295:  So is this, with a empty second item:
    """

    # Arrange
    source_markdown = """* a
*

* c"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[BLANK(2,2):]",
        "[BLANK(3,1):]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):c:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_296():
    """
    Test case 296:  (part 1) These are loose lists, even though there is no space between the items, because one of the items directly contains two block-level elements with a blank line between them:
    """

    # Arrange
    source_markdown = """- a
- b

  c
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):b:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,3):]",
        "[text(4,3):c:]",
        "[end-para:::True]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_297():
    """
    Test case 297:  (part 2) These are loose lists, even though there is no space between the items, because one of the items directly contains two block-level elements with a blank line between them:
    """

    # Arrange
    source_markdown = """- a
- b

  [ref]: /url
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):b:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[link-ref-def(4,3):True::ref:: :/url:::::]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_297a():
    """
    Test case 297a:  variation
    """

    # Arrange
    source_markdown = """- a
- b

  # Heading
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):b:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[atx(4,3):1:0:]",
        "[text(4,5):Heading: ]",
        "[end-atx:::False]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
<h1>Heading</h1>
</li>
<li>
<p>d</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_297b():
    """
    Test case 297b:  variation
    """

    # Arrange
    source_markdown = """- a
- b

  Heading
  -------
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):b:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[setext(5,3):-:7::(4,3)]",
        "[text(4,3):Heading:]",
        "[end-setext:::False]",
        "[li(6,1):2::]",
        "[para(6,3):]",
        "[text(6,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
<h2>Heading</h2>
</li>
<li>
<p>d</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_297c():
    """
    Test case 297c:  variation
    """

    # Arrange
    source_markdown = """- a
- b

  <!-- script
  line
  -->
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):b:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[html-block(4,3)]",
        "[text(4,3):<!-- script\nline\n-->:]",
        "[end-html-block:::False]",
        "[li(7,1):2::]",
        "[para(7,3):]",
        "[text(7,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
<!-- script
line
-->
</li>
<li>
<p>d</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_297d():
    """
    Test case 297d:  variation
    """

    # Arrange
    source_markdown = """- a
- b

      script
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):b:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[icode-block(4,7):    :]",
        "[text(4,7):script:]",
        "[end-icode-block:::True]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
<pre><code>script
</code></pre>
</li>
<li>
<p>d</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_297e():
    """
    Test case 297e:  variation
    """

    # Arrange
    source_markdown = """- a
- b

   ```script
   my script
   ```
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):b:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[fcode-block(4,4):`:3:script:::: :]",
        "[text(5,3):my script:\a \a\x03\a]",
        "[end-fcode-block: :3:False]",
        "[li(7,1):2::]",
        "[para(7,3):]",
        "[text(7,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
<pre><code class="language-script">my script
</code></pre>
</li>
<li>
<p>d</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_297f():
    """
    Test case 297f:  variation
    """

    # Arrange
    source_markdown = """- a
- b

   ```script
   my script
   ```
  <!-- script
  line
  -->
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):b:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[fcode-block(4,4):`:3:script:::: :]",
        "[text(5,3):my script:\a \a\x03\a]",
        "[end-fcode-block: :3:False]",
        "[html-block(7,3)]",
        "[text(7,3):<!-- script\nline\n-->:]",
        "[end-html-block:::False]",
        "[li(10,1):2::]",
        "[para(10,3):]",
        "[text(10,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>a</p>
</li>
<li>
<p>b</p>
<pre><code class="language-script">my script
</code></pre>
<!-- script
line
-->
</li>
<li>
<p>d</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_298():
    """
    Test case 298:  This is a tight list, because the blank lines are in a code block:
    """

    # Arrange
    source_markdown = """- a
- ```
  b


  ```
- c"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[fcode-block(2,3):`:3::::::]",
        "[text(3,3):b\n\x03\n\x03:]",
        "[end-fcode-block::3:False]",
        "[li(7,1):2::]",
        "[para(7,3):]",
        "[text(7,3):c:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a</li>
<li>
<pre><code>b


</code></pre>
</li>
<li>c</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_299():
    """
    Test case 299:  This is a tight list, because the blank line is between two paragraphs of a sublist. So the sublist is loose while the outer list is tight:
    """

    # Arrange
    source_markdown = """- a
  - b

    c
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :    ]",
        "[para(2,5):]",
        "[text(2,5):b:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,5):]",
        "[text(4,5):c:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_300():
    """
    Test case 300:  This is a tight list, because the blank line is inside the block quote:
    """

    # Arrange
    source_markdown = """* a
  > b
  >
* c"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  >]",
        "[para(2,5):]",
        "[text(2,5):b:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):c:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<blockquote>
<p>b</p>
</blockquote>
</li>
<li>c</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_300a():
    """
    Test case 300a:  variation
    """

    # Arrange
    source_markdown = """* a
  > b
  >
1) c"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  >]",
        "[para(2,5):]",
        "[text(2,5):b:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
        "[olist(4,1):):1:3:]",
        "[para(4,4):]",
        "[text(4,4):c:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<blockquote>
<p>b</p>
</blockquote>
</li>
</ul>
<ol>
<li>c</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_300b():
    """
    Test case 300b:  variation
    """

    # Arrange
    source_markdown = """* a
  > b
  >
  * c"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  >]",
        "[para(2,5):]",
        "[text(2,5):b:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[end-block-quote:::True]",
        "[ulist(4,3):*::4:  ]",
        "[para(4,5):]",
        "[text(4,5):c:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<blockquote>
<p>b</p>
</blockquote>
<ul>
<li>c</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_301():
    """
    Test case 301:  This list is tight, because the consecutive block elements are not separated by blank lines:
    """

    # Arrange
    source_markdown = """- a
  > b
  ```
  c
  ```
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):b:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,3):`:3::::::]",
        "[text(4,3):c:]",
        "[end-fcode-block::3:False]",
        "[li(6,1):2::]",
        "[para(6,3):]",
        "[text(6,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_301a():
    """
    Test case 301a:  variation
    """

    # Arrange
    source_markdown = """- a
  >> b
  ```
  c
  ```
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :]",
        "[block-quote(2,4):  :  >> ]",
        "[para(2,6):]",
        "[text(2,6):b:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,3):`:3::::::]",
        "[text(4,3):c:]",
        "[end-fcode-block::3:False]",
        "[li(6,1):2::]",
        "[para(6,3):]",
        "[text(6,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<blockquote>
<blockquote>
<p>b</p>
</blockquote>
</blockquote>
<pre><code>c
</code></pre>
</li>
<li>d</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_301b():
    """
    Test case 301b:  variation
    """

    # Arrange
    source_markdown = """- a
  > b
   ```
   c
   ```
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > ]",
        "[para(2,5):]",
        "[text(2,5):b:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,4):`:3::::: :]",
        "[text(4,3):c:\a \a\x03\a]",
        "[end-fcode-block: :3:False]",
        "[li(6,1):2::]",
        "[para(6,3):]",
        "[text(6,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_301cx():
    """
    Test case 301cx:  variation
    """

    # Arrange
    source_markdown = """- a
  > b
      c
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  ]",
        "[para(2,5):\n    ]",
        "[text(2,5):b\nc::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<blockquote>
<p>b
c</p>
</blockquote>
</li>
<li>d</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_301ca():
    """
    Test case 301ca:  variation
    """

    # Arrange
    source_markdown = """- a
  > b
  >    c
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  > ]",
        "[para(2,5):\n   ]",
        "[text(2,5):b\nc::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<blockquote>
<p>b
c</p>
</blockquote>
</li>
<li>d</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_301cb():
    """
    Test case 301cb:  variation
    """

    # Arrange
    source_markdown = """> b
    c
- d"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):\n    ]",
        "[text(1,3):b\nc::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[ulist(3,1):-::2:]",
        "[para(3,3):]",
        "[text(3,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<blockquote>
<p>b
c</p>
</blockquote>
<ul>
<li>d</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_301d():
    """
    Test case 301d:  variation
    """

    # Arrange
    source_markdown = """- a
  > b
  >
  >     c
- d"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[block-quote(2,3):  :  > \n  >\n  > ]",
        "[para(2,5):]",
        "[text(2,5):b:]",
        "[end-para:::True]",
        "[BLANK(3,4):]",
        "[icode-block(4,9):    :]",
        "[text(4,9):c:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):d:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<blockquote>
<p>b</p>
<pre><code>c
</code></pre>
</blockquote>
</li>
<li>d</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_302():
    """
    Test case 302:  (part 1) A single-paragraph list is tight:
    """

    # Arrange
    source_markdown = """- a"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_303():
    """
    Test case 303:  (part 2) A single-paragraph list is tight:
    """

    # Arrange
    source_markdown = """- a
  - b"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):b:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>a
<ul>
<li>b</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_304():
    """
    Test case 304:  This list is loose, because of the blank line between the two block elements in the list item:
    """

    # Arrange
    source_markdown = """1. ```
   foo
   ```

   bar"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   ]",
        "[fcode-block(1,4):`:3::::::]",
        "[text(2,4):foo:]",
        "[end-fcode-block::3:False]",
        "[BLANK(4,1):]",
        "[para(5,4):]",
        "[text(5,4):bar:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>foo
</code></pre>
<p>bar</p>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_305x():
    """
    Test case 305:  (part 1) Here the outer list is loose, the inner list tight:
    """

    # Arrange
    source_markdown = """* foo
  * bar

  baz"""
    expected_tokens = [
        "[ulist(1,1):*::2::  ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[ulist(2,3):*::4:  ]",
        "[para(2,5):]",
        "[text(2,5):bar:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
        "[para(4,3):]",
        "[text(4,3):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_305a():
    """
    Test case 305a:  variation on 305
    """

    # Arrange
    source_markdown = """* foo
* foogle    
  * bar

  baz"""
    expected_tokens = [
        "[ulist(1,1):*::2::  ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3)::    ]",
        "[text(2,3):foogle:]",
        "[end-para:::True]",
        "[ulist(3,3):*::4:  ]",
        "[para(3,5):]",
        "[text(3,5):bar:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[para(5,3):]",
        "[text(5,3):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>foo</p>
</li>
<li>
<p>foogle</p>
<ul>
<li>bar</li>
</ul>
<p>baz</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_305b():
    """
    Test case 305b:  variation on 305
    """

    # Arrange
    source_markdown = """* foo
 * foogle    
   * bar

   baz"""
    expected_tokens = [
        "[ulist(1,1):*::2::   ]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[li(2,2):3: :]",
        "[para(2,4)::    ]",
        "[text(2,4):foogle:]",
        "[end-para:::True]",
        "[ulist(3,4):*::5:   ]",
        "[para(3,6):]",
        "[text(3,6):bar:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[para(5,4):]",
        "[text(5,4):baz:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>foo</p>
</li>
<li>
<p>foogle</p>
<ul>
<li>bar</li>
</ul>
<p>baz</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_306():
    """
    Test case 306:  (part 2) Here the outer list is loose, the inner list tight:
    """

    # Arrange
    source_markdown = """- a
  - b
  - c

- d
  - e
  - f"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):a:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):b:]",
        "[end-para:::True]",
        "[li(3,3):4:  :]",
        "[para(3,5):]",
        "[text(3,5):c:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
        "[li(5,1):2::]",
        "[para(5,3):]",
        "[text(5,3):d:]",
        "[end-para:::True]",
        "[ulist(6,3):-::4:  ]",
        "[para(6,5):]",
        "[text(6,5):e:]",
        "[end-para:::True]",
        "[li(7,3):4:  :]",
        "[para(7,5):]",
        "[text(7,5):f:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_extra_01x():
    """
    Test case List01:  link definition within a list item
                       copy of test_link_reference_definitions_161 but within list item
    """

    # Arrange
    source_markdown = """- [foo]: /url "title"

  [foo]"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        '[link-ref-def(1,3):True::foo:: :/url:: :title:"title":]',
        "[BLANK(2,1):]",
        "[para(3,3):]",
        "[link(3,3):shortcut:/url:title::::foo:::::]",
        "[text(3,4):foo:]",
        "[end-link:::False]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><a href="/url" title="title">foo</a></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_extra_01a():
    """
    Test case Bq03a:  link definition within a list item
                      copy of test_link_reference_definitions_161 but within
                      two distinct list items
    """

    # Arrange
    source_markdown = """- [foo]: /url "title"
- [foo]"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        '[link-ref-def(1,3):True::foo:: :/url:: :title:"title":]',
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[link(2,3):shortcut:/url:title::::foo:::::]",
        "[text(2,4):foo:]",
        "[end-link:::False]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li></li>
<li><a href="/url" title="title">foo</a></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_list_items_extra_01b():
    """
    Test case Bq03a:  link definition within a list item
                      copy of test_link_reference_definitions_164 but within
                      a single list item
    """

    # Arrange
    source_markdown = """- [Foo bar]:
  <my url>
  'title'

  [Foo bar]"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[link-ref-def(1,3):True::foo bar:Foo bar:\n:my%20url:<my url>:\n:title:'title':]",
        "[BLANK(4,1):]",
        "[para(5,3):]",
        "[link(5,3):shortcut:my%20url:title::::Foo bar:::::]",
        "[text(5,4):Foo bar:]",
        "[end-link:::False]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><a href="my%20url" title="title">Foo bar</a></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
