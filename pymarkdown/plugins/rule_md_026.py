"""
Module to implement a plugin that looks for trailing punctuation in headings.
"""

from typing import Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class RuleMd026(RulePlugin):
    """
    Class to implement a plugin that looks for trailing punctuation in headings.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__start_token: Optional[MarkdownToken] = None
        self.__heading_text = ""
        self.__punctuation = ""

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-trailing-punctuation",
            plugin_id="MD026",
            plugin_enabled_by_default=True,
            plugin_description="Trailing punctuation present in heading text.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md026.md",
            plugin_configuration="punctuation",
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__punctuation = self.plugin_configuration.get_string_property(
            "punctuation", default_value=".,;:!。，；：！"
        )

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__start_token = None
        self.__heading_text = ""

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if token.is_setext_heading or token.is_atx_heading:
            self.__heading_text = ""
            self.__start_token = token
        elif token.is_end_token:
            self.__next_token_end(token, context)
        elif self.__start_token:
            if token.is_text:
                text_token = cast(TextMarkdownToken, token)
                self.__heading_text += text_token.token_text
            else:
                self.__heading_text = ""

    def __next_token_end(
        self, token: MarkdownToken, context: PluginScanContext
    ) -> None:
        if token.is_setext_heading_end or token.is_atx_heading_end:
            if self.__heading_text:
                if token.is_atx_heading_end:
                    use_original_position = False
                    line_delta = 0
                    column_delta = len(self.__heading_text) - 1
                else:
                    use_original_position = True
                    line_delta = self.__heading_text.count(
                        ParserHelper.newline_character
                    )
                    if line_delta:
                        split_heading_text = self.__heading_text.split(
                            ParserHelper.newline_character
                        )
                        column_delta = len(split_heading_text[-1]) - 1
                    else:
                        column_delta = len(self.__heading_text) - 1
                if self.__heading_text[-1] in self.__punctuation:
                    assert self.__start_token is not None
                    self.report_next_token_error(
                        context,
                        self.__start_token,
                        line_number_delta=line_delta,
                        column_number_delta=column_delta,
                        use_original_position=use_original_position,
                    )
            self.__start_token = None
        else:
            self.__heading_text = ""
