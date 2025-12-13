"""
Module to implement a plugin that looks for headings that do not start at the
beginning of the line.
"""

from typing import Dict, List, Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.plugins.utils.container_token_manager import ContainerTokenManager
from pymarkdown.tokens.atx_heading_markdown_token import AtxHeadingMarkdownToken
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.setext_heading_markdown_token import SetextHeadingMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class RuleMd023(RulePlugin):
    """
    Class to implement a plugin that looks for headings that do not start at the
    beginning of the line.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__setext_start_token: Optional[SetextHeadingMarkdownToken] = None
        self.__any_leading_whitespace_detected = False
        self.__seen_first_line_of_setext = False
        self.__container_manager = ContainerTokenManager()
        self.__last_skipped_text_token: Optional[TextMarkdownToken] = None
        self.__leading_spaces_split: Dict[ListStartMarkdownToken, List[str]] = {}

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="heading-start-left, header-start-left",
            plugin_id="MD023",
            plugin_enabled_by_default=True,
            plugin_description="Headings must start at the beginning of the line.",
            plugin_version="0.5.2",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md023.md",
            plugin_supports_fix=True,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__setext_start_token = None
        self.__any_leading_whitespace_detected = False
        self.__seen_first_line_of_setext = False
        self.__container_manager.clear()
        self.__leading_spaces_split = {}
        self.__last_skipped_text_token = None

    def __fix_adjustments(self, ex_ws: str, ind: int = 0) -> str:
        if self.__container_manager.container_token_stack:
            stack_length = len(self.__container_manager.container_token_stack)
            atx_container_token = self.__container_manager.container_token_stack[
                stack_length - 1
            ]
        else:
            atx_container_token = None

        fixed_whitespace = ""
        if atx_container_token is not None:
            if atx_container_token.is_block_quote_start:
                fixed_whitespace = " " if ex_ws[0] == "\t" else ""
            else:
                fixed_whitespace = ""
                if ex_ws[0] == "\t":

                    list_start_token = cast(ListStartMarkdownToken, atx_container_token)
                    track_line_index = self.__container_manager.bq_line_index[
                        stack_length
                    ]
                    adjust_line_index = self.__container_manager.list_adjust_map[
                        stack_length
                    ]

                    if list_start_token in self.__leading_spaces_split:
                        split_spaces = self.__leading_spaces_split[list_start_token]
                    else:
                        assert list_start_token.leading_spaces is not None
                        split_spaces = list_start_token.leading_spaces.split("\n")
                        self.__leading_spaces_split[list_start_token] = split_spaces
                    split_spaces[track_line_index - adjust_line_index + ind] = (
                        " " * list_start_token.indent_level
                    )
        return fixed_whitespace

    def __handle_atx_heading(
        self, context: PluginScanContext, token: AtxHeadingMarkdownToken
    ) -> None:
        if not token.extracted_whitespace:
            return

        if context.in_fix_mode:
            self.register_fix_token_request(
                context,
                token,
                "next_token",
                "extracted_whitespace",
                self.__fix_adjustments(token.extracted_whitespace),
            )
        else:
            self.report_next_token_error(context, token)

    def __handle_setext_heading(
        self, context: PluginScanContext, token: SetextHeadingMarkdownToken
    ) -> None:
        self.__setext_start_token = token
        self.__any_leading_whitespace_detected = bool(token.extracted_whitespace)
        if self.__any_leading_whitespace_detected and context.in_fix_mode:
            assert token.extracted_whitespace
            whitespace_to_add = " " if token.extracted_whitespace[0] == "\t" else ""
            self.register_fix_token_request(
                context,
                token,
                "next_token",
                "extracted_whitespace",
                whitespace_to_add,
            )
        self.__seen_first_line_of_setext = False
        self.__last_skipped_text_token = None

    def __handle_setext_heading_end(
        self, context: PluginScanContext, token: EndMarkdownToken
    ) -> None:
        if self.__last_skipped_text_token and context.in_fix_mode:
            self.__handle_text(context, self.__last_skipped_text_token, True)

        if token.extracted_whitespace:
            self.__any_leading_whitespace_detected = True
            if context.in_fix_mode:
                self.register_fix_token_request(
                    context,
                    token,
                    "next_token",
                    "extracted_whitespace",
                    self.__fix_adjustments(token.extracted_whitespace),
                )

        if self.__any_leading_whitespace_detected:
            assert self.__setext_start_token is not None
            self.report_next_token_error(
                context, self.__setext_start_token, use_original_position=True
            )
        self.__setext_start_token = None

    def __handle_text_split_end(
        self, next_split_end_whitespace: str, split_index: int, new_end_parts: List[str]
    ) -> None:
        split_next_split = next_split_end_whitespace.split(
            ParserHelper.whitespace_split_character
        )
        if len(split_next_split) == 2 and split_next_split[0]:
            self.__any_leading_whitespace_detected = True
            fix_string = self.__fix_adjustments(split_next_split[0], ind=split_index)
            new_split_value = (
                fix_string
                + ParserHelper.whitespace_split_character
                + split_next_split[1]
            )
            if new_split_value == ParserHelper.whitespace_split_character:
                new_end_parts.append("")
            else:
                new_end_parts.append(new_split_value)
        elif next_split_end_whitespace:
            new_end_parts.append(
                ParserHelper.whitespace_split_character + next_split_end_whitespace
            )
        else:
            new_end_parts.append(next_split_end_whitespace)

    # pylint: disable=too-many-arguments
    def __handle_text_split(
        self,
        context: PluginScanContext,
        split_text: List[str],
        split_end_whitespace: Optional[List[str]],
        split_index: int,
        new_text_parts: List[str],
        new_end_parts: List[str],
        is_setext_end: bool,
    ) -> None:
        next_split_end_whitespace = None
        if split_end_whitespace is not None:
            next_split_end_whitespace = split_end_whitespace[split_index]
        next_split_text = split_text[split_index]

        if context.in_fix_mode:
            if next_split_text and ParserHelper.is_character_replacement_marker(
                next_split_text, 0
            ):
                start_index, _, end_index = ParserHelper.get_replacement_indices(
                    next_split_text, 0
                )
                assert start_index == 0
                next_split_text = next_split_text[end_index + 1 :]

                ind = -1 if is_setext_end else 0
                self.__fix_adjustments("\t", ind=ind)
            new_text_parts.append(next_split_text)

        if self.__seen_first_line_of_setext and next_split_end_whitespace is not None:
            self.__handle_text_split_end(
                next_split_end_whitespace, split_index, new_end_parts
            )
        else:
            self.__seen_first_line_of_setext = True
            if next_split_end_whitespace is not None:
                new_end_parts.append(next_split_end_whitespace)

    # pylint: enable=too-many-arguments

    def __handle_text(
        self,
        context: PluginScanContext,
        token: TextMarkdownToken,
        is_setext_end: bool = False,
    ) -> None:
        if (
            not self.__setext_start_token
            or (self.__any_leading_whitespace_detected and not context.in_fix_mode)
            or (not token.end_whitespace and not is_setext_end)
        ):
            self.__last_skipped_text_token = token
            return

        self.__last_skipped_text_token = None
        assert context.in_fix_mode or not self.__any_leading_whitespace_detected

        split_text = token.token_text.split(ParserHelper.newline_character)
        split_end_whitespace = None
        if token.end_whitespace is not None:
            split_end_whitespace = token.end_whitespace.split(
                ParserHelper.newline_character
            )
            assert len(split_text) == len(split_end_whitespace)

        new_text_parts: List[str] = []
        new_end_parts: List[str] = []
        for split_index in range(len(split_text)):
            self.__handle_text_split(
                context,
                split_text,
                split_end_whitespace,
                split_index,
                new_text_parts,
                new_end_parts,
                is_setext_end,
            )

        if context.in_fix_mode:
            new_end_parts_combined = "\n".join(new_end_parts)
            if (
                token.end_whitespace is not None
                and new_end_parts_combined != token.end_whitespace
            ):
                self.register_fix_token_request(
                    context,
                    token,
                    "next_token",
                    "end_whitespace",
                    new_end_parts_combined,
                )

            new_text_parts_combined = "\n".join(new_text_parts)
            if new_text_parts_combined != token.token_text:
                self.register_fix_token_request(
                    context,
                    token,
                    "next_token",
                    "token_text",
                    new_text_parts_combined,
                )

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        self.__container_manager.premanage_container_tokens(token)

        if token.is_atx_heading:
            atx_token = cast(AtxHeadingMarkdownToken, token)
            self.__handle_atx_heading(context, atx_token)
        elif token.is_setext_heading:
            setext_token = cast(SetextHeadingMarkdownToken, token)
            self.__handle_setext_heading(context, setext_token)
        elif token.is_text:
            text_token = cast(TextMarkdownToken, token)
            self.__handle_text(context, text_token)
        elif token.is_setext_heading_end:
            end_token = cast(EndMarkdownToken, token)
            self.__handle_setext_heading_end(context, end_token)

        if token.is_list_end:
            end_token = cast(EndMarkdownToken, token)
            list_start_token = end_token.start_markdown_token
            if list_start_token in self.__leading_spaces_split and context.in_fix_mode:
                assert list_start_token.is_list_start
                list_token = cast(ListStartMarkdownToken, list_start_token)
                new_leading_spaces = self.__leading_spaces_split[list_token]
                self.register_fix_token_request(
                    context,
                    list_start_token,
                    "next_token",
                    "leading_spaces",
                    "\n".join(new_leading_spaces),
                )

        self.__container_manager.manage_container_tokens(token)
