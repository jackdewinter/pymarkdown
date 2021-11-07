"""
Module to provide tests related to the dial home helper for the scanner.
"""
import datetime
import os
import tempfile
from test.markdown_scanner import MarkdownScanner

from pymarkdown.dial_home_helper import DialHomeHelper
from pymarkdown.main import PyMarkdownLint


def test_dialhome_basic():
    """
    Basic test of dialing home and verifying that the current version is the
    same as the published version.
    """

    # Arrange
    temp_file = None
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        log_file_name = temp_file.name
    try:
        scanner = MarkdownScanner()
        supplied_arguments = [
            "--log-level",
            "INFO",
            "--log-file",
            log_file_name,
            "--force-version",
            "plugins",
            "info",
            "BAD000",
        ]

        expected_return_code = 1
        expected_output = "Unable to find a plugin with an id or name of 'BAD000'."
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(
            arguments=supplied_arguments,
            disable_version_checking=False,
            suppress_first_line_heading_rule=False,
        )

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )

        with open(log_file_name) as file:
            file_data = file.read()
        split_file_data = file_data.split("\n")
        assert len(split_file_data) > 2
        assert (
            split_file_data[0]
            == "Looking for semantic version information in standard location."
        )
        assert split_file_data[1] == "Semantic version for calling module is '0.9.2'."
        assert split_file_data[2].startswith("extension front-matter:")
    finally:
        if os.path.exists(log_file_name):
            os.remove(log_file_name)


def test_dialhome_mock_failure():
    """
    Basic test of dialing home with a mock failure when trying to retrieve the
    version from the web page.
    """

    # Arrange
    scanner = MarkdownScanner()
    supplied_arguments = [
        "-x-version",
        "--force-version",
        "plugins",
        "info",
        "BAD000",
    ]

    expected_return_code = 1
    expected_output = (
        "WARN: Cannot retrive the published package version: "
        + "Fetch webpage error: 404 Client Error: "
        + "Not Found for url: https://pypi.org/project/pymarkdownlntxxxxxx/\n"
        + "Unable to find a plugin with an id or name of 'BAD000'."
    )
    expected_error = ""

    # Act
    execute_results = scanner.invoke_main(
        arguments=supplied_arguments,
        disable_version_checking=False,
        suppress_first_line_heading_rule=False,
    )

    # Assert
    execute_results.assert_results(
        expected_output, expected_error, expected_return_code
    )


def test_dialhome_versions_equal():
    """
    Test to verify that the version number that the executable reports and the
    version that the `get_semantic_version_from_version_module` function reports
    are equal.
    """

    # Arrange
    dial_home_helper = DialHomeHelper("not-a-valid-package-name")
    scanner = MarkdownScanner()
    supplied_arguments = [
        "version",
    ]

    # Act
    execute_results = scanner.invoke_main(arguments=supplied_arguments)
    (
        module_version,
        version_error,
    ) = dial_home_helper.get_semantic_version_from_version_module("../pymarkdown")

    # Assert
    executable_version = execute_results.std_out.getvalue().strip()
    assert (
        execute_results.return_code == 0
    ), f"Version command failed to execute: {execute_results.return_code}"

    assert not version_error, f"Error extraction version from module: {version_error}"
    assert module_version, "Module version was not extracted from the current module."
    assert (
        module_version == executable_version
    ), f"Embedded version {module_version} and executed version {executable_version} were different."


def test_dialhome_versions_bad_relative_path():
    """
    Test to verify that helper will fail gracefully if the correct path to a
    viable python.py file is not specified.
    """

    # Arrange
    dial_home_helper = DialHomeHelper("not-a-valid-package-name")

    # Act
    (
        _,
        version_error,
    ) = dial_home_helper.get_semantic_version_from_version_module()

    # Assert
    assert version_error, "Error should have been logged."
    assert version_error.startswith(
        "AssertionError encountered while determining semantic version: 'Version module file '"
    ), "Error prefix is not as expected."
    assert version_error.endswith(
        "version.py' does not exist.'"
    ), "Error suffix is not as expected."


