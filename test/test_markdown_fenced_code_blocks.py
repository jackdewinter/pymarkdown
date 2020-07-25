"""
https://github.github.com/gfm/#fenced-code-blocks
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import (
    assert_if_lists_different,
    assert_if_strings_different,
    assert_token_consistency,
)


# pylint: disable=too-many-lines
@pytest.mark.gfm
def test_fenced_code_blocks_089():
    """
    Test case 089:  Simple example with backticks
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """```
<
 >
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text:\a<\a&lt;\a\n \a>\a&gt;\a:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code>&lt;
 &gt;
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_090():
    """
    Test case 090:  Simple example with tildes
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """~~~
<
 >
~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:3::::::]",
        "[text:\a<\a&lt;\a\n \a>\a&gt;\a:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code>&lt;
 &gt;
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_091():
    """
    Test case 091:  Fewer than three backticks is not enough:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """``
foo
``"""
    expected_tokens = ["[para(1,1):\n\n]", "[icode-span:foo]", "[end-para]"]
    expected_gfm = """<p><code>foo</code></p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_092():
    """
    Test case 092:  (part a) The closing code fence must use the same character as the opening fence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """```
aaa
~~~
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text:aaa\n~~~:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code>aaa
~~~
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_093():
    """
    Test case 093:  (part b) The closing code fence must use the same character as the opening fence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """~~~
aaa
```
~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:3::::::]",
        "[text:aaa\n```:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code>aaa
```
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_094():
    """
    Test case 094:  (part a) The closing code fence must be at least as long as the opening fence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """````
aaa
```
``````"""
    expected_tokens = [
        "[fcode-block(1,1):`:4::::::]",
        "[text:aaa\n```:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code>aaa
```
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_095():
    """
    Test case 095:  (part b) The closing code fence must be at least as long as the opening fence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """~~~~
aaa
~~~
~~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:4::::::]",
        "[text:aaa\n~~~:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code>aaa
~~~
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_096():
    """
    Test case 096:  (part a) Unclosed code blocks are closed by the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """```"""
    expected_tokens = ["[fcode-block(1,1):`:3::::::]", "[end-fcode-block]"]
    expected_gfm = """<pre><code></code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_097():
    """
    Test case 097:  (part b) Unclosed code blocks are closed by the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """`````

```
aaa"""
    expected_tokens = [
        "[fcode-block(1,1):`:5::::::]",
        "[BLANK(2,1):]",
        "[text:```\naaa:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code>
```
aaa
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_098():
    """
    Test case 098:  (part c) Unclosed code blocks are closed by the end of the document (or the enclosing block quote or list item):
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> ```
> aaa

bbb"""
    expected_tokens = [
        "[block-quote(1,1):]",
        "[fcode-block(1,3):`:3::::::]",
        "[text:aaa:]",
        "[end-fcode-block]",
        "[end-block-quote]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text:bbb:]",
        "[end-para]",
    ]
    expected_gfm = """<blockquote>
<pre><code>aaa
</code></pre>
</blockquote>
<p>bbb</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_098a():
    """
    Test case 098a:  Modified 98 without a space between the block quote indicator and the string.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> ```
>aaa

bbb"""
    expected_tokens = [
        "[block-quote(1,1):]",
        "[fcode-block(1,3):`:3::::::]",
        "[text:aaa:]",
        "[end-fcode-block]",
        "[end-block-quote]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text:bbb:]",
        "[end-para]",
    ]
    expected_gfm = """<blockquote>
<pre><code>aaa
</code></pre>
</blockquote>
<p>bbb</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_098b():
    """
    Test case 098b:  Modified 98 with extra ">" before second line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> ```
>> aaa

bbb"""
    expected_tokens = [
        "[block-quote(1,1):]",
        "[fcode-block(1,3):`:3::::::]",
        "[text:\a>\a&gt;\a aaa:]",
        "[end-fcode-block]",
        "[end-block-quote]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text:bbb:]",
        "[end-para]",
    ]
    expected_gfm = """<blockquote>
<pre><code>&gt; aaa
</code></pre>
</blockquote>
<p>bbb</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_098c():
    """
    Test case 098c:  Modified 98 with less ">" before second line.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """> ```
aaa

bbb"""
    expected_tokens = [
        "[block-quote(1,1):]",
        "[fcode-block(1,3):`:3::::::]",
        "[end-fcode-block]",
        "[end-block-quote]",
        "[para(2,1):]",
        "[text:aaa:]",
        "[end-para]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text:bbb:]",
        "[end-para]",
    ]
    expected_gfm = """<blockquote>
<pre><code></code></pre>
</blockquote>
<p>aaa</p>
<p>bbb</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_099():
    """
    Test case 099:  A code block can have all empty lines as its content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """```

  
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[BLANK(2,1):]",
        "[BLANK(3,1):  ]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code>
  
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_100():
    """
    Test case 100:  A code block can be empty:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """```
```"""
    expected_tokens = ["[fcode-block(1,1):`:3::::::]", "[end-fcode-block]"]
    expected_gfm = """<pre><code></code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_101():
    """
    Test case 101:  (part a)  Fences can be indented. If the opening fence is indented, content lines will have equivalent opening indentation removed, if present:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ ```
 aaa
aaa
```"""
    expected_tokens = [
        "[fcode-block(1,2):`:3::::: :]",
        "[text:aaa\naaa:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code>aaa
aaa
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_102():
    """
    Test case 102:  (part b)  Fences can be indented. If the opening fence is indented, content lines will have equivalent opening indentation removed, if present:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """  ```
aaa
  aaa
aaa
  ```"""
    expected_tokens = [
        "[fcode-block(1,3):`:3:::::  :]",
        "[text:aaa\naaa\naaa:]",
        "[end-fcode-block:  ]",
    ]
    expected_gfm = """<pre><code>aaa
aaa
aaa
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_103():
    """
    Test case 103:  (part c)  Fences can be indented. If the opening fence is indented, content lines will have equivalent opening indentation removed, if present:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   ```
   aaa
    aaa
  aaa
   ```"""
    expected_tokens = [
        "[fcode-block(1,4):`:3:::::   :]",
        "[text:aaa\n aaa\naaa:]",
        "[end-fcode-block:   ]",
    ]
    expected_gfm = """<pre><code>aaa
 aaa
