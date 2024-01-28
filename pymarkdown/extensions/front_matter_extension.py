"""
Module to implement the front matter extensions.
"""

import logging
from typing import Any, List, Optional, Tuple, Union

import yaml
from application_properties import ApplicationPropertiesFacade
from yaml import SafeLoader

from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager_constants import (
    ExtensionManagerConstants,
)
from pymarkdown.extension_manager.parser_extension import ParserExtension
from pymarkdown.extensions.front_matter_markdown_token import FrontMatterMarkdownToken
from pymarkdown.general.constants import Constants
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.general.source_providers import SourceProvider
from pymarkdown.leaf_blocks.thematic_leaf_block_processor import (
    ThematicLeafBlockProcessor,
)
from pymarkdown.tokens.markdown_token import MarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class FrontMatterExtension(ParserExtension):
    """
    Extension to implement the front matter extensions.
    """

    def __init__(self) -> None:
        self.__allow_blank_lines = False

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
        self.__allow_blank_lines = extension_specific_facade.get_boolean_property(
            "allow_blank_lines", default_value=False
        )

    # pylint: disable=too-many-arguments
    def process_header_if_present(
        self,
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
            first_line_in_document.rstrip(Constants.ascii_whitespace),
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
            ) = self.__handle_document_front_matter(next_line, source_provider)
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

    # pylint: enable=too-many-arguments

    def __handle_document_front_matter(
        self, token_to_use: str, source_provider: SourceProvider
    ) -> Tuple[
        Optional[str], Optional[FrontMatterMarkdownToken], int, Optional[List[str]]
    ]:
        starting_line = token_to_use
        clean_starting_line = starting_line.rstrip(Constants.ascii_whitespace)
        repeat_again = True
        have_closing = False
        collected_lines: List[str] = []
        POGGER.info("Metadata prefix detected, scanning for metadata header.")
        next_line = None
        while repeat_again:
            next_line = source_provider.get_next_line()
            if next_line and next_line.rstrip(Constants.ascii_whitespace):
                start_char, _ = ThematicLeafBlockProcessor.is_thematic_break(
                    next_line.rstrip(Constants.ascii_whitespace),
                    0,
                    "",
                    whitespace_allowed_between_characters=False,
                )
                have_closing = bool(
                    start_char
                ) and clean_starting_line == next_line.rstrip(
                    Constants.ascii_whitespace
                )
                repeat_again = not have_closing
            elif not self.__allow_blank_lines:
                repeat_again = False
                assert next_line is not None
                collected_lines.append(next_line)
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
        matter_map = FrontMatterExtension.__validate_yaml(collected_lines)
        POGGER.debug("ret=$s,type=$s", matter_map, type(matter_map))
        if matter_map is None or isinstance(matter_map, str):
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
    def __validate_yaml(collected_lines: List[str]) -> Union[Any, str]:
        loaded_document = None
        try:
            # print(collected_lines)
            joined_lines = "\n".join(collected_lines)
            loaded_document = yaml.load(joined_lines, SafeLoader)
            did_load_as_yaml = not isinstance(loaded_document, str)
        except yaml.MarkedYAMLError:
            did_load_as_yaml = False

        # This is specifically to trigger test_front_matter_20.
        assert not (
            loaded_document
            and did_load_as_yaml
            and "test" in loaded_document
            and loaded_document["test"] == "assert"
        )

        if did_load_as_yaml:
            did_load_as_yaml = loaded_document is not None

        return (
            loaded_document
            if did_load_as_yaml
            else "Front matter was not parseable as valid YAML."
        )
