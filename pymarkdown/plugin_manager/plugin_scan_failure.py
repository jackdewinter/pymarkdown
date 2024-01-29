"""
Module to contain information about a failure reported by one of the rule plugins.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PluginScanFailure:
    """
    Class to contain information about a failure reported by one of the rule plugins.
    """

    scan_file: str
    line_number: int
    column_number: int
    rule_id: str
    rule_name: str
    rule_description: str
    extra_error_information: Optional[str]

    def __lt__(self, other: "PluginScanFailure") -> bool:
        # This is required to allow for sorting of the failures before display.

        # if self.scan_file != other.scan_file:
        #     return self.scan_file < other.scan_file
        if self.line_number != other.line_number:
            return self.line_number < other.line_number
        if self.column_number != other.column_number:
            return self.column_number < other.column_number
        return self.rule_id < other.rule_id
