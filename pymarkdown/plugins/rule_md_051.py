"""
Module to implement a plugin that ensures that locally aimed link fragments are valid.
"""

from enum import Enum
from html.parser import HTMLParser
from typing import Dict, List, Set, cast
import re
import urllib

from pymarkdown.plugin_manager.plugin_details import (
    PluginDetailsV2,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken
from pymarkdown.tokens.link_start_markdown_token import LinkStartMarkdownToken
from pymarkdown.tokens.raw_html_markdown_token import RawHtmlMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken

class RuleMd051States(Enum):
    """
    Enumeration to provide guidance on what to look for as the tokens come in.
    """

    LOOK_FOR_LINKS_OR_HEADINGS = 0
    LOOK_FOR_ATX_END = 1
    LOOK_FOR_SETEXT_END = 2
    LOOK_FOR_HTML_BLOCK_END = 3

class MyHTMLParser(HTMLParser):

    def __init__(self):
        self.valid_targets : List[str] = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        found_target = next(
            (
                value
                for attr, value in attrs
                if tag == "a"
                and attr in ["id", "name"]
                or tag != "a"
                and attr == "id"
            ),
            None,
        )
        if found_target is not None:
            self.valid_targets.append(found_target)

class RuleMd051(RulePlugin):
    """
    Class to implement a plugin that ensures that locally aimed link fragments are valid.
    """

    __PUNCTUATION_REGEXP = re.compile(r'[^\w\- ]')

    def __init__(self) -> None:
        """
        Initialize an instance of the RuleMd048 class.
        """
        super().__init__()

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="link-fragments",
            plugin_id="MD051",
            plugin_enabled_by_default=True,
            plugin_description="Link fragments should be valid.",
            plugin_version="0.5.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md051.md",
            plugin_configuration="ignore_case",
            # plugin_supports_fix=True,
            # plugin_fix_level=2,
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__ignore_case = self.plugin_configuration.get_boolean_property_with_default(            "ignore_case",            True        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("ignore_case", self.__ignore_case),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__current_heading = ""
        self.__heading_state = RuleMd051States.LOOK_FOR_LINKS_OR_HEADINGS
        self.__present_headings : Dict[str,int]= {}
        self.__available_headings : Set[str] = set()
        self.__link_tokens : List[LinkStartMarkdownToken] = []

    def completed_file(self, context: PluginScanContext) -> None:
        """
        Event that the file being currently scanned is now completed.
        """
        for link_token in self.__link_tokens:
            link_text = link_token.link_uri[1:]
            if link_text != "top" and link_text not in self.__available_headings:
                self.report_next_token_error(
                    context, link_token, extra_error_information=None
                )
# ?plain=1#L14
    def __encodeURIComponent(self, s: str) -> str:
        """
        Python equivalent of JavaScript's encodeURIComponent().
        Encodes all characters except: A-Z a-z 0-9 - _ . ! ~ * ' ( )
        """
        return urllib.parse.quote(s, safe="~-_.!~*'()")

    def __ascii_downcase(self, text:str) -> str:
        return ''.join(c.lower() if c.isascii() else c for c in text)

    def __add_current_heading(self):
        """
        https://github.com/gjtorikian/html-pipeline/blob/f13a1534cb650ba17af400d1acd3a22c28004c09/lib/html/pipeline/toc_filter.rb#L30
        """

        converted_heading = self.__ascii_downcase(self.__current_heading) if self.__ignore_case else self.__current_heading
        converted_heading = RuleMd051.__PUNCTUATION_REGEXP.sub('', converted_heading)
        converted_heading = converted_heading.replace(' ', '-')

        count = self.__present_headings.get(converted_heading, 0)
        unique_suffix = f"-{count}" if count > 0 else ''
        unique_heading = self.__encodeURIComponent(converted_heading + unique_suffix)

        self.__present_headings[converted_heading] = count + 1
        self.__available_headings.add(unique_heading)
        self.__current_heading = ""

    def __handle_raw_html(self, raw_token:RawHtmlMarkdownToken):
        parser = MyHTMLParser()
        x = f"<{raw_token.extra_data}>"
        parser.feed(x)
        parser.close()
        for i in parser.valid_targets:
            self.__current_heading = i
            self.__add_current_heading()

    def __handle_html_block(self):
        parser = MyHTMLParser()
        parser.feed(self.__current_heading)
        parser.close()
        for i in parser.valid_targets:
            self.__current_heading = i
            self.__add_current_heading()
        self.__current_heading = ""

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if self.__heading_state == RuleMd051States.LOOK_FOR_LINKS_OR_HEADINGS:
            if token.is_atx_heading:
                self.__heading_state = RuleMd051States.LOOK_FOR_ATX_END
            elif token.is_setext_heading:
                self.__heading_state = RuleMd051States.LOOK_FOR_SETEXT_END
            elif token.is_inline_raw_html:
                self.__handle_raw_html(cast(RawHtmlMarkdownToken, token))
            elif token.is_html_block:
                self.__heading_state = RuleMd051States.LOOK_FOR_HTML_BLOCK_END
            elif token.is_inline_link:
                link_token = cast(LinkStartMarkdownToken, token)
                if link_token.link_uri.startswith("#"):
                    self.__link_tokens.append(link_token)

        elif self.__heading_state == RuleMd051States.LOOK_FOR_ATX_END:
            if token.is_atx_heading_end:
                self.__add_current_heading()
                self.__heading_state = RuleMd051States.LOOK_FOR_LINKS_OR_HEADINGS
            elif token.is_text:
                text_token = cast(TextMarkdownToken, token)
                self.__current_heading += text_token.token_text
        elif self.__heading_state == RuleMd051States.LOOK_FOR_SETEXT_END:
            if token.is_setext_heading_end:
                self.__heading_state = RuleMd051States.LOOK_FOR_LINKS_OR_HEADINGS
        elif self.__heading_state == RuleMd051States.LOOK_FOR_HTML_BLOCK_END:
            if token.is_html_block_end:
                self.__handle_html_block()
                self.__heading_state = RuleMd051States.LOOK_FOR_LINKS_OR_HEADINGS
            elif token.is_text:
                text_token = cast(TextMarkdownToken, token)
                self.__current_heading += text_token.token_text
