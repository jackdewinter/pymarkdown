"""
Module to implement a plugin that looks for trailing punctuation in headings.
"""
from pymarkdown.markdown_token import (
    AtxHeadingMarkdownToken,
    EndMarkdownToken,
    MarkdownToken,
    SetextHeadingMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd026(Plugin):
    """
    Class to implement a plugin that looks for trailing punctuation in headings.
    """

    def __init__(self):
        super().__init__()
        self.__start_token = None
        self.__heading_text = None
        self.__punctuation = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers
            plugin_name="no-trailing-punctuation",
            plugin_id="MD026",
            plugin_enabled_by_default=True,
            plugin_description="Trailing punctuation in heading",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md026---trailing-punctuation-in-heading
        # Parameters: punctuation (string; default ".,;:!?。，；：？")

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__punctuation = self.get_configuration_value(
            "punctuation", default_value=".,;:!?。，；：？"
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__start_token = None
        self.__heading_text = None

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        if isinstance(token, (AtxHeadingMarkdownToken, SetextHeadingMarkdownToken)):
            self.__heading_text = ""
            self.__start_token = token
        elif isinstance(token, EndMarkdownToken):
            if token.type_name in (
                MarkdownToken.token_atx_heading,
                MarkdownToken.token_setext_heading,
            ):

                if self.__heading_text:
                    if self.__heading_text[-1] in self.__punctuation:
                        self.report_next_token_error(self.__start_token)
                self.__start_token = None
            else:
                self.__heading_text = ""
        elif self.__start_token:
            if isinstance(token, TextMarkdownToken):
                self.__heading_text += token.token_text
            else:
                self.__heading_text = ""
