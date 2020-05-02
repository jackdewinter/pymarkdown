"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.markdown_token import (
    AtxHeaderMarkdownToken,
    EndMarkdownToken,
    MarkdownToken,
    SetextHeaderMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd026(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def __init__(self):
        super().__init__()
        self.start_token = None
        self.header_text = None
        self.punctuation = None

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
        self.punctuation = self.get_configuration_value(
            "punctuation", default_value=".,;:!?。，；：？"
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.start_token = None
        self.header_text = None

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        if isinstance(token, (AtxHeaderMarkdownToken, SetextHeaderMarkdownToken)):
            self.header_text = ""
            self.start_token = token
        elif isinstance(token, EndMarkdownToken):
            if token.type_name in (
                MarkdownToken.token_atx_header,
                MarkdownToken.token_setext_header,
            ):

                if self.header_text:
                    if self.header_text[-1] in self.punctuation:
                        self.report_next_token_error(self.start_token)
                self.start_token = None
            else:
                self.header_text = ""
        elif self.start_token:
            if isinstance(token, TextMarkdownToken):
                self.header_text += token.token_text
            else:
                self.header_text = ""
