"""
Module to provide for an encapsulation of the link element.
"""

import logging
from typing import List, Optional, cast

from pymarkdown.general.constants import Constants
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.links.link_helper_properties import LinkHelperProperties
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.tokens.reference_markdown_token import ReferenceMarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)

POGGER = ParserLogger(logging.getLogger(__name__))


class LinkStartMarkdownToken(ReferenceMarkdownToken):
    """
    Class to provide for an encapsulation of the link element.
    """

    def __init__(
        self,
        text_from_blocks: str,
        line_number: int,
        column_number: int,
        lhp: LinkHelperProperties,
    ) -> None:
        # assert lhp.pre_inline_link is not None
        # assert lhp.label_type is not None
        # assert lhp.inline_link is not None
        ReferenceMarkdownToken.__init__(
            self,
            lhp,
            LinkStartMarkdownToken.get_markdown_token_type(),
            "",
            text_from_blocks,
            line_number=line_number,
            column_number=column_number,
            requires_end_token=True,
            can_force_close=False,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_inline_link

    # pylint: enable=protected-access

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            LinkStartMarkdownToken,
            LinkStartMarkdownToken.__rehydrate_inline_link,
            LinkStartMarkdownToken.__rehydrate_inline_link_end,
        )

    @staticmethod
    def __rehydrate_inline_link(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the start of the link from the token.
        """
        _ = previous_token

        inline_current_token = cast(LinkStartMarkdownToken, current_token)
        context.block_stack.append(current_token)
        rehydrated_text = LinkStartMarkdownToken.rehydrate_inline_link_text_from_token(
            inline_current_token
        )
        return LinkStartMarkdownToken.insert_leading_whitespace_at_newlines(
            context, rehydrated_text
        )

    @staticmethod
    def __rehydrate_inline_link_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the end of the link from the token.
        """
        _ = (current_token, previous_token, next_token)

        del context.block_stack[-1]
        return ""

    @staticmethod
    def rehydrate_inline_link_text_from_token(
        link_token: ReferenceMarkdownToken,
    ) -> str:
        """
        Given a link token, rehydrate it's original text from the token.
        """

        link_parts = []
        if link_token.label_type == Constants.link_type__shortcut:
            link_parts.extend(
                [
                    "[",
                    ParserHelper.remove_all_from_text(link_token.text_from_blocks),
                    "]",
                ]
            )
        elif link_token.label_type == Constants.link_type__full:
            assert link_token.ex_label is not None
            link_parts.extend(
                ["[", link_token.text_from_blocks, "][", link_token.ex_label, "]"]
            )
        elif link_token.label_type == Constants.link_type__collapsed:
            link_parts.extend(["[", link_token.text_from_blocks, "][]"])
        else:
            assert link_token.label_type == Constants.link_type__inline
            LinkStartMarkdownToken.__rehydrate_inline_link_text_from_token_type_inline(
                link_token, link_parts
            )

        return "".join(link_parts)

    @staticmethod
    def __rehydrate_inline_link_text_from_token_type_inline(
        link_token: ReferenceMarkdownToken, link_parts: List[str]
    ) -> None:
        assert link_token.before_title_whitespace is not None
        assert link_token.before_link_whitespace is not None
        link_parts.extend(
            [
                "[",
                ParserHelper.remove_all_from_text(link_token.text_from_blocks),
                "](",
                link_token.before_link_whitespace,
                f"<{link_token.active_link_uri}>"
                if link_token.did_use_angle_start
                else link_token.active_link_uri,
                link_token.before_title_whitespace,
            ]
        )
        if link_token.active_link_title:
            if link_token.inline_title_bounding_character == "'":
                title_prefix = "'"
                title_suffix = "'"
            elif link_token.inline_title_bounding_character == "(":
                title_prefix = "("
                title_suffix = ")"
            else:
                title_prefix = '"'
                title_suffix = '"'

            assert link_token.after_title_whitespace is not None
            link_parts.extend(
                [
                    title_prefix,
                    link_token.active_link_title,
                    title_suffix,
                    link_token.after_title_whitespace,
                ]
            )
        link_parts.append(")")

    @staticmethod
    def insert_leading_whitespace_at_newlines(
        context: MarkdownTransformContext, text_to_modify: str
    ) -> str:
        """
        Deal with re-inserting any removed whitespace at the starts of lines.
        """
        if ParserHelper.newline_character in text_to_modify:
            owning_paragraph_token = next(
                (
                    context.block_stack[search_index]
                    for search_index in range(len(context.block_stack) - 1, -1, -1)
                    if context.block_stack[search_index].is_paragraph
                ),
                None,
            )

            POGGER.debug(
                f"text>before>{ParserHelper.make_value_visible(text_to_modify)}"
            )
            text_to_modify = ParserHelper.remove_all_from_text(text_to_modify)
            POGGER.debug(
                f"text>after>{ParserHelper.make_value_visible(text_to_modify)}"
            )

            if owning_paragraph_token:
                paragraph_token = cast(ParagraphMarkdownToken, owning_paragraph_token)
                (
                    text_to_modify,
                    paragraph_token.rehydrate_index,
                ) = ParserHelper.recombine_string_with_whitespace(
                    text_to_modify,
                    paragraph_token.extracted_whitespace,
                    paragraph_token.rehydrate_index,
                    post_increment_index=False,
                )
        return text_to_modify

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            LinkStartMarkdownToken,
            LinkStartMarkdownToken.__handle_start_link_token,
            LinkStartMarkdownToken.__handle_end_link_token,
        )

    @staticmethod
    def __handle_start_link_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = transform_state

        link_token = cast(LinkStartMarkdownToken, next_token)
        return "".join(
            [
                output_html,
                '<a href="',
                link_token.link_uri,
                f'" title="{link_token.link_title}' if link_token.link_title else "",
                '">',
            ]
        )

    @staticmethod
    def __handle_end_link_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (next_token, transform_state)

        return f"{output_html}</a>"
