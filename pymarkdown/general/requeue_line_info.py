"""
Module to provide a container for lines that need to be requeued.
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RequeueLineInfo:
    """
    Class to provide a container for lines that need to be requeued.
    """

    lines_to_requeue: List[str]
    force_ignore_first_as_lrd: bool
