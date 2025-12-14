"""
Module to provide context when reporting any errors.
"""

from __future__ import annotations

from io import TextIOWrapper
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple, Union

from typing_extensions import override

from pymarkdown.plugin_manager.bad_plugin_error import BadPluginError
from pymarkdown.plugin_manager.fix_line_record import FixLineRecord
from pymarkdown.plugin_manager.fix_token_record import FixTokenRecord
from pymarkdown.plugin_manager.plugin_modify_context import PluginModifyContext
from pymarkdown.plugin_manager.plugin_scan_failure import PluginScanFailure
from pymarkdown.plugin_manager.replace_tokens_record import ReplaceTokensRecord
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
        actual_tokens: List[MarkdownToken],
        fix_mode: bool,
        file_output: Optional[TextIOWrapper],
        fix_token_map: Optional[Dict[MarkdownToken, List[FixTokenRecord]]],
        replace_tokens_list: Optional[List[ReplaceTokensRecord]],
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
        self.__replace_token_list = replace_tokens_list
        self.__actual_tokens = actual_tokens

    # pylint: enable=too-many-arguments

    def register_replace_tokens_request(
        self,
        plugin_id: str,
        start_token: MarkdownToken,
        end_token: MarkdownToken,
        replacement_tokens: List[MarkdownToken],
    ) -> None:
        """
        Register a sequence of tokens and what to replace them with.
        """
        assert self.__replace_token_list is not None
        new_record = ReplaceTokensRecord(
            plugin_id, start_token, end_token, replacement_tokens
        )
        self.__replace_token_list.append(new_record)

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

    def get_replace_tokens_list(self) -> List[ReplaceTokensRecord]:
        """
        Get the current list of replacement records/tokens.
        """
        assert self.__replace_token_list is not None
        return self.__replace_token_list

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
        error_token: Optional[MarkdownToken] = None,
        override_is_error_token_prefaced_by_blank_line: Optional[bool] = None,
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

        if override_is_error_token_prefaced_by_blank_line is not None:
            is_error_token_prefaced_by_blank_line = (
                override_is_error_token_prefaced_by_blank_line
            )
        else:
            is_error_token_prefaced_by_blank_line = self.__calc_x(error_token)

        new_entry = PluginScanFailure(
            scan_file,
            line_number,
            column_number,
            rule_id,
            rule_name,
            rule_description,
            extra_error_information,
            is_error_token_prefaced_by_blank_line,
        )
        self.__reported.append(new_entry)

    # pylint: enable=too-many-arguments

    def __calc_x_rewind_if_inline(
        self, index_to_check: int, current_token: MarkdownToken, dd: bool
    ) -> Tuple[int, MarkdownToken, bool, bool]:
        # For an inline, rewind back to the last text token.  If the text token was
        # not on the same line as the inline token, by definition there is text on
        # the line, so break out of this check.
        #
        # Note that in special cases, such as a link being at the start of a parapgrah,
        # we may not have any text element before the paragraph element.
        do_break = False
        if (
            not current_token.is_leaf
            and not current_token.is_container
            and not current_token.is_text
        ):
            while (
                index_to_check >= 0
                and not self.__actual_tokens[index_to_check].is_text
                and not self.__actual_tokens[index_to_check].is_paragraph
            ):
                index_to_check -= 1
            assert index_to_check >= 0
            if (
                current_token.line_number
                != self.__actual_tokens[index_to_check].line_number
            ):
                do_break = True
            else:
                current_token = self.__actual_tokens[index_to_check]
                dd = True
        return index_to_check, current_token, dd, do_break

    def __calc_x_rewind_if_text(
        self, index_to_check: int, current_token: MarkdownToken, dd: bool
    ) -> Tuple[int, MarkdownToken, bool]:
        if current_token.is_text:
            # Text blocks can only occur within leaf elements, so work backwards until
            # we hit a leaf element.
            while (
                index_to_check >= 0 and not self.__actual_tokens[index_to_check].is_leaf
            ):
                index_to_check -= 1
            if index_to_check > 0:
                index_to_check -= 1
            current_token = self.__actual_tokens[index_to_check]
            dd = True
        elif current_token.is_paragraph:
            if index_to_check > 0:
                index_to_check -= 1
            current_token = self.__actual_tokens[index_to_check]
        return index_to_check, current_token, dd

    def __calc_x(self, error_token: Optional[MarkdownToken]) -> bool:
        if error_token is None:
            return False

        is_error_token_prefaced_by_blank_line = False
        for i, j in enumerate(self.__actual_tokens):  # pragma: no cover
            if not (
                j.line_number == error_token.line_number
                and j.column_number == error_token.column_number
                and j.token_name == error_token.token_name
            ):
                continue

            index_to_check = i
            current_token = error_token
            dd = False

            index_to_check, current_token, dd, do_break = (
                self.__calc_x_rewind_if_inline(index_to_check, current_token, dd)
            )
            if do_break:
                break

            index_to_check, current_token, dd = self.__calc_x_rewind_if_text(
                index_to_check, current_token, dd
            )

            # Lists can have trailing
            if current_token.is_list_start:
                while (
                    index_to_check >= 0
                    and self.__actual_tokens[index_to_check - 1].is_list_end
                ):
                    index_to_check -= 1
                    # should we be doing this more generally? i.e. list closing and opening a fcb... ?
                    # assert False  -- check to see if we need is_list_end or is_block_quote_end
                if index_to_check > 0:
                    index_to_check -= 1
                current_token = self.__actual_tokens[index_to_check]
                dd = True
            assert index_to_check >= 0
            if not dd and index_to_check > 0:
                index_to_check -= 1
            is_error_token_prefaced_by_blank_line = self.__actual_tokens[
                index_to_check
            ].is_blank_line
            break
        return is_error_token_prefaced_by_blank_line

    def report_on_triggered_rules(self) -> None:
        """
        Report on the various points where rules were triggered,
        in sorted order.
        """
        for next_entry in sorted(self.__reported):
            self.owning_manager.log_scan_failure(next_entry)
        self.__reported.clear()

    def get_triggered_rules(self) -> Set[str]:
        """
        Get information on any rules that were triggered.
        """
        return {next_entry.rule_id.lower() for next_entry in self.__reported}

    def is_pragma_on_line(self, line_number: int) -> bool:
        """
        Determine if there is a pragma on the specified line.
        """
        return self.owning_manager.is_pragma_on_line(line_number)

    def calc_pragma_offset(self, token: MarkdownToken, line_number_delta: int) -> int:
        """
        Calculate the pragma offset for a given token and line number delta.
        """
        pragma_offset = 0
        for line_index in range(line_number_delta):
            modified_line_number = token.line_number + line_index + 1 + pragma_offset
            if self.owning_manager.is_pragma_on_line(modified_line_number):
                pragma_offset += 1
        return pragma_offset


# pylint: enable=too-many-instance-attributes
