"""
Module to allow for the details on the extension to be encapsulated.
"""


# pylint: disable=too-many-instance-attributes
class ExtensionDetails:
    """
    Class to allow for the details on the extension to be encapsulated.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        extension_id,
        extension_name,
        extension_description,
        extension_enabled_by_default,
        extension_version,
        extension_interface_version,
        extension_url=None,
        extension_configuration=None,
    ):
        (
            self.__extension_id,
            self.__extension_name,
            self.__extension_description,
            self.__extension_enabled_by_default,
            self.__extension_version,
            self.__extension_interface_version,
            self.__extension_url,
            self.__extension_configuration,
        ) = (
            extension_id,
            extension_name,
            extension_description,
            extension_enabled_by_default,
            extension_version,
            extension_interface_version,
            extension_url,
            extension_configuration,
        )

    # pylint: enable=too-many-arguments

    @property
    def extension_id(self):
        """
        Property to get the id of the extension.
        """
        return self.__extension_id

    @property
    def extension_name(self):
        """
        Property to get the name of the extension.
        """
        return self.__extension_name

    @property
    def extension_description(self):
        """
        Property to get the short description of the extension.
        """
        return self.__extension_description

    @property
    def extension_enabled_by_default(self):
        """
        Property to get whether the extension is enabled by default.
        """
        return self.__extension_enabled_by_default

    @property
    def extension_version(self):
        """
        Property to get the version of the extension.
        """
        return self.__extension_version

    @property
    def extension_interface_version(self):
        """
        Property to get the interface version of the extension.
        """
        return self.__extension_interface_version

    @property
    def extension_url(self):
        """
        Property to get the optional url for the extension.
        """
        return self.__extension_url

    @property
    def extension_configuration(self):
        """
        Property to get the optional configuration items for the extension.
        """
        return self.__extension_configuration


# pylint: enable=too-many-instance-attributes
