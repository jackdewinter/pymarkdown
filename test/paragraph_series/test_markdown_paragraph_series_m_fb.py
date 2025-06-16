"""
https://github.github.com/gfm/#paragraph
"""

from test.utils import act_and_assert

import pytest

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_nl_fb() -> None:
    """
    Test case:  Ordered list newline fenced block
    was:        test_list_blocks_256jx
    """

    # Arrange
    source_markdown = """1.
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[fcode-block(2,1):`:3::::::]",
        "[text(3,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_nl_all_i3_fb() -> None:
    """
    Test case:  Ordered list newline (all indented) fenced block
    """

    # Arrange
    source_markdown = """1.
   ```
   foo
   ```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   \n]",
        "[BLANK(1,3):]",
        "[fcode-block(2,4):`:3::::::]",
        "[text(3,4):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code>foo
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_nl_i2_fb() -> None:
    """
    Test case:  Ordered list newline indent of 2 fenced block
    was:        test_list_blocks_256jxa
    """

    # Arrange
    source_markdown = """1.
  ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[fcode-block(2,3):`:3:::::  :]",
        "[text(3,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_nl_i3_fb() -> None:
    """
    Test case:  Ordered list newline indent of 2 fenced block
    was:        test_list_blocks_256jxb
    """

    # Arrange
    source_markdown = """1.
   ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[fcode-block(2,4):`:3::::::]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
        "[para(3,1):]",
        "[text(3,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(4,1):`:3::::::]",
        "[text(5,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<ol>
<li>
<pre><code></code></pre>
</li>
</ol>
<p>foo</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_t_nl_fb() -> None:
    """
    Test case:  Ordered list text newline fenced block
    was:        test_list_blocks_256ja
    """

    # Arrange
    source_markdown = """1.  abc
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:4:]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(2,1):`:3::::::]",
        "[text(3,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_t_nl_all_i4_fb() -> None:
    """
    Test case:  Ordered list text newline (all indented) fenced block
    """

    # Arrange
    source_markdown = """1.  abc
    ```
    foo
    ```
"""
    expected_tokens = [
        "[olist(1,1):.:1:4::    \n    \n    \n]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3::::::]",
        "[text(3,5):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<pre><code>foo
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_t_nl_i2_fb() -> None:
    """
    Test case:  Ordered list text newline indent of 2 fenced block
    was:        test_list_blocks_256jaa
    """

    # Arrange
    source_markdown = """1.  abc
  ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:4:]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(2,3):`:3:::::  :]",
        "[text(3,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_t_nl_i3_fb() -> None:
    """
    Test case:  Ordered list text newline indent of 3 fenced block
    was:        test_list_blocks_256jab
    """

    # Arrange
    source_markdown = """1.  abc
   ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:4:]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(2,4):`:3:::::   :]",
        "[text(3,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_ol_nl_fb() -> None:
    """
    Test case:  Ordered list x2 newline fenced block
    """

    # Arrange
    source_markdown = """1. 1.
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(2,1):`:3::::::]",
        "[text(3,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_ol_nl_all_i6_fb() -> None:
    """
    Test case:  Ordered list x2 newline fenced block
    """

    # Arrange
    source_markdown = """1. 1.
      ```
      foo
      ```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :      \n      \n      \n]",
        "[BLANK(1,6):]",
        "[fcode-block(2,7):`:3::::::]",
        "[text(3,7):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<pre><code>foo
