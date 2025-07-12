"""
Module to provide structure to extend the parser
"""

from abc import ABC, abstractmethod

from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.my_application_properties_facade import MyApplicationPropertiesFacade


class ParserExtension(ABC):
    """
    Class to provide structure for extensions to how the parser handles various concepts.
    """

    @abstractmethod
    def get_identifier(self) -> str:
        """
        Get the identifier associated with this extension.
        """

    @abstractmethod
    def get_details(self) -> ExtensionDetails:
        """
        Get the details for the extension.
        """

    @abstractmethod
    def apply_configuration(
        self, extension_specific_facade: MyApplicationPropertiesFacade
    ) -> None:
        """
        Apply any configuration required by the extension.
        """
