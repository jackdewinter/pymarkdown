"""
Module to provide for an encapsulation of the link reference definition element.
"""

# pylint: disable=too-many-instance-attributes
from typing import List, Optional, Union, cast

from typing_extensions import override

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.links.link_reference_info import LinkReferenceInfo
from pymarkdown.links.link_reference_titles import LinkReferenceTitles
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)


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

        if link_value:
            self.__link_destination, self.__link_title = (
                link_value.inline_link,
                link_value.inline_title,
            )
        else:
            self.__link_destination, self.__link_title = "", ""

        if link_debug:
            (
                self.__link_name_debug,
                self.__link_destination_whitespace,
                self.__link_destination_raw,
                self.__link_title_whitespace,
                self.__link_title_raw,
                self.__end_whitespace,
            ) = (
                (
                    ""
                    if link_debug.collected_destination == self.__link_name
                    else link_debug.collected_destination
                ),
                link_debug.line_destination_whitespace,
                (
                    ""
                    if link_debug.inline_raw_link == self.__link_destination
                    else link_debug.inline_raw_link
                ),
                link_debug.line_title_whitespace,
                (
                    ""
                    if link_debug.inline_raw_title == self.__link_title
                    else link_debug.inline_raw_title
                ),
                link_debug.end_whitespace,
            )
        else:
            self.__link_name_debug = self.__link_destination_whitespace = (
                self.__link_destination_raw
            ) = self.__link_title_whitespace = self.__link_title_raw = (
                self.__end_whitespace
            ) = ""

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
        assert self.__end_whitespace is not None, "This field should be defined."
        assert self.__link_title_raw is not None, "This field should be defined."
        assert self.__link_title is not None, "This field should be defined."
        assert self.__link_title_whitespace is not None, "This field should be defined."
        assert self.__link_destination_raw is not None, "This field should be defined."
        assert self.__link_destination is not None, "This field should be defined."
        assert (
            self.__link_destination_whitespace is not None
        ), "This field should be defined."
        assert self.__link_name_debug is not None, "This field should be defined."
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

    @override
    def _modify_token(self, field_name: str, field_value: Union[str, int]) -> bool:
        if field_name == "link_destination_whitespace" and isinstance(field_value, str):
            self.__link_destination_whitespace = field_value
            extra_data = self.__validate_proper_fields_are_valid(
                self.extracted_whitespace
            )
            super()._set_extra_data(extra_data)
            return True
        if field_name == "link_title_whitespace" and isinstance(field_value, str):
            self.__link_title_whitespace = field_value
            extra_data = self.__validate_proper_fields_are_valid(
                self.extracted_whitespace
            )
            super()._set_extra_data(extra_data)
            return True
        if field_name == "link_name_debug" and isinstance(field_value, str):
            self.__link_name_debug = field_value
            extra_data = self.__validate_proper_fields_are_valid(
                self.extracted_whitespace
            )
            super()._set_extra_data(extra_data)
            return True
        return super()._modify_token(field_name, field_value)

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            LinkReferenceDefinitionMarkdownToken,
            LinkReferenceDefinitionMarkdownToken.__rehydrate_link_reference_definition,
            None,
        )

    @staticmethod
    def __rehydrate_link_reference_definition(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        _ = (previous_token, context)

        current_lrd_token = cast(LinkReferenceDefinitionMarkdownToken, current_token)
        link_title_text = (
            current_lrd_token.link_title_raw or current_lrd_token.link_title
        )
        link_destination_text = (
            current_lrd_token.link_destination_raw or current_lrd_token.link_destination
        )
        assert (
            current_lrd_token.link_destination_whitespace is not None
        ), "This field should be defined."
        assert link_destination_text is not None, "This field should be defined."
        assert (
            current_lrd_token.link_title_whitespace is not None
        ), "This field should be defined."
        assert link_title_text is not None, "This field should be defined."
        assert (
            current_lrd_token.end_whitespace is not None
        ), "This field should be defined."
        link_def_parts: List[str] = [
            current_lrd_token.extracted_whitespace,
            "[",
            current_lrd_token.link_name_debug or current_lrd_token.link_name,
            "]:",
            current_lrd_token.link_destination_whitespace,
            link_destination_text,
            current_lrd_token.link_title_whitespace,
            link_title_text,
            current_lrd_token.end_whitespace,
            ParserHelper.newline_character,
        ]

        return "".join(link_def_parts)

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            LinkReferenceDefinitionMarkdownToken,
            LinkReferenceDefinitionMarkdownToken.__handle_link_reference_definition_token,
            None,
        )

    @staticmethod
    def __handle_link_reference_definition_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (transform_state, next_token)

        return output_html


# pylint: enable=too-many-instance-attributes
