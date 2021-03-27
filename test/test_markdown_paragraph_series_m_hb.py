"""
https://github.github.com/gfm/#paragraph
"""
import pytest

from .utils import act_and_assert

# pylint: disable=too-many-lines


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_nl_hb():
    """
    Test case:  Ordered list newline html block
    was:        test_list_blocks_256k
    """

    # Arrange
    source_markdown = """1.
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[html-block(2,1)]",
        "[text(2,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
<script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_nl_all_i3_hb():
    """
    Test case:  Ordered list newline (all indented) html block
    """

    # Arrange
    source_markdown = """1.
   <script>
   foo
   </script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   ]",
        "[BLANK(1,3):]",
        "[html-block(2,4)]",
        "[text(2,4):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<script>
foo
</script>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_nl_i2_hb():
    """
    Test case:  Ordered list newline indent of 2 html block
    was:        test_list_blocks_256kxa
    """

    # Arrange
    source_markdown = """1.
  <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[html-block(2,1)]",
        "[text(2,3):<script>\nfoo\n</script>:  ]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol>
  <script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_nl_i3_hb():
    """
    Test case:  Ordered list newline indent of 3 html block
    was:        test_list_blocks_256kxb
    """

    # Arrange
    source_markdown = """1.
   <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[html-block(2,4)]",
        "[text(2,4):<script>:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[para(3,1):\n]",
        "[text(3,1):foo\n::\n]",
        "[raw-html(4,1):/script]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<script>
</li>
</ol>
<p>foo
</script></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_t_nl_hb():
    """
    Test case:  Ordered list text newline html block
    was:        test_list_blocks_256ka
    """

    # Arrange
    source_markdown = """1.  abc
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:4:]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[html-block(2,1)]",
        "[text(2,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
<script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_t_nl_all_i4_hb():
    """
    Test case:  Ordered list text newline html block
    """

    # Arrange
    source_markdown = """1.  abc
    <script>
    foo
    </script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:4::    \n    \n    ]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::False]",
        "[html-block(2,5)]",
        "[text(2,5):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<script>
foo
</script>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_t_nl_i3_hb():
    """
    Test case:  Ordered list text newline indent of 3 html block
    was:        test_list_blocks_256kaa
    """

    # Arrange
    source_markdown = """1.  abc
   <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:4:]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[html-block(2,1)]",
        "[text(2,4):<script>\nfoo\n</script>:   ]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc</li>
</ol>
   <script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_t_nl_i4_hb():
    """
    Test case:  Ordered list text newline indent of 4 html block
    was:        test_list_blocks_256kab
    """

    # Arrange
    source_markdown = """1.  abc
    <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:4::    ]",
        "[para(1,5):]",
        "[text(1,5):abc:]",
        "[end-para:::False]",
        "[html-block(2,5)]",
        "[text(2,5):<script>:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[para(3,1):\n]",
        "[text(3,1):foo\n::\n]",
        "[raw-html(4,1):/script]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<script>
</li>
</ol>
<p>foo
</script></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_ol_nl_hb():
    """
    Test case:  Ordered list x2 newline html block
    """

    # Arrange
    source_markdown = """1. 1.
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[BLANK(1,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(2,1)]",
        "[text(2,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_ol_nl_all_i6_hb():
    """
    Test case:  Ordered list x2 newline (all indented) html block
    """

    # Arrange
    source_markdown = """1. 1.
      <script>
      foo
      </script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :      \n      \n      ]",
        "[BLANK(1,6):]",
        "[html-block(2,7)]",
        "[text(2,7):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>
<script>
foo
</script>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_ol_t_nl_hb():
    """
    Test case:  Ordered list x2 text newline html block
    was:        test_list_blocks_256kb
    """

    # Arrange
    source_markdown = """1. 1. abc
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(2,1)]",
        "[text(2,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc</li>
</ol>
</li>
</ol>
<script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_ol_t_nl_all_i6_hb():
    """
    Test case:  Ordered list x2 text newline html block
    """

    # Arrange
    source_markdown = """1. 1. abc
      <script>
      foo
      </script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[olist(1,4):.:1:6:   :      \n      \n      ]",
        "[para(1,7):]",
        "[text(1,7):abc:]",
        "[end-para:::False]",
        "[html-block(2,7)]",
        "[text(2,7):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>abc
