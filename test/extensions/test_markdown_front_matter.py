"""
Tests for the optional front-matter processing
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import act_and_assert

import pytest

from pymarkdown.general.bad_tokenization_error import BadTokenizationError

config_map = {"extensions": {"front-matter": {"enabled": True}}}


@pytest.mark.gfm
def test_front_matter_01():
    """
    Any whitespace before the three - characters causes it not to fire.
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
        "[end-setext::]",
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
        "[front-matter(1,1):---:---:['Title: my document']:{'title': 'my document'}]",
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
        config_map=config_map,
    )


@pytest.mark.gfm
def test_front_matter_06():
    """
    There must be an opening and closing boundary for it to be eligible as front matter.
    Even if there is just a field name and no value.
    """

    # Arrange
    source_markdown = """---
test:
---
"""
    expected_tokens = [
        "[front-matter(1,1):---:---:['test:']:{'test': ''}]",
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
    There must be an opening and closing boundary for it to be eligible as front matter.
    Containing a single line field name and value is normal.
    """

    # Arrange
    source_markdown = """---
test: abc
---
"""
    expected_tokens = [
        "[front-matter(1,1):---:---:['test: abc']:{'test': 'abc'}]",
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
    There must be an opening and closing boundary for it to be eligible as front matter.
    In normal mode, a multiline field value is indicated by a second line that is indented
    by at least 4 characters.
    """

    # Arrange
    source_markdown = """---
test: abc
    def
---
"""
    expected_tokens = [
        "[front-matter(1,1):---:---:['test: abc', '    def']:{'test': 'abc\\ndef'}]",
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
    If a field name does not start a new line or there isn't 4+ spaces at the start,
    the entire header is abandoned.
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
        "[end-setext::]",
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
    A field name can be indented as many as 3 characters, as long as it ends with a ':'.
    """

    # Arrange
    source_markdown = """---
test: abc
   def:
---
"""
    expected_tokens = [
        "[front-matter(1,1):---:---:['test: abc', '   def:']:{'test': 'abc', 'def': ''}]",
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
    A front matter element must contain at least one field name.
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
    A continuation without a field to associate it with is bad.
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


@pytest.mark.gfm
def test_front_matter_13():
    """
    If a blank line is encountered before the end marker, the entire header is
    thrown out.
    """

    # Arrange
    source_markdown = """---

Title: my document
---
---
"""
    expected_tokens = [
        "[tbreak(1,1):-::---]",
        "[BLANK(2,1):]",
        "[setext(4,1):-:3::(3,1)]",
        "[text(3,1):Title: my document:]",
        "[end-setext::]",
        "[tbreak(5,1):-::---]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<hr />
<h2>Title: my document</h2>
<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_14():
    """
    Any whitespace after the three - characters in the start boundary is acceptable.
    """

    # Arrange
    source_markdown = """---\a\a
Title: my document
---
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[front-matter(1,1):---  :---:['Title: my document']:{'title': 'my document'}]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_15():
    """
    Any whitespace after the three - characters in the end boundary is acceptable.
    """

    # Arrange
    source_markdown = """---
Title: my document
---\a\a
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[front-matter(1,1):---:---  :['Title: my document']:{'title': 'my document'}]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_16():
    """
    More than three - characters in the boundary is not acceptable.
    """

    # Arrange
    source_markdown = """----
Title: my document
----
"""
    expected_tokens = [
        "[tbreak(1,1):-::----]",
        "[setext(3,1):-:4::(2,1)]",
        "[text(2,1):Title: my document:]",
        "[end-setext::]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<hr />\n<h2>Title: my document</h2>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_front_matter_17():
    """
    This is an extension of test_front_matter_13. If a blank line is encountered
    before the end marker, but after a field name, the entire header is still thrown out.
    """

    # Arrange
    source_markdown = """---
Title: my document

---
---
"""
    expected_tokens = [
        "[tbreak(1,1):-::---]",
        "[para(2,1):]",
        "[text(2,1):Title: my document:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[tbreak(4,1):-::---]",
        "[tbreak(5,1):-::---]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<hr />
<p>Title: my document</p>
<hr />
<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_18():
    """
    This is an extension of test_front_matter_13/17. If a blank line is encountered
    before the end marker, but after a field name and indented by at least 4 spaces,
    the front matter is still valid.
    """

    # Arrange
    source_markdown = """---
Title: my document
/a/a/a/a
---
---
""".replace(
        "/a", " "
    )
    expected_tokens = [
        "[front-matter(1,1):---:---:['Title: my document', '    ']:{'title': 'my document\\n'}]",
        "[tbreak(5,1):-::---]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_19():
    """
    This is an extension of test_front_matter_18. If a blank line is encountered
    before the end marker, but before a field name and indented by at least 4 spaces,
    the front matter is no longer valid.
    """

    # Arrange
    source_markdown = """---
/a/a/a/a
Title: my document
---
---
""".replace(
        "/a", " "
    )
    expected_tokens = [
        "[tbreak(1,1):-::---]",
        "[BLANK(2,1):    ]",
        "[setext(4,1):-:3::(3,1)]",
        "[text(3,1):Title: my document:]",
        "[end-setext::]",
        "[tbreak(5,1):-::---]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<hr />
<h2>Title: my document</h2>
<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_front_matter_20():
    """
    This is a made up example for testing.  Due to code in the extension handler,
    this will throw an exception when the a header `test` with value `assert` is
    parsed.
    """

    # Arrange
    source_markdown = """---
test: assert
---
"""
    expected_tokens = []
    expected_gfm = ""

    # Act & Assert
    try:
        act_and_assert(
            source_markdown, expected_gfm, expected_tokens, config_map=config_map
        )
        raise AssertionError("An exception should have been thrown before this point.")
    except BadTokenizationError as this_error:
        assert (
            str(this_error) == "An unhandled error occurred processing the document."
        ), f"message={this_error}"


def test_front_matter_21():
    """
    Test to make sure that a properly setup front matter section and enabled
    extension works as intended.

    This function shadows
    test_api_config_with_strict_and_good_extension_initialize
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "pragmas", "extensions_issue_637.md"
    )
    supplied_arguments = [
        "-s",
        "extensions.front-matter.enabled=$!True",
        "scan",
        source_path,
    ]

    expected_return_code = 0
    expected_output = ""
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_front_matter_21a():
    """
    Variance on 21, but with an improperly activated front matter extension.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "pragmas", "extensions_issue_637.md"
    )
    supplied_arguments = [
        "-s",
        "extensions.front-matter.enabled=true",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: MD041: First line in file should be a top level heading "
        + "(first-line-heading,first-line-h1)\n"
        + f"{source_path}:2:1: MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{source_path}:6:1: MD003: Heading style should be consistent throughout the document. "
        + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
        + f"{source_path}:8:1: MD003: Heading style should be consistent throughout the document. "
        + "[Expected: setext; Actual: atx] (heading-style,header-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_front_matter_21b():
    """
    Variance on 21, but with an improperly activated front matter extension.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "pragmas", "extensions_issue_637.md"
    )
    supplied_arguments = [
        "--strict-config",
        "-s",
        "extensions.front-matter.enabled=true",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = ""
    expected_error = """Configuration error ValueError encountered while initializing extensions:
The value for property 'extensions.front-matter.enabled' must be of type 'bool'."""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_front_matter_21c():
    """
    Variance on 21, but with an improperly activated front matter extension.
    """

    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "pragmas", "extensions_issue_637.md"
    )
    supplied_arguments = [
        "--strict-config",
        "-s",
        "extensions.front-matter.enabledd=true",
        "scan",
        source_path,
    ]

    expected_return_code = 1
    expected_output = (
        f"{source_path}:1:1: MD041: First line in file should be a top level heading "
        + "(first-line-heading,first-line-h1)\n"
        + f"{source_path}:2:1: MD022: Headings should be surrounded by blank lines. "
        + "[Expected: 1; Actual: 0; Above] (blanks-around-headings,blanks-around-headers)\n"
        + f"{source_path}:6:1: MD003: Heading style should be consistent throughout the document. "
        + "[Expected: setext; Actual: atx] (heading-style,header-style)\n"
        + f"{source_path}:8:1: MD003: Heading style should be consistent throughout the document. "
        + "[Expected: setext; Actual: atx] (heading-style,header-style)"
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments, suppress_first_line_heading_rule=False
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )
