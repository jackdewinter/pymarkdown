"""
Module to implement a plugin that looks for spaces within emphasis sections.
"""
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class RuleMd037(RulePlugin):
    """
    Class to implement a plugin that looks for spaces within emphasis sections.
    """

    def __init__(self):
        super().__init__()
        self.__block_stack = None
        self.__start_emphasis_token = None
        self.__emphasis_token_list = []

    def get_details(self):
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

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__block_stack = []
        self.__start_emphasis_token = None
        self.__emphasis_token_list = []

    def __handle_start_emphasis(self, context, token):
        if (
            token.is_paragraph_end
            or token.is_setext_heading_end
            or token.is_atx_heading_end
        ):
            del self.__block_stack[-1]
            self.__start_emphasis_token = None
            self.__emphasis_token_list = []
        elif (
            token.is_text and token.token_text == self.__start_emphasis_token.token_text
        ):
            assert self.__emphasis_token_list
            first_capture_token = self.__emphasis_token_list[0]
            did_first_start_with_space = (
                first_capture_token.is_text and first_capture_token.token_text[0] == " "
            )
            last_capture_token = self.__emphasis_token_list[-1]
            did_last_end_with_space = (
                last_capture_token.is_text and last_capture_token.token_text[-1] == " "
            )
            if did_first_start_with_space or did_last_end_with_space:
                self.report_next_token_error(context, self.__start_emphasis_token)

            self.__start_emphasis_token = None
            self.__emphasis_token_list = []
        else:
            self.__emphasis_token_list.append(token)

    def next_token(self, context, token):
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
            if token.token_text in ("*", "**", "_", "__"):
                self.__start_emphasis_token = token
