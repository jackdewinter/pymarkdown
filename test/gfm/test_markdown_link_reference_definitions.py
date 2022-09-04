# pylint: disable=too-many-lines
"""
https://github.github.com/gfm/#link-reference-definitions
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_link_reference_definitions_161():
    """
    Test case 161:  (part 1) A link reference definition does not correspond to a structural element of a document.
    """

    # Arrange
    source_markdown = """[foo]: /url "title"

[foo]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/url:title::::foo:False::::]",
        "[text(3,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_162():
    """
    Test case 162:  (part 2) A link reference definition does not correspond to a structural element of a document.
    """

    # Arrange
    source_markdown = """   [foo]:\a
      /url\a\a
           'the title'\a\a

[foo]""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[link-ref-def(1,4):True:   :foo:: \n      :/url::  \n           :the title:'the title':  ]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[link(5,1):shortcut:/url:the title::::foo:False::::]",
        "[text(5,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="the title">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_163():
    """
    Test case 163:  (part 3) A link reference definition does not correspond to a structural element of a document.
    """

    # Arrange
    source_markdown = """[Foo*bar\\]]:my_(url) 'title (with parens)'

[Foo*bar\\]]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo*bar\\]:Foo*bar\\]::my_(url):: :title (with parens):'title (with parens)':]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:my_(url):title (with parens)::::Foo*bar\\]:False::::]",
        "[text(3,2):Foo:]",
        "[text(3,5):*:]",
        "[text(3,6):bar\\\b]:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="my_(url)" title="title (with parens)">Foo*bar]</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_164():
    """
    Test case 164:  (part 4) A link reference definition does not correspond to a structural element of a document.
    """

    # Arrange
    source_markdown = """[Foo bar]:
<my url>
'title'

[Foo bar]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo bar:Foo bar:\n:my%20url:<my url>:\n:title:'title':]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[link(5,1):shortcut:my%20url:title::::Foo bar:False::::]",
        "[text(5,2):Foo bar:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="my%20url" title="title">Foo bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_165():
    """
    Test case 165:  The title may extend over multiple lines:
    """

    # Arrange
    source_markdown = """[foo]: /url '
title
line1
line2
'

[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:: :\ntitle\nline1\nline2\n:'\ntitle\nline1\nline2\n':]",
        "[BLANK(6,1):]",
        "[para(7,1):]",
        "[link(7,1):shortcut:/url:\ntitle\nline1\nline2\n::::foo:False::::]",
        "[text(7,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url" title="
title
line1
line2
">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_165a():
    """
    Test case 165a:  variation of 165 to try and include a blank line
    """

    # Arrange
    source_markdown = """[foo

bar]: /url 'title'

[foo\n\nbar]"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):bar:]",
        "[text(3,4):]:]",
        "[text(3,5):: /url 'title':]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):foo:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[para(7,1):]",
        "[text(7,1):bar:]",
        "[text(7,4):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo</p>
<p>bar]: /url 'title'</p>
<p>[foo</p>
<p>bar]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_166():
    """
    Test case 166:  However, it may not contain a blank line:
    """

    # Arrange
    source_markdown = """[foo]: /url 'title

with blank line'

[foo]"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        "[text(1,6):: /url 'title:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):with blank line':]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):foo:]",
        "[text(5,5):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]: /url 'title</p>
<p>with blank line'</p>
<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_166a():
    """
    Test case 166a:  variation of 166 to try and include a blank line
        in the title
    """

    # Arrange
    source_markdown = """[foo]: /url 'title
with blank line

[foo]"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        "[text(1,6):: /url 'title\nwith blank line::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):[:]",
        "[text(4,2):foo:]",
        "[text(4,5):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]: /url 'title\nwith blank line</p>\n<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_166b():
    """
    Test case 166b:  variation of 166 to try and include a newline into the title
    """

    # Arrange
    source_markdown = """[foo]: /url
'title
with blank line

