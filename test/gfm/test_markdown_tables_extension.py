"""
https://github.github.com/gfm/#tables-extension-
"""

from test.utils import act_and_assert

import pytest

config_map = {"extensions": {"markdown-tables": {"enabled": True}}}


def test_tables_extension_198_disabled() -> None:
    """
    Test case 198:  The delimiter row consists of cells whose only content are hyphens (-), and optionally, a leading or trailing colon (:), or both, to indicate left, right, or center alignment respectively.
    """

    # Arrange
    source_markdown = """| foo | bar |
| --- | --- |
| baz | bim |"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| foo | bar |\n| --- | --- |\n| baz | bim |::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>| foo | bar |\n| --- | --- |\n| baz | bim |</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_tables_extension_198_enabled_x() -> None:
    """
    Test case 198:  The delimiter row consists of cells whose only content are hyphens (-), and optionally, a leading or trailing colon (:), or both, to indicate left, right, or center alignment respectively.

    test_link_reference_definitions_161
    """

    # Arrange
    source_markdown = """| foo | bar |
| --- | --- |
| baz | bim |"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_198_enabled_with_leading_same() -> None:
    """
    variation on 198 with leading spaces, all the same

    test_whitespaces_lrd_with_spaces_before_same
    """

    # Arrange
    source_markdown = """ | foo | bar |
 | --- | --- |
 | baz | bim |"""
    expected_tokens = [
        "[table(1,2)]",
        "[table-header(1,2)]",
        "[table-header-item(1,2)]",
        "[text(1,2):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,2)]",
        "[text(1,2):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,2)]",
        "[table-row(1,2)]",
        "[table-row-item(1,2)]",
        "[text(1,2):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,2)]",
        "[text(1,2):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_198_enabled_with_leading_different() -> None:
    """
    variation on 198 with leading spaces, all different

    test_whitespaces_lrd_with_spaces_before_different
    """

    # Arrange
    source_markdown = """ | foo | bar |
  | --- | --- |
| baz | bim |"""
    expected_tokens = [
        "[table(1,2)]",
        "[table-header(1,2)]",
        "[table-header-item(1,2)]",
        "[text(1,2):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,2)]",
        "[text(1,2):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,2)]",
        "[table-row(1,2)]",
        "[table-row-item(1,2)]",
        "[text(1,2):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,2)]",
        "[text(1,2):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_198_enabled_with_trailing_single() -> None:
    """
    variation on 198 with trailing spaces, all the same
    """

    # Arrange
    source_markdown = """| foo | bar |\a
| --- | --- |\a
| baz | bim |\a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_198_enabled_with_trailing_double() -> None:
    """
    variation on 198 with trailing spaces, all the same
    """

    # Arrange
    source_markdown = """| foo | bar |\a\a
| --- | --- |\a\a
| baz | bim |\a\a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_198_enabled_with_trailing_triple() -> None:
    """
    variation on 198 with trailing spaces, all the same
    """

    # Arrange
    source_markdown = """| foo | bar |\a\a\a
| --- | --- |\a\a\a
| baz | bim |\a\a\a""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_198_enabled_with_empty_columns() -> None:
    """
    variation on 198 with trailing spaces, all the same
    """

    # Arrange
    source_markdown = """| foo | bar |
| --- | --- |
|||"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1)::]",
        "[end-table-row-item:|::False]",
        "[table-row-item(1,1)]",
        "[text(1,1)::]",
        "[end-table-row-item:|::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td></td>
<td></td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_198_enabled_with_internal_tabs() -> None:
    """
    Test case 198:  The delimiter row consists of cells whose only content are hyphens (-), and optionally, a leading or trailing colon (:), or both, to indicate left, right, or center alignment respectively.
    """

    # Arrange
    source_markdown = """|\tfoo |\tbar |
|\t--- |\t--- |
|\tbaz |\tbim |"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_199_disabled() -> None:
    """
    Test case 199:  Cells in one column don’t need to match length, though it’s easier to read if they are. Likewise, use of leading and trailing pipes may be inconsistent:
    """

    # Arrange
    source_markdown = """| abc | defghi |
:-: | -----------:
bar | baz"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| abc | defghi |\n:-: | -----------:\nbar | baz::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>| abc | defghi |\n:-: | -----------:\nbar | baz</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_tables_extension_199_enabled() -> None:
    """
    Test case 199:  Cells in one column don’t need to match length, though it’s easier to read if they are. Likewise, use of leading and trailing pipes may be inconsistent:
    """

    # Arrange
    source_markdown = """| abc | defghi |
:-: | -----------:
bar | baz"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1):center]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1):right]",
        "[text(1,1):defghi:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1):center]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1):right]",
        "[text(1,1):baz:]",
        "[end-table-row-item:::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th align="center">abc</th>
<th align="right">defghi</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">bar</td>
<td align="right">baz</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_199_enabled_all_three() -> None:
    """
    Test case 199:  Cells in one column don’t need to match length, though it’s easier to read if they are. Likewise, use of leading and trailing pipes may be inconsistent:
    """

    # Arrange
    source_markdown = """| abc | defghi | jkl |
| :-: | -----------: | :--- |
| bar | baz | bam |"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1):center]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1):right]",
        "[text(1,1):defghi:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1):left]",
        "[text(1,1):jkl:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1):center]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1):right]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1):left]",
        "[text(1,1):bam:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th align="center">abc</th>
<th align="right">defghi</th>
<th align="left">jkl</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">bar</td>
<td align="right">baz</td>
<td align="left">bam</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_199_enabled_bad_center() -> None:
    """
    Test case 199:  Cells in one column don’t need to match length, though it’s easier to read if they are. Likewise, use of leading and trailing pipes may be inconsistent:
    """

    # Arrange
    source_markdown = """| abc | defghi | jkl |
| :: | -----------: | :--- |
| bar | baz | bam |"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| abc | defghi | jkl |\n| :: | -----------: | :--- |\n| bar | baz | bam |::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>| abc | defghi | jkl |
| :: | -----------: | :--- |
| bar | baz | bam |</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_199_enabled_bad_right_length() -> None:
    """
    Test case 199:  Cells in one column don’t need to match length, though it’s easier to read if they are. Likewise, use of leading and trailing pipes may be inconsistent:
    """

    # Arrange
    source_markdown = """| abc | defghi | jkl |
| :-: | : | :--- |
| bar | baz | bam |"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| abc | defghi | jkl |\n| :-: | : | :--- |\n| bar | baz | bam |::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>| abc | defghi | jkl |
| :-: | : | :--- |
| bar | baz | bam |</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_199_enabled_bad_right_character() -> None:
    """
    Test case 199:  Cells in one column don’t need to match length, though it’s easier to read if they are. Likewise, use of leading and trailing pipes may be inconsistent:
    """

    # Arrange
    source_markdown = """| abc | defghi | jkl |
| :-: | --; | :--- |
| bar | baz | bam |"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| abc | defghi | jkl |\n| :-: | --; | :--- |\n| bar | baz | bam |::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>| abc | defghi | jkl |
| :-: | --; | :--- |
| bar | baz | bam |</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_199_enabled_bad_left_length() -> None:
    """
    Test case 199:  Cells in one column don’t need to match length, though it’s easier to read if they are. Likewise, use of leading and trailing pipes may be inconsistent:
    """

    # Arrange
    source_markdown = """| abc | defghi | jkl |
| :-: | ---: | : |
| bar | baz | bam |"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| abc | defghi | jkl |\n| :-: | ---: | : |\n| bar | baz | bam |::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>| abc | defghi | jkl |
| :-: | ---: | : |
| bar | baz | bam |</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_199_enabled_bad_left_character() -> None:
    """
    Test case 199:  Cells in one column don’t need to match length, though it’s easier to read if they are. Likewise, use of leading and trailing pipes may be inconsistent:
    """

    # Arrange
    source_markdown = """| abc | defghi | jkl |
| :-: | ---: | ;--- |
| bar | baz | bam |"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| abc | defghi | jkl |\n| :-: | ---: | ;--- |\n| bar | baz | bam |::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>| abc | defghi | jkl |
| :-: | ---: | ;--- |
| bar | baz | bam |</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_200_disabled() -> None:
    """
    Test case 200:  Include a pipe in a cell’s content by escaping it, including inside other inline spans:
    """

    # Arrange
    source_markdown = """| f\\|oo  |
| ------ |
| b `\\|` az |
| b **\\|** im |"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):| f\\\b|oo  |\n| ------ |\n| b ::\n\n]",
        "[icode-span(3,5):\\|:`::]",
        "[text(3,9): az |\n| b ::\n]",
        "[emphasis(4,5):2:*]",
        "[text(4,7):\\\b|:]",
        "[end-emphasis(4,9)::]",
        "[text(4,11): im |:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>| f|oo  |\n| ------ |\n| b <code>\\|</code> az |\n| b <strong>|</strong> im |</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_tables_extension_200_enabled() -> None:
    """
    Test case 200:  Include a pipe in a cell’s content by escaping it, including inside other inline spans:
    """

    # Arrange
    source_markdown = """| f\\|oo  |
| ------ |
| b `\\|` az |
| b **\\|** im |"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):f\\\b|oo:]",
        "[end-table-header-item:  |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):b :]",
        "[icode-span(1,3):\\|:`::]",
        "[text(1,7): az:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):b :]",
        "[emphasis(1,3):2:*]",
        "[text(1,5):\\\b|:]",
        "[end-emphasis(1,7)::]",
        "[text(1,9): im:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>f|oo</th>
</tr>
</thead>
<tbody>
<tr>
<td>b <code>|</code> az</td>
</tr>
<tr>
<td>b <strong>|</strong> im</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_200_enabled_trailing_escaped_bar() -> None:
    """
    Test case 200:  Include a pipe in a cell’s content by escaping it, including inside other inline spans:
    """

    # Arrange
    source_markdown = """| f\\|oo  |
| ------ |
| b `\\|` az \\|
| b **\\|** im |"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):f\\\b|oo:]",
        "[end-table-header-item:  |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):b :]",
        "[icode-span(1,3):\\|:`::]",
        "[text(1,7): az \\\b|:]",
        "[end-table-row-item:::False]",
        "[end-table-row:::False]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):b :]",
        "[emphasis(1,3):2:*]",
        "[text(1,5):\\\b|:]",
        "[end-emphasis(1,7)::]",
        "[text(1,9): im:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>f|oo</th>
</tr>
</thead>
<tbody>
<tr>
<td>b <code>|</code> az |</td>
</tr>
<tr>
<td>b <strong>|</strong> im</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_200_enabled_trailing_escaped_bar_2() -> None:
    """
    Test case 200:  Include a pipe in a cell’s content by escaping it, including inside other inline spans:
    """

    # Arrange
    source_markdown = """| f\\|oo  |
| ------ |
| b `\\|` az \\|\a\a
| b **\\|** im |""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):f\\\b|oo:]",
        "[end-table-header-item:  |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):b :]",
        "[icode-span(1,3):\\|:`::]",
        "[text(1,7): az \\\b|:]",
        "[end-table-row-item:  ::False]",
        "[end-table-row:::False]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):b :]",
        "[emphasis(1,3):2:*]",
        "[text(1,5):\\\b|:]",
        "[end-emphasis(1,7)::]",
        "[text(1,9): im:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>f|oo</th>
</tr>
</thead>
<tbody>
<tr>
<td>b <code>|</code> az |</td>
</tr>
<tr>
<td>b <strong>|</strong> im</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_200_enabled_only_escaped_bar() -> None:
    """
    Test case 200:  Include a pipe in a cell’s content by escaping it, including inside other inline spans:
    """

    # Arrange
    source_markdown = """|\\||
| ------ |
|\\|
|\\||"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):\\\b|:]",
        "[end-table-header-item:|::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):\\\b|:]",
        "[end-table-row-item:::False]",
        "[end-table-row:::False]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):\\\b|:]",
        "[end-table-row-item:|::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>|</th>
</tr>
</thead>
<tbody>
<tr>
<td>|</td>
</tr>
<tr>
<td>|</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_200_enabled_a() -> None:
    """
    Test case 200:  Include a pipe in a cell’s content by escaping it, including inside other inline spans:
    """

    # Arrange
    source_markdown = """| b `\\|` oo  |
| ------ |

b `\\|` oo

"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):b :]",
        "[icode-span(1,3):\\|:`::]",
        "[text(1,7): oo:]",
        "[end-table-header-item:  |::False]",
        "[end-table-header:::False]",
        "[end-table:::False]",
        "[BLANK(3,1):]",
        "[para(4,1):]",
        "[text(4,1):b :]",
        "[icode-span(4,3):\\|:`::]",
        "[text(4,7): oo:]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>b <code>|</code> oo</th>
</tr>
</thead>
</table>
<p>b <code>\\|</code> oo</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_200_enabled_b() -> None:
    """
    Test case 200:  Include a pipe in a cell’s content by escaping it, including inside other inline spans:
    """

    # Arrange
    source_markdown = """| b `a\\|b` oo  |
| ------ |
| b `a\\|b` az |
"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):b :]",
        "[icode-span(1,3):a\\|b:`::]",
        "[text(1,9): oo:]",
        "[end-table-header-item:  |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):b :]",
        "[icode-span(1,3):a\\|b:`::]",
        "[text(1,9): az:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>b <code>a|b</code> oo</th>
</tr>
</thead>
<tbody>
<tr>
<td>b <code>a|b</code> az</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_disabled() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
> bar"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| abc | def |\n| --- | --- |\n| bar | baz |::\n\n]",
        "[end-para:::True]",
        "[block-quote(4,1)::> ]",
        "[para(4,3):]",
        "[text(4,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<p>| abc | def |\n| --- | --- |\n| bar | baz |</p>\n<blockquote>\n<p>bar</p>\n</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_tables_extension_201_enabled_x() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:

    test_link_reference_definitions_185e
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
> bar"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[block-quote(4,1)::> ]",
        "[para(4,3):]",
        "[text(4,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<blockquote>
<p>bar</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_xa() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

> bar"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(4,1):]",
        "[block-quote(5,1)::> ]",
        "[para(5,3):]",
        "[text(5,3):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<blockquote>
<p>bar</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_xb() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
  > bar"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[block-quote(4,3):  :  > ]",
        "[para(4,5):]",
        "[text(4,5):bar:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<blockquote>
<p>bar</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_ax() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:

    test_link_reference_definitions_185ax
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
# bar"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[atx(4,1):1:0:]",
        "[text(4,3):bar: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<h1>bar</h1>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_aa() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

# bar"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(4,1):]",
        "[atx(5,1):1:0:]",
        "[text(5,3):bar: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<h1>bar</h1>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_ab() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
  # bar"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[atx(4,3):1:0:  ]",
        "[text(4,5):bar: ]",
        "[end-atx::]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<h1>bar</h1>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_bx() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:

    test_whitespaces_lrd_with_spaces_followed_by_thematic
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
-----"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[tbreak(4,1):-::-----]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_ba() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

-----"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(4,1):]",
        "[tbreak(5,1):-::-----]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_bb() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
  -----"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[tbreak(4,3):-:  :-----]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<hr />"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_cx() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:

    test_link_reference_definitions_185c
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
    abc"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[icode-block(4,5):    :]",
        "[text(4,5):abc:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<pre><code>abc
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_ca() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

    abc"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(4,1):]",
        "[icode-block(5,5):    :]",
        "[text(5,5):abc:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<pre><code>abc
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_dx() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:

    test_link_reference_definitions_185b
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
```python"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[fcode-block(4,1):`:3:python:::::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<pre><code class="language-python"></code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_da() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

```python"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(4,1):]",
        "[fcode-block(5,1):`:3:python:::::]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<pre><code class="language-python"></code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_db() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
  ```python"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[fcode-block(4,3):`:3:python::::  :]",
        "[end-fcode-block::::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<pre><code class="language-python"></code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_ex() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:

    test_link_reference_definitions_185d
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
<!-- comment -->"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[html-block(4,1)]",
        "[text(4,1):<!-- comment -->:]",
        "[end-html-block:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<!-- comment -->"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_ea() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

