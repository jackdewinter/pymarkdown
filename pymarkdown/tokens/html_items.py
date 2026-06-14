from abc import ABC, abstractmethod
from typing import Dict, Optional

from typing_extensions import override

from pymarkdown.general.parser_helper import ParserHelper


class HtmlItems(ABC):
    @abstractmethod
    def get_raw_html_text(self) -> str:
        """
        Get the raw html text to produce.
        """


class HtmlOpenTagItem(HtmlItems):
    def __init__(self, tag_name: str, attributes: Optional[Dict[str, str]] = None):
        self.__tag_name = tag_name
        self.__attributes = attributes

    @override
    def get_raw_html_text(self) -> str:
        parts = [f"<{self.__tag_name}"]

        if self.__attributes:
            parts.extend(f' {i}="{j}"' for i, j in self.__attributes.items())
        parts.append(">")
        return "".join(parts)


class HtmlCloseTagItem(HtmlItems):
    def __init__(self, tag_name: str):
        self.__tag_name = tag_name

    @override
    def get_raw_html_text(self) -> str:
        return f"</{self.__tag_name}>"


class HtmlOpenCloseTagItem(HtmlItems):
    def __init__(self, tag_name: str, attributes: Optional[Dict[str, str]] = None):
        self.__tag_name = tag_name
        self.__attributes = attributes

    @override
    def get_raw_html_text(self) -> str:
        parts = [f"<{self.__tag_name}"]
        if self.__attributes:
            parts.extend(f' {i}="{j}"' for i, j in self.__attributes.items())
        if self.__tag_name.lower() in ["br", "img", "hr"]:
            parts.append(" ")
        parts.append("/>")
        return "".join(parts)


class FormatOnlyNewLineHtmlItem(HtmlItems):
    @override
    def get_raw_html_text(self) -> str:
        return ParserHelper.newline_character


class AutolinkTextItem(HtmlItems):
    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


class CodeSpanItem(HtmlItems):
    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


class CodeBlockItem(HtmlItems):
    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


class HtmlBlockItem(HtmlItems):
    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


class SetExtTextItem(HtmlItems):
    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


class NormalTextItem(HtmlItems):
    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


class SingleRawHtmlItem(HtmlItems):
    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return f"<{self.__text_content}>"


class UriAutolinkTextItem(HtmlItems):
    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


class HtmlBlockNewLineHtmlItem(HtmlItems):
    @override
    def get_raw_html_text(self) -> str:
        return ParserHelper.newline_character


class ZuluHtmlItem(HtmlItems):
    def __init__(self, raw_html_text: str):
        self.__raw_html_text = raw_html_text

    @override
    def get_raw_html_text(self) -> str:
        return self.__raw_html_text
