"""
Module to provide a high level abstraction of the extensions.
"""
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:  # pragma: no cover
    from pymarkdown.extension_manager.extension_manager import ExtensionManager


class ParseBlockPassProperties:
    """
    Class to provide a high level abstraction of the extensions.
    """

    def __init__(self, extension_manager: "ExtensionManager") -> None:
        self.__front_matter_enabled, self.__pragmas_enabled = (
            extension_manager.is_front_matter_enabled,
            extension_manager.is_linter_pragmas_enabled,
        )
        self.pragma_lines: Dict[int, str] = {}

    @property
    def is_front_matter_enabled(self) -> bool:
        """
        Returns whether front matter parsing is enabled.
        """
        return self.__front_matter_enabled

    @property
    def is_pragmas_enabled(self) -> bool:
        """
        Returns whether pragma parsing is enabled.
        """
        return self.__pragmas_enabled
