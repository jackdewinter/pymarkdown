



from abc import ABC, abstractmethod
from typing_extensions import override

from pymarkdown.general.parser_helper import ParserHelper


class HtmlItems(ABC):
    @abstractmethod
    def get_raw_html_text(self) -> str:
        """
        Get the raw html text to produce.
        """

class HtmlStartTagItem(HtmlItems):
    def __init__(self, tag_name : str):
        self.__tag_name = tag_name

    @override
    def get_raw_html_text(self) -> str:
        return f"<{self.__tag_name}>"
class HtmlCloseTagItem(HtmlItems):
    def __init__(self, tag_name : str):
        self.__tag_name = tag_name

    @override
    def get_raw_html_text(self) -> str:
        return f"</{self.__tag_name}>"

class FormatOnlyNewLineHtmlItem(HtmlItems):
    @override
    def get_raw_html_text(self) -> str:
        return ParserHelper.newline_character
class ZuluHtmlItem(HtmlItems):
    def __init__(self, raw_html_text : str):
        self.__raw_html_text = raw_html_text

    @override
    def get_raw_html_text(self) -> str:
        return self.__raw_html_text