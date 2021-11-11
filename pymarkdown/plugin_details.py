"""
Module to provide details about a plugin, supplied by the plugin.
"""


# pylint: disable=too-few-public-methods,too-many-instance-attributes
class PluginDetails:
    """
    Class to provide details about a plugin, supplied by the plugin.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        plugin_id,
        plugin_name,
        plugin_description,
        plugin_enabled_by_default,
        plugin_version,
        plugin_interface_version,
        plugin_url=None,
        plugin_configuration=None,
    ):
        (
            self.plugin_id,
            self.plugin_name,
            self.plugin_description,
            self.plugin_enabled_by_default,
            self.plugin_version,
            self.plugin_interface_version,
            self.plugin_url,
            self.plugin_configuration,
        ) = (
            plugin_id,
            plugin_name,
            plugin_description,
            plugin_enabled_by_default,
            plugin_version,
            plugin_interface_version,
            plugin_url,
            plugin_configuration,
        )

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods,too-many-instance-attributes
