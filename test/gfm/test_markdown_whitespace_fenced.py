"""
Testing various aspects of whitespaces around fenced code blocks.
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """  ```python
abc"""
    expected_tokens = [
        "[fcode-block(1,3):`:3:python::::  :]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """  ```python
abc
  ```"""
    expected_tokens = [
        "[fcode-block(1,3):`:3:python::::  :]",
        "[text(2,1):abc:]",
        "[end-fcode-block:  ::3:False]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_too_many_spaces_before():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """abc
    ```python
    abc"""
    expected_tokens = [
        "[para(1,1):\n    \n    ]",
        "[text(1,1):abc\n```python\nabc::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>abc
```python
abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t ```python
 \t abc"""
    expected_tokens = [
        "[icode-block(1,5): \t:\n \t]",
        "[text(1,5): ```python\n abc:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code> ```python
 abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_form_feeds_before():
    """
    Test case:  Fenced Code blocks preceeded by spaces and form feeds.
    """

    # Arrange
    source_markdown = """ \u000C ```python
 \u000C abc"""
    expected_tokens = [
        "[para(1,2): \u000C \n ]",
        "[text(1,2):```python\n\u000C abc::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>```python
\u000C abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_list():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
    ```python
    abc"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::  :]",
        "[text(3,3):abc:\a  \a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_list_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
    ```python
    abc
    ```"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::  :]",
        "[text(3,3):abc:\a  \a\x03\a]",
        "[end-fcode-block:  ::3:False]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_block_quotes():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> def
    ```python
    abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):\n\n    \n    ]",
        "[text(1,3):abc\ndef\n```python\nabc::\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
```python
abc</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_block_quotes_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> def
    ```python
    abc
    ```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n\n]",
        "[para(1,3):\n\n    \n    \n    ]",
        "[text(1,3):abc\ndef\n::\n\n]",
        "[icode-span(3,5):python\a\n\a \aabc\a\n\a \a:```::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
<code>python abc </code></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
    ```python
    abc"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n]",
        "[para(2,5):\n    \n    ]",
        "[text(2,5):def\n```python\nabc::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
```python
abc</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
    ```python
    abc
    ```"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n\n]",
        "[para(2,5):\n    \n    \n    ]",
        "[text(2,5):def\n::\n]",
        "[icode-span(3,5):python\a\n\a \aabc\a\n\a \a:```::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
<code>python abc </code></p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes_with_single_x():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   ```python
>   abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[fcode-block(3,5):`:3:python::::  :]",
        "[text(4,3):abc:\a  \a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<pre><code class="language-python">abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_html_open_with_spaces_before_within_double_block_quotes_with_single_x():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   <style>