aaa
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_104():
    """
    Test case 104:  Four spaces indentation produces an indented code block:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    ```
    aaa
    ```"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    \n    ]",
        "[text:```\naaa\n```:]",
        "[end-icode-block]",
    ]
    expected_gfm = """<pre><code>```
aaa
```
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_105():
    """
    Test case 105:  (part a) Closing fences may be indented by 0-3 spaces, and their indentation need not match that of the opening fence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """```
aaa
  ```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text:aaa:]",
        "[end-fcode-block:  ]",
    ]
    expected_gfm = """<pre><code>aaa
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_106():
    """
    Test case 106:  (part b) Closing fences may be indented by 0-3 spaces, and their indentation need not match that of the opening fence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """   ```
aaa
  ```"""
    expected_tokens = [
        "[fcode-block(1,4):`:3:::::   :]",
        "[text:aaa:]",
        "[end-fcode-block:  ]",
    ]
    expected_gfm = """<pre><code>aaa
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_107():
    """
    Test case 107:  This is not a closing fence, because it is indented 4 spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """```
aaa
    ```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text:aaa\n    ```:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code>aaa
    ```
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_108():
    """
    Test case 108:  (part a) Code fences (opening and closing) cannot contain internal spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """``` ```
aaa"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[icode-span: ]",
        """[text:
aaa::\n]""",
        "[end-para]",
    ]
    expected_gfm = """<p><code> </code>
aaa</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_109():
    """
    Test case 109:  (part b) Code fences (opening and closing) cannot contain internal spaces:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """~~~~~~
aaa
~~~ ~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:6::::::]",
        "[text:aaa\n~~~ ~~:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code>aaa
~~~ ~~
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_110():
    """
    Test case 110:  Fenced code blocks can interrupt paragraphs, and can be followed directly by paragraphs, without a blank line between:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo
```
bar
```
baz"""
    expected_tokens = [
        "[para(1,1):]",
        "[text:foo:]",
        "[end-para]",
        "[fcode-block(2,1):`:3::::::]",
        "[text:bar:]",
        "[end-fcode-block]",
        "[para(5,1):]",
        "[text:baz:]",
        "[end-para]",
    ]
    expected_gfm = """<p>foo</p>
<pre><code>bar
</code></pre>
<p>baz</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_111():
    """
    Test case 111:  Other blocks can also occur before and after fenced code blocks without an intervening blank line:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo
---
~~~
bar
~~~
# baz"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text:foo:]",
        "[end-setext::]",
        "[fcode-block(3,1):~:3::::::]",
        "[text:bar:]",
        "[end-fcode-block]",
        "[atx(6,1):1:0:]",
        "[text:baz: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>foo</h2>
<pre><code>bar
</code></pre>
<h1>baz</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_112():
    """
    Test case 112:  (part a) An info string can be provided after the opening code fence.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """```ruby
def foo(x)
  return 3
end
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:ruby:::::]",
        "[text:def foo(x)\n  return 3\nend:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code class="language-ruby">def foo(x)
  return 3
end
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_113():
    """
    Test case 113:  (part b) An info string can be provided after the opening code fence.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """~~~~    ruby startline=3 $%@#$
def foo(x)
  return 3
end
~~~~~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:4:ruby:: startline=3 $%@#$:::    ]",
        "[text:def foo(x)\n  return 3\nend:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code class="language-ruby">def foo(x)
  return 3
end
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_114():
    """
    Test case 114:  (part c) An info string can be provided after the opening code fence.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """````;
````"""
    expected_tokens = ["[fcode-block(1,1):`:4:;:::::]", "[end-fcode-block]"]
    expected_gfm = """<pre><code class="language-;"></code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_115():
    """
    Test case 115:  Info strings for backtick code blocks cannot contain backticks:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """``` aa ```
foo"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[icode-span:aa]",
        """[text:
foo::\n]""",
        "[end-para]",
    ]
    expected_gfm = """<p><code>aa</code>
foo</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_116():
    """
    Test case 116:  Info strings for tilde code blocks can contain backticks and tildes:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """~~~ aa ``` ~~~
foo
~~~"""
    expected_tokens = [
        "[fcode-block(1,1):~:3:aa:: ``` ~~~::: ]",
        "[text:foo:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code class="language-aa">foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)


@pytest.mark.gfm
def test_fenced_code_blocks_117():
    """
    Test case 117:  Closing code fences cannot have info strings:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """```
``` aaa
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3::::::]",
        "[text:``` aaa:]",
        "[end-fcode-block]",
    ]
    expected_gfm = """<pre><code>``` aaa
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
    assert_token_consistency(source_markdown, actual_tokens)
