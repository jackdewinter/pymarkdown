"""Simple utility to ensure that a given rule has full code coverage.
"""

import sys
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

print(len(sys.argv))
print(sys.argv[0])
print(sys.argv[1])
print(sys.argv[2])
rule_prefix = sys.argv[1]
xml_file_to_load = sys.argv[2]

try:
    xml_document = ET.parse(xml_file_to_load).getroot()
except ParseError:
    print(f"Project XML file '{xml_file_to_load}' is not a valid XML file.")
    sys.exit(1)

if xml_document.tag != "coverage":
    print(
        f"Project XML file '{xml_file_to_load}' is not a proper coverage-format XML file."
    )
    sys.exit(1)

DID_FIND_RULE = False
for next_class in xml_document.findall(".//class"):
    class_name = next_class.get("name")
    file_name = next_class.get("filename")
    if class_name == f"{rule_prefix}.py" and file_name == f"plugins/{rule_prefix}.py":
        print(next_class.attrib["line-rate"])
        print(next_class.attrib["branch-rate"])

        if next_class.attrib["line-rate"] != "1":
            matching_percentage = float(next_class.attrib["line-rate"]) * 100.0
            print(
                f"Line coverage for module '{file_name}' is less than 100.0% ({matching_percentage}%)."
            )
            sys.exit(1)
        if next_class.attrib["branch-rate"] != "1":
            matching_percentage = float(next_class.attrib["branch-rate"]) * 100.0
            print(
                f"Branch coverage for module '{file_name}' is less than 100.0% ({matching_percentage}%)."
            )
            sys.exit(1)
        DID_FIND_RULE = True

if not DID_FIND_RULE:
    print("bad3")
    sys.exit(1)

sys.exit(0)