>   abc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[html-block(3,3)]",
        "[text(3,5):<style>\n  abc:  ]",
        "[end-html-block:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
  <style>
  abc
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes_with_single_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   ```python
>   abc
>   ```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[fcode-block(3,5):`:3:python::::  :]",
        "[text(4,3):abc:\a  \a\x03\a]",
        "[end-fcode-block:  ::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<pre><code class="language-python">abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_unordered_list_x():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
\t```python
\tabc"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::\t:]",
        "[text(3,1):abc:\a\t\a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_unordered_list_x_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
\t```python
\tabc
\t```"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::\t:]",
        "[text(3,1):abc:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_unordered_list_and_single_space_x():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc
 \t```python
 \tabc"""
    expected_tokens = [
        "[ulist(1,1):-::2:: \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::\t:]",
        "[text(3,1):abc:\a \t\a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_unordered_list_and_single_space_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc
 \t```python
 \tabc
 \t```"""
    expected_tokens = [
        "[ulist(1,1):-::2:: \n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::\t:]",
        "[text(3,1):abc:\a \t\a\x03\a]",
        "[end-fcode-block: \t::3:False]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_unordered_list_and_spaces():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  \t```python
  \tabc"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::\t:]",
        "[text(3,3):abc:\a\t\a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_unordered_list_and_spaces_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """
    # TODO: https://babelmark.github.io/?text=-+abc%0A++%09%60%60%60python%0A++%09abc%0A++%09%60%60%60
    # presents tab at the start of the block

    # Arrange
    source_markdown = """- abc
  \t```python
  \tabc
  \t```"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::\t:]",
        "[text(3,3):abc:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_unordered_double_list():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  - def
\t```python
\tabc"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :\t\n\t]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::False]",
        "[fcode-block(3,5):`:3:python:::::]",
        "[text(4,2):abc:]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>def
<pre><code class="language-python">abc
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_unordered_double_list_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  - def
\t```python
\tabc
\t```"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :\t\n\t\n\t]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::False]",
        "[fcode-block(3,5):`:3:python:::::]",
        "[text(4,2):abc:]",
        "[end-fcode-block:::3:False]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>def
<pre><code class="language-python">abc
</code></pre>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_list_x():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
\t```python
\tabc"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::\t:]",
        "[text(3,1):abc:\a\t\a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_list_x_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
\t```python
\tabc
\t```"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::\t:]",
        "[text(3,1):abc:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_ordered_list():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
    ```python
    abc"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python:::: :]",
        "[text(3,4):abc:\a \a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_ordered_list_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
    ```python
    abc
    ```"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python:::: :]",
        "[text(3,4):abc:\a \a\x03\a]",
        "[end-fcode-block: ::3:False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_list_and_single_space_x():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
 \t```python
 \tabc"""
    expected_tokens = [
        "[olist(1,1):.:1:3:: \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::\t:]",
        "[text(3,1):abc:\a \t\a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_list_and_single_space_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
 \t```python
 \tabc
 \t```"""
    expected_tokens = [
        "[olist(1,1):.:1:3:: \n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::\t:]",
        "[text(3,1):abc:\a \t\a\x03\a]",
        "[end-fcode-block: \t::3:False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_list_and_spaces_x():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
  \t```python
  \tabc"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::\t:]",
        "[text(3,1):abc:\a  \t\a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_list_and_spaces_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
  \t```python
  \tabc
  \t```"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  \n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::False]",
        "[fcode-block(2,5):`:3:python::::\t:]",
        "[text(3,1):abc:\a  \t\a\x03\a]",
        "[end-fcode-block:  \t::3:False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_double_list_x():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t  ```python
\t  abc"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\t  \n\t  ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[fcode-block(3,7):`:3:python:::::]",
        "[text(4,4):abc:]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_double_list_x_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t  ```python
\t  abc
\t  ```"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\t  \n\t  \n\t  ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[fcode-block(3,7):`:3:python:::::]",
        "[text(4,4):abc:]",
        "[end-fcode-block:::3:False]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_double_list_no_spaces_x():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t```python
\tabc"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,5):`:3:python::::\t:]",
        "[text(4,1):abc:\a\t\a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_double_list_no_spaces_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t```python
\tabc
\t```"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,5):`:3:python::::\t:]",
        "[text(4,1):abc:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_double_list_tab_after_indent():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
   ```python \tfred\tfred
   abc\tabc"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,4):`:3:python:: \tfred\tfred:::]",
        "[text(4,4):abc\tabc:]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<pre><code class="language-python">abc	abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_double_list_tab_after_indent_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
   ```python \tfred\tfred
   abc\tabc
   ```"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,4):`:3:python:: \tfred\tfred:::]",
        "[text(4,4):abc\tabc:]",
        "[end-fcode-block:::3:False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<pre><code class="language-python">abc	abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_double_list_one_space_after():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t ```python
\t abc"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,6):`:3:python::::\t :]",
        "[text(4,1):abc:\a\t \a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_double_list_one_space_after_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t ```python
\t abc
\t ```"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,6):`:3:python::::\t :]",
        "[text(4,1):abc:\a\t \a\x03\a]",
        "[end-fcode-block:\t ::3:False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_double_list_one_space_before():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
 \t```python
 \tabc"""
    expected_tokens = [
        "[olist(1,1):.:1:3:: \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,5):`:3:python::::\t:]",
        "[text(4,1):abc:\a \t\a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_double_list_one_space_before_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
 \t```python
 \tabc
 \t```"""
    expected_tokens = [
        "[olist(1,1):.:1:3:: \n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,5):`:3:python::::\t:]",
        "[text(4,1):abc:\a \t\a\x03\a]",
        "[end-fcode-block: \t::3:False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_double_list_only_spaces():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
    ```python
    abc"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,5):`:3:python:::: :]",
        "[text(4,4):abc:\a \a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_ordered_double_list_only_spaces_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
    ```python
    abc
    ```"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[fcode-block(3,5):`:3:python:::: :]",
        "[text(4,4):abc:\a \a\x03\a]",
        "[end-fcode-block: ::3:False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<pre><code class="language-python">abc
</code></pre>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_formfeeds_before_within_list():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
 \u000C \u000C```python
 \u000C \u000Cabc"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n]",
        "[para(1,3):\n \n ]",
        "[text(1,3):abc\n\u000C \u000C```python\n\u000C \u000Cabc::\n\n]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
\u000C \u000C```python
\u000C \u000Cabc</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_formfeeds_before_within_list_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
 \u000C \u000C```python
 \u000C \u000Cabc
 \u000C \u000C```"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n\n]",
        "[para(1,3):\n \n \n ]",
        "[text(1,3):abc\n\u000C \u000C::\n]",
        "[icode-span(2,5):python\a\n\a \a\u000C \u000Cabc\a\n\a \a\u000C \u000C:```::]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
\u000C \u000C<code>python \u000C \u000Cabc \u000C \u000C</code></li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes_with_zero_and_zero_spaces_at_start():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
```python
abc"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,1):`:3:python:::::]",
        "[text(4,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes_with_zero_and_zero_spaces_at_start_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
```python
abc
```"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,1):`:3:python:::::]",
        "[text(4,1):abc:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes_with_zero_and_one_space_at_start():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
 ```python
 abc"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,2):`:3:python:::: :]",
        "[text(4,2):abc:\a \a\x03\a]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes_with_zero_and_one_space_at_start_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
 ```python
 abc
 ```"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,2):`:3:python:::: :]",
        "[text(4,2):abc:\a \a\x03\a]",
        "[end-fcode-block: ::3:False]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes_with_zero_and_two_spaces_at_start():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
  ```python
  abc"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,3):`:3:python::::  :]",
        "[text(4,3):abc:\a  \a\x03\a]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes_with_zero_and_two_spaces_at_start_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
  ```python
  abc
  ```"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,3):`:3:python::::  :]",
        "[text(4,3):abc:\a  \a\x03\a]",
        "[end-fcode-block:  ::3:False]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes_with_zero_and_three_spaces_at_start():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
   ```python
   abc"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,4):`:3:python::::   :]",
        "[text(4,4):abc:\a   \a\x03\a]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes_with_zero_and_three_spaces_at_start_with_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
   ```python
   abc
   ```"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[fcode-block(3,4):`:3:python::::   :]",
        "[text(4,4):abc:\a   \a\x03\a]",
        "[end-fcode-block:   ::3:False]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
</blockquote>
<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes_with_zero_and_four_spaces_at_start():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quotes()


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quotes_x1():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
\t```python
\tabc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):\n\n\t\n\t]",
        "[text(1,3):abc\ndef\n```python\nabc::\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
```python
abc</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quotes_x1_and_close():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
\t```python
\tabc
\t```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n\n]",
        "[para(1,3):\n\n\t\n\t\n\t]",
        "[text(1,3):abc\ndef\n::\n\n]",
        "[icode-span(3,2):python\a\n\a \a\a\x03\a\t\aabc\a\n\a \a\a\x03\a\t\a:```::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
<code>python \tabc \t</code></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quotes_x2():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
  \t```python
  \tabc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):\n\n  \t\n  \t]",
        "[text(1,3):abc\ndef\n```python\nabc::\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
```python
abc</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quotes_x2_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
  \t```python
  \tabc
  \t```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n\n]",
        "[para(1,3):\n\n  \t\n  \t\n  \t]",
        "[text(1,3):abc\ndef\n::\n\n]",
        "[icode-span(3,4):python\a\n\a \aabc\a\n\a \a:```::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
<code>python abc </code></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quotes_repeat():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>\t```python
>\tghi"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::False]",
        "[fcode-block(3,5):`:3:python::::\t:]",
        "[text(4,3):ghi:\a\t\a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
<pre><code class="language-python">ghi
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quotes_repeat_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>\t```python
>\tghi
>\t```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>\n>]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::False]",
        "[fcode-block(3,5):`:3:python::::\t:]",
        "[text(4,3):ghi:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
<pre><code class="language-python">ghi
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quotes_bare_repeat():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t```python
>\tabc"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[fcode-block(1,5):`:3:python::::\t:]",
        "[text(2,2):abc:\a\t\a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quotes_bare_repeat_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t```python
>\tabc
>\t```"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>]",
        "[fcode-block(1,5):`:3:python::::\t:]",
        "[text(2,2):abc:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quotes_bare_with_space_repeat():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> \t```python
> \tabc"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[fcode-block(1,5):`:3:python::::\t:]",
        "[text(2,3):abc:\a\t\a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quotes_bare_with_space_repeat_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> \t```python
> \tabc
> \t```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[fcode-block(1,5):`:3:python::::\t:]",
        "[text(2,3):abc:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quotes_bare_with_many_tabs():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t```python\tttt
>\tabc\tdef\tghi"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>]",
        "[fcode-block(1,5):`:3:python::\tttt::\t:]",
        "[text(2,2):abc\tdef\tghi:\a\t\a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc	def	ghi
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quotes_bare_with_many_tabs_and_close():
    """
    Test case:  Fenced Code blocks preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t```python\tttt
>\tabc\tdef\tghi
>\t```"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>]",
        "[fcode-block(1,5):`:3:python::\tttt::\t:]",
        "[text(2,2):abc\tdef\tghi:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc	def	ghi
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


###


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_1a():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
> \t```python"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::False]",
        "[fcode-block(3,5):`:3:python::::\t:]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
<pre><code class="language-python"></code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_x():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t```python
>\tabc
>\t```"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>]",
        "[fcode-block(1,5):`:3:python::::\t:]",
        "[text(2,2):abc:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_1():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t```\tpython\tother\t
>\tabc\t
>\t```"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>]",
        "[fcode-block(1,5):`:3:python::\tother\t::\t:\t]",
        "[text(2,2):abc\t:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc\t
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_2():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t```\tpython\tother\t
>\tabc\t
>\t```\t"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>]",
        "[fcode-block(1,5):`:3:python::\tother\t::\t:\t]",
        "[text(2,2):abc\t\n\a\t\a\x03\a```\t:\a\t\a\x03\a]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc\t
```\t
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_with_space():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> \t```python
> \tabc
> \t```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[fcode-block(1,5):`:3:python::::\t:]",
        "[text(2,3):abc:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_with_2_spaces_x():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>  \t```python
