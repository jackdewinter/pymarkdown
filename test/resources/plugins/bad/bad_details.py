"""
Module to implement a sample plugin that has a bad constructor function.
"""
from pymarkdown.rule_plugin import RulePlugin


class BadDetails(RulePlugin):
    """
    Class to implement a sample plugin that has a bad details function.
    """

    def get_details(self):
        """
        Get the details for the plugin.
        """
        raise Exception("bad details")
