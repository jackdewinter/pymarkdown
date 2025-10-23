# pylint: disable=too-many-lines
"""
https://github.github.com/gfm/#link-reference-definitions
"""
from test.utils import act_and_assert

import pytest

config_map = {"extensions": {"markdown-tables": {"enabled": True}}}


@pytest.mark.gfm
def test_link_reference_definitions_161() -> None:
    """
    Test case 161:  (part 1) A link reference definition does not correspond to a structural element of a document.

    test_tables_extension_198_enabled_x
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
def test_link_reference_definitions_162() -> None:
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
def test_link_reference_definitions_163() -> None:
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
        "[text(3,2):Foo*bar\\\b]:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p><a href="my_(url)" title="title (with parens)">Foo*bar]</a></p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_164() -> None:
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
def test_link_reference_definitions_165() -> None:
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
def test_link_reference_definitions_165a() -> None:
    """
    Test case 165a:  variation of 165 to try and include a blank line
    """

    # Arrange
    source_markdown = """[foo

bar]: /url 'title'

[foo\n\nbar]"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[foo:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):bar]: /url 'title':]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):[foo:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[para(7,1):]",
        "[text(7,1):bar]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo</p>
<p>bar]: /url 'title'</p>
<p>[foo</p>
<p>bar]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_166() -> None:
    """
    Test case 166:  However, it may not contain a blank line:
    """

    # Arrange
    source_markdown = """[foo]: /url 'title

with blank line'

[foo]"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[foo]: /url 'title:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):with blank line':]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):[foo]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]: /url 'title</p>
<p>with blank line'</p>
<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_166a() -> None:
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
        "[text(1,1):[foo]: /url 'title\nwith blank line::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):[foo]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]: /url 'title\nwith blank line</p>\n<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_166b() -> None:
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
def test_link_reference_definitions_167() -> None:
    """
    Test case 167:  The title may be omitted:

    test_tables_extension_202_enabled
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
def test_link_reference_definitions_168() -> None:
    """
    Test case 168:  The link destination may not be omitted:
    """

    # Arrange
    source_markdown = """[foo]:

[foo]"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[foo]::]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[foo]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]:</p>
<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_169() -> None:
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
def test_link_reference_definitions_170() -> None:
    """
    Test case 170:  The title must be separated from the link destination by whitespace:
    """

    # Arrange
    source_markdown = """[foo]: <bar>(baz)

[foo]"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[foo]: :]",
        "[raw-html(1,8):bar]",
        "[text(1,13):(baz):]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):[foo]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]: <bar>(baz)</p>
<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_171() -> None:
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
def test_link_reference_definitions_172() -> None:
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
def test_link_reference_definitions_173() -> None:
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
def test_link_reference_definitions_174() -> None:
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
def test_link_reference_definitions_175() -> None:
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
def test_link_reference_definitions_176() -> None:
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
def test_link_reference_definitions_177() -> None:
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
def test_link_reference_definitions_178() -> None:
    """
    Test case 178:  This is not a link reference definition, because there are
                    non-whitespace characters after the title:
    """

    # Arrange
    source_markdown = """[foo]: /url "title" ok"""
    expected_tokens = [
        "[para(1,1):]",
        '[text(1,1):[foo]: /url \a"\a&quot;\atitle\a"\a&quot;\a ok:]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]: /url &quot;title&quot; ok</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_179() -> None:
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
def test_link_reference_definitions_180() -> None:
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
        "[text(3,1):[foo]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>[foo]: /url &quot;title&quot;
</code></pre>
<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_181() -> None:
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
        "[text(5,1):[foo]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>[foo]: /url
</code></pre>
<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_182() -> None:
    """
    Test case 182:  A link reference definition cannot interrupt a paragraph.

    test_whitespaces_tables_with_paragraph_before
    """

    # Arrange
    source_markdown = """Foo
[bar]: /baz

[bar]"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):Foo\n[bar]: /baz::\n]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):[bar]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo
[bar]: /baz</p>
<p>[bar]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183x() -> None:
    """
    Test case 183:  (part 1) However, it can directly follow other block elements,
                    such as headings and thematic breaks, and it need not be followed
                    by a blank line.

    test_whitespaces_tables_with_atx_before
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
def test_link_reference_definitions_183a() -> None:
    """
    Test case 183a:  variation of 183 with it following a thematic break

    test_whitespaces_tables_with_thematic_before
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
def test_link_reference_definitions_183b() -> None:
    """
    Test case 183b:  variation of 183 with it following a SetExt Heading

    test_whitespaces_tables_with_setext_before
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
def test_link_reference_definitions_183c() -> None:
    """
    Test case 183a:  variation of 183 with it following an indented code block

    test_whitespaces_tables_with_indented_code_block_before
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
def test_link_reference_definitions_183d() -> None:
    """
    Test case 183d:  variation of 183 with it following a fenced code block

    test_whitespaces_tables_with_fenced_code_block_before
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
def test_link_reference_definitions_183e() -> None:
    """
    Test case 183e:  variation of 183 with it following a HTML block

    test_whitespaces_tables_with_html_block_before
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
def test_link_reference_definitions_183fx() -> None:
    """
    Test case 183f:  variation of 183 with it following a block quote
                     due to the paragraph started in the block quote,
                     the LRD is not valid and is a continuation of the paragraph

    test_whitespaces_tables_with_block_quote_before_with_no_blank_in_bq
    """

    # Arrange
    source_markdown = """> A simple block quote
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n\n> ]",
        "[para(1,3):\n\n]",
        "[text(1,3):A simple block quote\n[foo]: /url\n[Foo]::\n\n]",
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
def test_link_reference_definitions_183fa() -> None:
    """
    Test case 183f:  variation of 183 with it following a block quote
                     due to the paragraph started in the block quote,
                     the LRD is not valid and is a continuation of the paragraph

    test_whitespaces_tables_with_block_quote_before_with_blank_in_bq
    """

    # Arrange
    source_markdown = """> this is a block quote
>
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>]",
        "[para(1,3):]",
        "[text(1,3):this is a block quote:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[end-block-quote:::True]",
        "[link-ref-def(3,1):True::foo:: :/url:::::]",
        "[block-quote(4,1)::> ]",
        "[para(4,3):]",
        "[link(4,3):shortcut:/url:::::Foo:False::::]",
        "[text(4,4):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>this is a block quote</p>
</blockquote>
<blockquote>
<p><a href="/url">Foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183fb() -> None:
    """
    Test case 183f:  variation of 183 with it following a block quote
                     due to the paragraph started in the block quote,
                     the LRD is not valid and is a continuation of the paragraph

    test_whitespaces_tables_with_block_quote_before_with_only_blank_in_bq
    """

    # Arrange
    source_markdown = """>
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[link-ref-def(2,1):True::foo:: :/url:::::]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[link(3,3):shortcut:/url:::::Foo:False::::]",
        "[text(3,4):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<blockquote>
