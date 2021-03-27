"""
Module to implement a plugin that looks for hard tabs in the files.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class RuleMd013(Plugin):
    """
    Class to implement a plugin that looks for hard tabs in the files.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            # line_length
            plugin_name="line-length",
            plugin_id="MD013",
            plugin_enabled_by_default=False,
            plugin_description="Line length",
            plugin_version="0.0.0",
            plugin_interface_version=1,
        )  # https://github.com/DavidAnson/markdownlint/blob/master/doc/Rules.md#md013---line-length
        # Parameters: line_length, heading_line_length, code_block_line_length, code_blocks, tables, headings, headers, strict (number; default 80, boolean; default true)
