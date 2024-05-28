"""
Module to provide details about a plugin, supplied by the plugin.
"""

from dataclasses import dataclass
from typing import Optional, Union


# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True)
class PluginDetails:
    """
    Class to provide details about a plugin, supplied by the plugin.
    """

    plugin_id: str
    plugin_name: str
    plugin_description: str
    plugin_enabled_by_default: bool
    plugin_version: str
    plugin_interface_version: int = 1
    plugin_url: Optional[str] = None
    plugin_configuration: Optional[str] = None


# pylint: enable=too-many-instance-attributes


@dataclass(frozen=True)
class PluginDetailsV2(PluginDetails):
    """
    Class to provide details about a plugin, supplied by the plugin.
    """

    plugin_supports_fix: bool = False
    plugin_interface_version: int = 2
    plugin_fix_level: int = 1


@dataclass(frozen=True)
class PluginDetailsV3(PluginDetailsV2):
    """
    Class to provide details about a plugin, supplied by the plugin.
    """

    plugin_interface_version: int = 3


@dataclass(frozen=True)
class QueryConfigItem:
    """
    Class to provide information on the configuration items for the plugin.
    """

    name: str
    value: Union[bool, int, str]