<script>
foo
</script>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_nl_i3_ol_nl_hb():
    """
    Test case:  Ordered list newline indent of 3 ordered list newline html block
    """

    # Arrange
    source_markdown = """1.
   1.
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
<script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_t_nl_i3_ol_nl_hb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline html block
    """

    # Arrange
    source_markdown = """1. abc
   1.
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\n1.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
<script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ul_t_nl_i2_ul_nl_hb():
    """
    Test case:  Unordered list text newline indent of 2 unordered list newline html block
    """

    # Arrange
    source_markdown = """- abc
  -
<script>
foo
</script>
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::]",
        "[end-ulist:::True]",
        "[html-block(3,1)]",
        "[text(3,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>
<script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ul_t_nl_i2_ulb_nl_hb():
    """
    Test case:  Unordered list text newline indent of 2 unordered list (b) newline html block
    """

    # Arrange
    source_markdown = """- abc
  *
<script>
foo
</script>
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n]",
        "[text(1,3):abc\n::\n]",
        "[text(2,1):*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[html-block(3,1)]",
        "[text(3,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ul>
<li>abc
*</li>
</ul>
<script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_nl_i3_ol_t_nl_hb():
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline html block
    """

    # Arrange
    source_markdown = """1.
   1. def
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def</li>
</ol>
</li>
</ol>
<script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_t_nl_i3_ol_t_nl_hb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline html block
    was:        test_list_blocks_256kc
    """

    # Arrange
    source_markdown = """1. abc
   1. def
<script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,1):<script>\nfoo\n</script>:]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
</li>
</ol>
<script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_nl_i3_ol_nl_i2_hb():
    """
    Test case:  Ordered list newline indent of 3 ordered list newline indent of 2 html block
    """

    # Arrange
    source_markdown = """1.
   1.
  <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,3):<script>\nfoo\n</script>:  ]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
</li>
</ol>
  <script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_t_nl_i3_ol_nl_i2_hb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline indent of 2 html block
    """

    # Arrange
    source_markdown = """1. abc
   1.
  <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\n1.::\n]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,3):<script>\nfoo\n</script>:  ]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.</li>
</ol>
  <script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ul_t_nl_i2_ul_nl_i1_hb():
    """
    Test case:  Unordered list text newline indent of 2 unordered list newline indent of 1 html block
    """

    # Arrange
    source_markdown = """- abc
  -
 <script>
foo
</script>
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::]",
        "[end-ulist:::True]",
        "[html-block(3,1)]",
        "[text(3,2):<script>\nfoo\n</script>: ]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
</li>
</ul>
 <script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ul_t_nl_i2_ulb_nl_i1_hb():
    """
    Test case:  Unordered list text newline indent of 2 unordered list (b) newline indent of 1 html block
    """

    # Arrange
    source_markdown = """- abc
  *
 <script>
foo
</script>
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  ]",
        "[para(1,3):\n]",
        "[text(1,3):abc\n::\n]",
        "[text(2,1):*:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[html-block(3,1)]",
        "[text(3,2):<script>\nfoo\n</script>: ]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ul>
<li>abc
*</li>
</ul>
 <script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_nl_i3_ol_t_nl_i2_hb():
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline indent of 2 html block
    """

    # Arrange
    source_markdown = """1.
   1. def
  <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,3):<script>\nfoo\n</script>:  ]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def</li>
</ol>
</li>
</ol>
  <script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_t_nl_i3_ol_t_nl_i2_hb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline indent of 2 html block
    was:        test_list_blocks_256kd
    """

    # Arrange
    source_markdown = """1. abc
   1. def
  <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[end-olist:::True]",
        "[end-olist:::True]",
        "[html-block(3,1)]",
        "[text(3,3):<script>\nfoo\n</script>:  ]",
        "[end-html-block:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
