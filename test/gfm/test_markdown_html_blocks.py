"""
https://github.github.com/gfm/#html-blocks
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_html_blocks_118():
    """
    Test case 118:  (weird sample) <pre> within a HTML block started by <table> will not affect the parser state
    """

    # Arrange
    source_markdown = """<table><tr><td>
<pre>
**Hello**,

_world_.
</pre>
</td></tr></table>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<table><tr><td>\n<pre>\n**Hello**,:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
        "[para(5,1):\n]",
        "[emphasis(5,1):1:_]",
        "[text(5,2):world:]",
        "[end-emphasis(5,7)::]",
        "[text(5,8):.\n::\n]",
        "[raw-html(6,1):/pre]",
        "[end-para:::False]",
        "[html-block(7,1)]",
        "[text(7,1):</td></tr></table>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<table><tr><td>
<pre>
**Hello**,
<p><em>world</em>.
</pre></p>
</td></tr></table>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_119():
    """
    Test case 119:  (part 1) Some simple examples follow. Here are some basic HTML blocks of type 6:
    """

    # Arrange
    source_markdown = """<table>
  <tr>
    <td>
           hi
    </td>
  </tr>
</table>

okay."""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<table>\n  <tr>\n    <td>\n           hi\n    </td>\n  </tr>\n</table>:]",
        "[end-html-block:::False]",
        "[BLANK(8,1):]",
        "[para(9,1):]",
        "[text(9,1):okay.:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<table>
  <tr>
    <td>
           hi
    </td>
  </tr>
</table>
<p>okay.</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_120():
    """
    Test case 120:  (part 2) Some simple examples follow. Here are some basic HTML blocks of type 6:
    """

    # Arrange
    source_markdown = """ <div>
  *hello*
         <foo><a>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,2):<div>\n  *hello*\n         <foo><a>: ]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """ <div>
  *hello*
         <foo><a>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_121():
    """
    Test case 121:  A block can also start with a closing tag:
    """

    # Arrange
    source_markdown = """</div>
*foo*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):</div>\n*foo*:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """</div>
*foo*"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_122():
    """
    Test case 122:  Here we have two HTML blocks with a Markdown paragraph between them:
    """

    # Arrange
    source_markdown = """<DIV CLASS="foo">

*Markdown*

</DIV>"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<DIV CLASS="foo">:]',
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[emphasis(3,1):1:*]",
        "[text(3,2):Markdown:]",
        "[end-emphasis(3,10)::]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[html-block(5,1)]",
        "[text(5,1):</DIV>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<DIV CLASS="foo">
<p><em>Markdown</em></p>
</DIV>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_123():
    """
    Test case 123:  (part 1) The tag on the first line can be partial, as long
                    as it is split where there would be whitespace:
    """

    # Arrange
    source_markdown = """<div id="foo"
  class="bar">
</div>"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<div id="foo"\n  class="bar">\n</div>:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div id="foo"
  class="bar">
</div>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_123a():
    """
    Test case 123a:  variation of 123 within a list
    """

    # Arrange
    source_markdown = """- <div id="foo"
class="bar">
</div>"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[html-block(1,3)]",
        '[text(1,3):<div id="foo":]',
        "[end-html-block:::True]",
        "[end-ulist:::True]",
        "[para(2,1):]",
        '[text(2,1):class=\a"\a&quot;\abar\a"\a&quot;\a\a>\a&gt;\a:]',
        "[end-para:::False]",
        "[html-block(3,1)]",
        "[text(3,1):</div>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<ul>
<li>
<div id="foo"
</li>
</ul>
<p>class=&quot;bar&quot;&gt;</p>
</div>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_123bx():
    """
    Test case 123b:  variation of 123 within a block quote
    """

    # Arrange
    source_markdown = """> <div id="foo"
class="bar">
</div>"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[html-block(1,3)]",
        '[text(1,3):<div id="foo":]',
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        '[text(2,1):class=\a"\a&quot;\abar\a"\a&quot;\a\a>\a&gt;\a:]',
        "[end-para:::False]",
        "[html-block(3,1)]",
        "[text(3,1):</div>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<blockquote>
<div id="foo"
</blockquote>
<p>class=&quot;bar&quot;&gt;</p>
</div>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_123ba():
    """
    Test case 123ba:  variation of 123b within a block quote with all
        lines starting with block quote
    """

    # Arrange
    source_markdown = """> <div id="foo"
> class="bar">
> </div>"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[html-block(1,3)]",
        '[text(1,3):<div id="foo"\nclass="bar">\n</div>:]',
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<div id="foo"
class="bar">
</div>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_123bb():
    """
    Test case 123bb:  variation of 123b within a block quote with all
        lines starting with block quote, and extra spaces
    """

    # Arrange
    source_markdown = """> <div id="foo"
