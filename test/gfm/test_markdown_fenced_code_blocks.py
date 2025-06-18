"""
https://github.github.com/gfm/#fenced-code-blocks
"""

from test.utils import act_and_assert

import pytest


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_fenced_code_blocks_089() -> None:
    """
    Test case 089:  Simple example with backticks
    """

    # Arrange
    source_markdown = """```
<
 >
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\a<\a&lt;\a\n \a>\a&gt;\a:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>&lt;
 &gt;
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_090() -> None:
    """
    Test case 090:  Simple example with tildes
    """

    # Arrange
    source_markdown = """~~~
<
 >
~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:3::::::]",
        "[text(2,1):\a<\a&lt;\a\n \a>\a&gt;\a:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>&lt;
 &gt;
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_091() -> None:
    """
    Test case 091:  Fewer than three backticks is not enough:
    """

    # Arrange
    source_markdown = """``
foo
``"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[icode-span(1,1):foo:``:\a\n\a \a:\a\n\a \a]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>foo</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_092() -> None:
    """
    Test case 092:  (part a) The closing code fence must use the same character as the opening fence:
    """

    # Arrange
    source_markdown = """```
aaa
~~~
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):aaa\n~~~:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>aaa
~~~
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_093() -> None:
    """
    Test case 093:  (part b) The closing code fence must use the same character as the opening fence:
    """

    # Arrange
    source_markdown = """~~~
aaa
```
~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:3::::::]",
        "[text(2,1):aaa\n```:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>aaa
```
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_094() -> None:
    """
    Test case 094:  (part a) The closing code fence must be at least as long as the opening fence:
    """

    # Arrange
    source_markdown = """````
aaa
```
``````"""
    expected_tokens = [
        "[fcode-block(1,1):`:4::::::]",
        "[text(2,1):aaa\n```:]",
        "[end-fcode-block:::6:False]",
    ]
    expected_gfm = """<pre><code>aaa
```
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_095() -> None:
    """
    Test case 095:  (part b) The closing code fence must be at least as long as the opening fence:
    """

    # Arrange
    source_markdown = """~~~~
aaa
~~~
~~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:4::::::]",
        "[text(2,1):aaa\n~~~:]",
        "[end-fcode-block:::4:False]",
    ]
    expected_gfm = """<pre><code>aaa
~~~
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096() -> None:
    """
    Test case 096:  (part a) Unclosed code blocks are closed by the end of the
                    document (or the enclosing block quote or list item):
    """

    # Arrange
    source_markdown = """```"""
    expected_tokens = ["[fcode-block(1,1):`:3::::::]", "[end-fcode-block::::True]"]
    expected_gfm = """<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096a() -> None:
    """
    Test case 096a:  variation of 96 with a trailing blank line
    """

    # Arrange
    source_markdown = """```
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096b() -> None:
    """
    Test case 096b:  variation of 96 with a pair of trailing blank lines
    """

    # Arrange
    source_markdown = """```

"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code>\n</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096c() -> None:
    """
    Test case 096c:  variation of 96 with a trio of trailing blank lines
    """

    # Arrange
    source_markdown = """```


"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03\n\x03:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code>

