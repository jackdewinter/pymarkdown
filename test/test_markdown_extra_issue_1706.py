"""
Extra tests.

https://github.com/jackdewinter/pymarkdown/issues/1706

"""

from test.markdown_scanner import MarkdownScanner
from test.pytest_execute import ExpectedResults
from test.utils import act_and_assert, create_temporary_markdown_file

TABLES_CONFIG_MAP = {"extensions": {"markdown-tables": {"enabled": True}}}
# front_matter_config_map = {"extensions": {"front-matter": {"enabled": True}}}
EXTENSION_ENABLE_FRONT_MATTER = "extensions.front-matter.enabled=$!True"


def test_extra_issue_1706_primary() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """# T

- a
    - b | c
"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):T: ]",
        "[end-atx::]",
        "[BLANK(2,1):]",
        "[ulist(3,1):-::2:]",
        "[para(3,3):]",
        "[text(3,3):a:]",
        "[end-para:::True]",
        "[ulist(4,5):-::6:    :]",
        "[para(4,7):]",
        "[text(4,7):b | c:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<h1>T</h1>
<ul>
<li>a
<ul>
<li>b | c</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=TABLES_CONFIG_MAP
    )


def test_extra_issue_1706_a() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """- a / - b | c
"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):]",
        "[text(1,3):a / - b | c:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>\n<li>a / - b | c</li>\n</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=TABLES_CONFIG_MAP
    )


def test_extra_issue_1706_b() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """a / - b \\|
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a / - b \\\b|:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = """<p>a / - b |</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=TABLES_CONFIG_MAP
    )


def test_extra_issue_1706_c() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """a / - b `X | Y` c
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a / - b :]",
        "[icode-span(1,9):X | Y:`::]",
        "[text(1,16): c:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = """<p>a / - b <code>X | Y</code> c</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=TABLES_CONFIG_MAP
    )


def test_extra_issue_1706_d() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """1. a / 1. b | c
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):a / 1. b | c:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>\n<li>a / 1. b | c</li>\n</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=TABLES_CONFIG_MAP
    )


def test_extra_issue_1706_e() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """> - a / > - b | c
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[ulist(1,3):-::4:]",
        "[para(1,5):]",
        "[text(1,5):a / \a>\a&gt;\a - b | c:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
        "[end-block-quote:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = (
        """<blockquote>\n<ul>\n<li>a / &gt; - b | c</li>\n</ul>\n</blockquote>"""
    )

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=TABLES_CONFIG_MAP
    )


def test_extra_issue_1706_f() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """a / - b | c
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a / - b | c:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = """<p>a / - b | c</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=TABLES_CONFIG_MAP
    )


def test_extra_issue_1706_g() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """a
- b | c
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a:]",
        "[end-para:::True]",
        "[ulist(2,1):-::2::]",
        "[para(2,3):]",
        "[text(2,3):b | c:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<p>a</p>\n<ul>\n<li>b | c</li>\n</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=TABLES_CONFIG_MAP
    )


def test_extra_issue_1706_h() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """a / - b &#124; c
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a / - b \a&#124;\a|\a c:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = """<p>a / - b | c</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=TABLES_CONFIG_MAP
    )


def test_extra_issue_1706_i() -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """a / - b | c
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):a / - b | c:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
    ]
    expected_gfm = """<p>a / - b | c</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens, config_map=None)


def test_extra_issue_1706_secondary_scan(scanner_default: MarkdownScanner) -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """---
test: assert
---
"""

    with create_temporary_markdown_file(source_markdown) as file_name:
        expected_results = ExpectedResults(
            return_code=1,
            expected_error=f"""

Unexpected Error(BadTokenizationError): An unhandled error occurred processing the '{file_name}' file.
""",
        )

        # Act
        supplied_arguments = ["--set", EXTENSION_ENABLE_FRONT_MATTER, "scan", file_name]
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)


def test_extra_issue_1706_secondary_fix(scanner_default: MarkdownScanner) -> None:
    """
    TBD
    """

    # Arrange
    source_markdown = """---
test: assert
---
"""

    with create_temporary_markdown_file(source_markdown) as file_name:
        expected_results = ExpectedResults(
            return_code=1,
            expected_error=f"""

Unexpected Error(BadTokenizationError): An unhandled error occurred processing the '{file_name}' file.
""",
        )

        # Act
        supplied_arguments = ["--set", EXTENSION_ENABLE_FRONT_MATTER, "fix", file_name]
        execute_results = scanner_default.invoke_main(arguments=supplied_arguments)

    # Assert
    execute_results.assert_results(expected_results=expected_results)
