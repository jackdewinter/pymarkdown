"""
Module to provide context to markdown transforms.
"""

import logging
from dataclasses import dataclass
from typing import List, Optional

from typing_extensions import Protocol

from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.tokens.markdown_token import MarkdownToken
from pymarkdown.transform_gfm.transform_state import TransformState

POGGER = ParserLogger(logging.getLogger(__name__))


@dataclass
class IndentAdjustment:
    """
    Class to hold indent adjustments.
    """

    adjustment: int = 0


# pylint: disable=too-few-public-methods
class MarkdownTransformContext:
    """
    Context to preserve state for the markdown transform.
    """

    def __init__(self) -> None:
        self.block_stack: List[MarkdownToken] = []
        self.container_token_stack: List[MarkdownToken] = []
        self.original_container_token_stack: List[MarkdownToken] = []
        self.container_token_indents: List[IndentAdjustment] = []


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class StartMarkdownTokenTransformProtocol(Protocol):
    """
    Protocol to call for the start token of a markdown transform.
    """

    def __call__(
        self,
        context: "MarkdownTransformContext",
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
    ) -> str: ...  # pragma: no cover


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class EndMarkdownTokenTransformProtocol(Protocol):
    """
    Protocol to allow registration of handlers for the markdown transform.
    """

    def __call__(
        self,
        context: "MarkdownTransformContext",
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
    ) -> str: ...  # pragma: no cover


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class StartMarkdownContainerTokenTransformProtocol(Protocol):
    """
    Protocol to call for the start container token of a markdown transform.
    """

    # pylint: disable=too-many-arguments
    def __call__(
        self,
        context: "MarkdownTransformContext",
        current_token: MarkdownToken,
        previous_token: Optional[MarkdownToken],
        next_token: Optional[MarkdownToken],
        transformed_data: str,
    ) -> str: ...  # pragma: no cover

    # pylint: enable=too-many-arguments


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class EndMarkdownContainerTokenTransformProtocol(Protocol):
    """
    Protocol to allow registration of handlers for the container tokens of a markdown transform.
    """

    def __call__(
        self,
        context: "MarkdownTransformContext",
        current_token: MarkdownToken,
        actual_tokens: List[MarkdownToken],
        token_index: int,
    ) -> str: ...  # pragma: no cover


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class RegisterMarkdownTransformHandlersProtocol(Protocol):
    """
    Protocol to allow registration of handlers for the markdown transform.
    """

    def __call__(
        self,
        type_to_register: type,
        start_function: StartMarkdownTokenTransformProtocol,
        end_function: Optional[EndMarkdownTokenTransformProtocol],
    ) -> None: ...  # pragma: no cover


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class StartHtmlTokenTransformProtocol(Protocol):
    """
    Protocol to call for the start token of a html transform.
    """

    def __call__(
        self,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str: ...  # pragma: no cover


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class EndHtmlTokenTransformProtocol(Protocol):
    """
    Protocol to call for the end token or a html transform.
    """

    def __call__(
        self,
        output_html: str,
        next_token: MarkdownToken,
        transform_state: TransformState,
    ) -> str: ...  # pragma: no cover


# pylint: enable=too-few-public-methods


# pylint: disable=too-few-public-methods
class RegisterHtmlTransformHandlersProtocol(Protocol):
    """
    Protocol to allow registration of handlers for the html transform.
    """

    def __call__(
        self,
        type_to_register: type,
        start_function: StartHtmlTokenTransformProtocol,
        end_function: Optional[EndHtmlTokenTransformProtocol],
    ) -> None: ...  # pragma: no cover


# pylint: enable=too-few-public-methods
