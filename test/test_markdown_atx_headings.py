"""
https://github.github.com/gfm/#atx-headings
"""
import pytest

from pymarkdown.tokenized_markdown import TokenizedMarkdown
from pymarkdown.transform_to_gfm import TransformToGfm

from .utils import assert_if_lists_different, assert_if_strings_different


@pytest.mark.gfm
def test_atx_headings_032():
    """
    Test case 032:  Simple headings
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """# foo
## foo
### foo
#### foo
##### foo
###### foo"""
    expected_tokens = [
        "[atx:1:0:]",
        "[text:foo: ]",
        "[end-atx::]",
        "[atx:2:0:]",
        "[text:foo: ]",
        "[end-atx::]",
        "[atx:3:0:]",
        "[text:foo: ]",
        "[end-atx::]",
        "[atx:4:0:]",
        "[text:foo: ]",
        "[end-atx::]",
        "[atx:5:0:]",
        "[text:foo: ]",
        "[end-atx::]",
        "[atx:6:0:]",
        "[text:foo: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h1>foo</h1>
<h2>foo</h2>
<h3>foo</h3>
<h4>foo</h4>
<h5>foo</h5>
<h6>foo</h6>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_033():
    """
    Test case 033:  More than six # characters is not a heading:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """####### foo"""
    expected_tokens = ["[para:]", "[text:####### foo:]", "[end-para]"]
    expected_gfm = """<p>####### foo</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_034():
    """
    Test case 034:  At least one space is required between the # characters and the heading’s contents, unless the heading is empty.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """#5 bolt

#hashtag"""
    expected_tokens = [
        "[para:]",
        "[text:#5 bolt:]",
        "[end-para]",
        "[BLANK:]",
        "[para:]",
        "[text:#hashtag:]",
        "[end-para]",
    ]
    expected_gfm = """<p>#5 bolt</p>
<p>#hashtag</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_035():
    """
    Test case 035:  this is not a heading, because the first # is escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """\\## foo"""
    expected_tokens = ["[para:]", "[text:## foo:]", "[end-para]"]
    expected_gfm = """<p>## foo</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_036():
    """
    Test case 036:  Contents are parsed as inlines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """# foo *bar* \\*baz\\*"""
    expected_tokens = ["[atx:1:0:]", "[text:foo *bar* *baz*: ]", "[end-atx::]"]
    expected_gfm = """<h1>foo *bar* *baz*</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    # TODO Expect this to fail when inline emphasis implemented
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_037():
    """
    Test case 037:  Leading and trailing whitespace is ignored in parsing inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """#                  foo                     """
    expected_tokens = [
        "[atx:1:0:]",
        "[text:foo:                  ]",
        "[end-atx:                     :]",
    ]
    expected_gfm = """<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_038():
    """
    Test case 038:  One to three spaces indentation are allowed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """ ### foo
  ## foo
   # foo"""
    expected_tokens = [
        "[atx:3:0: ]",
        "[text:foo: ]",
        "[end-atx::]",
        "[atx:2:0:  ]",
        "[text:foo: ]",
        "[end-atx::]",
        "[atx:1:0:   ]",
        "[text:foo: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h3>foo</h3>
<h2>foo</h2>
<h1>foo</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_039():
    """
    Test case 039:  (part a) Four spaces are too much:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """    # foo"""
    expected_tokens = ["[icode-block:    ]", "[text:# foo:]", "[end-icode-block]"]
    expected_gfm = """<pre><code># foo
</code></pre>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_040():
    """
    Test case 040:  (part b) Four spaces are too much:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """foo
    # bar"""
    expected_tokens = ["[para:\n    ]", "[text:foo\n# bar::\n]", "[end-para]"]
    expected_gfm = """<p>foo
# bar</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_041():
    """
    Test case 041:  A closing sequence of # characters is optional:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """## foo ##
  ###   bar    ###"""
    expected_tokens = [
        "[atx:2:2:]",
        "[text:foo: ]",
        "[end-atx:: ]",
        "[atx:3:3:  ]",
        "[text:bar:   ]",
        "[end-atx::    ]",
    ]
    expected_gfm = """<h2>foo</h2>
<h3>bar</h3>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_042():
    """
    Test case 042:  It need not be the same length as the opening sequence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """# foo ##################################
##### foo ##"""
    expected_tokens = [
        "[atx:1:34:]",
        "[text:foo: ]",
        "[end-atx:: ]",
        "[atx:5:2:]",
        "[text:foo: ]",
        "[end-atx:: ]",
    ]
    expected_gfm = """<h1>foo</h1>
<h5>foo</h5>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_043():
    """
    Test case 043:  Spaces are allowed after the closing sequence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """### foo ###     """
    expected_tokens = ["[atx:3:3:]", "[text:foo: ]", "[end-atx:     : ]"]
    expected_gfm = """<h3>foo</h3>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_044():
    """
    Test case 044:  A sequence of # characters with anything but spaces following it is not a closing sequence, but counts as part of the contents of the heading:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """### foo ### b"""
    expected_tokens = ["[atx:3:0:]", "[text:foo ### b: ]", "[end-atx::]"]
    expected_gfm = """<h3>foo ### b</h3>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_045():
    """
    Test case 045:  The closing sequence must be preceded by a space:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """# foo#"""
    expected_tokens = ["[atx:1:0:]", "[text:foo#: ]", "[end-atx::]"]
    expected_gfm = """<h1>foo#</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_046():
    """
    Test case 046:  Backslash-escaped # characters do not count as part of the closing sequence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """### foo \\###
## foo #\\##
# foo \\#"""
    expected_tokens = [
        "[atx:3:0:]",
        "[text:foo ###: ]",
        "[end-atx::]",
        "[atx:2:0:]",
        "[text:foo ###: ]",
        "[end-atx::]",
        "[atx:1:0:]",
        "[text:foo #: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h3>foo ###</h3>
<h2>foo ###</h2>
<h1>foo #</h1>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_047():
    """
    Test case 047:  (part a) ATX headings need not be separated from surrounding content by blank lines, and they can interrupt paragraphs:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """****
## foo
****"""
    expected_tokens = [
        "[tbreak:*::****]",
        "[atx:2:0:]",
        "[text:foo: ]",
        "[end-atx::]",
        "[tbreak:*::****]",
    ]
    expected_gfm = """<hr />
<h2>foo</h2>
<hr />"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_048():
    """
    Test case 048:  (part b) ATX headings need not be separated from surrounding content by blank lines, and they can interrupt paragraphs:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """Foo bar
# baz
Bar foo"""
    expected_tokens = [
        "[para:]",
        "[text:Foo bar:]",
        "[end-para]",
        "[atx:1:0:]",
        "[text:baz: ]",
        "[end-atx::]",
        "[para:]",
        "[text:Bar foo:]",
        "[end-para]",
    ]
    expected_gfm = """<p>Foo bar</p>
<h1>baz</h1>
<p>Bar foo</p>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_049():
    """
    Test case 049:  ATX headings can be empty:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """##\a
#
### ###""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[atx:2:0:]",
        "[text:: ]",
        "[end-atx::]",
        "[atx:1:0:]",
        "[text::]",
        "[end-atx::]",
        "[atx:3:3:]",
        "[text:: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2></h2>
<h1></h1>
<h3></h3>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)


@pytest.mark.gfm
def test_atx_headings_extra_1():
    """
    Test case extra 1:  ATX headings with a code span.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    transformer = TransformToGfm()
    source_markdown = """## this is a ``fun`` day"""
    expected_tokens = [
        "[atx:2:0:]",
        "[text:this is a : ]",
        "[icode-span:fun]",
        "[text: day:]",
        "[end-atx::]",
    ]
    expected_gfm = """<h2>this is a <code>fun</code> day</h2>"""

    # Act
    actual_tokens = tokenizer.transform(source_markdown)
    actual_gfm = transformer.transform(actual_tokens)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
    assert_if_strings_different(expected_gfm, actual_gfm)
