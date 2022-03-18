"""
Module to provide for an encapsulation of a plugin that was discovered.
"""


# pylint: disable=too-many-instance-attributes
from dataclasses import dataclass
from typing import List, Optional

from pymarkdown.plugin_manager.rule_plugin import RulePlugin


@dataclass(frozen=True)
class FoundPlugin:
    """
    Encapsulation of a plugin that was discovered.  While similar to the PluginDetails
    class, this is meant for an internal representation of the plugin, and not the
    external information provided.
    """

    plugin_id: str
    plugin_names: List[str]
    plugin_description: str
    plugin_instance: RulePlugin
    plugin_enabled_by_default: bool
    plugin_version: str
    plugin_interface_version: int
    plugin_file_name: str
    plugin_url: Optional[str]
    plugin_configuration: Optional[str]
    plugin_identifiers: List[str]


# pylint: enable=too-many-instance-attributes
