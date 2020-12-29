"""
Module to provide for a simple bootstrap for the project.
"""
import logging

from pymarkdown.main import PyMarkdownLint

LOGGER = logging.getLogger(__name__)


class Main:
    """
    Class to provide for a simple bootstrap for the project.
    """

    def main(self):
        """
        Main entrance point.
        """
        PyMarkdownLint().main()


if __name__ == "__main__":
    Main().main()
