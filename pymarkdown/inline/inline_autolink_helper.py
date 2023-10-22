"""
Module to help with the parsing of autolink inline elements.
"""
import logging
import re
import string
from typing import Optional, Tuple, Union, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.html.html_raw_helper import HtmlRawHelper
from pymarkdown.inline.inline_request import InlineRequest
from pymarkdown.inline.inline_response import InlineResponse
from pymarkdown.tokens.email_autolink_markdown_token import EmailAutolinkMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.raw_html_markdown_token import RawHtmlMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken
from pymarkdown.tokens.uri_autolink_markdown_token import UriAutolinkMarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class InlineAutoLinkHelper:
    __scheme_end_character = ":"
    __valid_scheme_characters = f"{string.ascii_letters}{string.digits}.-+"
    __valid_email_regex = (
        "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}"
        + "[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    )

    angle_bracket_start = "<"
    __angle_bracket_end = ">"

    """
    Class to help with the parsing of autolink inline elements.
    """

    @staticmethod
    def __handle_raw_html(
        between_brackets: str,
        remaining_line: str,
        inline_request: InlineRequest,
        new_column_number: int,
        closing_angle_index: int,
    ) -> Tuple[Optional[Union[RawHtmlMarkdownToken, TextMarkdownToken]], str, int]:
        assert inline_request.line_number is not None
        new_token, after_index = HtmlRawHelper.parse_raw_html(
            between_brackets,
            remaining_line,
            inline_request.line_number,
            new_column_number,
            inline_request,
        )
        if after_index != -1:
            closing_angle_index = after_index + inline_request.next_index + 1
            assert new_token is not None
            if new_token.is_inline_raw_html:
                html_token = cast(RawHtmlMarkdownToken, new_token)
                between_brackets = html_token.raw_tag
            else:
                between_brackets = between_brackets
        return new_token, between_brackets, closing_angle_index

    @staticmethod
    def handle_angle_brackets(inline_request: InlineRequest) -> InlineResponse:
        """
        Given an open angle bracket, determine which of the three possibilities it is.
        """
        closing_angle_index = inline_request.source_text.find(
            InlineAutoLinkHelper.__angle_bracket_end, inline_request.next_index
        )
        if closing_angle_index not in (-1, inline_request.next_index + 1):
            between_brackets, remaining_line = (
                inline_request.source_text[
                    inline_request.next_index + 1 : closing_angle_index
                ],
                inline_request.source_text[inline_request.next_index + 1 :],
            )
            closing_angle_index += 1

            assert inline_request.line_number is not None
            assert inline_request.column_number is not None
            assert inline_request.remaining_line is not None
            new_column_number = inline_request.column_number + len(
                inline_request.remaining_line
            )

            new_token: Optional[
                MarkdownToken
            ] = InlineAutoLinkHelper.__parse_valid_uri_autolink(
                between_brackets, inline_request.line_number, new_column_number
            )
            if not new_token:
                new_token = InlineAutoLinkHelper.__parse_valid_email_autolink(
                    between_brackets, inline_request.line_number, new_column_number
                )
            if not new_token:
                (
                    new_token,
                    between_brackets,
                    closing_angle_index,
                ) = InlineAutoLinkHelper.__handle_raw_html(
                    between_brackets,
                    remaining_line,
                    inline_request,
                    new_column_number,
                    closing_angle_index,
                )
        else:
            new_token, between_brackets = None, None

        inline_response = InlineResponse()
        if new_token:
            (
                inline_response.new_string,
                inline_response.new_index,
                inline_response.new_tokens,
                between_brackets,
            ) = (
                "",
                closing_angle_index,
                [new_token],
                f"{InlineAutoLinkHelper.angle_bracket_start}{between_brackets}{InlineAutoLinkHelper.__angle_bracket_end}",
            )
        else:
            inline_response.new_string, inline_response.new_index, between_brackets = (
                InlineAutoLinkHelper.angle_bracket_start,
                inline_request.next_index + 1,
                InlineAutoLinkHelper.angle_bracket_start,
            )

        (
            inline_response.delta_line_number,
            inline_response.delta_column_number,
        ) = ParserHelper.calculate_deltas(between_brackets)
        return inline_response

    @staticmethod
    def __parse_valid_email_autolink(
        text_to_parse: str, line_number: int, column_number: int
    ) -> Optional[EmailAutolinkMarkdownToken]:
        """
        Parse a possible email autolink and determine if it is valid.
        """
        return (
            EmailAutolinkMarkdownToken(text_to_parse, line_number, column_number)
            if re.match(InlineAutoLinkHelper.__valid_email_regex, text_to_parse)
            else None
        )

    @staticmethod
    def __parse_valid_uri_autolink(
        text_to_parse: str, line_number: int, column_number: int
    ) -> Optional[UriAutolinkMarkdownToken]:
        """
        Parse a possible uri autolink and determine if it is valid.
        """

        if (
            InlineAutoLinkHelper.angle_bracket_start not in text_to_parse
            and text_to_parse[0] in string.ascii_letters
        ):
            path_index, uri_scheme = ParserHelper.collect_while_one_of_characters(
                text_to_parse, 1, InlineAutoLinkHelper.__valid_scheme_characters
            )
            assert path_index is not None
            uri_scheme, text_to_parse_size = f"{text_to_parse[0]}{uri_scheme}", len(
                text_to_parse
            )
            if (
                2 <= len(uri_scheme) <= 32
                and path_index < text_to_parse_size
                and text_to_parse[path_index]
                == InlineAutoLinkHelper.__scheme_end_character
            ):
                path_index += 1
                while (
                    path_index < text_to_parse_size
                    and ord(text_to_parse[path_index]) > 32
                ):
                    path_index += 1
                if path_index == text_to_parse_size:
                    return UriAutolinkMarkdownToken(
                        text_to_parse, line_number, column_number
                    )
        else:
            uri_scheme, path_index = "", -1
        return None
