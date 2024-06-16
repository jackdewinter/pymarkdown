"""
Module to implement a plugin that ensures the code blocks maintain a consistent style.
"""

from typing import List, Optional, Tuple, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.plugin_manager.plugin_details import (
    PluginDetails,
    PluginDetailsV3,
    QueryConfigItem,
)
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin
from pymarkdown.tokens.blank_line_markdown_token import BlankLineMarkdownToken
from pymarkdown.tokens.fenced_code_block_markdown_token import (
    FencedCodeBlockMarkdownToken,
)
from pymarkdown.tokens.indented_code_block_markdown_token import (
    IndentedCodeBlockMarkdownToken,
)
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.text_markdown_token import TextMarkdownToken


class RuleMd046(RulePlugin):
    """
    Class to implement a plugin that ensures the code blocks maintain a consistent style.
    """

    __consistent_style = "consistent"
    __fenced_style = "fenced"
    __indented_style = "indented"
    __valid_styles = [
        __consistent_style,
        __fenced_style,
        __indented_style,
    ]

    def __init__(self) -> None:
        super().__init__()
        self.__style_type: str = ""
        self.__actual_style_type: str = ""
        self.__start_fix_token: Optional[MarkdownToken] = None
        self.__inner_fix_token: Optional[MarkdownToken] = None
        self.__token_before_start_fix_token: Optional[MarkdownToken] = None
        self.__last_token: Optional[MarkdownToken] = None

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetailsV3(
            plugin_name="code-block-style",
            plugin_id="MD046",
            plugin_enabled_by_default=True,
            plugin_description="Code block style",
            plugin_version="0.7.0",
            plugin_url="https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md046.md",
            plugin_configuration="style",
            plugin_supports_fix=True,
        )

    @classmethod
    def __validate_configuration_style(cls, found_value: str) -> None:
        if found_value not in RuleMd046.__valid_styles:
            raise ValueError(f"Allowable values: {RuleMd046.__valid_styles}")

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        self.__style_type = self.plugin_configuration.get_string_property(
            "style",
            default_value=RuleMd046.__consistent_style,
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
            if self.__style_type != RuleMd046.__consistent_style
            else ""
        )
        self.__last_token = None
        self.__start_fix_token = None
        self.__inner_fix_token = None

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if self.__start_fix_token:
            if token.is_end_token:
                end_token = cast(EndMarkdownToken, token)
                assert end_token.start_markdown_token == self.__start_fix_token
                self.__fix(context, end_token)
                self.__token_before_start_fix_token = None
                self.__start_fix_token = None
                self.__inner_fix_token = None
            else:
                assert (
                    token.is_text
                ), "Once into a code block, should either be a text token or an end token."
                assert self.__inner_fix_token is None
                self.__inner_fix_token = token
        elif token.is_code_block:
            current_style = (
                RuleMd046.__fenced_style
                if token.is_fenced_code_block
                else RuleMd046.__indented_style
            )
            if not self.__actual_style_type:
                self.__actual_style_type = current_style
            if self.__actual_style_type != current_style:
                if context.in_fix_mode:
                    self.__start_fix_token = token
                    self.__token_before_start_fix_token = self.__last_token
                else:
                    extra_data = (
                        f"Expected: {self.__actual_style_type}; Actual: {current_style}"
                    )
                    self.report_next_token_error(
                        context, token, extra_error_information=extra_data
                    )
        self.__last_token = token

    def __create_new_fenced_tokens(
        self,
    ) -> Tuple[List[MarkdownToken], EndMarkdownToken]:
        collected_count = 3
        new_fenced_start_token = FencedCodeBlockMarkdownToken(
            fence_character="`",
            fence_count=collected_count,
            extracted_text="",
            pre_extracted_text="",
            text_after_extracted_text="",
            pre_text_after_extracted_text="",
            extracted_whitespace="",
            extracted_whitespace_before_info_string="",
            position_marker=PositionMarker(0, 0, ""),
        )
        extracted_spaces = ""
        extra_end_data = f"{extracted_spaces}:{collected_count}"
        new_end_token = EndMarkdownToken(
            new_fenced_start_token.token_name,
            extracted_whitespace="",
            extra_end_data=extra_end_data,
            start_markdown_token=new_fenced_start_token,
            was_forced=False,
        )
        replacement_tokens: List[MarkdownToken] = [new_fenced_start_token]
        return replacement_tokens, new_end_token

    def __create_new_indented_tokens(
        self,
    ) -> Tuple[List[MarkdownToken], EndMarkdownToken]:
        new_indented_start_token = IndentedCodeBlockMarkdownToken(
            extracted_whitespace="    ", line_number=0, column_number=0
        )
        new_end_token = EndMarkdownToken(
            new_indented_start_token.token_name,
            extracted_whitespace="",
            extra_end_data=None,
            start_markdown_token=new_indented_start_token,
            was_forced=False,
        )

        if self.__inner_fix_token:
            inner_text_token = cast(TextMarkdownToken, self.__inner_fix_token)
            newlines_in_inner_text_token = ParserHelper.count_newlines_in_text(
                inner_text_token.token_text
            )
            for _ in range(newlines_in_inner_text_token):
                new_indented_start_token.add_indented_whitespace("    ")
        replacement_tokens = [cast(MarkdownToken, new_indented_start_token)]
        return replacement_tokens, new_end_token

    def __fix(self, context: PluginScanContext, end_fix_token: MarkdownToken) -> None:
        if self.__actual_style_type == RuleMd046.__fenced_style:
            replacement_tokens, new_end_token = self.__create_new_fenced_tokens()
        else:
            replacement_tokens, new_end_token = self.__create_new_indented_tokens()

        if self.__inner_fix_token:
            replacement_tokens.append(self.__inner_fix_token)
        replacement_tokens.append(new_end_token)

        if (
            self.__actual_style_type == RuleMd046.__indented_style
            and self.__token_before_start_fix_token
            and self.__token_before_start_fix_token.is_paragraph_end
        ):
            replacement_tokens.insert(
                0,
                BlankLineMarkdownToken(
                    extracted_whitespace="", position_marker=PositionMarker(0, 0, "")
                ),
            )

        assert self.__start_fix_token is not None
        self.register_replace_tokens_request(
            context, self.__start_fix_token, end_fix_token, replacement_tokens
        )
        self.__start_fix_token = None
        self.__inner_fix_token = None
