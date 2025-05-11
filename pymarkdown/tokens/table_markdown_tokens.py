from typing import Optional, cast

from pymarkdown.general.parser_helper import ParserHelper
from pymarkdown.general.position_marker import PositionMarker
from pymarkdown.leaf_blocks.table_block_tuple import TableRow
from pymarkdown.tokens.leaf_markdown_token import LeafMarkdownToken
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)


class TableMarkdownToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the main table markdown token.
    """

    def __init__(
        self,
        position_marker: PositionMarker,
    ) -> None:
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_table_main,
            extra_data=None,
            position_marker=position_marker,
            extracted_whitespace="",
            requires_end_token=True,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_table_main

    # pylint: enable=protected-access

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            TableMarkdownToken,
            TableMarkdownToken.__rehydrate_table_start,
            TableMarkdownToken.__rehydrate_table_end,
        )

    @staticmethod
    def __rehydrate_table_start(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        _ = (previous_token, current_token, context)
        return ""

    @staticmethod
    def __rehydrate_table_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        _ = (previous_token, current_token, context)
        return ""

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            TableMarkdownToken,
            TableMarkdownToken.__handle_start_table_token,
            TableMarkdownToken.__handle_end_table_token,
        )

    @staticmethod
    def __handle_start_table_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (transform_state, next_token)

        token_parts = []
        if (
            not output_html
            and transform_state.transform_stack
            and transform_state.transform_stack[-1].endswith("<li>")
        ):
            token_parts.append(ParserHelper.newline_character)
        token_parts.extend([output_html, "<table>", ParserHelper.newline_character])
        return "".join(token_parts)

    @staticmethod
    def __handle_end_table_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token

        return "".join([output_html, "</table>", ParserHelper.newline_character])


class TableMarkdownHeaderToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the table header markdown token.
    """

    def __init__(
        self,
        header_table_row: TableRow,
        separator_table_row: TableRow,
        position_marker: PositionMarker,
    ) -> None:
        if header_table_row:
            self.header_row_leading_whitespace = header_table_row.extracted_whitespace
            self.header_row_trailing_whitespace = header_table_row.trailing_whitespace
            self.did_header_row_start_with_separator = (
                header_table_row.did_start_with_separator
            )
            self.separator_table_row = separator_table_row
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_table_header,
            extra_data=None,
            position_marker=position_marker,
            extracted_whitespace="",
            requires_end_token=True,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_table_header

    # pylint: enable=protected-access

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            TableMarkdownHeaderToken,
            TableMarkdownHeaderToken.__rehydrate_table_header_start,
            TableMarkdownHeaderToken.__rehydrate_table_header_end,
        )

    @staticmethod
    def __rehydrate_table_header_start(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        context.block_stack.append(current_token)

        header_start_text = cast(
            TableMarkdownHeaderToken, current_token
        ).header_row_leading_whitespace
        return header_start_text + (
            "|"
            if cast(
                TableMarkdownHeaderToken, current_token
            ).did_header_row_start_with_separator
            else ""
        )

    @staticmethod
    def __rehydrate_table_header_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        _ = (previous_token, current_token, context)
        del context.block_stack[-1]
        start_token = cast(
            TableMarkdownHeaderToken,
            cast(EndMarkdownToken, current_token).start_markdown_token,
        )
        header_end_text = start_token.separator_table_row.extracted_whitespace
        header_end_text += (
            "|" if start_token.separator_table_row.did_start_with_separator else ""
        )
        for i in start_token.separator_table_row.columns:
            header_end_text += i.leading_whitespace + i.text + i.trailing_whitespace
        header_end_text += start_token.separator_table_row.trailing_whitespace
        return (
            start_token.header_row_trailing_whitespace + "\n" + header_end_text + "\n"
        )

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            TableMarkdownHeaderToken,
            TableMarkdownHeaderToken.__handle_start_table_token,
            TableMarkdownHeaderToken.__handle_end_table_token,
        )

    @staticmethod
    def __handle_start_table_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (transform_state, next_token)

        return "".join(
            [
                output_html,
                "<thead>",
                ParserHelper.newline_character,
                "<tr>",
                ParserHelper.newline_character,
            ]
        )

    @staticmethod
    def __handle_end_table_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token

        return "".join(
            [
                output_html,
                "</tr>",
                ParserHelper.newline_character,
                "</thead>",
                ParserHelper.newline_character,
            ]
        )


class TableMarkdownHeaderItemToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the table header item markdown token.
    """

    def __init__(
        self,
        leading_whitespace: str,
        column_alignment: Optional[str],
        position_marker: PositionMarker,
    ) -> None:
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_table_header_item,
            extra_data=column_alignment,
            position_marker=position_marker,
            extracted_whitespace=leading_whitespace,
            requires_end_token=True,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_table_header_item

    # pylint: enable=protected-access

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            TableMarkdownHeaderItemToken,
            TableMarkdownHeaderItemToken.__rehydrate_table_header_item_start,
            TableMarkdownHeaderItemToken.__rehydrate_table_header_item_end,
        )

    @staticmethod
    def __rehydrate_table_header_item_start(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        _ = (previous_token, current_token, context)
        return cast(TableMarkdownHeaderItemToken, current_token).extracted_whitespace

    @staticmethod
    def __rehydrate_table_header_item_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        _ = (previous_token, current_token, context)
        return cast(EndMarkdownToken, current_token).extracted_whitespace

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            TableMarkdownHeaderItemToken,
            TableMarkdownHeaderItemToken.__handle_start_table_token,
            TableMarkdownHeaderItemToken.__handle_end_table_token,
        )

    @staticmethod
    def __handle_start_table_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (transform_state, next_token)

        if next_token.extra_data:
            text_to_add = f'<th align="{next_token.extra_data}">'
        else:
            text_to_add = "<th>"
        return "".join(
            [
                output_html,
                text_to_add,
            ]
        )

    @staticmethod
    def __handle_end_table_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token

        return "".join(
            [
                output_html,
                "</th>",
                ParserHelper.newline_character,
            ]
        )


class TableMarkdownBodyToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the table header markdown token.
    """

    def __init__(
        self,
        position_marker: PositionMarker,
    ) -> None:
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_table_body,
            extra_data=None,
            position_marker=position_marker,
            extracted_whitespace="",
            requires_end_token=True,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_table_body

    # pylint: enable=protected-access

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            TableMarkdownBodyToken,
            TableMarkdownBodyToken.__rehydrate_table_body_token_start,
            TableMarkdownBodyToken.__rehydrate_table_body_token_end,
        )

    @staticmethod
    def __rehydrate_table_body_token_start(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        _ = (previous_token, current_token, context)
        return ""

    @staticmethod
    def __rehydrate_table_body_token_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        _ = (previous_token, current_token, context)
        return ""

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            TableMarkdownBodyToken,
            TableMarkdownBodyToken.__handle_start_table_token,
            TableMarkdownBodyToken.__handle_end_table_token,
        )

    @staticmethod
    def __handle_start_table_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (transform_state, next_token)

        return "".join(
            [
                output_html,
                "<tbody>",
                ParserHelper.newline_character,
            ]
        )

    @staticmethod
    def __handle_end_table_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token

        return "".join([output_html, "</tbody>", ParserHelper.newline_character])


class TableMarkdownRowToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the table header markdown token.
    """

    def __init__(
        self,
        leading_whitespace: str,
        trailing_whitespace: str,
        did_start_with_separator: bool,
        delta: int,
        position_marker: PositionMarker,
    ) -> None:
        self.leading_whitespace = leading_whitespace
        self.trailing_whitespace = trailing_whitespace
        self.did_start_with_separator = did_start_with_separator
        self.delta = delta
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_table_row,
            extra_data=None,
            position_marker=position_marker,
            extracted_whitespace="",
            requires_end_token=True,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_table_row

    # pylint: enable=protected-access

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            TableMarkdownRowToken,
            TableMarkdownRowToken.__rehydrate_table_row_start,
            TableMarkdownRowToken.__rehydrate_table_row_end,
        )

    @staticmethod
    def __rehydrate_table_row_start(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        _ = (previous_token, current_token, context)
        context.block_stack.append(current_token)
        return cast(TableMarkdownRowToken, current_token).leading_whitespace + (
            "|"
            if cast(TableMarkdownRowToken, current_token).did_start_with_separator
            else ""
        )

    @staticmethod
    def __rehydrate_table_row_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        _ = (previous_token, current_token, context)
        del context.block_stack[-1]
        return (
            cast(EndMarkdownToken, current_token).extracted_whitespace
            + cast(
                TableMarkdownRowToken,
                cast(EndMarkdownToken, current_token).start_markdown_token,
            ).trailing_whitespace
            + "\n"
        )

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            TableMarkdownRowToken,
            TableMarkdownRowToken.__handle_start_table_token,
            TableMarkdownRowToken.__handle_end_table_token,
        )

    @staticmethod
    def __handle_start_table_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (transform_state, next_token)

        return "".join(
            [
                output_html,
                "<tr>",
                ParserHelper.newline_character,
            ]
        )

    @staticmethod
    def __handle_end_table_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token

        ff = [output_html]
        ff.extend("<td></td>\n" for _ in range(_.start_markdown_token.delta))
        ff.extend(("</tr>", ParserHelper.newline_character))
        return "".join(ff)


class TableMarkdownRowItemToken(LeafMarkdownToken):
    """
    Class to provide for an encapsulation of the table header markdown token.
    """

    def __init__(
        self,
        leading_whitespace: str,
        column_alignment: Optional[str],
        position_marker: PositionMarker,
    ) -> None:
        LeafMarkdownToken.__init__(
            self,
            MarkdownToken._token_table_row_item,
            extra_data=column_alignment,
            position_marker=position_marker,
            extracted_whitespace=leading_whitespace,
            requires_end_token=True,
        )

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_table_row_item

    # pylint: enable=protected-access

    def register_for_markdown_transform(
        self, registration_function: RegisterMarkdownTransformHandlersProtocol
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """
        registration_function(
            TableMarkdownRowItemToken,
            TableMarkdownRowItemToken.__rehydrate_table_row_item_start,
            TableMarkdownRowItemToken.__rehydrate_table_row_item_end,
        )

    @staticmethod
    def __rehydrate_table_row_item_start(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        _ = (previous_token, current_token, context)
        return cast(TableMarkdownRowItemToken, current_token).extracted_whitespace

    @staticmethod
    def __rehydrate_table_row_item_end(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the link reference definition from the token.
        """
        _ = (previous_token, current_token, context)
        return cast(TableMarkdownRowItemToken, current_token).extracted_whitespace

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            TableMarkdownRowItemToken,
            TableMarkdownRowItemToken.__handle_start_table_token,
            TableMarkdownRowItemToken.__handle_end_table_token,
        )

    @staticmethod
    def __handle_start_table_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (transform_state, next_token)

        if next_token.extra_data:
            text_to_add = f'<td align="{next_token.extra_data}">'
        else:
            text_to_add = "<td>"
        return "".join(
            [
                output_html,
                text_to_add,
            ]
        )

    @staticmethod
    def __handle_end_table_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = next_token

        return "".join([output_html, "</td>", ParserHelper.newline_character])
