"""
https://github.github.com/gfm/#backslash-escapes
"""

from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_backslash_escapes_308():
    """
    Test case 308:  Any ASCII punctuation character may be backslash-escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """\\!\\\"\\#\\$\\%\\&\\'\\(\\)\\*\\+\\,\\-\\.\\/\\:\\;\\<\\=\\>\\?\\@\\[\\]\\^\\_\\`\\{\\|\\}\\~"""
    expected_tokens = [
        "[para:]",
        "[text:!&quot;#$%&amp;'()*+,-./:;&lt;=&gt;?@[]^_`{|}~:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_309():
    """
    Test case 309:  Backslashes before other characters are treated as literal backslashes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """\\→\\A\\a\\ \\3\\φ\\«"""
    expected_tokens = [
        "[para:]",
        "[text:\\→\\A\\a\\ \\3\\φ\\«:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_310():
    """
    Test case 310:  Escaped characters are treated as regular characters and do not have their usual Markdown meanings:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
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
        """[text:*not emphasized*
&lt;br/&gt; not a tag
[not a link](/foo)
`not code`
1. not a list
* not a list
# not a heading
[foo]: /url &quot;not a reference&quot;
&amp;ouml; not a character entity::\n\n\n\n\n\n\n\n]""",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO in flux with inlines
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_311():
    """
    Test case 311:  If a backslash is itself escaped, the following character is not:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """\\\\*emphasis*"""
    expected_tokens = [
        "[para:]",
        "[text:\\*emphasis*:]",
        "[end-para]",
    ]
    print(">>" + str(expected_tokens[1]))

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO will fail when emphasis added
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_312():
    """
    Test case 312:  A backslash at the end of the line is a hard line break:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo\\
bar"""
    expected_tokens =  ['[para:\n]', '[text:foo:]', '[hard-break]', '[text:\nbar:]', '[end-para]']

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_313():
    """
    Test case 313:  (part 1) Backslash escapes do not work in code blocks, code spans, autolinks, or raw HTML:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """`` \\[\\` ``"""
    expected_tokens = [
        "[para:]",
        "[icode-span:\\[\\`]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_314():
    """
    Test case 314:  (part 2) Backslash escapes do not work in code blocks, code spans, autolinks, or raw HTML:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    \\[\\]"""
    expected_tokens = [
        "[icode-block:    ]",
        "[text:\\[\\]:]",
        "[end-icode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_315():
    """
    Test case 315:  (part 3) Backslash escapes do not work in code blocks, code spans, autolinks, or raw HTML:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """~~~
\\[\\]
~~~"""
    expected_tokens = ["[fcode-block:~:3::::]", "[text:\\[\\]:]", "[end-fcode-block]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_316():
    """
    Test case 316:  (part 4) Backslash escapes do not work in code blocks, code spans, autolinks, or raw HTML:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<http://example.com?find=\\*>"""
    expected_tokens = [
        "[para:]",
        "[text:&lt;http://example.com?find=*&gt;:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO will fail when autolinks break added
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_317():
    """
    Test case 317:  (part 5) Backslash escapes do not work in code blocks, code spans, autolinks, or raw HTML:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """<a href="/bar\\/)">"""
    expected_tokens = [
        "[html-block]",
        '[text:<a href="/bar\\/)">:]',
        "[end-html-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_318():
    """
    Test case 318:  (part 1) But they work in all other contexts, including URLs and link titles, link references, and info strings in fenced code blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo](/bar\\* "ti\\*tle")"""
    expected_tokens = [
        "[para:]",
        "[text:[foo](/bar* &quot;ti*tle&quot;):]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO will fail when link definitions added
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_319():
    """
    Test case 319:  (part 2) But they work in all other contexts, including URLs and link titles, link references, and info strings in fenced code blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """[foo]

[foo]: /bar\\* "ti\\*tle"
"""
    expected_tokens = [
        "[para:]",
        "[text:[foo]:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:[foo]: /bar* &quot;ti*tle&quot;:]",
        "[end-para]",
        "[BLANK:]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO will fail when link definitions added
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_320():
    """
    Test case 320:  (part 3) But they work in all other contexts, including URLs and link titles, link references, and info strings in fenced code blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """``` foo\\+bar
foo
```"""
    expected_tokens = [
        "[fcode-block:`:3:foo+bar::: ]",
        "[text:foo:]",
        "[end-fcode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_320a():
    """
    Test case 320a:  (part 3) But they work in all other contexts, including URLs and link titles, link references, and info strings in fenced code blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """``` foo\\+\\bar
foo
```"""
    expected_tokens = [
        "[fcode-block:`:3:foo+\\bar::: ]",
        "[text:foo:]",
        "[end-fcode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_backslash_escapes_320b():
    """
    Test case 320b:  (part 3) But they work in all other contexts, including URLs and link titles, link references, and info strings in fenced code blocks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """``` foo\\+bar\\
foo
```"""
    expected_tokens = [
        "[fcode-block:`:3:foo+bar\\::: ]",
        "[text:foo:]",
        "[end-fcode-block]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
