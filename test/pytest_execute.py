"""
Module to provide functionality to test scripts from within pytest.
"""
import difflib
import io
import logging
import os
import sys
import traceback
from abc import ABC, abstractmethod

from pymarkdown.parser_helper import ParserHelper

LOGGER = logging.getLogger(__name__)


class InProcessResult:
    """
    Class to provide for an encapsulation of the results of an execution.
    """

    def __init__(self, return_code, std_out, std_err):
        self.__return_code = return_code
        self.__std_out = std_out
        self.__std_err = std_err

    # pylint: disable=too-many-arguments
    @classmethod
    def compare_versus_expected(
        cls,
        stream_name,
        actual_stream,
        expected_text,
        additional_text=None,
        log_extra=None,
    ):
        """
        Do a thorough comparison of the actual stream against the expected text.
        """

        if additional_text:
            assert actual_stream.getvalue().strip().startswith(expected_text.strip()), (
                f"Block\n---\n{expected_text}\n---\nwas not found at the start of"
                + "\n---\n{actual_stream.getvalue()}\nExtra:{log_extra}"
            )

            for next_text_block in additional_text:
                was_found = next_text_block.strip() in actual_stream.getvalue().strip()
                diff = difflib.ndiff(
                    next_text_block.strip().splitlines(),
                    actual_stream.getvalue().strip().splitlines(),
                )

                diff_values = ParserHelper.newline_character.join(list(diff))
                print(diff_values, file=sys.stderr)
                if not was_found:
                    raise AssertionError(
                        f"Block\n---\n{next_text_block}\n---\nwas not found in\n---\n{actual_stream.getvalue()}"
                    )
        elif actual_stream.getvalue().strip() != expected_text.strip():
            diff = difflib.ndiff(
                expected_text.splitlines(), actual_stream.getvalue().splitlines()
            )

            diff_values = f"{ParserHelper.newline_character.join(list(diff))}\n---\n"

            LOGGER.warning(
                "actual>>%s",
                ParserHelper.make_value_visible(actual_stream.getvalue()),
            )
            print(
                f"WARN>actual>>{ParserHelper.make_value_visible(actual_stream.getvalue())}"
            )
            LOGGER.warning("expect>>%s", ParserHelper.make_value_visible(expected_text))
            print(f"WARN>expect>>{ParserHelper.make_value_visible(expected_text)}")
            if log_extra:
                print(f"log_extra:{log_extra}")
            raise AssertionError(f"{stream_name} not as expected:\n{diff_values}")

    # pylint: enable=too-many-arguments

    @property
    def return_code(self):
        """
        Return code provided after execution.
        """
        return self.__return_code

    @property
    def std_out(self):
        """
        Standard output collected during execution.
        """
        return self.__std_out

    # pylint: disable=too-many-arguments
    def assert_results(
        self,
        stdout=None,
        stderr=None,
        error_code=0,
        additional_error=None,
        alternate_stdout=None,
    ):
        """
        Assert the results are as expected in the "assert" phase.
        """

        try:
            if stdout:
                if alternate_stdout:
                    try:
                        self.compare_versus_expected(
                            "Stdout",
                            self.__std_out,
                            stdout,
                            log_extra=self.__std_err.getvalue(),
                        )
                    except AssertionError:
                        self.compare_versus_expected(
                            "Stdout",
                            self.__std_out,
                            alternate_stdout,
                            log_extra=self.__std_err.getvalue(),
                        )
                else:
                    self.compare_versus_expected(
                        "Stdout",
                        self.__std_out,
                        stdout,
                        log_extra=self.__std_err.getvalue(),
                    )
            else:
                assert_text = (
                    f"Expected stdout to be empty, not: {self.__std_out.getvalue()}"
                )
                if self.__std_err.getvalue():
                    assert_text += f"\nStdErr was:{self.__std_err.getvalue()}"
                assert not self.__std_out.getvalue(), assert_text

            if stderr:
                self.compare_versus_expected(
                    "Stderr", self.__std_err, stderr, additional_error
                )
            else:
                assert (
                    not self.__std_err.getvalue()
                ), f"Expected stderr to be empty, not: {self.__std_err.getvalue()}"

            assert (
                self.__return_code == error_code
            ), f"Actual error code ({self.__return_code}) and expected error code ({error_code}) differ."

        finally:
            self.__std_out.close()
            self.__std_err.close()

    # pylint: enable=too-many-arguments


# pylint: disable=too-few-public-methods
class SystemState:
    """
    Class to provide an encapsulation of the system state so that we can restore
    it later.
    """

    def __init__(self):
        """
        Initializes a new instance of the SystemState class.
        """

        self.saved_stdout = sys.stdout
        self.saved_stderr = sys.stderr
        self.saved_cwd = os.getcwd()
        self.saved_env = os.environ
        self.saved_argv = sys.argv

    def restore(self):
        """
        Restore the system state variables to what they were before.
        """

        os.chdir(self.saved_cwd)
        os.environ = self.saved_env  # noqa B003
        sys.argv = self.saved_argv
        sys.stdout = self.saved_stdout
        sys.stderr = self.saved_stderr


# pylint: enable=too-few-public-methods


class InProcessExecution(ABC):
    """
    Handle the in-process execution of the script's mainline.
    """

    @abstractmethod
    def execute_main(self):
        """
        Provides the code to execute the mainline.  Should be simple like:
        MyObjectClass().main()
        """

    @abstractmethod
    def get_main_name(self):
        """
        Provides the main name to associate with the mainline.  Gets set as
        the first argument to the program.
        """

    @classmethod
    def handle_system_exit(cls, exit_exception, std_error):
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
    def handle_normal_exception(cls):
        """
        Handle the processing of a normal exception as a result of our execution.
        """
        try:
            exception_type, exception_value, trace_back = sys.exc_info()
            traceback.print_exception(
                exception_type, exception_value, trace_back.tb_next
            )
        finally:
            del trace_back
        return 1

    # pylint: disable=broad-except
    def invoke_main(
        self, arguments=None, cwd=None, suppress_first_line_heading_rule=True
    ):
        """
        Invoke the mainline so that we can capture results.
        """
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

        std_output = io.StringIO()
        std_error = io.StringIO()
        sys.stdout = std_output
        sys.stderr = std_error

        sys.argv = arguments.copy() if arguments else []
        sys.argv.insert(0, self.get_main_name())

        if cwd:
            os.chdir(cwd)

        try:
            returncode = 0
            self.execute_main()
        except SystemExit as this_exception:
            returncode = self.handle_system_exit(this_exception, std_error)
        except Exception:
            returncode = self.handle_normal_exception()
        finally:
            saved_state.restore()

        return InProcessResult(returncode, std_output, std_error)

    # pylint: enable=broad-except