>   class="bar">
> </div>"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[html-block(1,3)]",
        '[text(1,3):<div id="foo"\n  class="bar">\n</div>:]',
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<div id="foo"
  class="bar">
</div>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_123c():
    """
    Test case 123c:  variation of 123 within a SetExt Heading
    """

    # Arrange
    source_markdown = """<div id="foo"
class="bar">
---"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<div id="foo"\nclass="bar">\n---:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div id="foo"
class="bar">
---"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_123d():
    """
    Test case 123c:  variation of 123 within a Atx Heading
    """

    # Arrange
    source_markdown = """# <div id="foo"
class="bar">"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        '[text(1,3):\a<\a&lt;\adiv id=\a"\a&quot;\afoo\a"\a&quot;\a: ]',
        "[end-atx::]",
        "[para(2,1):]",
        '[text(2,1):class=\a"\a&quot;\abar\a"\a&quot;\a\a>\a&gt;\a:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<h1>&lt;div id=&quot;foo&quot;</h1>
<p>class=&quot;bar&quot;&gt;</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_124():
    """
    Test case 124:  (part 2) The tag on the first line can be partial, as long
                    as it is split where there would be whitespace:
    """

    # Arrange
    source_markdown = """<div id="foo" class="bar
  baz">
</div>"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<div id="foo" class="bar\n  baz">\n</div>:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div id="foo" class="bar
  baz">
</div>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_125():
    """
    Test case 125:  An open tag need not be closed:
    """

    # Arrange
    source_markdown = """<div>
*foo*

*bar*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div>\n*foo*:]",
        "[end-html-block:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[emphasis(4,1):1:*]",
        "[text(4,2):bar:]",
        "[end-emphasis(4,5)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<div>
*foo*
<p><em>bar</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_126():
    """
    Test case 126:  (part 1) A partial tag need not even be completed (garbage in, garbage out):
    """

    # Arrange
    source_markdown = """<div id="foo"
*hi*"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<div id="foo"\n*hi*:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div id="foo"
*hi*"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_127():
    """
    Test case 127:  (part 2) A partial tag need not even be completed (garbage in, garbage out):
    """

    # Arrange
    source_markdown = """<div class
foo"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div class\nfoo:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div class
foo"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_128():
    """
    Test case 128:  The initial tag doesn’t even need to be a valid tag, as long as it starts like one:
    """

    # Arrange
    source_markdown = """<div *???-&&&-<---
*foo*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div *???-&&&-<---\n*foo*:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div *???-&&&-<---
*foo*"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_129():
    """
    Test case 129:  (part 1) In type 6 blocks, the initial tag need not be on a line by itself:
    """

    # Arrange
    source_markdown = """<div><a href="bar">*foo*</a></div>"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<div><a href="bar">*foo*</a></div>:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div><a href="bar">*foo*</a></div>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_130():
    """
    Test case 130:  (part 2) In type 6 blocks, the initial tag need not be on a line by itself:
    """

    # Arrange
    source_markdown = """<table><tr><td>
foo
</td></tr></table>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<table><tr><td>\nfoo\n</td></tr></table>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<table><tr><td>
foo
</td></tr></table>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_131():
    """
    Test case 131:  Everything until the next blank line or end of document gets included in the HTML block.
    """

    # Arrange
    source_markdown = """<div></div>
``` c
int x = 33;
```"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div></div>\n``` c\nint x = 33;\n```:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div></div>
``` c
int x = 33;
```"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_132():
    """
    Test case 132:  To start an HTML block with a tag that is not in the list of
                    block-level tags in (6), you must put the tag by itself on
                    the first line (and it must be complete):
    """

    # Arrange
    source_markdown = """<a href="foo">
*bar*
</a>"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<a href="foo">\n*bar*\n</a>:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<a href="foo">
*bar*
</a>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_133():
    """
    Test case 133:  (part 1) In type 7 blocks, the tag name can be anything:
    """

    # Arrange
    source_markdown = """<Warning>
*bar*
</Warning>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<Warning>\n*bar*\n</Warning>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<Warning>
*bar*
</Warning>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_134():
    """
    Test case 134:  (part 2) In type 7 blocks, the tag name can be anything:
    """

    # Arrange
    source_markdown = """<i class="foo">
*bar*
</i>"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<i class="foo">\n*bar*\n</i>:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<i class="foo">
*bar*
</i>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_135():
    """
    Test case 135:  (part 3) In type 7 blocks, the tag name can be anything:
    """

    # Arrange
    source_markdown = """</ins>
