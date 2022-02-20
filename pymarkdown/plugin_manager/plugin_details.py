"""
Module to provide details about a plugin, supplied by the plugin.
"""


# pylint: disable=too-many-instance-attributes
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
            self.__plugin_id,
            self.__plugin_name,
            self.__plugin_description,
            self.__plugin_enabled_by_default,
            self.__plugin_version,
            self.__plugin_interface_version,
            self.__plugin_url,
            self.__plugin_configuration,
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

    @property
    def plugin_id(self):
        """
        Gets the id associated with the plugin.
        """
        return self.__plugin_id

    @property
    def plugin_name(self):
        """
        Gets the names associated with the plugin.
        """
        return self.__plugin_name

    @property
    def plugin_description(self):
        """
        Gets the description of the plugin.
        """
        return self.__plugin_description

    @property
    def plugin_enabled_by_default(self):
        """
        Gets a value indicating whether the plugin is enabled by default.
        """
        return self.__plugin_enabled_by_default

    @property
    def plugin_version(self):
        """
        Gets the version of the plugin.
        """
        return self.__plugin_version

    @property
    def plugin_interface_version(self):
        """
        Gets the interface version of the plugin.
        """
        return self.__plugin_interface_version

    @property
    def plugin_url(self):
        """
        Gets the optional url for the plugin.
        """
        return self.__plugin_url

    @property
    def plugin_configuration(self):
        """
        Gets the optional configuration items for the plugin.
        """
        return self.__plugin_configuration


# pylint: enable=too-many-instance-attributes
