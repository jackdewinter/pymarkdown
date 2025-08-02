import os
import sys
from test.utils import assert_that_exception_is_raised

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
        "Provided path 'some-manner-of-path' does not exist.",
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
        == """WARNING  pymarkdown.main:main.py:336 Provided path 'some-manner-of-path' does not exist.
WARNING  pymarkdown.main:main.py:336 No matching files found.
"""
    )
    assert not did_complete


@pytest.mark.timeout(30)
def test_api_exceptions_example_good(caplog: pytest.LogCaptureFixture) -> None:
    """
    Test to make sure that if there is at least one thing to scan,
    the README.md in this case, it will scan it.
    """

    source_path = "."
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
