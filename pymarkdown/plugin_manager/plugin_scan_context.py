"""
Module to provide context when reporting any errors.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pymarkdown.plugin_manager.plugin_scan_failure import PluginScanFailure

if TYPE_CHECKING:  # pragma: no cover
    from pymarkdown.plugin_manager.plugin_manager import PluginManager


class PluginScanContext:
    """
    Class to provide context when reporting any errors.
    """

    def __init__(self, owning_manager: PluginManager, scan_file: str):
        self.owning_manager, self.scan_file, self.line_number = (
            owning_manager,
            scan_file,
            0,
        )
        self.__reported: List[PluginScanFailure] = []

    # pylint: disable=too-many-arguments
    def add_triggered_rule(
        self,
        scan_file: str,
        line_number: int,
        column_number: int,
        rule_id: str,
        rule_name: str,
        rule_description: str,
        extra_error_information: Optional[str],
    ) -> None:
        """
        Add the triggering information for a rule.
        """
        new_entry = PluginScanFailure(
            scan_file,
            line_number,
            column_number,
            rule_id,
            rule_name,
            rule_description,
            extra_error_information,
        )
        self.__reported.append(new_entry)

    # pylint: enable=too-many-arguments

    def report_on_triggered_rules(self) -> None:
        """
        Report on the various points where rules were triggered,
        in sorted order.
        """
        reported_and_sorted = sorted(self.__reported)
        for next_entry in reported_and_sorted:
            self.owning_manager.log_scan_failure(next_entry)
        self.__reported.clear()