[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[para(2,1):\n]",
        "[text(2,1):'title\nwith blank line::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[link(5,1):shortcut:/url:::::foo:False::::]",
        "[text(5,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>'title\nwith blank line</p>\n<p><a href="/url">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_167():
    """
    Test case 167:  The title may be omitted:
    """

    # Arrange
    source_markdown = """[foo]:
/url

[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo::\n:/url:::::]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[link(4,1):shortcut:/url:::::foo:False::::]",
        "[text(4,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_168():
    """
    Test case 168:  The link destination may not be omitted:
    """

    # Arrange
    source_markdown = """[foo]:

[foo]"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        "[text(1,6):::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):foo:]",
        "[text(3,5):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]:</p>
<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_169():
    """
    Test case 169:  However, an empty link destination may be specified using angle brackets:
    """

    # Arrange
    source_markdown = """[foo]: <>

[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: ::<>::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut::::::foo:False::::]",
        "[text(3,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_170():
    """
    Test case 170:  The title must be separated from the link destination by whitespace:
    """

    # Arrange
    source_markdown = """[foo]: <bar>(baz)

[foo]"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        "[text(1,6):: :]",
        "[raw-html(1,8):bar]",
        "[text(1,13):(baz):]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):foo:]",
        "[text(3,5):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]: <bar>(baz)</p>
<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_171():
    """
    Test case 171:  Both title and destination can contain backslash escapes and literal backslashes:
    """

    # Arrange
    source_markdown = """[foo]: /url\\bar\\*baz "foo\\"bar\\baz"

[foo]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::foo:: :/url%5Cbar*baz:/url\\bar\\*baz: :foo&quot;bar\\baz:"foo\\"bar\\baz":]',
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/url%5Cbar*baz:foo&quot;bar\\baz::::foo:False::::]",
        "[text(3,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="/url%5Cbar*baz" title="foo&quot;bar\\baz">foo</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_172():
    """
    Test case 172:  A link can come before its corresponding definition:
    """

    # Arrange
    source_markdown = """[foo]

[foo]: url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:url:::::foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :url:::::]",
    ]
    expected_gfm = """<p><a href="url">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_173():
    """
    Test case 173:  If there are several matching definitions, the first one takes precedence:
    """

    # Arrange
    source_markdown = """[foo]

[foo]: first
[foo]: second"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:first:::::foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :first:::::]",
        "[link-ref-def(4,1):False::foo:: :second:::::]",
    ]
    expected_gfm = """<p><a href="first">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_174():
    """
    Test case 174:  (part 1) As noted in the section on Links, matching of labels is case-insensitive (see matches).
    """

    # Arrange
    source_markdown = """[FOO]: /url

[Foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:FOO: :/url:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/url:::::Foo:False::::]",
        "[text(3,2):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/url">Foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_175():
    """
    Test case 175:  (part 2) As noted in the section on Links, matching of labels is case-insensitive (see matches).
    """

    # Arrange
    source_markdown = """[ΑΓΩ]: /φου

[αγω]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::αγω:ΑΓΩ: :/%CF%86%CE%BF%CF%85:/φου::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/%CF%86%CE%BF%CF%85:::::αγω:False::::]",
        "[text(3,2):αγω:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/%CF%86%CE%BF%CF%85">αγω</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_176():
    """
    Test case 176:  Here is a link reference definition with no corresponding
                    link. It contributes nothing to the document.
    """

    # Arrange
    source_markdown = """[foo]: /url"""
    expected_tokens = ["[link-ref-def(1,1):True::foo:: :/url:::::]"]
    expected_gfm = """"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_177():
    """
    Test case 177:  Here is another one:
    """

    # Arrange
    source_markdown = """[
foo
]: /url
bar"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:\nfoo\n: :/url:::::]",
        "[para(4,1):]",
        "[text(4,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_178():
    """
    Test case 178:  This is not a link reference definition, because there are
                    non-whitespace characters after the title:
    """

    # Arrange
    source_markdown = """[foo]: /url "title" ok"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        '[text(1,6):: /url \a"\a&quot;\atitle\a"\a&quot;\a ok:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]: /url &quot;title&quot; ok</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_179():
    """
    Test case 179:  This is a link reference definition, but it has no title:
    """

    # Arrange
    source_markdown = """[foo]: /url
"title" ok"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[para(2,1):]",
        '[text(2,1):\a"\a&quot;\atitle\a"\a&quot;\a ok:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>&quot;title&quot; ok</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_180():
    """
    Test case 180:  This is not a link reference definition, because it is indented four spaces:
    """

    # Arrange
    source_markdown = """    [foo]: /url "title"

