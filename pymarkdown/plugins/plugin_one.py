"""
Module to implement a sample plugin that just reports that it has been called.
"""
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class PluginOne(RulePlugin):
    """
    Class to implement a sample plugin that just reports that it has been called.
    """

    __valid_values = [0, 1, 2]

    def __init__(self) -> None:
        super().__init__()
        self.test_value = None
        self.other_test_value = None

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="debug-only",
            plugin_id="MD999",
            plugin_enabled_by_default=False,
            plugin_description="Debug plugin",
            plugin_version="0.0.0",
            plugin_interface_version=1,
        )

    @classmethod
    def __validate_configuration_other_test_value(cls, found_value: int) -> None:
        if found_value not in PluginOne.__valid_values:
            raise ValueError(f"Allowable values: {found_value}")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration.
        """
        print(f"{self.get_details().plugin_id}>>init_from_config")
        self.test_value = self.plugin_configuration.get_integer_property(
            "test_value", default_value=1
        )
        print(f"{self.get_details().plugin_id}>>test_value>>{self.test_value}")
        self.other_test_value = self.plugin_configuration.get_integer_property(
            "other_test_value",
            default_value=1,
            valid_value_fn=self.__validate_configuration_other_test_value,
        )
        print(
            f"{self.get_details().plugin_id}>>other_test_value>>{self.other_test_value}"
        )
        if self.test_value == 10:
            raise Exception("because")

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        print(f"{self.get_details().plugin_id}>>starting_new_file>>")

    def next_line(self, context: PluginScanContext, line: str) -> None:
        """
        Event that a new line is being processed.
        """
        _ = context
        print(f"{self.get_details().plugin_id}>>next_line:{line}")

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        _ = context
        print(f"{self.get_details().plugin_id}>>token:{token}")
        if self.test_value == 20:
            raise Exception("because")

    def completed_file(self, context: PluginScanContext) -> None:
        """
        Event that the file being currently scanned is now completed.
        """
        _ = context
        print(f"{self.get_details().plugin_id}>>completed_file")
