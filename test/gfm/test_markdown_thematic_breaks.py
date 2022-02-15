"""
https://github.github.com/gfm/#thematic-breaks
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_thematic_breaks_013():
    """
    Test case 013:  A line consisting of 0-3 spaces of indentation, followed by a sequence of three or more matching -, _, or * characters, each followed optionally by any number of spaces or tabs, forms a thematic break.
    """

    # Arrange
    source_markdown = """***
---
___"""
    expected_tokens = [
        "[tbreak(1,1):*::***]",
        "[tbreak(2,1):-::---]",
        "[tbreak(3,1):_::___]",
    ]
    expected_gfm = """<hr />
<hr />
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_014():
    """
    Test case 014:  (part a) Wrong characters:
    """

    # Arrange
    source_markdown = """+++"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):+++:]", "[end-para:::True]"]
    expected_gfm = """<p>+++</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_015():
    """
    Test case 015:  (part b) Wrong characters:
    """

    # Arrange
    source_markdown = """==="""
    expected_tokens = ["[para(1,1):]", "[text(1,1):===:]", "[end-para:::True]"]
    expected_gfm = """<p>===</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_016():
    """
    Test case 016:  Not enough characters:
    """

    # Arrange
    source_markdown = """--
**
__"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):--\n::\n]",
        "[text(2,1):**:]",
        "[text(2,3):\n::\n]",
        "[text(3,1):__:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>--
**
__</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_017():
    """
    Test case 017:  One to three spaces indent are allowed:
    """

    # Arrange
    source_markdown = """ ***
  ***
   ***"""
    expected_tokens = [
        "[tbreak(1,2):*: :***]",
        "[tbreak(2,3):*:  :***]",
        "[tbreak(3,4):*:   :***]",
    ]
    expected_gfm = """<hr />
<hr />
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_018():
    """
    Test case 018:  (part a) Four spaces is too many:
    """

    # Arrange
    source_markdown = """    ***"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):***:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>***
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_019():
    """
    Test case 019:  (part b) Four spaces is too many:
    """

    # Arrange
    source_markdown = """Foo
    ***"""
    expected_tokens = [
        "[para(1,1):\n    ]",
        "[text(1,1):Foo\n::\n]",
        "[text(2,5):***:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo
***</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_020():
    """
    Test case 020:  More than three characters may be used:
    """

    # Arrange
    source_markdown = """_____________________________________"""
    expected_tokens = ["[tbreak(1,1):_::_____________________________________]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_021():
    """
    Test case 021:  (part a) Spaces are allowed between the characters:
    """

    # Arrange
    source_markdown = """ - - -"""
    expected_tokens = ["[tbreak(1,2):-: :- - -]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_022():
    """
    Test case 022:  (part b) Spaces are allowed between the characters:
    """

    # Arrange
    source_markdown = """ **  * ** * ** * **"""
    expected_tokens = ["[tbreak(1,2):*: :**  * ** * ** * **]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_023():
    """
    Test case 023:  (part c) Spaces are allowed between the characters:
    """

    # Arrange
    source_markdown = """-     -      -      -"""
    expected_tokens = ["[tbreak(1,1):-::-     -      -      -]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_024():
    """
    Test case 024:  Spaces are allowed at the end:
    """

    # Arrange
    source_markdown = """- - - -    """
    expected_tokens = ["[tbreak(1,1):-::- - - -    ]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_025():
    """
    Test case 025:  However, no other characters may occur in the line:
    """

    # Arrange
    source_markdown = """_ _ _ _ a

a------

---a---"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):_:]",
        "[text(1,2): :]",
        "[text(1,3):_:]",
        "[text(1,4): :]",
        "[text(1,5):_:]",
        "[text(1,6): :]",
        "[text(1,7):_:]",
        "[text(1,8): a:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):a------:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):---a---:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>_ _ _ _ a</p>
<p>a------</p>
<p>---a---</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_026():
    """
    Test case 026:  It is required that all of the non-whitespace characters be the same. So, this is not a thematic break:
    """

    # Arrange
    source_markdown = """ *-*"""
    expected_tokens = [
        "[para(1,2): ]",
        "[emphasis(1,2):1:*]",
        "[text(1,3):-:]",
        "[end-emphasis(1,4)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><em>-</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_027():
    """
    Test case 027:  Thematic breaks do not need blank lines before or after:
    """

    # Arrange
    source_markdown = """- foo
***
- bar"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(2,1):*::***]",
        "[ulist(3,1):-::2:]",
        "[para(3,3):]",
        "[text(3,3):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>foo</li>
</ul>
<hr />
<ul>
<li>bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_028():
    """
    Test case 028:  Thematic breaks can interrupt a paragraph:
    """

    # Arrange
    source_markdown = """Foo
***
bar"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):Foo:]",
        "[end-para:::False]",
        "[tbreak(2,1):*::***]",
        "[para(3,1):]",
        "[text(3,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo</p>
<hr />
<p>bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_029():
    """
    Test case 029:  If a line of dashes that meets the above conditions for being a thematic break could also be interpreted as the underline of a setext heading, the interpretation as a setext heading takes precedence. Thus, for example, this is a setext heading, not a paragraph followed by a thematic break:
    """

    # Arrange
    source_markdown = """Foo
---
bar"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):Foo:]",
        "[end-setext::]",
        "[para(3,1):]",
        "[text(3,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<h2>Foo</h2>
<p>bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_030():
    """
    Test case 030:  When both a thematic break and a list item are possible interpretations of a line, the thematic break takes precedence:
    """

    # Arrange
    source_markdown = """* Foo
* * *
* Bar"""
    expected_tokens = [
        "[ulist(1,1):*::2:]",
        "[para(1,3):]",
        "[text(1,3):Foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[tbreak(2,1):*::* * *]",
        "[ulist(3,1):*::2:]",
        "[para(3,3):]",
        "[text(3,3):Bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Foo</li>
</ul>
<hr />
<ul>
<li>Bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_031():
    """
    Test case 031:  If you want a thematic break in a list item, use a different bullet:
    """

    # Arrange
    source_markdown = """
- Foo
- * * *"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[ulist(2,1):-::2:]",
        "[para(2,3):]",
        "[text(2,3):Foo:]",
        "[end-para:::True]",
        "[li(3,1):2::]",
        "[tbreak(3,3):*::* * *]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>Foo</li>
<li>
<hr />
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_thematic_breaks_031o():
    """
    Test case 031o:  variation on 31 with ordered list
    """

    # Arrange
    source_markdown = """
1) Foo
1) * * *"""
    expected_tokens = [
        "[BLANK(1,1):]",
        "[olist(2,1):):1:3:]",
        "[para(2,4):]",
        "[text(2,4):Foo:]",
        "[end-para:::True]",
        "[li(3,1):3::1]",
        "[tbreak(3,4):*::* * *]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>Foo</li>
<li>
<hr />
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