*bar*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):</ins>\n*bar*:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """</ins>
*bar*"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_136():
    """
    Test case 136:  These rules are designed to allow us to work with tags that
                    can function as either block-level or inline-level tags. The
                    <del> tag is a nice example. We can surround content with <del>
                    tags in three different ways. In this case, we get a raw HTML
                    block, because the <del> tag is on a line by itself:
    """

    # Arrange
    source_markdown = """<del>
*foo*
</del>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<del>\n*foo*\n</del>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<del>
*foo*
</del>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_137():
    """
    Test case 137:  In this case, we get a raw HTML block that just includes the
                    <del> tag (because it ends with the following blank line).
                    So the contents get interpreted as CommonMark:
    """

    # Arrange
    source_markdown = """<del>

*foo*

</del>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<del>:]",
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[emphasis(3,1):1:*]",
        "[text(3,2):foo:]",
        "[end-emphasis(3,5)::]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[html-block(5,1)]",
        "[text(5,1):</del>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<del>
<p><em>foo</em></p>
</del>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_138():
    """
    Test case 138:  Finally, in this case, the <del> tags are interpreted as raw
                    HTML inside the CommonMark paragraph. (Because the tag is not
                    on a line by itself, we get inline HTML rather than an HTML
                    block.)
    """

    # Arrange
    source_markdown = """<del>*foo*</del>"""
    expected_tokens = [
        "[para(1,1):]",
        "[raw-html(1,1):del]",
        "[emphasis(1,6):1:*]",
        "[text(1,7):foo:]",
        "[end-emphasis(1,10)::]",
        "[raw-html(1,11):/del]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><del><em>foo</em></del></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_139():
    """
    Test case 139:  A pre tag (type 1):
    """

    # Arrange
    source_markdown = """<pre language="haskell"><code>
import Text.HTML.TagSoup

main :: IO ()
main = print $ parseTags tags
</code></pre>
okay"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<pre language="haskell"><code>\nimport Text.HTML.TagSoup:]',
        "[BLANK(3,1):]",
        "[text(4,1):main :: IO ()\nmain = print $ parseTags tags\n</code></pre>:]",
        "[end-html-block:::False]",
        "[para(7,1):]",
        "[text(7,1):okay:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre language="haskell"><code>
import Text.HTML.TagSoup

main :: IO ()
main = print $ parseTags tags
</code></pre>
<p>okay</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_140():
    """
    Test case 140:  A script tag (type 1):
    """

    # Arrange
    source_markdown = """<script type="text/javascript">
// JavaScript example

document.getElementById("demo").innerHTML = "Hello JavaScript!";
</script>
okay"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<script type="text/javascript">\n// JavaScript example:]',
        "[BLANK(3,1):]",
        '[text(4,1):document.getElementById("demo").innerHTML = "Hello JavaScript!";\n</script>:]',
        "[end-html-block:::False]",
        "[para(6,1):]",
        "[text(6,1):okay:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<script type="text/javascript">
// JavaScript example

document.getElementById("demo").innerHTML = "Hello JavaScript!";
</script>
<p>okay</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_141():
    """
    Test case 141:  A style tag (type 1):
    """

    # Arrange
    source_markdown = """<style
  type="text/css">
h1 {color:red;}

p {color:blue;}
</style>
okay"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<style\n  type="text/css">\nh1 {color:red;}:]',
        "[BLANK(4,1):]",
        "[text(5,1):p {color:blue;}\n</style>:]",
        "[end-html-block:::False]",
        "[para(7,1):]",
        "[text(7,1):okay:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<style
  type="text/css">
h1 {color:red;}

p {color:blue;}
</style>
<p>okay</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_142():
    """
    Test case 142:  (part 1) If there is no matching end tag, the block will end
                    at the end of the document (or the enclosing block quote or
                    list item):
    """

    # Arrange
    source_markdown = """<style
  type="text/css">

foo"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<style\n  type="text/css">:]',
        "[BLANK(3,1):]",
        "[text(4,1):foo:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<style
  type="text/css">

foo"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_142a():
    """
    Test case 142a:  variation of 142 with extra parameter
    """

    # Arrange
    source_markdown = """<style
  foo="bar"
  type="text/css">

foo"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<style\n  foo="bar"\n  type="text/css">:]',
        "[BLANK(4,1):]",
        "[text(5,1):foo:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<style
  foo="bar"
  type="text/css">

foo"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_143x():
    """
    Test case 143:  (part 2) If there is no matching end tag, the block will end
                    at the end of the document (or the enclosing block quote or
                    list item):
    """

    # Arrange
    source_markdown = """> <div>
> foo

bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[html-block(1,3)]",
        "[text(1,3):<div>\nfoo:]",
        "[end-html-block:::False]",
        "[end-block-quote:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<div>
foo
</blockquote>
<p>bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_143a():
    """
    Test case 143a:  variation of 143 with extra line
    """

    # Arrange
    source_markdown = """> <div>