def test_dialhome_verify_bad_package_name():
    """
    Test to verify that helper fails nicely with a bad pacakge name.
    """

    # Arrange
    dial_home_helper = DialHomeHelper("not-a-valid-package-name")

    # Act
    version_message = dial_home_helper.verify_version_is_currrent(
        "0.0.0", force_version_check=True
    )

    # Assert
    assert version_message, "Error should have been logged."
    assert (
        version_message
        == "WARN: Cannot retrive the published package version: "
        + "Fetch webpage error: 404 Client Error: "
        + "Not Found for url: https://pypi.org/project/not-a-valid-package-name/"
    )


def test_dialhome_verify_good_package_name():
    """
    Test to verify that helper works nicely with a bad pacakge name.
    """

    # Arrange
    dial_home_helper = DialHomeHelper(PyMarkdownLint().package_name)

    # Act
    (
        module_version,
        version_error,
    ) = dial_home_helper.get_semantic_version_from_version_module("../pymarkdown")
    assert module_version
    assert not version_error
    version_message = dial_home_helper.verify_version_is_currrent(
        module_version, force_version_check=True
    )

    # Assert
    assert not version_message, "Error should not have been logged."


class BadWebPageDialHomeHelper(DialHomeHelper):
    """
    Class to simulate a bad web page.
    """

    def fetch_web_page(self, url_to_fetch):
        """
        Fetch the specified web page, reporting an error is there were any
        problems getting the web page.
        """
        _ = url_to_fetch
        return BadWebPageResponse("nothing that matters"), None


class ZeroVersionDialHomeHelper(DialHomeHelper):
    """
    Class to simulate a web page from PyPi.org that has a different version
    number than the current one.
    """

    def fetch_web_page(self, url_to_fetch):
        """
        Fetch the specified web page, reporting an error is there were any
        problems getting the web page.
        """
        _ = url_to_fetch
        return (
            BadWebPageResponse(
                '<h1 class="package-header__name">'
                + PyMarkdownLint().package_name
                + " 0.0.0</h1>"
            ),
            None,
        )


# pylint: disable=too-few-public-methods
class BadWebPageResponse:
    """
    Class to provide for a simulated bad web page response.
    """

    def __init__(self, text_response):
        self.__text_response = text_response

    @property
    def text(self):
        """
        Text encapsulated in the response.
        """
        return self.__text_response


# pylint: enable=too-few-public-methods


def test_dialhome_verify_bad_web_page_contents():
    """
    Test to verify that helper fails gracefully when a bad web page is returned.
    """

    # Arrange
    dial_home_helper = BadWebPageDialHomeHelper(PyMarkdownLint().package_name)

    # Act
    (
        module_version,
        version_error,
    ) = dial_home_helper.get_semantic_version_from_version_module("../pymarkdown")
    assert module_version
    assert not version_error
    version_message = dial_home_helper.verify_version_is_currrent(
        module_version, force_version_check=True
    )

    # Assert
    assert (
        version_message
        == "WARN: Cannot retrive the published package version: "
        + "Semantic version lookup error (AssertionError): "
        + "Start of expected web page content not found at response from pypi.org."
    ), "Expected bad web page format."


def test_dialhome_verify_different_web_page_version():
    """
    Test to verify that helper fails with an easy-to-read message when the
    version number returned is not the same as the module version.
    """

    # Arrange
    dial_home_helper = ZeroVersionDialHomeHelper(PyMarkdownLint().package_name)

    # Act
    (
        module_version,
        version_error,
    ) = dial_home_helper.get_semantic_version_from_version_module("../pymarkdown")
    assert module_version
    assert not version_error
    version_message = dial_home_helper.verify_version_is_currrent(
        module_version, force_version_check=True
    )

    # Assert
    assert (
        version_message
        == "WARN: Current application version '0.0.0' differs from the published version '0.9.2'.\n"
        + "  Please update the pymarkdownlnt application version."
    )


