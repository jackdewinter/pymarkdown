"""Module to handle the collection and annotation of user properties in test reports, required for coverage collection."""

# conftest.py
import json
import os
from typing import List
from xml.etree import ElementTree as ET

import pytest
from _pytest.config import Config
from _pytest.main import Session
from _pytest.python import Function

user_properties_map = {}


def pytest_collection_modifyitems(
    session: Session, config: Config, items: List[pytest.Item]
) -> None:
    """During test collection, gather any user properties from test functions to be added to the XML report later."""

    _ = (session, config)

    # If we are not annotating user properties, then skip processing.
    if os.getenv("PYTEST_ANNOTATE_USER_PROPERTIES", "") != "1":
        return

    # For each collected item, check for user_properties markers on functions, collecting them into a map.
    for next_item in items:

        # For each function item, check for user_properties markers.
        if not isinstance(next_item, Function):
            continue
        for next_marker in next_item.own_markers:
            if next_marker.name == "user_properties":

                # Extract the relative file name and test name to use as the key.
                relative_file_name = next_item.location[0]
                assert relative_file_name.endswith(".py")
                class_name = (
                    relative_file_name[:-3].replace("/", ".").replace("\\", ".")
                )
                key_data_str = str(
                    {"classname": class_name, "test-name": next_item.location[2]}
                )

                # Extract the user properties from the marker and store them in the map.
                assert isinstance(next_marker.args, tuple)
                assert len(next_marker.args) >= 1
                assert isinstance(next_marker.args[0], (dict, list))
                user_properties_map[key_data_str] = next_marker.args[0]


def pytest_sessionfinish(session: "Session", exitstatus: int) -> None:
    """Once all tests are complete, update the XML report with any user properties collected during test collection."""

    _ = exitstatus

    # If we are not annotating user properties, then skip processing.
    if os.getenv("PYTEST_ANNOTATE_USER_PROPERTIES", "") != "1":
        return

    # If an XML report file is not specified, then skip processing.
    if hasattr(session.config, "option") and session.config.option.xmlpath:

        # Load the XML report file.
        xml_path = session.config.option.xmlpath
        tree = ET.parse(xml_path)

        # For each test case in the XML report, add any user properties that are present in the map.
        for testsuite in tree.getroot().findall("testsuite"):
            for testcase in testsuite.findall("testcase"):
                key_data_str = str(
                    {
                        "classname": testcase.attrib["classname"],
                        "test-name": testcase.attrib["name"],
                    }
                )
                try:
                    if key_data_str in user_properties_map:
                        testcase.set(
                            "custom_data", json.dumps(user_properties_map[key_data_str])
                        )
                except Exception as this_exception:
                    print(key_data_str)
                    print(this_exception)
                    raise
        # Save the XML report file, with any modifications.
        tree.write(xml_path)
