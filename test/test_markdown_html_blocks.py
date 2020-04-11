"""
https://github.github.com/gfm/#html-blocks
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_html_blocks_118():
    """
    Test case 118:  (weird sample) <pre> within a HTML block started by <table> will not affect the parser state
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<table><tr><td>
<pre>
**Hello**,

_world_.
</pre>
</td></tr></table>"""
    expected_tokens = [
        "[html-block]",
        "[text:<table><tr><td>\n<pre>\n**Hello**,:]",
        "[end-html-block]",
        "[BLANK:]",
        "[para:\n]",
        "[emphasis:1]",
        "[text:world:]",
        "[end-emphasis::1]",
        "[text:.\n::\n]",
        "[raw-html:/pre]",
        "[end-para]",
        "[html-block]",
        "[text:</td></tr></table>:]",
        "[end-html-block]",
    ]
    expected_gfm = """<table><tr><td>
<pre>
**Hello**,
<p><em>world</em>.
</pre></p>
</td></tr></table>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_119():
    """
    Test case 119:  (part 1) Some simple examples follow. Here are some basic HTML blocks of type 6:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<table>
  <tr>
    <td>
           hi
    </td>
  </tr>
</table>

okay."""
    expected_tokens = [
        "[html-block]",
        "[text:<table>\n  <tr>\n    <td>\n           hi\n    </td>\n  </tr>\n</table>:]",
        "[end-html-block]",
        "[BLANK:]",
        "[para:]",
        "[text:okay.:]",
        "[end-para]",
    ]
    expected_gfm = """<table>
  <tr>
    <td>
           hi
    </td>
  </tr>
</table>
<p>okay.</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_120():
    """
    Test case 120:  (part 2) Some simple examples follow. Here are some basic HTML blocks of type 6:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ <div>
  *hello*
         <foo><a>"""
    expected_tokens = [
        "[html-block]",
        "[text:<div>\n  *hello*\n         <foo><a>: ]",
        "[end-html-block]",
    ]
    expected_gfm = """ <div>
  *hello*
         <foo><a>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_121():
    """
    Test case 121:  A block can also start with a closing tag:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """</div>
*foo*"""
    expected_tokens = [
        "[html-block]",
        "[text:</div>\n*foo*:]",
        "[end-html-block]",
    ]
    expected_gfm = """</div>
*foo*"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_122():
    """
    Test case 122:  Here we have two HTML blocks with a Markdown paragraph between them:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<DIV CLASS="foo">

*Markdown*

</DIV>"""
    expected_tokens = [
        "[html-block]",
        '[text:<DIV CLASS="foo">:]',
        "[end-html-block]",
        "[BLANK:]",
        "[para:]",
        "[emphasis:1]",
        "[text:Markdown:]",
        "[end-emphasis::1]",
        "[end-para]",
        "[BLANK:]",
        "[html-block]",
        "[text:</DIV>:]",
        "[end-html-block]",
    ]
    expected_gfm = """<DIV CLASS="foo">
<p><em>Markdown</em></p>
</DIV>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_123():
    """
    Test case 123:  (part 1) The tag on the first line can be partial, as long as it is split where there would be whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div id="foo"
  class="bar">
</div>"""
    expected_tokens = [
        "[html-block]",
        '[text:<div id="foo"\n  class="bar">\n</div>:]',
        "[end-html-block]",
    ]
    expected_gfm = """<div id="foo"
  class="bar">
</div>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_124():
    """
    Test case 124:  (part 2) The tag on the first line can be partial, as long as it is split where there would be whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div id="foo" class="bar
  baz">
</div>"""
    expected_tokens = [
        "[html-block]",
        '[text:<div id="foo" class="bar\n  baz">\n</div>:]',
        "[end-html-block]",
    ]
    expected_gfm = """<div id="foo" class="bar
  baz">
</div>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_125():
    """
    Test case 125:  An open tag need not be closed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div>
*foo*