def test_dialhome_with_non_existent_marker_file():
    """
    Test to make sure that dialhome works with a marker file that is not there.
    """

    # Arrange
    dial_home_helper = ZeroVersionDialHomeHelper(PyMarkdownLint().package_name)
    if os.path.exists(dial_home_helper.marker_path):
        os.remove(dial_home_helper.marker_path)

    # Act
    (
        module_version,
        version_error,
    ) = dial_home_helper.get_semantic_version_from_version_module("../pymarkdown")
    assert module_version
    assert not version_error
    version_message = dial_home_helper.verify_version_is_currrent(
        module_version, force_version_check=False
    )

    # Assert
    assert (
        version_message
        == "WARN: Current application version '0.0.0' differs from the published version '0.9.2'.\n"
        + "  Please update the pymarkdownlnt application version."
    )


def test_dialhome_with_bad_marker_file():
    """
    Test to make sure that dialhome works with a marker file that contains bad information.
    """

    # Arrange
    dial_home_helper = ZeroVersionDialHomeHelper(PyMarkdownLint().package_name)
    with open(dial_home_helper.marker_path, "wt") as marker_file:
        marker_file.write("something that is not an epoch\n")

    # Act
    (
        module_version,
        version_error,
    ) = dial_home_helper.get_semantic_version_from_version_module("../pymarkdown")
    assert module_version
    assert not version_error
    version_message = dial_home_helper.verify_version_is_currrent(
        module_version, force_version_check=False
    )

    # Assert
    assert (
        version_message
        == "WARN: Current application version '0.0.0' differs from the published version '0.9.2'.\n"
        + "  Please update the pymarkdownlnt application version."
    )


def test_dialhome_with_day_old_marker_file():
    """
    Test to make sure that dialhome works with a marker file that is a day old.
    """

    # Arrange
    dial_home_helper = ZeroVersionDialHomeHelper(PyMarkdownLint().package_name)
    marker_timestamp = int(datetime.datetime.now().timestamp())
    marker_timestamp -= 60 * 60 * 24
    dial_home_helper.refresh_check_marker(marker_timestamp)

    # Act
    (
        module_version,
        version_error,
    ) = dial_home_helper.get_semantic_version_from_version_module("../pymarkdown")
    assert module_version
    assert not version_error
    version_message = dial_home_helper.verify_version_is_currrent(
        module_version, force_version_check=False
    )

    # Assert
    assert not version_message


def test_dialhome_with_seven_day_old_marker_file():
    """
    Test to make sure that dialhome works with a marker file that is a day old.
    """

    # Arrange
    dial_home_helper = ZeroVersionDialHomeHelper(PyMarkdownLint().package_name)
    marker_timestamp = int(datetime.datetime.now().timestamp())
    marker_timestamp -= (60 * 60 * 24 * 7) + 30
    dial_home_helper.refresh_check_marker(marker_timestamp)

    # Act
    (
        module_version,
        version_error,
    ) = dial_home_helper.get_semantic_version_from_version_module("../pymarkdown")
    assert module_version
    assert not version_error
    version_message = dial_home_helper.verify_version_is_currrent(
        module_version, force_version_check=False
    )

    # Assert
    assert (
        version_message
        == "WARN: Current application version '0.0.0' differs from the published version '0.9.2'.\n"
        + "  Please update the pymarkdownlnt application version."
    )


def test_dialhome_refresh_marker_bad():
    """
    Test to make sure we report an error if unable to write the
    check marker file, but continue.
    """

    # Arrange
    dial_home_helper = DialHomeHelper(PyMarkdownLint().package_name)
    if os.path.exists(dial_home_helper.marker_path):
        if os.path.isfile(dial_home_helper.marker_path):
            os.remove(dial_home_helper.marker_path)
        else:
            os.rmdir(dial_home_helper.marker_path)
    try:
        os.makedirs(dial_home_helper.marker_path)

        # Act
        error_value = dial_home_helper.refresh_check_marker(1)

        # Assert
        assert error_value
    finally:
        if os.path.exists(dial_home_helper.marker_path):
            os.rmdir(dial_home_helper.marker_path)