> foo
> bar

bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[html-block(1,3)]",
        "[text(1,3):<div>\nfoo\nbar:]",
        "[end-html-block:::False]",
        "[end-block-quote:::False]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<div>
foo
bar
</blockquote>
<p>bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_143b():
    """
    Test case 143b:  variation of 143 with extra two lines
    """

    # Arrange
    source_markdown = """> <div>
> foo
> bar
> baz

bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[html-block(1,3)]",
        "[text(1,3):<div>\nfoo\nbar\nbaz:]",
        "[end-html-block:::False]",
        "[end-block-quote:::False]",
        "[BLANK(5,1):]",
        "[para(6,1):]",
        "[text(6,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<div>
foo
bar
baz
</blockquote>
<p>bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_143c():
    """
    Test case 143b:  variation of 143 with extra three lines
    """

    # Arrange
    source_markdown = """> <div>
>foo
> bar
>baz

bar"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n>]",
        "[html-block(1,3)]",
        "[text(1,3):<div>\nfoo\nbar\nbaz:]",
        "[end-html-block:::False]",
        "[end-block-quote:::False]",
        "[BLANK(5,1):]",
        "[para(6,1):]",
        "[text(6,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<div>
foo
bar
baz
</blockquote>
<p>bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_144():
    """
    Test case 144:  (part 3) If there is no matching end tag, the block will end
                    at the end of the document (or the enclosing block quote or
                    list item):
    """

    # Arrange
    source_markdown = """- <div>
- foo"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[html-block(1,3)]",
        "[text(1,3):<div>:]",
        "[end-html-block:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):foo:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<div>
</li>
<li>foo</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_144a():
    """
    Test case 144a:  Variation of 144 to add extra paragraph
    """

    # Arrange
    source_markdown = """- <div>
- foo

foo"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[html-block(1,3)]",
        "[text(1,3):<div>:]",
        "[end-html-block:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):foo:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ul>
<li>
<div>
</li>
<li>foo</li>
</ul>
<p>foo</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_145():
    """
    Test case 145:  (part 1) The end tag can occur on the same line as the start tag:
    """

    # Arrange
    source_markdown = """<style>p{color:red;}</style>
*foo*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<style>p{color:red;}</style>:]",
        "[end-html-block:::False]",
        "[para(2,1):]",
        "[emphasis(2,1):1:*]",
        "[text(2,2):foo:]",
        "[end-emphasis(2,5)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<style>p{color:red;}</style>
<p><em>foo</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_146():
    """
    Test case 146:  (part 2) The end tag can occur on the same line as the start tag:
    """

    # Arrange
    source_markdown = """<!-- foo -->*bar*
*baz*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<!-- foo -->*bar*:]",
        "[end-html-block:::False]",
        "[para(2,1):]",
        "[emphasis(2,1):1:*]",
        "[text(2,2):baz:]",
        "[end-emphasis(2,5)::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<!-- foo -->*bar*
<p><em>baz</em></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_147():
    """
    Test case 147:  Note that anything on the last line after the end tag will be included in the HTML block:
    """

    # Arrange
    source_markdown = """<script>
foo
</script>1. *bar*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<script>\nfoo\n</script>1. *bar*:]",
        "[end-html-block:::False]",
    ]
    expected_gfm = """<script>
foo
</script>1. *bar*"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_148():
    """
    Test case 148:  A comment (type 2):
    """

    # Arrange
    source_markdown = """<!-- Foo

bar
   baz -->
okay"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<!-- Foo:]",
        "[BLANK(2,1):]",
        "[text(3,1):bar\n   baz -->:]",
        "[end-html-block:::False]",
        "[para(5,1):]",
        "[text(5,1):okay:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<!-- Foo

bar
   baz -->
<p>okay</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_149():
    """
    Test case 149:  A processing instruction (type 3):
    """

    # Arrange
    source_markdown = """<?php

  echo '>';

?>
okay"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<?php:]",
        "[BLANK(2,1):]",
        "[text(3,3):echo '>';:  ]",
        "[BLANK(4,1):]",
        "[text(5,1):?>:]",
        "[end-html-block:::False]",
        "[para(6,1):]",
        "[text(6,1):okay:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<?php

  echo '>';

