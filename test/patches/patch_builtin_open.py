"""
Module to patch the "builtin.open" function.
"""

import unittest.mock
from contextlib import contextmanager
from test.patches.patch_base import PatchBase
from typing import Any, Dict, Generator, Tuple


class PatchBuiltinOpen(PatchBase):
    """
    Class to patch the "builtin.open" function.
    """

    def __init__(self) -> None:
        super().__init__("builtins.open")
        self.mock_patcher = None
        self.patched_open = None
        self.open_file_args = None

        self.content_map: Dict[str, str] = {}
        self.exception_map: Dict[str, Tuple[str, Exception]] = {}

    def start(self, log_action: bool = True) -> None:
        """
        Start the patching of the "open" function.
        """
        super().start(log_action=log_action)

        self._add_side_effect(self.__my_open)
        if log_action:
            self._add_action_comment(f"started: map={self.exception_map}")

    def stop(
        self, log_action: bool = True, print_action_comments: bool = False
    ) -> None:
        """
        Stop the patching of the "open" function.
        """
        super().stop(log_action=log_action, print_action_comments=print_action_comments)

    def register_text_content_for_file(
        self, exact_file_name: str, file_contents: str
    ) -> None:
        """
        Register text content to return when the specified file is opened for reading as
        a test file.
        """
        self.content_map[exact_file_name] = file_contents
        if len(file_contents) > 20:
            file_contents = f"{file_contents[:19]}..."
        self._add_action_comment(
            f"register_text_content[{exact_file_name}]=[{file_contents}]]"
        )

    def register_exception_for_file(
        self, exact_file_name: str, file_mode: str, exception_to_throw: Exception
    ) -> None:
        """
        Register an exception to raise when the specified file is opened with the given mode.
        """
        self.exception_map[exact_file_name] = (file_mode, exception_to_throw)
        self._add_action_comment(
            f"register_exception[{exact_file_name}]=[{file_mode}],[{type(exception_to_throw)}]"
        )

    def __my_open(self, *args: Any, **kwargs: Any) -> Any:
        """
        Provide alternate handling of the "builtins.open" function.
        """
        filename = args[0]
        filemode = args[1] if len(args) > 1 else "r"
        if filename in self.content_map and filemode == "r":
            self._add_action_comment("text-content-match")

            content = self.content_map[filename]
            file_object = unittest.mock.mock_open(read_data=content).return_value
            file_object.__iter__.return_value = content.splitlines(True)
            return file_object

        if filename in self.exception_map:
            match_filemode, exception_to_throw = self.exception_map[filename]
            if filemode == match_filemode:
                self._add_action_comment(str((args, "exception-match")))
                raise exception_to_throw
            self._add_action_comment(str((args, "exception-mode-mismatch")))

        # pylint: disable=unspecified-encoding
        self.stop(log_action=False)
        try:
            self._add_action_comment(f"passthrough = [{args}]")

            return open(
                filename,
                filemode,
                **kwargs,
            )
        finally:
            self.start(log_action=False)
        # pylint: enable=unspecified-encoding


@contextmanager
def path_builtin_open_with_exception(
    exception_path: str,
    file_mode: str,
    exception_to_throw: Exception,
    print_action_comments: bool = False,
) -> Generator[None, None, None]:
    """
    Patch the builtin.open function, registering an exception to be thrown.
    """
    patch = PatchBuiltinOpen()
    patch.register_exception_for_file(exception_path, file_mode, exception_to_throw)
    patch.start()
    try:
        yield
    finally:
        patch.stop(print_action_comments=print_action_comments)
