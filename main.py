"""
Module to provide for a simple bootstrap for the project.
"""

import cProfile
import os

from pymarkdown.main import PyMarkdownLint

class Main:
    """
    Class to provide for a simple bootstrap for the project.
    """

    def main(self):
        """
        Main entrance point.
        """
        try:
            import cProfile
            import os

            from pymarkdown.main import PyMarkdownLint

            performance_run_indicator = (
                os.getenv("PYMARKDOWNLINT__PERFRUN", "0").strip().lower()
            )
            if performance_run_indicator in ("1", "true"):
                cProfile.run(
                    "from pymarkdown.main import PyMarkdownLint; PyMarkdownLint().main()",
                    "p0.prof",
                )
            else:
                PyMarkdownLint().main()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    Main().main()
