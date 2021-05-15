"""
Module to provide for...
"""
import logging

from pymarkdown.markdown_token import MarkdownToken, MarkdownTokenClass
from pymarkdown.parser_logger import ParserLogger

POGGER = ParserLogger(logging.getLogger(__name__))


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
