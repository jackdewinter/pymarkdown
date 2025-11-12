#!/usr/bin/env python

"""Utility to scan PyTest tests for extra code coverage.
"""

import argparse
import io
import json
import logging
import os
import sys
import traceback
from copy import copy
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple, cast
from xml.etree import ElementTree as ET

import pytest
from coverage import Coverage, CoverageData
from coverage.data import add_data_to_hash
from coverage.misc import Hasher

CoverageArc = Tuple[int, int]
"""Type alias for coverage arc provided by coverage.py."""


@dataclass
class FunctionLocation:
    """Data class to represent the location of a test function in a file."""

    file_name: str
    """Name of the file containing the function."""
    line_number: Optional[int]
    """Line number of the function in the file."""
    test_name: str
    """Name of the function."""

    @property
    def function_file_position(self) -> str:
        """Get a string representation of the function location within a file."""
        return f"{self.file_name}:{self.line_number}:1"


class DuplicateCoverageScannerException(Exception):
    """Exception class for errors found when analyzing the code coverage."""


# pylint: disable=too-few-public-methods
class SystemState:
    """
    Class to provide an encapsulation of the system state so that we can restore
    it later.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the SystemState class.
        """

        self.saved_stdin = sys.stdin
        self.saved_stdout = sys.stdout
        self.saved_stderr = sys.stderr
        self.saved_cwd = os.getcwd()
        self.saved_env = os.environ
        self.saved_argv = sys.argv

    def restore(self) -> None:
        """
        Restore the system state variables to what they were before.
        """

        os.chdir(self.saved_cwd)
        os.environ = self.saved_env  # noqa B003
        sys.argv = self.saved_argv
        sys.stdin = self.saved_stdin
        sys.stdout = self.saved_stdout
        sys.stderr = self.saved_stderr


# pylint: enable=too-few-public-methods


@dataclass
class TestCoverage:
    """Data class to represent the coverage information for the measured set of tests."""

    test_function_locations: List[FunctionLocation]
    """List of locations of tests that contributed to this coverage."""
    coverage_arcs_by_file_map: Dict[str, Set[CoverageArc]]
    """Map of file names to sets of coverage arcs covered by the tests in test_function_locations."""

    def __len__(self) -> int:
        """Get the number of arcs in the coverage.

        Mostly used for overlapping calculations
        """
        return sum(map(len, self.coverage_arcs_by_file_map.values()))

    def is_subset_of(self, other_test_coverage: "TestCoverage") -> bool:
        """
        Determine if this TestCoverage is a subset of another TestCoverage.
        """
        # One instance is a subset of another instance if all its arcs are contained in the other.
        # The other test coverage may have additional files/arcs, but as long as all arcs in this
        # instance are in the other, then this is a subset.
        return all(
            file_set.issubset(
                other_test_coverage.coverage_arcs_by_file_map.get(filename, set())
            )
            for filename, file_set in self.coverage_arcs_by_file_map.items()
        )

    def intersect_with(self, other_test_coverage: "TestCoverage") -> "TestCoverage":
        """
        Intersect this TestCoverage with another TestCoverage, producing a new TestCoverage object.
        """
        arc_coverage_map = {
            filename: combined_file_names
            for filename, file_set in self.coverage_arcs_by_file_map.items()
            if filename in other_test_coverage.coverage_arcs_by_file_map
            and (
                combined_file_names := file_set
                & other_test_coverage.coverage_arcs_by_file_map[filename]
            )
        }
        return TestCoverage([], arc_coverage_map)

    def subtract(self, other_test_coverage: "TestCoverage") -> "TestCoverage":
        """
        Produce a new TestCoverage object which is this TestCoverage minus the other TestCoverage.
        """
        arc_coverage_map = {
            filename: resulting_file_set
            for filename, file_set in self.coverage_arcs_by_file_map.items()
            if (
                resulting_file_set := file_set
                - other_test_coverage.coverage_arcs_by_file_map.get(filename, set())
            )
        }
        return TestCoverage([], arc_coverage_map)