>  \tabc
>  \t```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[fcode-block(1,5):`:3:python:::: \t:]",
        "[text(2,3):abc:\a \t\a\x03\a]",
        "[end-fcode-block: \t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_with_2_spaces_with_less_indent():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> \t```python
>  \tabc
>  \t```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[fcode-block(1,5):`:3:python::::\t:]",
        "[text(2,3):abc:\a \t\a\x03\a]",
        "[end-fcode-block: \t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_with_2_spaces_with_more_indent():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> \t```python
>  \t abc
>  \t ```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[fcode-block(1,5):`:3:python::::\t:]",
        "[text(2,3):abc:\a \t \a \a]",
        "[end-fcode-block: \t ::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python"> abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_with_2_spaces_with_no_indent():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t```python
>  \tabc
>  \t```"""
    expected_tokens = [
        "[block-quote(1,1)::>\n> \n> ]",
        "[fcode-block(1,5):`:3:python::::\t:]",
        "[text(2,3):abc:\a \t\a\x03\a]",
        "[end-fcode-block: \t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_with_2_spaces_with_max_indent_x():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>    ```python
> \tabc
> ```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[fcode-block(1,6):`:3:python::::   :]",
        "[text(2,3):abc:\a\t\a\x03\a]",
        "[end-fcode-block:::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_with_2_spaces_with_max_indent_max_1():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>    ```python
> \t\tabc
> ```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[fcode-block(1,6):`:3:python::::   :]",
        "[text(2,3):abc:\a\t\a\x03\a\a\t\a   \a]",
        "[end-fcode-block:::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">   abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_with_2_spaces_with_max_indent_max_2():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>  ```python
> \tabc
> ```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[fcode-block(1,4):`:3:python:::: :]",
        "[text(2,3):abc:\a\t\a \a]",
        "[end-fcode-block:::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python"> abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_with_2_spaces_with_max_indent_max_3():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>    ```python
> \t\t abc
> ```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[fcode-block(1,6):`:3:python::::   :]",
        "[text(2,3):abc:\a\t\a\x03\a\a\t\a   \a ]",
        "[end-fcode-block:::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">    abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_with_2_spaces_with_max_indent_max_4():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>  ```python
> \t abc
> ```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[fcode-block(1,4):`:3:python:::: :]",
        "[text(2,3):abc:\a\t\a \a ]",
        "[end-fcode-block:::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">  abc
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_with_2_spaces_with_varying_indent_1():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t```python
>\tdef _xyz():
>\t\tpass
>\t```"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>\n>]",
        "[fcode-block(1,5):`:3:python::::\t:]",
        "[text(2,2):def _xyz():\n\a\t\t\a\t\apass:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">def _xyz():
\tpass
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_with_2_spaces_with_varying_indent_2():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """>\t```python
>\tdef _xyz():
>\t\t  pass
>\t```"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>\n>]",
        "[fcode-block(1,5):`:3:python::::\t:]",
        "[text(2,2):def _xyz():\n\a\t\t  \a\t  \apass:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">def _xyz():