<!-- comment -->"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(4,1):]",
        "[html-block(5,1)]",
        "[text(5,1):<!-- comment -->:]",
        "[end-html-block:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<!-- comment -->"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_eb() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
   <!-- comment -->"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[html-block(4,1)]",
        "[text(4,4):<!-- comment -->:   ]",
        "[end-html-block:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
   <!-- comment -->"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_fx() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:

    test_whitespaces_lrd_with_spaces_followed_by_lrd
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | [baz] |
[baz]: /url"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[link(1,1):shortcut:/url:::::baz:False::::]",
        "[text(1,2):baz:]",
        "[end-link::]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[link-ref-def(4,1):True::baz:: :/url:::::]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td><a href="/url">baz</a></td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_fa() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | [baz] |

[baz]: /url"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[link(1,1):shortcut:/url:::::baz:False::::]",
        "[text(1,2):baz:]",
        "[end-link::]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(4,1):]",
        "[link-ref-def(5,1):True::baz:: :/url:::::]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td><a href="/url">baz</a></td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_fb() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | [baz] |
  [baz]: /url"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[link(1,1):shortcut:/url:::::baz:False::::]",
        "[text(1,2):baz:]",
        "[end-link::]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[link-ref-def(4,3):True:  :baz:: :/url:::::]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td><a href="/url">baz</a></td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_gx() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:

    test_link_reference_definitions_185gx
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
1. bar"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[olist(4,1):.:1:3:]",
        "[para(4,4):]",
        "[text(4,4):bar:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<ol>
<li>bar</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_ga() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

1. bar"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(4,1):]",
        "[olist(5,1):.:1:3:]",
        "[para(5,4):]",
        "[text(5,4):bar:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<ol>
<li>bar</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_gb() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
  1. bar"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[olist(4,3):.:1:5:  ]",
        "[para(4,6):]",
        "[text(4,6):bar:]",
        "[end-para:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<ol>
<li>bar</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_hx() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:

    test_link_reference_definitions_185fx
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
- bar"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[ulist(4,1):-::2:]",
        "[para(4,3):]",
        "[text(4,3):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<ul>
<li>bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_201_enabled_ha() -> None:
    """
    Test case 201:  (part 1) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |

- bar"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(4,1):]",
        "[ulist(5,1):-::2:]",
        "[para(5,3):]",
        "[text(5,3):bar:]",
        "[end-para:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>
<ul>
<li>bar</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_202_disabled() -> None:
    """
    Test case 202:  (part 2) The table is broken at the first empty line, or beginning of another block-level structure:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
bar

bar"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):| abc | def |\n| --- | --- |\n| bar | baz |\nbar::\n\n\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[para(6,1):]",
        "[text(6,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>| abc | def |\n| --- | --- |\n| bar | baz |\nbar</p>\n<p>bar</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_tables_extension_202_enabled() -> None:
    """
    Test case 202:  (part 2) The table is broken at the first empty line, or beginning of another block-level structure:
                    note that tables gooble up lines as a single column until a blank line or another block-level structure is found

    test_link_reference_definitions_167
    test_link_reference_definitions_185x
    test_link_reference_definitions_184
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar | baz |
bar

bar"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item:::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
        "[para(6,1):]",
        "[text(6,1):bar:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
<tr>
<td>bar</td>
<td></td>
</tr>
</tbody>
</table>
<p>bar</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_203_disabled() -> None:
    """
    Test case 203:  The header row must match the delimiter row in the number of cells. If not, a table will not be recognized:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- |
