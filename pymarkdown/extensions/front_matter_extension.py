"""
Module to implement the front matter extensions.
"""
import logging
import string
from typing import Dict, List, Optional, Tuple, Union, cast

from application_properties import ApplicationPropertiesFacade

from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager_constants import (
    ExtensionManagerConstants,
)
from pymarkdown.extension_manager.parser_extension import ParserExtension
from pymarkdown.extensions.front_matter_markdown_token import FrontMatterMarkdownToken
from pymarkdown.leaf_blocks.thematic_leaf_block_processor import (
    ThematicLeafBlockProcessor,
)
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.position_marker import PositionMarker
from pymarkdown.source_providers import SourceProvider
from pymarkdown.transform_state import TransformState

POGGER = ParserLogger(logging.getLogger(__name__))


class FrontMatterExtension(ParserExtension):
    """
    Extension to implement the front matter extensions.
    """

    def get_identifier(self) -> str:
        """
        Get the identifier associated with this extension.
        """
        return "front-matter"

    def get_details(self) -> ExtensionDetails:
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=self.get_identifier(),
            extension_name="Front Matter Metadata",
            extension_description="Allows metadata to be parsed from document front matter.",
            extension_enabled_by_default=False,
            extension_version="0.5.0",
            extension_interface_version=ExtensionManagerConstants.EXTENSION_INTERFACE_VERSION_BASIC,
            extension_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/extensions/front-matter.md",
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
    def handle_front_matter_token(
        output_html: str, next_token: MarkdownToken, transform_state: TransformState
    ) -> str:
        """
        Handle the front matter token.  Note that it does not contribute anything
        at all to the HTML output.
        """
        _ = (next_token, transform_state)

        return output_html

    @staticmethod
    def rehydrate_front_matter(
        current_token: MarkdownToken, previous_token: MarkdownToken
    ) -> str:
        """
        Rehydrate the front matter text from the token.
        """
        _ = previous_token

        front_mater_token = cast(FrontMatterMarkdownToken, current_token)
        front_matter_parts = [front_mater_token.start_boundary_line]
        front_matter_parts.extend(front_mater_token.collected_lines)
        front_matter_parts.extend([front_mater_token.end_boundary_line, ""])
        return ParserHelper.newline_character.join(front_matter_parts)

    @staticmethod
    def process_header_if_present(
        first_line_in_document: str,
        line_number: int,
        requeue: List[str],
        source_provider: SourceProvider,
        tokenized_document: List[MarkdownToken],
    ) -> Tuple[Optional[str], int, List[str]]:
        """
        Take care of processing eligibility and processing for front matter support.
        """
        start_char, extracted_index = ThematicLeafBlockProcessor.is_thematic_break(
            first_line_in_document.rstrip(),
            0,
            "",
            whitespace_allowed_between_characters=False,
            skip_whitespace_check=True,
        )
        next_line: Optional[str] = first_line_in_document
        if start_char == "-" and extracted_index == 3:
            assert next_line is not None
            (
                next_line,
                new_token,
                line_number,
                requeue_lines,
            ) = FrontMatterExtension.__handle_document_front_matter(
                next_line, source_provider
            )
            if new_token:
                tokenized_document.append(new_token)
            else:
                assert requeue_lines is not None
                requeue.extend(requeue_lines)
                next_line = requeue[0]
                del requeue[0]
            POGGER.debug("self.tokenized_document>>$", tokenized_document)
            POGGER.debug("requeue>>$", requeue)
        return next_line, line_number, requeue

    @staticmethod
    def __handle_document_front_matter(
        token_to_use: str, source_provider: SourceProvider
    ) -> Tuple[
        Optional[str], Optional[FrontMatterMarkdownToken], int, Optional[List[str]]
    ]:
        starting_line = token_to_use
        clean_starting_line = starting_line.rstrip()
        repeat_again = True
        have_closing = False
        collected_lines: List[str] = []
        POGGER.info("Metadata prefix detected, scanning for metadata header.")
        next_line = None
        while repeat_again:
            next_line = source_provider.get_next_line()
            if next_line and next_line.rstrip():
                start_char, _ = ThematicLeafBlockProcessor.is_thematic_break(
                    next_line.rstrip(),
                    0,
                    "",
                    whitespace_allowed_between_characters=False,
                )
                have_closing = (
                    bool(start_char) and clean_starting_line == next_line.rstrip()
                )
                repeat_again = not have_closing
            else:
                repeat_again = next_line is not None
            if repeat_again:
                assert next_line is not None
                collected_lines.append(next_line)

        if not have_closing:
            POGGER.info(
                "Metadata prefix abandoned. End of document reached before closing fence encountered."
            )
            collected_lines.insert(0, starting_line)
            return None, None, 1, collected_lines

        POGGER.info("Metadata prefix collected. Verifying validity.")
        matter_map = FrontMatterExtension.__is_front_matter_valid(collected_lines)
        POGGER.debug("ret=$s,type=$s", matter_map, type(matter_map))
        if isinstance(matter_map, str):
            POGGER.info("Metadata validation failed: $", matter_map)
            collected_lines.insert(0, starting_line)
            collected_lines.append(starting_line)
            return None, None, 1, collected_lines

        POGGER.info("Metadata validation succeeded.")
        position_marker = PositionMarker(1, 0, starting_line)
        assert next_line is not None
        new_token = FrontMatterMarkdownToken(
            starting_line, next_line, collected_lines, matter_map, position_marker
        )
        return (
            source_provider.get_next_line(),
            new_token,
            3 + len(collected_lines),
            None,
        )

    @staticmethod
    def __is_front_matter_valid(
        collected_lines: List[str],
    ) -> Union[Dict[str, str], str]:
        ascii_letters_and_digits = f"{string.ascii_letters}{string.digits}_-"

        current_title = ""
        current_value = ""
        value_map: Dict[str, str] = {}

        for next_line in collected_lines:
            POGGER.debug("Next fm:>$s<", next_line)
            next_index, _ = ParserHelper.extract_spaces(next_line, 0)
            assert next_index is not None
            if next_index >= 4:
                POGGER.debug("Indented line established.")
                if not current_title:
                    return "Continuation line encountered before a keyword line."
                current_value += f"\n{next_line.strip()}"
                POGGER.debug("current_value>$<", current_value)
            else:
                if not next_line.strip():
                    return "Blank line encountered before end of metadata."

                POGGER.debug("Non-indented line established.")
                if current_title:
                    POGGER.debug("Adding '$' as '$'.", current_title, current_value)
                    value_map[current_title] = current_value

                (
                    next_index,
                    collected_title,
                ) = ParserHelper.collect_while_one_of_characters(
                    next_line, next_index, ascii_letters_and_digits
                )
                assert next_index is not None
                assert collected_title is not None
                current_title = collected_title
                if next_index < len(next_line) and next_line[next_index] == ":":
                    current_value = next_line[next_index + 1 :].strip()
                else:
                    return "Newline did not start with `keyword:`."
        if current_title:
            POGGER.debug("Adding final '$' as '$'.", current_title, current_value)
            value_map[current_title.lower()] = current_value

            # This is specifically to trigger test_front_matter_20.
            assert current_title != "test" or current_value != "assert"
        return value_map or "No valid metadata header lines were found."