</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096d() -> None:
    """
    Test case 096c:  variation of 96 with a trio of trailing blank lines
        that have varying levels of space
    """

    # Arrange
    source_markdown = """```
/a
/a/a
""".replace(
        "/a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,2):\n\x03  \n\x03: ]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code>\a
\a\a
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096e() -> None:
    """
    Test case 096e:  variation of 96 with a simple line followed by
        a blank line with spaces
    """

    # Arrange
    source_markdown = """```
abc
/a/a
""".replace(
        "/a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):abc\n\x03  \n\x03:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code>abc
  
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096f() -> None:
    """
    Test case 096f:  variation of 96 with a simple line followed by
        a blank line
    """

    # Arrange
    source_markdown = """```
abc

"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):abc\n\x03\n\x03:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code>abc

</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_097() -> None:
    """
    Test case 097:  (part b) Unclosed code blocks are closed by the end of the
                    document (or the enclosing block quote or list item):
    """

    # Arrange
    source_markdown = """`````

```
aaa"""
    expected_tokens = [
        "[fcode-block(1,1):`:5::::::]",
        "[text(2,1):\n```\naaa:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code>
```
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_098x() -> None:
    """
    Test case 098:  (part c) Unclosed code blocks are closed by the end of the
                    document (or the enclosing block quote or list item):
    """

    # Arrange
    source_markdown = """> ```
> aaa

bbb"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,3):aaa:]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):bbb:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>aaa
</code></pre>
</blockquote>
<p>bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_098a() -> None:
    """
    Test case 098a:  variation of 98 with no space between the block quote
        and the text on the second line
    """

    # Arrange
    source_markdown = """> ```
>aaa

bbb"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,2):aaa:]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):bbb:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>aaa
</code></pre>
</blockquote>
<p>bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_098b() -> None:
    """
    Test case 098b:  variation of 98 with extra block quote on the second line
    """

    # Arrange
    source_markdown = """> ```
>> aaa

bbb"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,2):\a>\a&gt;\a aaa:]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):bbb:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt; aaa
</code></pre>
</blockquote>
<p>bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_098c() -> None:
    """
    Test case 098c:  variation of 98 with no block quote on the second line
    """

    # Arrange
    source_markdown = """> ```
aaa

bbb"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
        "[para(2,1):]",
        "[text(2,1):aaa:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):bbb:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code></code></pre>
</blockquote>
<p>aaa</p>
<p>bbb</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099x() -> None:
    """
    Test case 099:  A code block can have all empty lines as its content:
    """

    # Arrange
    source_markdown = """```

\a\a
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03  :]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>
\a\a
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099a() -> None:
    """
    Test case 099a:  variation of 99 with extra blank line within
    """

    # Arrange
    source_markdown = """```

\a\a

```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03  \n\x03:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>
\a\a

</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099b() -> None:
    """
    Test case 099b:  variation of 99 with extra blank lines with various spaces within
    """

    # Arrange
    source_markdown = """```

\a
\a\a
\a

```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03 \n\x03  \n\x03 \n\x03:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>
\a
\a\a
\a

</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099c() -> None:
    """
    Test case 099c:  variation of 99 with prefix and suffix text lines
    """

    # Arrange
    source_markdown = """```
z
\a
\a\a
\a
z
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):z\n\x03 \n\x03  \n\x03 \nz:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>z
\a
\a\a
\a
z
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099d() -> None:
    """
    Test case 099d:  variation of 99 with prefix and suffix text lines
        and only a single blank line with spaces
    """

    # Arrange
    source_markdown = """```
z
\a
z
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):z\n\x03 \nz:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>z
\a
z
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099e() -> None:
    """
    Test case 099e:  variation of 99 with blank lines with spaces
    """

    # Arrange
    source_markdown = """```
\a
\a\a
\a
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,2):\n\x03  \n\x03 : ]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>\a
\a\a
\a
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099f() -> None:
    """
    Test case 099e:  variation of 99 with blank lines with spaces
        and the middle line with text
    """

    # Arrange
    source_markdown = """```

\a
\a\aabc
\a

```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03 \n  abc\n\x03 \n\x03:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>
\a
\a\aabc
\a

</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099g() -> None:
    """
    Test case 099g:  variation of 99, more combinations
    """

    # Arrange
    source_markdown = """```
z

\a
\a\a
\a

z
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):z\n\x03\n\x03 \n\x03  \n\x03 \n\x03\nz:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>z

\a
\a\a
\a

z
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099h() -> None:
    """
    Test case 099h:  variation of 99, more combinations
    """

    # Arrange
    source_markdown = """`````

