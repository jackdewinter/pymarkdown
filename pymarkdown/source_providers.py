"""
Module to provide a tokenization of a markdown-encoded string.
"""


# pylint: disable=too-few-public-methods
class InMemorySourceProvider:
    """
    Class to provide for a source provider that is totally within memory.
    """

    def __init__(self, source_text):
        self.source_text = source_text
        self.next_token = self.source_text.split("\n", 1)

    def get_next_line(self):
        """
        Get the next line from the source provider.
        """
        token_to_use = None
        if self.next_token:
            if len(self.next_token) == 2:
                token_to_use = self.next_token[0]
                self.next_token = self.next_token[1].split("\n", 1)
            else:
                assert self.next_token
                token_to_use = self.next_token[0]
                self.next_token = None
        return token_to_use


# pylint: enable=too-few-public-methods
