"""
Module to implement a plugin that looks for spaces within emphasis sections.
"""
from typing import List, Optional, cast

from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.inline_markdown_token import TextMarkdownToken


class RuleMd037(RulePlugin):
    """
    Class to implement a plugin that looks for spaces within emphasis sections.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__block_stack: List[MarkdownToken] = []
        self.__start_emphasis_token: Optional[TextMarkdownToken] = None
        self.__emphasis_token_list: List[MarkdownToken] = []

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-space-in-emphasis",
            plugin_id="MD037",
            plugin_enabled_by_default=True,
            plugin_description="Spaces inside emphasis markers",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md037.md",
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__block_stack = []
        self.__start_emphasis_token = None
        self.__emphasis_token_list = []

    def __handle_emphasis_text(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        text_token = cast(TextMarkdownToken, token)
        assert self.__start_emphasis_token is not None
        if text_token.token_text == self.__start_emphasis_token.token_text:
            assert self.__emphasis_token_list
            did_first_start_with_space = self.__handle_emphasis_text_space_check(0)
            did_last_end_with_space = self.__handle_emphasis_text_space_check(-1)
            if did_first_start_with_space or did_last_end_with_space:
                assert self.__start_emphasis_token is not None
                self.report_next_token_error(context, self.__start_emphasis_token)

            self.__start_emphasis_token = None
            self.__emphasis_token_list = []
        else:
            self.__emphasis_token_list.append(token)

    def __handle_emphasis_text_space_check(self, token_text_index: int) -> bool:
        first_capture_token = self.__emphasis_token_list[token_text_index]
        assert first_capture_token.is_text
        other_text_token = cast(TextMarkdownToken, first_capture_token)
        return other_text_token.token_text[token_text_index] == " "

    def __handle_start_emphasis(
        self, context: PluginScanContext, token: MarkdownToken
    ) -> None:
        if (
            token.is_paragraph_end
            or token.is_setext_heading_end
            or token.is_atx_heading_end
        ):
            del self.__block_stack[-1]
            self.__start_emphasis_token = None
            self.__emphasis_token_list = []
        elif token.is_text and self.__start_emphasis_token is not None:
            self.__handle_emphasis_text(context, token)
        else:
            self.__emphasis_token_list.append(token)

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if self.__start_emphasis_token:
            self.__handle_start_emphasis(context, token)
        elif token.is_paragraph or token.is_setext_heading or token.is_atx_heading:
            self.__block_stack.append(token)
        elif token.is_paragraph_end or token.is_setext_heading_end:
            del self.__block_stack[-1]
        elif (
            token.is_text
            and self.__block_stack
            and (
                self.__block_stack[-1].is_paragraph
                or self.__block_stack[-1].is_setext_heading
                or self.__block_stack[-1].is_atx_heading
            )
        ):
            text_token = cast(TextMarkdownToken, token)
            if text_token.token_text in ("*", "**", "_", "__"):
                self.__start_emphasis_token = text_token