*bar*"""
    expected_tokens = [
        "[html-block]",
        "[text:<div>\n*foo*:]",
        "[end-html-block]",
        "[BLANK:]",
        "[para:]",
        "[emphasis:1]",
        "[text:bar:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<div>
*foo*
<p><em>bar</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_126():
    """
    Test case 126:  (part 1) A partial tag need not even be completed (garbage in, garbage out):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div id="foo"
*hi*"""
    expected_tokens = [
        "[html-block]",
        '[text:<div id="foo"\n*hi*:]',
        "[end-html-block]",
    ]
    expected_gfm = """<div id="foo"
*hi*"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_127():
    """
    Test case 127:  (part 2) A partial tag need not even be completed (garbage in, garbage out):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div class
foo"""
    expected_tokens = [
        "[html-block]",
        "[text:<div class\nfoo:]",
        "[end-html-block]",
    ]
    expected_gfm = """<div class
foo"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_128():
    """
    Test case 128:  The initial tag doesn’t even need to be a valid tag, as long as it starts like one:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div *???-&&&-<---
*foo*"""
    expected_tokens = [
        "[html-block]",
        "[text:<div *???-&&&-<---\n*foo*:]",
        "[end-html-block]",
    ]
    expected_gfm = """<div *???-&&&-<---
*foo*"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_129():
    """
    Test case 129:  (part 1) In type 6 blocks, the initial tag need not be on a line by itself:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div><a href="bar">*foo*</a></div>"""
    expected_tokens = [
        "[html-block]",
        '[text:<div><a href="bar">*foo*</a></div>:]',
        "[end-html-block]",
    ]
    expected_gfm = """<div><a href="bar">*foo*</a></div>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_130():
    """
    Test case 130:  (part 2) In type 6 blocks, the initial tag need not be on a line by itself:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<table><tr><td>
foo
</td></tr></table>"""
    expected_tokens = [
        "[html-block]",
        "[text:<table><tr><td>\nfoo\n</td></tr></table>:]",
        "[end-html-block]",
    ]
    expected_gfm = """<table><tr><td>
foo
</td></tr></table>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_131():
    """
    Test case 131:  Everything until the next blank line or end of document gets included in the HTML block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div></div>
``` c
int x = 33;
```"""
    expected_tokens = [
        "[html-block]",
        "[text:<div></div>\n``` c\nint x = 33;\n```:]",
        "[end-html-block]",
    ]
    expected_gfm = """<div></div>
``` c
int x = 33;
```"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_132():
    """
    Test case 132:  To start an HTML block with a tag that is not in the list of block-level tags in (6), you must put the tag by itself on the first line (and it must be complete):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a href="foo">
*bar*
</a>"""
    expected_tokens = [
        "[html-block]",
        '[text:<a href="foo">\n*bar*\n</a>:]',
        "[end-html-block]",
    ]
    expected_gfm = """<a href="foo">
*bar*
</a>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_133():
    """
    Test case 133:  (part 1) In type 7 blocks, the tag name can be anything:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<Warning>
*bar*
</Warning>"""
    expected_tokens = [
        "[html-block]",
        "[text:<Warning>\n*bar*\n</Warning>:]",
        "[end-html-block]",
    ]
    expected_gfm = """<Warning>
*bar*
</Warning>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_134():
    """
    Test case 134:  (part 2) In type 7 blocks, the tag name can be anything:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<i class="foo">
*bar*
</i>"""
    expected_tokens = [
        "[html-block]",
        '[text:<i class="foo">\n*bar*\n</i>:]',
        "[end-html-block]",
    ]
    expected_gfm = """<i class="foo">
*bar*
</i>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_135():
    """
    Test case 135:  (part 3) In type 7 blocks, the tag name can be anything:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """</ins>
*bar*"""
    expected_tokens = [
        "[html-block]",
        "[text:</ins>\n*bar*:]",
        "[end-html-block]",
    ]
    expected_gfm = """</ins>
