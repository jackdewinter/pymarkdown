"""
Module to encapsulate the transitions from Markdown to HTML.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional

from typing_extensions import override

from pymarkdown.general.parser_helper import ParserHelper


# pylint: disable=too-few-public-methods
class HtmlItems(ABC):
    """
    Base class for all of the HTML items.
    """

    @abstractmethod
    def get_raw_html_text(self) -> str:
        """
        Get the raw html text to produce.
        """


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class HtmlOpenTagItem(HtmlItems):
    """
    Class to encapsulate an HTML Open tag, such as <a>.
    """

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


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class HtmlCloseTagItem(HtmlItems):
    """
    Class to encapsulate an HTML Close tag, such as </a>.
    """

    def __init__(self, tag_name: str):
        self.__tag_name = tag_name

    @override
    def get_raw_html_text(self) -> str:
        return f"</{self.__tag_name}>"


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class HtmlOpenCloseTagItem(HtmlItems):
    """
    Class to encapsulate an HTML Open/Close tag, such as <br/>.
    """

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


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class FormatOnlyNewLineHtmlItem(HtmlItems):
    """
    Class to encapsulate a newline that is mostly inserted for compatability to example format.
    """

    @override
    def get_raw_html_text(self) -> str:
        return ParserHelper.newline_character


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class HtmlBlockNewLineHtmlItem(HtmlItems):
    """
    Class to encapsulate a newline within an HTML block.
    """

    @override
    def get_raw_html_text(self) -> str:
        return ParserHelper.newline_character


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class EmailAutolinkTextItem(HtmlItems):
    """
    Class to encapsulate text content for an email autolink.
    """

    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class UriAutolinkTextItem(HtmlItems):
    """
    Class to encapsulate text content for an uri autolink.
    """

    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class CodeSpanItem(HtmlItems):
    """
    Class to encapsulate text content for a codespan.
    """

    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class CodeBlockItem(HtmlItems):
    """
    Class to encapsulate text content for a code block.
    """

    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class HtmlBlockItem(HtmlItems):
    """
    Class to encapsulate text content for a html block.

    Note that this content "looks" like valid HTML but may not be valid HTML.
    """

    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class SingleRawHtmlItem(HtmlItems):
    """
    Class to encapsulate text content for a single HTML element.

    Note that this content "looks" like valid HTML but may not be valid HTML.
    """

    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return f"<{self.__text_content}>"


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class SetExtTextItem(HtmlItems):
    """
    Class to encapsulate text content for a setext heading
    """

    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class NormalTextItem(HtmlItems):
    """
    Class to encapsulate text content for a normal text section.
    """

    def __init__(self, text_content: str):
        self.__text_content = text_content

    @override
    def get_raw_html_text(self) -> str:
        return self.__text_content


# pylint: enable=too-few-public-methods
