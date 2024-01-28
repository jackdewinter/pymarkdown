"""
Module to provide a base class for any patch classes.
"""

import unittest
from typing import Any, List, Optional, Union
from unittest.mock import AsyncMock, MagicMock, _patch


class PatchBase:
    """
    Class to provide a base class for any patch classes.
    """

    def __init__(self, function_name_to_patch: str) -> None:
        self.__mock_patcher: Optional[_patch[Union[MagicMock, AsyncMock]]] = None
        self.__patched_function: Optional[MagicMock] = None
        self.__function_name_to_patch = function_name_to_patch
        self.__action_comments: List[str] = []

    def _add_action_comment(self, comment_to_add: str) -> None:
        # sourcery skip: remove-unnecessary-cast
        self.__action_comments.append(str(comment_to_add))

    def _add_side_effect(self, callable_function: Any) -> None:
        assert self.__patched_function is not None
        self.__patched_function.side_effect = callable_function

    def start(self, log_action: bool = True) -> None:
        """
        Start the capturing of calls and apply any needed mocking.
        """
        if log_action:
            self._add_action_comment("starting")
        self.__mock_patcher = unittest.mock.patch(self.__function_name_to_patch)
        assert self.__mock_patcher is not None
        self.__patched_function = self.__mock_patcher.start()

    def stop(
        self, log_action: bool = True, print_action_comments: bool = False
    ) -> None:
        """
        Stop the capturing of calls and any needed mocking.
        """
        assert self.__mock_patcher is not None
        if log_action:
            self._add_action_comment("stopping")

        self.__mock_patcher.stop()
        self.__mock_patcher = None
        self.__patched_function = None
        if log_action:
            self._add_action_comment("stopped")
        if print_action_comments:
            print("\n".join(self.__action_comments))