<p><a href="/url">Foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183gxx() -> None:
    """
    Test case 183g:  variation of 183 with it following a list

    test_whitespaces_tables_with_unordered_before_with_no_blank_in_list
    """

    # Arrange
    source_markdown = """- A simple list
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):\n]",
        "[text(1,3):A simple list\n[foo]: /url::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[Foo]:]",
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
def test_link_reference_definitions_183gxa() -> None:
    """
    Test case 183g:  variation of 183 with it following a list

    test_whitespaces_tables_with_unordered_before_with_only_blank_in_list
    """

    # Arrange
    source_markdown = """-
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[BLANK(1,2):]",
        "[end-ulist:::True]",
        "[link-ref-def(2,1):True::foo:: :/url:::::]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[link(3,3):shortcut:/url:::::Foo:False::::]",
        "[text(3,4):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ul>
<li></li>
</ul>
<blockquote>
<p><a href="/url">Foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183gxb() -> None:
    """
    Test case 183g:  variation of 183 with it following a list

    test_whitespaces_tables_with_unordered_list_before_with_blank_in_list
    """

    # Arrange
    source_markdown = """- this is a block quote

[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):]",
        "[text(1,3):this is a block quote:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[end-ulist:::True]",
        "[link-ref-def(3,1):True::foo:: :/url:::::]",
        "[block-quote(4,1)::> ]",
        "[para(4,3):]",
        "[link(4,3):shortcut:/url:::::Foo:False::::]",
        "[text(4,4):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ul>
<li>this is a block quote</li>
</ul>
<blockquote>
<p><a href="/url">Foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183gxc() -> None:
    """
    Test case 183g:  variation of 183 with it following a list

    test_whitespaces_tables_with_ordered_list_before_with_blank_in_list
    """

    # Arrange
    source_markdown = """1. this is a block quote

[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):this is a block quote:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[end-olist:::True]",
        "[link-ref-def(3,1):True::foo:: :/url:::::]",
        "[block-quote(4,1)::> ]",
        "[para(4,3):]",
        "[link(4,3):shortcut:/url:::::Foo:False::::]",
        "[text(4,4):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ol>
<li>this is a block quote</li>
</ol>
<blockquote>
<p><a href="/url">Foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183gxd() -> None:
    """
    Test case 183g:  variation of 183 with it following a list

    test_whitespaces_tables_with_ordered_before_with_no_blank_in_list
    """

    # Arrange
    source_markdown = """1. this is a block quote
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n]",
        "[text(1,4):this is a block quote\n[foo]: /url::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[Foo]:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ol>
<li>this is a block quote
[foo]: /url</li>
</ol>
<blockquote>
<p>[Foo]</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183gxe() -> None:
    """
    Test case 183g:  variation of 183 with it following a list

    test_whitespaces_tables_with_ordered_before_with_only_blank_in_list
    """

    # Arrange
    source_markdown = """1.
[foo]: /url
> [Foo]"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[link-ref-def(2,1):True::foo:: :/url:::::]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[link(3,3):shortcut:/url:::::Foo:False::::]",
        "[text(3,4):Foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<blockquote>
