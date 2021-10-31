"""
Module to implement a plugin that looks for inline HTML in the files.
"""
from pymarkdown.parser_helper import ParserHelper
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd033(Plugin):
    """
    Class to implement a plugin that looks for inline HTML in the files.
    """

    def __init__(self):
        super().__init__()
        self.__allowed_elements = None
        self.__allow_first_image_element = None
        self.__is_next_html_block_start = None
        self.__is_first_element = None
        self.__is_first_html_block = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="no-inline-html",
            plugin_id="MD033",
            plugin_enabled_by_default=True,
            plugin_description="Inline HTML",
            plugin_version="0.5.0",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md033.md",
            plugin_configuration="allowed_elements, allow_first_image_element",
        )

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration information.
        """
        self.__allow_first_image_element = (
            self.plugin_configuration.get_boolean_property(
                "allow_first_image_element", default_value=True
            )
        )
        allowed_elements = self.plugin_configuration.get_string_property(
            "allowed_elements",
            default_value="!--,![CDATA[,?",
        )
        self.__allowed_elements = []
        for next_element in allowed_elements.split(","):
            next_element = next_element.strip()
            if next_element:
                self.__allowed_elements.append(next_element)

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        self.__is_next_html_block_start = False
        self.__is_first_html_block = False
        self.__is_first_element = True

    def __look_for_html_start(self, context, token, tag_text):
        full_tag_text = tag_text.lower()
        if tag_text.startswith("/"):
            return
        if tag_text.startswith("![CDATA["):
            tag_text = "![CDATA["
        elif tag_text.startswith("!--"):
            tag_text = "!--"
        else:
            _, tag_text = ParserHelper.collect_until_one_of_characters(
                tag_text, 0, " \n\t/>"
            )
        extra_data = f"Element: {tag_text}"

        is_first_image_element = False
        if (
            self.__is_first_html_block
            and self.__allow_first_image_element
            and tag_text.lower() == "h1"
        ):
            is_first_image_element = full_tag_text.endswith("</h1>")
            if is_first_image_element:
                full_tag_text = full_tag_text[0 : -len("</h1>")]
                end_of_start_heading_index = full_tag_text.find(">")
                assert end_of_start_heading_index != -1
                full_tag_text = full_tag_text[end_of_start_heading_index + 1 :]
                end_of_image_index = full_tag_text.find(">")
                is_first_image_element = (
                    full_tag_text.startswith("<img")
                    and end_of_image_index == len(full_tag_text) - 1
                )

        if not is_first_image_element and tag_text not in self.__allowed_elements:
            self.report_next_token_error(
                context, token, extra_error_information=extra_data
            )

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        if token.is_inline_raw_html:
            self.__is_first_html_block = False
            self.__look_for_html_start(context, token, token.raw_tag)
        elif token.is_html_block:
            self.__is_next_html_block_start = True
            self.__is_first_html_block = self.__is_first_element
        elif token.is_text and self.__is_next_html_block_start:
            self.__look_for_html_start(context, token, token.token_text[1:])
        else:
            self.__is_next_html_block_start = False

        self.__is_first_element = False
