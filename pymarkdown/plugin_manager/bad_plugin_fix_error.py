"""
Module to provide for an error in fixing a document.
"""


class BadPluginFixError(Exception):
    """
    Class to provide for an error in fixing a document.
    """

    def __init__(self, formatted_message: str):
        super().__init__(formatted_message)
