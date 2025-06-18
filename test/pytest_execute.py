"""
Module to provide functionality to test scripts from within pytest.
"""

import difflib
import io
import logging
import os
import sys
import tempfile
import traceback
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union

LOGGER = logging.getLogger(__name__)

DEFAULT_FILE_ENCODING = "utf-8"


class InProcessResult:
    """
    Class to provide for an encapsulation of the results of an execution.
    """

    def __init__(
        self, return_code: int, std_out: io.StringIO, std_err: io.StringIO
    ) -> None:
        self.__return_code = return_code
        self.__std_out = std_out
        self.__std_err = std_err

    @staticmethod
    def make_value_visible(value_to_modify: Any) -> str:
        """
        For the given value, turn it into a string if necessary, and then replace
        any known "invisible" characters with more visible strings.
        """
        return (
            str(value_to_modify)
            .replace("\b", "\\b")
            .replace("\a", "\\a")
            .replace("\t", "\\t")
            .replace("\n", "\\n")
        )

    @staticmethod
    def compare_versus_expected(
        stream_name: str,
        actual_stream: Union[io.StringIO, str],
        expected_stream: Union[io.StringIO, str],
        additional_text: Optional[List[str]] = None,
        log_extra: Optional[str] = None,
    ) -> None:
        """
        Do a thorough comparison of the actual stream against the expected text.
        """

        actual_stream_text = (
            actual_stream
            if isinstance(actual_stream, str)
            else actual_stream.getvalue()
        )
        expected_stream_text = (
            expected_stream
            if isinstance(expected_stream, str)
            else expected_stream.getvalue()
        )
        if additional_text:
            assert actual_stream_text.strip().startswith(
                expected_stream_text.strip()
            ), (
                f"Block\n---\n{expected_stream_text}\n---\nwas not found at the start of"
                + f"\n---\n{actual_stream_text}\nExtra:{log_extra}"
            )

            for next_text_block in additional_text:
                was_found = next_text_block.strip() in actual_stream_text.strip()
                diff = difflib.ndiff(
                    next_text_block.strip().splitlines(),
                    actual_stream_text.strip().splitlines(),
                )

                diff_values = "\n".join(list(diff))
                print(diff_values, file=sys.stderr)
                if not was_found:
                    raise AssertionError(
                        f"Block\n---\n{next_text_block}\n---\nwas not found in\n---\n{actual_stream_text}"
                    )
        elif actual_stream_text.strip() != expected_stream_text.strip():
            diff = difflib.ndiff(
                expected_stream_text.splitlines(), actual_stream_text.splitlines()
            )

            diff_values = "\n".join(list(diff))
            diff_values = f"{diff_values}\n---\n"

            LOGGER.warning(
                "actual>>%s",
                InProcessResult.make_value_visible(actual_stream_text),
            )
            print(
                f"WARN>actual>>{InProcessResult.make_value_visible(actual_stream_text)}"
            )
            LOGGER.warning(
                "expect>>%s", InProcessResult.make_value_visible(expected_stream_text)
            )
            print(
                f"WARN>expect>>{InProcessResult.make_value_visible(expected_stream_text)}"
            )
            if log_extra:
                print(f"log_extra:{log_extra}")
            raise AssertionError(f"{stream_name} not as expected:\n{diff_values}")

    @property
    def return_code(self) -> int:
        """
        Return code provided after execution.
        """
        return self.__return_code

    @property
    def std_out(self) -> io.StringIO:
        """
        Standard output collected during execution.
        """
        return self.__std_out

    @property
    def std_err(self) -> io.StringIO:
        """
        Standard output collected during execution.
        """
        return self.__std_err

    # pylint: disable=too-many-arguments
    def assert_results(
        self,
        stdout: Optional[Union[io.StringIO, str]] = None,
        stderr: Optional[Union[io.StringIO, str]] = None,
        error_code: int = 0,
        additional_error: Optional[List[str]] = None,
        output_parts: Optional[List[str]] = None,  # TODO Better name
    ) -> None:
        """
        Assert the results are as expected in the "assert" phase.
        """

        try:
            if stdout:
                extra_value = self.__std_err.getvalue() if self.__std_err else None
                InProcessResult.compare_versus_expected(
                    "Stdout",
                    self.__std_out,
                    stdout,
                    log_extra=extra_value,
                )
            elif output_parts:
                for next_part in output_parts:
                    escaped_next_part = next_part.replace("\n", "\\n")
                    escaped_output = self.__std_out.getvalue().replace("\n", "\\n")
                    assert_text = f"Part '{escaped_next_part}' is not present in output '{escaped_output}'."
                    assert next_part in self.__std_out.getvalue(), assert_text
            else:
                assert_text = (
                    f"Expected stdout to be empty, not: {self.__std_out.getvalue()}"
                )
                if self.__std_err.getvalue():
                    assert_text += f"\nStdErr was:{self.__std_err.getvalue()}"
                assert not self.__std_out.getvalue(), assert_text

            if stderr:
                InProcessResult.compare_versus_expected(
                    "Stderr", self.__std_err, stderr, additional_error
                )
            else:
                error_message = (
                    "None" if not self.__std_err else self.__std_err.getvalue()
                )
                assert (
                    not self.__std_err or not self.__std_err.getvalue()
                ), f"Expected stderr to be empty, not: {error_message}"

            assert (
                self.__return_code == error_code
            ), f"Actual error code ({self.__return_code}) and expected error code ({error_code}) differ."

        finally:
            if self.__std_out:
                self.__std_out.close()
            if self.__std_err:
                self.__std_err.close()

    # pylint: enable=too-many-arguments

    @staticmethod
    def assert_resultant_file(file_path: str, expected_contents: str) -> None:
        """
        Assert the contents of a given file against it's expected contents.
        """

        split_expected_contents = expected_contents.split("\n")
        with open(file_path, "r", encoding=DEFAULT_FILE_ENCODING) as infile:
            split_actual_contents = infile.readlines()
        for line_index, line_content in enumerate(split_actual_contents):
            if line_content[-1] == "\n":
                split_actual_contents[line_index] = line_content[:-1]

        are_different = len(split_expected_contents) != len(split_actual_contents)
        if not are_different:
            index = 0
            while index < len(split_expected_contents):
                are_different = (
                    split_expected_contents[index] != split_actual_contents[index]
                )
                if are_different:
                    break
                index += 1

        if are_different:
            diff = difflib.ndiff(split_actual_contents, split_expected_contents)
            diff_values = "\n".join(list(diff))
            raise AssertionError(
                f"Actual and expected contents of '{file_path}' are not equal:\n---\n{diff_values}\n---\n"
            )


# pylint: disable=too-few-public-methods
class SystemState:
    """
    Class to provide an encapsulation of the system state so that we can restore
    it later.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the SystemState class.
        """

        self.saved_stdin = sys.stdin
        self.saved_stdout = sys.stdout
        self.saved_stderr = sys.stderr
        self.saved_cwd = os.getcwd()
        self.saved_env = os.environ
        self.saved_argv = sys.argv

    def restore(self) -> None:
        """
        Restore the system state variables to what they were before.
        """

        os.chdir(self.saved_cwd)
        os.environ = self.saved_env  # noqa B003
        sys.argv = self.saved_argv
        sys.stdin = self.saved_stdin
        sys.stdout = self.saved_stdout
        sys.stderr = self.saved_stderr


# pylint: enable=too-few-public-methods


class InProcessExecution(ABC):
    """
    Handle the in-process execution of the script's mainline.
    """

    @abstractmethod
    def execute_main(self, direct_arguments: Optional[List[str]] = None) -> None:
        """
        Provides the code to execute the mainline.  Should be simple like:
        MyObjectClass().main()
        """

    @abstractmethod
    def get_main_name(self) -> str:
        """
        Provides the main name to associate with the mainline.  Gets set as
        the first argument to the program.
        """

    @classmethod
    def handle_system_exit(
        cls, exit_exception: SystemExit, std_error: io.StringIO
    ) -> int:
        """
        Handle the processing of an "early" exit as a result of our execution.
        """
        returncode = exit_exception.code
        if isinstance(returncode, str):
            std_error.write("f{exit_exception}\n")
            returncode = 1
        elif returncode is None:
            returncode = 0
        return returncode

    @classmethod
    def handle_normal_exception(cls) -> int:
        """
        Handle the processing of a normal exception as a result of our execution.
        """
        trace_back = None
        try:
            exception_type, exception_value, trace_back = sys.exc_info()
            assert exception_type is not None
            assert exception_value is not None
            assert trace_back is not None
            traceback.print_exception(
                exception_type, exception_value, trace_back.tb_next
            )
        finally:
            if trace_back:
                del trace_back
        return 1

    # pylint: disable=too-many-arguments, too-many-locals, too-many-branches
    def invoke_main(
        self,
        arguments: List[str],
        cwd: Optional[str] = None,
        suppress_first_line_heading_rule: bool = True,
        standard_input_to_use: Optional[str] = None,
        use_direct_arguments: bool = False,
    ) -> InProcessResult:
        """
        Invoke the mainline so that we can capture results.
        """

        keep_directory = os.getenv("PTEST_KEEP_DIRECTORY", None)
        if keep_directory and os.path.isdir(keep_directory):
            if (
                len(arguments) >= 2
                and arguments[-2] == "scan"
                and os.path.isfile(arguments[-1])
            ):
                with tempfile.NamedTemporaryFile(
                    "wt",
                    encoding="utf-8",
                    dir=keep_directory,
                    suffix=".md",
                    delete=False,
                ) as temp_file:
                    with open(arguments[-1], "rt", encoding="utf-8") as fixed_file:
                        temp_file.write(fixed_file.read())

        if suppress_first_line_heading_rule:
            new_arguments = arguments.copy() if arguments else []
            if "--disable-rules" not in new_arguments:
                new_arguments.insert(0, "--disable-rules")
                new_arguments.insert(1, "md041")
            else:
                disable_index = new_arguments.index("--disable-rules")
                disable_value = new_arguments[disable_index + 1]
                if not disable_value.endswith(","):
                    disable_value += ","
                disable_value += "md041"
                new_arguments[disable_index + 1] = disable_value
            arguments = new_arguments

        saved_state = SystemState()

        if standard_input_to_use is not None:
            sys.stdin = io.StringIO(standard_input_to_use)
        std_output = io.StringIO()
        std_error = io.StringIO()

        sys.stdout = std_output
        sys.stderr = std_error

        direct_arguments = None
        if use_direct_arguments:
            direct_arguments = arguments
        else:
            sys.argv = arguments.copy() if arguments else []
            sys.argv.insert(0, self.get_main_name())

        if cwd:
            os.chdir(cwd)

        # pylint: disable=broad-exception-caught
        try:
            returncode = 0
            self.execute_main(direct_arguments)
        except SystemExit as this_exception:
            returncode = self.handle_system_exit(this_exception, std_error)
        except Exception:
            returncode = self.handle_normal_exception()
        finally:
            saved_state.restore()
        # pylint: enable=broad-exception-caught

        return InProcessResult(returncode, std_output, std_error)

    # pylint: enable=too-many-arguments, too-many-locals, too-many-branches