\t  pass
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2_bare_with_2_spaces_with_varying_indent_3():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> \t```python
> \tdef _xyz():
> \t\t  pass
> \t```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[fcode-block(1,5):`:3:python::::\t:]",
        "[text(2,3):def _xyz():\n\a\t\t  \a\t  \apass:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-python">def _xyz():
\t  pass
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_double_block_quote():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
\t```python"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n\t]",
        "[text(2,5):def\n```python::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
```python</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_double_block_quote_with_single_x():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
>\t```python"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::False]",
        "[end-block-quote::>:True]",
        "[fcode-block(3,5):`:3:python::::\t:]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<pre><code class="language-python"></code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_double_block_quote_with_single_and_space():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
> \t```python"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> ]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::False]",
        "[end-block-quote::> :True]",
        "[fcode-block(3,5):`:3:python::::\t:]",
        "[end-fcode-block::::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def</p>
</blockquote>
<pre><code class="language-python"></code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


###


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_info():
    """
    Test case:  Fenced Code blocks info string followed by spaces.
    """

    # Arrange
    source_markdown = """```  python
abc"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::  ]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_info():
    """
    Test case:  Fenced Code block info string followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """```\tpython
abc"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::\t]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_form_feeds_before_info():
    """
    Test case:  Fenced Code blocks info string followed by form feeds.
    """

    # Arrange
    source_markdown = """```\u000Cpython
abc"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::\u000C]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_after_info():
    """
    Test case:  Fenced Code blocks info string followed by spaces.
    """

    # Arrange
    source_markdown = """```python  