<p><a href="/url">Foo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183ga() -> None:
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
        "[text(1,3):A simple list\nfoo]: /url::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[Foo]:]",
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
def test_link_reference_definitions_183gb() -> None:
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
        "[text(1,3):A simple list\n[foo]: /url::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[Foo]:]",
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
def test_link_reference_definitions_183gc() -> None:
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
        "[text(1,4):A simple list\n[foo]: /url::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[Foo]:]",
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
def test_link_reference_definitions_183gd() -> None:
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
        "[text(1,3):A simple list\n[foo]: /url::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text(3,3):[Foo]:]",
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
def test_link_reference_definitions_183ge() -> None:
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
        "[text(3,3):[Foo]:]",
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
def test_link_reference_definitions_183gf() -> None:
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
        "[text(3,3):[Foo]:]",
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
def test_link_reference_definitions_183gg() -> None:
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
        "[text(1,3):A simple list\n[foo]: /url::\n]",
        "[end-para:::True]",
        "[block-quote(3,3):  :  > ]",
        "[para(3,5):]",
        "[text(3,5):[Foo]:]",
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
def test_link_reference_definitions_184() -> None:
    """
    Test case 184:  (part 2) However, it can directly follow other block elements,
                    such as headings and thematic breaks, and it need not be followed
                    by a blank line.

    test_tables_extension_202_enabled
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
def test_link_reference_definitions_185x() -> None:
    """
    Test case 185:  (part 3) However, it can directly follow other block elements,
                    such as headings and thematic breaks, and it need not be followed
                    by a blank line.

    - test_tables_extension_202_enabled, related
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
def test_link_reference_definitions_185ax() -> None:
    """
    Test case 185a:  variation of 185 with Atx Heading between

    test_tables_extension_201_enabled_ax
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
def test_link_reference_definitions_185aa() -> None:
    """
    Test case 185a:  variation of 185 with Atx Heading between
    """

    # Arrange
    source_markdown = """[foo]: /url
'start of
# Abc
[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[para(2,1):]",
        "[text(2,1):'start of:]",
        "[end-para:::False]",
        "[atx(3,1):1:0:]",
        "[text(3,3):Abc: ]",
        "[end-atx::]",
        "[para(4,1):]",
        "[link(4,1):shortcut:/url:::::foo:False::::]",
        "[text(4,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>'start of</p>
<h1>Abc</h1>
<p><a href="/url">foo</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_185b() -> None:
    """
    Test case 185b:  variation of 185 with fenced code block between

    test_tables_extension_201_enabled_dx
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
def test_link_reference_definitions_185c() -> None:
    """
    Test case 185c:  variation of 185 with indented code block between

    test_tables_extension_201_enabled_cx
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
def test_link_reference_definitions_185d() -> None:
    """
    Test case 185d:  variation of 185 with HTML Block between

    test_tables_extension_201_enabled_ex
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
def test_link_reference_definitions_185e() -> None:
    """
    Test case 185a:  variation of 185 with Block Quote between

    test_tables_extension_201_enabled_x
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
def test_link_reference_definitions_185fx() -> None:
    """
    Test case 185a:  variation of 185 with List between

    test_tables_extension_201_enabled_hx
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
def test_link_reference_definitions_185fa() -> None:
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
def test_link_reference_definitions_185gx() -> None:
    """
    Test case 185a:  variation of 185 with List between

    test_tables_extension_201_enabled_gx
    """

    # Arrange
    source_markdown = """[foo]: /url
1. This is a simple list
   [foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[olist(2,1):.:1:3::   ]",
        "[para(2,4):\n]",
        "[text(2,4):This is a simple list\n::\n]",
        "[link(3,1):shortcut:/url:::::foo:False::::]",
        "[text(3,2):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>This is a simple list
<a href="/url">foo</a></li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_186() -> None:
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
def test_link_reference_definitions_187() -> None:
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
def test_link_reference_definitions_188x() -> None:
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
def test_link_reference_definitions_188a() -> None:
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
def test_link_reference_definitions_188b() -> None:
    """
    Test case 188b: variation of 188 with only start and text
    """

    # Arrange
    source_markdown = """[foo"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):[foo:]", "[end-para:::True]"]
    expected_gfm = """<p>[foo</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188c() -> None:
    """
    Test case 188c: variation of 188 with only link label
    """

    # Arrange
    source_markdown = """[foo]"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):[foo]:]", "[end-para:::True]"]
    expected_gfm = """<p>[foo]</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188d() -> None:
    """
    Test case 188d: variation of 188 with only link label and following colon
    """

    # Arrange
    source_markdown = """[foo]:"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):[foo]::]", "[end-para:::True]"]
    expected_gfm = """<p>[foo]:</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188e() -> None:
    """
    Test case 188e: variation of 188 with only link label and url, and start of title
    """

    # Arrange
    source_markdown = """[foo]: /url ("""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[foo]: /url (:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo]: /url (</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01cx() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- [foo]:
- /url"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):[foo]::]",
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
def test_link_reference_definitions_extra_01ca() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- abc
- [foo]: /url"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[link-ref-def(2,3):True::foo:: :/url:::::]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc</li>
<li></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01cb() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- [foo]: /url
- 'abc'"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[link-ref-def(1,3):True::foo:: :/url:::::]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):'abc':]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li></li>
<li>'abc'</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01cc() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- [foo]: /url
- abc"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[link-ref-def(1,3):True::foo:: :/url:::::]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):abc:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li></li>
<li>abc</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01cd() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- [foo]: /url
  - abc"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[link-ref-def(1,3):True::foo:: :/url:::::]",
        "[ulist(2,3):-::4:  ]",
        "[para(2,5):]",
        "[text(2,5):abc:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li>abc</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01ce() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
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
def test_link_reference_definitions_extra_01cf() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- [foo]:
  /url
  'title'"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[link-ref-def(1,3):True::foo::\n:/url::\n:title:'title':]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01cg() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- [foo]: /url
  - [foo2]: /url2"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[link-ref-def(1,3):True::foo:: :/url:::::]",
        "[ulist(2,3):-::4:  ]",
        "[link-ref-def(2,5):True::foo2:: :/url2:::::]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<ul>
<li></li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01ch() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- [foo]: /url
- [foo2]: /url2"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[link-ref-def(1,3):True::foo:: :/url:::::]",
        "[li(2,1):2::]",
        "[link-ref-def(2,3):True::foo2:: :/url2:::::]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li></li>
<li></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01cj() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- [foo]: /url
[foo2]: /url2"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[link-ref-def(1,3):True::foo:: :/url:::::]",
        "[end-ulist:::True]",
        "[link-ref-def(2,1):True::foo2:: :/url2:::::]",
    ]
    expected_gfm = """<ul>
<li></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01ck() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- [foo]: /url
> [foo2]: /url2"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[link-ref-def(1,3):True::foo:: :/url:::::]",
        "[end-ulist:::True]",
        "[block-quote(2,1)::> ]",
        "[link-ref-def(2,3):True::foo2:: :/url2:::::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ul>
<li></li>
</ul>
<blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01cl() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- [foo]: /url
1. [foo2]: /url2"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[link-ref-def(1,3):True::foo:: :/url:::::]",
        "[end-ulist:::True]",
        "[olist(2,1):.:1:3:]",
        "[link-ref-def(2,4):True::foo2:: :/url2:::::]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ul>
<li></li>
</ul>
<ol>
<li></li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01cm() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- [foo]: /url
- [foo2]: /url2"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[link-ref-def(1,3):True::foo:: :/url:::::]",
        "[li(2,1):2::]",
        "[link-ref-def(2,3):True::foo2:: :/url2:::::]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li></li>
<li></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_01cn() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """- [foo]:
- /url"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):[foo]::]",
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
def test_link_reference_definitions_extra_01d() -> None:
    """
    Test case extra 01d:  variation of 1 split across ordered list items
    """

    # Arrange
    source_markdown = """1. [foo]:
1. /url"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):[foo]::]",
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
def test_link_reference_definitions_extra_02x() -> None:
    """
    Test case extra 02:  variation
    """
    ## NOTE: Difference in interpreation from CommonMark

    # Arrange
    source_markdown = """> [foo]:
/url"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[para(1,3):\n]",
        "[text(1,3):[foo]:\n/url::\n]",
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
def test_link_reference_definitions_extra_02ax() -> None:
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
def test_link_reference_definitions_extra_02aa() -> None:
    """
    Test case extra 02a:  variation of 2 within block quote
    """

    # Arrange
    source_markdown = """> [foo]:
> /url
> "abc"
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n]",
        '[link-ref-def(1,3):True::foo::\n:/url::\n:abc:"abc":]',
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_02bx() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """> [foo]:
>> /url"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):[foo]::]",
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
def test_link_reference_definitions_extra_02ba() -> None:
    """
    Test case extra 02ba:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """> [foo]:
>>> /url"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):[foo]::]",
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
def test_link_reference_definitions_extra_02cx() -> None:
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
        "[text(1,4):[foo]:\n/url::\n]",
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
def test_link_reference_definitions_extra_02ca() -> None:
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
        "[text(1,5):[foo]:\n/url::\n]",
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


@pytest.mark.gfm
def test_link_reference_definitions_extra_03x() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote

    renamed from test_link_reference_definitions_extra_02bcx
    """

    # Arrange
    source_markdown = """> [foo]:
>> [foo]:
>> # abc"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):[foo]::]",
        "[end-para:::True]",
        "[block-quote(2,1)::>> \n>> ]",
        "[para(2,4):]",
        "[text(2,4):[foo]::]",
        "[end-para:::False]",
        "[atx(3,4):1:0:]",
        "[text(3,6):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>[foo]:</p>
<blockquote>
<p>[foo]:</p>
<h1>abc</h1>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_03a() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """>> [foo]:
>> [foo]:
>> # abc"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::>> \n>> \n>> ]",
        "[link-ref-def(1,4):True::foo::\n:%5Bfoo%5D::[foo]:::::]",
        "[atx(3,4):1:0:]",
        "[text(3,6):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<h1>abc</h1>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_03b() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote

    # May seem like 2 LRD starts, but the LRD start itself qualifies as a link destination https://github.github.com/gfm/#link-destination
    """

    # Arrange
    source_markdown = """[foo]:
[foo]:
# abc"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo::\n:%5Bfoo%5D::[foo]:::::]",
        "[atx(3,1):1:0:]",
        "[text(3,3):abc: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>abc</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_03c() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """> # this is a heading
>> [foo]:
>> # abc"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[atx(1,3):1:0:]",
        "[text(1,5):this is a heading: ]",
        "[end-atx::]",
        "[block-quote(2,1)::>> \n>> ]",
        "[para(2,4):]",
        "[text(2,4):[foo]::]",
        "[end-para:::False]",
        "[atx(3,4):1:0:]",
        "[text(3,6):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h1>this is a heading</h1>
<blockquote>
<p>[foo]:</p>
<h1>abc</h1>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_03d() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """> this is a heading
> ---------
>> [foo]:
>> # abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[setext(2,3):-:9::(1,3)]",
        "[text(1,3):this is a heading:]",
        "[end-setext::]",
        "[block-quote(3,1)::>> \n>> ]",
        "[para(3,4):]",
        "[text(3,4):[foo]::]",
        "[end-para:::False]",
        "[atx(4,4):1:0:]",
        "[text(4,6):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h2>this is a heading</h2>
<blockquote>
<p>[foo]:</p>
<h1>abc</h1>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_03e() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """>     this is a heading
>> [foo]:
>> # abc"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[icode-block(1,7):    :]",
        "[text(1,7):this is a heading:]",
        "[end-icode-block:::True]",
        "[block-quote(2,1)::>> \n>> ]",
        "[para(2,4):]",
        "[text(2,4):[foo]::]",
        "[end-para:::False]",
        "[atx(3,4):1:0:]",
        "[text(3,6):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>this is a heading
</code></pre>
<blockquote>
<p>[foo]:</p>
<h1>abc</h1>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_03fx() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """> ```Python
> print("Hello World")
> ```
>> [foo]:
>> # abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[fcode-block(1,3):`:3:Python:::::]",
        '[text(2,3):print(\a"\a&quot;\aHello World\a"\a&quot;\a):]',
        "[end-fcode-block:::3:False]",
        "[block-quote(4,1)::>> \n>> ]",
        "[para(4,4):]",
        "[text(4,4):[foo]::]",
        "[end-para:::False]",
        "[atx(5,4):1:0:]",
        "[text(5,6):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-Python">print(&quot;Hello World&quot;)
</code></pre>
<blockquote>
<p>[foo]:</p>
<h1>abc</h1>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_03fa() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """> ```Python
> print("Hello World")
>> [foo]:
>> # abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>]",
        "[fcode-block(1,3):`:3:Python:::::]",
        '[text(2,3):print(\a"\a&quot;\aHello World\a"\a&quot;\a)\n\a>\a&gt;\a [foo]:\n\a>\a&gt;\a # abc:]',
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-Python">print(&quot;Hello World&quot;)
&gt; [foo]:
&gt; # abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_03gx() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """> <!-- comment -->
>> [foo]:
>> # abc"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[html-block(1,3)]",
        "[text(1,3):<!-- comment -->:]",
        "[end-html-block:::False]",
        "[block-quote(2,1)::>> \n>> ]",
        "[para(2,4):]",
        "[text(2,4):[foo]::]",
        "[end-para:::False]",
        "[atx(3,4):1:0:]",
        "[text(3,6):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<!-- comment -->
<blockquote>
<p>[foo]:</p>
<h1>abc</h1>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_03ga() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """> <some-tag>
>> [foo]:
>> # abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n>]",
        "[html-block(1,3)]",
        "[text(1,3):<some-tag>\n> [foo]:\n> # abc:]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<some-tag>
> [foo]:
> # abc
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_03gb() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """> <some-tag>
>
>> [foo]:
>> # abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>]",
        "[html-block(1,3)]",
        "[text(1,3):<some-tag>:]",
        "[end-html-block:::False]",
        "[BLANK(2,2):]",
        "[block-quote(3,1)::>> \n>> ]",
        "[para(3,4):]",
        "[text(3,4):[foo]::]",
        "[end-para:::False]",
        "[atx(4,4):1:0:]",
        "[text(4,6):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<some-tag>
<blockquote>
<p>[foo]:</p>
<h1>abc</h1>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_03h() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """> | title1 | title2 |
> | --- | --- |
> | r1c1 | r1c2 |
>> [foo]:
>> # abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):title1:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):title2:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):r1c1:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):r1c2:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[block-quote(4,1)::>> \n>> ]",
        "[para(4,4):]",
        "[text(4,4):[foo]::]",
        "[end-para:::False]",
        "[atx(5,4):1:0:]",
        "[text(5,6):abc: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>title1</th>
<th>title2</th>
</tr>
</thead>
<tbody>
<tr>
<td>r1c1</td>
<td>r1c2</td>
</tr>
</tbody>
</table>
<blockquote>
<p>[foo]:</p>
<h1>abc</h1>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
        show_debug=False,
    )


@pytest.mark.gfm
def test_link_reference_definitions_extra_04x() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """- [foo]:
  - [foo]:
    # abc"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):[foo]::]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :    ]",
        "[para(2,5):]",
        "[text(2,5):[foo]::]",
        "[end-para:::False]",
        "[atx(3,5):1:0:]",
        "[text(3,7):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>[foo]:
<ul>
<li>[foo]:
<h1>abc</h1>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_04a() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """- [foo]:
  [foo]:
  # abc"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[link-ref-def(1,3):True::foo::\n:%5Bfoo%5D::[foo]:::::]",
        "[atx(3,3):1:0:]",
        "[text(3,5):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h1>abc</h1>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_04b() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """- # heading
  - [foo]:
    # abc"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[atx(1,3):1:0:]",
        "[text(1,5):heading: ]",
        "[end-atx::]",
        "[ulist(2,3):-::4:  :    ]",
        "[para(2,5):]",
        "[text(2,5):[foo]::]",
        "[end-para:::False]",
        "[atx(3,5):1:0:]",
        "[text(3,7):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h1>heading</h1>
<ul>
<li>[foo]:
<h1>abc</h1>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_04c() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """- heading
  ==========
  - [foo]:
    # abc"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):=:10::(1,3)]",
        "[text(1,3):heading:]",
        "[end-setext::]",
        "[ulist(3,3):-::4:  :    ]",
        "[para(3,5):]",
        "[text(3,5):[foo]::]",
        "[end-para:::False]",
        "[atx(4,5):1:0:]",
        "[text(4,7):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h1>heading</h1>
<ul>
<li>[foo]:
<h1>abc</h1>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_04d() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """-     icb
  - [foo]:
    # abc"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[icode-block(1,7):    :]",
        "[text(1,7):icb:]",
        "[end-icode-block:::True]",
        "[ulist(2,3):-::4:  :    ]",
        "[para(2,5):]",
        "[text(2,5):[foo]::]",
        "[end-para:::False]",
        "[atx(3,5):1:0:]",
        "[text(3,7):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>icb
</code></pre>
<ul>
<li>[foo]:
<h1>abc</h1>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_04ex() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """- ```Python
  print("Hello World")
  ```
  - [foo]:
    # abc"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[fcode-block(1,3):`:3:Python:::::]",
        '[text(2,3):print(\a"\a&quot;\aHello World\a"\a&quot;\a):]',
        "[end-fcode-block:::3:False]",
        "[ulist(4,3):-::4:  :    ]",
        "[para(4,5):]",
        "[text(4,5):[foo]::]",
        "[end-para:::False]",
        "[atx(5,5):1:0:]",
        "[text(5,7):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code class="language-Python">print(&quot;Hello World&quot;)
</code></pre>
<ul>
<li>[foo]:
<h1>abc</h1>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_04ea() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """- ```Python
  print("Hello World")
  - [foo]:
    # abc"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[fcode-block(1,3):`:3:Python:::::]",
        '[text(2,3):print(\a"\a&quot;\aHello World\a"\a&quot;\a)\n- [foo]:\n  # abc:]',
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code class="language-Python">print(&quot;Hello World&quot;)
- [foo]:
  # abc
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_04fx() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """- <!-- comment -->
  - [foo]:
    # abc"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[html-block(1,3)]",
        "[text(1,3):<!-- comment -->:]",
        "[end-html-block:::False]",
        "[ulist(2,3):-::4:  :    ]",
        "[para(2,5):]",
        "[text(2,5):[foo]::]",
        "[end-para:::False]",
        "[atx(3,5):1:0:]",
        "[text(3,7):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<!-- comment -->
<ul>
<li>[foo]:
<h1>abc</h1>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_04fa() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """- <some-tag>
  - [foo]:
    # abc"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[html-block(1,3)]",
        "[text(1,3):<some-tag>\n- [foo]:\n  # abc:]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<some-tag>
- [foo]:
  # abc
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_04fb() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """- <some-tag>

  - [foo]:
    # abc"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[html-block(1,3)]",
        "[text(1,3):<some-tag>:]",
        "[end-html-block:::False]",
        "[BLANK(2,1):]",
        "[ulist(3,3):-::4:  :    ]",
        "[para(3,5):]",
        "[text(3,5):[foo]::]",
        "[end-para:::False]",
        "[atx(4,5):1:0:]",
        "[text(4,7):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<some-tag>
<ul>
<li>[foo]:
<h1>abc</h1>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_04g() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """- | title1 | title2 |
  | --- | --- |
  | r1c1 | r1c2 |
  - [foo]:
    # abc"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):title1:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):title2:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):r1c1:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):r1c2:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[ulist(4,3):-::4:  :    ]",
        "[para(4,5):]",
        "[text(4,5):[foo]::]",
        "[end-para:::False]",
        "[atx(5,5):1:0:]",
        "[text(5,7):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<table>
<thead>
<tr>
<th>title1</th>
<th>title2</th>
</tr>
</thead>
<tbody>
<tr>
<td>r1c1</td>
<td>r1c2</td>
</tr>
</tbody>
</table>
<ul>
<li>[foo]:
<h1>abc</h1>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
        show_debug=False,
    )


