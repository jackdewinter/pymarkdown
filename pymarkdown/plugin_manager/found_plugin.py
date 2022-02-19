"""
Module to provide for an encapsulation of a plugin that was discovered.
"""


# pylint: disable=too-many-instance-attributes
class FoundPlugin:
    """
    Encapsulation of a plugin that was discovered.  While similar to the PluginDetails
    class, this is meant for an internal representation of the plugin, and not the
    external information provided.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        plugin_id,
        plugin_name,
        plugin_description,
        plugin_instance,
        plugin_enabled_by_default,
        plugin_version,
        plugin_interface_version,
        instance_file_name,
        plugin_url,
        plugin_configuration,
    ):
        """
        Initializes a new instance of the FoundPlugin class.
        """
        (
            self.__plugin_id,
            self.__plugin_names,
            self.__plugin_description,
            self.__plugin_instance,
            self.__plugin_enabled_by_default,
            self.__plugin_version,
            self.__plugin_interface_version,
            self.__plugin_file_name,
            self.__plugin_url,
            self.__plugin_configuration,
        ) = (
            plugin_id.strip().lower(),
            [],
            plugin_description,
            plugin_instance,
            plugin_enabled_by_default,
            plugin_version,
            plugin_interface_version,
            instance_file_name,
            plugin_url,
            plugin_configuration,
        )
        for next_name in plugin_name.lower().split(","):
            next_name = next_name.strip()
            if next_name:
                self.__plugin_names.append(next_name)

    # pylint: enable=too-many-arguments

    @property
    def plugin_id(self):
        """
        Gets the id associated with the plugin.
        """
        return self.__plugin_id

    @property
    def plugin_names(self):
        """
        Gets the names associated with the plugin.
        """
        return self.__plugin_names

    @property
    def plugin_identifiers(self):
        """
        Gets the identifiers (id+names) for the plugin.
        """
        plugin_keys = [self.plugin_id]
        plugin_keys.extend(self.plugin_names)
        return plugin_keys

    @property
    def plugin_description(self):
        """
        Gets the description of the plugin.
        """
        return self.__plugin_description

    @property
    def plugin_instance(self):
        """
        Gets the actual instance of the plugin.
        """
        return self.__plugin_instance

    @property
    def plugin_file_name(self):
        """
        Gets the filename where the plugin's class is stored.
        """
        return self.__plugin_file_name

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

    @property
    def plugin_enabled_by_default(self):
        """
        Gets a value indicating whether the plugin is enabled by default.
        """
        return self.__plugin_enabled_by_default


# pylint: enable=too-many-instance-attributes
