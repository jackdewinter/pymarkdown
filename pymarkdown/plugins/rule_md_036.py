"""
Module to implement a plugin that looks for single line emphasis text that looks
like it is being used instead of a heading.
"""
from enum import Enum
from typing import Optional, cast

from pymarkdown.inline_markdown_token import TextMarkdownToken
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class RuleMd036States(Enum):
    """
    Enumeration to provide guidance on what to look for as the tokens come in.
    """

    LOOK_FOR_PARAGRAPH = 0
    LOOK_FOR_EMPHASIS_START = 1
    LOOK_FOR_ELIGIBLE_TEXT = 2
    LOOK_FOR_EMPHASIS_END = 3
    LOOK_FOR_PARAGRAPH_END = 4


class RuleMd036(RulePlugin):
    """
    Class to implement a plugin that looks for single line emphasis text that looks
    like it is being used instead of a heading.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__punctuation: str = ""
        self.__current_state: RuleMd036States = RuleMd036States.LOOK_FOR_PARAGRAPH
        self.__start_token: Optional[MarkdownToken] = None

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-emphasis-as-heading,no-emphasis-as-header",
            plugin_id="MD036",
            plugin_enabled_by_default=True,
            plugin_description="Emphasis possibly used instead of a heading element.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md036.md",
            plugin_configuration="punctuation",
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__punctuation = self.plugin_configuration.get_string_property(
            "punctuation", default_value=".,;:!?。，；：？"
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__current_state = RuleMd036States.LOOK_FOR_PARAGRAPH
        self.__start_token = None

    def __handle_look_for_parapgraph(self, token: MarkdownToken) -> RuleMd036States:
        new_state = RuleMd036States.LOOK_FOR_PARAGRAPH
        if token.is_paragraph:
            new_state = RuleMd036States.LOOK_FOR_EMPHASIS_START
            self.__start_token = token
        return new_state

    def __handle_look_for_emphasis_start(self, token: MarkdownToken) -> RuleMd036States:
        return (
            RuleMd036States.LOOK_FOR_ELIGIBLE_TEXT
            if token.is_inline_emphasis
            else RuleMd036States.LOOK_FOR_PARAGRAPH
        )

    def __handle_look_for_eligible_text(self, token: MarkdownToken) -> RuleMd036States:
        new_state = RuleMd036States.LOOK_FOR_PARAGRAPH
        if token.is_text:
            text_token = cast(TextMarkdownToken, token)
            if (
                ParserHelper.newline_character not in text_token.token_text
                and text_token.token_text[-1] not in self.__punctuation
            ):
                new_state = RuleMd036States.LOOK_FOR_EMPHASIS_END
        return new_state

    def __handle_look_for_emphasis_end(self, token: MarkdownToken) -> RuleMd036States:
        return (
            RuleMd036States.LOOK_FOR_PARAGRAPH_END
            if token.is_inline_emphasis_end
            else RuleMd036States.LOOK_FOR_PARAGRAPH
        )

    def __handle_look_for_parapgraph_end(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> RuleMd036States:
        new_state = RuleMd036States.LOOK_FOR_PARAGRAPH
        if token.is_paragraph_end:
            assert self.__start_token is not None
            self.report_next_token_error(context, self.__start_token)
        return new_state

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        new_state = RuleMd036States.LOOK_FOR_PARAGRAPH

        if self.__current_state == RuleMd036States.LOOK_FOR_PARAGRAPH:
            new_state = self.__handle_look_for_parapgraph(token)
        elif self.__current_state == RuleMd036States.LOOK_FOR_EMPHASIS_START:
            new_state = self.__handle_look_for_emphasis_start(token)
        elif self.__current_state == RuleMd036States.LOOK_FOR_ELIGIBLE_TEXT:
            new_state = self.__handle_look_for_eligible_text(token)
        elif self.__current_state == RuleMd036States.LOOK_FOR_EMPHASIS_END:
            new_state = self.__handle_look_for_emphasis_end(token)
        else:
            assert self.__current_state == RuleMd036States.LOOK_FOR_PARAGRAPH_END
            new_state = self.__handle_look_for_parapgraph_end(context, token)

        self.__current_state = new_state
