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
