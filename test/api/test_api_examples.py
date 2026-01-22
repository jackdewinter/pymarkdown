import os
import sys
from test.utils import assert_that_exception_is_raised
from typing import List

import pytest

from pymarkdown.api import (
    PyMarkdownApi,
    PyMarkdownApiException,
    PyMarkdownApiNoFilesFoundException,
)


def test_api_api_basics_example(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test to make sure that we can retrieve the application version.
    """

    # Arrange
    source_path = "some-manner-of-path"

    # Act
    assert_that_exception_is_raised(
        PyMarkdownApiNoFilesFoundException,
        "No matching files found.",
        PyMarkdownApi().scan_path,
        source_path,
    )


def test_api_exceptions_example_bad(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test to make sure that if there is nothing to scan, this will report it.
    """

    source_path = "some-manner-of-path"
    try:
        PyMarkdownApi().scan_path(source_path)
        did_complete = True
    except PyMarkdownApiException as this_exception:
        print(f"API Exception: {this_exception}", file=sys.stderr)
        did_complete = False

    assert (
        caplog.text
        == """WARNING  pymarkdown.main:main.py:343 Provided path 'some-manner-of-path' does not exist.
"""
    )
    assert not did_complete


@pytest.mark.timeout(30)
def test_api_exceptions_example_good_directory_no_markdown_files(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Test to make sure that if there is a valid directory to scan, just no markdown files.
    """

    source_path = os.path.join(".", "newdocs")
    caught_exception = None
    try:
        PyMarkdownApi().scan_path(source_path)
    except PyMarkdownApiNoFilesFoundException as this_exception:
        caught_exception = this_exception

    assert caught_exception
    assert str(caught_exception) == "No matching files found."
    assert caplog.text == ""


@pytest.mark.timeout(60)
def test_api_exceptions_example_good_directory_markdown_files(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """
    Test to make sure that if there is a valid directory to scan, just no markdown files.
    """

    source_path = os.path.join(".", "newdocs", "src")
    try:
        PyMarkdownApi().scan_path(source_path)
        did_complete = True
    except PyMarkdownApiException as this_exception:
        print(f"API Exception: {this_exception}", file=sys.stderr)
        did_complete = False

    assert did_complete
    assert caplog.text == ""


def test_api_positive_results(
    caplog: pytest.LogCaptureFixture, capsys: pytest.CaptureFixture[str]
) -> None:
    """
    Test to make sure that we test the "sample.md" and the output
    from the API documentation.
    """

    resource_path = os.path.join(
        "test", "resources", "apis", "positive_results_sample.md"
    )

    try:
        scan_result = PyMarkdownApi().scan_path(resource_path)

        print(scan_result.scan_failures)
        print(scan_result.pragma_errors)

        did_complete = True
    except PyMarkdownApiException as this_exception:
        print(f"API Exception: {this_exception}", file=sys.stderr)
        did_complete = False

    assert did_complete
    assert caplog.text == ""
    captured = capsys.readouterr()
    assert captured.out == "[]\n[]\n"


def test_api_scan_failures(
    caplog: pytest.LogCaptureFixture, capsys: pytest.CaptureFixture[str]
) -> None:
    """
    Test to make sure that we test a modified "sample.md" and the output
    from the API documentation. This modification should cause Rule Md047
    to fire.
    """

    resource_path = os.path.join("test", "resources", "apis", "scan_failures_sample.md")

    try:
        scan_result = PyMarkdownApi().scan_path(resource_path)
        resource_path = os.path.abspath(resource_path)

        print(scan_result.scan_failures)
        print(scan_result.pragma_errors)

        did_complete = True
    except PyMarkdownApiException as this_exception:
        print(f"API Exception: {this_exception}", file=sys.stderr)
        did_complete = False

    assert did_complete
    assert caplog.text == ""
    captured = capsys.readouterr()
    modified_resource_path = resource_path.replace("\\", "\\\\")
    assert (
        captured.out
        == f"[PyMarkdownScanFailure(scan_file='{modified_resource_path}', line_number=3, column_number=18, rule_id='MD047', rule_name='single-trailing-newline', rule_description='Each file should end with a single newline character.', extra_error_information='')]\n[]\n"
    )


def test_api_extra_information(
    caplog: pytest.LogCaptureFixture, capsys: pytest.CaptureFixture[str]
) -> None:
    """
    Test to make sure that we test a modified "sample.md" that has extra
    information in its failure object.
    """

    resource_path = os.path.join(
        "test", "resources", "apis", "extra_information_sample.md"
    )

    try:
        scan_result = PyMarkdownApi().scan_path(resource_path)
        resource_path = os.path.abspath(resource_path)

        print(scan_result.scan_failures)
        print(scan_result.pragma_errors)

        did_complete = True
    except PyMarkdownApiException as this_exception:
        print(f"API Exception: {this_exception}", file=sys.stderr)
        did_complete = False

    assert did_complete
    assert caplog.text == ""
    captured = capsys.readouterr()
    modified_resource_path = resource_path.replace("\\", "\\\\")
    assert (
        captured.out
        == f"[PyMarkdownScanFailure(scan_file='{modified_resource_path}', line_number=3, column_number=2, rule_id='MD007', rule_name='ul-indent', rule_description='Unordered list indentation', extra_error_information=' [Expected: 0, Actual=1]')]\n[]\n"
    )


def test_api_pragma_failures(
    caplog: pytest.LogCaptureFixture, capsys: pytest.CaptureFixture[str]
) -> None:
    """
    Test to make sure that we test a modified "sample.md" with a malformed pragma.
    """

    resource_path = os.path.join(
        "test", "resources", "apis", "pragma_failures_sample.md"
    )

    try:
        scan_result = PyMarkdownApi().scan_path(resource_path)
        resource_path = os.path.abspath(resource_path)

        print(scan_result.scan_failures)
        print(scan_result.pragma_errors)

        did_complete = True
    except PyMarkdownApiException as this_exception:
        print(f"API Exception: {this_exception}", file=sys.stderr)
        did_complete = False

    assert did_complete
    assert caplog.text == ""
    captured = capsys.readouterr()
    modified_resource_path = resource_path.replace("\\", "\\\\")
    assert (
        captured.out
        == f"""[PyMarkdownScanFailure(scan_file='{modified_resource_path}', line_number=4, column_number=2, rule_id='MD007', rule_name='ul-indent', rule_description='Unordered list indentation', extra_error_information=' [Expected: 0, Actual=1]')]
[PyMarkdownPragmaError(file_path='{modified_resource_path}', line_number=3, pragma_error="Inline configuration command 'disable-next-line' unable to find a plugin with the id 'invalid'.")]
"""
    )


def test_api_scan_with_exclusions() -> None:
    """
    Test to make sure that scanning for files that match a given glob and do
    match a given exclusion pattern produces reliable results.
    """

    # Arrange
    base_path = os.path.join("test", "resources", "rules", "md001")
    source_path = os.path.join(base_path, "*.md")
    expected_relative_paths: List[str] = [
        "empty.md",
        "front_matter_with_alternate_title.md",
        "front_matter_with_no_title.md",
        "front_matter_with_title.md",
        "proper_atx_heading_incrementing.md",
        "proper_setext_heading_incrementing.md",
    ]
    expected_paths: List[str] = []
    for i in expected_relative_paths:
        expected_paths.append(os.path.join(os.path.abspath(base_path), i))

    # Act
    scan_result = PyMarkdownApi().scan_path(
        source_path, exclude_patterns=["*improper*", "*front*"]
    )

    # Assert
    assert not scan_result.critical_errors
    assert not scan_result.pragma_errors
    assert scan_result.scan_failures and len(scan_result.scan_failures) == 2

    assert scan_result.scan_failures[0].scan_file == os.path.join(
        os.path.abspath(base_path), "proper_setext_heading_incrementing.md"
    )
    assert scan_result.scan_failures[0].line_number == 7
    assert scan_result.scan_failures[0].column_number == 1
    assert scan_result.scan_failures[0].rule_id == "MD003"

    assert scan_result.scan_failures[1].scan_file == os.path.join(
        os.path.abspath(base_path), "proper_setext_heading_incrementing.md"
    )
    assert scan_result.scan_failures[1].line_number == 9
    assert scan_result.scan_failures[1].column_number == 1
    assert scan_result.scan_failures[1].rule_id == "MD003"


def test_api_scan_with_file_does_not_exist() -> None:
    """
    Test to make sure that scanning for files that match a given glob and do
    match a given exclusion pattern produces reliable results.
    """

    # Arrange
    base_path = os.path.join("test", "resources", "rules", "md001")
    source_path = os.path.join(base_path, "blah.abc")
    assert not os.path.exists(source_path)

    # Act
    caught_exception = None
    try:
        _ = PyMarkdownApi().scan_path(source_path)
    except PyMarkdownApiNoFilesFoundException as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception is not None
