import os
import sys
import traceback
import io
import difflib


class InProcessResult:
    def __init__(self, return_code, std_out, std_err):
        self.return_code = return_code
        self.std_out = std_out
        self.std_err = std_err

    def assert_results(self, stdout=None, stderr=None, error_code=0):
        """
        Assert the results are as expected in the "assert" phase.
        """

        try:
            if stdout:
                if self.std_out.getvalue() != stdout:
                    diff = difflib.ndiff(
                        stdout.splitlines(), self.std_out.getvalue().splitlines()
                    )

                    diff_values = "\n".join(list(diff))
                    assert False, "Stdout not as expected:\n" + diff_values
            else:
                assert not self.std_out.getvalue()

            if stderr:
                if self.std_err.getvalue() != stderr:
                    diff = difflib.ndiff(
                        stderr.splitlines(), self.std_err.getvalue().splitlines()
                    )
                    diff_values = "\n".join(list(diff))
                    assert False, "Stderr not as expected:\n" + diff_values
            else:
                assert not self.std_err.getvalue()

            assert self.return_code == error_code, (
                "Actual error code ("
                + str(self.return_code)
                + ") and expected error code ("
                + str(error_code)
                + ") differ."
            )

        finally:
            self.std_out.close()
            self.std_err.close()

class InProcessExecution:

    def efg(self):
        pass

    def ghi(self):
        return "bob"

    def abc(self, arguments = []):

        saved_stdout = sys.stdout
        saved_stderr = sys.stderr
        saved_cwd = os.getcwd()
        saved_env = os.environ
        saved_argv = sys.argv

        std_output = io.StringIO()
        sys.stdout = std_output

        std_error = io.StringIO()
        sys.stderr = std_error

        sys.argv = []
        sys.argv.append(self.ghi())
        for i in arguments:
            sys.argv.append(i)
        

        try:
            returncode = 0
            self.efg()
        except SystemExit as exc:
            returncode = exc.code
            if isinstance(returncode, str):
                std_error.write('{}\n'.format(exc))
                returncode = 1
            elif returncode is None:
                returncode = 0
        except Exception as exc:
            returncode = 1
            try:
                et, ev, tb = sys.exc_info()
                traceback.print_exception(et, ev, tb.tb_next)
            finally:
                del tb
        finally:
            os.chdir(saved_cwd)
            os.environ = saved_env
            sys.argv = saved_argv
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr

        return InProcessResult(returncode, std_output, std_error)