```
aaa
`````"""
    expected_tokens = [
        "[fcode-block(1,1):`:5::::::]",
        "[text(2,1):\n```\naaa:]",
        "[end-fcode-block:::5:False]",
    ]
    expected_gfm = """<pre><code>
```
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099i() -> None:
    """
    Test case 099i:  variation of 99, more combinations
    """

    # Arrange
    source_markdown = """`````


```
aaa
`````"""
    expected_tokens = [
        "[fcode-block(1,1):`:5::::::]",
        "[text(2,1):\n\x03\n```\naaa:]",
        "[end-fcode-block:::5:False]",
    ]
    expected_gfm = """<pre><code>

```
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099j() -> None:
    """
    Test case 099j:  variation of 99, more combinations
    """

    # Arrange
    source_markdown = """`````


bbb

ccc

```
aaa
`````"""
    expected_tokens = [
        "[fcode-block(1,1):`:5::::::]",
        "[text(2,1):\n\x03\nbbb\n\x03\nccc\n\x03\n```\naaa:]",
        "[end-fcode-block:::5:False]",
    ]
    expected_gfm = """<pre><code>

bbb

ccc

```
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099ja() -> None:
    """
    Test case 099ja:  variation of 99, more combinations
    """

    # Arrange
    source_markdown = """`````


bbb

ccc

```
aaa
`````
"""
    expected_tokens = [
        "[fcode-block(1,1):`:5::::::]",
        "[text(2,1):\n\x03\nbbb\n\x03\nccc\n\x03\n```\naaa:]",
        "[end-fcode-block:::5:False]",
        "[BLANK(11,1):]",
    ]
    expected_gfm = """<pre><code>

bbb

ccc

```
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099k() -> None:
    """
    Test case 099k:  variation of 99, more combinations
    """

    # Arrange
    source_markdown = """```



\a
\a\aabc
\a



```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\n\x03\n\x03\n\x03 \n  abc\n\x03 \n\x03\n\x03\n\x03:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>


\a
\a\aabc
\a



</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099l() -> None:
    """
    Test case 099l:  variation of 99, more combinations
    """

    # Arrange
    source_markdown = """```
z



\a
\a\a
\a



z
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):z\n\x03\n\x03\n\x03\n\x03 \n\x03  \n\x03 \n\x03\n\x03\n\x03\nz:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>z



\a
\a\a
\a



z
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_100() -> None:
    """
    Test case 100:  A code block can be empty:
    """

    # Arrange
    source_markdown = """```
```"""
    expected_tokens = ["[fcode-block(1,1):`:3::::::]", "[end-fcode-block:::3:False]"]
    expected_gfm = """<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_101() -> None:
    """
    Test case 101:  (part a)  Fences can be indented. If the opening fence is indented,
                    content lines will have equivalent opening indentation removed,
                    if present:
    """

    # Arrange
    source_markdown = """ ```
 aaa
aaa
```"""
    expected_tokens = [
        "[fcode-block(1,2):`:3::::: :]",
        "[text(2,2):aaa\naaa:\a \a\x03\a]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>aaa
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_102() -> None:
    """
    Test case 102:  (part b)  Fences can be indented. If the opening fence is
                    indented, content lines will have equivalent opening indentation
                    removed, if present:
    """

    # Arrange
    source_markdown = """  ```
aaa
  aaa
aaa
  ```"""
    expected_tokens = [
        "[fcode-block(1,3):`:3:::::  :]",
        "[text(2,1):aaa\n\a  \a\x03\aaaa\naaa:]",
        "[end-fcode-block:  ::3:False]",
    ]
    expected_gfm = """<pre><code>aaa
