"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.markdown_token import (
    EmphasisMarkdownToken,
    EndMarkdownToken,
    MarkdownToken,
    ParagraphMarkdownToken,
    TextMarkdownToken,
)
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd036(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def __init__(self):
        super().__init__()
        self.punctuation = None
        self.current_state = None
        self.start_token = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # headings, headers, emphasis
            plugin_name="no-emphasis-as-heading,no-emphasis-as-header",
            plugin_id="MD036",
            plugin_enabled_by_default=True,
            plugin_description="Emphasis used instead of a heading",
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md036---emphasis-used-instead-of-a-heading
        # Parameters: punctuation (string; default ".,;:!?。，；：！？")

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
        self.current_state = 0
        self.start_token = None

    def next_token(self, token):
        """
        Event that a new token is being processed.
        """
        new_state = 0
        if self.current_state == 0:
            if isinstance(token, ParagraphMarkdownToken):
                new_state = 1
                self.start_token = token
        elif self.current_state == 1:
            if isinstance(token, EmphasisMarkdownToken):
                new_state = 2
        elif self.current_state == 2:
            if isinstance(token, TextMarkdownToken):
                if (
                    "\n" not in token.token_text
                    and token.token_text[-1] not in self.punctuation
                ):
                    new_state = 3
        elif self.current_state == 3:
            if (
                isinstance(token, EndMarkdownToken)
                and token.type_name == MarkdownToken.token_inline_emphasis
            ):
                new_state = 4
        else:
            assert self.current_state == 4
            if (
                isinstance(token, EndMarkdownToken)
                and token.type_name == MarkdownToken.token_paragraph
            ):
                self.report_next_token_error(self.start_token)

        self.current_state = new_state