*bar*"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_136():
    """
    Test case 136:  These rules are designed to allow us to work with tags that can function as either block-level or inline-level tags. The <del> tag is a nice example. We can surround content with <del> tags in three different ways. In this case, we get a raw HTML block, because the <del> tag is on a line by itself:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<del>
*foo*
</del>"""
    expected_tokens = [
        "[html-block]",
        "[text:<del>\n*foo*\n</del>:]",
        "[end-html-block]",
    ]
    expected_gfm = """<del>
*foo*
</del>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_137():
    """
    Test case 137:  In this case, we get a raw HTML block that just includes the <del> tag (because it ends with the following blank line). So the contents get interpreted as CommonMark:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<del>

*foo*

</del>"""
    expected_tokens = [
        "[html-block]",
        "[text:<del>:]",
        "[end-html-block]",
        "[BLANK:]",
        "[para:]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[end-para]",
        "[BLANK:]",
        "[html-block]",
        "[text:</del>:]",
        "[end-html-block]",
    ]
    expected_gfm = """<del>
<p><em>foo</em></p>
</del>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_138():
    """
    Test case 138:  Finally, in this case, the <del> tags are interpreted as raw HTML inside the CommonMark paragraph. (Because the tag is not on a line by itself, we get inline HTML rather than an HTML block.)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<del>*foo*</del>"""
    expected_tokens = [
        "[para:]",
        "[raw-html:del]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[raw-html:/del]",
        "[end-para]",
    ]
    expected_gfm = """<p><del><em>foo</em></del></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_139():
    """
    Test case 139:  A pre tag (type 1):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<pre language="haskell"><code>
import Text.HTML.TagSoup

main :: IO ()
main = print $ parseTags tags
</code></pre>
okay"""
    expected_tokens = [
        "[html-block]",
        '[text:<pre language="haskell"><code>\nimport Text.HTML.TagSoup:]',
        "[BLANK:]",
        "[text:main :: IO ()\nmain = print $ parseTags tags\n</code></pre>:]",
        "[end-html-block]",
        "[para:]",
        "[text:okay:]",
        "[end-para]",
    ]
    expected_gfm = """<pre language="haskell"><code>
import Text.HTML.TagSoup

main :: IO ()
main = print $ parseTags tags
</code></pre>
<p>okay</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_140():
    """
    Test case 140:  A script tag (type 1):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<script type="text/javascript">
// JavaScript example

document.getElementById("demo").innerHTML = "Hello JavaScript!";
</script>
okay"""
    expected_tokens = [
        "[html-block]",
        '[text:<script type="text/javascript">\n// JavaScript example:]',
        "[BLANK:]",
        '[text:document.getElementById("demo").innerHTML = "Hello JavaScript!";\n</script>:]',
        "[end-html-block]",
        "[para:]",
        "[text:okay:]",
        "[end-para]",
    ]
    expected_gfm = """<script type="text/javascript">
// JavaScript example

document.getElementById("demo").innerHTML = "Hello JavaScript!";
</script>
<p>okay</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_141():
    """
    Test case 141:  A style tag (type 1):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<style
  type="text/css">
h1 {color:red;}

p {color:blue;}
</style>
okay"""
    expected_tokens = [
        "[html-block]",
        '[text:<style\n  type="text/css">\nh1 {color:red;}:]',
        "[BLANK:]",
        "[text:p {color:blue;}\n</style>:]",
        "[end-html-block]",
        "[para:]",
        "[text:okay:]",
        "[end-para]",
    ]
    expected_gfm = """<style
  type="text/css">
h1 {color:red;}

p {color:blue;}
</style>
<p>okay</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_142():
    """
    Test case 142:  (part 1) If there is no matching end tag, the block will end at the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<style
  type="text/css">

foo"""
    expected_tokens = [
        "[html-block]",
        '[text:<style\n  type="text/css">:]',
        "[BLANK:]",
        "[text:foo:]",
        "[end-html-block]",
    ]
    expected_gfm = """<style
  type="text/css">

foo"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_143():
    """
    Test case 143:  (part 2) If there is no matching end tag, the block will end at the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> <div>
