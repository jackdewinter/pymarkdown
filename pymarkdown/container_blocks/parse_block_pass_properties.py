"""
Module to provide a high level abstraction of the extensions.
"""
from typing import TYPE_CHECKING, Dict, Optional, cast

from pymarkdown.extensions.disallowed_raw_html import MarkdownDisallowRawHtmlExtension

if TYPE_CHECKING:  # pragma: no cover
    from pymarkdown.extension_manager.extension_manager import ExtensionManager


class ParseBlockPassProperties:
    """
    Class to provide a high level abstraction of the extensions.
    """

    def __init__(self, extension_manager: "ExtensionManager") -> None:
        (
            self.__front_matter_enabled,
            self.__pragmas_enabled,
            self.__disallow_raw_html_enabled,
        ) = (
            extension_manager.is_front_matter_enabled,
            extension_manager.is_linter_pragmas_enabled,
            extension_manager.is_disallow_raw_html_enabled,
        )
        self.pragma_lines: Dict[int, str] = {}

        self.__disable_raw_html_extension = None
        if self.__disallow_raw_html_enabled:
            ext_instance = extension_manager.get_extension_instance(
                MarkdownDisallowRawHtmlExtension().get_identifier()
            )
            self.__disable_raw_html_extension = cast(
                MarkdownDisallowRawHtmlExtension, ext_instance
            )

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

    @property
    def is_disallow_raw_html_enabled(self) -> bool:
        """
        Returns whether disallow raw html is enabled.
        """
        return self.__disallow_raw_html_enabled

    @property
    def disallow_raw_html(self) -> Optional[MarkdownDisallowRawHtmlExtension]:
        return self.__disable_raw_html_extension
