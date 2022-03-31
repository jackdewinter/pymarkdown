"""
Module to provide for encapsulation on a group of container indices.
"""

from dataclasses import dataclass


@dataclass
class ContainerIndices:
    """
    Class to provide for encapsulation on a group of container indices.
    """

    ulist_index: int
    olist_index: int
    block_index: int

    def __str__(self) -> str:
        return (
            f"{{ContainerIndices:ulist_index:{self.ulist_index};olist_index:{self.olist_index};"
            + f"block_index:{self.block_index}}}"
        )