aaa
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_103() -> None:
    """
    Test case 103:  (part c)  Fences can be indented. If the opening fence is indented,
                    content lines will have equivalent opening indentation removed,
                    if present:
    """

    # Arrange
    source_markdown = """   ```
   aaa
    aaa
  aaa
   ```"""
    expected_tokens = [
        "[fcode-block(1,4):`:3:::::   :]",
        "[text(2,4):aaa\n\a   \a\x03\a aaa\n\a  \a\x03\aaaa:\a   \a\x03\a]",
        "[end-fcode-block:   ::3:False]",
    ]
    expected_gfm = """<pre><code>aaa
 aaa
aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_104() -> None:
    """
    Test case 104:  Four spaces indentation produces an indented code block:
    """

    # Arrange
    source_markdown = """    ```
    aaa
    ```"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    \n    ]",
        "[text(1,5):```\naaa\n```:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>```
aaa
```
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_105() -> None:
    """
    Test case 105:  (part a) Closing fences may be indented by 0-3 spaces, and
                    their indentation need not match that of the opening fence:
    """

    # Arrange
    source_markdown = """```
aaa
  ```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):aaa:]",
        "[end-fcode-block:  ::3:False]",
    ]
    expected_gfm = """<pre><code>aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_106() -> None:
    """
    Test case 106:  (part b) Closing fences may be indented by 0-3 spaces, and
                    their indentation need not match that of the opening fence:
    """

    # Arrange
    source_markdown = """   ```
aaa
  ```"""
    expected_tokens = [
        "[fcode-block(1,4):`:3:::::   :]",
        "[text(2,1):aaa:]",
        "[end-fcode-block:  ::3:False]",
    ]
    expected_gfm = """<pre><code>aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_107() -> None:
    """
    Test case 107:  This is not a closing fence, because it is indented 4 spaces:
    """

    # Arrange
    source_markdown = """```
aaa
    ```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):aaa\n    ```:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code>aaa
    ```
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_108() -> None:
    """
    Test case 108:  (part a) Code fences (opening and closing) cannot contain internal spaces:
    """

    # Arrange
    source_markdown = """``` ```
aaa"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[icode-span(1,1): :```::]",
        """[text(1,8):
aaa::\n]""",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code> </code>
aaa</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_109() -> None:
    """
    Test case 109:  (part b) Code fences (opening and closing) cannot contain internal spaces:
    """

    # Arrange
    source_markdown = """~~~~~~
aaa
~~~ ~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:6::::::]",
        "[text(2,1):aaa\n~~~ ~~:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code>aaa
~~~ ~~
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_110() -> None:
    """
    Test case 110:  Fenced code blocks can interrupt paragraphs, and can be followed
                    directly by paragraphs, without a blank line between:
    """

    # Arrange
    source_markdown = """foo
```
bar
```
baz"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(2,1):`:3::::::]",
        "[text(3,1):bar:]",
        "[end-fcode-block:::3:False]",
        "[para(5,1):]",
        "[text(5,1):baz:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo</p>
<pre><code>bar
</code></pre>
<p>baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_111() -> None:
    """
    Test case 111:  Other blocks can also occur before and after fenced code blocks without an intervening blank line:
    """

    # Arrange
    source_markdown = """foo
---
~~~
bar
~~~
# baz"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):foo:]",
        "[end-setext::]",
        "[fcode-block(3,1):~:3::::::]",
        "[text(4,1):bar:]",
        "[end-fcode-block:::3:False]",
        "[atx(6,1):1:0:]",
        "[text(6,3):baz: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>foo</h2>
<pre><code>bar
</code></pre>
<h1>baz</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_112() -> None:
    """
    Test case 112:  (part a) An info string can be provided after the opening code fence.
    """

    # Arrange
    source_markdown = """```ruby
def foo(x)
  return 3
end
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:ruby:::::]",
        "[text(2,1):def foo(x)\n  return 3\nend:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code class="language-ruby">def foo(x)
  return 3
end
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_113() -> None:
    """
    Test case 113:  (part b) An info string can be provided after the opening code fence.
    """

    # Arrange
    source_markdown = """~~~~    ruby startline=3 $%@#$
def foo(x)
  return 3
