"""
Module to allow for the details on the extension to be encapsulated.
"""

from dataclasses import dataclass
from typing import Optional

# pylint: disable=too-many-instance-attributes


@dataclass(frozen=True)
class ExtensionDetails:
    """
    Class to allow for the details on the extension to be encapsulated.
    """

    extension_id: str
    extension_name: str
    extension_description: str
    extension_enabled_by_default: bool
    extension_version: str
    extension_interface_version: int
    extension_url: Optional[str]
    extension_configuration: Optional[str]


# pylint: enable=too-many-instance-attributes
