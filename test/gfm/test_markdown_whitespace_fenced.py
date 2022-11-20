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
def test_whitespaces_fenced_code_open_with_one_space_before():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """  ```python
 abc"""
    expected_tokens = [
        "[fcode-block(1,3):`:3:python::::  :]",
        "[text(2,2):abc:\a \a\x03\a]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<pre><code class="language-python">abc
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_block_quote():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> def
    ```python"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n    ]",
        "[text(1,3):abc\ndef\n```python::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
```python</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quote():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
    ```python"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n]",
        "[para(2,5):\n    ]",
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
def test_whitespaces_fenced_code_open_with_spaces_before_within_double_block_quote_with_single():
    """
    Test case:  Fenced Code blocks preceeded by spaces.
    """

    # Arrange
    source_markdown = """> abc
> > def
>   ```python"""
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
        "[fcode-block(3,5):`:3:python::::  :]",
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
def test_whitespaces_fenced_code_open_with_tabs_before():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """ \t```python
abc"""
    expected_tokens = [
        "[icode-block(1,5): \t:]",
        "[text(1,5):```python:]",
        "[end-icode-block:::False]",
        "[para(2,1):]",
        "[text(2,1):abc:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<pre><code>```python
</code></pre>
<p>abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
\t```python"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n]",
        "[para(1,3):\n\n\t]",
        "[text(1,3):abc\ndef\n```python::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
```python</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_1x():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>\t```python"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>]",
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
def test_whitespaces_fenced_code_open_with_tabs_before_within_block_quote_inside_2x():
    """
    Test case:  Fenced Code block preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>\t```python
>\tabc
>\t```"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>\n>]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::False]",
        "[fcode-block(3,5):`:3:python::::\t:]",
        "[text(4,3):abc:\a\t\a\x03\a]",
        "[end-fcode-block:\t::3:False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
<pre><code class="language-python">abc
</code></pre>
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


@pytest.mark.gfm
def test_whitespaces_fenced_code_open_with_form_feeds_before():
    """
    Test case:  Fenced Code blocks preceeded by form feeds.
    """

    # Arrange
    source_markdown = """ \u000C```python
abc"""
    expected_tokens = [
        "[para(1,2): \u000C\n]",
        "[text(1,2):```python\nabc::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>```python
abc</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


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
@pytest.mark.skip
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
        "[text(2,3):abc\n\t```:]",
        "[end-fcode-block::::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code class="language-python">abc
\t```
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
@pytest.mark.skip
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