| bar |"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| abc | def |\n| --- |\n| bar |::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>| abc | def |\n| --- |\n| bar |</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_tables_extension_203_enabled() -> None:
    """
    Test case 203:  The header row must match the delimiter row in the number of cells. If not, a table will not be recognized:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- |
| bar |"""
    expected_tokens = [
        "[para(1,1):\n\n]",
        "[text(1,1):| abc | def |\n| --- |\n| bar |::\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>| abc | def |\n| --- |\n| bar |</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_204_disabled() -> None:
    """
    Test case 204:  The remainder of the table’s rows may vary in the number of cells. If there are a number of cells fewer than the number of cells in the header row, empty cells are inserted. If there are greater, the excess is ignored:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar |
| bar | baz | boo |"""
    expected_tokens = [
        "[para(1,1):\n\n\n]",
        "[text(1,1):| abc | def |\n| --- | --- |\n| bar |\n| bar | baz | boo |::\n\n\n]",
        "[end-para:::True]",
    ]
    expected_gfm = (
        """<p>| abc | def |\n| --- | --- |\n| bar |\n| bar | baz | boo |</p>"""
    )

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_tables_extension_204_enabled() -> None:
    """
    Test case 204:  The remainder of the table’s rows may vary in the number of cells. If there are a number of cells fewer than the number of cells in the header row, empty cells are inserted. If there are greater, the excess is ignored:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |
| bar |
| bar | baz | boo |"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,1)]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[table-row(1,1)]",
        "[table-row-item(1,1)]",
        "[text(1,1):bar:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,1)]",
        "[text(1,1):baz:]",
        "[end-table-row-item: |::False]",
        "[end-table-row: boo |::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
<tbody>
<tr>
<td>bar</td>
<td></td>
</tr>
<tr>
<td>bar</td>
<td>baz</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_205_disabled() -> None:
    """
    Test case 205:  If there are no rows in the body, no <tbody> is generated in HTML output:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |"""
    expected_tokens = [
        "[para(1,1):\n]",
        "[text(1,1):| abc | def |\n| --- | --- |::\n]",
        "[end-para:::True]",
    ]
    expected_gfm = """<p>| abc | def |\n| --- | --- |</p>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_tables_extension_205_enabled() -> None:
    """
    Test case 205:  If there are no rows in the body, no <tbody> is generated in HTML output:
    """

    # Arrange
    source_markdown = """| abc | def |
| --- | --- |"""
    expected_tokens = [
        "[table(1,1)]",
        "[table-header(1,1)]",
        "[table-header-item(1,1)]",
        "[text(1,1):abc:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,1)]",
        "[text(1,1):def:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[end-table:::False]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>abc</th>
<th>def</th>
</tr>
</thead>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_extra_in_block() -> None:
    """
    Test case extra 1:  TBD
    """

    # Arrange
    source_markdown = """> | foo | bar |
> | --- | --- |
> | baz | bim |"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_extra_in_block_in_block_after_first_line() -> None:
    """
    Test case extra 1:  TBD
    """

    # Arrange
    source_markdown = """> | foo | bar |
>> | --- | --- |
>> | baz | bim |"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):| foo | bar |:]",
        "[end-para:::True]",
        "[block-quote(2,1)::>> \n>> ]",
        "[para(2,4):\n]",
        "[text(2,4):| --- | --- |\n| baz | bim |::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>| foo | bar |</p>
<blockquote>
<p>| --- | --- |
| baz | bim |</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_extra_in_block_in_block_after_first_line_xx() -> None:
    """
    Test case extra 1:  TBD
    """

    # Arrange
    source_markdown = """> | --- | --- |
> | baz | bim |"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):\n]",
        "[text(1,3):| --- | --- |\n| baz | bim |::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>| --- | --- |
| baz | bim |</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_extra_in_block_in_block_after_first_line_xa() -> None:
    """
    Test case extra 1:  TBD
    """

    # Arrange
    source_markdown = """>> | --- | --- |
>> | baz | bim |"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::>> \n>> ]",
        "[para(1,4):\n]",
        "[text(1,4):| --- | --- |\n| baz | bim |::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>| --- | --- |
| baz | bim |</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_extra_in_block_in_block_after_first_line_xb() -> None:
    """
    Test case extra 1:  TBD
    """

    # Arrange
    source_markdown = """> | abc | def |
> | -:- | -:- |"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> ]",
        "[para(1,3):\n]",
        "[text(1,3):| abc | def |\n| -:- | -:- |::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>| abc | def |
| -:- | -:- |</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_extra_in_block_in_block_after_first_line_xc() -> None:
    """
    Test case extra 1:  TBD
    """

    # Arrange
    source_markdown = """>> | foo | bar |
> | --- | --- |
> | baz | bim |"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::>> \n> \n> ]",
        "[para(1,4):\n\n]",
        "[text(1,4):| foo | bar |\n| --- | --- |\n| baz | bim |::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>| foo | bar |
| --- | --- |
| baz | bim |</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_extra_in_block_in_block_after_first_line_xd() -> None:
    """
    Test case extra 1:  TBD
    """

    # Arrange
    source_markdown = """> | foo | bar |
>> | --- | --- |
>> | baz | bim |"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):| foo | bar |:]",
        "[end-para:::True]",
        "[block-quote(2,1)::>> \n>> ]",
        "[para(2,4):\n]",
        "[text(2,4):| --- | --- |\n| baz | bim |::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>| foo | bar |</p>
<blockquote>
<p>| --- | --- |
| baz | bim |</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_tables_extension_extra_in_block_in_block_after_first_line_xe() -> None:
    """
    Test case extra 1:  TBD
    """

    # Arrange
    source_markdown = """> abc
> def
> | foo | bar |
>> | --- | --- |
>> | baz | bim |"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):\n\n]",
        "[text(1,3):abc\ndef\n| foo | bar |::\n\n]",
        "[end-para:::True]",
        "[block-quote(4,1)::>> \n>> ]",
        "[para(4,4):\n]",
        "[text(4,4):| --- | --- |\n| baz | bim |::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
| foo | bar |</p>
<blockquote>
<p>| --- | --- |
| baz | bim |</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_whitespaces_tables_extension_with_spaces_within_ulist() -> None:
    """
    Test case: Table within a single unordered list item, preceeded by just enough spaces.

    Related: test_whitespaces_lrd_with_spaces_within_ulist_leading_para_x
    """

    # Arrange
    source_markdown = """+ abc
  | foo | bar |
  | --- | --- |
  | baz | bim |"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_whitespaces_tables_extension_with_spaces_extra_within_ulist() -> None:
    """
    Test case: Table within a single unordered list item, preceeded by extra spaces.

    Related: test_whitespaces_lrd_with_spaces_extra_within_ulist_leading_para
    """

    # Arrange
    source_markdown = """+ abc
    | foo | bar |
    | --- | --- |
    | baz | bim |"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[table(2,5)]",
        "[table-header(2,5)]",
        "[table-header-item(2,5)]",
        "[text(2,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,5)]",
        "[text(2,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,5)]",
        "[table-row(2,5)]",
        "[table-row-item(2,5)]",
        "[text(2,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,5)]",
        "[text(2,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_whitespaces_tables_extension_with_spaces_within_olist() -> None:
    """
    Test case: Table within a single ordered list item, preceeded by just enough spaces.
    """

    # Arrange
    source_markdown = """1. | foo | bar |
   | --- | --- |
   | baz | bim |"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   ]",
        "[table(1,4)]",
        "[table-header(1,4)]",
        "[table-header-item(1,4)]",
        "[text(1,4):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,4)]",
        "[text(1,4):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,4)]",
        "[table-row(1,4)]",
        "[table-row-item(1,4)]",
        "[text(1,4):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,4)]",
        "[text(1,4):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_whitespaces_tables_extension_with_spaces_extra_within_olist() -> None:
    """
    Test case: Table within a single ordered list item, preceeded by extra spaces.
    """

    # Arrange
    source_markdown = """1. abc
    | foo | bar |
    | --- | --- |
    | baz | bim |"""
    expected_tokens = [
        "[olist(1,1):.:1:3::   \n   \n   ]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[table(2,5)]",
        "[table-header(2,5)]",
        "[table-header-item(2,5)]",
        "[text(2,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,5)]",
        "[text(2,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,5)]",
        "[table-row(2,5)]",
        "[table-row-item(2,5)]",
        "[text(2,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,5)]",
        "[text(2,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_whitespaces_tables_extension_with_spaces_within_block_quote() -> None:
    """
    Test case: Table within a single block quote, preceeded by just enough spaces.

    Related: test_whitespaces_lrd_with_spaces_within_block_quote
    """

    # Arrange
    source_markdown = """> abc
> | foo | bar |
> | --- | --- |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[end-table:::False]",
        "[end-block-quote:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_whitespaces_tables_extension_with_spaces_extra_within_block_quote() -> None:
    """
    Test case: Table within a single block quote, preceeded by extra spaces.

    Related: test_whitespaces_tables_extension_with_spaces_within_block_quote
    """

    # Arrange
    source_markdown = """> abc
>  | foo | bar |
>  | --- | --- |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[table(2,4)]",
        "[table-header(2,4)]",
        "[table-header-item(2,4)]",
        "[text(2,4):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,4)]",
        "[text(2,4):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[end-table:::False]",
        "[end-block-quote:::False]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.skip
def test_whitespaces_tables_extension_with_spaces_after_block_quote() -> None:
    """
    Test case: TAble after text within single block quote, without any block quote start character.
        As LRDs cannot interrupt a paragraph, this should be treated as an extension of the paragraph.

    Related: test_whitespaces_lrd_with_spaces_after_block_quote
    """

    # Arrange
    source_markdown = """> abc
> def
  | foo | bar |
  | --- | --- |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n]",
        "[para(1,3):\n\n  \n]",
        "[text(1,3):abc\ndef\n[fred]: /url\n[fred]::\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """needs regen"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_whitespaces_tables_extension_with_some_spaces_after_double_block_quotes() -> (
    None
):
    """
    Test case: Table after text within double block quote, without any block quote start character.

    Related: test_whitespaces_lrd_with_spaces_after_block_quote
    """

    # Arrange
    source_markdown = """> > abc
> > def
  | foo | bar |
  | --- | --- |
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n\n\n]",
        "[para(1,5):\n\n  \n  ]",
        "[text(1,5):abc\ndef\n| foo | bar |\n| --- | --- |::\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>abc
def
| foo | bar |
| --- | --- |</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_whitespaces_tables_extension_with_extra_spaces_after_double_block_quotes() -> (
    None
):
    """
    Test case: Table after text within double block quote, without any block quote start character.
       As there are 4 characters on the line after the block quote, technically only an indented code
       block can follow.  However, since indented code blocks cannot interrupt a paragraph, it becomes
       a continuation of the paragraph.

    Related: test_whitespaces_lrd_with_extra_spaces_after_double_block_quotes
    """

    # Arrange
    source_markdown = """> > abc
