# pylint: disable=too-many-lines
"""
https://github.github.com/gfm/#link-reference-definitions
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    assert_if_lists_different,
    assert_if_strings_different,
    assert_token_consistency,
)


@pytest.mark.gfm
def test_link_reference_definitions_161():
    """
    Test case 161:  (part 1) A link reference definition does not correspond to a structural element of a document.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]: /url "title"

[foo]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::foo:: :/url:: :title:"title":]',
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link:shortcut:/url:title::::foo:::::]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/url" title="title">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_162():
    """
    Test case 162:  (part 2) A link reference definition does not correspond to a structural element of a document.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
        "[link:shortcut:/url:the title::::foo:::::]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/url" title="the title">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_163():
    """
    Test case 163:  (part 3) A link reference definition does not correspond to a structural element of a document.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[Foo*bar\\]]:my_(url) 'title (with parens)'

[Foo*bar\\]]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo*bar\\]:Foo*bar\\]::my_(url):: :title (with parens):'title (with parens)':]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link:shortcut:my_(url):title (with parens)::::Foo*bar\\]:::::]",
        "[text:Foo:]",
        "[text:*:]",
        "[text:bar\\\b]:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = (
        """<p><a href="my_(url)" title="title (with parens)">Foo*bar]</a></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_164():
    """
    Test case 164:  (part 4) A link reference definition does not correspond to a structural element of a document.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[Foo bar]:
<my url>
'title'

[Foo bar]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo bar:Foo bar:\n:my%20url:<my url>:\n:title:'title':]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[link:shortcut:my%20url:title::::Foo bar:::::]",
        "[text:Foo bar:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="my%20url" title="title">Foo bar</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_165():
    """
    Test case 165:  The title may extend over multiple lines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
        "[link:shortcut:/url:\ntitle\nline1\nline2\n::::foo:::::]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/url" title="
title
line1
line2
">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_166():
    """
    Test case 166:  However, it may not contain a blank line:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]: /url 'title

with blank line'

[foo]"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[text:: /url 'title:]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:with blank line':]",
        "[end-para]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[end-para]",
    ]
    expected_gfm = """<p>[foo]: /url 'title</p>
<p>with blank line'</p>
<p>[foo]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_167():
    """
    Test case 167:  The title may be omitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]:
/url

[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo::\n:/url:::::]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[link:shortcut:/url:::::foo:::::]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/url">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_168():
    """
    Test case 168:  The link destination may not be omitted:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]:

[foo]"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[text:::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[end-para]",
    ]
    expected_gfm = """<p>[foo]:</p>
<p>[foo]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_169():
    """
    Test case 169:  However, an empty link destination may be specified using angle brackets:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]: <>

[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: ::<>::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link:shortcut::::::foo:::::]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_170():
    """
    Test case 170:  The title must be separated from the link destination by whitespace:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]: <bar>(baz)

[foo]"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[text:: :]",
        "[raw-html:bar]",
        "[text:(baz):]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[end-para]",
    ]
    expected_gfm = """<p>[foo]: <bar>(baz)</p>
<p>[foo]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_171():
    """
    Test case 171:  Both title and destination can contain backslash escapes and literal backslashes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]: /url\\bar\\*baz "foo\\"bar\\baz"

[foo]"""
    expected_tokens = [
        '[link-ref-def(1,1):True::foo:: :/url%5Cbar*baz:/url\\bar\\*baz: :foo&quot;bar\\baz:"foo\\"bar\\baz":]',
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link:shortcut:/url%5Cbar*baz:foo&quot;bar\\baz::::foo:::::]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = (
        """<p><a href="/url%5Cbar*baz" title="foo&quot;bar\\baz">foo</a></p>"""
    )

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_172():
    """
    Test case 172:  A link can come before its corresponding definition:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]

[foo]: url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:shortcut:url:::::foo:::::]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :url:::::]",
    ]
    expected_gfm = """<p><a href="url">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_173():
    """
    Test case 173:  If there are several matching definitions, the first one takes precedence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]

[foo]: first
[foo]: second"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:shortcut:first:::::foo:::::]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[link-ref-def(3,1):True::foo:: :first:::::]",
        "[link-ref-def(4,1):False::foo:: :second:::::]",
    ]
    expected_gfm = """<p><a href="first">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_174():
    """
    Test case 174:  (part 1) As noted in the section on Links, matching of labels is case-insensitive (see matches).
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[FOO]: /url

[Foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:FOO: :/url:::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link:shortcut:/url:::::Foo:::::]",
        "[text:Foo:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/url">Foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_175():
    """
    Test case 175:  (part 2) As noted in the section on Links, matching of labels is case-insensitive (see matches).
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[ΑΓΩ]: /φου

[αγω]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::αγω:ΑΓΩ: :/%CF%86%CE%BF%CF%85:/φου::::]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[link:shortcut:/%CF%86%CE%BF%CF%85:::::αγω:::::]",
        "[text:αγω:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/%CF%86%CE%BF%CF%85">αγω</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_176():
    """
    Test case 176:  Here is a link reference definition with no corresponding link. It contributes nothing to the document.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]: /url"""
    expected_tokens = ["[link-ref-def(1,1):True::foo:: :/url:::::]"]
    expected_gfm = """"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_177():
    """
    Test case 177:  Here is another one:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[
foo
]: /url
bar"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:\nfoo\n: :/url:::::]",
        "[para(4,1):]",
        "[text:bar:]",
        "[end-para]",
    ]
    expected_gfm = """<p>bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_178():
    """
    Test case 178:  This is not a link reference definition, because there are non-whitespace characters after the title:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]: /url "title" ok"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        '[text:: /url \a"\a&quot;\atitle\a"\a&quot;\a ok:]',
        "[end-para]",
    ]
    expected_gfm = """<p>[foo]: /url &quot;title&quot; ok</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_179():
    """
    Test case 179:  This is a link reference definition, but it has no title:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]: /url
"title" ok"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[para(2,1):]",
        '[text:\a"\a&quot;\atitle\a"\a&quot;\a ok:]',
        "[end-para]",
    ]
    expected_gfm = """<p>&quot;title&quot; ok</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_180():
    """
    Test case 180:  This is not a link reference definition, because it is indented four spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    [foo]: /url "title"

[foo]"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        '[text:[foo]: /url \a"\a&quot;\atitle\a"\a&quot;\a:]',
        "[end-icode-block]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[end-para]",
    ]
    expected_gfm = """<pre><code>[foo]: /url &quot;title&quot;