</code></pre>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_ol_t_nl_fb() -> None:
    """
    Test case:  Ordered list x2 text newline fenced block
    was:        test_list_blocks_256jb
    """

    # Arrange
    source_markdown = """1. 1. abc
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(2,1):`:3::::::]",
        "[text(3,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_ol_t_nl_all_i6_fb() -> None:
    """
    Test case:  Ordered list x2 text newline fenced block
    """

    # Arrange
    source_markdown = """1. 1. abc
      ```
      foo
      ```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :      \n      \n      \n]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,7):`:3::::::]",
        "[text(3,7):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
<pre><code>foo
</code></pre>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_nl_i3_ol_nl_fb() -> None:
    """
    Test case:  Ordered list newline indent of 3 ordered list newline fenced block
    """

    # Arrange
    source_markdown = """1.
   1.
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,1):`:3::::::]",
        "[text(4,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_t_nl_i3_ol_nl_fb() -> None:
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline fenced block
    """

    # Arrange
    source_markdown = """1. abc
   1.
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\n1.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,1):`:3::::::]",
        "[text(4,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ul_t_nl_i2_ul_nl_fb() -> None:
    """
    Test case:  Unordered list text newline indent of 2 unordered list newline fenced block
    """

    # Arrange
    source_markdown = """- abc
  -
```
foo
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::]",
        "[end-ulist:::True]",
        "[fcode-block(3,1):`:3::::::]",
        "[text(4,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ul_t_nl_i2_ulb_nl_fb() -> None:
    """
    Test case:  Unordered list text newline indent of 2 unordered list (b) newline fenced block
    """

    # Arrange
    source_markdown = """- abc
  *
```
foo
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n]",
        "[text(1,3):abc\n*::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[fcode-block(3,1):`:3::::::]",
        "[text(4,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ul>
<li>abc
*</li>
</ul>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_nl_i3_ol_t_nl_fb() -> None:
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline fenced block
    was:        test_list_blocks_256jc
    """

    # Arrange
    source_markdown = """1.
   1. abc
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,1):`:3::::::]",
        "[text(4,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_t_nl_i3_ol_t_nl_fb() -> None:
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline fenced block
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,1):`:3::::::]",
        "[text(4,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_nl_i3_ol_nl_i2_fb() -> None:
    """
    Test case:  Ordered list newline indent of 3 ordered list newline indent of 2 fenced block
    """

    # Arrange
    source_markdown = """1.
   1.
  ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,3):`:3:::::  :]",
        "[text(4,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_t_nl_i3_ol_nl_i2_fb() -> None:
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline indent of 2 fenced block
    """

    # Arrange
    source_markdown = """1. abc
   1.
  ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\n1.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,3):`:3:::::  :]",
        "[text(4,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ul_t_nl_i2_ul_nl_i1_fb() -> None:
    """
    Test case:  Unordered list text newline indent of 2 unordered list newline indent of 1 fenced block
    """

    # Arrange
    source_markdown = """- abc
  -
 ```
foo
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::]",
        "[end-ulist:::True]",
        "[fcode-block(3,2):`:3::::: :]",
        "[text(4,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ul_t_nl_i2_ulb_nl_i1_fb() -> None:
    """
    Test case:  Unordered list text newline indent of 2 unordered list newline indent of 1 fenced block
    """

    # Arrange
    source_markdown = """- abc
  *
 ```
foo
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n]",
        "[text(1,3):abc\n*::\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[fcode-block(3,2):`:3::::: :]",
        "[text(4,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ul>
<li>abc
*</li>
</ul>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_nl_i3_ol_t_nl_i2_fb() -> None:
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline indent of 2 fenced block
    was:        test_list_blocks_256jd
    """

    # Arrange
    source_markdown = """1.
   1. abc
  ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,3):`:3:::::  :]",
        "[text(4,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_t_nl_i3_ol_t_nl_i2_fb() -> None:
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline indent of 2 fenced block
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
  ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,3):`:3:::::  :]",
        "[text(4,1):foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<pre><code>foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_nl_i3_ol_nl_i3_fb() -> None:
    """
    Test case:  Ordered list newline indent of 3 ordered list newline indent of 3 fenced block
    """

    # Arrange
    source_markdown = """1.
   1.
   ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[fcode-block(3,4):`:3::::::]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(5,1):`:3::::::]",
        "[text(6,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
<pre><code></code></pre>
</li>
</ol>
<p>foo</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_t_nl_i3_ol_nl_i3_fb() -> None:
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline indent of 3 fenced block
    """

    # Arrange
    source_markdown = """1. abc
   1.
   ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\n1.::\n]",
        "[end-para:::False]",
        "[fcode-block(3,4):`:3::::::]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(5,1):`:3::::::]",
        "[text(6,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
<pre><code></code></pre>
</li>
</ol>
<p>foo</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ul_t_nl_i2_ul_nl_i2_fb() -> None:
    """
    Test case:  Unordered list text newline indent of 3 unordered list newline indent of 3 fenced block
    """

    # Arrange
    source_markdown = """- abc
  -
  ```
foo
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::]",
        "[fcode-block(3,3):`:3::::::]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(5,1):`:3::::::]",
        "[text(6,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
<pre><code></code></pre>
</li>
</ul>
<p>foo</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ul_t_nl_i2_ulb_nl_i2_fb() -> None:
    """
    Test case:  Unordered list text newline indent of 3 unordered list (b) newline indent of 3 fenced block
    """

    # Arrange
    source_markdown = """- abc
  *
  ```
foo
```
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[para(1,3):\n]",
        "[text(1,3):abc\n*::\n]",
        "[end-para:::False]",
        "[fcode-block(3,3):`:3::::::]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(5,1):`:3::::::]",
        "[text(6,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<ul>
<li>abc
*
<pre><code></code></pre>
</li>
</ul>
<p>foo</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_nl_i3_ol_t_nl_i3_fb() -> None:
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline indent of 3 fenced block
    was:        test_list_blocks_256je
    """

    # Arrange
    source_markdown = """1.
   1. abc
   ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,4):`:3::::::]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(5,1):`:3::::::]",
        "[text(6,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
<pre><code></code></pre>
</li>
</ol>
<p>foo</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_fb_ol_t_nl_i3_ol_t_nl_i3_fb() -> None:
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline indent of 3 fenced block
    """

    # Arrange
    source_markdown = """1. abc
   1. abc
   ```
foo
```
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,4):`:3::::::]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
        "[para(4,1):]",
        "[text(4,1):foo:]",
        "[end-para:::False]",
        "[fcode-block(5,1):`:3::::::]",
        "[text(6,1)::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>abc</li>
</ol>
<pre><code></code></pre>
</li>
</ol>
<p>foo</p>
<pre><code></code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