> > def
    | foo | bar |
    | --- | --- |
"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,3)::> > \n> > \n\n\n]",
        "[para(1,5):\n\n    \n    ]",
        "[text(1,5):abc\ndef\n| foo | bar |\n| --- | --- |::\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>abc
def
| foo | bar |
| --- | --- |</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.skip
def test_whitespaces_tables_extension_with_spaces_within_single_block_quote_after_double_block_quote() -> (
    None
):
    """
    Test case: Table after text within single block quote, occurring after a double block quote.

    Related: test_whitespaces_lrd_with_spaces_within_single_block_quote_after_double_block_quote
    """

    # Arrange
    source_markdown = """> abc
> > def
>   | foo | bar |
>   | --- | --- |
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n> \n> \n]",
        "[para(2,5):\n  \n  ]",
        "[text(2,5):def\n| foo | bar |\n| --- | --- |::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
[fred]: /url
[fred]</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


def test_tables_extension_extra_in_block_in_block_xx() -> None:
    """
    Test case extra 1:  TBD
    similar to test_link_reference_definitions_extra_02cx
    """

    # Arrange
    source_markdown = """>> | foo | bar |
> | --- | --- |
> | baz | bim |"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::>> \n> \n> ]",
        "[para(1,4):\n\n]",
        "[text(1,4):| foo | bar |\n| --- | --- |\n| baz | bim |::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<p>| foo | bar |
| --- | --- |
| baz | bim |</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


def test_tables_extension_extra_in_block_in_block_xa() -> None:
    """
    Test case extra 1:  TBD
    similar to test_link_reference_definitions_extra_02ca
    """

    # Arrange
    source_markdown = """>>> | foo | bar |
> | --- | --- |
> | baz | bim |"""
    expected_tokens = [
        "[block-quote(1,1)::]",
        "[block-quote(1,2)::]",
        "[block-quote(1,3)::>>> \n> \n> ]",
        "[para(1,5):\n\n]",
        "[text(1,5):| foo | bar |\n| --- | --- |\n| baz | bim |::\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<blockquote>
<blockquote>
<p>| foo | bar |
| --- | --- |
| baz | bim |</p>
</blockquote>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_header_line_only() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    test_html_blocks_extra_02x
    """

    # Arrange
    source_markdown = """- | foo | bar |
- some text
some other text
"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n]",
        "[para(1,3):]",
        "[text(1,3):| foo | bar |:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):\n]",
        "[text(2,3):some text\nsome other text::\n]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>| foo | bar |</li>
<li>some text
some other text</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_header_line_only_x() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item

    test_extra_054x
    """

    # Arrange
    source_markdown = """> | foo | bar |
>
> some text
> some other text
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):| foo | bar |:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[para(3,3):\n]",
        "[text(3,3):some text\nsome other text::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<p>| foo | bar |</p>
<p>some text
some other text</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_header_line_only_a() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item

    test_extra_054x
    """

    # Arrange
    source_markdown = """> | foo | bar |
>
> some text
> some other text
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> \n]",
        "[para(1,3):]",
        "[text(1,3):| foo | bar |:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[para(3,3):\n]",
        "[text(3,3):some text\nsome other text::\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<p>| foo | bar |</p>
<p>some text
some other text</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(source_markdown, expected_gfm, expected_tokens)


@pytest.mark.gfm
def test_tables_extension_extra_in_list_header_line_only_with_separator_in_seperate_list_item() -> (
    None
):
    """
    Test case extra 02:  variation of 1 with html block started in list item
    test_html_blocks_extra_02x
    """

    # Arrange
    source_markdown = """- | foo | bar |
- | --- | --- |
- some text
some other text
"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n]",
        "[para(1,3):]",
        "[text(1,3):| foo | bar |:]",
        "[end-para:::True]",
        "[li(2,1):2::]",
        "[para(2,3):]",
        "[text(2,3):| --- | --- |:]",
        "[end-para:::True]",
        "[li(3,1):2::]",
        "[para(3,3):\n]",
        "[text(3,3):some text\nsome other text::\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>| foo | bar |</li>
<li>| --- | --- |</li>
<li>some text
some other text</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_header_and_separator_only() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    test_html_blocks_extra_02x
    """

    # Arrange
    source_markdown = """- | foo | bar |
  | --- | --- |
- some text
some other text
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n\n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[end-table:::False]",
        "[li(3,1):2::]",
        "[para(3,3):\n]",
        "[text(3,3):some text\nsome other text::\n]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
</table>
</li>
<li>some text
some other text</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_header_and_separator_only_lrd_in_next_list_item() -> (
    None
):
    """
    Test case extra 02:  variation of 1 with html block started in list item
    test_html_blocks_extra_02x

    NOTE: variations made as LRD is tokenized
    """

    # Arrange
    source_markdown = """- | foo | bar |
  | --- | --- |
- [foo]: /url
- [foo]
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[end-table:::False]",
        "[li(3,1):2::]",
        "[link-ref-def(3,3):True::foo:: :/url:::::]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[link(4,3):shortcut:/url:::::foo:False::::]",
        "[text(4,4):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
</table>
</li>
<li></li>
<li><a href="/url">foo</a></li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_header_and_separator_only_lrd_in_previous_list_item() -> (
    None
):
    """
    Test case extra 02:  variation of 1 with html block started in list item
    test_html_blocks_extra_02x
    """

    # Arrange
    source_markdown = """- [foo]: /url
- | foo | bar |
  | --- | --- |
- [foo]
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n]",
        "[link-ref-def(1,3):True::foo:: :/url:::::]",
        "[li(2,1):2::]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[end-table:::False]",
        "[li(4,1):2::]",
        "[para(4,3):]",
        "[link(4,3):shortcut:/url:::::foo:False::::]",
        "[text(4,4):foo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li></li>
<li>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
</table>
</li>
<li><a href="/url">foo</a></li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_followed_by_new_line_and_atx() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """- | foo | bar |
  | -- | -- |
  | baz | bim |

  # bac
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n\n  \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(4,1):]",
        "[atx(5,3):1:0:]",
        "[text(5,5):bac: ]",
        "[end-atx::]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
<h1>bac</h1>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_followed_by_new_line_and_atx() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    test_block_quotes_extra_03bb
    """

    # Arrange
    source_markdown = """> | foo | bar |
> | -- | -- |
> | baz | bim |
>
> # bac
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n>\n> \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(4,2):]",
        "[atx(5,3):1:0:]",
        "[text(5,5):bac: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
<h1>bac</h1>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_header_only_after_text_and_new_line() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """- abc

  | foo | bar |
"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n  \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[para(3,3):]",
        "[text(3,3):| foo | bar |:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<p>abc</p>
<p>| foo | bar |</p>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_header_only_after_text_and_new_line() -> (
    None
):
    """
    Test case extra 02:  variation of 1 with html block started in list item
    test_whitespaces_lrd_with_tabs_before_within_block_quotes_bare_over_more_lines_3b
    """

    # Arrange
    source_markdown = """> abc
>
> | foo | bar |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[para(3,3):]",
        "[text(3,3):| foo | bar |:]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<p>| foo | bar |</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_after_paragraph() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item

    note that the list is not loose, as there are no blank lines between the list items,
    but some parsers might think this is a loose list.
    """

    # Arrange
    source_markdown = """+ this is text
  | foo | bar |
  | --- | --- |
  | foo | bar |
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n]",
        "[para(1,3):]",
        "[text(1,3):this is text:]",
        "[end-para:::True]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>this is text<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_after_paragraph() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> this is text
> | foo | bar |
> | --- | --- |
> | foo | bar |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[para(1,3):]",
        "[text(1,3):this is text:]",
        "[end-para:::True]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-block-quote:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is text</p>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_after_atx() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """+ # Heading
  | foo | bar |
  | --- | --- |
  | foo | bar |
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n]",
        "[atx(1,3):1:0:]",
        "[text(1,5):Heading: ]",
        "[end-atx::]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<h1>Heading</h1>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_after_atx() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> # Heading
