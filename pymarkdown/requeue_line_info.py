"""
Module to provide a container for lines that need to be requeued.
"""


# pylint: disable=too-few-public-methods
class RequeueLineInfo:
    """
    Class to provide a container for lines that need to be requeued.
    """

    def __init__(self, lines_to_requeue=None, force_ignore_first_as_lrd=None):
        self.lines_to_requeue = lines_to_requeue
        self.force_ignore_first_as_lrd = force_ignore_first_as_lrd


# pylint: enable=too-few-public-methods
