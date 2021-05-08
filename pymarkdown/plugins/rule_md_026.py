"""
Module to implement a plugin that looks for trailing punctuation in headings.
"""
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
            plugin_name="no-trailing-punctuation",
            plugin_id="MD026",
            plugin_enabled_by_default=True,
            plugin_description="Trailing punctuation present in heading text.",
            plugin_version="0.5.0",
            plugin_interface_version=1,
        )

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__punctuation = self.plugin_configuration.get_string_property(
            "punctuation", default_value=".,;:!。，；：！"
        )

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__start_token = None
        self.__heading_text = None

    def next_token(self, context, token):
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
                self.__heading_text += token.token_text
            else:
                self.__heading_text = ""

    def __next_token_end(self, token, context):
        if token.is_setext_heading_end or token.is_atx_heading_end:
            if self.__heading_text:
                if token.is_atx_heading_end:
                    use_original_position = False
                    line_delta = 0
                    column_delta = len(self.__heading_text) - 1
                else:
                    use_original_position = True
                    line_delta = self.__heading_text.count("\n")
                    if line_delta:
                        split_heading_text = self.__heading_text.split("\n")
                        column_delta = len(split_heading_text[-1]) - 1
                    else:
                        column_delta = len(self.__heading_text) - 1
                if self.__heading_text[-1] in self.__punctuation:
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
