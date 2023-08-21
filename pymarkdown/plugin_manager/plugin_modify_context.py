"""
Module to provide for a context with which tokens can be modified.
"""
from abc import abstractproperty


class PluginModifyContext:
    """
    Class to provide for a context with which tokens can be modified.
    """

    # pylint: disable=deprecated-decorator
    @abstractproperty
    def is_during_line_pass(self) -> bool:
        """
        Report on whether fix mode is currently going through a line pass.
        """

    # pylint: enable=deprecated-decorator

    # pylint: disable=deprecated-decorator
    @abstractproperty
    def in_fix_mode(self) -> bool:
        """
        Report on whether the application is in fix mode.x
        """

    # pylint: enable=deprecated-decorator