> | foo | bar |
> | --- | --- |
> | foo | bar |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[atx(1,3):1:0:]",
        "[text(1,5):Heading: ]",
        "[end-atx::]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-block-quote:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<h1>Heading</h1>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_followed_atx() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """+ | foo | bar |
  | --- | --- |
  | foo | bar |
  # Heading
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[atx(4,3):1:0:]",
        "[text(4,5):Heading: ]",
        "[end-atx::]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<h1>Heading</h1>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_followed_atx() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> | foo | bar |
> | --- | --- |
> | foo | bar |
> # Heading
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[atx(4,3):1:0:]",
        "[text(4,5):Heading: ]",
        "[end-atx::]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<h1>Heading</h1>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_after_thematic() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """+ ----
  | foo | bar |
  | --- | --- |
  | foo | bar |
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n]",
        "[tbreak(1,3):-::----]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<hr />
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_after_thematic() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> ----
> | foo | bar |
> | --- | --- |
> | foo | bar |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[tbreak(1,3):-::----]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-block-quote:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<hr />
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_followed_thematic() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """+ | foo | bar |
  | --- | --- |
  | foo | bar |
  ----
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[tbreak(4,3):-::----]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<hr />
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_followed_thematic() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> | foo | bar |
> | --- | --- |
> | foo | bar |
> ----
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[tbreak(4,3):-::----]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<hr />
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_after_indented_block() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """-     indented
      code block
  | foo | bar |
  | --- | --- |
  | foo | bar |
"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n  \n]",
        "[icode-block(1,7):    :\n    ]",
        "[text(1,7):indented\ncode block:]",
        "[end-icode-block:::False]",
        "[table(3,3)]",
        "[table-header(3,3)]",
        "[table-header-item(3,3)]",
        "[text(3,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(3,3)]",
        "[text(3,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,3)]",
        "[table-row(3,3)]",
        "[table-row-item(3,3)]",
        "[text(3,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(3,3)]",
        "[text(3,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code>indented
code block
</code></pre>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_after_indented_block() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """>     indented
>     code block
> | foo | bar |
> | --- | --- |
> | foo | bar |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[icode-block(1,7):    :\n    ]",
        "[text(1,7):indented\ncode block:]",
        "[end-icode-block:::False]",
        "[table(3,3)]",
        "[table-header(3,3)]",
        "[table-header-item(3,3)]",
        "[text(3,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(3,3)]",
        "[text(3,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,3)]",
        "[table-row(3,3)]",
        "[table-row-item(3,3)]",
        "[text(3,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(3,3)]",
        "[text(3,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-block-quote:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<pre><code>indented
code block
</code></pre>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_followed_indented_block() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """+ | foo | bar |
  | --- | --- |
  | foo | bar |
      indented
      code block
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n  \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[icode-block(4,7):    :\n    ]",
        "[text(4,7):indented\ncode block:]",
        "[end-icode-block:::True]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<pre><code>indented
code block
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_followed_indented_block() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> | foo | bar |
> | --- | --- |
> | foo | bar |
>     indented
>     code block
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[icode-block(4,7):    :\n    ]",
        "[text(4,7):indented\ncode block:]",
        "[end-icode-block:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<pre><code>indented
code block
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_after_fenced_block() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """+ ```sh
  echo foo
  ```
  | foo | bar |
  | --- | --- |
  | foo | bar |
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n  \n  \n]",
        "[fcode-block(1,3):`:3:sh:::::]",
        "[text(2,3):echo foo:]",
        "[end-fcode-block:::3:False]",
        "[table(4,3)]",
        "[table-header(4,3)]",
        "[table-header-item(4,3)]",
        "[text(4,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(4,3)]",
        "[text(4,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(4,3)]",
        "[table-row(4,3)]",
        "[table-row-item(4,3)]",
        "[text(4,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(4,3)]",
        "[text(4,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<pre><code class="language-sh">echo foo
</code></pre>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_after_fenced_block() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> ```sh
> echo foo
> ```
> | foo | bar |
> | --- | --- |
> | foo | bar |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> ]",
        "[fcode-block(1,3):`:3:sh:::::]",
        "[text(2,3):echo foo:]",
        "[end-fcode-block:::3:False]",
        "[table(4,3)]",
        "[table-header(4,3)]",
        "[table-header-item(4,3)]",
        "[text(4,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(4,3)]",
        "[text(4,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(4,3)]",
        "[table-row(4,3)]",
        "[table-row-item(4,3)]",
        "[text(4,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(4,3)]",
        "[text(4,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-block-quote:::False]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<pre><code class="language-sh">echo foo
</code></pre>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_followed_fenced_block() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """+ | foo | bar |
  | --- | --- |
  | foo | bar |
  ```sh
  echo foo
  ```
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n  \n  \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[fcode-block(4,3):`:3:sh:::::]",
        "[text(5,3):echo foo:]",
        "[end-fcode-block:::3:False]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<pre><code class="language-sh">echo foo
</code></pre>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_followed_fenced_block() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> | foo | bar |
> | --- | --- |
> | foo | bar |
> ```sh
> echo foo
> ```
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> \n> \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[fcode-block(4,3):`:3:sh:::::]",
        "[text(5,3):echo foo:]",
        "[end-fcode-block:::3:False]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<pre><code class="language-sh">echo foo
</code></pre>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_after_html_block() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """+ <!-- comment -->
  | foo | bar |
  | --- | --- |
  | foo | bar |
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n]",
        "[html-block(1,3)]",
        "[text(1,3):<!-- comment -->:]",
        "[end-html-block:::False]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<!-- comment -->
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_after_html_block() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> <!-- comment -->
> | foo | bar |
> | --- | --- |
> | foo | bar |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> ]",
        "[html-block(1,3)]",
        "[text(1,3):<!-- comment -->:]",
        "[end-html-block:::False]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-block-quote:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<!-- comment -->
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_followed_html_block() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """+ | foo | bar |
  | --- | --- |
  | foo | bar |
  <!-- comment -->
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[html-block(4,3)]",
        "[text(4,3):<!-- comment -->:]",
        "[end-html-block:::False]",
        "[BLANK(5,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<!-- comment -->
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_followed_html_block() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> | foo | bar |
> | --- | --- |
> | foo | bar |
> <!-- comment -->
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[html-block(4,3)]",
        "[text(4,3):<!-- comment -->:]",
        "[end-html-block:::False]",
        "[end-block-quote:::True]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<!-- comment -->
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_after_lrd() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """+ [boo]: /url
  | foo | bar |
  | --- | --- |
  | foo | bar |

  [boo]
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n\n  \n]",
        "[link-ref-def(1,3):True::boo:: :/url:::::]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
        "[para(6,3):]",
        "[link(6,3):shortcut:/url:::::boo:False::::]",
        "[text(6,4):boo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<a href="/url">boo</a></li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
        show_debug=False,
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_after_lrd() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> [boo]: /url
> | foo | bar |
> | --- | --- |
> | foo | bar |
>
> [boo]
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n]",
        "[link-ref-def(1,3):True::boo:: :/url:::::]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,2):]",
        "[para(6,3):]",
        "[link(6,3):shortcut:/url:::::boo:False::::]",
        "[text(6,4):boo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<p><a href="/url">boo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
        show_debug=False,
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_after_lrd_a() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> abc
>
> [boo]: /url
> | foo | bar |
> | --- | --- |
> | foo | bar |
>
> [boo]
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>\n> \n> \n> \n> \n>\n> \n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[link-ref-def(3,3):True::boo:: :/url:::::]",
        "[table(4,3)]",
        "[table-header(4,3)]",
        "[table-header-item(4,3)]",
        "[text(4,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(4,3)]",
        "[text(4,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(4,3)]",
        "[table-row(4,3)]",
        "[table-row-item(4,3)]",
        "[text(4,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(4,3)]",
        "[text(4,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(7,2):]",
        "[para(8,3):]",
        "[link(8,3):shortcut:/url:::::boo:False::::]",
        "[text(8,4):boo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(9,1):]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<p><a href="/url">boo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
        show_debug=False,
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_followed_lrd() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """+ [boo]
  | foo | bar |
  | --- | --- |
  | foo | bar |
  [boo]: /url
"""
    expected_tokens = [
        "[ulist(1,1):+::2::  \n  \n  \n  \n]",
        "[para(1,3):]",
        "[link(1,3):shortcut:/url:::::boo:False::::]",
        "[text(1,4):boo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[link-ref-def(5,3):True::boo:: :/url:::::]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li><a href="/url">boo</a><table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_quote_followed_lrd() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> [boo](/url)
> | foo | bar |
> | --- | --- |
> | foo | bar |
> [boo]: /url
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n> ]",
        "[para(1,3):]",
        "[link(1,3):inline:/url:::::boo:False::::]",
        "[text(1,4):boo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[link-ref-def(5,3):True::boo:: :/url:::::]",
        "[end-block-quote:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<p><a href="/url">boo</a></p>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_chxb() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """>\a
> | foo | bar |
> | --- | --- |
> | foo | bar |
>
> [boo](/url)
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n]",
        "[BLANK(1,3):]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,2):]",
        "[para(6,3):]",
        "[link(6,3):inline:/url:::::boo:False::::]",
        "[text(6,4):boo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<p><a href="/url">boo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_list_cha() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> [boo]
