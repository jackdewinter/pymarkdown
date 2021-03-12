"""
Module to implement a plugin that looks for single line emphasis text that looks
like it is being used instead of a heading.
"""
from enum import Enum

from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd036States(Enum):
    """
    Enumeration to provide guidance on what to look for as the tokens come in.
    """

    LOOK_FOR_PARAGRAPH = 0
    LOOK_FOR_EMPHASIS_START = 1
    LOOK_FOR_ELIGIBLE_TEXT = 2
    LOOK_FOR_EMPHASIS_END = 3
    LOOK_FOR_PARAGRAPH_END = 4


class RuleMd036(Plugin):
    """
    Class to implement a plugin that looks for single line emphasis text that looks
    like it is being used instead of a heading.
    """

    def __init__(self):
        super().__init__()
        self.__punctuation = None
        self.__current_state = None
        self.__start_token = None

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
        self.__punctuation = self.plugin_configuration.get_string_property(
            "punctuation", default_value=".,;:!?。，；：？"
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__current_state = RuleMd036States.LOOK_FOR_PARAGRAPH
        self.__start_token = None

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        new_state = RuleMd036States.LOOK_FOR_PARAGRAPH

        if self.__current_state == RuleMd036States.LOOK_FOR_PARAGRAPH:
            if token.is_paragraph:
                new_state = RuleMd036States.LOOK_FOR_EMPHASIS_START
                self.__start_token = token
        elif self.__current_state == RuleMd036States.LOOK_FOR_EMPHASIS_START:
            if token.is_inline_emphasis:
                new_state = RuleMd036States.LOOK_FOR_ELIGIBLE_TEXT
        elif self.__current_state == RuleMd036States.LOOK_FOR_ELIGIBLE_TEXT:
            if token.is_text:
                if (
                    "\n" not in token.token_text
                    and token.token_text[-1] not in self.__punctuation
                ):
                    new_state = RuleMd036States.LOOK_FOR_EMPHASIS_END
        elif self.__current_state == RuleMd036States.LOOK_FOR_EMPHASIS_END:
            if token.is_inline_emphasis_end:
                new_state = RuleMd036States.LOOK_FOR_PARAGRAPH_END
        else:
            assert self.__current_state == RuleMd036States.LOOK_FOR_PARAGRAPH_END
            if token.is_paragraph_end:
                self.report_next_token_error(context, self.__start_token)

        self.__current_state = new_state
