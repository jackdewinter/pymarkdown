"""
https://github.github.com/gfm/#atx-headings
"""
from pymarkdown.tokenized_markdown import TokenizedMarkdown

from .utils import assert_if_lists_different


def test_atx_headings_032():
    """
    Test case 032:  Simple headings
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """# foo
## foo
### foo
#### foo
##### foo
###### foo"""
    expected_tokens = [
        "[atx:1:foo:: ::]",
        "[atx:2:foo:: ::]",
        "[atx:3:foo:: ::]",
        "[atx:4:foo:: ::]",
        "[atx:5:foo:: ::]",
        "[atx:6:foo:: ::]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_033():
    """
    Test case 033:  More than six # characters is not a heading:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """####### foo"""
    expected_tokens = ["[para:]", "[text:####### foo:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_034():
    """
    Test case 034:  At least one space is required between the # characters and the heading’s contents, unless the heading is empty.
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
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

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_035():
    """
    Test case 035:  this is not a heading, because the first # is escaped:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """\\## foo"""
    expected_tokens = ["[para:]", "[text:\\## foo:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_036():
    """
    Test case 036:  Contents are parsed as inlines:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """# foo *bar* \\*baz\\*"""
    expected_tokens = ["[atx:1:foo *bar* \\*baz\\*:: ::]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    # TODO Expect this to fail when inline code blocks implemented
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_037():
    """
    Test case 037:  Leading and trailing whitespace is ignored in parsing inline content:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """#                  foo                     """
    expected_tokens = ["[atx:1:foo                     ::                  ::]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_038():
    """
    Test case 038:  One to three spaces indentation are allowed:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """ ### foo
  ## foo
   # foo"""
    expected_tokens = ["[atx:3:foo: : ::]", "[atx:2:foo:  : ::]", "[atx:1:foo:   : ::]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_039():
    """
    Test case 039:  (part a) Four spaces are too much:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """    # foo"""
    expected_tokens = ["[icode-block:    ]", "[text:# foo:]", "[end-icode-block]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_040():
    """
    Test case 040:  (part b) Four spaces are too much:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """foo
    # bar"""
    expected_tokens = ["[para:]", "[text:foo\n    # bar:]", "[end-para]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_041():
    """
    Test case 041:  A closing sequence of # characters is optional:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """## foo ##
  ###   bar    ###"""
    expected_tokens = ["[atx:2:foo:: :: ]", "[atx:3:bar:  :   ::    ]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_042():
    """
    Test case 042:  It need not be the same length as the opening sequence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """# foo ##################################
##### foo ##"""
    expected_tokens = ["[atx:1:foo:: :: ]", "[atx:5:foo:: :: ]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_043():
    """
    Test case 043:  Spaces are allowed after the closing sequence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """### foo ###     """
    expected_tokens = ["[atx:3:foo:: :     : ]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_044():
    """
    Test case 044:  A sequence of # characters with anything but spaces following it is not a closing sequence, but counts as part of the contents of the heading:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """### foo ### b"""
    expected_tokens = ["[atx:3:foo ### b:: ::]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_045():
    """
    Test case 045:  The closing sequence must be preceded by a space:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """# foo#"""
    expected_tokens = ["[atx:1:foo#:: ::]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_046():
    """
    Test case 046:  Backslash-escaped # characters do not count as part of the closing sequence:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """### foo \\###
## foo #\\##
# foo \\#"""
    expected_tokens = [
        "[atx:3:foo \\###:: ::]",
        "[atx:2:foo #\\##:: ::]",
        "[atx:1:foo \\#:: ::]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_047():
    """
    Test case 047:  (part a) ATX headings need not be separated from surrounding content by blank lines, and they can interrupt paragraphs:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """****
## foo
****"""
    expected_tokens = ["[tbreak:*::****]", "[atx:2:foo:: ::]", "[tbreak:*::****]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


def test_atx_headings_048():
    """
    Test case 048:  (part b) ATX headings need not be separated from surrounding content by blank lines, and they can interrupt paragraphs:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """Foo bar
# baz
Bar foo"""
    expected_tokens = [
        "[para:]",
        "[text:Foo bar:]",
        "[end-para]",
        "[atx:1:baz:: ::]",
        "[para:]",
        "[text:Bar foo:]",
        "[end-para]",
    ]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)


# pylint: disable=trailing-whitespace
def test_atx_headings_049():
    """
    Test case 049:  ATX headings can be empty:
    """

    # Arrange
    tokenizer = TokenizedMarkdown()
    source_markdown = """## 
#
### ###"""
    expected_tokens = ["[atx:2::: ::]", "[atx:1:::::]", "[atx:3::: ::]"]

    # Act
    actual_tokens = tokenizer.transform(source_markdown)

    # Assert
    assert_if_lists_different(expected_tokens, actual_tokens)