?>
<p>okay</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_150():
    """
    Test case 150:  A declaration (type 4):
    """

    # Arrange
    source_markdown = """<!DOCTYPE html>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<!DOCTYPE html>:]",
        "[end-html-block:::False]",
    ]
    expected_gfm = """<!DOCTYPE html>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_151():
    """
    Test case 151:  CDATA (type 5):
    """

    # Arrange
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
        "[html-block(1,1)]",
        "[text(1,1):<![CDATA[\nfunction matchwo(a,b)\n{\n  if (a < b && a < 0) then {\n    return 1;:]",
        "[BLANK(6,1):]",
        "[text(7,3):} else {:  ]",
        "[BLANK(8,1):]",
        "[text(9,5):return 0;\n  }\n}\n]]>:    ]",
        "[end-html-block:::False]",
        "[para(13,1):]",
        "[text(13,1):okay:]",
        "[end-para:::True]",
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

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_152():
    """
    Test case 152:  (part 1) The opening tag can be indented 1-3 spaces, but not 4:
    """

    # Arrange
    source_markdown = """  <!-- foo -->

    <!-- foo -->"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,3):<!-- foo -->:  ]",
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[icode-block(3,5):    :]",
        "[text(3,5):\a<\a&lt;\a!-- foo --\a>\a&gt;\a:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """  <!-- foo -->
<pre><code>&lt;!-- foo --&gt;
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_153():
    """
    Test case 153:  (part 2) The opening tag can be indented 1-3 spaces, but not 4:
    """

    # Arrange
    source_markdown = """  <div>

    <div>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,3):<div>:  ]",
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[icode-block(3,5):    :]",
        "[text(3,5):\a<\a&lt;\adiv\a>\a&gt;\a:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """  <div>
<pre><code>&lt;div&gt;
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_154():
    """
    Test case 154:  An HTML block of types 1–6 can interrupt a paragraph, and need not be preceded by a blank line.
    """

    # Arrange
    source_markdown = """Foo
<div>
bar
</div>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):Foo:]",
        "[end-para:::False]",
        "[html-block(2,1)]",
        "[text(2,1):<div>\nbar\n</div>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<p>Foo</p>
<div>
bar
</div>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_155():
    """
    Test case 155:  However, a following blank line is needed, except at the end
                    of a document, and except for blocks of types 1–5, above:
    """

    # Arrange
    source_markdown = """<div>
bar
</div>
*foo*"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div>\nbar\n</div>\n*foo*:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div>
bar
</div>
*foo*"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_156():
    """
    Test case 156:  HTML blocks of type 7 cannot interrupt a paragraph:
    """

    # Arrange
    source_markdown = """Foo
<a href="bar">
baz"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):Foo\n::\n]",
        '[raw-html(2,1):a href="bar"]',
        "[text(2,15):\nbaz::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo
<a href="bar">
baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_157():
    """
    Test case 157:  (part 1) This rule differs from John Gruber’s original Markdown syntax specification
    """

    # Arrange
    source_markdown = """<div>

*Emphasized* text.

</div>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div>:]",
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[emphasis(3,1):1:*]",
        "[text(3,2):Emphasized:]",
        "[end-emphasis(3,12)::]",
        "[text(3,13): text.:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[html-block(5,1)]",
        "[text(5,1):</div>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div>
<p><em>Emphasized</em> text.</p>
</div>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_158():
    """
    Test case 158:  (part 2) This rule differs from John Gruber’s original Markdown syntax specification
    """

    # Arrange
    source_markdown = """<div>
*Emphasized* text.
</div>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<div>\n*Emphasized* text.\n</div>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<div>
*Emphasized* text.
</div>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_159():
    """
    Test case 159:  The rule given above seems a simpler and more elegant way of
                    achieving the same expressive power, which is also much simpler
                    to parse.
    """

    # Arrange
    source_markdown = """<table>

<tr>

<td>
Hi
</td>

</tr>

</table>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<table>:]",
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[html-block(3,1)]",
        "[text(3,1):<tr>:]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
        "[html-block(5,1)]",
        "[text(5,1):<td>\nHi\n</td>:]",
        "[end-html-block:::False]",
        "[BLANK(8,1):]",
        "[html-block(9,1)]",
        "[text(9,1):</tr>:]",
        "[end-html-block:::False]",
        "[BLANK(10,1):]",
        "[html-block(11,1)]",
        "[text(11,1):</table>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<table>
