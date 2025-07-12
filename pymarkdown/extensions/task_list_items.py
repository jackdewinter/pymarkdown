"""
Module to provide for a list item that can be check off.
"""

from typing import Optional, cast

from pymarkdown.extension_manager.extension_impl import ExtensionDetails
from pymarkdown.extension_manager.extension_manager_constants import (
    ExtensionManagerConstants,
)
from pymarkdown.extension_manager.parser_extension import ParserExtension
from pymarkdown.my_application_properties_facade import MyApplicationPropertiesFacade
from pymarkdown.tokens.inline_markdown_token import InlineMarkdownToken
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    MarkdownTransformContext,
    RegisterHtmlTransformHandlersProtocol,
    RegisterMarkdownTransformHandlersProtocol,
)


class MarkdownTaskListItemsExtension(ParserExtension):
    """
    Extension to implement the task list items extension.
    """

    def get_identifier(self) -> str:
        """
        Get the identifier associated with this extension.
        """
        return "markdown-task-list-items"

    def get_details(self) -> ExtensionDetails:
        """
        Get the details for the extension.
        """
        return ExtensionDetails(
            extension_id=self.get_identifier(),
            extension_name="Markdown Task List Items",
            extension_description="Allows parsing of Markdown task list items.",
            extension_enabled_by_default=False,
            extension_version="0.5.0",
            extension_interface_version=ExtensionManagerConstants.EXTENSION_INTERFACE_VERSION_BASIC,
            extension_url="https://pymarkdown.readthedocs.io/en/latest/extensions/task-list-items/",
            extension_configuration=None,
        )

    def apply_configuration(
        self, extension_specific_facade: MyApplicationPropertiesFacade
    ) -> None:
        """
        Apply any configuration required by the extension.
        """
        _ = extension_specific_facade  # pragma: no cover


class TaskListToken(InlineMarkdownToken):
    """
    Token that contains the pragmas for the document.
    """

    def __init__(
        self,
        checked_character: str,
        line_number: int,
        column_number: int,
    ) -> None:
        self.__checked_character = checked_character
        InlineMarkdownToken.__init__(
            self,
            InlineMarkdownToken._token_task_list,
            checked_character,
            line_number=line_number,
            column_number=column_number,
        )

    @property
    def checked_character(self) -> str:
        """
        Returns the character that is in the checkbox.
        """
        return self.__checked_character

    # pylint: disable=protected-access
    @staticmethod
    def get_markdown_token_type() -> str:
        """
        Get the type of markdown token for rehydration purposes.
        """
        return MarkdownToken._token_task_list

    # pylint: enable=protected-access

    def register_for_markdown_transform(
        self,
        registration_function: RegisterMarkdownTransformHandlersProtocol,
    ) -> None:
        """
        Register any rehydration handlers for leaf markdown tokens.
        """

        registration_function(
            TaskListToken,
            TaskListToken.__rehydrate_task_list_token,
            None,
        )

    @staticmethod
    def __rehydrate_task_list_token(
        context: MarkdownTransformContext,
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str:
        """
        Rehydrate the markdown characters from the token.
        """
        _ = previous_token, context

        task_list_token = cast(TaskListToken, current_token)
        return f"[{task_list_token.checked_character}]"

    @staticmethod
    def register_for_html_transform(
        register_handlers: RegisterHtmlTransformHandlersProtocol,
    ) -> None:
        """
        Register any functions required to generate HTML from the tokens.
        """
        register_handlers(
            TaskListToken,
            TaskListToken.__handle_pragma_token,
            None,
        )

    @staticmethod
    def __handle_pragma_token(
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str:
        _ = (transform_state, next_token)

        task_list_token = cast(TaskListToken, next_token)
        if task_list_token.checked_character == " ":
            output_html += '<input type="checkbox">'
        else:
            output_html += '<input checked="" type="checkbox">'
        return output_html