</li>
</ol>
  <script>
foo
</script>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_nl_i3_ol_nl_i3_hb():
    """
    Test case:  Ordered list newline indent of 3 ordered list newline indent of 2 html block
    """

    # Arrange
    source_markdown = """1.
   1.
   <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   ]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   ]",
        "[BLANK(2,6):]",
        "[end-olist:::True]",
        "[html-block(3,4)]",
        "[text(3,4):<script>:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):\n]",
        "[text(4,1):foo\n::\n]",
        "[raw-html(5,1):/script]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li></li>
</ol>
<script>
</li>
</ol>
<p>foo
</script></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_t_nl_i3_ol_nl_i3_hb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list newline indent of 2 html block
    """

    # Arrange
    source_markdown = """1. abc
   1.
   <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[para(1,4):\n]",
        "[text(1,4):abc\n1.::\n]",
        "[end-para:::False]",
        "[html-block(3,4)]",
        "[text(3,4):<script>:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):\n]",
        "[text(4,1):foo\n::\n]",
        "[raw-html(5,1):/script]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
1.
<script>
</li>
</ol>
<p>foo
</script></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ul_t_nl_i2_ul_nl_i2_hb():
    """
    Test case:  Unordered list text newline indent of 2 unordered list newline indent of 2 html block
    """

    # Arrange
    source_markdown = """- abc
  -
  <script>
foo
</script>
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[setext(2,3):-:1::(1,3)]",
        "[text(1,3):abc:]",
        "[end-setext::]",
        "[html-block(3,3)]",
        "[text(3,3):<script>:]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
        "[para(4,1):\n]",
        "[text(4,1):foo\n::\n]",
        "[raw-html(5,1):/script]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ul>
<li>
<h2>abc</h2>
<script>
</li>
</ul>
<p>foo
</script></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ul_t_nl_i2_ulb_nl_i2_hb():
    """
    Test case:  Unordered list text newline indent of 2 unordered list (b) newline indent of 2 html block
    """

    # Arrange
    source_markdown = """- abc
  *
  <script>
foo
</script>
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  ]",
        "[para(1,3):\n]",
        "[text(1,3):abc\n::\n]",
        "[text(2,1):*:]",
        "[end-para:::False]",
        "[html-block(3,3)]",
        "[text(3,3):<script>:]",
        "[end-html-block:::True]",
        "[end-ulist:::True]",
        "[para(4,1):\n]",
        "[text(4,1):foo\n::\n]",
        "[raw-html(5,1):/script]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ul>
<li>abc
*
<script>
</li>
</ul>
<p>foo
</script></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_nl_i3_ol_t_nl_i3_hb():
    """
    Test case:  Ordered list newline indent of 3 ordered list text newline indent of 2 html block
    """

    # Arrange
    source_markdown = """1.
   1. def
   <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[olist(2,4):.:1:6:   :   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,4)]",
        "[text(3,4):<script>:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):\n]",
        "[text(4,1):foo\n::\n]",
        "[raw-html(5,1):/script]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>
<ol>
<li>def</li>
</ol>
<script>
</li>
</ol>
<p>foo
</script></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_paragraph_series_m_hb_ol_t_nl_i3_ol_t_nl_i3_hb():
    """
    Test case:  Ordered list text newline indent of 3 ordered list text newline indent of 2 html block
    was:        test_list_blocks_256ke
    """

    # Arrange
    source_markdown = """1. abc
   1. def
   <script>
foo
</script>
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :   ]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::False]",
        "[end-olist:::True]",
        "[html-block(3,4)]",
        "[text(3,4):<script>:]",
        "[end-html-block:::True]",
        "[end-olist:::True]",
        "[para(4,1):\n]",
        "[text(4,1):foo\n::\n]",
        "[raw-html(5,1):/script]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def</li>
</ol>
<script>
</li>
</ol>
<p>foo
</script></p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
