"""
Module to provide for an encapsulation of the text element.
"""

import logging
from typing import List, Optional, Tuple, Union, cast

from typing_extensions import override

from pymarkdown.general.constants import Constants
from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.indented_code_block_markdown_token import (
    IndentedCodeBlockMarkdownToken,
)
from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)

POGGER = ParserLogger(logging.getLogger(__name__))


class TextMarkdownToken(InlineMarkdownToken):
    """
    Class to provide for an encapsulation of the text element.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        token_text: str,
        extracted_whitespace: str,
        end_whitespace: Optional[str] = None,
        position_marker: Optional[PositionMarker] = None,
        line_number: int = 0,
        column_number: int = 0,
        is_special: bool = False,
        tabified_text: Optional[str] = None,
    ):
        (
            self.__token_text,
            self.__extracted_whitespace,
            self.__end_whitespace,
            self.__tabified_text,
        ) = (token_text, extracted_whitespace, end_whitespace, tabified_text)
        InlineMarkdownToken.__init__(
            self,
            MarkdownToken._token_text,
            "",
            position_marker=position_marker,
            line_number=line_number,
            column_number=column_number,
            is_special=is_special,
        )
        self.__compose_extra_data_field()

    # pylint: enable=too-many-arguments
    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_text

    # pylint: enable=protected-access

    def _set_token_text(self, new_text: str) -> None:
        self.__token_text = new_text
        self.__compose_extra_data_field()

    @property
    def token_text(self) -> str:
        """
        Returns the text associated with the token.
        """
        return self.__token_text

    @property
    def extracted_whitespace(self) -> str:
        """
        Returns any whitespace that was extracted before the processing of this element occurred.
        """
        return self.__extracted_whitespace

    @property
    def end_whitespace(self) -> Optional[str]:
        """
        Returns any whitespace that was extracted after the processing of this element occurred.
        """
        return self.__end_whitespace

    @property
    def tabified_text(self) -> Optional[str]:
        """
        Returns any text that had a tab character in it.
        """
        return self.__tabified_text

    def create_copy(self) -> "TextMarkdownToken":
        """
        Create a copy of this token.
        """
        return TextMarkdownToken(
            self.__token_text,
            self.__extracted_whitespace,
            self.__end_whitespace,
            line_number=self.line_number,
            column_number=self.column_number,
        )

    @override
    def _modify_token(self, field_name: str, field_value: Union[str, int]) -> bool:
        if field_name == "token_text" and isinstance(field_value, str):
            self.__token_text = field_value
            self.__compose_extra_data_field()

            return True
        if field_name == "end_whitespace" and isinstance(field_value, str):
            self.__end_whitespace = field_value
            self.__compose_extra_data_field()

            return True
        return False

    def __compose_extra_data_field(self) -> None:
        """
        Compose the object's self.extra_data field from the local object's variables.
        """

        data_field_parts = [self.__token_text, self.__extracted_whitespace]
        if self.__end_whitespace:
            data_field_parts.append(self.__end_whitespace)
            assert not self.__tabified_text
        elif self.__tabified_text:
            data_field_parts.extend(("", self.__tabified_text))
        self._set_extra_data(MarkdownToken.extra_data_separator.join(data_field_parts))

    def remove_final_whitespace(self) -> str:
        """
        Remove any final whitespace.  Used by paragraph blocks so that they do not
        end with a hard break.
        """

        removed_whitespace = ""
        # POGGER.debug("self.__tabified_text=:$:", self.__tabified_text)
        # POGGER.debug("self.__token_text=:$:", self.__token_text)
        (
            collected_whitespace_length,
            first_non_whitespace_index,
        ) = ParserHelper.collect_backwards_while_one_of_characters(
            self.__token_text, -1, Constants.ascii_whitespace
        )
        # POGGER.debug("collected_whitespace_length=:$:", collected_whitespace_length)
        # POGGER.debug("first_non_whitespace_index=:$:", first_non_whitespace_index)

        assert first_non_whitespace_index is not None
        if collected_whitespace_length:
            removed_whitespace = self.__token_text[
                first_non_whitespace_index : first_non_whitespace_index
                + collected_whitespace_length
            ]
            self.__token_text = self.__token_text[:first_non_whitespace_index]
            if self.__tabified_text:
                (
                    collected_whitespace_length,
                    first_non_whitespace_index,
                ) = ParserHelper.collect_backwards_while_one_of_characters(
                    self.__tabified_text, -1, Constants.ascii_whitespace
                )
                # POGGER.debug("collected_whitespace_length=:$:", collected_whitespace_length)
                # POGGER.debug("first_non_whitespace_index=:$:", first_non_whitespace_index)
                assert collected_whitespace_length is not None
                assert first_non_whitespace_index is not None
                removed_whitespace = self.__tabified_text[
                    first_non_whitespace_index : first_non_whitespace_index
                    + collected_whitespace_length
                ]
                self.__tabified_text = self.__tabified_text[:first_non_whitespace_index]
        self.__compose_extra_data_field()
        return removed_whitespace

    def combine(
        self, other_text_token: MarkdownToken, remove_leading_spaces: int
    ) -> str:
        """
        Combine the two text tokens together with a line feed between.
        If remove_leading_spaces > 0, then that many leading spaces will be
        removed from each line, if present.
        If remove_leading_spaces == -1, then.
        If remove_leading_spaces == 0, then.
        """

        if other_text_token.is_blank_line:
            text_to_combine = ""
            tabified_text_to_combine: Optional[str] = ""
            (
                whitespace_present,
                blank_line_sequence,
            ) = (
                other_text_token.extra_data,
                ParserHelper.replace_noop_character,
            )
        else:
            assert other_text_token.is_text
            text_other_token = cast(TextMarkdownToken, other_text_token)

            text_to_combine = text_other_token.token_text
            tabified_text_to_combine = text_other_token.tabified_text
            (
                whitespace_present,
                blank_line_sequence,
            ) = (
                text_other_token.extracted_whitespace,
                "",
            )

        removed_whitespace, prefix_whitespace = self.__combine_handle_whitespace(
            remove_leading_spaces, whitespace_present
        )

        if self.__tabified_text or tabified_text_to_combine:
            other_token_text = tabified_text_to_combine or text_to_combine

            this_token_text = self.__tabified_text or self.__token_text
            # POGGER.debug("this_token_text>:$:<", this_token_text)
            # POGGER.debug("blank_line_sequence>:$:<", blank_line_sequence)
            # POGGER.debug("prefix_whitespace>:$:<", prefix_whitespace)
            # POGGER.debug("other_token_text>:$:<", other_token_text)

            self.__tabified_text = (
                f"{this_token_text}{ParserHelper.newline_character}{blank_line_sequence}"
                + f"{prefix_whitespace}{other_token_text}"
            )
        self.__token_text = (
            f"{self.__token_text}{ParserHelper.newline_character}{blank_line_sequence}"
            + f"{prefix_whitespace}{text_to_combine}"
        )
        self.__compose_extra_data_field()
        return removed_whitespace

    def __combine_handle_whitespace(
        self, remove_leading_spaces: int, whitespace_present: Optional[str]
    ) -> Tuple[str, str]:
        prefix_whitespace = ""
        whitespace_to_append, removed_whitespace = None, ""
        if not remove_leading_spaces:
            assert whitespace_present is not None
            prefix_whitespace = whitespace_present
        elif remove_leading_spaces == -1:
            whitespace_to_append, prefix_whitespace = whitespace_present, ""
        else:
            assert whitespace_present is not None
            whitespace_present_size = len(whitespace_present)
            POGGER.debug(
                "whitespace_present>>$>>$<<",
                whitespace_present_size,
                whitespace_present,
            )
            POGGER.debug("remove_leading_spaces>>$<<", remove_leading_spaces)
            if whitespace_present_size < remove_leading_spaces:
                removed_whitespace, prefix_whitespace = whitespace_present, ""
            else:
                removed_whitespace, prefix_whitespace = (
                    whitespace_present[:remove_leading_spaces],
                    whitespace_present[remove_leading_spaces:],
                )

        if whitespace_to_append is not None:
            self.__extracted_whitespace = (
                f"{self.__extracted_whitespace}"
                + f"{ParserHelper.newline_character}{whitespace_to_append}"
            )
        return removed_whitespace, prefix_whitespace

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            TextMarkdownToken,
            TextMarkdownToken.__rehydrate_text,
            None,
        )

    @staticmethod
    def __rehydrate_text(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the text from the token.
        """
        _ = previous_token

        if (
            context.block_stack[-1].is_inline_link
            or context.block_stack[-1].is_inline_image
        ):
            return ""

        prefix_text = ""
        current_text_token = cast(TextMarkdownToken, current_token)
        POGGER.debug(
            f">>rehydrate_text>>:{ParserHelper.make_value_visible(current_text_token.token_text)}:<<"
        )
        # main_text = ParserHelper.resolve_noops_from_text(current_text_token.token_text)
        main_text = ParserHelper.remove_all_from_text(
            current_text_token.token_text, include_noops=True
        )

        POGGER.debug(f"<<rehydrate_text>>{ParserHelper.make_value_visible(main_text)}")

        POGGER.debug(
            f">>leading_whitespace>>:{ParserHelper.make_value_visible(current_text_token.extracted_whitespace)}:<<"
        )
        leading_whitespace = ParserHelper.remove_all_from_text(
            current_text_token.extracted_whitespace
        )
        POGGER.debug(
            f"<<leading_whitespace>>:{ParserHelper.make_value_visible(leading_whitespace)}:<<"
        )

        extra_line = ""
        assert context.block_stack
        if context.block_stack[-1].is_indented_code_block:
            code_block_token = cast(
                IndentedCodeBlockMarkdownToken, context.block_stack[-1]
            )
            (
                main_text,
                prefix_text,
                leading_whitespace,
            ) = TextMarkdownToken.__reconstitute_indented_text(
                main_text,
                code_block_token.extracted_whitespace,
                code_block_token.indented_whitespace,
                leading_whitespace,
            )
        elif context.block_stack[-1].is_html_block:
            extra_line = ParserHelper.newline_character
        elif context.block_stack[-1].is_paragraph:
            main_text = TextMarkdownToken.__reconstitute_paragraph_text(
                context, main_text, current_text_token
            )
        elif context.block_stack[-1].is_setext_heading:
            main_text = TextMarkdownToken.__reconstitute_setext_text(
                main_text, current_text_token
            )

        POGGER.debug(
            f"<<prefix_text>>{ParserHelper.make_value_visible(prefix_text)}"
            + f"<<leading_whitespace>>{ParserHelper.make_value_visible(leading_whitespace)}"
            + f"<<main_text>>{ParserHelper.make_value_visible(main_text)}<<"
        )
        return "".join([prefix_text, leading_whitespace, main_text, extra_line])

    @staticmethod
    def __reconstitute_paragraph_text(
        context: MarkdownTransformContext,
        main_text: str,
        current_token: "TextMarkdownToken",
    ) -> str:
        """
        For a paragraph block, figure out the text that got us here.
        """
        if ParserHelper.newline_character in main_text:
            owner_paragraph_token = cast(
                ParagraphMarkdownToken, context.block_stack[-1]
            )
            (
                main_text,
                owner_paragraph_token.rehydrate_index,
            ) = ParserHelper.recombine_string_with_whitespace(
                main_text,
                owner_paragraph_token.extracted_whitespace,
                owner_paragraph_token.rehydrate_index,
            )
            assert current_token.end_whitespace
            main_text, _ = ParserHelper.recombine_string_with_whitespace(
                main_text,
                current_token.end_whitespace,
                start_text_index=0,
                post_increment_index=True,
                add_whitespace_after=True,
            )
        return main_text

    @staticmethod
    def __reconstitute_indented_text(
        main_text: str,
        prefix_text: str,
        indented_whitespace: str,
        leading_whitespace: str,
    ) -> Tuple[str, str, str]:
        """
        For an indented code block, figure out the text that got us here.
        """
        recombined_text, _ = ParserHelper.recombine_string_with_whitespace(
            main_text,
            f"{prefix_text}{leading_whitespace}{indented_whitespace}",
            start_text_index=0,
            post_increment_index=True,
        )
        return f"{recombined_text}{ParserHelper.newline_character}", "", ""

    @staticmethod
    def __reconstitute_setext_text_item(
        text_part_index: int,
        text_part_value: str,
        rejoined_token_text: List[str],
        split_parent_whitespace_text: List[str],
    ) -> None:
        ws_prefix_text = ""
        ws_suffix_text = ""
        if split_parent_whitespace_text[text_part_index]:
            split_setext_text = split_parent_whitespace_text[text_part_index].split(
                ParserHelper.whitespace_split_character
            )
            split_setext_text_size = len(split_setext_text)
            if split_setext_text_size == 1:
                assert text_part_index == 0
                ws_suffix_text = split_setext_text[0]
                # if text_part_index == 0:
                #     ws_suffix_text = split_setext_text[0]
                # else:
                #     ws_prefix_text = split_setext_text[0]
            else:
                assert split_setext_text_size == 2
                ws_prefix_text = split_setext_text[0]
                ws_suffix_text = split_setext_text[1]

        rejoined_token_text.append(
            "".join([ws_prefix_text, text_part_value, ws_suffix_text])
        )

    @staticmethod
    def __reconstitute_setext_text(
        main_text: str, current_token: "TextMarkdownToken"
    ) -> str:
        """
        For a setext heading block, figure out the text that got us here.

        Because of the unique formatting of the setext data, the recombine_string_with_whitespace
        function cannot be used for this.
        """

        if ParserHelper.newline_character in main_text:
            split_token_text = main_text.split(ParserHelper.newline_character)
            assert current_token.end_whitespace is not None
            split_parent_whitespace_text = current_token.end_whitespace.split(
                ParserHelper.newline_character
            )

            rejoined_token_text: List[str] = []
            for text_part_index, text_part_value in enumerate(split_token_text):
                TextMarkdownToken.__reconstitute_setext_text_item(
                    text_part_index,
                    text_part_value,
                    rejoined_token_text,
                    split_parent_whitespace_text,
                )

            main_text = ParserHelper.newline_character.join(rejoined_token_text)
        else:
            POGGER.debug(f"main_text>>{ParserHelper.make_value_visible(main_text)}")
            POGGER.debug(
                f"current_token>>{ParserHelper.make_value_visible(current_token)}"
            )
            if current_token.end_whitespace and current_token.end_whitespace.endswith(
                ParserHelper.whitespace_split_character
            ):
                main_text = f"{current_token.end_whitespace[:-1]}{main_text}"
        return main_text

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            TextMarkdownToken, TextMarkdownToken.__handle_text_token, None
        )

    @staticmethod
    def __handle_text_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        """
        Handle the text token.
        """
        text_token = cast(TextMarkdownToken, next_token)
        adjusted_text_token = ParserHelper.resolve_all_from_text(text_token.token_text)

        token_parts: List[str] = []
        if transform_state.is_in_code_block:
            POGGER.debug(
                "text_token.extracted_whitespace>:$:<", text_token.extracted_whitespace
            )
            leading_space = ParserHelper.resolve_all_from_text(
                text_token.extracted_whitespace
            )

            POGGER.debug("leading_space>:$:<", leading_space)
            POGGER.debug("adjusted_text_token>:$:<", adjusted_text_token)
            token_parts.extend(
                [
                    leading_space,
                    adjusted_text_token,
                ]
            )
        elif transform_state.is_in_html_block:
            POGGER.debug(
                "text_token.extracted_whitespace>:$:<", text_token.extracted_whitespace
            )
            leading_space = ParserHelper.resolve_all_from_text(
                text_token.extracted_whitespace
            )

            POGGER.debug("leading_space>:$:<", leading_space)
            POGGER.debug("adjusted_text_token>:$:<", adjusted_text_token)
            POGGER.debug("newline_character>:$:<", ParserHelper.newline_character)
            token_parts.extend(
                [
                    leading_space,
                    adjusted_text_token,
                    ParserHelper.newline_character,
                ]
            )
        elif transform_state.is_in_setext_block:
            token_parts.append(adjusted_text_token)
        else:
            TextMarkdownToken.__handle_text_token_normal(
                token_parts, text_token, adjusted_text_token
            )

        token_parts.insert(0, output_html)
        return "".join(token_parts)

    @staticmethod
    def __handle_text_token_normal(
        token_parts: List[str],
        text_token: "TextMarkdownToken",
        adjusted_text_token: str,
    ) -> None:
        POGGER.debug("adjusted_text_token>:$:<", adjusted_text_token)
        POGGER.debug("text_token.end_whitespace>:$:<", text_token.end_whitespace)
        if text_token.end_whitespace is not None:
            newlines_in_adjusted = ParserHelper.count_newlines_in_text(
                adjusted_text_token
            )

            resolved_whitespace = ParserHelper.resolve_all_from_text(
                text_token.end_whitespace
            )
            POGGER.debug("resolved_whitespace>:$:<", resolved_whitespace)
            newlines_in_whitespace = ParserHelper.count_newlines_in_text(
                resolved_whitespace
            )
            arrays_to_combine: List[List[str]] = []
            if newlines_in_adjusted == newlines_in_whitespace:
                arrays_to_combine.append(adjusted_text_token.split("\n"))
            else:
                TextMarkdownToken.__handle_text_token_normal_enhanced(
                    arrays_to_combine, text_token
                )

            arrays_to_combine.append(resolved_whitespace.split("\n"))
            assert len(arrays_to_combine[0]) == len(arrays_to_combine[1])
            POGGER.debug("arrays_to_combine>:$:<", arrays_to_combine)
            final_parts: List[str] = []
            for loop_index in range(len(arrays_to_combine[0]) * 2):
                loop_index_mod = loop_index % 2
                loop_index_div = loop_index // 2
                if loop_index_mod == 0 and final_parts:
                    final_parts.append("\n")
                POGGER.debug(
                    "$-->final_parts>:$:<...$,$",
                    loop_index,
                    final_parts,
                    loop_index_mod,
                    loop_index_div,
                )
                final_parts.append(arrays_to_combine[loop_index_mod][loop_index_div])
                POGGER.debug("final_parts>:$:<", final_parts)
            adjusted_text_token = "".join(final_parts)
        token_parts.append(adjusted_text_token)

    @staticmethod
    def __handle_text_token_normal_enhanced(
        arrays_to_combine: List[List[str]], text_token: "TextMarkdownToken"
    ) -> None:
        """
        This should only happen in the case where there are replacement characters that
        include replacing a character sequence with a newline.  Specifically target that.
        """

        assert "\a" in text_token.token_text
        replace_character_count = ParserHelper.count_characters_in_text(
            text_token.token_text, "\a"
        )
        assert replace_character_count % 3 == 0

        start_index = 0
        current_line = ""
        processed_lines: List[str] = []
        next_index, found_prefix = ParserHelper.collect_until_one_of_characters(
            text_token.token_text, start_index, "\a\n"
        )
        assert next_index is not None
        assert found_prefix is not None
        # POGGER.debug("next_index>:$:<", next_index)
        # POGGER.debug("found_prefix>:$:<", found_prefix)
        while next_index < len(text_token.token_text):
            current_line += found_prefix
            if text_token.token_text[next_index] == "\a":
                # POGGER.debug("before>:$:<", text_token.token_text[start_index:next_index])
                middle_index = text_token.token_text.find("\a", next_index + 1)
                # POGGER.debug("replace>:$:<", text_token.token_text[next_index+1:middle_index])
                start_index = text_token.token_text.find("\a", middle_index + 1)
                # POGGER.debug("with>:$:<", text_token.token_text[middle_index+1:start_index])
                current_line += text_token.token_text[middle_index + 1 : start_index]
            else:
                processed_lines.append(current_line)
                current_line = ""
                start_index = next_index
            next_index, found_prefix = ParserHelper.collect_until_one_of_characters(
                text_token.token_text, start_index + 1, "\a\n"
            )
            assert next_index is not None
            assert found_prefix is not None
            # POGGER.debug("next_index>:$:<", next_index)
            # POGGER.debug("found_prefix>:$:<", found_prefix)
        current_line += found_prefix

        # POGGER.debug("currernt_line>:$:<", current_line)
        assert current_line
        processed_lines.append(current_line)

        arrays_to_combine.append(processed_lines)