</code></pre>
<p>[foo]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_181():
    """
    Test case 181:  This is not a link reference definition, because it occurs inside a code block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """```
[foo]: /url
```

[foo]"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text:[foo]: /url:]",
        "[end-fcode-block::3]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[end-para]",
    ]
    expected_gfm = """<pre><code>[foo]: /url
</code></pre>
<p>[foo]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_182():
    """
    Test case 182:  A link reference definition cannot interrupt a paragraph.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo
[bar]: /baz

[bar]"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text:Foo\n::\n]",
        "[text:[:]",
        "[text:bar:]",
        "[text:]:]",
        "[text:: /baz:]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text:[:]",
        "[text:bar:]",
        "[text:]:]",
        "[end-para]",
    ]
    expected_gfm = """<p>Foo
[bar]: /baz</p>
<p>[bar]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_183():
    """
    Test case 183:  (part 1) However, it can directly follow other block elements, such as headings and thematic breaks, and it need not be followed by a blank line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """# [Foo]
[foo]: /url
> bar"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text:\a \a\x03\a:]",
        "[link:shortcut:/url:::::Foo:::::]",
        "[text:Foo: ]",
        "[end-link::]",
        "[end-atx::]",
        "[link-ref-def(2,1):True::foo:: :/url:::::]",
        "[block-quote(3,1)::> ]",
        "[para(3,3):]",
        "[text:bar:]",
        "[end-para]",
        "[end-block-quote]",
    ]
    expected_gfm = """<h1><a href="/url">Foo</a></h1>
<blockquote>
<p>bar</p>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_184():
    """
    Test case 184:  (part 2) However, it can directly follow other block elements, such as headings and thematic breaks, and it need not be followed by a blank line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]: /url
bar
===
[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[setext(3,1):=:3::(2,1)]",
        "[text:bar:]",
        "[end-setext::]",
        "[para(4,1):]",
        "[link:shortcut:/url:::::foo:::::]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<h1>bar</h1>
<p><a href="/url">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_185():
    """
    Test case 185:  (part 3) However, it can directly follow other block elements, such as headings and thematic breaks, and it need not be followed by a blank line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]: /url
===
[foo]"""
    expected_tokens = [
        "[link-ref-def(1,1):True::foo:: :/url:::::]",
        "[para(2,1):\n]",
        "[text:===\n::\n]",
        "[link:shortcut:/url:::::foo:::::]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p>===
<a href="/url">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_186():
    """
    Test case 186:  Several link reference definitions can occur one after another, without intervening blank lines.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
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
        "[link:shortcut:/foo-url:foo::::foo:::::]",
        "[text:foo:]",
        "[end-link::]",
        "[text:,\n::\n]",
        "[link:shortcut:/bar-url:bar::::bar:::::]",
        "[text:bar:]",
        "[end-link::]",
        "[text:,\n::\n]",
        "[link:shortcut:/baz-url:::::baz:::::]",
        "[text:baz:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/foo-url" title="foo">foo</a>,
<a href="/bar-url" title="bar">bar</a>,
<a href="/baz-url">baz</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_187():
    """
    Test case 187:  Link reference definitions can occur inside block containers, like lists and block quotations. They affect the entire document, not just the container in which they are defined:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]

> [foo]: /url"""
    expected_tokens = [
        "[para(1,1):]",
        "[link:shortcut:/url:::::foo:::::]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK(2,1):]",
        "[block-quote(3,1)::> ]",
        "[link-ref-def(3,3):True::foo:: :/url:::::]",
        "[end-block-quote]",
    ]
    expected_gfm = """<p><a href="/url">foo</a></p>
<blockquote>
</blockquote>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188():
    """
    Test case 188:  Whether something is a link reference definition is independent of whether the link reference it defines is used in the document.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]: /url"""
    expected_tokens = ["[link-ref-def(1,1):True::foo:: :/url:::::]"]
    expected_gfm = """"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188a():
    """
    Test case 188a:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """["""
    expected_tokens = ["[para(1,1):]", "[text:[:]", "[end-para]"]
    expected_gfm = """<p>[</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188b():
    """
    Test case 188b:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo"""
    expected_tokens = ["[para(1,1):]", "[text:[:]", "[text:foo:]", "[end-para]"]
    expected_gfm = """<p>[foo</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188c():
    """
    Test case 188c:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[end-para]",
    ]
    expected_gfm = """<p>[foo]</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188d():
    """
    Test case 188d:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]:"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[text:::]",
        "[end-para]",
    ]
    expected_gfm = """<p>[foo]:</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_link_reference_definitions_188e():
    """
    Test case 188e:  variation
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]: /url ("""
    expected_tokens = [
        "[para(1,1):]",
        "[text:[:]",
        "[text:foo:]",
        "[text:]:]",
        "[text:: /url (:]",
        "[end-para]",
    ]
    expected_gfm = """<p>[foo]: /url (</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
