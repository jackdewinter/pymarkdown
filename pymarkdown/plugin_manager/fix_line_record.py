"""
Module to hold information regarding a line fix that was made.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class FixLineRecord:
    """
    Class to hold information regarding a line fix that was made.
    """

    source: str
    line_number: int
    plugin_id: str
