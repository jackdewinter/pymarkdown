"""
https://github.github.com/gfm/#backslash-escapes
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
def test_backslash_escapes_308():
    """
    Test case 308:  Any ASCII punctuation character may be backslash-escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\!\\\"\\#\\$\\%\\&\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\\\\\]\\^\\_\\`\\{\\|\\}\\~"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b!\\\b\a\"\a&quot;\a\\\b#\\\b$\\\b%\\\b\a&\a&amp;\a\\\b'\\\b(\\\b)\\\b*\\\b+\\\b,\\\b-\\\b.\\\b/\\\b:\\\b;\\\b\a<\a&lt;\a\\\b=\\\b\a>\a&gt;\a\\\b?\\\b@\\\b[\\\b\\\\\b]\\\b^\\\b_\\\b`\\\b{\\\b|\\\b}\\\b~:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>!&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?@[\\]^_`{|}~</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_309():
    """
    Test case 309:  Backslashes before other characters are treated as literal backslashes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\→\\A\\a\\ \\3\\φ\\«"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\→\\A\\a\\ \\3\\φ\\«:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\\→\\A\\a\\ \\3\\φ\\«</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_310():
    """
    Test case 310:  Escaped characters are treated as regular characters and do not have their usual Markdown meanings:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\*not emphasized*
\\<br/> not a tag
\\[not a link](/foo)
\\`not code`
1\\. not a list
\\* not a list
\\# not a heading
\\[foo]: /url "not a reference"
\\&ouml; not a character entity"""
    expected_tokens = [
        "[para(1,1):\n\n\n\n\n\n\n\n]",
        "[text(1,1):\\\b*not emphasized:]",
        "[text(1,17):*:]",
        "[text(1,18):\n\\\b\a<\a&lt;\abr/\a>\a&gt;\a not a tag\n\\\b[not a link::\n\n]",
        "[text(3,13):]:]",
        """[text(3,14):(/foo)
\\\b`not code`
1\\\b. not a list
\\\b* not a list
\\\b# not a heading
\\\b[foo::\n\n\n\n\n]""",
        "[text(8,6):]:]",
        """[text(8,7):: /url \a\"\a&quot;\anot a reference\a\"\a&quot;\a
\\\b\a&\a&amp;\aouml; not a character entity::\n]""",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>*not emphasized*
&lt;br/&gt; not a tag
[not a link](/foo)
`not code`
1. not a list
* not a list
# not a heading
[foo]: /url &quot;not a reference&quot;
&amp;ouml; not a character entity</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_311():
    """
    Test case 311:  If a backslash is itself escaped, the following character is not:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\\\*emphasis*"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\\\b\\:]",
        "[emphasis(1,3):1:*]",
        "[text(1,4):emphasis:]",
        "[end-emphasis(1,12)::1:*:False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\\<em>emphasis</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_312():
    """
    Test case 312:  A backslash at the end of the line is a hard line break:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo\\
bar"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):foo:]",
        "[hard-break(1,4):\\]",
        "[text(2,1):\nbar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo<br />
bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_313():
    """
    Test case 313:  (part 1) Backslash escapes do not work in code blocks, code spans, autolinks, or raw HTML:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """`` \\[\\` ``"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):\\[\\`:``: : ]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>\\[\\`</code></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_314():
    """
    Test case 314:  (part 2) Backslash escapes do not work in code blocks, code spans, autolinks, or raw HTML:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    \\[\\]"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):\\[\\]:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>\\[\\]
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_315():
    """
    Test case 315:  (part 3) Backslash escapes do not work in code blocks, code spans, autolinks, or raw HTML:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """~~~
\\[\\]
~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:3::::::]",
        "[text(2,1):\\[\\]:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code>\\[\\]
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_316():
    """
    Test case 316:  (part 4) Backslash escapes do not work in code blocks, code spans, autolinks, or raw HTML:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<http://example.com?find=\\*>"""
    expected_tokens = [
        "[para(1,1):]",
        "[uri-autolink(1,1):http://example.com?find=\\*]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="http://example.com?find=%5C*">http://example.com?find=\\*</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_317():
    """
    Test case 317:  (part 5) Backslash escapes do not work in code blocks, code spans, autolinks, or raw HTML:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """<a href="/bar\\/)">"""
    expected_tokens = [
        "[html-block(1,1)]",
        '[text(1,1):<a href="/bar\\/)">:]',
        "[end-html-block:::True]",
    ]
    expected_gfm = """<a href="/bar\\/)">"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_318():
    """
    Test case 318:  (part 1) But they work in all other contexts, including URLs and link titles, link references, and info strings in fenced code blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo](/bar\\* "ti\\*tle")"""
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/bar*:ti*tle:/bar\\*:ti\\*tle::foo:False:":: :]',
        "[text(1,2):foo:]",
        "[end-link:::False]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/bar*" title="ti*tle">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_319():
    """
    Test case 319:  (part 2) But they work in all other contexts, including URLs and link titles, link references, and info strings in fenced code blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """[foo]

[foo]: /bar\\* "ti\\*tle"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[link(1,1):shortcut:/bar*:ti*tle::::foo:::::]",
        "[text(1,2):foo:]",
        "[end-link:::False]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::foo:: :/bar*:/bar\\*: :ti*tle:"ti\\*tle":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p><a href="/bar*" title="ti*tle">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_320():
    """
    Test case 320:  (part 3) But they work in all other contexts, including URLs and link titles, link references, and info strings in fenced code blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """``` foo\\+bar
foo
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:foo+bar:foo\\+bar:::: ]",
        "[text(2,1):foo:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code class="language-foo+bar">foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_320a():
    """
    Test case 320a:  (part 3) But they work in all other contexts, including URLs and link titles, link references, and info strings in fenced code blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """``` foo\\+\\bar
foo
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:foo+\\bar:foo\\+\\bar:::: ]",
        "[text(2,1):foo:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code class="language-foo+\\bar">foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_320b():
    """
    Test case 320b:  (part 3) But they work in all other contexts, including URLs and link titles, link references, and info strings in fenced code blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """``` foo\\+bar\\
foo
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:foo+bar\\:foo\\+bar\\:::: ]",
        "[text(2,1):foo:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code class="language-foo+bar\\">foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_backslash_escapes_320c():
    """
    Test case 320c:  (part 3) But they work in all other contexts, including URLs and link titles, link references, and info strings in fenced code blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """``` foo \\+bar\\
foo
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:foo:: +bar\\: \\+bar\\:: ]",
        "[text(2,1):foo:]",
        "[end-fcode-block::3:False]",
    ]
    expected_gfm = """<pre><code class="language-foo">foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