end
~~~~~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:4:ruby:: startline=3 $%@#$:::    ]",
        "[text(2,1):def foo(x)\n  return 3\nend:]",
        "[end-fcode-block:::7:False]",
    ]
    expected_gfm = """<pre><code class="language-ruby">def foo(x)
  return 3
end
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_114() -> None:
    """
    Test case 114:  (part c) An info string can be provided after the opening code fence.
    """

    # Arrange
    source_markdown = """````;
````"""
    expected_tokens = ["[fcode-block(1,1):`:4:;:::::]", "[end-fcode-block:::4:False]"]
    expected_gfm = """<pre><code class="language-;"></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_115() -> None:
    """
    Test case 115:  Info strings for backtick code blocks cannot contain backticks:
    """

    # Arrange
    source_markdown = """``` aa ```
foo"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[icode-span(1,1):aa:```: : ]",
        """[text(1,11):
foo::\n]""",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>aa</code>
foo</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_116() -> None:
    """
    Test case 116:  Info strings for tilde code blocks can contain backticks and tildes:
    """

    # Arrange
    source_markdown = """~~~ aa ``` ~~~
foo
~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:3:aa:: ``` ~~~::: ]",
        "[text(2,1):foo:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code class="language-aa">foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_117() -> None:
    """
    Test case 117:  Closing code fences cannot have info strings:
    """

    # Arrange
    source_markdown = """```
``` aaa
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):``` aaa:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>``` aaa
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_01x() -> None:
    """
    Test case extra 01:  start a "list block" within a fenced code block
    """

    # Arrange
    source_markdown = """```
- some text
some other text
```
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):- some text\nsome other text:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<pre><code>- some text
some other text
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_01a() -> None:
    """
    Test case extra 01:  "start" a "link reference defintion" within a fenced code block
    """

    # Arrange
    source_markdown = """```
- [foo]:
/url
```
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):- [foo]:\n/url:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<pre><code>- [foo]:
/url
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_02x() -> None:
    """
    Test case extra 02:  start a fenced code block in a list item,
         starting a new list item without closing the block
    """

    # Arrange
    source_markdown = """- ```
- some text
some other text
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[fcode-block(1,3):`:3::::::]",
        "[end-fcode-block::::True]",
        "[li(2,1):2::]",
        "[para(2,3):\n]",
        "[text(2,3):some text\nsome other text::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,1):`:3::::::]",
        "[text(5,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code></code></pre>
</li>
<li>some text
some other text</li>
</ul>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_02a() -> None:
    """
    Test case extra 02:  variation of 2 with LRD instead of text in second list item

    NOTE: Due to https://talk.commonmark.org/t/block-quotes-laziness-and-link-reference-definitions/3751
          the GFM output has been adjusted to compensate for PyMarkdown using a token and not parsing
          the text afterwards.
    """
    # Arrange
    source_markdown = """- ```
- [foo]:
/url
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[fcode-block(1,3):`:3::::::]",
        "[end-fcode-block::::True]",
        "[li(2,1):2::]",
        "[para(2,3):\n]",
        "[text(2,3):[foo]:\n/url::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[fcode-block(4,1):`:3::::::]",
        "[text(5,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code></code></pre>
</li>
<li>[foo]:
/url</li>
</ul>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_03x() -> None:
    """
    Test case extra 03:  variation of 1 where list already opened but no new list item

    NOTE: Small change to output to remove newline at pre/code at end.
    """

    # Arrange
    source_markdown = """- ```
  some text
some other text
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,3):some text:]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
        "[para(3,1):]",
        "[text(3,1):some other text:]",
        "[end-para:::False]",
        "[fcode-block(4,1):`:3::::::]",
        "[text(5,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>some text