@pytest.mark.gfm
def test_link_reference_definitions_extra_05ax() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """- # heading
  - ## heading
    - [foo]:
      # abc"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[atx(1,3):1:0:]",
        "[text(1,5):heading: ]",
        "[end-atx::]",
        "[ulist(2,3):-::4:  ]",
        "[atx(2,5):2:0:]",
        "[text(2,8):heading: ]",
        "[end-atx::]",
        "[ulist(3,5):-::6:    :      ]",
        "[para(3,7):]",
        "[text(3,7):[foo]::]",
        "[end-para:::False]",
        "[atx(4,7):1:0:]",
        "[text(4,9):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h1>heading</h1>
<ul>
<li>
<h2>heading</h2>
<ul>
<li>[foo]:
<h1>abc</h1>
</li>
</ul>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_05aa() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """1. # heading
   1. # heading
      - [foo]:
      # abc"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[atx(1,4):1:0:]",
        "[text(1,6):heading: ]",
        "[end-atx::]",
        "[olist(2,4):.:1:6:   :      ]",
        "[atx(2,7):1:0:]",
        "[text(2,9):heading: ]",
        "[end-atx::]",
        "[ulist(3,7):-::8:      :]",
        "[para(3,9):]",
        "[text(3,9):[foo]::]",
        "[end-para:::False]",
        "[end-ulist:::True]",
        "[atx(4,7):1:0:]",
        "[text(4,9):abc: ]",
        "[end-atx::]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h1>heading</h1>
