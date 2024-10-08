"""
Module to work with the rules to keep track of the current container "leading space" index.
"""

from dataclasses import dataclass
from typing import List, cast

from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.setext_heading_markdown_token import SetextHeadingMarkdownToken


@dataclass
class ClosedContainerAdjustments:
    """
    Keep track of line space used by already closed containers.
    """

    adjustment: int = 0
    count: int = 0
    count2: int = 0


class LeadingSpaceIndexTracker:
    """
    Class to track the leading spaces for each container.
    """

    def __init__(self) -> None:
        self.__closed_container_adjustments: List[ClosedContainerAdjustments] = []
        self.__container_token_stack: List[MarkdownToken] = []
        self.__end_tokens: List[EndMarkdownToken] = []
        self.__since_last_non_end_token: List[MarkdownToken] = []

    def clear(self) -> None:
        """
        Clear all tracking (at the beginning of a new file).
        """
        self.__closed_container_adjustments.clear()
        self.__container_token_stack.clear()
        self.__end_tokens.clear()

    def open_container(self, token: MarkdownToken) -> None:
        """
        Open a new container.
        """
        assert token.is_block_quote_start or token.is_list_start
        self.__container_token_stack.append(token)
        self.__closed_container_adjustments.append(ClosedContainerAdjustments())

    def register_container_end(self, token: MarkdownToken) -> None:
        """
        Register the end of the current container for processing once the
        next non-end token is encountered.
        """
        assert token.is_block_quote_end or token.is_list_end
        self.__end_tokens.append(cast(EndMarkdownToken, token))

    def have_any_registered_container_ends(self) -> bool:
        """
        Check to see if any container ends have been registered and not processed.
        """
        return bool(self.__end_tokens)

    def process_container_end(self, token: MarkdownToken) -> MarkdownToken:
        """
        Process a registered container end.
        """

        if self.__container_token_stack[-1].is_block_quote_start:
            self.__process_container_end_block_quote(token)
        else:
            self.__process_container_end_list(token)

        del self.__closed_container_adjustments[-1]
        del self.__end_tokens[-1]

        last_token_on_stack = self.__container_token_stack[-1]
        del self.__container_token_stack[-1]
        return last_token_on_stack

    def track_since_last_non_end_token(self, token: MarkdownToken) -> None:
        """
        Keep track of the last non-end token and any end tokens since then.
        """
        if not token.is_end_token:
            self.__since_last_non_end_token.clear()
        self.__since_last_non_end_token.append(token)

    def get_closed_container_info(self, index: int) -> ClosedContainerAdjustments:
        """
        Get the current information on all closed containers.
        """
        return self.__closed_container_adjustments[index]

    def in_at_least_one_container(self) -> bool:
        """
        Check to see if we are in at least one container.
        """
        return bool(self.__container_token_stack)

    def get_container_stack_size(self) -> int:
        """
        Get the number of containers that we are currently in.
        """
        return len(self.__container_token_stack)

    def get_container_stack_item(self, index: int) -> MarkdownToken:
        """
        Get a specific container from the stack.
        """
        return self.__container_token_stack[index]

    @staticmethod
    def calculate_token_line_number(token: MarkdownToken) -> int:
        """
        Since setext tokens are "weird", helper function to calculate the line number.
        """
        if token.is_setext_heading:
            setext_token = cast(SetextHeadingMarkdownToken, token)
            return setext_token.original_line_number
        return token.line_number

    def __process_container_end_block_quote(self, token: MarkdownToken) -> None:
        for stack_index in range(len(self.__container_token_stack) - 2, -1, -1):
            current_stack_token = self.__container_token_stack[stack_index]
            if current_stack_token.is_block_quote_start:
                line_number_delta = (
                    LeadingSpaceIndexTracker.calculate_token_line_number(token)
                    - self.__container_token_stack[-1].line_number
                )
                if self.__end_tokens[-1].extra_end_data is not None:
                    line_number_delta += 1
                self.__closed_container_adjustments[
                    stack_index
                ].adjustment += line_number_delta
                self.__closed_container_adjustments[stack_index].count += 1

                does_current_container_have_weird_kludge_six = (
                    self.__container_token_stack[-1].is_block_quote_start
                    and cast(
                        BlockQuoteMarkdownToken, self.__container_token_stack[-1]
                    ).weird_kludge_six
                )
                was_last_non_end_token_blank_line = (
                    self.__end_tokens
                    and self.__since_last_non_end_token
                    and self.__since_last_non_end_token[0].is_blank_line
                )

                if (
                    does_current_container_have_weird_kludge_six
                    and not was_last_non_end_token_blank_line
                ):
                    self.__closed_container_adjustments[stack_index].count2 += 1
                break

    def __process_container_end_list(self, token: MarkdownToken) -> None:
        for stack_index in range(len(self.__container_token_stack) - 2, -1, -1):
            current_stack_token = self.__container_token_stack[stack_index]
            if current_stack_token.is_list_start:
                line_number_delta = (
                    LeadingSpaceIndexTracker.calculate_token_line_number(token)
                    - self.__container_token_stack[-1].line_number
                )
                if (
                    self.__end_tokens[-1].start_markdown_token.line_number
                    == current_stack_token.line_number
                ):
                    line_number_delta -= 1
                self.__closed_container_adjustments[
                    stack_index
                ].adjustment += line_number_delta
                break

    def get_tokens_block_quote_bleading_space_index(self, token: MarkdownToken) -> int:
        """
        Get the index of the token within the contain block quote's bleading_spaces string.
        """
        container_index = self.get_container_stack_size() - 1
        assert self.__container_token_stack[container_index].is_block_quote_start
        block_quote_token = cast(
            BlockQuoteMarkdownToken, self.__container_token_stack[container_index]
        )
        last_closed_container_info = self.__closed_container_adjustments[-1]

        assert (
            block_quote_token.bleading_spaces is not None
        ), "At least one line should have been processed."
        return (
            LeadingSpaceIndexTracker.calculate_token_line_number(token)
            - block_quote_token.line_number
        ) - (last_closed_container_info.adjustment - last_closed_container_info.count2)
