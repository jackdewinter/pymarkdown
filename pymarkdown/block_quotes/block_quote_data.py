"""
Module to encapuslate information about the current state of block quotes.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class BlockQuoteData:
    """
    Class to encapuslate information about the current state of block quotes.
    """

    current_count: int
    stack_count: int

    def __str__(self) -> str:
        return f"BlockQuoteData(current_count={self.current_count},stack_count={self.stack_count})"
