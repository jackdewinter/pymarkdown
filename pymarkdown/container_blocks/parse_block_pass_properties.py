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
        """
        Note: is_strike_through_enabled is not included in this list as it exclusively
              effects the inline processing which does not require these properties
        """

        (
            self.__front_matter_enabled,
            self.__pragmas_enabled,
            self.__disallow_raw_html_enabled,
            self.__task_lists_enabled,
            self.__tables_enabled,
        ) = (
            extension_manager.is_front_matter_enabled,
            extension_manager.is_linter_pragmas_enabled,
            extension_manager.is_disallow_raw_html_enabled,
            extension_manager.is_task_list_items_enabled,
            extension_manager.is_tables_enabled,
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

    @property
    def is_task_lists_enabled(self) -> bool:
        """
        Returns whether task lists are enabled.
        """
        return self.__task_lists_enabled

    @property
    def is_tables_enabled(self) -> bool:
        """
        Returns whether tables are enabled.
        """
        return self.__tables_enabled