> | foo | bar |
> | --- | --- |
> | foo | bar |
>
> [boo]: /url
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> ]",
        "[para(1,3):]",
        "[link(1,3):shortcut:/url:::::boo:False::::]",
        "[text(1,4):boo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[table(2,3)]",
        "[table-header(2,3)]",
        "[table-header-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,3)]",
        "[table-row(2,3)]",
        "[table-row-item(2,3)]",
        "[text(2,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,3)]",
        "[text(2,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,2):]",
        "[link-ref-def(6,3):True::boo:: :/url:::::]",
        "[end-block-quote:::False]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<p><a href="/url">boo</a></p>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_tables_extension_extra_in_block_chb() -> None:
    """
    Test case extra 02:  variation of 1 with html block started in list item
    """

    # Arrange
    source_markdown = """> | foo | bar |
> | --- | --- |
> | foo | bar |
> [boo](/url)
>
> [boo](/url)
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> \n> \n>\n> \n]",
        "[table(1,3)]",
        "[table-header(1,3)]",
        "[table-header-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,3)]",
        "[table-row(1,3)]",
        "[table-row-item(1,3)]",
        "[text(1,3):foo:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,3)]",
        "[text(1,3):bar:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[para(4,3):]",
        "[link(4,3):inline:/url:::::boo:False::::]",
        "[text(4,4):boo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[BLANK(5,2):]",
        "[para(6,3):]",
        "[link(6,3):inline:/url:::::boo:False::::]",
        "[text(6,4):boo:]",
        "[end-link::]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>foo</td>
<td>bar</td>
</tr>
</tbody>
</table>
<p><a href="/url">boo</a></p>
<p><a href="/url">boo</a></p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
        show_debug=False,
    )


def test_whitespaces_tables_with_tabs_before_x() -> None:
    """
    Test case 198:  The

    test_whitespaces_lrd_with_tabs_before_x
    """

    # Arrange
    source_markdown = """\t| foo | bar |
\t| --- | --- |
\t| baz | bim |"""
    expected_tokens = [
        "[icode-block(1,5):\t:\n\t\n\t]",
        "[text(1,5):| foo | bar |\n| --- | --- |\n| baz | bim |:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>| foo | bar |
| --- | --- |
| baz | bim |
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown, expected_gfm, expected_tokens, config_map=config_map
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_unordered_list_x() -> None:
    """
    Test case:  tables preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
\t| foo | bar |
\t| --- | --- |
\t| baz | bim |

"""
    expected_tokens = [
        "[ulist(1,1):-::2::\n\n\n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[table(2,5)]",
        "[table-header(2,5)]",
        "[table-header-item(2,5)]",
        "[text(2,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,5)]",
        "[text(2,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,5)]",
        "[table-row(2,5)]",
        "[table-row-item(2,5)]",
        "[text(2,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,5)]",
        "[text(2,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_unordered_list_and_single_space() -> (
    None
):
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """- abc
 \t| foo | bar |
 \t| --- | --- |
 \t| baz | bim |

"""
    expected_tokens = [
        "[ulist(1,1):-::2:: \n \n \n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[table(2,5)]",
        "[table-header(2,5)]",
        "[table-header-item(2,5)]",
        "[text(2,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,5)]",
        "[text(2,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,5)]",
        "[table-row(2,5)]",
        "[table-row-item(2,5)]",
        "[text(2,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,5)]",
        "[text(2,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_unordered_list_and_spaces() -> None:
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  \t| foo | bar |
  \t| --- | --- |
  \t| baz | bim |

"""
    expected_tokens = [
        "[ulist(1,1):-::2::  \n  \n  \n\n]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[table(2,5)]",
        "[table-header(2,5)]",
        "[table-header-item(2,5)]",
        "[text(2,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,5)]",
        "[text(2,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,5)]",
        "[table-row(2,5)]",
        "[table-row-item(2,5)]",
        "[text(2,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,5)]",
        "[text(2,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_unordered_double_list() -> None:
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """- abc
  - def
\t| foo | bar |
\t| --- | --- |
\t| baz | bim |
"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :\n\n\n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[table(3,5)]",
        "[table-header(3,5)]",
        "[table-header-item(3,5)]",
        "[text(3,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(3,5)]",
        "[text(3,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,5)]",
        "[table-row(3,5)]",
        "[table-row-item(3,5)]",
        "[text(3,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(3,5)]",
        "[text(3,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(6,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>def<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ul>
</li>
</ul>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_ordered_list_x() -> None:
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
\t| foo | bar |
\t| --- | --- |
\t| baz | bim |
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::\n\n\n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[table(2,5)]",
        "[table-header(2,5)]",
        "[table-header-item(2,5)]",
        "[text(2,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,5)]",
        "[text(2,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,5)]",
        "[table-row(2,5)]",
        "[table-row-item(2,5)]",
        "[text(2,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,5)]",
        "[text(2,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_ordered_list_and_single_space() -> (
    None
):
    """
    Test case:  LRD preceeded by spaces.
    """

    # Arrange
    source_markdown = """1. abc
 \t| foo | bar |
 \t| --- | --- |
 \t| baz | bim |
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:: \n \n \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[table(2,5)]",
        "[table-header(2,5)]",
        "[table-header-item(2,5)]",
        "[text(2,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,5)]",
        "[text(2,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,5)]",
        "[table-row(2,5)]",
        "[table-row-item(2,5)]",
        "[text(2,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,5)]",
        "[text(2,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_ordered_list_and_spaces() -> None:
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
  \t| foo | bar |
  \t| --- | --- |
  \t| baz | bim |
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::  \n  \n  \n]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[table(2,5)]",
        "[table-header(2,5)]",
        "[table-header-item(2,5)]",
        "[text(2,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,5)]",
        "[text(2,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,5)]",
        "[table-row(2,5)]",
        "[table-row-item(2,5)]",
        "[text(2,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,5)]",
        "[text(2,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_ordered_double_list_x() -> None:
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t  | foo | bar |
\t  | --- | --- |
\t  | baz | bim |
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n\n\n]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[table(3,7)]",
        "[table-header(3,7)]",
        "[table-header-item(3,7)]",
        "[text(3,7):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(3,7)]",
        "[text(3,7):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,7)]",
        "[table-row(3,7)]",
        "[table-row-item(3,7)]",
        "[text(3,7):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(3,7)]",
        "[text(3,7):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_ordered_double_list_no_spaces() -> (
    None
):
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t| foo | bar |
\t| --- | --- |
\t| baz | bim |
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n\n\n]",
        "[para(2,7):\n\t\n\t\n\t]",
        "[text(2,7):def\n| foo | bar |\n| --- | --- |\n| baz | bim |::\n\n\n]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
| foo | bar |
| --- | --- |
| baz | bim |</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_ordered_double_list_tab_after_indent() -> (
    None
):
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
   \t| foo | bar |
   \t| --- | --- |
   \t| baz | bim |
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n\n\n]",
        "[para(2,7):\n   \t\n   \t\n   \t]",
        "[text(2,7):def\n| foo | bar |\n| --- | --- |\n| baz | bim |::\n\n\n]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
| foo | bar |
| --- | --- |
| baz | bim |</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_ordered_double_list_one_space() -> (
    None
):
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t | foo | bar |
\t | --- | --- |
\t | baz | bim |
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n\n\n]",
        "[para(2,7):\n\t \n\t \n\t ]",
        "[text(2,7):def\n| foo | bar |\n| --- | --- |\n| baz | bim |::\n\n\n]",
        "[end-para:::True]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def
| foo | bar |
| --- | --- |
| baz | bim |</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_ordered_double_list_two_spaces() -> (
    None
):
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """1. abc
   1. def
\t  | foo | bar |
\t  | --- | --- |
\t  | baz | bim |
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[para(1,4):]",
        "[text(1,4):abc:]",
        "[end-para:::True]",
        "[olist(2,4):.:1:6:   :\n\n\n]",
        "[para(2,7):]",
        "[text(2,7):def:]",
        "[end-para:::True]",
        "[table(3,7)]",
        "[table-header(3,7)]",
        "[table-header-item(3,7)]",
        "[text(3,7):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(3,7)]",
        "[text(3,7):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,7)]",
        "[table-row(3,7)]",
        "[table-row-item(3,7)]",
        "[text(3,7):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(3,7)]",
        "[text(3,7):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(6,1):]",
        "[end-olist:::True]",
        "[end-olist:::True]",
    ]
    expected_gfm = """<ol>
<li>abc
<ol>
<li>def<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ol>
</li>
</ol>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_block_quotes_x1() -> None:
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
\t| foo | bar |
\t| --- | --- |
\t| baz | bim |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n\n\n]",
        "[para(1,3):\n\n\t\n\t\n\t]",
        "[text(1,3):abc\ndef\n| foo | bar |\n| --- | --- |\n| baz | bim |::\n\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