[foo]"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        '[text(1,5):[foo]: /url \a"\a&quot;\atitle\a"\a&quot;\a:]',
        "[end-icode-block:::False]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[:]",
        "[text(3,2):foo:]",
        "[text(3,5):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>[foo]: /url &quot;title&quot;
</code></pre>
<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_181():
    """
    Test case 181:  This is not a link reference definition, because it occurs inside a code block:
    """

    # Arrange
    source_markdown = """```
[foo]: /url
```

[foo]"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):[foo]: /url:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):[:]",
        "[text(5,2):foo:]",
        "[text(5,5):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>[foo]: /url
</code></pre>
<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_182():
    """
    Test case 182:  A link reference definition cannot interrupt a paragraph.
    """

    # Arrange
    source_markdown = """Foo
[bar]: /baz

[bar]"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):Foo\n::\n]",
        "[text(2,1):[:]",
        "[text(2,2):bar:]",
        "[text(2,5):]:]",
        "[text(2,6):: /baz:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):[:]",
        "[text(4,2):bar:]",
        "[text(4,5):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo
[bar]: /baz</p>
<p>[bar]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183():
    """
    Test case 183:  (part 1) However, it can directly follow other block elements,
                    such as headings and thematic breaks, and it need not be followed
                    by a blank line.
    """

    # Arrange
    source_markdown = """# [Foo]
[foo]: /url
> bar"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3)::\a \a\x03\a]",
        "[link(1,3):shortcut:/url:::::Foo:False::::]",
        "[text(1,4):Foo:]",
        "[end-link::]",
        "[end-atx::]",
        "[link-ref-def(2,1):True::foo:: :/url:::::]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<h1><a href="/url">Foo</a></h1>
<blockquote>
<p>bar</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183a():
    """
    Test case 183a:  variation of 183 with it following a thematic break
    """

    # Arrange
    source_markdown = """---
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[tbreak(1,1):-::---]",
        "[link-ref-def(2,1):True::foo:: :/url:::::]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[link(3,3):shortcut:/url:::::Foo:False::::]",
        "[text(3,4):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<hr />
<blockquote>
<p><a href="/url">Foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183b():
    """
    Test case 183b:  variation of 183 with it following a SetExt Heading
    """

    # Arrange
    source_markdown = """abc
---
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):abc:]",
        "[end-setext::]",
        "[link-ref-def(3,1):True::foo:: :/url:::::]",
        "[block-quote(4,1)::> ]",
        "[para(4,3):]",
        "[link(4,3):shortcut:/url:::::Foo:False::::]",
        "[text(4,4):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<h2>abc</h2>
<blockquote>
<p><a href="/url">Foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183c():
    """
    Test case 183a:  variation of 183 with it following an indented code block
    """

    # Arrange
    source_markdown = """    indented code block
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):indented code block:]",
        "[end-icode-block:::False]",
        "[link-ref-def(2,1):True::foo:: :/url:::::]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[link(3,3):shortcut:/url:::::Foo:False::::]",
        "[text(3,4):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<pre><code>indented code block
</code></pre>
<blockquote>
<p><a href="/url">Foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183d():
    """
    Test case 183d:  variation of 183 with it following a fenced code block
    """

    # Arrange
    source_markdown = """```text
indented code block
```
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:text:::::]",
        "[text(2,1):indented code block:]",
        "[end-fcode-block:::3:False]",
        "[link-ref-def(4,1):True::foo:: :/url:::::]",
        "[block-quote(5,1)::> ]",
        "[para(5,3):]",
        "[link(5,3):shortcut:/url:::::Foo:False::::]",
        "[text(5,4):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<pre><code class="language-text">indented code block
</code></pre>
<blockquote>
<p><a href="/url">Foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183e():
    """
    Test case 183e:  variation of 183 with it following a HTML block
    """

    # Arrange
    source_markdown = """<script>
