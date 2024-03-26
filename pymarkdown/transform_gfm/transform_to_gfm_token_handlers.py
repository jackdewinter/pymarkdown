"""
Module to provide for the handlers for tokens to allow transformation into HTML.
"""

import inspect
import logging
from typing import Dict, List, Optional, cast

from pymarkdown.extensions.extension_token_types import ExtensionTokenTypes
from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.tokens.markdown_token import EndMarkdownToken, MarkdownToken
from pymarkdown.tokens.token_types import TokenTypes
from pymarkdown.transform_gfm.transform_state import TransformState
from pymarkdown.transform_markdown.markdown_transform_context import (
    EndHtmlTokenTransformProtocol,
    StartHtmlTokenTransformProtocol,
)

POGGER = ParserLogger(logging.getLogger(__name__))


# pylint: disable=too-few-public-methods


class TransformToGfmTokenHandlers:
    """
    Class to provide for the handlers for tokens to allow transformation into HTML.
    """

    def __init__(self) -> None:
        self.__start_token_handlers: Dict[str, StartHtmlTokenTransformProtocol] = {}
        self.__end_token_handlers: Dict[str, EndHtmlTokenTransformProtocol] = {}

        ert = TokenTypes.get_inline_token_types()
        ert.extend(TokenTypes.get_leaf_token_types())
        ert.extend(TokenTypes.get_container_token_types())
        ert.extend(TokenTypes.get_special_token_types())
        ert.extend(ExtensionTokenTypes.get_token_types())

        for token_type in ert:
            token_init_fn = token_type.__dict__["__init__"]
            init_parameters = {
                i: "" for i in inspect.getfullargspec(token_init_fn)[0] if i != "self"
            }
            handler_instance = token_type(**init_parameters)
            handler_instance.register_for_html_transform(self.__register_handlers)

    def __register_handlers(
        self,
        token_type: type,
        start_token_handler: StartHtmlTokenTransformProtocol,
        end_token_handler: Optional[EndHtmlTokenTransformProtocol] = None,
    ) -> None:
        """
        Register the handlers necessary to deal with token's start and end.
        """
        assert issubclass(
            token_type, MarkdownToken
        ), f"Token class '{token_type}' must be descended from the 'MarkdownToken' class."

        # This is being done to create a rough "default" instance of the type in
        # question.  Because it is a rough creation and we have no intentions of
        # using it, each parameter is an empty string.  Therefore, we expect that
        # mypy will have issues when we create the instance, hence ignoring them.
        #
        # That was the old way, and had problems.  The new way is to call a new
        # static method directly.  Both are here until that is completed.

        # if "get_markdown_token_type" in token_type.__dict__:
        token_name = token_type.__dict__["get_markdown_token_type"].__func__()
        # else:
        #     token_init_fn = token_type.__dict__["__init__"]
        #     init_parameters = {
        #         i: "" for i in inspect.getfullargspec(token_init_fn)[0] if i != "self"
        #     }
        #     handler_instance = token_type(**init_parameters)  # type: ignore
        #     token_name = handler_instance.token_name

        assert token_name, "This must not be empty."
        self.__start_token_handlers[token_name] = start_token_handler
        if end_token_handler:
            self.__end_token_handlers[token_name] = end_token_handler

    # pylint: disable=too-many-arguments
    def apply_transformation(
        self,
        transform_state: TransformState,
        actual_tokens: List[MarkdownToken],
        actual_tokens_size: int,
        next_token: MarkdownToken,
        output_html: str,
    ) -> str:
        """
        Apply the required tranformation for the current token.
        """
        transform_state.add_trailing_text = None
        transform_state.add_leading_text = None
        transform_state.next_token = None

        if (transform_state.actual_token_index + 1) < actual_tokens_size:
            transform_state.next_token = actual_tokens[
                transform_state.actual_token_index + 1
            ]
        if next_token.token_name in self.__start_token_handlers:
            start_handler_fn = self.__start_token_handlers[next_token.token_name]
            POGGER.debug("next_token>:$:<", next_token)
            POGGER.debug("output_html>:$:<", output_html)
            output_html = start_handler_fn(output_html, next_token, transform_state)
            POGGER.debug("output_html>:$:<", output_html)

        elif next_token.is_end_token:
            end_token = cast(EndMarkdownToken, next_token)
            if end_token.type_name not in self.__end_token_handlers:
                raise AssertionError(
                    f"Markdown token end type {end_token.type_name} not supported."
                )
            end_handler_fn = self.__end_token_handlers[end_token.type_name]
            POGGER.debug("end_token>:$:<", end_token)
            POGGER.debug("output_html>:$:<", output_html)
            output_html = end_handler_fn(output_html, end_token, transform_state)
            POGGER.debug("output_html>:$:<", output_html)
        else:
            raise AssertionError(
                f"Markdown token type {type(next_token)} not supported."
            )
        return output_html

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods
