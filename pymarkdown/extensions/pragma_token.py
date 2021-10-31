"""
Module to provide for linter instructions that can be embedded within the document.
"""
import logging

from pymarkdown.extension_impl import ExtensionDetails
from pymarkdown.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods
class PragmaExtension:
    """
    Extension to implement the pragma extensions.
    """

    @classmethod
    def get_identifier(cls):
        """
        Get the identifier associated with this extension.
        """
        return "linter-pragmas"

    @classmethod
    def get_details(cls):
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=cls.get_identifier(),
            extension_name="Pragma Linter Instructions",
            extension_description="Allows parsing of instructions for the linter.",
            extension_enabled_by_default=True,
            extension_version="0.5.0",
            extension_interface_version=1,
            extension_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/extensions/pragmas.md",
            extension_configuration=None,
        )

    @classmethod
    def apply_configuration(cls, extension_specific_facade):
        """
        Apply any configuration required by the extension.
        """
        _ = extension_specific_facade

    @staticmethod
    def look_for_pragmas(
        position_marker,
        line_to_parse,
        container_depth,
        extracted_whitespace,
        parser_properties,
    ):
        """
        Look for a pragma in the current line.
        """

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

            start_index, _ = ParserHelper.extract_whitespace(
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
                return True
        return False

    # pylint: disable=too-many-locals, too-many-arguments
    @staticmethod
    def compile_single_pragma(
        scan_file,
        next_line_number,
        pragma_lines,
        all_ids,
        document_pragmas,
        log_pragma_failure,
    ):
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
        after_whitespace_index, _ = ParserHelper.extract_whitespace(
            line_after_prefix, 0
        )
        command_data = line_after_prefix[
            after_whitespace_index
            + len(PragmaToken.pragma_title) : -len(PragmaToken.pragma_suffix)
        ]
        after_command_index, command = ParserHelper.extract_until_whitespace(
            command_data, 0
        )
        command = command.lower()
        if not command:
            log_pragma_failure(
                scan_file,
                actual_line_number,
                "Inline configuration specified without command.",
            )
        elif command == "disable-next-line":
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
        else:
            log_pragma_failure(
                scan_file,
                actual_line_number,
                f"Inline configuration command '{command}' not understood.",
            )

    # pylint: enable=too-many-locals, too-many-arguments


# pylint: enable=too-few-public-methods


class PragmaToken(MarkdownToken):
    """
    Token that contains the pragmas for the document.
    """

    pragma_prefix = "<!--"
    pragma_alternate_prefix = "<!---"
    pragma_title = "pyml "
    pragma_suffix = "-->"

    def __init__(self, pragma_lines):
        self.__pragma_lines = pragma_lines

        serialized_pragmas = ""
        for next_line_number in pragma_lines:
            serialized_pragmas += (
                f";{next_line_number}:{pragma_lines[next_line_number]}"
            )

        MarkdownToken.__init__(
            self,
            MarkdownToken._token_pragma,
            MarkdownTokenClass.SPECIAL,
            is_extension=True,
            extra_data=serialized_pragmas[1:],
        )

    @property
    def pragma_lines(self):
        """
        Returns the pragma lines for the document.
        """
        return self.__pragma_lines
