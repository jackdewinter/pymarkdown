"""
Module to implement a sample plugin that just reports that it has been called.
"""
from pymarkdown.plugin_manager import Plugin, PluginDetails


class PluginOne(Plugin):
    """
    Class to implement a sample plugin that just reports that it has been called.
    """

    __valid_values = [0, 1, 2]

    def __init__(self):
        super().__init__()
        self.test_value = None
        self.other_test_value = None

    def get_details(self):
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="debug-only",
            plugin_id="MD999",
            plugin_enabled_by_default=False,
            plugin_description="Debug plugin",
        )

    @classmethod
    def __validate_configuration_other_test_value(cls, found_value):
        if found_value not in PluginOne.__valid_values:
            raise ValueError(f"Allowable values: {str(found_value)}")

    def initialize_from_config(self):
        """
        Event to allow the plugin to load configuration.
        """
        print(self.get_details().plugin_id + ">>init_from_config")
        self.test_value = self.plugin_configuration.get_integer_property(
            "test_value", default_value=1
        )
        print(self.get_details().plugin_id + ">>test_value>>" + str(self.test_value))
        self.other_test_value = self.plugin_configuration.get_integer_property(
            "other_test_value",
            default_value=1,
            valid_value_fn=self.__validate_configuration_other_test_value,
        )
        print(
            self.get_details().plugin_id
            + ">>other_test_value>>"
            + str(self.other_test_value)
        )
        if self.test_value == 10:
            raise Exception("because")

    def starting_new_file(self):
        """
        Event that the a new file to be scanned is starting.
        """
        print(self.get_details().plugin_id + ">>starting_new_file>>")

    def next_line(self, context, line):
        """
        Event that a new line is being processed.
        """
        print(self.get_details().plugin_id + ">>next_line:" + line)

    def next_token(self, context, token):
        """
        Event that a new token is being processed.
        """
        print(self.get_details().plugin_id + ">>token:" + str(token))
        if self.test_value == 20:
            raise Exception("because")

    def completed_file(self, context):
        """
        Event that the file being currently scanned is now completed.
        """
        print(self.get_details().plugin_id + ">>completed_file")