class DuplicateCoveragePyTestPlugin:
    """PyTest plugin to collect coverage information for each test function."""

    def __init__(self) -> None:
        self.__current_location: Optional[FunctionLocation] = None
        self.__was_test_skipped = False
        self.__coverage_collector = Coverage(
            branch=True, data_file=None, omit=os.path.basename(__file__)
        )
        self.__is_coverage_valid = False
        self.__fatal_errors: List[Tuple[FunctionLocation, str]] = []
        self.test_coverage_by_hash_map: Dict[str, TestCoverage] = {}

    def get_fatal_errors(self) -> List[Tuple[FunctionLocation, str]]:
        """Determine if any fatal errors were recorded during coverage collection."""
        return self.__fatal_errors[:]

    def pytest_runtest_logstart(
        self, nodeid: str, location: Tuple[str, Optional[int], str]
    ) -> None:
        """Start of a test run for a specific test function."""

        logging.debug(
            "Start of test %s (%s) at %s:%s",
            location[2],
            nodeid,
            location[0],
            location[1],
        )
        self.__current_location = FunctionLocation(
            location[0], location[1], location[2]
        )
        self.__was_test_skipped = False
        self.__is_coverage_valid = True

    def pytest_runtest_logfinish(
        self, nodeid: str, location: Tuple[str, Optional[int], str]
    ) -> None:
        """Finish of a test run for a specific test function."""

        logging.debug(
            "Stop of test %s (%s) at %s:%s",
            location[2],
            nodeid,
            location[0],
            location[1],
        )
        self.__current_location = None
        self.__is_coverage_valid = False

    def pytest_report_teststatus(
        self, report: pytest.TestReport
    ) -> Optional[Tuple[str, str, str]]:
        """Report the test status for a specific test function."""

        if report.when == "setup":
            logging.debug("Starting coverage collection.")
            self.__start_collecting_coverage()
            logging.debug("Started coverage collection.")
        elif report.when == "call":
            self.__was_test_skipped = report.outcome == "skipped"
            logging.debug("Test result: %s", report.outcome)
        elif report.when == "teardown":
            logging.debug("Stopping coverage collection.")
            self.__stop_collecting_coverage()
            logging.debug("Stopped coverage collection.")

    def __mark_test_with_exception(
        self, as_past_verb: str, as_current_verb: str
    ) -> None:
        """Mark the current test as having had an exception during coverage collection."""

        logging.exception(
            "Exception during %s coverage collection. Aborting coverage for this test.",
            as_past_verb,
        )
        self.__is_coverage_valid = False
        assert self.__current_location is not None
        self.__fatal_errors.append(
            (self.__current_location, f"{as_current_verb} exception")
        )

    # pylint: disable=broad-exception-caught
    def __start_collecting_coverage(self) -> None:

        try:
            self.__coverage_collector.erase()
            self.__coverage_collector.start()
        except Exception:
            self.__mark_test_with_exception("starting", "start")

    # pylint: enable=broad-exception-caught

    # pylint: disable=broad-exception-caught
    def __process_coverage_data(self) -> None:
        assert self.__current_location is not None
        try:

            # Get the coverage data object, building a covered_arcs_list collection of all files
            # that have covered arcs. If we have a test that does not cover any arcs, then we are
            # not interested in tracking it.
            current_hasher = Hasher()
            collected_data: CoverageData = self.__coverage_collector.get_data()
            covered_arcs_list: Dict[str, Set[Tuple[int, int]]] = {}
            for file_name in collected_data.measured_files():

                # We do not need to limit this to just the files in the current working directory, as
                # coverage.py will only report files that were specified in the .coveragerc file.
                add_data_to_hash(collected_data, file_name, current_hasher)
                if covered_arcs := set(collected_data.arcs(file_name)):
                    covered_arcs_list[file_name] = covered_arcs
            if not covered_arcs_list:
                return

            # Either add a new hash entry for the coverage data, or append to an existing one.
            # I.e. multiple tests with identical coverage will share the same hash entry, but we
            # want to track all the tests that contributed to that coverage. Note that we do not
            # need to update the coverage arcs list, as they will be identical for all tests with
            # the same hash.
            if (
                text_hash := current_hasher.hexdigest()
            ) in self.test_coverage_by_hash_map:
                self.test_coverage_by_hash_map[
                    text_hash
                ].test_function_locations.append(self.__current_location)
            else:
                self.test_coverage_by_hash_map[text_hash] = TestCoverage(
                    test_function_locations=[self.__current_location],
                    coverage_arcs_by_file_map=covered_arcs_list,
                )

        except Exception:
            self.__mark_test_with_exception("processing", "processing")

    # pylint: enable=broad-exception-caught

    # pylint: disable=broad-exception-caught
    def __stop_collecting_coverage(self) -> None:

        # If the coverage is still valid (i.e. no exceptions), then try and stop the coverage collection.
        try:
            if self.__is_coverage_valid:
                self.__coverage_collector.stop()
                if not self.__was_test_skipped:
                    self.__process_coverage_data()
        except Exception:
            self.__mark_test_with_exception("stopping", "stop")
        finally:
            self.__current_location = None
            self.__was_test_skipped = False

    # pylint: enable=broad-exception-caught


