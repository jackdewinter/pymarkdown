"""
Module to provide for an element that can be added to the stack.
"""

from typing import Any, List, Optional

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.tokens.block_quote_markdown_token import BlockQuoteMarkdownToken
from pymarkdown.tokens.container_markdown_token import ContainerMarkdownToken
from pymarkdown.tokens.fenced_code_block_markdown_token import (
    FencedCodeBlockMarkdownToken,
)
from pymarkdown.tokens.html_block_markdown_token import HtmlBlockMarkdownToken
from pymarkdown.tokens.indented_code_block_markdown_token import (
    IndentedCodeBlockMarkdownToken,
)
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.new_list_item_markdown_token import NewListItemMarkdownToken
from pymarkdown.tokens.ordered_list_start_markdown_token import (
    OrderedListStartMarkdownToken,
)
from pymarkdown.tokens.paragraph_markdown_token import ParagraphMarkdownToken
from pymarkdown.tokens.unordered_list_start_markdown_token import (
    UnorderedListStartMarkdownToken,
)


class StackToken:
    """
    Class to provide for an element to place on the stack.
    """

    _stack_base_document = "document"
    _stack_unordered_list = "ulist"
    _stack_ordered_list = "olist"
    _stack_html_block = "html-block"
    _stack_block_quote = "block-quote"
    _stack_fenced_code = "fcode-block"
    _stack_indented_code = "icode-block"
    _stack_paragraph = "para"
    _stack_link_definition = "linkdef"
    _stack_table_rows = "table-rows"

    def __init__(
        self,
        type_name: str,
        matching_markdown_token: Optional[MarkdownToken] = None,
        extra_data: Optional[str] = None,
    ) -> None:
        self.__type_name, self.__extra_data, self.__matching_markdown_token = (
            type_name,
            extra_data,
            matching_markdown_token,
        )

    def __str__(self) -> str:
        add_extra = f":{self.extra_data}" if self.extra_data else ""
        return f"StackToken({self.type_name}{add_extra})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: Any) -> bool:
        """
        Overrides the default implementation
        """
        assert isinstance(other, StackToken), "Cover other objects."
        return self.type_name == other.type_name and self.extra_data == other.extra_data

    @property
    def type_name(self) -> str:
        """
        Returns the type name associated with this stack token.
        """
        return self.__type_name

    @property
    def extra_data(self) -> Optional[str]:
        """
        Returns the extra data associated with this stack token.
        """
        return self.__extra_data

    @property
    def matching_markdown_token(self) -> Optional[MarkdownToken]:
        """
        Returns the matching markdown associated with this stack token.
        """
        return self.__matching_markdown_token

    def reset_matching_markdown_token(
        self, new_matching_markdown_token: MarkdownToken
    ) -> None:
        """
        Reset the matching markdown token.  To be used only when rewinding.
        """
        self.__matching_markdown_token = new_matching_markdown_token

    def generate_close_markdown_token_from_stack_token(
        self,
        extracted_whitespace: str = "",
        extra_end_data: Optional[str] = None,
        was_forced: bool = False,
    ) -> EndMarkdownToken:
        """
        Generate the token emitted to close off the current stack token
        """

        assert (
            self._stack_link_definition != self.type_name
        ), "A stack LRD token must never create a matching close token."
        assert self.matching_markdown_token, str(self)

        return EndMarkdownToken(
            self.type_name,
            extracted_whitespace,
            extra_end_data,
            self.matching_markdown_token,
            was_forced,
        )

    @property
    def is_document(self) -> bool:
        """
        Is this stack token a document token?
        """
        return self.type_name == self._stack_base_document

    @property
    def is_unordered_list(self) -> bool:
        """
        Is this stack token the unordered list token?
        """
        return self.type_name == self._stack_unordered_list

    @property
    def is_ordered_list(self) -> bool:
        """
        Is this stack token the ordered list token?
        """
        return self.type_name == self._stack_ordered_list

    @property
    def is_list(self) -> bool:
        """
        Is this stack token one of the list tokens?
        """
        return self.is_ordered_list or self.is_unordered_list

    @property
    def is_html_block(self) -> bool:
        """
        Is this stack token a html block token?
        """
        return self.type_name == self._stack_html_block

    @property
    def is_code_block(self) -> bool:
        """
        Is this stack token a fenced code block or indented code block token?
        """
        return self.is_fenced_code_block or self.is_indented_code_block

    @property
    def is_fenced_code_block(self) -> bool:
        """
        Is this stack token a fenced code block token?
        """
        return self.type_name == self._stack_fenced_code

    @property
    def is_indented_code_block(self) -> bool:
        """
        Is this stack token an indented code block token?
        """
        return self.type_name == self._stack_indented_code

    @property
    def is_block_quote(self) -> bool:
        """
        Is this stack token a block quote token?
        """
        return self.type_name == self._stack_block_quote

    @property
    def is_paragraph(self) -> bool:
        """
        Is this stack token a paragraph token?
        """
        return self.type_name == self._stack_paragraph

    @property
    def was_link_definition_started(self) -> bool:
        """
        Is this stack token a link definition started token?
        """
        return self.type_name == self._stack_link_definition

    @property
    def was_table_block_started(self) -> bool:
        """
        Is this stack token a table block token?
        """
        return self.type_name == self._stack_table_rows


class DocumentStackToken(StackToken):
    """
    Class to provide for a stack token at the root.
    """

    def __init__(self) -> None:
        StackToken.__init__(self, StackToken._stack_base_document)


class ParagraphStackToken(StackToken):
    """
    Class to provide for a stack token for a paragraph.
    """

    def __init__(self, matching_markdown_token: ParagraphMarkdownToken) -> None:
        StackToken.__init__(
            self,
            StackToken._stack_paragraph,
            matching_markdown_token=matching_markdown_token,
        )


class BlockQuoteStackToken(StackToken):
    """
    Class to provide for a stack token for a block quote.
    """

    def __init__(self, matching_markdown_token: BlockQuoteMarkdownToken) -> None:
        StackToken.__init__(
            self,
            StackToken._stack_block_quote,
            matching_markdown_token=matching_markdown_token,
        )


class IndentedCodeBlockStackToken(StackToken):
    """
    Class to provide for a stack token for an indented code block.
    """

    def __init__(self, matching_markdown_token: IndentedCodeBlockMarkdownToken) -> None:
        StackToken.__init__(
            self,
            StackToken._stack_indented_code,
            matching_markdown_token=matching_markdown_token,
        )


class FencedCodeBlockStackToken(StackToken):
    """
    Class to provide for a stack token for a fenced code block.
    """

    def __init__(
        self,
        code_fence_character: str,
        fence_character_count: int,
        whitespace_start_count: int,
        matching_markdown_token: FencedCodeBlockMarkdownToken,
    ) -> None:
        (
            self.__code_fence_character,
            self.__fence_character_count,
            self.__whitespace_start_count,
        ) = (code_fence_character, fence_character_count, whitespace_start_count)
        StackToken.__init__(
            self,
            StackToken._stack_fenced_code,
            matching_markdown_token=matching_markdown_token,
            extra_data=":".join(
                [
                    self.__code_fence_character,
                    str(self.__fence_character_count),
                    str(self.__whitespace_start_count),
                ]
            ),
        )

    @property
    def code_fence_character(self) -> str:
        """
        Returns the fence character associated with this stack token.
        """
        return self.__code_fence_character

    @property
    def fence_character_count(self) -> int:
        """
        Returns the fence character count associated with this stack token.
        """
        return self.__fence_character_count

    @property
    def whitespace_start_count(self) -> int:
        """
        Returns the count of whitespaces preceding this stack token.
        """
        return self.__whitespace_start_count