> foo

bar"""
    expected_tokens = [
        "[block-quote:]",
        "[html-block]",
        "[text:<div>\nfoo:]",
        "[end-html-block]",
        "[BLANK:]",
        "[end-block-quote]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
    ]
    expected_gfm = """<blockquote>
<div>
foo
</blockquote>
<p>bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_144():
    """
    Test case 144:  (part 3) If there is no matching end tag, the block will end at the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- <div>
- foo"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[html-block]",
        "[text:<div>:]",
        "[end-html-block]",
        "[li:2]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<div>
</li>
<li>foo</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_144a():
    """
    Test case 144a:  Modification of 144 to add extra paragraph
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- <div>
- foo

foo"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[html-block]",
        "[text:<div>:]",
        "[end-html-block]",
        "[li:2]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[BLANK:]",
        "[end-ulist]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
    ]
    expected_gfm = """<ul>
<li>
<div>
</li>
<li>foo</li>
</ul>
<p>foo</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_144b():
    """
    Test case 144b:  Modification of 144 to add extra paragraph
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """- <div>
- foo"""
    expected_tokens = [
        "[ulist:-::2:]",
        "[html-block]",
        "[text:<div>:]",
        "[end-html-block]",
        "[li:2]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
        "[end-ulist]",
    ]
    expected_gfm = """<ul>
<li>
<div>
</li>
<li>foo</li>
</ul>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_145():
    """
    Test case 145:  (part 1) The end tag can occur on the same line as the start tag:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<style>p{color:red;}</style>
*foo*"""
    expected_tokens = [
        "[html-block]",
        "[text:<style>p{color:red;}</style>:]",
        "[end-html-block]",
        "[para:]",
        "[emphasis:1]",
        "[text:foo:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<style>p{color:red;}</style>
<p><em>foo</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_146():
    """
    Test case 146:  (part 2) The end tag can occur on the same line as the start tag:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<!-- foo -->*bar*
*baz*"""
    expected_tokens = [
        "[html-block]",
        "[text:<!-- foo -->*bar*:]",
        "[end-html-block]",
        "[para:]",
        "[emphasis:1]",
        "[text:baz:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<!-- foo -->*bar*
<p><em>baz</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_147():
    """
    Test case 147:  Note that anything on the last line after the end tag will be included in the HTML block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<script>
foo
</script>1. *bar*"""
    expected_tokens = [
        "[html-block]",
        "[text:<script>\nfoo\n</script>1. *bar*:]",
        "[end-html-block]",
    ]
    expected_gfm = """<script>
foo
</script>1. *bar*"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_148():
    """
    Test case 148:  A comment (type 2):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<!-- Foo

bar
   baz -->
okay"""
    expected_tokens = [
        "[html-block]",
        "[text:<!-- Foo:]",
        "[BLANK:]",
        "[text:bar\n   baz -->:]",
        "[end-html-block]",
        "[para:]",
        "[text:okay:]",
        "[end-para]",
    ]
    expected_gfm = """<!-- Foo

bar
   baz -->
<p>okay</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_149():
    """
    Test case 149:  A processing instruction (type 3):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<?php

  echo '>';

?>
okay"""
    expected_tokens = [
        "[html-block]",
        "[text:<?php:]",
        "[BLANK:]",
        "[text:echo '>';:  ]",
        "[BLANK:]",
        "[text:?>:]",
        "[end-html-block]",
        "[para:]",
        "[text:okay:]",
        "[end-para]",
    ]
    expected_gfm = """<?php

  echo '>';

