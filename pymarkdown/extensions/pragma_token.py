"""
Module to provide for linter instructions that can be embedded within the document.
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

from typing_extensions import Protocol

from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager_constants import (
    ExtensionManagerConstants,
)
from pymarkdown.extension_manager.parser_extension import ParserExtension
from pymarkdown.general.constants import Constants
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.my_application_properties_facade import MyApplicationPropertiesFacade
from pymarkdown.plugin_manager.found_plugin import FoundPlugin
from pymarkdown.tokens.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)

POGGER = ParserLogger(logging.getLogger(__name__))


@dataclass
class GeneralPragmaDisableStart:
    """Data class to hold the start of a general pragma disable."""

    rule_id: str
    start_line: int


# pylint: disable=too-few-public-methods
class LogPragmaFailureProtocol(Protocol):
    """
    Protocol to specify a function that allows failures to be reported.
    """

    def __call__(  # noqa: E704
        self, scan_file: str, line_number: int, pragma_error: str
    ) -> None: ...  # pragma: no cover


# pylint: enable=too-few-public-methods


class PragmaExtension(ParserExtension):
    """
    Extension to implement the pragma extensions.
    """

    def get_identifier(self) -> str:
        """
        Get the identifier associated with this extension.
        """
        return "linter-pragmas"

    def get_details(self) -> ExtensionDetails:
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=self.get_identifier(),
            extension_name="Pragma Linter Instructions",
            extension_description="Allows parsing of instructions for the linter.",
            extension_enabled_by_default=True,
            extension_version="0.5.0",
            extension_interface_version=ExtensionManagerConstants.EXTENSION_INTERFACE_VERSION_BASIC,
            extension_url="https://pymarkdown.readthedocs.io/en/latest/extensions/pragmas/",
            extension_configuration=None,
        )

    def apply_configuration(
        self, extension_specific_facade: MyApplicationPropertiesFacade
    ) -> None:
        """
        Apply any configuration required by the extension.
        """
        _ = extension_specific_facade

    @staticmethod
    def look_for_pragmas(
        position_marker: PositionMarker,
        line_to_parse: str,
        container_depth: int,
        extracted_whitespace: Optional[str],
        parser_properties: ParseBlockPassProperties,
    ) -> bool:
        """
        Look for a pragma in the current line.
        """

        POGGER.debug("look_for_pragmas - >$<", line_to_parse)
        POGGER.debug("look_for_pragmas - ws >$<", extracted_whitespace)
        used_standard_prefix = line_to_parse.startswith(PragmaToken.pragma_prefix)
        used_alternate_prefix = line_to_parse.startswith(
            PragmaToken.pragma_alternate_prefix
        )
        if (
            not container_depth
            and not extracted_whitespace
            and (used_standard_prefix or used_alternate_prefix)
        ):
            was_extended_prefix = line_to_parse.startswith(
                PragmaToken.pragma_alternate_prefix
            )

            start_index, _ = ParserHelper.extract_spaces(
                line_to_parse,
                len(
                    PragmaToken.pragma_alternate_prefix
                    if was_extended_prefix
                    else PragmaToken.pragma_prefix
                ),
            )
            remaining_line = (
                line_to_parse[start_index:].rstrip(Constants.ascii_whitespace).lower()
            )
            if remaining_line.startswith(PragmaToken.pragma_title):
                found_matching_suffix = (
                    remaining_line.endswith(PragmaToken.pragma_suffix)
                    if used_standard_prefix
                    else remaining_line.endswith(PragmaToken.pragma_alternate_suffix)
                )
                if found_matching_suffix:
                    index_number = (
                        -position_marker.line_number
                        if was_extended_prefix
                        else position_marker.line_number
                    )
                    parser_properties.pragma_lines[index_number] = line_to_parse
                    POGGER.debug(
                        "pragma $ extracted - >$<", index_number, line_to_parse
                    )
                    return True
        POGGER.debug("pragma not extracted - >$<", line_to_parse)
        return False

    # pylint: disable=too-many-arguments, too-many-locals
    @staticmethod
    def compile_single_pragma(
        scan_file: str,
        next_line_number: int,
        pragma_lines: Dict[int, str],
        all_ids: Dict[str, FoundPlugin],
        document_pragmas: Dict[int, Set[str]],
        document_pragma_ranges: List[Tuple[int, int, Set[str]]],
        general_pragma_ranges: List[Tuple[int, int, str]],
        active_general_pragmas: Dict[str, GeneralPragmaDisableStart],
        log_pragma_failure: LogPragmaFailureProtocol,
        actual_pragma_line_numbers: List[int],
    ) -> None:
        """
        Compile a single pragma line, validating it before adding it to the dictionary of pragmas.
        """
        if next_line_number > 0:
            prefix_length = len(PragmaToken.pragma_prefix)
            actual_line_number = next_line_number
            suffix_to_use = PragmaToken.pragma_suffix
        else:
            prefix_length = len(PragmaToken.pragma_alternate_prefix)
            actual_line_number = -next_line_number
            suffix_to_use = PragmaToken.pragma_alternate_suffix

        actual_pragma_line_numbers.append(actual_line_number)

        line_after_prefix = pragma_lines[next_line_number][prefix_length:]
        after_whitespace_index, _ = ParserHelper.extract_spaces_verified(
            line_after_prefix, 0
        )
        after_whitespace_index, _ = ParserHelper.extract_spaces_verified(
            line_after_prefix, after_whitespace_index + len(PragmaToken.pragma_title)
        )
        command_data = line_after_prefix[after_whitespace_index : -len(suffix_to_use)]
        after_command_index, command = ParserHelper.extract_until_spaces_verified(
            command_data, 0
        )
        command = command.lower()
        if not command:
            log_pragma_failure(
                scan_file,
                actual_line_number,
                "Inline configuration specified without command.",
            )
        elif command == "disable":
            PragmaExtension.__handle_general_disable(
                command_data,
                after_command_index,
                scan_file,
                actual_line_number,
                log_pragma_failure,
                all_ids,
                command,
                active_general_pragmas,
            )
        elif command == "enable":
            PragmaExtension.__handle_general_enable(
                command_data,
                after_command_index,
                scan_file,
                actual_line_number,
                log_pragma_failure,
                all_ids,
                command,
                active_general_pragmas,
                general_pragma_ranges,
            )
        elif command == "disable-next-line":
            PragmaExtension.__handle_disable_next_line(
                command_data,
                after_command_index,
                log_pragma_failure,
                scan_file,
                actual_line_number,
                document_pragmas,
                all_ids,
                command,
            )
        elif command == "disable-num-lines":
            PragmaExtension.__handle_disable_num_lines(
                command_data,
                after_command_index,
                log_pragma_failure,
                scan_file,
                actual_line_number,
                document_pragma_ranges,
                all_ids,
                command,
            )
        else:
            log_pragma_failure(
                scan_file,
                actual_line_number,
                f"Inline configuration command '{command}' not understood.",
            )

    # pylint: enable=too-many-arguments, too-many-locals

    @staticmethod
    def end(
        active_general_pragmas: Dict[str, GeneralPragmaDisableStart],
        general_pragma_ranges: List[Tuple[int, int, str]],
    ) -> None:
        """
        End the pragma extension compilation.
        """
        general_pragma_ranges.extend(
            (i.start_line, 9999, i.rule_id) for _, i in active_general_pragmas.items()
        )

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_general_disable(
        command_data: str,
        after_command_index: int,
        scan_file: str,
        actual_line_number: int,
        log_pragma_failure: LogPragmaFailureProtocol,
        all_ids: Dict[str, FoundPlugin],
        command: str,
        active_general_pragmas: Dict[str, GeneralPragmaDisableStart],
    ) -> None:
        if processed_ids := PragmaExtension.__parse_rules_to_exclude(
            command_data,
            after_command_index,
            scan_file,
            actual_line_number,
            command,
            log_pragma_failure,
            all_ids,
        ):
            for next_rule_id in processed_ids:
                if next_rule_id in active_general_pragmas:
                    POGGER.debug(
                        "File $:line $: General pragma $ already disabled. Ignoring.",
                        scan_file,
                        actual_line_number,
                        next_rule_id,
                    )
                else:
                    active_general_pragmas[next_rule_id] = GeneralPragmaDisableStart(
                        next_rule_id, actual_line_number
                    )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_general_enable(
        command_data: str,
        after_command_index: int,
        scan_file: str,
        actual_line_number: int,
        log_pragma_failure: LogPragmaFailureProtocol,
        all_ids: Dict[str, FoundPlugin],
        command: str,
        active_general_pragmas: Dict[str, GeneralPragmaDisableStart],
        general_pragma_ranges: List[Tuple[int, int, str]],
    ) -> None:
        if processed_ids := PragmaExtension.__parse_rules_to_exclude(
            command_data,
            after_command_index,
            scan_file,
            actual_line_number,
            command,
            log_pragma_failure,
            all_ids,
        ):
            for next_rule_id in processed_ids:
                if next_rule_id in active_general_pragmas:
                    disable_record = active_general_pragmas[next_rule_id]
                    general_pragma_ranges.append(
                        (
                            disable_record.start_line,
                            actual_line_number,
                            disable_record.rule_id,
                        )
                    )
                    del active_general_pragmas[next_rule_id]
                else:
                    POGGER.debug(
                        "File $:line $: General pragma $ already enabled. Ignoring.",
                        scan_file,
                        actual_line_number,
                        next_rule_id,
                    )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_disable_next_line(
        command_data: str,
        after_command_index: int,
        log_pragma_failure: LogPragmaFailureProtocol,
        scan_file: str,
        actual_line_number: int,
        document_pragmas: Dict[int, Set[str]],
        all_ids: Dict[str, FoundPlugin],
        command: str,
    ) -> None:
        if processed_ids := PragmaExtension.__parse_rules_to_exclude(
            command_data,
            after_command_index,
            scan_file,
            actual_line_number,
            command,
            log_pragma_failure,
            all_ids,
        ):
            document_pragmas[actual_line_number + 1] = processed_ids

    @staticmethod
    def __parse_rules_to_exclude(
        command_data: str,
        after_number_index: int,
        scan_file: str,
        actual_line_number: int,
        command: str,
        log_pragma_failure: LogPragmaFailureProtocol,
        all_ids: Dict[str, FoundPlugin],
    ) -> Set[str]:
        ids_to_disable = command_data[after_number_index:].split(",")
        processed_ids = set()
        for next_id in ids_to_disable:
            next_id = next_id.strip(" ").lower()
            if not next_id:
                log_pragma_failure(
                    scan_file,
                    actual_line_number,
                    f"Inline configuration command '{command}' specified a plugin with a blank id.",
                )
            elif next_id in all_ids:
                normalized_id = all_ids[next_id].plugin_id
                processed_ids.add(normalized_id)
            else:
                log_pragma_failure(
                    scan_file,
                    actual_line_number,
                    f"Inline configuration command '{command}' unable to find a plugin with the id '{next_id}'.",
                )
        return processed_ids

    # pylint: enable=too-many-arguments
    # pylint: disable=too-many-arguments

    @staticmethod
    def __handle_disable_num_lines_parse(
        command_data: str,
        after_command_index: int,
        log_pragma_failure: LogPragmaFailureProtocol,
        scan_file: str,
        actual_line_number: int,
        command: str,
    ) -> Tuple[bool, int, Optional[int]]:
        after_space_index, _ = ParserHelper.extract_spaces_verified(
            command_data, after_command_index
        )
        if after_space_index == len(command_data):
            log_pragma_failure(
                scan_file,
                actual_line_number,
                f"Inline configuration command '{command}' was not followed by a count and a list of plugin ids to temporarily disable.",
            )
            return False, -1, None
        after_num_index, extracted_number = ParserHelper.extract_until_spaces_verified(
            command_data, after_space_index
        )

        try:
            count_value = int(extracted_number)
        except ValueError:
            count_value = -1
        if count_value < 1:
            log_pragma_failure(
                scan_file,
                actual_line_number,
                f"Inline configuration command '{command}' specified a count '{extracted_number}' that is not a valid positive integer.",
            )
            return False, -1, None

        after_number_index, _ = ParserHelper.extract_spaces_verified(
            command_data, after_num_index
        )
        if after_number_index == len(command_data):
            log_pragma_failure(
                scan_file,
                actual_line_number,
                f"Inline configuration command '{command}' and its count were not followed by a list of plugin ids to temporarily disable.",
            )
            return False, -1, None
        return True, after_number_index, count_value

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_disable_num_lines(
        command_data: str,
        after_command_index: int,
        log_pragma_failure: LogPragmaFailureProtocol,
        scan_file: str,
        actual_line_number: int,
        document_pragma_ranges: List[Tuple[int, int, Set[str]]],
        all_ids: Dict[str, FoundPlugin],
        command: str,
    ) -> None:
        (
            is_ok,
            after_number_index,
            count_value,
        ) = PragmaExtension.__handle_disable_num_lines_parse(
            command_data,
            after_command_index,
            log_pragma_failure,
            scan_file,
            actual_line_number,
            command,
        )
        if not is_ok:
            return

        if processed_ids := PragmaExtension.__parse_rules_to_exclude(
            command_data,
            after_number_index,
            scan_file,
            actual_line_number,
            command,
            log_pragma_failure,
            all_ids,
        ):
            assert count_value is not None
            pragma_tuple = (
                actual_line_number + 1,
                actual_line_number + count_value,
                processed_ids,
            )
            document_pragma_ranges.append(pragma_tuple)

    # pylint: enable=too-many-arguments


class PragmaToken(MarkdownToken):
    """
    Token that contains the pragmas for the document.
    """

    pragma_prefix = "<!--"
    pragma_alternate_prefix = "<!---"
    pragma_title = "pyml "
    pragma_suffix = "-->"
    pragma_alternate_suffix = "--->"

    def __init__(self, pragma_lines: Dict[int, str]) -> None:
        self.__pragma_lines = pragma_lines

        MarkdownToken.__init__(
            self,
            MarkdownToken._token_pragma,
            MarkdownTokenClass.SPECIAL,
            is_extension=True,
            extra_data="",
        )
        self.__compose_extra_data_field()

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """
        serialized_pragmas = "".join(
            f";{next_line_number}:{self.__pragma_lines[next_line_number]}"
            for next_line_number in self.__pragma_lines
        )
        self._set_extra_data(serialized_pragmas[1:])

    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_pragma

    @property
    def pragma_lines(self) -> Dict[int, str]:
        """
        Returns the pragma lines for the document.
        """
        return self.__pragma_lines

    def adjust_pragma_line_number(
        self, initial_line_number: int, new_line_number: int
    ) -> None:
        """Perform an adjustment to the line number of a given pragma."""
        old_pragma = self.__pragma_lines[initial_line_number]
        del self.__pragma_lines[initial_line_number]
        self.__pragma_lines[new_line_number] = old_pragma
        self.__compose_extra_data_field()

    def register_for_markdown_transform(
        self,
        registration_function: RegisterMarkdownTransformHandlersProtocol,
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """

        # Note, because the Pragma token contains every pragma contained
        # within the file, this is handled globally in TransformToMarkdown's
        # __handle_pragma_processing.
        _ = registration_function

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            PragmaToken,
            PragmaToken.__handle_pragma_token,
            None,
        )

    @staticmethod
    def __handle_pragma_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (transform_state, next_token)

        return output_html