</code></pre>
</li>
</ul>
<p>some other text</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_03a() -> None:
    """
    Test case extra 03:  variation of 3 with LRD instead of text in second list item
    """

    # Arrange
    source_markdown = """- ```
  [foo]:
/url
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,3):[foo]::]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
        "[para(3,1):]",
        "[text(3,1):/url:]",
        "[end-para:::False]",
        "[fcode-block(4,1):`:3::::::]",
        "[text(5,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>[foo]:
</code></pre>
</li>
</ul>
<p>/url</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_04x() -> None:
    """
    Test case extra 04:  start a "block quote" within a fenced code block
    """

    # Arrange
    source_markdown = """```
> some text
some other text
```
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\a>\a&gt;\a some text\nsome other text:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<pre><code>&gt; some text
some other text
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_04a() -> None:
    """
    Test case extra 04:  variation of 4 with LRD instead of text in second line
    """

    # Arrange
    source_markdown = """```
> [foo]:
/url
```
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\a>\a&gt;\a [foo]:\n/url:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<pre><code>&gt; [foo]:
/url
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_05x() -> None:
    """
    Test case extra 05:  variation of 4 where block quote already opened
    """

    # Arrange
    source_markdown = """> ```
> some text
some other text
```
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,3):some text:]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
        "[para(3,1):]",
        "[text(3,1):some other text:]",
        "[end-para:::False]",
        "[fcode-block(4,1):`:3::::::]",
        "[text(5,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>some text
</code></pre>
</blockquote>
<p>some other text</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_05a() -> None:
    """
    Test case extra 05:  variation of 5 with LRD instead of text in second line

    NOTE: Small change to output to remove newline at pre/code at end.
    """

    # Arrange
    source_markdown = """> ```
> [foo]:
/url
```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[text(2,3):[foo]::]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
        "[para(3,1):]",
        "[text(3,1):/url:]",
        "[end-para:::False]",
        "[fcode-block(4,1):`:3::::::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code>[foo]:
</code></pre>
</blockquote>
<p>/url</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_06x() -> None:
    """
    Test case extra 06:  variation of 4 where block already opened but
                         no block quote line start character
    """

    # Arrange
    source_markdown = """> ```
  some text
some other text
```
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
        "[para(2,3):  \n]",
        "[text(2,3):some text\nsome other text::\n]",
        "[end-para:::False]",
        "[fcode-block(4,1):`:3::::::]",
        "[text(5,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code></code></pre>
</blockquote>
<p>some text
some other text</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_06a() -> None:
    """
    Test case extra 06a:  variation of 6 with LRD instead of text in second line
    """

    # Arrange
    source_markdown = """> ```
  [foo]:
/url
```"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[fcode-block(1,3):`:3::::::]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
        "[link-ref-def(2,3):True:  :foo::\n:/url:::::]",
        "[fcode-block(4,1):`:3::::::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code></code></pre>
</blockquote>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_07() -> None:
    """
    Test case extra 07:  mixed "block quotes" and "list blocks"
    """

    # Arrange
    source_markdown = """```
* a
  > b
  >
* c
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):* a\n  \a>\a&gt;\a b\n  \a>\a&gt;\a\n* c:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>* a
  &gt; b
  &gt;
* c
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_08x() -> None:
    """
    Test case extra 08:  capturing text and newlines alike
    """

    # Arrange
    source_markdown = """```
abc

def
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):abc\n\x03\ndef:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>abc

def
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_08a() -> None:
    """
    Test case extra 08:  variation of 8 with extra newlines
    """

    # Arrange
    source_markdown = """```

abc

def
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):\nabc\n\x03\ndef:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>
abc

def
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_08b() -> None:
    """
    Test case extra 08:  variation of 8 with close fence and extra tex
    """

    # Arrange
    source_markdown = """```
abc
```

abc

def
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,1):abc:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(4,1):]",
        "[para(5,1):]",
        "[text(5,1):abc:]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[para(7,1):]",
        "[text(7,1):def:]",
        "[end-para:::False]",
        "[fcode-block(8,1):`:3::::::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code>abc