<tr>
<td>
Hi
</td>
</tr>
</table>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_160():
    """
    Test case 160:  The rule given above seems a simpler and more elegant way of
                    achieving the same expressive power, which is also much simpler
                    to parse.
    """

    # Arrange
    source_markdown = """<table>

  <tr>

    <td>
      Hi
    </td>

  </tr>

</table>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<table>:]",
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[html-block(3,1)]",
        "[text(3,3):<tr>:  ]",
        "[end-html-block:::False]",
        "[BLANK(4,1):]",
        "[icode-block(5,5):    :\n    \n    ]",
        "[text(5,5):\a<\a&lt;\atd\a>\a&gt;\a\n  Hi\n\a<\a&lt;\a/td\a>\a&gt;\a:]",
        "[end-icode-block:::False]",
        "[BLANK(8,1):]",
        "[html-block(9,1)]",
        "[text(9,3):</tr>:  ]",
        "[end-html-block:::False]",
        "[BLANK(10,1):]",
        "[html-block(11,1)]",
        "[text(11,1):</table>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<table>
  <tr>
<pre><code>&lt;td&gt;
  Hi
&lt;/td&gt;
</code></pre>
  </tr>
</table>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_160a():
    """
    Test case 160a:  variation of 160 with the blank lines removed
    """

    # Arrange
    source_markdown = """<table>
  <tr>
    <td>
      Hi
    </td>
  </tr>
</table>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<table>\n  <tr>\n    <td>\n      Hi\n    </td>\n  </tr>\n</table>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<table>
  <tr>
    <td>
      Hi
    </td>
  </tr>
</table>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_cov1():
    """
    Test case cov1:  Based on coverage analysis.
    """

    # Arrange
    source_markdown = """<hr/>
</x-table>

</x-table>"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<hr/>\n</x-table>:]",
        "[end-html-block:::False]",
        "[BLANK(3,1):]",
        "[html-block(4,1)]",
        "[text(4,1):</x-table>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<hr/>
</x-table>
</x-table>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_cov2x():
    """
    Test case cov2:  Based on coverage analysis.
    """

    # Arrange
    source_markdown = """</hrx
>
</x-table>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\a/hrx:]",
        "[end-para:::True]",
        "[block-quote(2,1)::>]",
        "[BLANK(2,2):]",
        "[end-block-quote:::True]",
        "[html-block(3,1)]",
        "[text(3,1):</x-table>:]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<p>&lt;/hrx</p>
<blockquote>
</blockquote>
</x-table>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_cov2a():
    """
    Test case cov2:  Based on coverage analysis.
    """

    # Arrange
    source_markdown = """</hrx
>
> </x-table>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\a/hrx:]",
        "[end-para:::True]",
        "[block-quote(2,1)::>\n> ]",
        "[BLANK(2,2):]",
        "[html-block(3,3)]",
        "[text(3,3):</x-table>:]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p>&lt;/hrx</p>
<blockquote>
</x-table>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_cov2b():
    """
    Test case cov2:  Based on coverage analysis.
    """

    # Arrange
    source_markdown = """</hrx
>
 </x-table>"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\a<\a&lt;\a/hrx:]",
        "[end-para:::True]",
        "[block-quote(2,1)::>]",
        "[BLANK(2,2):]",
        "[end-block-quote:::True]",
        "[html-block(3,1)]",
        "[text(3,2):</x-table>: ]",
        "[end-html-block:::True]",
    ]
    expected_gfm = """<p>&lt;/hrx</p>
<blockquote>
</blockquote>
 </x-table>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_cov3():
    """
    Test case cov3:  Based on coverage analysis.
    """

    # Arrange
    source_markdown = """<!bad>
</x-table>"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):\a<\a&lt;\a!bad\a>\a&gt;\a\n::\n]",
        "[raw-html(2,1):/x-table]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;!bad&gt;
</x-table></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_cov4():
    """
    Test case cov4:  Based on coverage analysis.
    """

    # Arrange
    source_markdown = """<
bad>
</x-table>"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):\a<\a&lt;\a\nbad\a>\a&gt;\a\n::\n\n]",
        "[raw-html(3,1):/x-table]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&lt;
bad&gt;
</x-table></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_01x():
    """
    Test case extra 01:  start a "list block" within a HTML code block
    """

    # Arrange
    source_markdown = """<script>
- some text
some other text
</script>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<script>\n- some text\nsome other text\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<script>
- some text
some other text
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_01a():
    """
    Test case extra 01:  variation of 1 with a LRD instead of text
    """

    # Arrange
    source_markdown = """<script>
- [foo]:
/url
</script>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<script>\n- [foo]:\n/url\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<script>
- [foo]:
/url
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_02x():
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """- <script>
- some text
some other text
</script>
"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n\n]",
        "[html-block(1,3)]",
        "[text(1,3):<script>:]",
        "[end-html-block:::True]",
        "[li(2,1):2::]",
        "[para(2,3):\n\n]",
        "[text(2,3):some text\nsome other text\n::\n\n]",
        "[raw-html(4,1):/script]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<script>
