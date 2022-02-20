"""
https://github.github.com/gfm/#atx-headings
"""
from test.utils import act_and_assert

import pytest


@pytest.mark.gfm
def test_atx_headings_032():
    """
    Test case 032:  Simple headings
    """

    # Arrange
    source_markdown = """# foo
## foo
### foo
#### foo
##### foo
###### foo"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):foo: ]",
        "[end-atx::]",
        "[atx(2,1):2:0:]",
        "[text(2,4):foo: ]",
        "[end-atx::]",
        "[atx(3,1):3:0:]",
        "[text(3,5):foo: ]",
        "[end-atx::]",
        "[atx(4,1):4:0:]",
        "[text(4,6):foo: ]",
        "[end-atx::]",
        "[atx(5,1):5:0:]",
        "[text(5,7):foo: ]",
        "[end-atx::]",
        "[atx(6,1):6:0:]",
        "[text(6,8):foo: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>foo</h1>
<h2>foo</h2>
<h3>foo</h3>
<h4>foo</h4>
<h5>foo</h5>
<h6>foo</h6>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_033():
    """
    Test case 033:  More than six # characters is not a heading:
    """

    # Arrange
    source_markdown = """####### foo"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):####### foo:]", "[end-para:::True]"]
    expected_gfm = """<p>####### foo</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_034():
    """
    Test case 034:  At least one space is required between the # characters and the heading’s contents, unless the heading is empty.
    """

    # Arrange
    source_markdown = """#5 bolt

#hashtag"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):#5 bolt:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,1):]",
        "[text(3,1):#hashtag:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>#5 bolt</p>
