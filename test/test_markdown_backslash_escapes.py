"""
https://github.github.com/gfm/#backslash-escapes
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


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
        "[para:]",
        "[text:!&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?@[\\]^_`{|}~:]",
        "[end-para]",
    ]
    expected_gfm = """<p>!&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?@[\\]^_`{|}~</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[text:\\→\\A\\a\\ \\3\\φ\\«:]",
        "[end-para]",
    ]
    expected_gfm = """<p>\\→\\A\\a\\ \\3\\φ\\«</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:\n\n\n\n\n\n\n\n]",
        "[text:*not emphasized:]",
        "[text:*:]",
        "[text:\n&lt;br/&gt; not a tag\n[not a link::\n\n]",
        "[text:]:]",
        """[text:(/foo)
`not code`
1. not a list
* not a list
# not a heading
[foo::\n\n\n\n\n]""",
        "[text:]:]",
        """[text:: /url &quot;not a reference&quot;
&amp;ouml; not a character entity::\n]""",
        "[end-para]",
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
        "[para:]",
        "[text:\\:]",
        "[emphasis:1]",
        "[text:emphasis:]",
        "[end-emphasis::1]",
        "[end-para]",
    ]
    expected_gfm = """<p>\\<em>emphasis</em></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:\n]",
        "[text:foo:]",
        "[hard-break]",
        "[text:\nbar:]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo<br />
bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[icode-span:\\[\\`]",
        "[end-para]",
    ]
    expected_gfm = """<p><code>\\[\\`</code></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[icode-block:    ]",
        "[text:\\[\\]:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>\\[\\]
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
    expected_tokens = ["[fcode-block:~:3::::]", "[text:\\[\\]:]", "[end-fcode-block]"]
    expected_gfm = """<pre><code>\\[\\]
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[uri-autolink:http://example.com?find=\\*]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="http://example.com?find=%5C*">http://example.com?find=\\*</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[html-block]",
        '[text:<a href="/bar\\/)">:]',
        "[end-html-block]",
    ]
    expected_gfm = """<a href="/bar\\/)">"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[link:/bar*:ti*tle]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
    ]
    expected_gfm = """<p><a href="/bar*" title="ti*tle">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[para:]",
        "[link:/bar*:ti*tle]",
        "[text:foo:]",
        "[end-link::]",
        "[end-para]",
        "[BLANK:]",
        "[BLANK:]",
    ]
    expected_gfm = """<p><a href="/bar*" title="ti*tle">foo</a></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[fcode-block:`:3:foo+bar::: ]",
        "[text:foo:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code class="language-foo+bar">foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[fcode-block:`:3:foo+\\bar::: ]",
        "[text:foo:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code class="language-foo+\\bar">foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


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
        "[fcode-block:`:3:foo+bar\\::: ]",
        "[text:foo:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code class="language-foo+bar\\">foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
