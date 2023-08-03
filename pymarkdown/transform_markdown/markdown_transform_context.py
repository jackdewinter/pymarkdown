import logging
from typing import List

from pymarkdown.general.parser_logger import ParserLogger
from pymarkdown.tokens.markdown_token import MarkdownToken

POGGER = ParserLogger(logging.getLogger(__name__))


class MarkdownTransformContext:
    def __init__(self) -> None:
        self.block_stack: List[MarkdownToken] = []
        self.container_token_stack: List[MarkdownToken] = []