<ol>
<li>
<h1>heading</h1>
<ul>
<li>[foo]:</li>
</ul>
<h1>abc</h1>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_05ab() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """1. # heading
   1. # heading
      1. [foo]:
         # abc"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[atx(1,4):1:0:]",
        "[text(1,6):heading: ]",
        "[end-atx::]",
        "[olist(2,4):.:1:6:   ]",
        "[atx(2,7):1:0:]",
        "[text(2,9):heading: ]",
        "[end-atx::]",
        "[olist(3,7):.:1:9:      :         ]",
        "[para(3,10):]",
        "[text(3,10):[foo]::]",
        "[end-para:::False]",
        "[atx(4,10):1:0:]",
        "[text(4,12):abc: ]",
        "[end-atx::]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<h1>heading</h1>
<ol>
<li>
<h1>heading</h1>
<ol>
<li>[foo]:
<h1>abc</h1>
</li>
</ol>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_05bx() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """> # heading
> - ## heading
>   - [foo]:
>     # abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[atx(1,3):1:0:]",
        "[text(1,5):heading: ]",
        "[end-atx::]",
        "[ulist(2,3):-::4:]",
        "[atx(2,5):2:0:]",
        "[text(2,8):heading: ]",
        "[end-atx::]",
        "[ulist(3,5):-::6:  :    ]",
        "[para(3,7):]",
        "[text(3,7):[foo]::]",
        "[end-para:::False]",
        "[atx(4,7):1:0:]",
        "[text(4,9):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<h1>heading</h1>
<ul>
<li>
<h2>heading</h2>
<ul>
<li>[foo]:
<h1>abc</h1>
</li>
</ul>
</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_05cx() -> None:
    """
    Test case extra 02b:  variation of 2 within different block quote
    """

    # Arrange
    source_markdown = """- # heading
  > ## heading
  > - [foo]:
  >   # abc"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[atx(1,3):1:0:]",
        "[text(1,5):heading: ]",
        "[end-atx::]",
        "[block-quote(2,3):  :  > \n  > \n  > ]",
        "[atx(2,5):2:0:]",
        "[text(2,8):heading: ]",
        "[end-atx::]",
        "[ulist(3,5):-::6::  ]",
        "[para(3,7):]",
        "[text(3,7):[foo]::]",
        "[end-para:::False]",
        "[atx(4,7):1:0:]",
        "[text(4,9):abc: ]",
        "[end-atx::]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h1>heading</h1>
<blockquote>
<h2>heading</h2>
<ul>
<li>[foo]:
<h1>abc</h1>
</li>
</ul>
</blockquote>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, show_debug=False)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06a() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [fred]: /url
[fred]"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[link-ref-def(1,4):True::fred:: :/url:::::]",
        "[end-olist:::True]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06b() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [foo]:
   /url"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[link-ref-def(1,4):True::foo::\n:/url:::::]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06c() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [fred]: /url 'abc'
[fred]"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[link-ref-def(1,4):True::fred:: :/url:: :abc:'abc':]",
        "[end-olist:::True]",
        "[para(2,1):]",
        "[link(2,1):shortcut:/url:abc::::fred:False::::]",
        "[text(2,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<p><a href="/url" title="abc">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06d() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [foo]:
   /url
   'title'"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[link-ref-def(1,4):True::foo::\n:/url::\n:title:'title':]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06e() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [foo]: /url
[foo2]: /url2"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[link-ref-def(1,4):True::foo:: :/url:::::]",
        "[end-olist:::True]",
        "[link-ref-def(2,1):True::foo2:: :/url2:::::]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06f() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [foo]: /url
> [foo2]: /url2"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[link-ref-def(1,4):True::foo:: :/url:::::]",
        "[end-olist:::True]",
        "[block-quote(2,1)::> ]",
        "[link-ref-def(2,3):True::foo2:: :/url2:::::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06g() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [foo]: /url
> [foo2]: /url2"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[link-ref-def(1,4):True::foo:: :/url:::::]",
        "[end-olist:::True]",
        "[block-quote(2,1)::> ]",
        "[link-ref-def(2,3):True::foo2:: :/url2:::::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06h() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [foo]: /url
1. [foo2]: /url2"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[link-ref-def(1,4):True::foo:: :/url:::::]",
        "[li(2,1):3::1]",
        "[link-ref-def(2,4):True::foo2:: :/url2:::::]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
<li></li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06j() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1.
  [fred]: /url
[fred]"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[link-ref-def(2,3):True:  :fred:: :/url:::::]",
        "[para(3,1):]",
        "[link(3,1):shortcut:/url:::::fred:False::::]",
        "[text(3,2):fred:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<p><a href="/url">fred</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06k() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [foo]:
   /url"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[link-ref-def(1,4):True::foo::\n:/url:::::]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06l() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [foo]:
/url"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):\n]",
        "[text(1,4):[foo]:\n/url::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>[foo]:
/url</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06m() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [foo]: /url
   1. 'abc'"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[link-ref-def(1,4):True::foo:: :/url:::::]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):'abc':]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>'abc'</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06n() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [foo]: /url
   1. [foo2]: /url2"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[link-ref-def(1,4):True::foo:: :/url:::::]",
        "[olist(2,4):.:1:6:   ]",
        "[link-ref-def(2,7):True::foo2:: :/url2:::::]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06p() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. abc
1. [foo]: /url"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[li(2,1):3::1]",
        "[link-ref-def(2,4):True::foo:: :/url:::::]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
<li></li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06q() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [foo]: /url
1. abc"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[link-ref-def(1,4):True::foo:: :/url:::::]",
        "[li(2,1):3::1]",
        "[para(2,4):]",
        "[text(2,4):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
<li>abc</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_06r() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """1. [foo]: /url
1. [foo2]: /url2"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[link-ref-def(1,4):True::foo:: :/url:::::]",
        "[li(2,1):3::1]",
        "[link-ref-def(2,4):True::foo2:: :/url2:::::]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li></li>
