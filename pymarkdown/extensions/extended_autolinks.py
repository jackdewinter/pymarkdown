"""
Module to provide for extending what is considered to be an autolink.
"""

from typing import Optional, Tuple, cast

from application_properties import ApplicationPropertiesFacade

from pymarkdown.container_blocks.parse_block_pass_properties import (
    ParseBlockPassProperties,
)
from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager_constants import (
    ExtensionManagerConstants,
)
from pymarkdown.extension_manager.parser_extension import ParserExtension
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.inline.inline_request import InlineRequest
from pymarkdown.inline.inline_response import InlineResponse
from pymarkdown.tokens.email_autolink_markdown_token import EmailAutolinkMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken
from pymarkdown.tokens.uri_autolink_markdown_token import UriAutolinkMarkdownToken


class MarkdownExtendedAutolinksExtension(ParserExtension):
    """
    Extension to implement the extended autolinks extension.
    """

    __valid_autolink_domain_characters = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"
    )
    __email_first_part = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-_+"
    )
    __email_domain_part = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-_"
    )
    __xmpp_resource_part = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.@"
    )

    def get_identifier(self) -> str:
        """
        Get the identifier associated with this extension.
        """
        return "markdown-extended-autolinks"

    def get_details(self) -> ExtensionDetails:
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=self.get_identifier(),
            extension_name="Markdown Extended Autolinks",
            extension_description="Allows extended parsing of Markdown Autolinks.",
            extension_enabled_by_default=False,
            extension_version="0.5.0",
            extension_interface_version=ExtensionManagerConstants.EXTENSION_INTERFACE_VERSION_BASIC,
            extension_url="https://github.github.com/gfm/#autolinks-extension-",
            extension_configuration=None,
        )

    def apply_configuration(
        self, extension_specific_facade: ApplicationPropertiesFacade
    ) -> None:
        """
        Apply any configuration required by the extension.
        """
        _ = extension_specific_facade  # pragma: no cover

    @staticmethod
    def __handle_www_autolink_prefix(
        inline_request: InlineRequest,
    ) -> Tuple[bool, bool, Optional[int]]:
        is_valid_prefix = not inline_request.next_index or inline_request.source_text[
            inline_request.next_index - 1
        ] in (" ", "(", "*", "_", "~")

        is_valid_start = False
        num_collected, new_index = ParserHelper.collect_while_character(
            inline_request.source_text, inline_request.next_index, "w"
        )
        if new_index is not None and new_index < len(inline_request.source_text):
            is_valid_start = (
                new_index is not None
                and inline_request.source_text[new_index] == "."
                and num_collected == 3
            )
            if is_valid_start:
                new_index += 1

        return is_valid_prefix, is_valid_start, new_index

    @staticmethod
    def __handle_www_autolink_domain(
        source_text: str, new_index: int
    ) -> Tuple[int, Optional[str]]:
        domain_parts = []
        keep_collecting = True
        while keep_collecting:
            index_after_collect, ex_text = ParserHelper.collect_while_one_of_characters(
                source_text,
                new_index,
                MarkdownExtendedAutolinksExtension.__valid_autolink_domain_characters,
            )
            if not ex_text:
                new_index -= 1
                break
            assert index_after_collect is not None
            domain_parts.append(ex_text)
            new_index = index_after_collect
            keep_collecting = (
                index_after_collect < len(source_text)
                and source_text[index_after_collect] == "."
            )
            if keep_collecting:
                new_index += 1
        if (
            len(domain_parts) >= 2
            and "_" not in domain_parts[-1]
            and "_" not in domain_parts[-2]
        ):
            return new_index, ".".join(domain_parts)
        return -1, None

    @staticmethod
    def __handle_www_autolink_valid_path(source_text: str, new_index: int) -> int:
        current_index = new_index
        if current_index < len(source_text) and source_text[current_index] == "/":
            current_index, _ = ParserHelper.collect_until_one_of_characters_verified(
                source_text, current_index + 1, " \t\n<"
            )

            # Strip any trailing characters.
            while source_text[current_index - 1] in "?!.,:*_~":
                current_index -= 1

            # Balance out any parentheses.
            curent_path = source_text[new_index:current_index]
            keep_going = True
            while keep_going and curent_path.endswith(")"):
                current_path_open_count = curent_path.count("(")
                current_path_close_count = curent_path.count(")")
                if current_path_close_count > current_path_open_count:
                    current_index -= 1
                    curent_path = source_text[new_index:current_index]
                else:
                    keep_going = False

            if curent_path.endswith(";"):
                amper_index = curent_path.rfind("&")
                if amper_index != -1:
                    reference_text = curent_path[amper_index + 1 : -1]
                    if reference_text.isalnum():
                        current_index -= len(reference_text) + 2
        return current_index

    @staticmethod
    def handle_www_autolink(
        parser_properties: ParseBlockPassProperties, inline_request: InlineRequest
    ) -> InlineResponse:
        """
        Take care of the "www." versions, that start with a 'w'
        """
        _ = parser_properties
        inline_response = InlineResponse()
        new_token, between_brackets = None, None

        (
            is_valid_prefix,
            is_valid_start,
            new_index,
        ) = MarkdownExtendedAutolinksExtension.__handle_www_autolink_prefix(
            inline_request
        )
        if is_valid_prefix and is_valid_start:
            assert new_index is not None
            (
                next_index,
                _,
            ) = MarkdownExtendedAutolinksExtension.__handle_www_autolink_domain(
                inline_request.source_text, new_index
            )
            if next_index != -1:
                next_index = (
                    MarkdownExtendedAutolinksExtension.__handle_www_autolink_valid_path(
                        inline_request.source_text, next_index
                    )
                )
                auto_link_text = inline_request.source_text[
                    inline_request.next_index : next_index
                ]
            if next_index != -1:
                assert inline_request.line_number is not None
                assert inline_request.column_number is not None
                assert inline_request.remaining_line is not None
                new_token = UriAutolinkMarkdownToken(
                    auto_link_text,
                    inline_request.line_number,
                    inline_request.column_number + len(inline_request.remaining_line),
                    add_http_prefix=True,
                )

        if new_token:
            (
                inline_response.new_string,
                inline_response.new_index,
                inline_response.new_tokens,
                between_brackets,
            ) = (
                "",
                next_index,
                [new_token],
                auto_link_text,
            )
        else:
            # Skip the current character
            inline_response.new_string, inline_response.new_index, between_brackets = (
                inline_request.source_text[inline_request.next_index : new_index],
                new_index,
                inline_request.source_text[inline_request.next_index : new_index],
            )

        (
            inline_response.delta_line_number,
            inline_response.delta_column_number,
        ) = ParserHelper.calculate_deltas(between_brackets)
        return inline_response

    @staticmethod
    def __handle_http_autolink_prefix(
        inline_request: InlineRequest,
    ) -> Tuple[bool, bool, int]:
        is_valid_prefix = not inline_request.next_index or inline_request.source_text[
            inline_request.next_index - 1
        ] in (" ", "(", "*", "_", "~")

        is_valid_start = False
        new_index = inline_request.next_index + 1
        first_pattern = "http://"
        second_pattern = "https://"
        rest_of_line = inline_request.source_text[inline_request.next_index :]
        if rest_of_line.startswith(first_pattern):
            is_valid_start = True
            new_index = inline_request.next_index + len(first_pattern)
        elif rest_of_line.startswith(second_pattern):
            is_valid_start = True
            new_index = inline_request.next_index + len(second_pattern)

        return is_valid_prefix, is_valid_start, new_index

    @staticmethod
    def handle_http_autolink(
        parser_properties: ParseBlockPassProperties, inline_request: InlineRequest
    ) -> InlineResponse:
        """
        Take care of the "http://" and "https://" versions, that start with an 'h'
        """
        _ = parser_properties
        inline_response = InlineResponse()
        new_token, between_brackets = None, None

        (
            is_valid_prefix,
            is_valid_start,
            new_index,
        ) = MarkdownExtendedAutolinksExtension.__handle_http_autolink_prefix(
            inline_request
        )
        if is_valid_prefix and is_valid_start:
            (
                next_index,
                _,
            ) = MarkdownExtendedAutolinksExtension.__handle_www_autolink_domain(
                inline_request.source_text, new_index
            )
            if next_index != -1:
                next_index = (
                    MarkdownExtendedAutolinksExtension.__handle_www_autolink_valid_path(
                        inline_request.source_text, next_index
                    )
                )
                autolink_text = inline_request.source_text[
                    inline_request.next_index : next_index
                ]
            if next_index != -1:
                assert inline_request.line_number is not None
                assert inline_request.column_number is not None
                assert inline_request.remaining_line is not None
                new_token = UriAutolinkMarkdownToken(
                    autolink_text,
                    inline_request.line_number,
                    inline_request.column_number + len(inline_request.remaining_line),
                    add_http_prefix=False,
                    add_angle_brackets=False,
                )

        if new_token:
            (
                inline_response.new_string,
                inline_response.new_index,
                inline_response.new_tokens,
                between_brackets,
            ) = (
                "",
                next_index,
                [new_token],
                autolink_text,
            )
        else:
            # Skip the current character
            inline_response.new_string, inline_response.new_index, between_brackets = (
                inline_request.source_text[inline_request.next_index : new_index],
                new_index,
                inline_request.source_text[inline_request.next_index : new_index],
            )

        (
            inline_response.delta_line_number,
            inline_response.delta_column_number,
        ) = ParserHelper.calculate_deltas(between_brackets)
        return inline_response

    @staticmethod
    def __handle_email_autolink_consume_inner(
        inline_request: InlineRequest,
        inline_response: InlineResponse,
        user_part_index: int,
        domain_part_index: int,
        user_id_part: str,
    ) -> Tuple[str, int]:
        collected_text = inline_request.source_text[user_part_index:domain_part_index]
        assert inline_request.current_string is not None
        assert inline_request.remaining_line is not None
        combined_text = inline_request.current_string + inline_request.remaining_line
        if not combined_text.endswith(user_id_part):
            left_index = len(inline_request.inline_blocks) - 1
            while (
                left_index >= 0
                and (
                    inline_request.inline_blocks[left_index].is_text
                    or inline_request.inline_blocks[left_index].is_special_text
                )
                and (len(combined_text) < len(user_id_part))
            ):
                text_token = cast(
                    TextMarkdownToken, inline_request.inline_blocks[left_index]
                )
                combined_text = text_token.token_text + combined_text
                left_index -= 1
            assert combined_text.endswith(user_id_part)
        inline_response.reduce_remaining_line_by = len(user_id_part)
        return collected_text, domain_part_index

    # pylint: disable=too-many-arguments
    @staticmethod
    def __handle_email_autolink_consume_token(
        inline_request: InlineRequest,
        inline_response: InlineResponse,
        user_part_index: int,
        domain_part_index: int,
        user_id_part: str,
        domain_part: str,
    ) -> Tuple[EmailAutolinkMarkdownToken, Optional[str], int]:
        assert user_part_index is not None
        assert domain_part_index is not None
        (
            collected_text,
            domain_part_index,
        ) = MarkdownExtendedAutolinksExtension.__handle_email_autolink_consume_inner(
            inline_request,
            inline_response,
            user_part_index,
            domain_part_index,
            user_id_part,
        )

        assert inline_request.line_number is not None
        assert inline_request.column_number is not None
        assert inline_request.remaining_line is not None
        if inline_request.remaining_line.endswith(user_id_part):
            new_column_number = inline_request.column_number - (
                len(user_id_part) - len(inline_request.remaining_line)
            )
            between_brackets = collected_text
        else:
            assert user_id_part.endswith(inline_request.remaining_line)
            fred = user_id_part[: -len(inline_request.remaining_line)]
            new_column_number = (
                inline_request.column_number
                + len(inline_request.remaining_line)
                - len(user_id_part)
            )
            between_brackets = inline_request.remaining_line + domain_part
            if fred[-1] != "_":
                between_brackets += "@"

        new_token = EmailAutolinkMarkdownToken(
            collected_text,
            inline_request.line_number,
            new_column_number,
            add_angle_brackets=False,
        )
        next_index = domain_part_index
        return new_token, between_brackets, next_index

    # pylint: enable=too-many-arguments

    @staticmethod
    def __handle_email_autolink_consume(
        inline_request: InlineRequest,
        inline_response: InlineResponse,
        at_index: int,
        between_brackets: Optional[str],
    ) -> Tuple[Optional[EmailAutolinkMarkdownToken], Optional[str], int]:
        _, user_part_index = (
            ParserHelper.collect_backwards_while_one_of_characters_verified(
                inline_request.source_text,
                at_index - 1,
                MarkdownExtendedAutolinksExtension.__email_first_part,
            )
        )
        user_id_part = inline_request.source_text[user_part_index:at_index]
        domain_part_index, domain_part = (
            ParserHelper.collect_while_one_of_characters_verified(
                inline_request.source_text,
                at_index + 1,
                MarkdownExtendedAutolinksExtension.__email_domain_part,
            )
        )
        new_token = None
        next_index = -1
        collected_text = inline_request.source_text[at_index:domain_part_index]
        if collected_text.endswith("."):
            collected_text = collected_text[:-1]
            domain_part_index -= 1
        if (
            ".." not in collected_text
            and collected_text.count(".") >= 1
            and not collected_text.endswith("-")
            and not collected_text.endswith("_")
        ):
            (
                new_token,
                between_brackets,
                next_index,
            ) = MarkdownExtendedAutolinksExtension.__handle_email_autolink_consume_token(
                inline_request,
                inline_response,
                user_part_index,
                domain_part_index,
                user_id_part,
                domain_part,
            )
        return new_token, between_brackets, next_index

    @staticmethod
    def __handle_mail_autolink_prefix(
        inline_request: InlineRequest,
    ) -> Tuple[bool, bool, int]:
        is_valid_prefix = not inline_request.next_index or inline_request.source_text[
            inline_request.next_index - 1
        ] in (" ", "(", "*", "_", "~")

        is_valid_start = False
        new_index = inline_request.next_index + 1
        first_pattern = "mailto:"
        second_pattern = "xmpp:"
        rest_of_line = inline_request.source_text[inline_request.next_index :]
        if rest_of_line.startswith(first_pattern):
            is_valid_start = True
            new_index = inline_request.next_index + len(first_pattern)
        elif rest_of_line.startswith(second_pattern):
            is_valid_start = True
            new_index = inline_request.next_index + len(second_pattern)

        return is_valid_prefix, is_valid_start, new_index

    @staticmethod
    def __handle_email_autolink_named_resource(
        inline_request: InlineRequest,
        is_valid_prefix: bool,
        is_valid_start: bool,
        domain_part_index: Optional[int],
    ) -> Optional[int]:
        if (
            is_valid_prefix
            and is_valid_start
            and inline_request.source_text[inline_request.next_index] == "x"
            and domain_part_index is not None
            and ParserHelper.is_character_at_index(
                inline_request.source_text, domain_part_index, "/"
            )
        ):
            after_ex_text_index, ex_text = ParserHelper.collect_while_one_of_characters(
                inline_request.source_text,
                domain_part_index + 1,
                MarkdownExtendedAutolinksExtension.__xmpp_resource_part,
            )
            if ex_text:
                domain_part_index = after_ex_text_index
        return domain_part_index

    @staticmethod
    def __handle_email_autolink_named_main(
        inline_request: InlineRequest,
    ) -> Tuple[bool, bool, int, int, Optional[int]]:
        next_index = -1
        collected_text = None
        domain_part_index: Optional[int] = None
        (
            is_valid_prefix,
            is_valid_start,
            new_index,
        ) = MarkdownExtendedAutolinksExtension.__handle_mail_autolink_prefix(
            inline_request
        )
        if is_valid_prefix and is_valid_start:
            user_part_index, _ = ParserHelper.collect_while_one_of_characters_verified(
                inline_request.source_text,
                new_index,
                MarkdownExtendedAutolinksExtension.__email_first_part,
            )
            is_valid_prefix = ParserHelper.is_character_at_index(
                inline_request.source_text, user_part_index, "@"
            )
        if is_valid_prefix and is_valid_start:
            user_part_index += 1
            domain_part_index, _ = (
                ParserHelper.collect_while_one_of_characters_verified(
                    inline_request.source_text,
                    user_part_index,
                    MarkdownExtendedAutolinksExtension.__email_domain_part,
                )
            )
            collected_text = inline_request.source_text[
                user_part_index:domain_part_index
            ]
            if collected_text.endswith("."):
                collected_text = collected_text[:-1]
                domain_part_index -= 1
            is_valid_prefix = (
                ".." not in collected_text
                and collected_text.count(".") >= 1
                and not collected_text.endswith("-")
                and not collected_text.endswith("_")
            )
        return (
            is_valid_prefix,
            is_valid_start,
            new_index,
            next_index,
            domain_part_index,
        )

    @staticmethod
    def __handle_email_autolink_named(
        parser_properties: ParseBlockPassProperties, inline_request: InlineRequest
    ) -> InlineResponse:
        """
        Take care of the "www." versions, that start with a 'w'
        """
        _ = parser_properties
        inline_response = InlineResponse()
        new_token, between_brackets = None, None
        domain_part_index: Optional[int] = None

        (
            is_valid_prefix,
            is_valid_start,
            new_index,
            next_index,
            domain_part_index,
        ) = MarkdownExtendedAutolinksExtension.__handle_email_autolink_named_main(
            inline_request
        )
        domain_part_index = (
            MarkdownExtendedAutolinksExtension.__handle_email_autolink_named_resource(
                inline_request, is_valid_prefix, is_valid_start, domain_part_index
            )
        )
        if is_valid_prefix and is_valid_start:
            assert domain_part_index is not None
            next_index = domain_part_index
            autolink_text = inline_request.source_text[
                inline_request.next_index : next_index
            ]
            assert inline_request.line_number is not None
            assert inline_request.column_number is not None
            new_token = UriAutolinkMarkdownToken(
                autolink_text,
                inline_request.line_number,
                inline_request.column_number,
                add_http_prefix=False,
                add_angle_brackets=False,
            )

        if new_token:
            (
                inline_response.new_string,
                inline_response.new_index,
                inline_response.new_tokens,
                between_brackets,
            ) = (
                "",
                next_index,
                [new_token],
                autolink_text,
            )
        else:
            # Skip the current character
            inline_response.new_string, inline_response.new_index, between_brackets = (
                inline_request.source_text[inline_request.next_index : new_index],
                new_index,
                inline_request.source_text[inline_request.next_index : new_index],
            )

        (
            inline_response.delta_line_number,
            inline_response.delta_column_number,
        ) = ParserHelper.calculate_deltas(between_brackets)
        return inline_response

    @staticmethod
    def handle_email_autolink(
        parser_properties: ParseBlockPassProperties, inline_request: InlineRequest
    ) -> InlineResponse:
        """
        Handle a normal email autolink
        """
        ff = inline_request.source_text[inline_request.next_index]
        if ff != "@":
            return MarkdownExtendedAutolinksExtension.__handle_email_autolink_named(
                parser_properties, inline_request
            )
        _ = parser_properties
        inline_response = InlineResponse()
        new_token = None
        between_brackets: Optional[str] = None
        new_index = inline_request.next_index + 1
        next_index = inline_request.next_index

        at_index = inline_request.next_index
        if 0 < at_index < len(inline_request.source_text):
            (
                new_token,
                between_brackets,
                next_index,
            ) = MarkdownExtendedAutolinksExtension.__handle_email_autolink_consume(
                inline_request, inline_response, at_index, between_brackets
            )

        if new_token:
            (
                inline_response.new_string,
                inline_response.new_index,
                inline_response.new_tokens,
            ) = (
                "",
                next_index,
                [new_token],
            )
        else:
            # Skip the current character
            inline_response.new_string, inline_response.new_index, between_brackets = (
                inline_request.source_text[inline_request.next_index : new_index],
                new_index,
                inline_request.source_text[inline_request.next_index : new_index],
            )

        assert between_brackets is not None
        (
            inline_response.delta_line_number,
            inline_response.delta_column_number,
        ) = ParserHelper.calculate_deltas(between_brackets)
        return inline_response