| foo | bar |
| --- | --- |
| baz | bim |</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_block_quotes_x2() -> None:
    """
    Test case:  LRD preceeded by spaces and tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
  \t| foo | bar |
  \t| --- | --- |
  \t| baz | bim |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n\n\n\n]",
        "[para(1,3):\n\n  \t\n  \t\n  \t]",
        "[text(1,3):abc\ndef\n| foo | bar |\n| --- | --- |\n| baz | bim |::\n\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def
| foo | bar |
| --- | --- |
| baz | bim |</p>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_block_quotes_repeat() -> None:
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> def
>\t| foo | bar |
>\t| --- | --- |
>\t| baz | bim |

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n>\n>\n>]",
        "[para(1,3):\n]",
        "[text(1,3):abc\ndef::\n]",
        "[end-para:::True]",
        "[table(3,5)]",
        "[table-header(3,5)]",
        "[table-header-item(3,5)]",
        "[text(3,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(3,5)]",
        "[text(3,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,5)]",
        "[table-row(3,5)]",
        "[table-row-item(3,5)]",
        "[text(3,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(3,5)]",
        "[text(3,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-block-quote:::False]",
        "[BLANK(6,1):]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<blockquote>
<p>abc
def</p>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_block_quotes_bare_repeat() -> None:
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\t| foo | bar |
>\t| --- | --- |
>\t| baz | bim |

"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>]",
        "[table(1,5)]",
        "[table-header(1,5)]",
        "[table-header-item(1,5)]",
        "[text(1,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,5)]",
        "[text(1,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,5)]",
        "[table-row(1,5)]",
        "[table-row-item(1,5)]",
        "[text(1,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,5)]",
        "[text(1,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-block-quote:::False]",
        "[BLANK(4,1):]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_block_quotes_bare_with_many_tabs() -> (
    None
):
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """>\t|\tfoo\t|\tbar\t|
>\t|\t---\t|\t---\t|
>\t|\tbaz\t|\tbim\t|"""
    expected_tokens = [
        "[block-quote(1,1)::>\n>\n>]",
        "[table(1,5)]",
        "[table-header(1,5)]",
        "[table-header-item(1,5)]",
        "[text(1,5):foo:]",
        "[end-table-header-item:\t|::False]",
        "[table-header-item(1,5)]",
        "[text(1,5):bar:]",
        "[end-table-header-item:\t|::False]",
        "[end-table-header:::False]",
        "[table-body(1,5)]",
        "[table-row(1,5)]",
        "[table-row-item(1,5)]",
        "[text(1,5):baz:]",
        "[end-table-row-item:\t|::False]",
        "[table-row-item(1,5)]",
        "[text(1,5):bim:]",
        "[end-table-row-item:\t|::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-block-quote:::True]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_block_quotes_bare_with_space_repeat_1a() -> (
    None
):
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> \t| foo | bar |
> \t| --- | --- |
> \t| baz | bim |

"""
    expected_tokens = [
        "[block-quote(1,1)::> \n> \n> ]",
        "[table(1,5)]",
        "[table-header(1,5)]",
        "[table-header-item(1,5)]",
        "[text(1,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(1,5)]",
        "[text(1,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(1,5)]",
        "[table-row(1,5)]",
        "[table-row-item(1,5)]",
        "[text(1,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(1,5)]",
        "[text(1,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[end-block-quote:::False]",
        "[BLANK(4,1):]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_double_block_quotes() -> None:
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
\t| foo | bar |
\t| --- | --- |
\t| baz | bim |
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n\n\n\n]",
        "[para(2,5):\n\t\n\t\n\t]",
        "[text(2,5):def\n| foo | bar |\n| --- | --- |\n| baz | bim |::\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
| foo | bar |
| --- | --- |
| baz | bim |</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_tables_with_tabs_before_within_double_block_quotes_with_single_x() -> (
    None
):
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
>\t| foo | bar |
>\t| --- | --- |
>\t| baz | bim |
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n>\n> \n> \n]",
        "[para(2,5):\n\t\n  \n  ]",
        "[text(2,5):def\n| foo | bar |\n| --- | --- |\n| baz | bim |::\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
| foo | bar |
| --- | --- |
| baz | bim |</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
        show_debug=True,
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_tables_with_tabs_before_within_double_block_quotes_with_single_a() -> (
    None
):
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """> abc
> > def
>\t# heading
"""
    expected_tokens = [
        "[block-quote(1,1)::> ]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[block-quote(2,1)::> > \n>\n> \n> \n]",
        "[para(2,5):\n\t\n  \n  ]",
        "[text(2,5):def\n| foo | bar |\n| --- | --- |\n| baz | bim |::\n\n\n]",
        "[end-para:::True]",
        "[end-block-quote:::True]",
        "[end-block-quote:::True]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<p>abc</p>
<blockquote>
<p>def
| foo | bar |
| --- | --- |
| baz | bim |</p>
</blockquote>
</blockquote>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_tabs_before_within_list_single_over_two_lines_b() -> (
    None
):
    """
    Test case:  LRD preceeded by tabs.
    """

    # Arrange
    source_markdown = """- abc
  - def

  \t| foo | bar |
  \t| --- | --- |
  \t| baz | bim |

[fred]"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :\n  \n  \n  \n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[table(4,5)]",
        "[table-header(4,5)]",
        "[table-header-item(4,5)]",
        "[text(4,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(4,5)]",
        "[text(4,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(4,5)]",
        "[table-row(4,5)]",
        "[table-row-item(4,5)]",
        "[text(4,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(4,5)]",
        "[text(4,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[para(8,1):]",
        "[text(8,1):[fred]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<ul>
<li>abc
<ul>
<li>def<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>
</li>
</ul>
</li>
</ul>
<p>[fred]</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_too_many_spaces_before() -> None:
    """
    Test case:  LRD preceeded by tabs.

    test_whitespaces_lrd_with_too_many_spaces_before
    """

    # Arrange
    source_markdown = """    | foo | bar |
    | --- | --- |
    | baz | bim |"""
    expected_tokens = [
        "[icode-block(1,5):    :\n    \n    ]",
        "[text(1,5):| foo | bar |\n| --- | --- |\n| baz | bim |:]",
        "[end-icode-block:::True]",
    ]
    expected_gfm = """<pre><code>| foo | bar |
| --- | --- |
| baz | bim |
</code></pre>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_tables_with_too_many_spaces_before_after_first() -> None:
    """
    Test case:  LRD preceeded by tabs.

    test_whitespaces_lrd_with_too_many_spaces_before_after_first
    """

    # Arrange
    source_markdown = """| foo | bar |
    | --- | --- |
    | baz | bim |"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[para(1,3):]",
        "[text(1,3):abc:]",
        "[end-para:::True]",
        "[ulist(2,3):-::4:  :\n  \n  \n  \n]",
        "[para(2,5):]",
        "[text(2,5):def:]",
        "[end-para:::True]",
        "[BLANK(3,1):]",
        "[table(4,5)]",
        "[table-header(4,5)]",
        "[table-header-item(4,5)]",
        "[text(4,5):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(4,5)]",
        "[text(4,5):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(4,5)]",
        "[table-row(4,5)]",
        "[table-row-item(4,5)]",
        "[text(4,5):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(4,5)]",
        "[text(4,5):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(7,1):]",
        "[end-ulist:::True]",
        "[end-ulist:::True]",
        "[para(8,1):]",
        "[text(8,1):[fred]:]",
        "[end-para:::True]",
    ]
    expected_gfm = """<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_increasing_spaces_before() -> None:
    """
    Test case:  Tables preceeded by tabs.

    test_link_reference_definitions_162
    """

    # Arrange
    source_markdown = """   | foo | bar |\a
      | --- | --- |\a\a
           | baz | bim |\a\a
""".replace(
        "\a", " "
    )
    expected_tokens = [
        "[para(1,4):   \n      \n           :  ]",
        "[text(1,4):| foo | bar |\n| --- | --- |:: \n]",
        "[hard-break(2,20):  :\n]",
        "[text(3,12):| baz | bim |:]",
        "[end-para:::True]",
        "[BLANK(4,1):]",
    ]
    expected_gfm = """<p>| foo | bar | 
| --- | --- |<br />
| baz | bim |</p>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_paragraph_before() -> None:
    """
    Test case:  Tables with paragraph before.

    test_link_reference_definitions_182
    """

    # Arrange
    source_markdown = """this is a paragraph
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[para(1,1):]",
        "[text(1,1):this is a paragraph:]",
        "[end-para:::True]",
        "[table(2,1)]",
        "[table-header(2,1)]",
        "[table-header-item(2,1)]",
        "[text(2,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,1)]",
        "[text(2,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,1)]",
        "[table-row(2,1)]",
        "[table-row-item(2,1)]",
        "[text(2,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,1)]",
        "[text(2,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<p>this is a paragraph</p>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_atx_before() -> None:
    """
    Test case:  Tables with atx heading before.

    test_link_reference_definitions_183x
    """

    # Arrange
    source_markdown = """# this is a heading
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[atx(1,1):1:0:]",
        "[text(1,3):this is a heading: ]",
        "[end-atx::]",
        "[table(2,1)]",
        "[table-header(2,1)]",
        "[table-header-item(2,1)]",
        "[text(2,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,1)]",
        "[text(2,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,1)]",
        "[table-row(2,1)]",
        "[table-row-item(2,1)]",
        "[text(2,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,1)]",
        "[text(2,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<h1>this is a heading</h1>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_thematic_before() -> None:
    """
    Test case:  Tables with thematic break before.

    test_link_reference_definitions_183a
    """

    # Arrange
    source_markdown = """---
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[tbreak(1,1):-::---]",
        "[table(2,1)]",
        "[table-header(2,1)]",
        "[table-header-item(2,1)]",
        "[text(2,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,1)]",
        "[text(2,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,1)]",
        "[table-row(2,1)]",
        "[table-row-item(2,1)]",
        "[text(2,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,1)]",
        "[text(2,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<hr />
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_setext_before() -> None:
    """
    Test case:  Tables with setext heading before.

    test_link_reference_definitions_183b
    """

    # Arrange
    source_markdown = """abcde
=====
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[setext(2,1):=:5::(1,1)]",
        "[text(1,1):abcde:]",
        "[end-setext::]",
        "[table(3,1)]",
        "[table-header(3,1)]",
        "[table-header-item(3,1)]",
        "[text(3,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(3,1)]",
        "[text(3,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,1)]",
        "[table-row(3,1)]",
        "[table-row-item(3,1)]",
        "[text(3,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(3,1)]",
        "[text(3,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<h1>abcde</h1>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_indented_code_block_before() -> None:
    """
    Test case:  Tables with indented code block before.

    test_link_reference_definitions_183c
    """

    # Arrange
    source_markdown = """    this is indented code
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[icode-block(1,5):    :]",
        "[text(1,5):this is indented code:]",
        "[end-icode-block:::False]",
        "[table(2,1)]",
        "[table-header(2,1)]",
        "[table-header-item(2,1)]",
        "[text(2,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,1)]",
        "[text(2,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,1)]",
        "[table-row(2,1)]",
        "[table-row-item(2,1)]",
        "[text(2,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,1)]",
        "[text(2,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<pre><code>this is indented code
</code></pre>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_fenced_code_block_before() -> None:
    """
    Test case:  Tables with fenced code block before.

    test_link_reference_definitions_183d
    """

    # Arrange
    source_markdown = """```text
this is indented code
```
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[fcode-block(1,1):`:3:text:::::]",
        "[text(2,1):this is indented code:]",
        "[end-fcode-block:::3:False]",
        "[table(4,1)]",
        "[table-header(4,1)]",
        "[table-header-item(4,1)]",
        "[text(4,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(4,1)]",
        "[text(4,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(4,1)]",
        "[table-row(4,1)]",
        "[table-row-item(4,1)]",
        "[text(4,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(4,1)]",
        "[text(4,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<pre><code class="language-text">this is indented code
</code></pre>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_html_block_before() -> None:
    """
    Test case:  Tables with mhtl block before.

    test_link_reference_definitions_183e
    """

    # Arrange
    source_markdown = """<script>
<~-- javascript comment -->
</script>
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[html-block(1,1)]",
        "[text(1,1):<script>\n<~-- javascript comment -->\n</script>:]",
        "[end-html-block:::False]",
        "[table(4,1)]",
        "[table-header(4,1)]",
        "[table-header-item(4,1)]",
        "[text(4,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(4,1)]",
        "[text(4,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(4,1)]",
        "[table-row(4,1)]",
        "[table-row-item(4,1)]",
        "[text(4,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(4,1)]",
        "[text(4,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(7,1):]",
    ]
    expected_gfm = """<script>
<~-- javascript comment -->
</script>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_block_quote_before_with_blank_in_bq() -> None:
    """
    Test case:  Tables with block quote before.

    test_link_reference_definitions_183fa
    """

    # Arrange
    source_markdown = """> this is a block quote
