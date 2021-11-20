"""
Module to provide a container for lines that need to be requeued.
"""


class RequeueLineInfo:
    """
    Class to provide a container for lines that need to be requeued.
    """

    def __init__(self, lines_to_requeue, force_ignore_first_as_lrd=None):
        assert lines_to_requeue
        self.__lines_to_requeue = lines_to_requeue
        self.__force_ignore_first_as_lrd = force_ignore_first_as_lrd

    @property
    def lines_to_requeue(self):
        """
        Zero or more lines to requeue with the parser.
        """
        return self.__lines_to_requeue

    @property
    def force_ignore_first_as_lrd(self):
        """
        Whether to ignore the first line as an LRD.
        """
        return self.__force_ignore_first_as_lrd
