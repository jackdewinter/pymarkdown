"""
Module to provide details about a plugin, supplied by the plugin.
"""

from dataclasses import dataclass
from typing import Optional, Union


# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True)
class PluginDetails:
    """Class to provide details about a plugin, supplied by the plugin."""

    plugin_id: str
    """Unique identifier of the form `AAANNN` or `AANNN`
    """
    plugin_name: str
    """Unique human readable name(s), comma-separated.
    """
    plugin_description: str
    """One sentence description for the Rule Plugin.
    """
    plugin_enabled_by_default: bool
    """Whether the Rule Plugin is enabled as default.
    """
    plugin_version: str
    """Semantic version of the Rule Plugin.
    """
    plugin_interface_version: int = 1
    """Interface version.
    """
    plugin_url: Optional[str] = None
    """Optional URL to more exhaustive documentation on the Rule Plugin.
    """
    plugin_configuration: Optional[str] = None
    """Optional comma-separated list of configuration values, for display only.
    """


# pylint: enable=too-many-instance-attributes


@dataclass(frozen=True)
class PluginDetailsV2(PluginDetails):
    """
    Class to provide details about a plugin, supplied by the plugin.
    """

    plugin_supports_fix: bool = False
    """Whether the Rule Plugin supports the autofix capability.
    """
    plugin_interface_version: int = 2
    """Interface version.
    """
    plugin_fix_level: int = 1
    """Relative ordering within the Fix workflow.
    """


@dataclass(frozen=True)
class PluginDetailsV3(PluginDetailsV2):
    """
    Class to provide details about a plugin, supplied by the plugin.
    """

    plugin_interface_version: int = 3
    """Interface version.
    """


@dataclass(frozen=True)
class QueryConfigItem:
    """
    Class to provide information on the configuration items for the plugin.
    """

    name: str
    value: Union[bool, int, str]
