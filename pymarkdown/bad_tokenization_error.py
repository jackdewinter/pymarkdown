"""
Module to provide an indication of an error while tokenizing the Markdown file.
"""


class BadTokenizationError(Exception):
    """
    Class to allow for a critical error during the tokenization of the Markdown file
    to be reported.
    """

    def __init__(self, formatted_message=None):
        if not formatted_message:
            formatted_message = (
                "File was not translated from Markdown text to Markdown tokens."
            )
        super(BadTokenizationError, self).__init__(formatted_message)
