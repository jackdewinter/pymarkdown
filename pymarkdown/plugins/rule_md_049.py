"""
Module to implement a plugin that ensures that the style of emphasis is consistent.
"""

from typing import List, Optional, Tuple, cast

from pymarkdown.general.constants import Constants
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetailsV2,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.emphasis_markdown_token import EmphasisMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.reference_markdown_token import ReferenceMarkdownToken


class RuleMd049(RulePlugin):
    """
    Class to implement a plugin that ensures that the style of emphasis is consistent.
    """

    __PLUGIN_ID = "MD049"

    __consistent_style = "consistent"
    __asterisk_style = "asterisk"
    __underscore_style = "underscore"
    __valid_styles = [
        __consistent_style,
        __asterisk_style,
        __underscore_style,
    ]

    def __init__(self) -> None:
        """
        Initialize an instance of the RuleMd048 class.
        """
        super().__init__()
        self.__style_type: str = ""
        self.__actual_style_type: str = ""
        self.__inline_link_token: Optional[ReferenceMarkdownToken] = None
        self.__inline_link_text: Optional[str] = None
        self.__open_emphasis: Optional[Tuple[EmphasisMarkdownToken, str]] = None

    def get_details(self) -> PluginDetailsV2:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="emphasis-style",
            plugin_id="MD049",
            plugin_enabled_by_default=True,
            plugin_description="Emphasis style",
            plugin_version="0.6.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md049.md",
            plugin_configuration="style",
            plugin_supports_fix=True,
            plugin_fix_level=2,
        )

    @classmethod
    def __validate_configuration_style(cls, found_value: str) -> None:
        if found_value not in RuleMd049.__valid_styles:
            raise ValueError(f"Allowable values: {RuleMd049.__valid_styles}")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__style_type = self.plugin_configuration.get_string_property_with_default(
            "style",
            RuleMd049.__consistent_style,
            valid_value_fn=self.__validate_configuration_style,
        )

    def query_config(self) -> List[QueryConfigItem]:
        """
        Query to find out the configuration that the rule is using.
        """
        return [
            QueryConfigItem("style", self.__style_type),
        ]

    def starting_new_file(self) -> None:
        """
        Event that the a new file to be scanned is starting.
        """
        self.__actual_style_type = (
            self.__style_type
            if self.__style_type != RuleMd049.__consistent_style
            else ""
        )
        self.__inline_link_token: Optional[ReferenceMarkdownToken] = None
        self.__inline_link_text: Optional[str] = None
        self.__open_emphasis: Optional[Tuple[EmphasisMarkdownToken, str]] = None

    def __swap_delimiter_in_link_text(
        self,
        emphasis_token: EmphasisMarkdownToken,
        close_column_number: int,
        replace_character: str,
    ) -> Optional[str]:
        """
        Return the enclosing link's label text with this span's delimiters swapped.

        The label text of an inline link is cached verbatim on the link token and
        rehydrated from that cache, so the emphasis token's own delimiter never
        reaches the output.  The delimiters have to be rewritten in the cache
        instead.  Returns None when the span cannot be located unambiguously in
        the cache, in which case the caller leaves the document alone.
        """
        assert self.__inline_link_token is not None
        link_text = self.__inline_link_text
        if link_text is None:
            return None

        # The cache is the label as it appeared in the source, so a column offset
        # maps straight onto it -- but only when the label was not shortened or
        # rewritten on the way in.
        if self.__inline_link_token.label_type != Constants.link_type__inline:
            return None

        start_column = emphasis_token.column_number
        close_column = close_column_number
        link_column = self.__inline_link_token.column_number
        start_offset, close_offset = (
            start_column - link_column - 1,
            close_column - link_column - 1,
        )
        if (
            start_offset < 0
            or close_offset < start_offset
            or close_offset >= len(link_text)
            or start_offset >= len(link_text)
        ):
            return None
        if (
            link_text[start_offset] != emphasis_token.emphasis_character
            or link_text[close_offset] != emphasis_token.emphasis_character
        ):
            return None

        return (
            link_text[:start_offset]
            + replace_character
            + link_text[start_offset + 1 : close_offset]
            + replace_character
            + link_text[close_offset + 1 :]
        )

    @staticmethod
    def __is_word_character(character: str) -> bool:
        """
        Is the character something an underscore delimiter can sit against?

        Underscore emphasis may not split a word, so a delimiter that has a
        word character on both sides stops being emphasis.  Whitespace and
        punctuation are safe on either side.
        """
        return not Constants.unicode_whitespace.contains(
            character
        ) and not Constants.punctuation_characters.contains(character)

    @classmethod
    def __underscore_emphasis_survives(
        cls, emphasis_token: EmphasisMarkdownToken
    ) -> bool:
        """
        Would replacing this span's delimiters with underscores keep it emphasis?

        Without the neighbouring source characters there is nothing to check
        against, so the answer is yes and the caller fixes as before.
        """
        preceding_character = emphasis_token.preceding_character
        following_character = emphasis_token.following_character
        if preceding_character is None or following_character is None:
            return True
        return not (
            cls.__is_word_character(preceding_character)
            or cls.__is_word_character(following_character)
        )

    def __track_inline_link(self, token: MarkdownToken) -> bool:
        """
        Track the label of an inline link, whose text is rewritten in place.
        """
        if token.is_inline_link_end:
            self.__inline_link_token, self.__inline_link_text = None, None
            return True
        if token.is_inline_link:
            self.__inline_link_token = cast(ReferenceMarkdownToken, token)
            self.__inline_link_text = self.__inline_link_token.text_from_blocks
            return True
        return False

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if self.__track_inline_link(token):
            return

        if token.is_end_token:
            end_token = cast(EndMarkdownToken, token)
            open_emphasis = self.__open_emphasis
            if (
                open_emphasis is None
                or open_emphasis[0] is not end_token.start_markdown_token
            ):
                return
            self.__open_emphasis = None
            self.__finish_emphasis(
                context, open_emphasis[0], open_emphasis[1], end_token.column_number
            )
            return

        if not token.is_inline_emphasis:
            return

        emphasis_token = cast(EmphasisMarkdownToken, token)
        if emphasis_token.emphasis_length != 1:
            return

        if emphasis_token.emphasis_character == "*":
            current_style = RuleMd049.__asterisk_style
        elif emphasis_token.emphasis_character == "_":
            current_style = RuleMd049.__underscore_style
        else:
            return

        if not self.__actual_style_type:
            self.__actual_style_type = current_style
        if self.__actual_style_type != current_style:
            if context.in_fix_mode:
                replace_character = (
                    "*"
                    if self.__actual_style_type == RuleMd049.__asterisk_style
                    else "_"
                )
                self.__open_emphasis = (emphasis_token, replace_character)
            else:
                extra_data = (
                    f"Expected: {self.__actual_style_type}; Actual: {current_style}"
                )
                self.report_next_token_error(
                    context, token, extra_error_information=extra_data
                )

    def __finish_emphasis(
        self,
        context: PluginScanContext,
        emphasis_token: EmphasisMarkdownToken,
        replace_character: str,
        close_column_number: int,
    ) -> None:
        """
        Register the fix for a span once its closer position is known.
        """
        if context.check_for_pragma_suppression(
            emphasis_token.line_number, RuleMd049.__PLUGIN_ID, False
        ):
            return

        if (
            self.__actual_style_type == RuleMd049.__underscore_style
            and not self.__underscore_emphasis_survives(emphasis_token)
        ):
            return

        if self.__inline_link_token is not None:
            new_link_text = self.__swap_delimiter_in_link_text(
                emphasis_token, close_column_number, replace_character
            )
            if new_link_text is None:
                return
            self.__inline_link_text = new_link_text
            self.register_fix_token_request(
                context,
                self.__inline_link_token,
                "next_token",
                "text_from_blocks",
                new_link_text,
            )
            return

        self.register_fix_token_request(
            context,
            emphasis_token,
            "next_token",
            "emphasis_character",
            replace_character,
        )
