"""
https://github.github.com/gfm/#html-blocks
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different

# pylint: disable=too-many-lines


def test_html_blocks_118():
    """
    Test case 118:  (weird sample) <pre> within a HTML block started by <table> will not affect the parser state
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<table><tr><td>
<pre>
**Hello**,

_world_.
</pre>
</td></tr></table>"""
    expected_tokens = [
        "[para:]",
        "[text:<table><tr><td>:]",
        "[text:<pre>:]",
        "[text:**Hello**,:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:_world_.:]",
        "[text:</pre>:]",
        "[text:</td></tr></table>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_119():
    """
    Test case 119:  (part 1) Some simple examples follow. Here are some basic HTML blocks of type 6:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<table>
  <tr>
    <td>
           hi
    </td>
  </tr>
</table>

okay."""
    expected_tokens = [
        "[para:]",
        "[text:<table>:]",
        "[text:<tr>:  ]",
        "[text:<td>:    ]",
        "[text:hi:           ]",
        "[text:</td>:    ]",
        "[text:</tr>:  ]",
        "[text:</table>:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:okay.:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_120():
    """
    Test case 120:  (part 2) Some simple examples follow. Here are some basic HTML blocks of type 6:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<div>
  *hello*
         <foo><a>"""
    expected_tokens = [
        "[para:]",
        "[text:<div>:]",
        "[text:*hello*:  ]",
        "[text:<foo><a>:         ]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_121():
    """
    Test case 121:  A block can also start with a closing tag:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """</div>
*foo*"""
    expected_tokens = ["[para:]", "[text:</div>:]", "[text:*foo*:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_122():
    """
    Test case 122:  Here we have two HTML blocks with a Markdown paragraph between them:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<DIV CLASS="foo">

*Markdown*

</DIV>"""
    expected_tokens = [
        "[para:]",
        '[text:<DIV CLASS="foo">:]',
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:*Markdown*:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:</DIV>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_123():
    """
    Test case 123:  (part 1) The tag on the first line can be partial, as long as it is split where there would be whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<div id="foo"
  class="bar">
</div>"""
    expected_tokens = [
        "[para:]",
        '[text:<div id="foo":]',
        '[text:class="bar">:  ]',
        "[text:</div>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_124():
    """
    Test case 124:  (part 2) The tag on the first line can be partial, as long as it is split where there would be whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<div id="foo" class="bar
  baz">
</div>"""
    expected_tokens = [
        "[para:]",
        '[text:<div id="foo" class="bar:]',
        '[text:baz">:  ]',
        "[text:</div>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_125():
    """
    Test case 125:  An open tag need not be closed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<div>
*foo*

*bar*"""
    expected_tokens = [
        "[para:]",
        "[text:<div>:]",
        "[text:*foo*:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:*bar*:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_126():
    """
    Test case 126:  (part 1) A partial tag need not even be completed (garbage in, garbage out):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<div id="foo"
*hi*"""
    expected_tokens = ["[para:]", '[text:<div id="foo":]', "[text:*hi*:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_127():
    """
    Test case 127:  (part 2) A partial tag need not even be completed (garbage in, garbage out):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<div class
foo"""
    expected_tokens = ["[para:]", "[text:<div class:]", "[text:foo:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_128():
    """
    Test case 128:  The initial tag doesn’t even need to be a valid tag, as long as it starts like one:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<div *???-&&&-<---
*foo*"""
    expected_tokens = [
        "[para:]",
        "[text:<div *???-&&&-<---:]",
        "[text:*foo*:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_129():
    """
    Test case 129:  (part 1) In type 6 blocks, the initial tag need not be on a line by itself:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<div><a href="bar">*foo*</a></div>"""
    expected_tokens = [
        "[para:]",
        '[text:<div><a href="bar">*foo*</a></div>:]',
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_130():
    """
    Test case 130:  (part 2) In type 6 blocks, the initial tag need not be on a line by itself:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<table><tr><td>
foo
</td></tr></table>"""
    expected_tokens = [
        "[para:]",
        "[text:<table><tr><td>:]",
        "[text:foo:]",
        "[text:</td></tr></table>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_131():
    """
    Test case 131:  Everything until the next blank line or end of document gets included in the HTML block.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<div></div>
``` c
int x = 33;
```"""
    expected_tokens = [
        "[para:]",
        "[text:<div></div>:]",
        "[end-para]",
        "[fcode-block:`:3:c::: ]",
        "[text:int x = 33;:]",
        "[end-fcode-block:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_132():
    """
    Test case 132:  To start an HTML block with a tag that is not in the list of block-level tags in (6), you must put the tag by itself on the first line (and it must be complete):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<a href="foo">
*bar*
</a>"""
    expected_tokens = [
        "[para:]",
        '[text:<a href="foo">:]',
        "[text:*bar*:]",
        "[text:</a>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_133():
    """
    Test case 133:  (part 1) In type 7 blocks, the tag name can be anything:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<Warning>
*bar*
</Warning>"""
    expected_tokens = [
        "[para:]",
        "[text:<Warning>:]",
        "[text:*bar*:]",
        "[text:</Warning>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_134():
    """
    Test case 134:  (part 2) In type 7 blocks, the tag name can be anything:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<i class="foo">
*bar*
</i>"""
    expected_tokens = [
        "[para:]",
        '[text:<i class="foo">:]',
        "[text:*bar*:]",
        "[text:</i>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_135():
    """
    Test case 135:  (part 3) In type 7 blocks, the tag name can be anything:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """</ins>
*bar*"""
    expected_tokens = ["[para:]", "[text:</ins>:]", "[text:*bar*:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_136():
    """
    Test case 136:  These rules are designed to allow us to work with tags that can function as either block-level or inline-level tags. The <del> tag is a nice example. We can surround content with <del> tags in three different ways. In this case, we get a raw HTML block, because the <del> tag is on a line by itself:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<del>
*foo*
</del>"""
    expected_tokens = [
        "[para:]",
        "[text:<del>:]",
        "[text:*foo*:]",
        "[text:</del>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_137():
    """
    Test case 137:  In this case, we get a raw HTML block that just includes the <del> tag (because it ends with the following blank line). So the contents get interpreted as CommonMark:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<del>

*foo*

</del>"""
    expected_tokens = [
        "[para:]",
        "[text:<del>:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:*foo*:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:</del>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_138():
    """
    Test case 138:  Finally, in this case, the <del> tags are interpreted as raw HTML inside the CommonMark paragraph. (Because the tag is not on a line by itself, we get inline HTML rather than an HTML block.)
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<del>*foo*</del>"""
    expected_tokens = ["[para:]", "[text:<del>*foo*</del>:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_139():
    """
    Test case 139:  A pre tag (type 1):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<pre language="haskell"><code>
import Text.HTML.TagSoup

main :: IO ()
main = print $ parseTags tags
</code></pre>
okay"""
    expected_tokens = [
        "[para:]",
        '[text:<pre language="haskell"><code>:]',
        "[text:import Text.HTML.TagSoup:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:main :: IO ():]",
        "[text:main = print $ parseTags tags:]",
        "[text:</code></pre>:]",
        "[text:okay:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_140():
    """
    Test case 140:  A script tag (type 1):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<script type="text/javascript">
// JavaScript example

document.getElementById("demo").innerHTML = "Hello JavaScript!";
</script>
okay"""
    expected_tokens = [
        "[para:]",
        '[text:<script type="text/javascript">:]',
        "[text:// JavaScript example:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        '[text:document.getElementById("demo").innerHTML = "Hello JavaScript!";:]',
        "[text:</script>:]",
        "[text:okay:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_141():
    """
    Test case 141:  A style tag (type 1):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<style
  type="text/css">
h1 {color:red;}

p {color:blue;}
</style>
okay"""
    expected_tokens = [
        "[para:]",
        "[text:<style:]",
        '[text:type="text/css">:  ]',
        "[text:h1 {color:red;}:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:p {color:blue;}:]",
        "[text:</style>:]",
        "[text:okay:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_142():
    """
    Test case 142:  (part 1) If there is no matching end tag, the block will end at the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<style
  type="text/css">

foo"""
    expected_tokens = [
        "[para:]",
        "[text:<style:]",
        '[text:type="text/css">:  ]',
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:foo:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_143():
    """
    Test case 143:  (part 2) If there is no matching end tag, the block will end at the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """> <div>
> foo

bar"""
    expected_tokens = [
        "[para:]",
        "[text:> <div>:]",
        "[text:> foo:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:bar:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when block quotes are implemented
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_144():
    """
    Test case 144:  (part 3) If there is no matching end tag, the block will end at the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """- <div>
- foo"""
    expected_tokens = ["[para:]", "[text:- <div>:]", "[text:- foo:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when list blocks are implemented
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_145():
    """
    Test case 145:  (part 1) The end tag can occur on the same line as the start tag:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<style>p{color:red;}</style>
*foo*"""
    expected_tokens = [
        "[para:]",
        "[text:<style>p{color:red;}</style>:]",
        "[text:*foo*:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_146():
    """
    Test case 146:  (part 2) The end tag can occur on the same line as the start tag:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<!-- foo -->*bar*
*baz*"""
    expected_tokens = [
        "[para:]",
        "[text:<!-- foo -->*bar*:]",
        "[text:*baz*:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_147():
    """
    Test case 147:  Note that anything on the last line after the end tag will be included in the HTML block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<script>
foo
</script>1. *bar*"""
    expected_tokens = [
        "[para:]",
        "[text:<script>:]",
        "[text:foo:]",
        "[text:</script>1. *bar*:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_148():
    """
    Test case 148:  A comment (type 2):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<!-- Foo

bar
   baz -->
okay"""
    expected_tokens = [
        "[para:]",
        "[text:<!-- Foo:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:bar:]",
        "[text:baz -->:   ]",
        "[text:okay:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_149():
    """
    Test case 149:  A processing instruction (type 3):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<?php

  echo '>';

?>
okay"""
    expected_tokens = [
        "[para:]",
        "[text:<?php:]",
        "[end-para]",
        "[BLANK:]",
        "[para:  ]",
        "[text:echo '>';:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:?>:]",
        "[text:okay:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_150():
    """
    Test case 150:  A declaration (type 4):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<!DOCTYPE html>"""
    expected_tokens = ["[para:]", "[text:<!DOCTYPE html>:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_151():
    """
    Test case 151:  CDATA (type 5):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
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
        "[para:]",
        "[text:<![CDATA[:]",
        "[text:function matchwo(a,b):]",
        "[text:{:]",
        "[text:if (a < b && a < 0) then {:  ]",
        "[text:return 1;:    ]",
        "[end-para]",
        "[BLANK:]",
        "[para:  ]",
        "[text:} else {:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:return 0;:]",
        "[end-icode-block]",
        "[para:  ]",
        "[text:}:]",
        "[text:}:]",
        "[text:]]>:]",
        "[text:okay:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_152():
    """
    Test case 152:  (part 1) The opening tag can be indented 1-3 spaces, but not 4:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """  <!-- foo -->

    <!-- foo -->"""
    expected_tokens = [
        "[para:  ]",
        "[text:<!-- foo -->:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:<!-- foo -->:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_153():
    """
    Test case 153:  (part 2) The opening tag can be indented 1-3 spaces, but not 4:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """  <div>

    <div>"""
    expected_tokens = [
        "[para:  ]",
        "[text:<div>:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:<div>:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_154():
    """
    Test case 154:  An HTML block of types 1–6 can interrupt a paragraph, and need not be preceded by a blank line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo
<div>
bar
</div>"""
    expected_tokens = [
        "[para:]",
        "[text:Foo:]",
        "[text:<div>:]",
        "[text:bar:]",
        "[text:</div>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_155():
    """
    Test case 155:  However, a following blank line is needed, except at the end of a document, and except for blocks of types 1–5, above:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<div>
bar
</div>
*foo*"""
    expected_tokens = [
        "[para:]",
        "[text:<div>:]",
        "[text:bar:]",
        "[text:</div>:]",
        "[text:*foo*:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_156():
    """
    Test case 156:  HTML blocks of type 7 cannot interrupt a paragraph:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo
<a href="bar">
baz"""
    expected_tokens = [
        "[para:]",
        "[text:Foo:]",
        '[text:<a href="bar">:]',
        "[text:baz:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_157():
    """
    Test case 157:  (part 1) This rule differs from John Gruber’s original Markdown syntax specification
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<div>

*Emphasized* text.

</div>"""
    expected_tokens = [
        "[para:]",
        "[text:<div>:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:*Emphasized* text.:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:</div>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_158():
    """
    Test case 158:  (part 2) This rule differs from John Gruber’s original Markdown syntax specification
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<div>
*Emphasized* text.
</div>"""
    expected_tokens = [
        "[para:]",
        "[text:<div>:]",
        "[text:*Emphasized* text.:]",
        "[text:</div>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_159():
    """
    Test case 159:  The rule given above seems a simpler and more elegant way of achieving the same expressive power, which is also much simpler to parse.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<table>

<tr>

<td>
Hi
</td>

</tr>

</table>"""
    expected_tokens = [
        "[para:]",
        "[text:<table>:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:<tr>:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:<td>:]",
        "[text:Hi:]",
        "[text:</td>:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:</tr>:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:</table>:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_160():
    """
    Test case 160:  The rule given above seems a simpler and more elegant way of achieving the same expressive power, which is also much simpler to parse.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<table>

  <tr>

    <td>
      Hi
    </td>

  </tr>

</table>
"""
    expected_tokens = [
        "[para:]",
        "[text:<table>:]",
        "[end-para]",
        "[BLANK:]",
        "[para:  ]",
        "[text:<tr>:]",
        "[end-para]",
        "[BLANK:]",
        "[icode-block:    ]",
        "[text:<td>:]",
        "[text:Hi:      ]",
        "[text:</td>:    ]",
        "[end-icode-block]",
        "[BLANK:]",
        "[para:  ]",
        "[text:</tr>:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:</table>:]",
        "[end-para]",
        "[BLANK:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_html_blocks_160a():
    """
    Test case 160a:  Test case 160 with the blank lines removed
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<table>
  <tr>
    <td>
      Hi
    </td>
  </tr>
</table>
"""
    expected_tokens = [
        "[para:]",
        "[text:<table>:]",
        "[text:<tr>:  ]",
        "[text:<td>:    ]",
        "[text:Hi:      ]",
        "[text:</td>:    ]",
        "[text:</tr>:  ]",
        "[text:</table>:]",
        "[end-para]",
        "[BLANK:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when html blocks are implemented
    assert_if_lists_different(expected_tokens, actual_tokens)