# pylint: disable=too-few-public-methods
class DuplicateCoverageScanner:
    """Class to scan PyTest tests for extra code coverage."""

    def __init__(self) -> None:
        """Initializes a new instance of the DuplicateCoverageScanner class."""
        self.__duplicate_coverage_plugin = DuplicateCoveragePyTestPlugin()

    @staticmethod
    def __is_warning_suppressed(
        suppression_map: Dict[str, Any],
        function_location: FunctionLocation,
        eligible_test_id: str,
        mark_as_used: bool,
    ) -> bool:

        assert function_location.file_name.endswith(".py")
        modified_file_name = (
            function_location.file_name[:-3].replace("/", ".").replace("\\", ".")
        )
        suppression_key = (
            f"{modified_file_name}::{function_location.test_name}::{eligible_test_id}"
        )

        is_suppressed = suppression_key in suppression_map
        if mark_as_used and is_suppressed:
            suppression_map[suppression_key]["used"] = True
        return is_suppressed

    def __output_identical_tests(self, suppression_map: Dict[str, Any]) -> int:

        identical_test_count = 0
        for (
            next_test_coverage
        ) in self.__duplicate_coverage_plugin.test_coverage_by_hash_map.values():

            # print("---")
            # print(",".join((i[len("C:\\enlistments\\pymarkdown\\"):] for i in next_test_coverage.coverage_arcs_by_file_map.keys())))
            # print("---")

            # If tests are identical in their coverage, then their coverage hash will be the same.
            # If we have a single location for the hash, then there is no duplication.
            if len(next_test_coverage.test_function_locations) <= 1:
                continue

            # Look for any identical test locations that are not suppressed, and if we still have
            # more than one, then continue.
            unsuppressed_identical_locations = [
                other_test_location
                for other_test_location in next_test_coverage.test_function_locations
                if not DuplicateCoverageScanner.__is_warning_suppressed(
                    suppression_map, other_test_location, "W001", mark_as_used=True
                )
            ]
            if len(unsuppressed_identical_locations) == 1:
                continue

            sorted_locations = sorted(
                unsuppressed_identical_locations,
                key=lambda x: (x.file_name, x.line_number, x.test_name),
            )
            print(
                f"{sorted_locations[0].function_file_position} I001: identical-coverage '{sorted_locations[0].test_name}': Listed tests have indentical coverage. (duplicate-test)"
            )
            identical_test_count += 1
            for next_unsuppressed_identical_location in sorted_locations[1:]:
                print(
                    f"    {next_unsuppressed_identical_location.function_file_position} W001: identical-to-parent '{next_unsuppressed_identical_location.test_name}': Removal suggested. (duplicated-test)"
                )
            print()
        return identical_test_count

    @staticmethod
    def __create_combined_test_coverage(
        *test_coverages: TestCoverage,
    ) -> TestCoverage:

        arc_coverage_map: Dict[str, Set[CoverageArc]] = {}
        for next_test_coverage in test_coverages:
            for (
                coverage_file_name,
                coverage_arcs,
            ) in next_test_coverage.coverage_arcs_by_file_map.items():
                arc_coverage_map.setdefault(coverage_file_name, set()).update(
                    coverage_arcs
                )
        return TestCoverage([], arc_coverage_map)

    def __calculate_overlapped_hashes_for_current_coverage_object(
        self,
    ) -> List[Tuple[TestCoverage, List[TestCoverage]]]:

        fully_overlapped_sets: List[Tuple[TestCoverage, List[TestCoverage]]] = []

        # Sort the sets by size of test coverage, largest first.
        sorted_sets = sorted(
            (
                TestCoverage(cov.test_function_locations, cov.coverage_arcs_by_file_map)
                for cov in self.__duplicate_coverage_plugin.test_coverage_by_hash_map.values()
            ),
            key=len,
            reverse=True,
        )

        # Grab the next largest set, and see if it is fully covered by the remaining sets.
        while sorted_sets and len(sorted_sets) > 1:
            next_largest_set = sorted_sets.pop(0)

            if not next_largest_set.is_subset_of(
                DuplicateCoverageScanner.__create_combined_test_coverage(*sorted_sets)
            ):
                continue
            related_sets = sorted(
                [
                    other_set
                    for other_set in sorted_sets
                    if other_set.intersect_with(next_largest_set)
                ],
                key=len,
                reverse=True,
            )

            next_largest_set_copy = copy(next_largest_set)
            overlapped_sets: List[TestCoverage] = []
            for related_set in related_sets:
                if not next_largest_set_copy:
                    break
                if next_largest_set_copy.intersect_with(related_set):
                    overlapped_sets.append(related_set)
                    next_largest_set_copy = next_largest_set_copy.subtract(related_set)

            if not next_largest_set_copy:
                fully_overlapped_sets.append((next_largest_set, overlapped_sets))
        return fully_overlapped_sets

    def __output_warnings_for_overlapped_tests(
        self, suppression_map: Dict[str, Any]
    ) -> int:

        overlapped_hashes = (
            self.__calculate_overlapped_hashes_for_current_coverage_object()
        )

        overlapped_test_count = 0
        for base_test, smaller_tests in overlapped_hashes:
            larger_test_location = base_test.test_function_locations[0]
            if DuplicateCoverageScanner.__is_warning_suppressed(
                suppression_map, larger_test_location, "W002", mark_as_used=True
            ):
                continue

            print(
                f"{larger_test_location.function_file_position} W002: broad-coverage '{larger_test_location.test_name}': Coverage of listed tests has same coverage.  Removal suggested. (larger-coverage)",
            )
            overlapped_test_count += 1
            for small_loc in (
                small_test.test_function_locations[0] for small_test in smaller_tests
            ):
                print(
                    f"    {small_loc.function_file_position}: I002: appropriate-coverage '{small_loc.test_name}': Part of replacement for broad coverage test. (smaller-test)",
                )
            print()
        return overlapped_test_count

    def __calculate_superseding_warnings_for_current_hash(
        self, current_coverage_hash: str, current_test: TestCoverage
    ) -> List[FunctionLocation]:

        # Look for tests that have different coverage hash, but covers all arcs of the current test.
        # Skip hashes that are the same as each other as that is handled elsewhere.
        result: List[FunctionLocation] = []
        current_files = current_test.coverage_arcs_by_file_map
        for (
            next_coverage_hash,
            next_test_coverage,
        ) in self.__duplicate_coverage_plugin.test_coverage_by_hash_map.items():
            if next_coverage_hash == current_coverage_hash:
                continue
            next_files = next_test_coverage.coverage_arcs_by_file_map
            if not set(current_files.keys()) >= set(next_files.keys()):
                continue
            if all(
                current_files[inner_filename] >= next_files.get(inner_filename, set())
                for inner_filename in current_files
            ):
                result.extend(next_test_coverage.test_function_locations)
        return result

    def __output_warnings_for_superseding_tests(
        self, suppression_map: Dict[str, Any]
    ) -> int:
        # sourcery skip: use-named-expression

        superseded_test_count = 0
        for (
            base_coverage_hash,
            base_tests,
        ) in self.__duplicate_coverage_plugin.test_coverage_by_hash_map.items():
            found_warning_locations = (
                self.__calculate_superseding_warnings_for_current_hash(
                    base_coverage_hash, base_tests
                )
            )
            if not found_warning_locations:
                continue

            larger_test_coverage = base_tests.test_function_locations[0]
            sorted_warnings = sorted(
                found_warning_locations,
                key=lambda x: (x.file_name, x.line_number, x.test_name),
            )
            unsuppressed_warnings = [
                next_warning
                for next_warning in sorted_warnings
                if not DuplicateCoverageScanner.__is_warning_suppressed(
                    suppression_map, next_warning, "W003", mark_as_used=True
                )
            ]
            if not unsuppressed_warnings:
                continue

            print(
                f"{larger_test_coverage.function_file_position} I003: superseding-coverage '{larger_test_coverage.test_name}': Coverage of listed tests fully covered by this test. (larger-coverage)",
            )
            superseded_test_count += 1
            for next_warning in unsuppressed_warnings:
                print(
                    f"    {next_warning.function_file_position} W003: superseded-coverage '{next_warning.test_name}': Removal suggested. (smaller-coverage)",
                )
            print()

        return superseded_test_count

    @staticmethod
    def __get_report_properties_from_testcase(testcase: ET.Element) -> List[Any]:

        found_properties: List[Any] = []
        if custom_data := testcase.attrib.get("custom_data"):
            try:
                found_properties.append(json.loads(custom_data))
            except Exception as this_exception:
                raise DuplicateCoverageScannerException(
                    f"Bad Json encountered loading custom_data field for test case '{testcase.attrib['name']}' from test report."
                ) from this_exception
        else:
            for next_property in testcase.findall("properties/property"):
                try:
                    found_properties.append(json.loads(next_property.attrib["value"]))
                except Exception as this_exception:
                    raise DuplicateCoverageScannerException(
                        f"Bad Json encountered loading property value for test case '{testcase.attrib['name']}' from test report."
                    ) from this_exception
        return found_properties

    @staticmethod
    def __load_previous_pytest_report_if_present(
        xml_path: Optional[str],
    ) -> Dict[str, Any]:

        if xml_path is None or not os.path.exists(xml_path):
            return {}

        try:
            xml_document = ET.parse(xml_path)
        except Exception as this_exception:
            raise DuplicateCoverageScannerException(
                f"Bad XML encountered loading previous pytest report from '{xml_path}'."
            ) from this_exception

        suppression_map: Dict[str, Any] = {}
        for testcase in xml_document.getroot().findall(".//testcase"):
            if testcase.find("skipped") is not None:
                continue

            testcase_key_prefix = (
                f"{testcase.attrib['classname']}::{testcase.attrib['name']}"
            )

            for (
                next_property
            ) in DuplicateCoverageScanner.__get_report_properties_from_testcase(
                testcase
            ):
                dup_cov = cast(
                    Optional[Dict[str, Any]],
                    (
                        next_property.get("DupCov")
                        if isinstance(next_property, dict)
                        else None
                    ),
                )
                if isinstance(dup_cov, dict):
                    for property_name, property_value in dup_cov.items():
                        if isinstance(property_value, dict):
                            suppression_map[
                                f"{testcase_key_prefix}::{property_name}"
                            ] = property_value
        return suppression_map

    # pylint: disable=broad-exception-caught
    def __run_pytest_and_collect_coverage(self, pytest_argument_list: List[str]) -> int:

        pytest_return_code = 3
        saved_state = SystemState()
        try:
            std_output = io.StringIO()
            std_error = io.StringIO()
            # TODO filter the output so we can tell how fast the tests are being run through

            sys.stdout = std_output
            sys.stderr = std_error

            if "-v" not in pytest_argument_list:
                pytest_argument_list.append("-v")

            pytest_return_code = pytest.main(
                pytest_argument_list, plugins=[self.__duplicate_coverage_plugin]
            )
        except Exception as this_exception:
            print(f"Unexpected error during pytest execution: {str(this_exception)}")
        finally:
            saved_state.restore()
        return pytest_return_code

    # pylint: enable=broad-exception-caught

    def __collect_pytest_coverage(self, pytest_argument_list: List[str]) -> int:
        if (
            pytest_return_code := self.__run_pytest_and_collect_coverage(
                pytest_argument_list
            )
        ) != 0:
            print(
                f"PyTest returned code non-zero code '{pytest_return_code}'. Aborting test coverage analysis."
            )
            return 4

        if fatal_errors := self.__duplicate_coverage_plugin.get_fatal_errors():
            for location, error in fatal_errors:
                print(f"{location.function_file_position} E001: fatal-error: {error}")
            print(
                "One or more tests reported errors collecting test coverage. Aborting test coverage analysis."
            )
            return 5
        return 0

    @staticmethod
    def __handle_arguments():
        parser = argparse.ArgumentParser(
            description="Analyze PyTest tests to determine if extra coverage is present."
        )
        parser.add_argument(
            "-t",
            "--test-report",
            dest="test_report",
            action="store",
            default="report/tests.xml",
            help="previously created XML test report file",
        )

        if "--" in sys.argv:
            idx = sys.argv.index("--")
            script_argument_list = sys.argv[1:idx]
            pytest_argument_list = sys.argv[idx + 1 :]
        else:
            script_argument_list = []
            pytest_argument_list = sys.argv[1:]
        parse_arguments = parser.parse_args(args=script_argument_list)
        return parse_arguments, pytest_argument_list

    # pylint: disable=broad-exception-caught
    def main(self) -> int:
        """Main entry point for the DuplicateCoverageScanner class."""

        parse_arguments, pytest_argument_list = (
            DuplicateCoverageScanner.__handle_arguments()
        )

        try:
            if collect_return_code := self.__collect_pytest_coverage(
                pytest_argument_list
            ):
                return collect_return_code

            suppression_map = (
                DuplicateCoverageScanner.__load_previous_pytest_report_if_present(
                    parse_arguments.test_report
                )
            )

            print()

            identical_test_count = self.__output_identical_tests(suppression_map)
            overlapped_test_count = self.__output_warnings_for_overlapped_tests(
                suppression_map
            )
            superseded_test_count = self.__output_warnings_for_superseding_tests(
                suppression_map
            )

            for k in [
                i for i, j in suppression_map.items() if not j.get("used", False)
            ]:
                print(f"Suppression '{k}' was not used.")

            print()
            print(
                f"Identical: {identical_test_count}, Overlapped: {overlapped_test_count}, Superseded: {superseded_test_count}"
            )
            if identical_test_count or overlapped_test_count or superseded_test_count:
                return 1
        except DuplicateCoverageScannerException as this_exception:
            print(f"Processing error during analysis: {str(this_exception)}")
            return 2
        except Exception as this_exception:
            print(
                f"Unexpected error during test coverage analysis: {str(this_exception)}"
            )
            print(traceback.format_exc())
            return 3
        return 0

    # pylint: enable=broad-exception-caught


# pylint: enable=too-few-public-methods


if __name__ == "__main__":
    sys.exit(DuplicateCoverageScanner().main())
