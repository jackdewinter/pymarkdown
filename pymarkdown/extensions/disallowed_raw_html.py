"""
Module to provide for disallowing raw HTML in document.
"""

import string
from typing import Set

from application_properties import ApplicationPropertiesFacade

from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager_constants import (
    ExtensionManagerConstants,
)
from pymarkdown.extension_manager.parser_extension import ParserExtension


class MarkdownDisallowRawHtmlExtension(ParserExtension):
    """
    Extension to implement the disallow rawhtml extension.
    """

    def __init__(self) -> None:
        self.__disallowed_tag_names: Set[str] = set()

    def get_identifier(self) -> str:
        """
        Get the identifier associated with this extension.
        """
        return "markdown-disallow-raw-html"

    def get_details(self) -> ExtensionDetails:
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=self.get_identifier(),
            extension_name="Markdown Disallow Raw HTML",
            extension_description="Disallows parsing of any raw HTML.",
            extension_enabled_by_default=False,
            extension_version="0.5.0",
            extension_interface_version=ExtensionManagerConstants.EXTENSION_INTERFACE_VERSION_BASIC,
            extension_url="https://github.github.com/gfm/#disallowed-raw-html-extension-",
            extension_configuration=None,
        )

    __valid_tag_name_characters = f"{string.ascii_letters}{string.digits}-"

    @staticmethod
    def is_valid_tag_name(tag_name: str) -> bool:
        """
        Determine if the html tag name is valid according to the html rules.
        """

        return (
            all(
                next_character
                in MarkdownDisallowRawHtmlExtension.__valid_tag_name_characters
                for next_character in tag_name.lower()
            )
            if tag_name
            else False
        )

    def apply_configuration(
        self, extension_specific_facade: ApplicationPropertiesFacade
    ) -> None:
        """
        Apply any configuration required by the extension.
        """
        self.__disallowed_tag_names = {
            "title",
            "textarea",
            "style",
            "xmp",
            "iframe",
            "noembed",
            "noframes",
            "script",
            "plaintext",
        }

        modify_tag_names = extension_specific_facade.get_string_property(
            "change_tag_names", default_value=None
        )
        if modify_tag_names is not None:
            tag_config_name = f"extensions.{self.get_identifier()}.change_tag_names"
            for next_tag_part in modify_tag_names.split(","):
                next_tag_part = next_tag_part.strip(" ")
                if not next_tag_part:
                    raise ValueError(
                        f"Configuration item '{tag_config_name}' contains at least one empty string."
                    )
                if next_tag_part[0] not in ("+", "-"):
                    raise ValueError(
                        f"Configuration item '{tag_config_name}' elements must either start with '+' or '-'."
                    )
                remaining_tag_part = next_tag_part[1:]
                if not MarkdownDisallowRawHtmlExtension.is_valid_tag_name(
                    remaining_tag_part
                ):
                    raise ValueError(
                        f"Configuration item '{tag_config_name}' contains an element '{remaining_tag_part}' that is not a valid tag name."
                    )
                if next_tag_part[0] == "+":
                    self.__disallowed_tag_names.add(remaining_tag_part.lower())
                else:
                    self.__disallowed_tag_names.remove(remaining_tag_part.lower())

    def is_html_tag_disallowed(self, tag_name: str) -> bool:
        """
        Determine if the specified tag name is allowed.
        """
        tag_name = tag_name.lower()
        return tag_name in self.__disallowed_tag_names