</li>
<li>some text
some other text
</script></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_02a():
    """
    Test case extra 02:  variation of 2 with LRD

    NOTE: Due to https://talk.commonmark.org/t/block-quotes-laziness-and-link-reference-definitions/3751
          the GFM output has been adjusted to compensate for PyMarkdown using a token and not parsing
          the text afterwards.
    """

    # Arrange
    source_markdown = """- <script>
- [foo]:
/url
</script>
"""

    expected_tokens = [
        "[ulist(1,1):-::2::\n\n]",
        "[html-block(1,3)]",
        "[text(1,3):<script>:]",
        "[end-html-block:::True]",
        "[li(2,1):2::]",
        "[para(2,3):\n\n]",
        "[text(2,3):[:]",
        "[text(2,4):foo:]",
        "[text(2,7):]:]",
        "[text(2,8)::\n/url\n::\n\n]",
        "[raw-html(4,1):/script]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<script>
</li>
<li>[foo]:
/url
</script></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_02b():
    """
    Test case extra 02:  variation of 2a with extra indents

    NOTE: Due to https://talk.commonmark.org/t/block-quotes-laziness-and-link-reference-definitions/3751
          the GFM output has been adjusted to compensate for PyMarkdown using a token and not parsing
          the text afterwards.
    """

    # Arrange
    source_markdown = """- <script>
- [foo]:
 /url
 script
"""

    expected_tokens = [
        "[ulist(1,1):-::2::\n\n]",
        "[html-block(1,3)]",
        "[text(1,3):<script>:]",
        "[end-html-block:::True]",
        "[li(2,1):2::]",
        "[para(2,3):\n \n ]",
        "[text(2,3):[:]",
        "[text(2,4):foo:]",
        "[text(2,7):]:]",
        "[text(2,8)::\n/url\nscript::\n\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<script>
</li>
<li>[foo]:
/url
script</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_02c():
    """
    Test case extra 02:  variation of 2b without indents

    NOTE: Due to https://talk.commonmark.org/t/block-quotes-laziness-and-link-reference-definitions/3751
          the GFM output has been adjusted to compensate for PyMarkdown using a token and not parsing
          the text afterwards.
    """

    # Arrange
    source_markdown = """- <script>
- [foo]:
/url
script
"""

    expected_tokens = [
        "[ulist(1,1):-::2::\n\n]",
        "[html-block(1,3)]",
        "[text(1,3):<script>:]",
        "[end-html-block:::True]",
        "[li(2,1):2::]",
        "[para(2,3):\n\n]",
        "[text(2,3):[:]",
        "[text(2,4):foo:]",
        "[text(2,7):]:]",
        "[text(2,8)::\n/url\nscript::\n\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<script>
</li>
<li>[foo]:
/url
script</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_03x():
    """
    Test case extra 03:  variation of 2 without list start on line 2
    """

    # Arrange
    source_markdown = """- <script>
  some text
some other text
</script>
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[html-block(1,3)]",
        "[text(1,3):<script>\nsome text:]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
        "[para(3,1):\n]",
        "[text(3,1):some other text\n::\n]",
        "[raw-html(4,1):/script]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ul>
<li>
<script>
some text
</li>
</ul>
<p>some other text
</script></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_03a():
    """
    Test case extra 03:  variation of 3 with LRD
    """

    # Arrange
    source_markdown = """- <script>
  [foo]:
/url
</script>
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[html-block(1,3)]",
        "[text(1,3):<script>\n[foo]::]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
        "[para(3,1):\n]",
        "[text(3,1):/url\n::\n]",
        "[raw-html(4,1):/script]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ul>
<li>
<script>
[foo]:
</li>
</ul>
<p>/url
</script></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_04x():
    """
    Test case extra 04:  variation of 1 with "block quote" on line 2
    """

    # Arrange
    source_markdown = """<script>
> some text
some other text
</script>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<script>\n> some text\nsome other text\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<script>
> some text
some other text
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_04a():
    """
    Test case extra 04:  variation of 4 with LRD
    """

    # Arrange
    source_markdown = """<script>
> [foo]:
/url
</script>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<script>\n> [foo]:\n/url\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<script>
> [foo]:
/url
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_05x():
    """
    Test case extra 05:  variation of 4 with HTML block in block quote
    """

    # Arrange
    source_markdown = """> <script>
> some text
some other text
</script>
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[html-block(1,3)]",
        "[text(1,3):<script>\nsome text:]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
        "[para(3,1):\n]",
        "[text(3,1):some other text\n::\n]",
        "[raw-html(4,1):/script]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<script>
some text
</blockquote>
<p>some other text
</script></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_05a():
    """
    Test case extra 05:  variation of 5 with LRD
    """

    # Arrange
    source_markdown = """> <script>
> [foo]:
/url
</script>
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[html-block(1,3)]",
        "[text(1,3):<script>\n[foo]::]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
        "[para(3,1):\n]",
        "[text(3,1):/url\n::\n]",
        "[raw-html(4,1):/script]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<script>
[foo]:
</blockquote>
<p>/url
</script></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_06x():
    """
    Test case extra 06:  variation of 4 with start on line 1 and not line 2
    """

    # Arrange
    source_markdown = """> <script>
  some text
some other text
</script>
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[html-block(1,3)]",
        "[text(1,3):<script>:]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
        "[para(2,3):  \n\n]",
        "[text(2,3):some text\nsome other text\n::\n\n]",
        "[raw-html(4,1):/script]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<script>
</blockquote>
<p>some text
some other text
</script></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_06a():
    """
    Test case extra 06:  variation of 6 with LRD

    NOTE: Due to https://talk.commonmark.org/t/block-quotes-laziness-and-link-reference-definitions/3751
          the GFM output has been adjusted to compensate for PyMarkdown using a token and not parsing
          the text afterwards.
    """

    # Arrange
    source_markdown = """> <script>
  [foo]:
/url
</script>
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[html-block(1,3)]",
        "[text(1,3):<script>:]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
        "[link-ref-def(2,3):True:  :foo::\n:/url:::::]",
        "[html-block(4,1)]",
        "[text(4,1):</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<script>
</blockquote>
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_07():
    """
    Test case extra 07:  mixed "block quotes" and "list blocks" inside of HTML block
    """

    # Arrange
    source_markdown = """<script>
* a
  > b
  >
* c
</script>
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<script>\n* a\n  > b\n  >\n* c\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<script>
* a
  > b
  >
* c
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_08x():
    """
    Test case extra 08
    """

    # Arrange
    source_markdown = """1. abc
   <!-- comment
   def:
      - ghi
   -->"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[html-block(2,4)]",
        "[text(2,4):<!-- comment\ndef:\n   - ghi\n-->:]",
        "[end-html-block:::False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<!-- comment
def:
   - ghi
-->
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_08a():
    """
    Test case extra 08
    """

    # Arrange
    source_markdown = """- abc
  <!-- comment
  def:
     - ghi
  -->"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,3):<!-- comment\ndef:\n   - ghi\n-->:]",
        "[end-html-block:::False]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<!-- comment
def:
   - ghi
-->
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_08b():
    """
    Test case extra 08
    """

    # Arrange
    source_markdown = """> abc
> <!-- comment
> def:
>    - ghi
> -->"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,3):<!-- comment\ndef:\n   - ghi\n-->:]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<!-- comment
def:
   - ghi
-->
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_08c():
    """
    Test case extra 08
    """

    # Arrange
    source_markdown = """1. abc
   <!-- comment
   def:
1. ghi
   -->"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[html-block(2,4)]",
        "[text(2,4):<!-- comment\ndef::]",
        "[end-html-block:::True]",
        "[li(4,1):3::1]",
        "[para(4,4):\n]",
        "[text(4,4):ghi\n--\a>\a&gt;\a::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<!-- comment
def:
</li>
<li>ghi
--&gt;</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_08d():
    """
    Test case extra 08
    """

    # Arrange
    source_markdown = """- abc
  <!-- comment
  def:
- ghi
  -->"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,3):<!-- comment\ndef::]",
        "[end-html-block:::True]",
        "[li(4,1):2::]",
        "[para(4,3):\n]",
        "[text(4,3):ghi\n--\a>\a&gt;\a::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<!-- comment
def:
</li>
<li>ghi
--&gt;</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_08e():
    """
    Test case extra 09
    """

    # Arrange
    source_markdown = """1. abc
   <!-- comment
   def:
   1. ghi
   -->"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[html-block(2,4)]",
        "[text(2,4):<!-- comment\ndef:\n1. ghi\n-->:]",
        "[end-html-block:::False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<!-- comment
def:
1. ghi
-->
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_08f():
    """
    Test case extra 08
    """

    # Arrange
    source_markdown = """- abc
  <!-- comment
  def:
  - ghi
  -->"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,3):<!-- comment\ndef:\n- ghi\n-->:]",
        "[end-html-block:::False]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<!-- comment
def:
- ghi
-->
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_09x():
    """
    Test case extra 09
    """

    # Arrange
    source_markdown = """1. abc
   <!-- comment
   def:
   > ghi
   -->"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[html-block(2,4)]",
        "[text(2,4):<!-- comment\ndef:\n> ghi\n-->:]",
        "[end-html-block:::False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<!-- comment
def:
> ghi
-->
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_html_blocks_extra_09a():
    """
    Test case extra 09
    """

    # Arrange
    source_markdown = """- abc
  <!-- comment
  def:
  > ghi
  -->"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[html-block(2,3)]",
        "[text(2,3):<!-- comment\ndef:\n> ghi\n-->:]",
        "[end-html-block:::False]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<!-- comment
def:
> ghi
-->
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