</code></pre>
<p>abc</p>
<p>def</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_08c() -> None:
    """
    Test case extra 08:  variation of 8b with trailing spaces
    """

    # Arrange
    source_markdown = """```
\a\a
abc

def
```""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text(2,3):\nabc\n\x03\ndef:  ]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code>\a\a
abc

def
</code></pre>""".replace(
        "\a", " "
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_09x() -> None:
    """
    Test case extra 09
    """

    # Arrange
    source_markdown = """1. abc
   ```yaml
   def:
      - ghi
   ```"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,4):`:3:yaml:::::]",
        "[text(3,4):def:\n   - ghi:]",
        "[end-fcode-block:::3:False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<pre><code class="language-yaml">def:
   - ghi
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_09a() -> None:
    """
    Test case extra 09
    """

    # Arrange
    source_markdown = """- abc
  ```yaml
  def:
     - ghi
  ```"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,3):`:3:yaml:::::]",
        "[text(3,3):def:\n   - ghi:]",
        "[end-fcode-block:::3:False]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<pre><code class="language-yaml">def:
   - ghi
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_09b() -> None:
    """
    Test case extra 09
    """

    # Arrange
    source_markdown = """> abc
> ```yaml
> def:
>    - ghi
> ```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,3):`:3:yaml:::::]",
        "[text(3,3):def:\n   - ghi:]",
        "[end-fcode-block:::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<pre><code class="language-yaml">def:
   - ghi
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_09c() -> None:
    """
    Test case extra 09
    """

    # Arrange
    source_markdown = """1. abc
   ```yaml
   def:
1. ghi
   ```"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,4):`:3:yaml:::::]",
        "[text(3,4):def::]",
        "[end-fcode-block::::True]",
        "[li(4,1):3::1]",
        "[para(4,4):]",
        "[text(4,4):ghi:]",
        "[end-para:::False]",
        "[fcode-block(5,4):`:3::::::]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<pre><code class="language-yaml">def:
</code></pre>
</li>
<li>ghi
<pre><code></code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_09d() -> None:
    """
    Test case extra 09
    """

    # Arrange
    source_markdown = """- abc
  ```yaml
  def:
- ghi
  ```"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,3):`:3:yaml:::::]",
        "[text(3,3):def::]",
        "[end-fcode-block::::True]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[text(4,3):ghi:]",
        "[end-para:::False]",
        "[fcode-block(5,3):`:3::::::]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<pre><code class="language-yaml">def:
</code></pre>
</li>
<li>ghi
<pre><code></code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_09e() -> None:
    """
    Test case extra 09
    """

    # Arrange
    source_markdown = """1. abc
   ```yaml
   def:
   1. ghi
   ```"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,4):`:3:yaml:::::]",
        "[text(3,4):def:\n1. ghi:]",
        "[end-fcode-block:::3:False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<pre><code class="language-yaml">def:
1. ghi
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_09f() -> None:
    """
    Test case extra 09
    """

    # Arrange
    source_markdown = """- abc
  ```yaml
  def:
  - ghi
  ```"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,3):`:3:yaml:::::]",
        "[text(3,3):def:\n- ghi:]",
        "[end-fcode-block:::3:False]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<pre><code class="language-yaml">def:
- ghi
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_10x() -> None:
    """
    Test case extra 10
    """

    # Arrange
    source_markdown = """1. abc
   ```yaml
   def:
   > ghi
   ```"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,4):`:3:yaml:::::]",
        "[text(3,4):def:\n\a>\a&gt;\a ghi:]",
        "[end-fcode-block:::3:False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<pre><code class="language-yaml">def:
&gt; ghi
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_extra_10a() -> None:
    """
    Test case extra 10
    """

    # Arrange
    source_markdown = """- abc
  ```yaml
  def:
  > ghi
  ```"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,3):`:3:yaml:::::]",
        "[text(3,3):def:\n\a>\a&gt;\a ghi:]",
        "[end-fcode-block:::3:False]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<pre><code class="language-yaml">def:
&gt; ghi
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
