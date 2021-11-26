"""
Module to encapuslate information about the current state of block quotes.
"""


class BlockQuoteData:
    """
    Class to encapuslate information about the current state of block quotes.
    """

    def __init__(self, this_bq_count, stack_bq_count):
        self.__this_bq_count = this_bq_count
        self.__stack_bq_count = stack_bq_count

    @property
    def current_count(self):
        """
        Current count of block quote for this line.
        """
        return self.__this_bq_count

    @property
    def stack_count(self):
        """
        Current count of block quote according to the token stack.
        """
        return self.__stack_bq_count
