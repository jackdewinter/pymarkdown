"""
Module to implement a plugin that looks for spaces within emphasis sections.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetailsV2
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


@dataclass
class EligibleEmphasis:
    """
    Emphasis characters that are eligible for actual emphasis.
    """

    emphasis_character: str
    start_index: int
    found_length: int
    character_before: Optional[str] = None
    character_after: Optional[str] = None
    text_token: Optional[TextMarkdownToken] = None


@dataclass
class PendingFixes:
    """
    Fixes that are pending being applied to the token.
    """

    token_to_modify: TextMarkdownToken
    start_index: int
    end_index: int


class RuleMd037(RulePlugin):
    """
    Class to implement a plugin that looks for spaces within emphasis sections.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__pending_fixes: List[PendingFixes] = []
        self.__block_token: Optional[MarkdownToken] = None
        self.__past_emphasis_list: List[EligibleEmphasis] = []

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV2(
            plugin_name="no-space-in-emphasis",
            plugin_id="MD037",
            plugin_enabled_by_default=True,
            plugin_description="Spaces inside emphasis markers",
            plugin_version="0.5.1",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md037.md",
            plugin_supports_fix=True,
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__block_token = None
        self.__past_emphasis_list = []

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_paragraph or token.is_setext_heading or token.is_atx_heading:
            self.__block_token = token
            self.__past_emphasis_list = []
        elif (
            token.is_paragraph_end
            or token.is_setext_heading_end
            or token.is_atx_heading_end
        ):
            self.__block_token = None
            self.__past_emphasis_list = []
            if self.__pending_fixes:
                self.__process_fixes(context)
        elif (
            token.is_text
            and self.__block_token is not None
            and (
                self.__block_token.is_paragraph
                or self.__block_token.is_setext_heading
                or self.__block_token.is_atx_heading
            )
        ):
            text_token = cast(TextMarkdownToken, token)
            self.__check_text_token(context, text_token)

    def __check_text_token(
        self, context: PluginScanContext, text_token: TextMarkdownToken
    ) -> None:
        start_index = 0
        next_index: Optional[int] = -1
        while next_index is not None:
            new_emphasis, next_index = self.__find_next_eligible_emphasis(
                text_token, start_index
            )
            if new_emphasis is not None:
                if (
                    self.__past_emphasis_list
                    and self.__past_emphasis_list[-1].emphasis_character
                    == new_emphasis.emphasis_character
                    and self.__past_emphasis_list[-1].found_length
                    == new_emphasis.found_length
                ):
                    self.__check(context, self.__past_emphasis_list[-1], new_emphasis)
                    del self.__past_emphasis_list[-1]
                else:
                    self.__past_emphasis_list.append(new_emphasis)
            if next_index is not None:
                found_emphasis_length = (
                    new_emphasis.found_length if new_emphasis is not None else 1
                )
                start_index = next_index + 1 + found_emphasis_length

    def __check(
        self,
        context: PluginScanContext,
        elibible_before: EligibleEmphasis,
        eligible_after: EligibleEmphasis,
    ) -> None:
        if elibible_before.character_after == " ":
            if context.in_fix_mode:
                assert elibible_before.text_token is not None
                self.__fix(elibible_before.text_token, elibible_before, True)
            else:
                self.__report(context, elibible_before, eligible_after.found_length)
        if eligible_after.character_before == " ":
            if context.in_fix_mode:
                assert eligible_after.text_token is not None
                self.__fix(eligible_after.text_token, eligible_after, False)
            else:
                self.__report(context, eligible_after, -1)

    def __process_fixes(self, context: PluginScanContext) -> None:
        current_token = None
        current_text = ""
        current_delta = 0
        for new_bob in self.__pending_fixes:
            if current_token != new_bob.token_to_modify:
                if current_token is not None:
                    self.register_fix_token_request(
                        context, current_token, "next_token", "token_text", current_text
                    )
                current_token = new_bob.token_to_modify
                current_text = current_token.token_text
                current_delta = 0
            current_text = (
                current_text[: new_bob.start_index - current_delta]
                + current_text[new_bob.end_index - current_delta :]
            )
            current_delta += new_bob.end_index - new_bob.start_index
        assert current_token is not None
        self.register_fix_token_request(
            context, current_token, "next_token", "token_text", current_text
        )
        self.__pending_fixes.clear()

    def __fix(
        self,
        token: TextMarkdownToken,
        eligible_after: EligibleEmphasis,
        was_after: bool,
    ) -> None:
        if was_after:
            start_fix_index = eligible_after.start_index + eligible_after.found_length
            end_fix_index, _ = ParserHelper.collect_while_one_of_characters_verified(
                token.token_text, start_fix_index, " \t"
            )
        else:
            _, start_fix_index = (
                ParserHelper.collect_backwards_while_one_of_characters_verified(
                    token.token_text, eligible_after.start_index - 1, " \t"
                )
            )
            end_fix_index = eligible_after.start_index
        self.__pending_fixes.append(PendingFixes(token, start_fix_index, end_fix_index))

    def __report(
        self,
        context: PluginScanContext,
        elibible_before: EligibleEmphasis,
        column_adjust: int,
    ) -> None:
        assert elibible_before.text_token is not None
        before_eligible_text = elibible_before.text_token.token_text[
            : elibible_before.start_index
        ]
        adj_before_eligible_text = ParserHelper.remove_all_from_text(
            before_eligible_text
        )
        line_number_delta = ParserHelper.count_newlines_in_text(
            adj_before_eligible_text
        )
        if line_number_delta:
            last_newline_index = adj_before_eligible_text.rindex("\n") + 1
            column_number_delta = len(adj_before_eligible_text) - last_newline_index
        else:
            column_number_delta = len(adj_before_eligible_text)
        self.report_next_token_error(
            context,
            elibible_before.text_token,
            line_number_delta=line_number_delta,
            column_number_delta=(column_number_delta + column_adjust),
        )

    def __find_next_eligible_emphasis(
        self, text_token: TextMarkdownToken, start_index: int
    ) -> Tuple[Optional[EligibleEmphasis], Optional[int]]:

        asterisk_index = text_token.token_text.find("*", start_index)
        underscore_index = text_token.token_text.find("_", start_index)
        if asterisk_index == -1 and underscore_index == -1:
            return None, None

        if (
            asterisk_index != -1
            and underscore_index != -1
            and asterisk_index < underscore_index
            or asterisk_index != -1
            and underscore_index == -1
        ):
            start_index = asterisk_index
            emphasis_character = "*"
        else:
            start_index = underscore_index
            emphasis_character = "_"

        character_before = (
            text_token.token_text[start_index - 1] if start_index else None
        )
        if character_before == "\b":
            return None, start_index
        found_length, _ = ParserHelper.collect_while_character_verified(
            text_token.token_text, start_index, emphasis_character
        )
        after_index = start_index + found_length
        character_after = (
            text_token.token_text[after_index]
            if after_index < len(text_token.token_text)
            else None
        )
        if character_before == "\a" and character_after == "\a":
            return None, start_index
        return (
            EligibleEmphasis(
                emphasis_character,
                start_index,
                found_length,
                character_before,
                character_after,
                text_token,
            ),
            start_index,
        )