class ListStackToken(StackToken):
    """
    Class to provide for a stack token for a list.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        type_name: str,
        indent_level: int,
        list_character: str,
        ws_before_marker: int,
        ws_after_marker: int,
        start_index: int,
        matching_markdown_token: ContainerMarkdownToken,
    ) -> None:
        (
            self.__indent_level,
            self.__list_character,
            self.__ws_before_marker,
            self.__ws_after_marker,
            self.__start_index,
        ) = (
            indent_level,
            list_character,
            ws_before_marker,
            ws_after_marker,
            start_index,
        )
        self.__last_new_list_token: Optional[NewListItemMarkdownToken] = None

        StackToken.__init__(
            self,
            type_name,
            matching_markdown_token=matching_markdown_token,
            extra_data=":".join(
                [
                    str(self.__indent_level),
                    self.__list_character,
                    str(self.__ws_before_marker),
                    str(self.__ws_after_marker),
                    str(self.__start_index),
                ]
            ),
        )

    # pylint: enable=too-many-arguments
    @property
    def indent_level(self) -> int:
        """
        Returns the indent level associated with this stack token.
        """
        return self.__indent_level

    @property
    def list_character(self) -> str:
        """
        Returns the list character associated with this stack token.
        """
        return self.__list_character

    @property
    def ws_before_marker(self) -> int:
        """
        Returns the whitespace occurring before this stack token.
        """
        return self.__ws_before_marker

    @property
    def ws_after_marker(self) -> int:
        """
        Returns the whitespace occurring after this stack token.
        """
        return self.__ws_after_marker

    @property
    def start_index(self) -> int:
        """
        Returns the start index for this stack token.
        """
        return self.__start_index

    @property
    def last_new_list_token(self) -> Optional[NewListItemMarkdownToken]:
        """
        Returns the last new-list token associated with this stack token.
        """
        return self.__last_new_list_token

    def set_last_new_list_token(self, new_list_token: NewListItemMarkdownToken) -> None:
        """
        Set the last new-list token associated with this stack token.
        """
        self.__last_new_list_token = new_list_token


class OrderedListStackToken(ListStackToken):
    """
    Class to provide for a stack token for an ordered list.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        indent_level: int,
        list_character: str,
        ws_before_marker: int,
        ws_after_marker: int,
        start_index: int,
        matching_markdown_token: OrderedListStartMarkdownToken,
    ) -> None:
        ListStackToken.__init__(
            self,
            StackToken._stack_ordered_list,
            indent_level,
            list_character,
            ws_before_marker,
            ws_after_marker,
            start_index,
            matching_markdown_token,
        )

    # pylint: enable=too-many-arguments


class UnorderedListStackToken(ListStackToken):
    """
    Class to provide for a stack token for an unordered list.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        indent_level: int,
        list_character: str,
        ws_before_marker: int,
        ws_after_marker: int,
        start_index: int,
        matching_markdown_token: UnorderedListStartMarkdownToken,
    ) -> None:
        ListStackToken.__init__(
            self,
            StackToken._stack_unordered_list,
            indent_level,
            list_character,
            ws_before_marker,
            ws_after_marker,
            start_index,
            matching_markdown_token,
        )

    # pylint: enable=too-many-arguments


class HtmlBlockStackToken(StackToken):
    """
    Class to provide for a stack token for a html block.
    """

    def __init__(
        self, html_block_type: str, matching_markdown_token: HtmlBlockMarkdownToken
    ) -> None:
        self.__html_block_type = html_block_type
        extra_data = html_block_type
        StackToken.__init__(
            self,
            StackToken._stack_html_block,
            matching_markdown_token=matching_markdown_token,
            extra_data=extra_data,
        )

    @property
    def html_block_type(self) -> str:
        """
        Returns the html block type associated with this stack token.
        """
        return self.__html_block_type


# pylint: disable=too-many-instance-attributes
class LinkDefinitionStackToken(StackToken):
    """
    Class to provide for a stack token for a possible link definition.
    """

    def __init__(
        self, extracted_whitespace: str, position_marker: PositionMarker
    ) -> None:
        (
            self.__extracted_whitespace,
            self.__start_position_marker,
        ) = (
            extracted_whitespace,
            position_marker,
        )
        self.original_stack_depth: Optional[int] = None
        self.original_document_depth: Optional[int] = None
        self.last_block_quote_stack_token: Optional[StackToken] = None
        self.last_block_quote_markdown_token_index: Optional[int] = None
        self.copy_of_last_block_quote_markdown_token: Optional[
            BlockQuoteMarkdownToken
        ] = None
        self.copy_of_token_stack: Optional[List[StackToken]] = None

        self.x1_token: Optional[MarkdownToken] = None
        self.copy_of_x1_token: Optional[MarkdownToken] = None
        self.x1_token_index: Optional[int] = None

        self.__continuation_lines: List[str] = []
        self.__unmodified_lines: List[str] = []
        # self.__original_lines: List[str] = []
        StackToken.__init__(self, StackToken._stack_link_definition)

    @property
    def extracted_whitespace(self) -> Optional[str]:
        """
        Returns the extracted whitespace associated with this stack token.
        """
        return self.__extracted_whitespace

    @property
    def continuation_lines(self) -> List[str]:
        """
        Returns the continuation lines associated with this stack token.
        """
        return self.__continuation_lines

    @property
    def unmodified_lines(self) -> List[str]:
        """
        Returns the unmodified continuation lines associated with this stack token.
        """
        return self.__unmodified_lines

    # @property
    # def original_lines(self) -> List[str]:
    #     """
    #     Returns the original lines associated with this stack token.
    #     """
    #     return self.__original_lines

    @property
    def start_position_marker(self) -> PositionMarker:
        """
        Returns the start position associated with this stack token.
        """
        return self.__start_position_marker

    def add_continuation_line(self, new_line: str) -> None:
        """
        Add the line to the collection of lines to keep as "continuations".
        """
        self.__continuation_lines.append(new_line)

    def add_unmodified_line(self, new_line: str) -> None:
        """
        Add the line to the collection of lines to keep as "umodified line".
        These are the same as the continuation_lines values, just with the exact
        text that was presented to the parser.
        """
        self.__unmodified_lines.append(new_line)

    # def add_original_line(self, new_line: str) -> None:
    #     """
    #     ...
    #     """
    #     self.__original_lines.append(new_line)

    def add_joined_lines_before_suffix(self, join_suffix: str) -> str:
        """
        Grab the continuation lines as a single line.
        """

        return (
            f"{ParserHelper.newline_character.join(self.continuation_lines)}"
            + f"{ParserHelper.newline_character}{join_suffix}"
            if self.continuation_lines
            else join_suffix
        )


