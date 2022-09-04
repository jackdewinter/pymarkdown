"""
https://github.github.com/gfm/#textual-content
"""

from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_textual_content_extra_1():
    """
    Test case extra 1: special characters should be escaped
    """

    # Arrange
    source_markdown = """each\bof\athese\x02should\x03be\x03escaped\x05!"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):each\x05\bof\x05\athese\x05\x02should\x05\x03be\x05\x03escaped\x05\x05!:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>each\bof\athese\x02should\x03be\x03escaped\x05!</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_2():
    """
    Test case extra 2: Alert character (\a or replacement character) by itself.
    """

    # Arrange
    source_markdown = """this character \a is me"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this character \x05\a is me:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this character \a is me</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_3():
    """
    Test case extra 3: Multiple alert characters (\a or replacement character).
    """

    # Arrange
    source_markdown = """this character \a is me \a or me"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this character \x05\a is me \x05\a or me:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this character \a is me \a or me</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_4():
    """
    Test case extra 4: Multiple alert characters and actual replacements
    """

    # Arrange
    source_markdown = """\a&\a&\a"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\x05\a\a&\a&amp;\a\x05\a\a&\a&amp;\a\x05\a:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\a&amp;\a&amp;\a</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_5():
    """
    Test case extra 5: Multiple alert characters and actual replacements in atx
    """

    # Arrange
    source_markdown = """# \a&\a&\a"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):\x05\a\a&\a&amp;\a\x05\a\a&\a&amp;\a\x05\a: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>\a&amp;\a&amp;\a</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_6():
    """
    Test case extra 6: Multiple alert characters and actual replacements in setext
    """

    # Arrange
    source_markdown = """\a&\a&\a
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\x05\a\a&\a&amp;\a\x05\a\a&\a&amp;\a\x05\a:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>\a&amp;\a&amp;\a</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_7():
    """
    Test case extra 7: Multiple alert characters and actual replacements
    """

    # Arrange
    source_markdown = """`\a<\a>\a`"""
    expected_tokens = [
        "[para(1,1):]",
        "[icode-span(1,1):\x05\a\a<\a&lt;\a\x05\a\a>\a&gt;\a\x05\a:`::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><code>\a&lt;\a&gt;\a</code></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_8():
    """
    Test case extra 8: Single backspace should be escaped
    """

    # Arrange
    source_markdown = """this character \b is me"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this character \x05\b is me:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this character \b is me</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_9():
    """
    Test case extra 9: Multiple backspace characters
    """

    # Arrange
    source_markdown = """this character \b is me \b or me"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this character \x05\b is me \x05\b or me:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this character \b is me \b or me</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_10():
    """
    Test case extra 10: Multiple backspace characters and actual backspaces
    """

    # Arrange
    source_markdown = """\b\\`\b\\`\b"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\x05\b\\\b`\x05\b\\\b`\x05\b:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\b`\b`\b</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_11():
    """
    Test case extra 11: Multiple backspace characters and actual backspaces in atx
    """

    # Arrange
    source_markdown = """# \b\\`\b\\`\b"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):\x05\b\\\b`\x05\b\\\b`\x05\b: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>\b`\b`\b</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_12():
    """
    Test case extra 12: Multiple backspace characters and actual backspaces in setext
    """

    # Arrange
    source_markdown = """\b\\`\b\\`\b
---"""
    expected_tokens = [
        "[setext(2,1):-:3::(1,1)]",
        "[text(1,1):\x05\b\\\b`\x05\b\\\b`\x05\b:]",
        "[end-setext::]",
    ]
    expected_gfm = """<h2>\b`\b`\b</h2>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_13():
    """
    Test case extra 13: Multiple backslash characters and actual backspaces in link
    """

    # Arrange
    source_markdown = """[foo\\*bar](/bar\\* "ti\\*tle")"""
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/bar*:ti*tle:/bar\\*:ti\\*tle::foo\\*bar:False:":: :]',
        "[text(1,2):foo\\\b*bar:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/bar*" title="ti*tle">foo*bar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_14():
    """
    Test case extra 14: Multiple backspace characters and actual backspaces in almost link
    """

    # Arrange
    source_markdown = """[foo\bbar](/bar\b "ti\btle")"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foo\x05\bbar:]",
        "[text(1,9):]:]",
        '[text(1,10):(/bar\x05\b \a"\a&quot;\ati\x05\btle\a"\a&quot;\a):]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foo\bbar](/bar\b &quot;ti\btle&quot;)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_15():
    """
    Test case extra 15: Backspace character and actual backspaces in link label
    """

    # Arrange
    source_markdown = """[foo\bbar](/bar "title")"""
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/bar:title::::foo\x05\bbar:False:":: :]',
        "[text(1,2):foo\x05\bbar:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/bar" title="title">foo\bbar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_16():
    """
    Test case extra 16: Backspace character and actual backspaces in link uri
    """

    # Arrange
    source_markdown = """[foobar](/b\bar "title")"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):[:]",
        "[text(1,2):foobar:]",
        "[text(1,8):]:]",
        '[text(1,9):(/b\x05\bar \a"\a&quot;\atitle\a"\a&quot;\a):]',
        "[end-para:::True]",
    ]
    expected_gfm = """<p>[foobar](/b\bar &quot;title&quot;)</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_17():
    """
    Test case extra 17: Backspace character and actual backspaces in link title
    """

    # Arrange
    source_markdown = """[foobar](/bar "ti\btle")"""
    expected_tokens = [
        "[para(1,1):]",
        '[link(1,1):inline:/bar:ti\btle::::foobar:False:":: :]',
        "[text(1,2):foobar:]",
        "[end-link::]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p><a href="/bar" title="ti\btle">foobar</a></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_18():
    """
    Test case extra 18: Backspace character and actual backspaces in LRD
    """

    # Arrange
    source_markdown = """before[fo\bo]after

[fo\bo]: /bar "ti\\*\btle"
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):before:]",
        "[link(1,7):shortcut:/bar:ti*\btle::::fo\x05\bo:False::::]",
        "[text(1,8):fo\x05\bo:]",
        "[end-link::]",
        "[text(1,13):after:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        '[link-ref-def(3,1):True::fo\bo:: :/bar:: :ti*\btle:"ti\\*\btle":]',
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>before<a href="/bar" title="ti*\btle">fo\bo</a>after</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_19():
    """
    Test case extra 19: Backspace character and actual backspaces in fenced block info
    """

    # Arrange
    source_markdown = """``` foo\b\\+\bbar
foo
```"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:foo\b+\bbar:foo\b\\+\bbar:::: ]",
        "[text(2,1):foo:]",
        "[end-fcode-block:::3:False]",
    ]
    expected_gfm = """<pre><code class="language-foo\b+\bbar">foo\n</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_20():
    """
    Test case extra 20: Whitespace split character
    NOTE: Since this is only appears not-naturally in whitespace, cannot come
          up with embedded test case.
    """

    # Arrange
    source_markdown = """this character \x02 is me"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this character \x05\x02 is me:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this character \x02 is me</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_21():
    """
    Test case extra 21: NOOP character
    NOTE: Since this is only appears not-naturally in whitespace, cannot come
          up with embedded test case.
    """

    # Arrange
    source_markdown = """this character \x03 is me"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this character \x05\x03 is me:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this character \x03 is me</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_23():
    """
    Test case extra 23: Escape character
    """

    # Arrange
    source_markdown = """this character \x05 is me"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this character \x05\x05 is me:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>this character \x05 is me</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_textual_content_extra_24():
    """
    Test case extra 24: all special characters, one after the other
    """

    # Arrange
    source_markdown = """\b\a\x02\x03\x05"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):\x05\b\x05\a\x05\x02\x05\x03\x05\x05:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>\b\a\x02\x03\x05</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
