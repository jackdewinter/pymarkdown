"""
Tests for the optional front-matter processing
"""
import pytest

from .utils import act_and_assert

config_map = {"extensions": {"front-matter": {"enabled", True}}}


@pytest.mark.gfm
def test_front_matter_01():
    """
    Any whitespace before the at least three - characters causes it not to fire.
    fill in layer - test_thematic_breaks_020
    """

    # Arrange
    source_markdown = """ ---
Title: my document
---
"""
    expected_tokens = [
        "[tbreak(1,2):-: :---]",
        "[setext(3,1):-:3::(2,1)]",
        "[text(2,1):Title: my document:]",
        "[end-setext:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<hr />
<h2>Title: my document</h2>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_02():
    """
    The starting character must be the '-' character, not the other two.
    """

    # Arrange
    source_markdown = """***
Title: my document
***
"""
    expected_tokens = [
        "[tbreak(1,1):*::***]",
        "[para(2,1):]",
        "[text(2,1):Title: my document:]",
        "[end-para:::False]",
        "[tbreak(3,1):*::***]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<hr />
<p>Title: my document</p>
<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_03():
    """
    Everything between the start and end is parsed, but not as part of HTML output.
    """

    # Arrange
    source_markdown = """---
Title: my document
---
---
"""
    expected_tokens = [
        "[front-matter(1,1):---:['Title: my document']:{'Title': ' my document'}]",
        "[tbreak(4,1):-::---]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_04():
    """
    There must be an opening and closing boundary for it to be eligible as front matter.
    """

    # Arrange
    source_markdown = """---
"""
    expected_tokens = ["[tbreak(1,1):-::---]", "[BLANK(2,1):]"]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        show_debug=False,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_front_matter_05():
    """
    There must be an opening and closing boundary for it to be eligible as front matter.
    """

    # Arrange
    source_markdown = """---
test:
"""
    expected_tokens = [
        "[tbreak(1,1):-::---]",
        "[para(2,1):]",
        "[text(2,1):test::]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
    ]
    expected_gfm = """<hr />
<p>test:</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        show_debug=False,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_front_matter_06():
    """
    There must be an opening and closing boundary for it to be eligible as front matter.
    """

    # Arrange
    source_markdown = """---
test:
---
"""
    expected_tokens = [
        "[front-matter(1,1):---:['test:']:{'test': ''}]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_07():
    """
    There must
    """

    # Arrange
    source_markdown = """---
test: abc
---
"""
    expected_tokens = [
        "[front-matter(1,1):---:['test: abc']:{'test': ' abc'}]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_08():
    """
    There must
    """

    # Arrange
    source_markdown = """---
test: abc
    def
---
"""
    expected_tokens = [
        "[front-matter(1,1):---:['test: abc', '    def']:{'test': ' abc\\n    def'}]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_09():
    """
    There must
    """

    # Arrange
    source_markdown = """---
test: abc
   def
---
"""
    expected_tokens = [
        "[tbreak(1,1):-::---]",
        "[setext(4,1):-:3::(2,1)]",
        "[text(2,1):test: abc\ndef::\n   \x02]",
        "[end-setext:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<hr />
<h2>test: abc
def</h2>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_10():
    """
    There must
    """

    # Arrange
    source_markdown = """---
test: abc
   def:
---
"""
    expected_tokens = [
        "[front-matter(1,1):---:['test: abc', '   def:']:{'test': ' abc', 'def': ''}]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_11():
    """
    There must 068
    """

    # Arrange
    source_markdown = """---
---"""
    expected_tokens = ["[tbreak(1,1):-::---]", "[tbreak(2,1):-::---]"]
    expected_gfm = """<hr />
<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_12():
    """
    There must
    """

    # Arrange
    source_markdown = """---
\a\a\a\acontinuation
---""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[tbreak(1,1):-::---]",
        "[icode-block(2,5):    :]",
        "[text(2,5):continuation:]",
        "[end-icode-block:::False]",
        "[tbreak(3,1):-::---]",
    ]
    expected_gfm = """<hr />
<pre><code>continuation
</code></pre>
<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )
