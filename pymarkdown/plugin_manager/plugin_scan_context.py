"""
Module to provide context when reporting any errors.
"""

from __future__ import annotations

from io import TextIOWrapper
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Union

from typing_extensions import override

from pymarkdown.plugin_manager.bad_plugin_error import BadPluginError
from pymarkdown.plugin_manager.fix_line_record import FixLineRecord
from pymarkdown.plugin_manager.fix_token_record import FixTokenRecord
from pymarkdown.plugin_manager.plugin_modify_context import PluginModifyContext
from pymarkdown.plugin_manager.plugin_scan_failure import PluginScanFailure
from pymarkdown.tokens.markdown_token import MarkdownToken

if TYPE_CHECKING:  # pragma: no cover
    from pymarkdown.plugin_manager.plugin_manager import PluginManager


# pylint: disable=too-many-instance-attributes
class PluginScanContext(PluginModifyContext):
    """
    Class to provide context when reporting any errors.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        owning_manager: PluginManager,
        scan_file: str,
        fix_mode: bool,
        file_output: Optional[TextIOWrapper],
        fix_token_map: Optional[Dict[MarkdownToken, List[FixTokenRecord]]],
    ):
        self.owning_manager, self.scan_file, self.line_number = (
            owning_manager,
            scan_file,
            0,
        )
        self.__reported: List[PluginScanFailure] = []
        self.__in_fix_mode = fix_mode
        self.__current_fix_line: Optional[str] = None
        self.__last_line_fixed: Optional[str] = None
        self.__line_change_record: List[FixLineRecord] = []
        self.__file_output = file_output
        self.__fix_token_map = fix_token_map

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def register_fix_token_request(
        self,
        token: MarkdownToken,
        plugin_id: str,
        plugin_action: str,
        field_name: str,
        field_value: Union[str, int],
    ) -> None:
        """
        Register a token to fix and how to fix it.
        """
        if self.__fix_token_map is None:
            return

        new_record = FixTokenRecord(
            token, plugin_id, plugin_action, field_name, field_value
        )
        if token not in self.__fix_token_map:
            existing_records: List[FixTokenRecord] = []
            self.__fix_token_map[token] = existing_records
        else:
            existing_records = self.__fix_token_map[token]
        existing_records.append(new_record)

    # pylint: enable=too-many-arguments

    def get_fix_token_map(self) -> Dict[MarkdownToken, List[FixTokenRecord]]:
        """
        Get the current map of tokens to fix and how to fix them.
        """
        assert self.__fix_token_map is not None
        return self.__fix_token_map

    @property
    @override
    def is_during_line_pass(self) -> bool:
        return self.__file_output is not None

    @property
    @override
    def in_fix_mode(self) -> bool:
        """
        Report on whether the application is in fix mode.
        """
        return self.__in_fix_mode

    @property
    def last_line_fixed(self) -> Optional[str]:
        """
        If in fix mode and processing lines, contains a transformed line.
        """
        return self.__last_line_fixed

    def set_last_line_fixed(self, new_line: Optional[str]) -> None:
        """
        While fixing a document line-by-line, set the current line's content.
        """
        self.__last_line_fixed = new_line

    @property
    def current_fix_line(self) -> Optional[str]:
        """
        If in fix mode and processing lines, contains a transformed line.
        """
        return self.__current_fix_line

    def set_current_fix_line(self, new_line: Optional[str]) -> None:
        """
        While fixing a document line-by-line, set the current line's content.
        """
        self.__current_fix_line = new_line

    @property
    def file_output(self) -> TextIOWrapper:
        """
        File object to use for writing fix information.
        """
        assert self.__file_output
        return self.__file_output

    def add_fix_line_record(self, change_record: FixLineRecord) -> None:
        """
        Add a record regarding a line fix that was made.
        """
        self.__line_change_record.append(change_record)

    @property
    def fix_line_records(self) -> List[FixLineRecord]:
        """
        Get any records detailing line fixes.
        """
        return self.__line_change_record

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
        does_support_fix: bool,
    ) -> None:
        """
        Add the triggering information for a rule.
        """
        if self.in_fix_mode:
            if does_support_fix:
                raise BadPluginError(
                    formatted_message=f"Plugin {rule_id}({rule_name}) reported a triggered rule while in fix mode."
                )
            return

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

    def get_triggered_rules(self) -> Set[str]:
        """
        Get information on any rules that were triggered.
        """
        return {next_entry.rule_id.lower() for next_entry in self.__reported}


# pylint: enable=too-many-instance-attributes