>
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>]",
        "[para(1,3):]",
        "[text(1,3):this is a block quote:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[end-block-quote:::True]",
        "[table(3,1)]",
        "[table-header(3,1)]",
        "[table-header-item(3,1)]",
        "[text(3,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(3,1)]",
        "[text(3,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,1)]",
        "[table-row(3,1)]",
        "[table-row-item(3,1)]",
        "[text(3,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(3,1)]",
        "[text(3,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is a block quote</p>
</blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_block_quote_before_with_only_blank_in_bq() -> None:
    """
    Test case:  Tables with block quote before.

    test_link_reference_definitions_183fb
    """

    # Arrange
    source_markdown = """>
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[block-quote(1,1)::>]",
        "[BLANK(1,2):]",
        "[end-block-quote:::True]",
        "[table(2,1)]",
        "[table-header(2,1)]",
        "[table-header-item(2,1)]",
        "[text(2,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,1)]",
        "[text(2,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,1)]",
        "[table-row(2,1)]",
        "[table-row-item(2,1)]",
        "[text(2,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,1)]",
        "[text(2,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<blockquote>
</blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_tables_with_block_quote_before_with_no_blank_in_bq() -> None:
    """
    Test case:  Tables with block quote before.

    test_link_reference_definitions_183fx
    """

    # Arrange
    source_markdown = """> this is a block quote
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>]",
        "[para(1,3):]",
        "[text(1,3):this is a block quote:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[end-block-quote:::True]",
        "[table(3,1)]",
        "[table-header(3,1)]",
        "[table-header-item(3,1)]",
        "[text(3,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(3,1)]",
        "[text(3,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,1)]",
        "[table-row(3,1)]",
        "[table-row-item(3,1)]",
        "[text(3,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(3,1)]",
        "[text(3,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<blockquote>
<p>this is a block quote</p>
</blockquote>
<table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_unordered_list_before_with_blank_in_list() -> None:
    """
    Test case:  Tables with unordered list before.

    test_link_reference_definitions_183gxb
    """

    # Arrange
    source_markdown = """- this is a block quote

| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[ulist(1,1):-::2::]",
        "[para(1,3):]",
        "[text(1,3):this is a block quote:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[end-ulist:::True]",
        "[table(3,1)]",
        "[table-header(3,1)]",
        "[table-header-item(3,1)]",
        "[text(3,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(3,1)]",
        "[text(3,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,1)]",
        "[table-row(3,1)]",
        "[table-row-item(3,1)]",
        "[text(3,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(3,1)]",
        "[text(3,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ul>
<li>this is a block quote</li>
</ul><table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_unordered_before_with_only_blank_in_list() -> None:
    """
    Test case:  Tables with block quote before.

    test_link_reference_definitions_183gxa
    """

    # Arrange
    source_markdown = """-
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[ulist(1,1):-::2:]",
        "[BLANK(1,2):]",
        "[end-ulist:::True]",
        "[table(2,1)]",
        "[table-header(2,1)]",
        "[table-header-item(2,1)]",
        "[text(2,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,1)]",
        "[text(2,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,1)]",
        "[table-row(2,1)]",
        "[table-row-item(2,1)]",
        "[text(2,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,1)]",
        "[text(2,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ul>
<li></li>
</ul><table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_tables_with_unordered_before_with_no_blank_in_list() -> None:
    """
    Test case:  Tables with block quote before.

    test_link_reference_definitions_183gxx
    """

    # Arrange
    source_markdown = """- this is a block quote
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>]",
        "[para(1,3):]",
        "[text(1,3):this is a block quote:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[end-block-quote:::True]",
        "[table(3,1)]",
        "[table-header(3,1)]",
        "[table-header-item(3,1)]",
        "[text(3,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(3,1)]",
        "[text(3,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,1)]",
        "[table-row(3,1)]",
        "[table-row-item(3,1)]",
        "[text(3,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(3,1)]",
        "[text(3,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ul>
<li>
<p>this is a block quote</p>
</li>
</ul><table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_ordered_list_before_with_blank_in_list() -> None:
    """
    Test case:  Tables with unordered list before.

    test_link_reference_definitions_183gxc
    """

    # Arrange
    source_markdown = """1. this is a block quote

| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[olist(1,1):.:1:3::]",
        "[para(1,4):]",
        "[text(1,4):this is a block quote:]",
        "[end-para:::True]",
        "[BLANK(2,1):]",
        "[end-olist:::True]",
        "[table(3,1)]",
        "[table-header(3,1)]",
        "[table-header-item(3,1)]",
        "[text(3,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(3,1)]",
        "[text(3,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,1)]",
        "[table-row(3,1)]",
        "[table-row-item(3,1)]",
        "[text(3,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(3,1)]",
        "[text(3,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ol>
<li>this is a block quote</li>
</ol><table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
def test_whitespaces_tables_with_ordered_before_with_only_blank_in_list() -> None:
    """
    Test case:  Tables with block quote before.

    test_link_reference_definitions_183gxe
    """

    # Arrange
    source_markdown = """1.
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[olist(1,1):.:1:3:]",
        "[BLANK(1,3):]",
        "[end-olist:::True]",
        "[table(2,1)]",
        "[table-header(2,1)]",
        "[table-header-item(2,1)]",
        "[text(2,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(2,1)]",
        "[text(2,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(2,1)]",
        "[table-row(2,1)]",
        "[table-row-item(2,1)]",
        "[text(2,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(2,1)]",
        "[text(2,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(5,1):]",
    ]
    expected_gfm = """<ol>
<li></li>
</ol><table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )


@pytest.mark.gfm
@pytest.mark.skip
def test_whitespaces_tables_with_ordered_before_with_no_blank_in_list() -> None:
    """
    Test case:  Tables with block quote before.

    test_link_reference_definitions_183gxd
    """

    # Arrange
    source_markdown = """1. this is a block quote
| foo | bar |
| --- | --- |
| baz | bim |
"""
    expected_tokens = [
        "[block-quote(1,1)::> \n>]",
        "[para(1,3):]",
        "[text(1,3):this is a block quote:]",
        "[end-para:::True]",
        "[BLANK(2,2):]",
        "[end-block-quote:::True]",
        "[table(3,1)]",
        "[table-header(3,1)]",
        "[table-header-item(3,1)]",
        "[text(3,1):foo:]",
        "[end-table-header-item: |::False]",
        "[table-header-item(3,1)]",
        "[text(3,1):bar:]",
        "[end-table-header-item: |::False]",
        "[end-table-header:::False]",
        "[table-body(3,1)]",
        "[table-row(3,1)]",
        "[table-row-item(3,1)]",
        "[text(3,1):baz:]",
        "[end-table-row-item: |::False]",
        "[table-row-item(3,1)]",
        "[text(3,1):bim:]",
        "[end-table-row-item: |::False]",
        "[end-table-row:::False]",
        "[end-table-body:::False]",
        "[end-table:::False]",
        "[BLANK(6,1):]",
    ]
    expected_gfm = """<ul>
<li>
<p>this is a block quote</p>
</li>
</ul><table>
<thead>
<tr>
<th>foo</th>
<th>bar</th>
</tr>
</thead>
<tbody>
<tr>
<td>baz</td>
<td>bim</td>
</tr>
</tbody>
</table>"""

    # Act & Assert
    act_and_assert(
        source_markdown,
        expected_gfm,
        expected_tokens,
        config_map=config_map,
    )
