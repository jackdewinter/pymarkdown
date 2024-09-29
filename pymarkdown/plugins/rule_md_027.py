"""
Module to implement a plugin that looks for excessive spaces after the block quote character.
"""

from typing import Dict, List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.plugins.utils.leading_space_index_tracker import (
    LeadingSpaceIndexTracker,
)
from pymarkdown.plugins.utils.list_tracker import ListTracker
from pymarkdown.tokens.blank_line_markdown_token import BlankLineMarkdownToken
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.fenced_code_block_markdown_token import (
    FencedCodeBlockMarkdownToken,
)
from pymarkdown.tokens.inline_code_span_markdown_token import (
    InlineCodeSpanMarkdownToken,
)
from pymarkdown.tokens.link_reference_definition_markdown_token import (
    LinkReferenceDefinitionMarkdownToken,
)
from pymarkdown.tokens.list_start_markdown_token import ListStartMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.new_list_item_markdown_token import NewListItemMarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.tokens.raw_html_markdown_token import RawHtmlMarkdownToken
from pymarkdown.tokens.setext_heading_markdown_token import SetextHeadingMarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


# pylint: disable=too-many-lines
# pylint: disable=too-many-instance-attributes
class RuleMd027(RulePlugin):
    """
    Class to implement a plugin that looks for excessive spaces after the block quote character.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__container_tokens: List[MarkdownToken] = []
        self.__bq_line_index: Dict[int, int] = {}
        self.__last_leaf_token: Optional[MarkdownToken] = None
        self.__line_index_at_bq_start: Optional[int] = None
        self.__is_paragraph_end_delayed = False
        self.__delayed_blank_line: Optional[MarkdownToken] = None
        self.__delayed_blank_line_bq_index: Optional[int] = None
        self.__delayed_blank_line_with_list_end = False
        self.__delayed_blank_line_container_token: Optional[MarkdownToken] = None
        self.__have_incremented_for_this_line = False
        self.__last_token: Optional[MarkdownToken] = None
        # self.__debug_on = False
        self.__list_tracker = ListTracker()
        self.__leading_space_index_tracker = LeadingSpaceIndexTracker()

        self.__delayed_bleading_fixes: Dict[
            MarkdownToken, List[Tuple[int, str, bool, BlankLineMarkdownToken]]
        ] = {}

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="no-multiple-space-blockquote",
            plugin_id="MD027",
            plugin_enabled_by_default=True,
            plugin_description="Multiple spaces after blockquote symbol",
            plugin_version="0.5.1",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md027.md",
            plugin_supports_fix=True,
            plugin_fix_level=5,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__container_tokens = []
        self.__bq_line_index = {}
        self.__last_leaf_token = None
        self.__line_index_at_bq_start = None
        self.__is_paragraph_end_delayed = False
        self.__delayed_blank_line = None
        self.__delayed_blank_line_bq_index = None
        self.__delayed_blank_line_container_token = None
        self.__delayed_blank_line_with_list_end = False
        self.__have_incremented_for_this_line = False
        self.__last_token = None
        self.__list_tracker.starting_new_file()
        self.__leading_space_index_tracker.clear()

    # pylint: disable=too-many-arguments
    def __report_issue(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        line_number_delta: int = 0,
        column_number_delta: int = 0,
        alternate_token: Optional[MarkdownToken] = None,
    ) -> bool:
        keep_going = True
        if context.in_fix_mode:
            if alternate_token:
                keep_going = self.__report_issue_alternate_token(
                    context, alternate_token
                )
            elif (
                self.__last_leaf_token
                and self.__last_leaf_token.is_setext_heading
                and token.is_text
            ):
                self.__report_issue_setext_text(context, token)
            elif (
                token.is_setext_heading
                or token.is_thematic_break
                or token.is_fenced_code_block
                or token.is_atx_heading
                or token.is_blank_line
            ):
                self.register_fix_token_request(
                    context, token, "next_token", "extracted_whitespace", ""
                )
            elif token.is_new_list_item:
                self.__report_issue_new_list_item(context, token)
            elif token.is_list_start:
                self.__report_issue_list_start(context, token)
            else:
                self.__report_issue_link_reference(context, token)
        else:
            self.report_next_token_error(
                context,
                token,
                line_number_delta=line_number_delta,
                column_number_delta=column_number_delta,
            )
        return keep_going

    # pylint: enable=too-many-arguments

    def __report_issue_alternate_token(
        self,
        context: PluginScanContext,
        alternate_token: MarkdownToken,
    ) -> bool:
        if alternate_token.is_paragraph:
            para_token = cast(ParagraphMarkdownToken, alternate_token)
            extracted_whitespace = "\n" * ParserHelper.count_newlines_in_text(
                para_token.extracted_whitespace
            )
            self.register_fix_token_request(
                context,
                alternate_token,
                "next_token",
                "extracted_whitespace",
                extracted_whitespace,
            )
            return False
        assert (
            alternate_token.is_setext_heading_end
            or alternate_token.is_fenced_code_block_end
        )
        self.register_fix_token_request(
            context, alternate_token, "next_token", "extracted_whitespace", ""
        )
        return True

    def __report_issue_setext_text(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        text_token = cast(TextMarkdownToken, token)
        whitespace_parts = []
        assert text_token.end_whitespace is not None
        for next_line in text_token.end_whitespace.split("\n"):
            split_character_index = next_line.find(
                ParserHelper.whitespace_split_character
            )
            if split_character_index == -1:
                whitespace_parts.append(next_line)
            else:
                whitespace_parts.append(next_line[split_character_index + 1 :])
        recombined_whitespace = "\n".join(whitespace_parts)
        assert recombined_whitespace != text_token.end_whitespace
        self.register_fix_token_request(
            context, token, "next_token", "end_whitespace", recombined_whitespace
        )

    def __report_issue_new_list_item(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        list_start_token = cast(NewListItemMarkdownToken, token)
        adjust_amount = len(list_start_token.extracted_whitespace)
        self.register_fix_token_request(
            context, token, "next_token", "extracted_whitespace", ""
        )
        self.register_fix_token_request(
            context,
            token,
            "next_token",
            "indent_level",
            list_start_token.indent_level - adjust_amount,
        )
        # self.register_fix_token_request(context, token, "next_token", "column_number", list_start_token.column_number - adjust_amount)
        self.__list_tracker.register(token, adjust_amount)

    def __report_issue_list_start(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        list_start_token = cast(ListStartMarkdownToken, token)
        adjust_amount = len(list_start_token.extracted_whitespace)
        self.register_fix_token_request(
            context, token, "next_token", "extracted_whitespace", ""
        )
        self.register_fix_token_request(
            context,
            token,
            "next_token",
            "indent_level",
            list_start_token.indent_level - adjust_amount,
        )
        self.register_fix_token_request(
            context,
            token,
            "next_token",
            "column_number",
            list_start_token.column_number - adjust_amount,
        )
        self.__list_tracker.register(token, adjust_amount)

    def __report_issue_link_reference(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        assert token.is_link_reference_definition
        lrd_token = cast(LinkReferenceDefinitionMarkdownToken, token)
        if lrd_token.extracted_whitespace:
            self.register_fix_token_request(
                context, token, "next_token", "extracted_whitespace", ""
            )
        assert lrd_token.link_destination_whitespace

        modified_whitespace = "\n" * ParserHelper.count_newlines_in_text(
            lrd_token.link_destination_whitespace
        )
        if modified_whitespace != lrd_token.link_destination_whitespace:
            self.register_fix_token_request(
                context,
                token,
                "next_token",
                "link_destination_whitespace",
                modified_whitespace,
            )

        if lrd_token.link_title_whitespace:
            modified_whitespace = "\n" * ParserHelper.count_newlines_in_text(
                lrd_token.link_title_whitespace
            )
            if modified_whitespace != lrd_token.link_title_whitespace:
                self.register_fix_token_request(
                    context,
                    token,
                    "next_token",
                    "link_title_whitespace",
                    modified_whitespace,
                )

    def __process_delayed_paragraph_end(
        self, token: MarkdownToken, num_container_tokens: int
    ) -> None:
        if self.__is_paragraph_end_delayed:
            # if self.__debug_on:
            #     print("[[Processing delayed paragraph end]]")
            #     print(f"delay-para-end-->token->{ParserHelper.make_value_visible(token)}")
            #     print(f"delay-para-end-->index->{self.__bq_line_index[num_container_tokens]}")

            assert (
                token.is_blank_line
                or token.is_fenced_code_block
                or token.is_thematic_break
                or token.is_html_block
                or token.is_list_start
                or token.is_atx_heading
                or token.is_block_quote_end
            )
            self.__bq_line_index[num_container_tokens] += 1
            self.__have_incremented_for_this_line = True
            # if self.__debug_on:
            #     print(f"delay-para-end-->index->{self.__bq_line_index[num_container_tokens]}")
            #     print("[[Delayed paragraph end processed]]")
            self.__is_paragraph_end_delayed = False

    # pylint: disable=too-many-arguments
    def __process_delayed_blank_line(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        allow_block_quote_end: bool,
        is_block_quote_end: bool,
    ) -> None:
        if (
            self.__delayed_blank_line
            and not (
                token.is_leaf_end_token
                or (allow_block_quote_end and token.is_block_quote_end)
            )
            and (
                not self.__have_incremented_for_this_line
                or token.is_blank_line
                or is_block_quote_end
            )
        ):
            self.__have_incremented_for_this_line = False
            assert self.__delayed_blank_line_bq_index is not None
            self.__handle_blank_line(
                context,
                self.__delayed_blank_line,
                num_container_tokens,
                self.__delayed_blank_line_bq_index,
            )
            self.__delayed_blank_line = None
            self.__delayed_blank_line_bq_index = None
            self.__delayed_blank_line_with_list_end = False
            self.__delayed_blank_line_container_token = None

    # pylint: enable=too-many-arguments

    def __process_pending_container_end_tokens(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        _ = context
        while self.__leading_space_index_tracker.have_any_registered_container_ends():
            self.__leading_space_index_tracker.process_container_end(token)

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        # if self.__debug_on:
        #     print(f">>{ParserHelper.make_value_visible(token)}")
        if (
            self.__have_incremented_for_this_line
            and not token.is_end_token
            and not token.is_blank_line
        ):
            self.__have_incremented_for_this_line = False

        if not token.is_end_token or token.is_end_of_stream:
            self.__process_pending_container_end_tokens(context, token)

        num_container_tokens = len(
            [i for i in self.__container_tokens if i.is_block_quote_start]
        )
        # if self.__debug_on:
        #     print(f"num->bqs:{num_container_tokens}, self.__have_incremented_for_this_line=" + \
        #       f"{self.__have_incremented_for_this_line}")
        #     if num_container_tokens in self.__bq_line_index:
        #         print(f"{self.__bq_line_index[num_container_tokens]}-->token>" + \
        #           f"{ParserHelper.make_value_visible(token)}")
        #     else:
        #         print(f"token>{ParserHelper.make_value_visible(token)}")
        #     if self.__container_tokens:
        #         print(f"self.__container_tokens>{ParserHelper.make_value_visible(self.__container_tokens)}")
        if token.is_block_quote_start:
            self.__leading_space_index_tracker.open_container(token)
            self.__handle_block_quote_start(token)
        elif token.is_block_quote_end:
            self.__leading_space_index_tracker.register_container_end(token)
            self.__handle_block_quote_end(context, token, num_container_tokens)
        elif token.is_list_start:
            self.__leading_space_index_tracker.open_container(token)
            self.__handle_list_start(context, token, num_container_tokens)
        elif token.is_list_end:
            self.__leading_space_index_tracker.register_container_end(token)
            self.__handle_list_end(context, token)
        elif token.is_new_list_item:
            self.__handle_new_list_item(context, token, num_container_tokens)
        else:
            self.__list_tracker.next_token(token)
            if num_container_tokens:
                self.__handle_within_block_quotes(context, token)

        self.__leading_space_index_tracker.track_since_last_non_end_token(token)

        self.__last_token = token

    def __handle_block_quote_start(self, token: MarkdownToken) -> None:
        self.__container_tokens.append(token)

        num_container_tokens = len(
            [i for i in self.__container_tokens if i.is_block_quote_start]
        )
        self.__bq_line_index[num_container_tokens] = 0
        self.__is_paragraph_end_delayed = False
        # if self.__debug_on:
        #     print(f"bq>{ParserHelper.make_value_visible(self.__container_tokens[-1])}")

    # pylint: disable=too-many-arguments
    def __register_blank_line(
        self,
        token: BlockQuoteMarkdownToken,
        index: int,
        mod: str,
        did_x: bool,
        blank_line_token: BlankLineMarkdownToken,
    ) -> None:
        if token in self.__delayed_bleading_fixes:
            delayed_list = self.__delayed_bleading_fixes[token]
        else:
            delayed_list = []
            self.__delayed_bleading_fixes[token] = delayed_list
        delayed_list.append((index, mod, did_x, blank_line_token))

    # pylint: enable=too-many-arguments

    def __handle_block_quote_end(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
    ) -> None:
        self.__process_delayed_paragraph_end(token, num_container_tokens)
        self.__process_delayed_blank_line(
            context, token, num_container_tokens, False, True
        )

        num_container_tokens = len(
            [i for i in self.__container_tokens if i.is_block_quote_start]
        )
        # if self.__debug_on:
        #     print(f"leading_spaces>{ParserHelper.make_value_visible(self.__container_tokens[-1].leading_spaces)}")
        block_quote_token = cast(BlockQuoteMarkdownToken, self.__container_tokens[-1])
        assert block_quote_token.bleading_spaces is not None

        if (
            self.__delayed_bleading_fixes
            and block_quote_token in self.__delayed_bleading_fixes
        ):
            split_leading_spaces = block_quote_token.bleading_spaces.split(
                ParserHelper.newline_character
            )
            delayed_list = self.__delayed_bleading_fixes[block_quote_token]
            for delayed_list_item in delayed_list:
                block_quote_index = delayed_list_item[0]
                modified_part = delayed_list_item[1]
                split_leading_spaces[block_quote_index] = modified_part

                did_trigger = delayed_list_item[2]
                if not did_trigger:
                    blank_token = delayed_list_item[3]
                    # assert False
                    self.report_next_token_error(
                        context,
                        blank_token,
                        column_number_delta=-(blank_token.column_number - 1),
                    )
            if context.in_fix_mode:
                self.register_fix_token_request(
                    context,
                    block_quote_token,
                    "next_token",
                    "bleading_spaces",
                    "\n".join(split_leading_spaces),
                )
            del self.__delayed_bleading_fixes[block_quote_token]

        newlines_in_container = block_quote_token.bleading_spaces.count(
            ParserHelper.newline_character
        )
        if (
            not (
                block_quote_token.bleading_spaces
                and block_quote_token.bleading_spaces.endswith(
                    ParserHelper.newline_character
                )
            )
            and self.__container_tokens
            and block_quote_token.bleading_spaces
        ):
            # if self.__debug_on:
            #     print(f"newlines_in_container>{newlines_in_container}")
            newlines_in_container += 1

        # if self.__debug_on:
        #     print(f"newlines_in_container>{newlines_in_container}")
        #     print(f"__bq_line_index>{self.__bq_line_index[num_container_tokens]}")
        #     print(f"__is_paragraph_end_delayed>{self.__is_paragraph_end_delayed}")
        #     print(f"__delayed_blank_line>{self.__delayed_blank_line}")
        # if (
        #     self.__delayed_blank_line
        #     and newlines_in_container != self.__bq_line_index[num_container_tokens]
        # ):
        #     self.__bq_line_index[num_container_tokens] += 1

        # assert newlines_in_container == self.__bq_line_index[num_container_tokens], (
        #     str(newlines_in_container)
        #     + " == "
        #     + str(self.__bq_line_index[num_container_tokens])
        # )
        del self.__bq_line_index[num_container_tokens]
        del self.__container_tokens[-1]
        end_token = cast(EndMarkdownToken, token)
        if end_token.extra_end_data and num_container_tokens > 1:
            self.__bq_line_index[num_container_tokens - 1] -= 1

    def __get_last_block_quote(self) -> Optional[MarkdownToken]:
        return next(
            (
                self.__container_tokens[i]
                for i in range(len(self.__container_tokens) - 1, -1, -1)
                if self.__container_tokens[i].is_block_quote_start
            ),
            None,
        )

    def __check_list_starts(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        is_new_list_item: bool,
    ) -> None:
        # if self.__debug_on:
        #     print(f"num_container_tokens={num_container_tokens};")
        #     print(f"container_tokens={ParserHelper.make_value_visible(self.__container_tokens)};")
        _ = num_container_tokens
        if found_block_quote_token := self.__get_last_block_quote():
            # is_start_properly_scoped = False
            is_start_properly_scoped = (
                (found_block_quote_token == self.__container_tokens[-2])
                if is_new_list_item
                else (found_block_quote_token == self.__container_tokens[-1])
            )
            # if self.__debug_on:
            #     print(
            #         f"is_start_properly_scoped={is_start_properly_scoped};"
            #         + f"found_block_quote_token={ParserHelper.make_value_visible(found_block_quote_token)}"
            #     )
            #     print(f"token.extracted_whitespace>:{token.extracted_whitespace}:")
            #     print(f"self.__last_token>:{ParserHelper.make_value_visible(self.__last_token)}:")

            # In rare cases, a block quote is ended in the middle of a line.
            # This is one of those cases.
            list_token = cast(ListStartMarkdownToken, token)
            whitespace_to_use = list_token.extracted_whitespace
            if (
                self.__last_token
                and self.__last_token.is_end_token
                and self.__last_token.is_block_quote_end
            ):
                end_token = cast(EndMarkdownToken, self.__last_token)
                block_quote_token = cast(
                    BlockQuoteMarkdownToken, end_token.start_markdown_token
                )
                # if self.__debug_on:
                #     print(f"self.__last_token.start_markdown_token>:{ParserHelper.make_value_visible(\
                #       self.__last_token.start_markdown_token)}:")
                #     print("BOOM")
                assert block_quote_token.bleading_spaces is not None
                split_line_length = block_quote_token.bleading_spaces.split("\n")[-1]
                # if self.__debug_on:
                #     print(f"BOOM:{split_line_length}:")
                whitespace_to_use = whitespace_to_use[len(split_line_length) :]

            if is_start_properly_scoped and whitespace_to_use:
                column_number_delta = -(token.column_number - len(whitespace_to_use))
                # if self.__debug_on:
                #     print("list-error")
                #     line_index = (
                #         self.__bq_line_index[num_container_tokens] + 0
                #     )
                #     print(f"5>{line_index}")
                #     print(f"column-delta>{column_number_delta}")
                self.__report_issue(
                    context, token, column_number_delta=column_number_delta
                )

    def __handle_list_start(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
    ) -> None:
        self.__list_tracker.list_start(token)

        self.__process_delayed_blank_line(
            context, token, num_container_tokens, False, False
        )
        self.__process_delayed_paragraph_end(token, num_container_tokens)
        self.__check_list_starts(context, token, num_container_tokens, False)
        self.__container_tokens.append(token)

    def __handle_new_list_item(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
    ) -> None:
        self.__list_tracker.new_list_item(token)
        # if self.__debug_on:
        #     print(
        #         f"num_container_tokens={num_container_tokens}, __is_paragraph_end_delayed="
        #         + f"{self.__is_paragraph_end_delayed}, self.__have_incremented_for_this_line="
        #         + f"{self.__have_incremented_for_this_line}"
        #     )
        if (
            num_container_tokens
            and not self.__have_incremented_for_this_line
            and self.__is_paragraph_end_delayed
        ):
            self.__bq_line_index[num_container_tokens] += 1
            self.__is_paragraph_end_delayed = False
        self.__check_list_starts(context, token, num_container_tokens, True)

    def __handle_list_end(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        self.__list_tracker.list_end()
        if self.__delayed_blank_line:
            self.__delayed_blank_line_with_list_end = True

        if registration_map := self.__list_tracker.get_registrations():
            end_token = cast(EndMarkdownToken, token)
            list_token = cast(ListStartMarkdownToken, end_token.start_markdown_token)
            if list_token.leading_spaces:
                split_leading_spaces = list_token.leading_spaces.split("\n")
                for registered_token, adj in registration_map.items():
                    start, stop = self.__list_tracker.get_start_stop(registered_token)
                    for next_index in range(start, stop):
                        assert adj > 0
                        split_leading_spaces[next_index] = split_leading_spaces[
                            next_index
                        ][:-adj]
                        # else:
                        #     split_leading_spaces[next_index] = split_leading_spaces[next_index] + (" " * -adj)
                rebuilt_leading_spaces = "\n".join(split_leading_spaces)
                if rebuilt_leading_spaces != list_token.leading_spaces:
                    self.register_fix_token_request(
                        context,
                        list_token,
                        "next_token",
                        "leading_spaces",
                        rebuilt_leading_spaces,
                    )

        self.__list_tracker.list_end_cleanup()
        del self.__container_tokens[-1]

    def __handle_blank_line(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        delayed_bq_index: int,
    ) -> None:
        # if self.__debug_on:
        #     print(f"__handle_blank_line>>{token}<<")
        blank_line_token = cast(BlankLineMarkdownToken, token)

        assert self.__delayed_blank_line_container_token is not None
        scoped_token = self.__delayed_blank_line_container_token
        if scoped_token is not None and scoped_token.is_block_quote_start:

            self.__handle_blank_line_inner(
                scoped_token, delayed_bq_index, blank_line_token, token
            )

        if blank_line_token.extracted_whitespace:
            # if self.__debug_on:
            #     print("blank-error")

            self.__report_issue(context, token)

        assert self.__bq_line_index
        self.__bq_line_index[num_container_tokens] += 1

    def __handle_blank_line_inner(
        self,
        scoped_token: MarkdownToken,
        delayed_bq_index: int,
        blank_line_token: BlankLineMarkdownToken,
        token: MarkdownToken,
    ) -> None:
        scoped_block_quote_token = cast(BlockQuoteMarkdownToken, scoped_token)
        assert scoped_block_quote_token.bleading_spaces is not None
        split_leading_spaces = scoped_block_quote_token.bleading_spaces.split(
            ParserHelper.newline_character
        )

        container_index = (
            self.__leading_space_index_tracker.get_container_stack_size() - 1
        )
        if self.__leading_space_index_tracker.get_container_stack_item(
            container_index
        ).is_block_quote_start:
            block_quote_index = self.__leading_space_index_tracker.get_tokens_block_quote_bleading_space_index(
                token
            )
        else:
            block_quote_index = delayed_bq_index

        # If we are closing other containers, can cause issues. So do not fire.
        is_end_with_other_closed_containers = (
            block_quote_index == len(split_leading_spaces) - 1
            and self.__delayed_blank_line_with_list_end
        )

        # If we have matching nested block quotes, and then a blank line, we need to prevent
        # the firing.
        is_special_case = (
            block_quote_index == 0
            and len(split_leading_spaces) == 1
            and blank_line_token.line_number != scoped_block_quote_token.line_number
        )

        assert (
            not is_special_case
            and not is_end_with_other_closed_containers
            and block_quote_index < len(split_leading_spaces)
        )

        specific_block_quote_prefix = split_leading_spaces[block_quote_index]
        mod_specific_block_quote_prefix = specific_block_quote_prefix.rstrip(" ")
        if mod_specific_block_quote_prefix != specific_block_quote_prefix:
            self.__register_blank_line(
                scoped_block_quote_token,
                block_quote_index,
                mod_specific_block_quote_prefix,
                bool(blank_line_token.extracted_whitespace),
                blank_line_token,
            )

    def __handle_common_element(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        is_directly_within_block_quote: bool,
    ) -> None:
        common_token = cast(BlankLineMarkdownToken, token)
        if common_token.extracted_whitespace and is_directly_within_block_quote:
            column_number_delta = -(
                token.column_number - len(common_token.extracted_whitespace)
            )
            self.__report_issue(context, token, column_number_delta=column_number_delta)
        self.__bq_line_index[num_container_tokens] += 1
        self.__last_leaf_token = token

    def __handle_atx_heading_or_thematic_break(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        is_directly_within_block_quote: bool,
    ) -> None:
        self.__handle_common_element(
            context, token, num_container_tokens, is_directly_within_block_quote
        )

    def __handle_setext_heading(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        is_directly_within_block_quote: bool,
    ) -> None:
        setext_token = cast(SetextHeadingMarkdownToken, token)
        if setext_token.extracted_whitespace and is_directly_within_block_quote:
            line_number_delta = setext_token.original_line_number - token.line_number
            column_number_delta = -(
                setext_token.original_column_number
                - len(setext_token.extracted_whitespace)
            )
            # if self.__debug_on:
            #     print("setext-error")
            #     print(f"line->{token.original_line_number},col={token.original_column_number}")
            #     print(f"delta->line->{line_number_delta},col={column_number_delta}")
            self.__report_issue(
                context,
                token,
                line_number_delta=line_number_delta,
                column_number_delta=column_number_delta,
            )
        self.__last_leaf_token = token

    def __handle_setext_heading_end(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        is_directly_within_block_quote: bool,
    ) -> None:
        end_token = cast(EndMarkdownToken, token)
        if end_token.extracted_whitespace and is_directly_within_block_quote:
            # if self.__debug_on:
            #     print("setext_heading_end-error")
            assert self.__last_leaf_token is not None
            column_number_delta = -(
                self.__last_leaf_token.column_number
                - len(end_token.extracted_whitespace)
            )
            assert self.__last_leaf_token is not None
            self.__report_issue(
                context,
                self.__last_leaf_token,
                column_number_delta=column_number_delta,
                alternate_token=token,
            )
        self.__bq_line_index[num_container_tokens] += 1
        self.__last_leaf_token = None

    def __handle_fenced_code_block(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        is_directly_within_block_quote: bool,
    ) -> None:
        self.__handle_common_element(
            context, token, num_container_tokens, is_directly_within_block_quote
        )
        self.__line_index_at_bq_start = self.__bq_line_index[num_container_tokens]

    def __handle_fenced_code_block_end(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        is_directly_within_block_quote: bool,
    ) -> None:  # sourcery skip: extract-method
        fenced_token = cast(FencedCodeBlockMarkdownToken, token)
        if fenced_token.extracted_whitespace and is_directly_within_block_quote:
            scoped_block_quote_token = cast(
                BlockQuoteMarkdownToken, self.__container_tokens[-1]
            )
            assert scoped_block_quote_token.bleading_spaces is not None
            split_leading_spaces = scoped_block_quote_token.bleading_spaces.split(
                ParserHelper.newline_character
            )
            specific_block_quote_prefix = split_leading_spaces[
                self.__bq_line_index[num_container_tokens]
            ]

            assert self.__line_index_at_bq_start is not None
            line_number_delta = 1 + (
                self.__bq_line_index[num_container_tokens]
                - self.__line_index_at_bq_start
            )
            column_number_delta = -(len(specific_block_quote_prefix) + 1)

            # if self.__debug_on:
            #     print(f"end-container>>{ParserHelper.make_value_visible(self.__container_tokens[-1])}")
            #     print(f"split_leading_spaces>>{ParserHelper.make_value_visible(split_leading_spaces)}")
            #     print("specific_block_quote_prefix>>:" + \
            #       f"{ParserHelper.make_value_visible(specific_block_quote_prefix)}:")
            #     print("fenced-end-error")
            assert self.__last_leaf_token is not None
            self.__report_issue(
                context,
                self.__last_leaf_token,
                line_number_delta=line_number_delta,
                column_number_delta=column_number_delta,
                alternate_token=token,
            )
        self.__last_leaf_token = None
        self.__bq_line_index[num_container_tokens] += 1

    # pylint: disable=too-many-arguments
    def __report_lrd_error(
        self,
        lrd_token: LinkReferenceDefinitionMarkdownToken,
        num_container_tokens: int,
        context: PluginScanContext,
        token: MarkdownToken,
        scoped_block_quote_token: BlockQuoteMarkdownToken,
    ) -> None:
        assert lrd_token.link_name_debug is not None
        assert scoped_block_quote_token.bleading_spaces is not None
        line_number_delta = (
            lrd_token.link_name_debug.count(ParserHelper.newline_character) + 1
        )

        split_array_index = (
            self.__bq_line_index[num_container_tokens] + line_number_delta
        )
        split_leading_spaces = scoped_block_quote_token.bleading_spaces.split(
            ParserHelper.newline_character
        )
        specific_block_quote_prefix = split_leading_spaces[split_array_index]

        column_number_delta = -(len(specific_block_quote_prefix) + 1)

        # if self.__debug_on:
        #     print(f"line_number_delta>>{line_number_delta}")
        #     print(f"split_array_index>>{split_array_index}")
        #     print(f"end-container>>{ParserHelper.make_value_visible(self.__container_tokens[-1])}")
        #     print(f"split_leading_spaces>>{ParserHelper.make_value_visible(split_leading_spaces)}")
        #     print("specific_block_quote_prefix>>:" + \
        #       f"{ParserHelper.make_value_visible(specific_block_quote_prefix)}:")
        #     print("lrd-2-error")
        self.__report_issue(
            context,
            token,
            line_number_delta=line_number_delta,
            column_number_delta=column_number_delta,
        )

    # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def __handle_link_reference_definition_check_after(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        lrd_token: LinkReferenceDefinitionMarkdownToken,
        leading_spaces: str,
    ) -> None:
        assert lrd_token.link_name_debug is not None
        assert lrd_token.link_title_whitespace is not None
        line_number_delta = (
            lrd_token.link_name_debug.count(ParserHelper.newline_character)
            + lrd_token.link_title_whitespace.count(ParserHelper.newline_character)
            + 1
        )

        split_array_index = (
            self.__bq_line_index[num_container_tokens] + line_number_delta
        )
        split_leading_spaces = leading_spaces.split(ParserHelper.newline_character)
        specific_block_quote_prefix = split_leading_spaces[split_array_index]

        column_number_delta = -(len(specific_block_quote_prefix) + 1)
        # if self.__debug_on:
        #     print("line_number_delta>>" + str(line_number_delta))
        #     print("split_array_index>>" + str(split_array_index))
        #     print(f"end-container>>{ParserHelper.make_value_visible(self.__container_tokens[-1])}")
        #     print(f"split_leading_spaces>>{ParserHelper.make_value_visible(split_leading_spaces)}")
        #     print("specific_block_quote_prefix>>:" + \
        #       f"{ParserHelper.make_value_visible(specific_block_quote_prefix)}:")
        #     print("lrd-3-error")
        self.__report_issue(
            context,
            token,
            line_number_delta=line_number_delta,
            column_number_delta=column_number_delta,
        )

    # pylint: enable=too-many-arguments

    def __handle_code_span(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        code_span_token = cast(InlineCodeSpanMarkdownToken, token)

        start_index = 0
        next_index = code_span_token.span_text.find("\x07\n\x07", start_index)
        recombine_list: List[str] = []
        while next_index != -1:
            recombine_list.extend(
                (code_span_token.span_text[start_index:next_index], "\n")
            )
            after_space_index, _ = ParserHelper.collect_while_spaces_verified(
                code_span_token.span_text, next_index + 3
            )
            is_there = ParserHelper.is_character_at_index(
                code_span_token.span_text, after_space_index, "\x07"
            )
            assert is_there
            start_index = after_space_index + 1
            next_index = code_span_token.span_text.find("\x07\n\x07", start_index)
        recombine_list.append(code_span_token.span_text[start_index:])
        recombined_span_text = "".join(recombine_list)
        if recombined_span_text != code_span_token.span_text:
            self.register_fix_token_request(
                context, token, "next_token", "span_text", recombined_span_text
            )

    def __handle_raw_html(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        raw_html_token = cast(RawHtmlMarkdownToken, token)
        recombine_list = []
        for next_tag_line in raw_html_token.raw_tag.split("\n"):
            if next_tag_line.startswith("\a"):
                after_space_index, _ = ParserHelper.collect_while_spaces_verified(
                    next_tag_line, 1
                )
                remaining_line = next_tag_line[after_space_index:]
                assert remaining_line.startswith("\a\x03\a")
                remaining_line = remaining_line[3:]
                recombine_list.append(remaining_line)
            else:
                recombine_list.append(next_tag_line)
        recombined_raw_tag = "\n".join(recombine_list)
        if recombined_raw_tag != raw_html_token.raw_tag:
            self.register_fix_token_request(
                context, token, "next_token", "raw_tag", recombined_raw_tag
            )

    def __handle_link_reference_definition(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
    ) -> None:
        scoped_block_quote_token = cast(
            BlockQuoteMarkdownToken, self.__container_tokens[-1]
        )
        if scoped_block_quote_token.is_block_quote_start:
            assert scoped_block_quote_token.bleading_spaces is not None
            leading_spaces = scoped_block_quote_token.bleading_spaces
        else:
            scoped_list_token = cast(
                ListStartMarkdownToken, self.__container_tokens[-1]
            )
            assert scoped_list_token.leading_spaces is not None
            leading_spaces = scoped_list_token.leading_spaces
        lrd_token = cast(LinkReferenceDefinitionMarkdownToken, token)
        if lrd_token.extracted_whitespace:
            column_number_delta = -(
                lrd_token.column_number - len(lrd_token.extracted_whitespace)
            )
            # if self.__debug_on:
            #     print("lrd-1-error")
            self.__report_issue(context, token, column_number_delta=column_number_delta)

        assert lrd_token.link_destination_whitespace is not None
        found_index = lrd_token.link_destination_whitespace.find(
            ParserHelper.newline_character
        )
        if found_index != -1 and ParserHelper.is_character_at_index_whitespace(
            lrd_token.link_destination_whitespace, found_index + 1
        ):
            self.__report_lrd_error(
                lrd_token,
                num_container_tokens,
                context,
                token,
                scoped_block_quote_token,
            )

        assert lrd_token.link_title_whitespace is not None
        found_index = lrd_token.link_title_whitespace.find(
            ParserHelper.newline_character
        )
        if found_index != -1 and ParserHelper.is_character_at_index_whitespace(
            lrd_token.link_title_whitespace, found_index + 1
        ):
            self.__handle_link_reference_definition_check_after(
                context, token, num_container_tokens, lrd_token, leading_spaces
            )

        assert lrd_token.link_name_debug is not None
        assert lrd_token.link_title_raw is not None
        self.__bq_line_index[num_container_tokens] += (
            1
            + lrd_token.link_name_debug.count(ParserHelper.newline_character)
            + lrd_token.link_destination_whitespace.count(
                ParserHelper.newline_character
            )
            + lrd_token.link_title_whitespace.count(ParserHelper.newline_character)
            + lrd_token.link_title_raw.count(ParserHelper.newline_character)
        )

    # pylint: disable=too-many-arguments
    def __scan_text(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        next_line: str,
        scoped_block_quote_token: BlockQuoteMarkdownToken,
        num_container_tokens: int,
        line_number_delta: int,
    ) -> None:
        found_index = next_line.find(ParserHelper.whitespace_split_character)
        if found_index != -1:
            next_line = next_line[:found_index]
        if next_line and found_index != -1:
            assert scoped_block_quote_token.bleading_spaces is not None
            split_leading_spaces = scoped_block_quote_token.bleading_spaces.split(
                ParserHelper.newline_character
            )
            split_array_index = (
                self.__bq_line_index[num_container_tokens] + line_number_delta + 1
            )
            specific_block_quote_prefix = split_leading_spaces[split_array_index]
            calculated_column_number = -(len(specific_block_quote_prefix) + 1)

            # if self.__debug_on:
            #     print(f"split_leading_spaces>>{ParserHelper.make_value_visible(split_leading_spaces)}")
            #     print(f"split_array_index>>{ParserHelper.make_value_visible(split_array_index)}")
            #     print("specific_block_quote_prefix>>:" + \
            #       f"{ParserHelper.make_value_visible(specific_block_quote_prefix)}:")
            #     print("setext-text-error")
            self.__report_issue(
                context,
                token,
                line_number_delta=line_number_delta,
                column_number_delta=calculated_column_number,
            )

    # pylint: enable=too-many-arguments

    def __handle_text(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        is_directly_within_block_quote: bool,
    ) -> None:
        assert self.__last_leaf_token is not None
        text_token = cast(TextMarkdownToken, token)
        if self.__last_leaf_token.is_setext_heading:
            if is_directly_within_block_quote:
                scoped_block_quote_token = cast(
                    BlockQuoteMarkdownToken, self.__container_tokens[-1]
                )
                assert scoped_block_quote_token.bleading_spaces is not None
                assert text_token.end_whitespace is not None

                for line_number_delta, next_line in enumerate(
                    text_token.end_whitespace.split(ParserHelper.newline_character)
                ):
                    self.__scan_text(
                        context,
                        token,
                        next_line,
                        scoped_block_quote_token,
                        num_container_tokens,
                        line_number_delta,
                    )
            assert text_token.end_whitespace is not None
            self.__bq_line_index[num_container_tokens] += (
                text_token.end_whitespace.count(ParserHelper.newline_character) + 1
            )
        elif (
            self.__last_leaf_token.is_html_block or self.__last_leaf_token.is_code_block
        ):
            self.__bq_line_index[num_container_tokens] += (
                text_token.token_text.count(ParserHelper.newline_character) + 1
            )

    def __handle_paragraph(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        is_directly_within_block_quote: bool,
    ) -> None:
        paragraph_token = cast(ParagraphMarkdownToken, token)
        self.__last_leaf_token = paragraph_token
        if is_directly_within_block_quote:
            scoped_block_quote_token = cast(
                BlockQuoteMarkdownToken, self.__container_tokens[-1]
            )
            # if self.__debug_on:
            #     print(f"para>>>{scoped_block_quote_token}")

            for line_number_delta, next_line in enumerate(
                paragraph_token.extracted_whitespace.split(
                    ParserHelper.newline_character
                )
            ):
                if next_line and scoped_block_quote_token.bleading_spaces:
                    # if self.__debug_on:
                    #     print(f"1>{self.__bq_line_index[num_container_tokens]}")
                    #     print(f"2>{line_number_delta}")
                    #     print(f"3>{ParserHelper.make_value_visible(scoped_block_quote_token)}")
                    split_leading_spaces = (
                        scoped_block_quote_token.bleading_spaces.split(
                            ParserHelper.newline_character
                        )
                    )
                    line_index = (
                        self.__bq_line_index[num_container_tokens] + line_number_delta
                    )
                    calculated_column_number = len(split_leading_spaces[line_index]) + 1
                    # if self.__debug_on:
                    #     print(f"4>{split_leading_spaces}")
                    #     print(f"5>{line_index}")
                    #     print(f"column>{calculated_column_number}")
                    #     print("para-error")
                    keep_going = self.__report_issue(
                        context,
                        scoped_block_quote_token,
                        line_number_delta=line_number_delta,
                        column_number_delta=-calculated_column_number,
                        alternate_token=paragraph_token,
                    )
                    if not keep_going:
                        break
        self.__bq_line_index[
            num_container_tokens
        ] += paragraph_token.extracted_whitespace.count(ParserHelper.newline_character)

    def __handle_within_block_quotes_prefix(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> Tuple[int, bool]:
        # if self.__debug_on:
        #     print("__handle_within_block_quotes")
        num_container_tokens = len(
            [i for i in self.__container_tokens if i.is_block_quote_start]
        )
        # if self.__debug_on:
        #     print(f"{self.__bq_line_index}-->index>{num_container_tokens}")
        #     print(f"{self.__bq_line_index[num_container_tokens]}-->token>{ParserHelper.make_value_visible(token)}")

        self.__process_delayed_paragraph_end(token, num_container_tokens)
        self.__process_delayed_blank_line(
            context, token, num_container_tokens, True, False
        )
        is_directly_within_block_quote = self.__container_tokens[
            -1
        ].is_block_quote_start
        # if self.__debug_on:
        #     print(f"{self.__bq_line_index[num_container_tokens]}-->token>{ParserHelper.make_value_visible(token)}")
        return num_container_tokens, is_directly_within_block_quote

    def __handle_within_block_quotes(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        (
            num_container_tokens,
            is_directly_within_block_quote,
        ) = self.__handle_within_block_quotes_prefix(context, token)

        if token.is_paragraph:
            self.__handle_paragraph(
                context, token, num_container_tokens, is_directly_within_block_quote
            )
        elif token.is_text:
            self.__handle_text(
                context, token, num_container_tokens, is_directly_within_block_quote
            )
        elif token.is_paragraph_end:
            self.__last_leaf_token = None
            self.__is_paragraph_end_delayed = True
            # if self.__debug_on:
            #     print("[[Delaying paragraph end]]")
        elif token.is_blank_line:
            self.__delayed_blank_line = token
            self.__delayed_blank_line_bq_index = self.__bq_line_index[
                num_container_tokens
            ]
            self.__delayed_blank_line_with_list_end = False
            self.__delayed_blank_line_container_token = self.__container_tokens[-1]
            # if self.__debug_on:
            #     print("[[Delaying blank line]]")
        elif token.is_atx_heading or token.is_thematic_break:
            self.__handle_atx_heading_or_thematic_break(
                context, token, num_container_tokens, is_directly_within_block_quote
            )
        elif token.is_setext_heading:
            self.__handle_setext_heading(context, token, is_directly_within_block_quote)
        elif token.is_setext_heading_end:
            self.__handle_setext_heading_end(
                context, token, num_container_tokens, is_directly_within_block_quote
            )
        elif token.is_atx_heading_end:
            self.__last_leaf_token = None
        elif token.is_link_reference_definition:
            self.__handle_link_reference_definition(
                context, token, num_container_tokens
            )
        else:
            self.__handle_within_block_quotes_remaining(
                context, token, num_container_tokens, is_directly_within_block_quote
            )
        # if self.__debug_on:
        #     print(f"{self.__bq_line_index[num_container_tokens]}<--token>{ParserHelper.make_value_visible(token)}")

    def __handle_within_block_quotes_remaining(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        is_directly_within_block_quote: bool,
    ) -> None:
        if token.is_inline_raw_html and context.in_fix_mode:
            self.__handle_raw_html(context, token)
        elif token.is_inline_code_span and context.in_fix_mode:
            self.__handle_code_span(context, token)
        else:
            self.__handle_within_block_quotes_blocks(
                token, context, num_container_tokens, is_directly_within_block_quote
            )

    def __handle_within_block_quotes_blocks(
        self,
        token: MarkdownToken,
        context: PluginScanContext,
        num_container_tokens: int,
        is_directly_within_block_quote: bool,
    ) -> None:
        if token.is_fenced_code_block:
            self.__handle_fenced_code_block(
                context, token, num_container_tokens, is_directly_within_block_quote
            )
        elif token.is_fenced_code_block_end:
            self.__handle_fenced_code_block_end(
                context, token, num_container_tokens, is_directly_within_block_quote
            )
        elif token.is_html_block or token.is_indented_code_block:
            self.__last_leaf_token = token
        elif token.is_html_block_end or token.is_indented_code_block_end:
            self.__last_leaf_token = None


# pylint: enable=too-many-instance-attributes