# pylint: enable=too-many-instance-attributes


class TableBlockStackToken(StackToken):
    """
    Class to provide for a stack token for a possible table block.
    """

    def __init__(
        self, extracted_whitespace: str, position_marker: PositionMarker
    ) -> None:
        (self.__start_position_marker, self.__extracted_whitespace) = (
            position_marker,
            extracted_whitespace,
        )
        self.original_stack_depth: Optional[int] = None
        self.original_document_depth: Optional[int] = None
        self.last_block_quote_stack_token: Optional[StackToken] = None
        self.last_block_quote_markdown_token_index: Optional[int] = None
        self.copy_of_last_block_quote_markdown_token: Optional[
            BlockQuoteMarkdownToken
        ] = None
        self.copy_of_token_stack: Optional[List[StackToken]] = None

        self.x1_token: Optional[MarkdownToken] = None
        self.copy_of_x1_token: Optional[MarkdownToken] = None
        self.x1_token_index: Optional[int] = None

        self.__continuation_lines: List[str] = []
        self.__unmodified_lines: List[str] = []
        StackToken.__init__(self, StackToken._stack_table_rows)

    @property
    def extracted_whitespace(self) -> Optional[str]:
        """
        Returns the extracted whitespace associated with this stack token.
        """
        return self.__extracted_whitespace

    @property
    def continuation_lines(self) -> List[str]:
        """
        Returns the continuation lines associated with this stack token.
        """
        return self.__continuation_lines

    @property
    def unmodified_lines(self) -> List[str]:
        """
        Returns the unmodified continuation lines associated with this stack token.
        """
        return self.__unmodified_lines

    @property
    def start_position_marker(self) -> PositionMarker:
        """
        Returns the start position associated with this stack token.
        """
        return self.__start_position_marker

    def add_continuation_line(self, new_line: str) -> None:
        """
        Add the line to the collection of lines to keep as "continuations".
        """
        self.__continuation_lines.append(new_line)

    def add_unmodified_line(self, new_line: str) -> None:
        """
        Add the line to the collection of lines to keep as "umodified line".
        These are the same as the continuation_lines values, just with the exact
        text that was presented to the parser.
        """
        self.__unmodified_lines.append(new_line)

    def add_joined_lines_before_suffix(self, join_suffix: str) -> str:
        """
        Grab the continuation lines as a single line.
        """

        return (
            f"{ParserHelper.newline_character.join(self.continuation_lines)}"
            + f"{ParserHelper.newline_character}{join_suffix}"
            if self.continuation_lines
            else join_suffix
        )
