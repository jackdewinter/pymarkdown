"""
Dial home helper.
"""
import datetime
import inspect
import logging
import os
import runpy
from pathlib import Path

import requests

LOGGER = logging.getLogger(__name__)


class DialHomeHelper:

    """
    Class to help with the dialing home of the application to see if there are new versions.
    """

    DEFAULT_EXPIRY_IN_DAYS = 7

    __package_info_start_text = '<h1 class="package-header__name">'
    __package_info_end_text = "</h1>"

    __version_file_name = "version.py"
    __version_variable_name = "__version__"

    __base_epoch_timestamp = 1633093200

    def __init__(self, package_name, expiry_in_days=DEFAULT_EXPIRY_IN_DAYS):
        self.__package_name = package_name
        self.__expiry_in_days = expiry_in_days

    # pylint: disable=broad-except
    @classmethod
    def get_semantic_version_from_version_module(cls, relative_path_to_adjust_by=None):
        """
        Use the call stack and standard file locations to load the semantic version.
        """
        registered_semantic_version = None
        LOGGER.info("Looking for semantic version information in standard location.")
        try:
            LOGGER.debug("Inspecting call stack to determine calling information.")
            call_stack = inspect.stack()
            assert len(call_stack) > 1, "Call stack must have more than 1 entry."

            root_script_directory = os.path.dirname(
                os.path.realpath(call_stack[1].filename)
            )
            if relative_path_to_adjust_by:
                root_script_directory = os.path.join(
                    root_script_directory, relative_path_to_adjust_by
                )
                root_script_directory = os.path.realpath(root_script_directory)
            assert os.path.exists(
                root_script_directory
            ), f"Root script directory '{root_script_directory}' does not exist."

            LOGGER.debug(
                "Verifying that version file `%s` exists.", root_script_directory
            )
            version_file_path = os.path.join(
                root_script_directory, DialHomeHelper.__version_file_name
            )
            assert os.path.exists(
                version_file_path
            ), f"Version module file '{version_file_path}' does not exist."
            assert os.path.isfile(
                version_file_path
            ), f"Version module file '{version_file_path}' is not a file."

            LOGGER.debug("Executing version file to extract metadata.")
            version_meta = runpy.run_path(version_file_path)
            assert (
                DialHomeHelper.__version_variable_name in version_meta
            ), f"Version variable '{DialHomeHelper.__version_variable_name}' is not in version module."
            registered_semantic_version = version_meta[
                DialHomeHelper.__version_variable_name
            ]
            LOGGER.info(
                "Semantic version for calling module is '%s'.",
                registered_semantic_version,
            )
            return registered_semantic_version, None
        except Exception as this_exception:
            error_value = f"{type(this_exception).__name__} encountered while determining semantic version: '{this_exception}'"
            LOGGER.error(error_value)
            return None, error_value

    # pylint: enable=broad-except

    @property
    def marker_path(self):
        """
        Get the path to the marker file.
        """
        return os.path.join(Path.home(), f".{self.__package_name}")

    # pylint: disable=broad-except
    def __get_marker_epochs(self):
        marker_epoch_time = 0
        if os.path.exists(self.marker_path):
            try:
                with open(self.marker_path, "rt") as marker_file:
                    file_lines = marker_file.readlines()
                assert len(file_lines) == 1, "Marker file must have only one line."
                file_lines = file_lines[0].strip()
                marker_epoch_time = int(file_lines)
            except Exception as this_exception:
                error_value = f"{type(this_exception).__name__} encountered while checking age of version marker: '{this_exception}'"
                LOGGER.warning(error_value)
        return int(datetime.datetime.now().timestamp()), marker_epoch_time

    # pylint: enable=broad-except

    def __has_check_marker_expired(self):
        current_epoch_time, marker_epoch_time = self.__get_marker_epochs()
        delta_epoch_in_seconds = current_epoch_time - marker_epoch_time
        delta_epoch_in_days = delta_epoch_in_seconds / 60 / 60 / 24
        return (
            marker_epoch_time < DialHomeHelper.__base_epoch_timestamp
            or delta_epoch_in_days >= self.__expiry_in_days
        )

    # pylint: disable=broad-except
    def refresh_check_marker(self, current_timestamp):
        """
        Refresh the check marker to a value containing the current timestamp.
        """
        error_value = None
        marker_line = f"{current_timestamp}\n"
        try:
            with open(self.marker_path, "wt") as marker_file:
                marker_file.write(marker_line)
        except Exception as this_exception:
            error_value = f"{type(this_exception).__name__} encountered while refreshing version marker: '{this_exception}'"
            LOGGER.warning(error_value)
        return error_value

    # pylint: enable=broad-except

    def verify_version_is_currrent(self, current_version, force_version_check=False):
        """
        Verify that the specified version of the module/package is current.
        """
        is_version_check_required = force_version_check
        if not is_version_check_required:
            is_version_check_required = self.__has_check_marker_expired()
        if not is_version_check_required:
            return None

        extract_version, extract_error = self.__get_pypi_package_version()
        if extract_error:
            return (
                f"WARN: Cannot retrive the published package version: {extract_error}"
            )

        if not force_version_check:
            self.refresh_check_marker(int(datetime.datetime.now().timestamp()))

        if current_version != extract_version:
            return (
                f"WARN: Current application version '{extract_version}' differs from the published version '{current_version}'.\n"
                + f"  Please update the {self.__package_name} application version."
            )
        return None

    # pylint: disable=broad-except
    def __get_pypi_package_version(self):

        response, response_error = self.fetch_web_page(
            f"https://pypi.org/project/{self.__package_name}/"
        )
        if response_error:
            return None, f"Fetch webpage error: {response_error}"

        extracted_package_version = None
        try:
            start_text_index = response.text.find(
                DialHomeHelper.__package_info_start_text
            )
            assert (
                start_text_index != -1
            ), "Start of expected web page content not found at response from pypi.org."
            end_text_index = response.text.find(
                DialHomeHelper.__package_info_end_text, start_text_index
            )
            assert (
                end_text_index != -1
            ), "End of expected web page content not found at response from pypi.org."
            useful_content = response.text[
                start_text_index
                + len(DialHomeHelper.__package_info_start_text) : end_text_index
            ].strip()

            split_useful_content = useful_content.split(" ")
            assert (
                len(split_useful_content) == 2
            ), "Extracted webpage content must have two parts separated by spaces."
            assert (
                split_useful_content[0] == self.__package_name
            ), f"Extracted package name '{split_useful_content[0]}' differs from the requested package name '{self.__package_name}'."

            extracted_package_version = split_useful_content[1]
        except Exception as this_exception:
            return (
                None,
                f"Semantic version lookup error ({type(this_exception).__name__}): {this_exception}",
            )

        return extracted_package_version, None

    # pylint: enable=broad-except

    # pylint: disable=no-self-use
    def fetch_web_page(self, url_to_fetch):
        """
        Fetch the specified web page, reporting an error is there were any
        problems getting the web page.
        """
        try:
            response = requests.get(url_to_fetch, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as this_exception:
            return None, this_exception
        return response, None

    # pylint: enable=no-self-use
