"""
Module to provide for an encapsulation of the link reference definition element.
"""

# pylint: disable=too-many-instance-attributes
from typing import Optional

from pymarkdown.links.link_reference_info import LinkReferenceInfo
from pymarkdown.links.link_reference_titles import LinkReferenceTitles
from pymarkdown.position_marker import PositionMarker
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken


class LinkReferenceDefinitionMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the link reference definition element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        did_add_definition: bool,
        extracted_whitespace: str,
        link_name: str,
        link_value: LinkReferenceTitles,
        link_debug: Optional[LinkReferenceInfo],
        position_marker: PositionMarker,
    ) -> None:
        self.__did_add_definition = did_add_definition
        self.__link_name = link_name

        assert link_value
        self.__link_destination, self.__link_title = (
            link_value.inline_link,
            link_value.inline_title,
        )
        # else:
        #     self.__link_destination, self.__link_title = "", ""

        assert link_debug
        (
            self.__link_name_debug,
            self.__link_destination_whitespace,
            self.__link_destination_raw,
            self.__link_title_whitespace,
            self.__link_title_raw,
            self.__end_whitespace,
        ) = (
            ""
            if link_debug.collected_destination == self.__link_name
            else link_debug.collected_destination,
            link_debug.line_destination_whitespace,
            ""
            if link_debug.inline_raw_link == self.__link_destination
            else link_debug.inline_raw_link,
            link_debug.line_title_whitespace,
            ""
            if link_debug.inline_raw_title == self.__link_title
            else link_debug.inline_raw_title,
            link_debug.end_whitespace,
        )
        # else:
        #     (
        #         self.__link_name_debug,
        #         self.__link_destination_whitespace,
        #         self.__link_destination_raw,
        #         self.__link_title_whitespace,
        #         self.__link_title_raw,
        #         self.__end_whitespace,
        #     ) = ("", "", "", "", "", "")

        extra_data = self.__validate_proper_fields_are_valid(extracted_whitespace)
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_link_reference_definition,
            extra_data,
            position_marker=position_marker,
            extracted_whitespace=extracted_whitespace,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_link_reference_definition

    # pylint: enable=protected-access

    def __validate_proper_fields_are_valid(self, extracted_whitespace: str) -> str:
        assert self.__end_whitespace is not None
        assert self.__link_title_raw is not None
        assert self.__link_title is not None
        assert self.__link_title_whitespace is not None
        assert self.__link_destination_raw is not None
        assert self.__link_destination is not None
        assert self.__link_destination_whitespace is not None
        assert self.__link_name_debug is not None
        return MarkdownToken.extra_data_separator.join(
            [
                str(self.did_add_definition),
                extracted_whitespace,
                self.__link_name,
                self.__link_name_debug,
                self.__link_destination_whitespace,
                self.__link_destination,
                self.__link_destination_raw,
                self.__link_title_whitespace,
                self.__link_title,
                self.__link_title_raw,
                self.__end_whitespace,
            ]
        )

    # pylint: enable=too-many-arguments
    @property
    def did_add_definition(self) -> bool:
        """
        Returns an indication of whether the definition was actually added.
        """
        return self.__did_add_definition

    @property
    def end_whitespace(self) -> Optional[str]:
        """
        Returns any whitespace that was extracted after the processing of this element occurred.
        """
        return self.__end_whitespace

    @property
    def link_name(self) -> str:
        """
        Returns the name of the link that was defined.
        """
        return self.__link_name

    @property
    def link_name_debug(self) -> Optional[str]:
        """
        Returns the name of the link that was defined, in debug form.
        """
        return self.__link_name_debug

    @property
    def link_destination_whitespace(self) -> Optional[str]:
        """
        Returns the whitespace that occurs before the link destination.
        """
        return self.__link_destination_whitespace

    @property
    def link_destination(self) -> Optional[str]:
        """
        Returns the destination (URI) of the link that was defined.
        """
        return self.__link_destination

    @property
    def link_destination_raw(self) -> Optional[str]:
        """
        Returns the destination (URI) of the link that was defined, in raw form.
        """
        return self.__link_destination_raw

    @property
    def link_title(self) -> Optional[str]:
        """
        Returns the title of the link that was defined.
        """
        return self.__link_title

    @property
    def link_title_raw(self) -> Optional[str]:
        """
        Returns the title of the link that was defined, in raw form.
        """
        return self.__link_title_raw

    @property
    def link_title_whitespace(self) -> Optional[str]:
        """
        Returns the whitespace that occurs after the link title.
        """
        return self.__link_title_whitespace


# pylint: enable=too-many-instance-attributes