<~-- javascript comment -->
</script>
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<script>\n<~-- javascript comment -->\n</script>:]",
        "[end-html-block:::False]",
        "[link-ref-def(4,1):True::foo:: :/url:::::]",
        "[block-quote(5,1)::> ]",
        "[para(5,3):]",
        "[link(5,3):shortcut:/url:::::Foo:False::::]",
        "[text(5,4):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<script>
<~-- javascript comment -->
</script>
<blockquote>
<p><a href="/url">Foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183f():
    """
    Test case 183f:  variation of 183 with it following a block quote
    """

    # Arrange
    source_markdown = """> A simple block quote
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n\n> ]",
        "[para(1,3):\n\n]",
        "[text(1,3):A simple block quote\n::\n]",
        "[text(2,1):[:]",
        "[text(2,2):foo:]",
        "[text(2,5):]:]",
        "[text(2,6):: /url\n::\n]",
        "[text(3,3):[:]",
        "[text(3,4):Foo:]",
        "[text(3,7):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>A simple block quote
[foo]: /url
[Foo]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183gx():
    """
    Test case 183g:  variation of 183 with it following a list
    """

    # Arrange
    source_markdown = """- A simple list
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n]",
        "[text(1,3):A simple list\n::\n]",
        "[text(2,1):[:]",
        "[text(2,2):foo:]",
        "[text(2,5):]:]",
        "[text(2,6):: /url:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[:]",
        "[text(3,4):Foo:]",
        "[text(3,7):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ul>
<li>A simple list
[foo]: /url</li>
</ul>
<blockquote>
<p>[Foo]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183ga():
    """
    Test case 183ga:  variation of 183g with an improperly started LRD
    """

    # Arrange
    source_markdown = """- A simple list
foo]: /url
> [Foo]"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n]",
        "[text(1,3):A simple list\nfoo::\n]",
        "[text(2,4):]:]",
        "[text(2,5):: /url:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[:]",
        "[text(3,4):Foo:]",
        "[text(3,7):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ul>
<li>A simple list
foo]: /url</li>
</ul>
<blockquote>
<p>[Foo]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183gb():
    """
    Test case 183ga:  variation of 183g with an improperly indented LRD
    """

    # Arrange
    source_markdown = """- A simple list
 [foo]: /url
> [Foo]"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n ]",
        "[text(1,3):A simple list\n::\n]",
        "[text(2,2):[:]",
        "[text(2,3):foo:]",
        "[text(2,6):]:]",
        "[text(2,7):: /url:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[:]",
        "[text(3,4):Foo:]",
        "[text(3,7):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ul>
<li>A simple list
[foo]: /url</li>
</ul>
<blockquote>
<p>[Foo]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183gc():
    """
    Test case 183ga:  variation of 183g with an improperly started LRD
        within an ordered list
    """

    # Arrange
    source_markdown = """1. A simple list
 [foo]: /url
> [Foo]"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n ]",
        "[text(1,4):A simple list\n::\n]",
        "[text(2,2):[:]",
        "[text(2,3):foo:]",
        "[text(2,6):]:]",
        "[text(2,7):: /url:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[:]",
        "[text(3,4):Foo:]",
        "[text(3,7):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ol>
<li>A simple list
[foo]: /url</li>
</ol>
<blockquote>
<p>[Foo]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183gd():
    """
    Test case 183gd:  variation of 183g with an overly indented LRD
    """

    # Arrange
    source_markdown = """- A simple list
    [foo]: /url
> [Foo]"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n  ]",
        "[text(1,3):A simple list\n::\n]",
        "[text(2,3):[:]",
        "[text(2,4):foo:]",
        "[text(2,7):]:]",
        "[text(2,8):: /url:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[:]",
        "[text(3,4):Foo:]",
        "[text(3,7):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ul>
<li>A simple list
[foo]: /url</li>
</ul>
<blockquote>
<p>[Foo]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183ge():
    """
    Test case 183ge:  variation of 183g with an improperly started LRD
    """

    # Arrange
    source_markdown = """- A simple list
*foo*: /url
> [Foo]"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n]",
        "[text(1,3):A simple list\n::\n]",
        "[emphasis(2,1):1:*]",
        "[text(2,2):foo:]",
        "[end-emphasis(2,5)::]",
        "[text(2,6):: /url:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[:]",
        "[text(3,4):Foo:]",
        "[text(3,7):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ul>
<li>A simple list
<em>foo</em>: /url</li>
</ul>
<blockquote>
<p>[Foo]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183gf():
    """
    Test case 183gf:  variation of 183g with no LRD
    """

    # Arrange
    source_markdown = """- A simple list
