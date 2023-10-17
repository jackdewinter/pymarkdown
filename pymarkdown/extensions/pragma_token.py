"""
Module to provide for linter instructions that can be embedded within the document.
"""
import logging
from typing import Dict, List, Optional, Set, Tuple

from application_properties import ApplicationPropertiesFacade
from typing_extensions import Protocol

from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager_constants import (
    ExtensionManagerConstants,
)
from pymarkdown.extension_manager.parser_extension import ParserExtension
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.plugin_manager.found_plugin import FoundPlugin
from pymarkdown.tokens.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods
class LogPragmaFailureProtocol(Protocol):
    """
    Protocol to specify a function that allows failures to be reported.
    """

    def __call__(self, scan_file: str, line_number: int, pragma_error: str) -> None:
        ...  # pragma: no cover


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
            extension_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/extensions/pragmas.md",
            extension_configuration=None,
        )

    def apply_configuration(
        self, extension_specific_facade: ApplicationPropertiesFacade
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
        if (
            not container_depth
            and not extracted_whitespace
            and (
                line_to_parse.startswith(PragmaToken.pragma_prefix)
                or line_to_parse.startswith(PragmaToken.pragma_alternate_prefix)
            )
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
            remaining_line = line_to_parse[start_index:].rstrip().lower()
            if remaining_line.startswith(
                PragmaToken.pragma_title
            ) and remaining_line.endswith(PragmaToken.pragma_suffix):
                index_number = (
                    -position_marker.line_number
                    if was_extended_prefix
                    else position_marker.line_number
                )
                parser_properties.pragma_lines[index_number] = line_to_parse
                POGGER.debug("pragma $ extracted - >$<", index_number, line_to_parse)
                return True
        POGGER.debug("pragma not extracted - >$<", line_to_parse)
        return False

    # pylint: disable=too-many-arguments
    @staticmethod
    def compile_single_pragma(
        scan_file: str,
        next_line_number: int,
        pragma_lines: Dict[int, str],
        all_ids: Dict[str, FoundPlugin],
        document_pragmas: Dict[int, Set[str]],
        document_pragma_ranges: List[Tuple[int, int, Set[str]]],
        log_pragma_failure: LogPragmaFailureProtocol,
    ) -> None:
        """
        Compile a single pragma line, validating it before adding it to the dictionary of pragmas.
        """
        if next_line_number > 0:
            prefix_length = len(PragmaToken.pragma_prefix)
            actual_line_number = next_line_number
        else:
            prefix_length = len(PragmaToken.pragma_alternate_prefix)
            actual_line_number = -next_line_number

        line_after_prefix = pragma_lines[next_line_number][prefix_length:].rstrip()
        after_whitespace_index, _ = ParserHelper.extract_spaces(line_after_prefix, 0)
        assert after_whitespace_index is not None
        command_data = line_after_prefix[
            after_whitespace_index
            + len(PragmaToken.pragma_title) : -len(PragmaToken.pragma_suffix)
        ]
        after_command_index, command = ParserHelper.extract_until_spaces(
            command_data, 0
        )
        assert command is not None
        assert after_command_index is not None
        command = command.lower()
        if not command:
            log_pragma_failure(
                scan_file,
                actual_line_number,
                "Inline configuration specified without command.",
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
        ids_to_disable = command_data[after_command_index:].split(",")
        processed_ids = set()
        for next_id in ids_to_disable:
            next_id = next_id.strip().lower()
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

        if processed_ids:
            document_pragmas[actual_line_number + 1] = processed_ids

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
        after_space_index, _ = ParserHelper.extract_spaces(
            command_data, after_command_index
        )
        assert after_space_index is not None
        if after_space_index == len(command_data):
            log_pragma_failure(
                scan_file,
                actual_line_number,
                f"Inline configuration command '{command}' was not followed by a count and a list of plugin ids to temporarily disable.",
            )
            return False, -1, None
        after_num_index, extracted_number = ParserHelper.extract_until_spaces(
            command_data, after_space_index
        )

        assert extracted_number is not None
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

        assert after_num_index is not None
        after_number_index, _ = ParserHelper.extract_spaces(
            command_data, after_num_index
        )
        if after_number_index == len(command_data):
            log_pragma_failure(
                scan_file,
                actual_line_number,
                f"Inline configuration command '{command}' and its count were not followed by a list of plugin ids to temporarily disable.",
            )
            return False, -1, None
        assert after_number_index is not None
        return True, after_number_index, count_value

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments, too-many-locals
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

        ids_to_disable = command_data[after_number_index:].split(",")
        processed_ids = set()
        for next_id in ids_to_disable:
            next_id = next_id.strip().lower()
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

        if processed_ids:
            assert count_value is not None
            pragma_tuple = (
                actual_line_number + 1,
                actual_line_number + count_value,
                processed_ids,
            )
            document_pragma_ranges.append(pragma_tuple)

    # pylint: enable=too-many-arguments, too-many-locals


class PragmaToken(MarkdownToken):
    """
    Token that contains the pragmas for the document.
    """

    pragma_prefix = "<!--"
    pragma_alternate_prefix = "<!---"
    pragma_title = "pyml "
    pragma_suffix = "-->"

    def __init__(self, pragma_lines: Dict[int, str]) -> None:
        self.__pragma_lines = pragma_lines

        serialized_pragmas = "".join(
            f";{next_line_number}:{pragma_lines[next_line_number]}"
            for next_line_number in pragma_lines
        )

        MarkdownToken.__init__(
            self,
            MarkdownToken._token_pragma,
            MarkdownTokenClass.SPECIAL,
            is_extension=True,
            extra_data=serialized_pragmas[1:],
        )

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
