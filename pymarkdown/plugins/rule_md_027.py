"""
Module to implement a plugin that looks for excessive spaces after the block quote character.
"""
from typing import Dict, List, Optional, cast

from pymarkdown.container_markdown_token import (
    BlockQuoteMarkdownToken,
    ListStartMarkdownToken,
)
from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.leaf_markdown_token import (
    BlankLineMarkdownToken,
    FencedCodeBlockMarkdownToken,
    LinkReferenceDefinitionMarkdownToken,
    ParagraphMarkdownToken,
    SetextHeadingMarkdownToken,
)
from pymarkdown.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


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
        self.__have_incremented_for_this_line = False
        self.__last_token: Optional[MarkdownToken] = None
        # self.__debug_on = False

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-multiple-space-blockquote",
            plugin_id="MD027",
            plugin_enabled_by_default=True,
            plugin_description="Multiple spaces after blockquote symbol",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md027.md",
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
        self.__have_incremented_for_this_line = False
        self.__last_token = None

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

    def __process_delayed_blank_line(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        allow_block_quote_end: bool,
    ) -> None:
        if (
            self.__delayed_blank_line
            and not (
                token.is_leaf_end_token
                or (allow_block_quote_end and token.is_block_quote_end)
            )
            and (not self.__have_incremented_for_this_line or token.is_blank_line)
        ):
            self.__have_incremented_for_this_line = False
            self.__handle_blank_line(
                context, self.__delayed_blank_line, num_container_tokens
            )
            self.__delayed_blank_line = None

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
            self.__handle_block_quote_start(token)
        elif token.is_block_quote_end:
            self.__handle_block_quote_end(context, token, num_container_tokens)
        elif token.is_list_start:
            self.__handle_list_start(context, token, num_container_tokens)
        elif token.is_list_end:
            self.__handle_list_end(num_container_tokens)
        elif token.is_new_list_item:
            self.__handle_new_list_item(context, token, num_container_tokens)
        elif num_container_tokens:
            self.__handle_within_block_quotes(context, token)

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

    def __handle_block_quote_end(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
    ) -> None:
        self.__process_delayed_paragraph_end(token, num_container_tokens)
        self.__process_delayed_blank_line(context, token, num_container_tokens, False)

        num_container_tokens = len(
            [i for i in self.__container_tokens if i.is_block_quote_start]
        )
        # if self.__debug_on:
        #     print(f"leading_spaces>{ParserHelper.make_value_visible(self.__container_tokens[-1].leading_spaces)}")
        block_quote_token = cast(BlockQuoteMarkdownToken, self.__container_tokens[-1])
        assert block_quote_token.bleading_spaces is not None
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
        if (
            self.__delayed_blank_line
            and newlines_in_container != self.__bq_line_index[num_container_tokens]
        ):
            self.__bq_line_index[num_container_tokens] += 1

        # assert newlines_in_container == self.__bq_line_index[num_container_tokens], (
        #     str(newlines_in_container)
        #     + " == "
        #     + str(self.__bq_line_index[num_container_tokens])
        # )
        del self.__bq_line_index[num_container_tokens]
        del self.__container_tokens[-1]

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
            is_start_properly_scoped = False
            if is_new_list_item:
                is_start_properly_scoped = (
                    found_block_quote_token == self.__container_tokens[-2]
                )
            else:
                is_start_properly_scoped = (
                    found_block_quote_token == self.__container_tokens[-1]
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
            if self.__last_token and self.__last_token.is_end_token:
                end_token = cast(EndMarkdownToken, self.__last_token)
                if end_token.start_markdown_token.is_block_quote_start:
                    block_quote_token = cast(
                        BlockQuoteMarkdownToken, end_token.start_markdown_token
                    )
                    # if self.__debug_on:
                    #     print(f"self.__last_token.start_markdown_token>:{ParserHelper.make_value_visible(\
                    #       self.__last_token.start_markdown_token)}:")
                    #     print("BOOM")
                    assert block_quote_token.bleading_spaces is not None
                    split_line_length = block_quote_token.bleading_spaces.split("\n")[
                        -1
                    ]
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
                self.report_next_token_error(
                    context, token, column_number_delta=column_number_delta
                )

    def __handle_list_start(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
    ) -> None:
        self.__process_delayed_blank_line(context, token, num_container_tokens, False)
        self.__process_delayed_paragraph_end(token, num_container_tokens)
        self.__check_list_starts(context, token, num_container_tokens, False)
        self.__container_tokens.append(token)

    def __handle_new_list_item(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
    ) -> None:
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

    def __handle_list_end(self, num_container_tokens: int) -> None:
        assert not (
            num_container_tokens
            and not self.__is_paragraph_end_delayed
            and not self.__have_incremented_for_this_line
        )
        del self.__container_tokens[-1]

    def __handle_blank_line(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
    ) -> None:
        # if self.__debug_on:
        #     print(f"__handle_blank_line>>{token}<<")
        blank_line_token = cast(BlankLineMarkdownToken, token)
        if blank_line_token.extracted_whitespace:
            # if self.__debug_on:
            #     print("blank-error")
            self.report_next_token_error(context, token)

        if self.__bq_line_index:
            self.__bq_line_index[num_container_tokens] += 1

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
            self.report_next_token_error(
                context, token, column_number_delta=column_number_delta
            )
        self.__bq_line_index[num_container_tokens] += 1
        self.__last_leaf_token = token

    def __handle_thematic_break(
        self,
        context: PluginScanContext,
        token: MarkdownToken,
        num_container_tokens: int,
        is_directly_within_block_quote: bool,
    ) -> None:
        self.__handle_common_element(
            context, token, num_container_tokens, is_directly_within_block_quote
        )

    def __handle_atx_heading(
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
            self.report_next_token_error(
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
            self.report_next_token_error(
                context, self.__last_leaf_token, column_number_delta=column_number_delta
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
    ) -> None:
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
            self.report_next_token_error(
                context,
                self.__last_leaf_token,
                line_number_delta=line_number_delta,
                column_number_delta=column_number_delta,
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
        self.report_next_token_error(
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
        self.report_next_token_error(
            context,
            token,
            line_number_delta=line_number_delta,
            column_number_delta=column_number_delta,
        )

    # pylint: enable=too-many-arguments

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
            self.report_next_token_error(
                context, token, column_number_delta=column_number_delta
            )

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
        if next_line:
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
            self.report_next_token_error(
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
                    self.report_next_token_error(
                        context,
                        scoped_block_quote_token,
                        line_number_delta=line_number_delta,
                        column_number_delta=-calculated_column_number,
                    )
        self.__bq_line_index[
            num_container_tokens
        ] += paragraph_token.extracted_whitespace.count(ParserHelper.newline_character)

    def __handle_within_block_quotes(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        # if self.__debug_on:
        #     print("__handle_within_block_quotes")
        num_container_tokens = len(
            [i for i in self.__container_tokens if i.is_block_quote_start]
        )
        # if self.__debug_on:
        #     print(f"{self.__bq_line_index}-->index>{num_container_tokens}")
        #     print(f"{self.__bq_line_index[num_container_tokens]}-->token>{ParserHelper.make_value_visible(token)}")

        self.__process_delayed_paragraph_end(token, num_container_tokens)
        self.__process_delayed_blank_line(context, token, num_container_tokens, True)
        is_directly_within_block_quote = self.__container_tokens[
            -1
        ].is_block_quote_start
        # if self.__debug_on:
        #     print(f"{self.__bq_line_index[num_container_tokens]}-->token>{ParserHelper.make_value_visible(token)}")

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
            # if self.__debug_on:
            #     print("[[Delaying blank line]]")
        elif token.is_atx_heading:
            self.__handle_atx_heading(
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
        elif token.is_thematic_break:
            self.__handle_thematic_break(
                context, token, num_container_tokens, is_directly_within_block_quote
            )
        elif token.is_link_reference_definition:
            self.__handle_link_reference_definition(
                context, token, num_container_tokens
            )
        else:
            self.__handle_within_block_quotes_blocks(
                token, context, num_container_tokens, is_directly_within_block_quote
            )
        # if self.__debug_on:
        #     print(f"{self.__bq_line_index[num_container_tokens]}<--token>{ParserHelper.make_value_visible(token)}")

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