<li></li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_07a() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """> [foo]: /url"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[link-ref-def(1,3):True::foo:: :/url:::::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_07b() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
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
        "[block-quote(2,1)::> ]",
        "[link-ref-def(2,3):True::foo:: :/url:::::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p><a href="/url">foo</a></p>
<blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_07c() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
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
        "[block-quote(2,1)::> ]",
        "[link-ref-def(2,3):True::foo:: :/url:::::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p><a href="/url">foo</a></p>
<blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_07d() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
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
        "[block-quote(2,1)::> ]",
        "[link-ref-def(2,3):True::foo:: :/url:::::]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p><a href="/url">foo</a></p>
<blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_07e() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """> [fred]: /url1
> > "title"
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[link-ref-def(1,3):True::fred:: :/url1:::::]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):]",
        '[text(2,5):\a"\a&quot;\atitle\a"\a&quot;\a:]',
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>&quot;title&quot;</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_07fx() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """> [fred]: /url1
> - "title"
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[link-ref-def(1,3):True::fred:: :/url1:::::]",
        "[ulist(2,3):-::4:]",
        "[para(2,5):]",
        '[text(2,5):\a"\a&quot;\atitle\a"\a&quot;\a:]',
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<ul>
<li>&quot;title&quot;</li>
</ul>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_07fa() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """> [fred]: /url1
- "title"
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[link-ref-def(1,3):True::fred:: :/url1:::::]",
        "[end-block-quote:::True]",
        "[ulist(2,1):-::2::]",
        "[para(2,3):]",
        '[text(2,3):\a"\a&quot;\atitle\a"\a&quot;\a:]',
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ul>
<li>&quot;title&quot;</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_07gx() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """> [fred]: /url1
> 1. "title"
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[link-ref-def(1,3):True::fred:: :/url1:::::]",
        "[olist(2,3):.:1:5:]",
        "[para(2,6):]",
        '[text(2,6):\a"\a&quot;\atitle\a"\a&quot;\a:]',
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<blockquote>
<ol>
<li>&quot;title&quot;</li>
</ol>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_extra_07ga() -> None:
    """
    Test case extra 01c:  variation of 1 split across list items
    """

    # Arrange
    source_markdown = """> [fred]: /url1
1. "title"
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n]",
        "[link-ref-def(1,3):True::fred:: :/url1:::::]",
        "[end-block-quote:::True]",
        "[olist(2,1):.:1:3::]",
        "[para(2,4):]",
        '[text(2,4):\a"\a&quot;\atitle\a"\a&quot;\a:]',
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<ol>
<li>&quot;title&quot;</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