<p>#hashtag</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_035():
    """
    Test case 035:  this is not a heading, because the first # is escaped:
    """

    # Arrange
    source_markdown = """\\## foo"""
    expected_tokens = ["[para(1,1):]", "[text(1,1):\\\b## foo:]", "[end-para:::True]"]
    expected_gfm = """<p>## foo</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_036():
    """
    Test case 036:  Contents are parsed as inlines:
    """

    # Arrange
    source_markdown = """# foo *bar* \\*baz\\*"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):foo : ]",
        "[emphasis(1,7):1:*]",
        "[text(1,8):bar:]",
        "[end-emphasis(1,11)::]",
        "[text(1,12): \\\b*baz\\\b*:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>foo <em>bar</em> *baz*</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_037():
    """
    Test case 037:  Leading and trailing whitespace is ignored in parsing inline content:
    """

    # Arrange
    source_markdown = """#                  foo                     """
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,20):foo:                  ]",
        "[end-atx:                     :]",
    ]
    expected_gfm = """<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_038():
    """
    Test case 038:  One to three spaces indentation are allowed:
    """

    # Arrange
    source_markdown = """ ### foo
  ## foo
   # foo"""
    expected_tokens = [
        "[atx(1,2):3:0: ]",
        "[text(1,6):foo: ]",
        "[end-atx::]",
        "[atx(2,3):2:0:  ]",
        "[text(2,6):foo: ]",
        "[end-atx::]",
        "[atx(3,4):1:0:   ]",
        "[text(3,6):foo: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h3>foo</h3>
<h2>foo</h2>
<h1>foo</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_039():
    """
    Test case 039:  (part a) Four spaces are too much:
    """

    # Arrange
    source_markdown = """    # foo"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):# foo:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code># foo
</code></pre>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_040():
    """
    Test case 040:  (part b) Four spaces are too much:
    """

    # Arrange
    source_markdown = """foo
    # bar"""
    expected_tokens = [
        "[para(1,1):\n    ]",
        "[text(1,1):foo\n# bar::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>foo
# bar</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_041():
    """
    Test case 041:  A closing sequence of # characters is optional:
    """

    # Arrange
    source_markdown = """## foo ##
  ###   bar    ###"""
    expected_tokens = [
        "[atx(1,1):2:2:]",
        "[text(1,4):foo: ]",
        "[end-atx:: ]",
        "[atx(2,3):3:3:  ]",
        "[text(2,9):bar:   ]",
        "[end-atx::    ]",
    ]
    expected_gfm = """<h2>foo</h2>
<h3>bar</h3>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_042():
    """
    Test case 042:  It need not be the same length as the opening sequence:
    """

    # Arrange
    source_markdown = """# foo ##################################
##### foo ##"""
    expected_tokens = [
        "[atx(1,1):1:34:]",
        "[text(1,3):foo: ]",
        "[end-atx:: ]",
        "[atx(2,1):5:2:]",
        "[text(2,7):foo: ]",
        "[end-atx:: ]",
    ]
    expected_gfm = """<h1>foo</h1>
<h5>foo</h5>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_043():
    """
    Test case 043:  Spaces are allowed after the closing sequence:
    """

    # Arrange
    source_markdown = """### foo ###     """
    expected_tokens = [
        "[atx(1,1):3:3:]",
        "[text(1,5):foo: ]",
        "[end-atx:     : ]",
    ]
    expected_gfm = """<h3>foo</h3>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_044():
    """
    Test case 044:  A sequence of # characters with anything but spaces following it is not a closing sequence, but counts as part of the contents of the heading:
    """

    # Arrange
    source_markdown = """### foo ### b"""
    expected_tokens = [
        "[atx(1,1):3:0:]",
        "[text(1,5):foo ### b: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h3>foo ### b</h3>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_045():
    """
    Test case 045:  The closing sequence must be preceded by a space:
    """

    # Arrange
    source_markdown = """# foo#"""
    expected_tokens = ["[atx(1,1):1:0:]", "[text(1,3):foo#: ]", "[end-atx::]"]
    expected_gfm = """<h1>foo#</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_046():
    """
    Test case 046:  Backslash-escaped # characters do not count as part of the closing sequence:
    """

    # Arrange
    source_markdown = """### foo \\###
## foo #\\##
# foo \\#"""
    expected_tokens = [
        "[atx(1,1):3:0:]",
        "[text(1,5):foo \\\b###: ]",
        "[end-atx::]",
        "[atx(2,1):2:0:]",
        "[text(2,4):foo #\\\b##: ]",
        "[end-atx::]",
        "[atx(3,1):1:0:]",
        "[text(3,3):foo \\\b#: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h3>foo ###</h3>
<h2>foo ###</h2>
<h1>foo #</h1>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_047():
    """
    Test case 047:  (part a) ATX headings need not be separated from surrounding content by blank lines, and they can interrupt paragraphs:
    """

    # Arrange
    source_markdown = """****
## foo
****"""
    expected_tokens = [
        "[tbreak(1,1):*::****]",
        "[atx(2,1):2:0:]",
        "[text(2,4):foo: ]",
        "[end-atx::]",
        "[tbreak(3,1):*::****]",
    ]
    expected_gfm = """<hr />
<h2>foo</h2>
<hr />"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_048():
    """
    Test case 048:  (part b) ATX headings need not be separated from surrounding content by blank lines, and they can interrupt paragraphs:
    """

    # Arrange
    source_markdown = """Foo bar
# baz
Bar foo"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):Foo bar:]",
        "[end-para:::False]",
        "[atx(2,1):1:0:]",
        "[text(2,3):baz: ]",
        "[end-atx::]",
        "[para(3,1):]",
        "[text(3,1):Bar foo:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>Foo bar</p>
<h1>baz</h1>
<p>Bar foo</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_atx_headings_049():
    """
    Test case 049:  ATX headings can be empty:
    """

    # Arrange
    source_markdown = """##\a
#
### ###""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[atx(1,1):2:0:]",
        "[text(1,4):: ]",
        "[end-atx::]",
        "[atx(2,1):1:0:]",
        "[text(2,2)::]",
        "[end-atx::]",
        "[atx(3,1):3:3:]",
        "[text(3,5):: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2></h2>
<h1></h1>
<h3></h3>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)
