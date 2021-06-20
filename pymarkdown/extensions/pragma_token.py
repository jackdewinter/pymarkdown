"""
Module to provide for linter instructions that can be embedded within the document.
"""
import logging

from pymarkdown.extension_impl import ExtensionDetails
from pymarkdown.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods
class PragmaExtension:
    """
    Extension to implement the pragma extensions.
    """

    @classmethod
    def get_details(cls):
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id="linter-pragmas",
            extension_name="Pragma Linter Instructions",
            extension_description="Allows parsing of instructions for the linter.",
            extension_enabled_by_default=True,
            extension_version="0.5.0",
            extension_interface_version=1,
            extension_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/extensions/pragmas.md",
            extension_configuration=None,
        )

    @classmethod
    def apply_configuration(cls, extension_specific_facade):
        """
        Apply any configuration required by the extension.
        """
        _ = extension_specific_facade


# pylint: enable=too-few-public-methods


class PragmaToken(MarkdownToken):
    """
    Token that contains the pragmas for the document.
    """

    pragma_prefix = "<!--"
    pragma_alternate_prefix = "<!---"
    pragma_title = "pyml "
    pragma_suffix = "-->"

    def __init__(self, pragma_lines):
        self.__pragma_lines = pragma_lines

        serialized_pragmas = ""
        for next_line_number in pragma_lines:
            serialized_pragmas += (
                ";" + str(next_line_number) + ":" + pragma_lines[next_line_number]
            )

        MarkdownToken.__init__(
            self,
            MarkdownToken._token_pragma,
            MarkdownTokenClass.SPECIAL,
            is_extension=True,
            extra_data=serialized_pragmas[1:],
        )

    @property
    def pragma_lines(self):
        """
        Returns the pragma lines for the document.
        """
        return self.__pragma_lines
