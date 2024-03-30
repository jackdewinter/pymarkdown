"""
Module to provide an indication of an error while tokenizing the Markdown file.
"""


class BadTokenizationError(Exception):
    """
    Class to allow for a critical error during the tokenization of the Markdown file
    to be reported.
    """

    def __init__(self, formatted_message: str):
        super().__init__(formatted_message)