?>
<p>okay</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_150():
    """
    Test case 150:  A declaration (type 4):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<!DOCTYPE html>"""
    expected_tokens = ["[html-block]", "[text:<!DOCTYPE html>:]", "[end-html-block]"]
    expected_gfm = """<!DOCTYPE html>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_151():
    """
    Test case 151:  CDATA (type 5):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<![CDATA[
function matchwo(a,b)
{
  if (a < b && a < 0) then {
    return 1;

  } else {

    return 0;
  }
}
]]>
okay"""
    expected_tokens = [
        "[html-block]",
        "[text:<![CDATA[\nfunction matchwo(a,b)\n{\n  if (a < b && a < 0) then {\n    return 1;:]",
        "[BLANK:]",
        "[text:} else {:  ]",
        "[BLANK:]",
        "[text:return 0;\n  }\n}\n]]>:    ]",
        "[end-html-block]",
        "[para:]",
        "[text:okay:]",
        "[end-para]",
    ]
    expected_gfm = """<![CDATA[
function matchwo(a,b)
{
  if (a < b && a < 0) then {
    return 1;

  } else {

    return 0;
  }
}
]]>
<p>okay</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_152():
    """
    Test case 152:  (part 1) The opening tag can be indented 1-3 spaces, but not 4:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  <!-- foo -->

    <!-- foo -->"""
    expected_tokens = [
        "[html-block]",
        "[text:<!-- foo -->:  ]",
        "[end-html-block]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:&lt;!-- foo --&gt;:]",
        "[end-icode-block]",
    ]
    expected_gfm = """  <!-- foo -->
<pre><code>&lt;!-- foo --&gt;
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_153():
    """
    Test case 153:  (part 2) The opening tag can be indented 1-3 spaces, but not 4:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  <div>

    <div>"""
    expected_tokens = [
        "[html-block]",
        "[text:<div>:  ]",
        "[end-html-block]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:&lt;div&gt;:]",
        "[end-icode-block]",
    ]
    expected_gfm = """  <div>
<pre><code>&lt;div&gt;
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_154():
    """
    Test case 154:  An HTML block of types 1–6 can interrupt a paragraph, and need not be preceded by a blank line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
<div>
bar
</div>"""
    expected_tokens = [
        "[para:]",
        "[text:Foo:]",
        "[end-para]",
        "[html-block]",
        "[text:<div>\nbar\n</div>:]",
        "[end-html-block]",
    ]
    expected_gfm = """<p>Foo</p>
<div>
bar
</div>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_155():
    """
    Test case 155:  However, a following blank line is needed, except at the end of a document, and except for blocks of types 1–5, above:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div>
bar
</div>
*foo*"""
    expected_tokens = [
        "[html-block]",
        "[text:<div>\nbar\n</div>\n*foo*:]",
        "[end-html-block]",
    ]
    expected_gfm = """<div>
bar
</div>
*foo*"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_156():
    """
    Test case 156:  HTML blocks of type 7 cannot interrupt a paragraph:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
<a href="bar">
baz"""
    expected_tokens = [
        "[para:\n\n]",
        "[text:Foo\n::\n]",
        '[raw-html:a href="bar"]',
        "[text:\nbaz::\n]",
        "[end-para]",
    ]
    expected_gfm = """<p>Foo
<a href="bar">
baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_157():
    """
    Test case 157:  (part 1) This rule differs from John Gruber’s original Markdown syntax specification
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div>

*Emphasized* text.

</div>"""
    expected_tokens = [
        "[html-block]",
        "[text:<div>:]",
        "[end-html-block]",
        "[BLANK:]",
        "[para:]",
        "[emphasis:1]",
        "[text:Emphasized:]",
        "[end-emphasis::1]",
        "[text: text.:]",
        "[end-para]",
        "[BLANK:]",
        "[html-block]",
        "[text:</div>:]",
        "[end-html-block]",
    ]
    expected_gfm = """<div>
<p><em>Emphasized</em> text.</p>
</div>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_158():
    """
    Test case 158:  (part 2) This rule differs from John Gruber’s original Markdown syntax specification
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<div>
*Emphasized* text.
</div>"""
    expected_tokens = [
        "[html-block]",
        "[text:<div>\n*Emphasized* text.\n</div>:]",
        "[end-html-block]",
    ]
    expected_gfm = """<div>
*Emphasized* text.
</div>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_159():
    """
    Test case 159:  The rule given above seems a simpler and more elegant way of achieving the same expressive power, which is also much simpler to parse.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<table>

