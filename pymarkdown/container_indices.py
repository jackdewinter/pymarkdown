"""
Module to provide for encapsulation on a group of container indices.
"""


class ContainerIndices:
    """
    Class to provide for encapsulation on a group of container indices.
    """

    def __init__(self, ulist_index, olist_index, block_index):
        self.__ulist_index = ulist_index
        self.__olist_index = olist_index
        self.__block_index = block_index

    @property
    def ulist_index(self):
        """
        Index of the next unordered list element, or -1 if none.
        """
        return self.__ulist_index

    @ulist_index.setter
    def ulist_index(self, value):
        self.__ulist_index = value

    @property
    def olist_index(self):
        """
        Index of the next ordered list element, or -1 if none.
        """
        return self.__olist_index

    @olist_index.setter
    def olist_index(self, value):
        self.__olist_index = value

    @property
    def block_index(self):
        """
        Index of the next block quote element, or -1 if none.
        """
        return self.__block_index

    @block_index.setter
    def block_index(self, value):
        self.__block_index = value

    def __str__(self):
        return (
            f"{{ContainerIndices:ulist_index:{self.ulist_index};olist_index:{self.olist_index};"
            + f"block_index:{self.block_index}}}"
        )