abc"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::  :::]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_after_info():
    """
    Test case:  Fenced Code block info string followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """```python\t
abc"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::\t:::]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_form_feeds_after_language():
    """
    Test case:  Fenced Code blocks info string followed by form feeds.
    """

    # Arrange
    source_markdown = """```python\u000C
abc"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::\u000C:::]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_form_feeds_after_info():
    """
    Test case:  Fenced Code blocks info string followed by form feeds.
    """

    # Arrange
    source_markdown = """```python a\u000C\a
abc""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:: a\u000C :::]",
        "[text(2,1):abc:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_tabs_within():
    """
    Test case:  Fenced Code blocks...
    """

    # Arrange
    source_markdown = """```python
abc\tdef
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::]",
        "[text(2,1):abc\tdef:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code class="language-python">abc\tdef
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_spaces_before():
    """
    Test case:  Fenced Code blocks closed preceeded by spaces.
    """

    # Arrange
    source_markdown = """```python
abc
  ```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::]",
        "[text(2,1):abc:]",
        "[end-fcode-block:  ::3:False]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_tabs_before():
    """
    Test case:  Fenced Code block closed preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """```python
abc
\t```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::]",
        "[text(2,1):abc\n\t```:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
\t```
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_tabs_before_x():
    """
    Test case:  Fenced Code block closed preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- ```python
  abc
  \t```"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[fcode-block(1,3):`:3:python:::::]",
        "[text(2,3):abc:]",
        "[end-fcode-block:\t::3:False]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code class="language-python">abc
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_form_feeds_before():
    """
    Test case:  Fenced Code blocks closed preceeded by form feeds.
    """

    # Arrange
    source_markdown = """```python
abc
\u000C```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python:::::]",
        "[text(2,1):abc\n\u000C```:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
\u000C```
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_spaces_after():
    """
    Test case:  Fenced Code blocks closed followed by spaces.
    """

    # Arrange
    source_markdown = """```python  
abc
``` """
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::  :::]",
        "[text(2,1):abc:]",
        "[end-fcode-block:: :3:False]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_tabs_after():
    """
    Test case:  Fenced Code block closed followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """```python  
abc
```\t"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::  :::]",
        "[text(2,1):abc\n```\t:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
```\t
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_tabs_after_and_before():
    """
    Test case:  Fenced Code block close followed by tabs and preceeded be spaces.
    """

    # Arrange
    source_markdown = """```python  
abc
  ```\t"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::  :::]",
        "[text(2,1):abc\n  ```\t:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
  ```\t
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_tabs_after_and_before_2():
    """
    Test case:  Fenced Code block close followed by tabs and preceeded be spaces.
    """

    # Arrange
    source_markdown = """- ```python  
  abc
  ```\t"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[fcode-block(1,3):`:3:python::  :::]",
        "[text(2,3):abc\n```\t:]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code class="language-python">abc
```\t
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_closed_with_form_feeds_after():
    """
    Test case:  Fenced Code blocks closed followed by form feeds.
    """

    # Arrange
    source_markdown = """```python  
abc
```\u000C"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::  :::]",
        "[text(2,1):abc\n```\u000C:]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
```\u000C
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_with_tabs_inside():
    """
    Test case:  Fenced Code block closed followed by spaces and tabs.
    """

    # Arrange
    source_markdown = """```python  
abc\tdef
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:python::  :::]",
        "[text(2,1):abc\tdef:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code class="language-python">abc\tdef
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