items
> [Foo]"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n]",
        "[text(1,3):A simple list\nitems::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[:]",
        "[text(3,4):Foo:]",
        "[text(3,7):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ul>
<li>A simple list
items</li>
</ul>
<blockquote>
<p>[Foo]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183gg():
    """
    Test case 183ga:  variation of 183g with a list before and a block quote after
    """

    # Arrange
    source_markdown = """- A simple list
[foo]: /url
  > [Foo]"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n]",
        "[para(1,3):\n]",
        "[text(1,3):A simple list\n::\n]",
        "[text(2,1):[:]",
        "[text(2,2):foo:]",
        "[text(2,5):]:]",
        "[text(2,6):: /url:]",
        "[end-para:::True]",
        "[block-quote(3,3):  :  > ]",
        "[para(3,5):]",
        "[text(3,5):[:]",
        "[text(3,6):Foo:]",
        "[text(3,9):]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>A simple list
[foo]: /url
<blockquote>
<p>[Foo]</p>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_184():
    """
    Test case 184:  (part 2) However, it can directly follow other block elements,
                    such as headings and thematic breaks, and it need not be followed
                    by a blank line.
    """

    # Arrange
    source_markdown = """[foo]: /url
bar
===
[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[setext(3,1):=:3::(2,1)]",
        "[text(2,1):bar:]",
        "[end-setext::]",
        "[para(4,1):]",
        "[link(4,1):shortcut:/url:::::foo:False::::]",
        "[text(4,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<h1>bar</h1>
<p><a href="/url">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_185():
    """
    Test case 185:  (part 3) However, it can directly follow other block elements,
                    such as headings and thematic breaks, and it need not be followed
                    by a blank line.
    """

    # Arrange
    source_markdown = """[foo]: /url
===
[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[para(2,1):\n]",
        "[text(2,1):===\n::\n]",
        "[link(3,1):shortcut:/url:::::foo:False::::]",
        "[text(3,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>===
<a href="/url">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_185a():
    """
    Test case 185a:  variation of 185 with Atx Heading between
    """

    # Arrange
    source_markdown = """[foo]: /url
# Abc
[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[atx(2,1):1:0:]",
        "[text(2,3):Abc: ]",
        "[end-atx::]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/url:::::foo:False::::]",
        "[text(3,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<h1>Abc</h1>
<p><a href="/url">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_185b():
    """
    Test case 185b:  variation of 185 with fenced code block between
    """

    # Arrange
    source_markdown = """[foo]: /url
```text
my text
```
[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[fcode-block(2,1):`:3:text:::::]",
        "[text(3,1):my text:]",
        "[end-fcode-block:::3:False]",
        "[para(5,1):]",
        "[link(5,1):shortcut:/url:::::foo:False::::]",
        "[text(5,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code class="language-text">my text
</code></pre>
<p><a href="/url">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_185c():
    """
    Test case 185c:  variation of 185 with indented code block between
    """

    # Arrange
    source_markdown = """[foo]: /url
    my text
[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[icode-block(2,5):    :]",
        "[text(2,5):my text:]",
        "[end-icode-block:::False]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/url:::::foo:False::::]",
        "[text(3,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<pre><code>my text\n</code></pre>\n<p><a href="/url">foo</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_185d():
    """
    Test case 185d:  variation of 185 with HTML Block between
    """

    # Arrange
    source_markdown = """[foo]: /url
<script>
<~-- javascript comment -->
</script>
[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[html-block(2,1)]",
        "[text(2,1):<script>\n<~-- javascript comment -->\n</script>:]",
        "[end-html-block:::False]",
        "[para(5,1):]",
        "[link(5,1):shortcut:/url:::::foo:False::::]",
        "[text(5,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<script>
<~-- javascript comment -->
</script>
<p><a href="/url">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_185e():
    """
    Test case 185a:  variation of 185 with Block Quote between
    """

    # Arrange
    source_markdown = """[foo]: /url
> This is a simple block quote
[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[block-quote(2,1)::> \n]",
        "[para(2,3):\n]",
        "[text(2,3):This is a simple block quote\n::\n]",
        "[link(3,1):shortcut:/url:::::foo:False::::]",
        "[text(3,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>This is a simple block quote
<a href="/url">foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_185fx():
    """
    Test case 185a:  variation of 185 with List between
    """

    # Arrange
    source_markdown = """[foo]: /url
- This is a simple list
[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[ulist(2,1):-::2::]",
        "[para(2,3):\n]",
        "[text(2,3):This is a simple list\n::\n]",
        "[link(3,1):shortcut:/url:::::foo:False::::]",
        "[text(3,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>This is a simple list
<a href="/url">foo</a></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_185fa():
    """
    Test case 185fa: variation of 185f with image
    """

    # Arrange
    source_markdown = """[foo]: /url
- This is a simple list
![foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[ulist(2,1):-::2::]",
        "[para(2,3):\n]",
        "[text(2,3):This is a simple list\n::\n]",
        "[image(3,1):shortcut:/url::foo::::foo:False::::]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>This is a simple list
<img src="/url" alt="foo" /></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_186():
    """
    Test case 186:  Several link reference definitions can occur one after another, without intervening blank lines.
    """

    # Arrange
    source_markdown = """[foo]: /foo-url "foo"
[bar]: /bar-url
  "bar"
[baz]: /baz-url

[foo],
[bar],
[baz]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::foo:: :/foo-url:: :foo:"foo":]',
        '[link-ref-def(2,1):True::bar:: :/bar-url::\n  :bar:"bar":]',
        "[link-ref-def(4,1):True::baz:: :/baz-url:::::]",
        "[BLANK(5,1):]",
        "[para(6,1):\n\n]",
        "[link(6,1):shortcut:/foo-url:foo::::foo:False::::]",
        "[text(6,2):foo:]",
        "[end-link::]",
        "[text(6,6):,\n::\n]",
        "[link(7,1):shortcut:/bar-url:bar::::bar:False::::]",
        "[text(7,2):bar:]",
        "[end-link::]",
        "[text(7,6):,\n::\n]",
        "[link(8,1):shortcut:/baz-url:::::baz:False::::]",
        "[text(8,2):baz:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/foo-url" title="foo">foo</a>,
<a href="/bar-url" title="bar">bar</a>,
<a href="/baz-url">baz</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_187():
    """
    Test case 187:  Link reference definitions can occur inside block containers,
                    like lists and block quotations. They affect the entire document,
                    not just the container in which they are defined:
    """

    # Arrange
    source_markdown = """[foo]

> [foo]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/url:::::foo:False::::]",
        "[text(1,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> ]",
        "[link-ref-def(3,3):True::foo:: :/url:::::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p><a href="/url">foo</a></p>
<blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188():
    """
    Test case 188:  Whether something is a link reference definition is independent
                    of whether the link reference it defines is used in the document.
    """

    # Arrange
    source_markdown = """[foo]: /url"""
    expected_tokens = ["[link-ref-def(1,1):True::foo:: :/url:::::]"]
    expected_gfm = """"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188a():
    """
    Test case 188a: variation of 188 with only start
    """

    # Arrange
    source_markdown = """["""
    expected_tokens = ["[para(1,1):]", "[text(1,1):[:]", "[end-para:::True]"]
    expected_gfm = """<p>[</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188b():
    """
    Test case 188b: variation of 188 with only start and text
    """

    # Arrange
    source_markdown = """[foo"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188c():
    """
    Test case 188c: variation of 188 with only link label
    """

    # Arrange
    source_markdown = """[foo]"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188d():
    """
    Test case 188d: variation of 188 with only link label and following colon
    """

    # Arrange
    source_markdown = """[foo]:"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        "[text(1,6):::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]:</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188e():
    """
    Test case 188e: variation of 188 with only link label and url, and start of title
    """

    # Arrange
    source_markdown = """[foo]: /url ("""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo:]",
        "[text(1,5):]:]",
        "[text(1,6):: /url (:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]: /url (</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01():
    """
    Test case extra 01:  LRD within list item

    NOTE: Due to https://talk.commonmark.org/t/block-quotes-laziness-and-link-reference-definitions/3751
          the GFM output has been adjusted to compensate for PyMarkdown using a token and not parsing
          the text afterwards.
    """

    # Arrange
    source_markdown = """- [foo]:
/url"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n]",
        "[text(1,3):[:]",
        "[text(1,4):foo:]",
        "[text(1,7):]:]",
        "[text(1,8)::\n/url::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>[foo]:
/url</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01a():
    """
    Test case extra 01a:  variation on 1 with proper indent
    """

    # Arrange
    source_markdown = """- [foo]:
  /url"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[link-ref-def(1,3):True::foo::\n:/url:::::]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01b():
    """
    Test case extra 01b:  variation on 1 with almost proper indent

    NOTE: Due to https://talk.commonmark.org/t/block-quotes-laziness-and-link-reference-definitions/3751
          the GFM output has been adjusted to compensate for PyMarkdown using a token and not parsing
          the text afterwards.
    """

    # Arrange
    source_markdown = """- [foo]:
 /url"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n ]",
        "[text(1,3):[:]",
        "[text(1,4):foo:]",
        "[text(1,7):]:]",
        "[text(1,8)::\n/url::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>[foo]:
/url</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01c():
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- [foo]:
- /url"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):[:]",
        "[text(1,4):foo:]",
        "[text(1,7):]:]",
        "[text(1,8):::]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):/url:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>[foo]:</li>
<li>/url</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01d():
    """
    Test case extra 01d:  variation of 1 split across ordered list items
    """

    # Arrange
    source_markdown = """1. [foo]:
1. /url"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):[:]",
        "[text(1,5):foo:]",
        "[text(1,8):]:]",
        "[text(1,9):::]",
        "[end-para:::True]",
        "[li(2,1):3::1]",
        "[para(2,4):]",
        "[text(2,4):/url:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>[foo]:</li>
<li>/url</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_02x():
    """
    Test case extra 02:  variation
    """

    # Arrange
    source_markdown = """> [foo]:
/url"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):\n]",
        "[text(1,3):[:]",
        "[text(1,4):foo:]",
        "[text(1,7):]:]",
        "[text(1,8)::\n/url::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>[foo]:
/url</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_02a():
    """
    Test case extra 02a:  variation of 2 within block quote
    """

    # Arrange
    source_markdown = """> [foo]:
> /url"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[link-ref-def(1,3):True::foo::\n:/url:::::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_02bx():
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """> [foo]:
>> /url"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):[:]",
        "[text(1,4):foo:]",
        "[text(1,7):]:]",
        "[text(1,8):::]",
        "[end-para:::True]",
        "[block-quote(2,1)::>> ]",
        "[para(2,4):]",
        "[text(2,4):/url:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>[foo]:</p>
<blockquote>
<p>/url</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_02ba():
    """
    Test case extra 02ba:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """> [foo]:
>>> /url"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):[:]",
        "[text(1,4):foo:]",
        "[text(1,7):]:]",
        "[text(1,8):::]",
        "[end-para:::True]",
        "[block-quote(2,1)::]",
        "[block-quote(2,2)::>>> ]",
        "[para(2,5):]",
        "[text(2,5):/url:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>[foo]:</p>
<blockquote>
<blockquote>
<p>/url</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_02cx():
    """
    Test case extra 02c:  variation of 2 within decreasing quote
    """

    # Arrange
    source_markdown = """>> [foo]:
> /url"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::>> \n> ]",
        "[para(1,4):\n]",
        "[text(1,4):[:]",
        "[text(1,5):foo:]",
        "[text(1,8):]:]",
        "[text(1,9)::\n/url::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>[foo]:
/url</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_02ca():
    """
    Test case extra 02c:  variation of 2 within more decreasing quote
    """

    # Arrange
    source_markdown = """>>> [foo]:
> /url"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::]",
        "[block-quote(1,3)::>>> \n> ]",
        "[para(1,5):\n]",
        "[text(1,5):[:]",
        "[text(1,6):foo:]",
        "[text(1,9):]:]",
        "[text(1,10)::\n/url::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>[foo]:
/url</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