<tr>

<td>
Hi
</td>

</tr>

</table>"""
    expected_tokens = [
        "[html-block]",
        "[text:<table>:]",
        "[end-html-block]",
        "[BLANK:]",
        "[html-block]",
        "[text:<tr>:]",
        "[end-html-block]",
        "[BLANK:]",
        "[html-block]",
        "[text:<td>\nHi\n</td>:]",
        "[end-html-block]",
        "[BLANK:]",
        "[html-block]",
        "[text:</tr>:]",
        "[end-html-block]",
        "[BLANK:]",
        "[html-block]",
        "[text:</table>:]",
        "[end-html-block]",
    ]
    expected_gfm = """<table>
<tr>
<td>
Hi
</td>
</tr>
</table>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_160():
    """
    Test case 160:  The rule given above seems a simpler and more elegant way of achieving the same expressive power, which is also much simpler to parse.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<table>

  <tr>

    <td>
      Hi
    </td>

  </tr>

</table>"""
    expected_tokens = [
        "[html-block]",
        "[text:<table>:]",
        "[end-html-block]",
        "[BLANK:]",
        "[html-block]",
        "[text:<tr>:  ]",
        "[end-html-block]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:&lt;td&gt;\n  Hi\n&lt;/td&gt;:]",
        "[end-icode-block]",
        "[BLANK:]",
        "[html-block]",
        "[text:</tr>:  ]",
        "[end-html-block]",
        "[BLANK:]",
        "[html-block]",
        "[text:</table>:]",
        "[end-html-block]",
    ]
    expected_gfm = """<table>
  <tr>
<pre><code>&lt;td&gt;
  Hi
&lt;/td&gt;
</code></pre>
  </tr>
</table>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_160a():
    """
    Test case 160a:  Test case 160 with the blank lines removed
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<table>
  <tr>
    <td>
      Hi
    </td>
  </tr>
</table>"""
    expected_tokens = [
        "[html-block]",
        "[text:<table>\n  <tr>\n    <td>\n      Hi\n    </td>\n  </tr>\n</table>:]",
        "[end-html-block]",
    ]
    expected_gfm = """<table>
  <tr>
    <td>
      Hi
    </td>
  </tr>
</table>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_cov1():
    """
    Test case cov1:  Based on coverage analysis.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<hr/>
</x-table>

</x-table>"""
    expected_tokens = [
        "[html-block]",
        "[text:<hr/>\n</x-table>:]",
        "[end-html-block]",
        "[BLANK:]",
        "[html-block]",
        "[text:</x-table>:]",
        "[end-html-block]",
    ]
    expected_gfm = """<hr/>
</x-table>
</x-table>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_cov2():
    """
    Test case cov2:  Based on coverage analysis.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """</hrx
>
</x-table>"""
    expected_tokens = [
        "[para:]",
        "[text:&lt;/hrx:]",
        "[end-para]",
        "[block-quote:]",
        "[BLANK:]",
        "[html-block]",
        "[text:</x-table>:]",
        "[end-html-block]",
        "[end-block-quote]",
    ]
    expected_gfm = """<p>&lt;/hrx</p>
<blockquote>
</x-table>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_cov3():
    """
    Test case cov3:  Based on coverage analysis.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<!bad>
</x-table>"""
    expected_tokens = [
        "[para:\n]",
        "[text:&lt;!bad&gt;\n::\n]",
        "[raw-html:/x-table]",
        "[end-para]",
    ]
    expected_gfm = """<p>&lt;!bad&gt;
</x-table></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_html_blocks_cov4():
    """
    Test case cov4:  Based on coverage analysis.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<
bad>
</x-table>"""
    expected_tokens = [
        "[para:\n\n]",
        "[text:&lt;\nbad&gt;\n::\n\n]",
        "[raw-html:/x-table]",
        "[end-para]",
    ]
    expected_gfm = """<p>&lt;
bad&gt;
</x-table></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
