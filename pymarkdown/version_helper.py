"""Module to provide features related to version reporting."""

import argparse
import os
import platform
import runpy

from pymarkdown.return_code_helper import ApplicationResult


class VersionHelper:
    """Class to provide features related to version reporting."""

    @staticmethod
    def get_semantic_version() -> str:
        """Get the semantic version associated with the application."""
        file_path = __file__
        assert os.path.isabs(
            file_path
        ), "This should hold on all operating systems.  This is to be sure of that assumption."
        file_path = file_path.replace(os.sep, "/")
        last_index = file_path.rindex("/")
        file_path = f"{file_path[: last_index + 1]}version.py"
        version_meta = runpy.run_path(file_path)
        return str(version_meta["__version__"])

    @staticmethod
    def argparse_subparser_name() -> str:
        """Name associated with the subparser."""
        return "version"

    @staticmethod
    def add_argparse_subparser(subparsers: argparse._SubParsersAction) -> None:  # type: ignore
        """
        Populate the argparse tree to allow for version support.
        """

        new_sub_parser = subparsers.add_parser(
            "version", help="version of the application"
        )

        new_sub_parser.add_argument(
            "--extended",
            dest="show_extended",
            action="store_true",
            default=False,
            help="show extended version information",
        )

    @staticmethod
    def handle_argparse_subparser(args: argparse.Namespace) -> ApplicationResult:
        """Handle the processing of any arguments tagged for this subprocessor."""

        if args.show_extended:
            python_version = f"{platform.python_version()} ({platform.python_implementation()}, {platform.python_compiler()})"
            operating_system = f"{platform.system()} {platform.release()}"

            print(f"PyMarkdown:         {VersionHelper.get_semantic_version()}")
            print(f"Python:             {python_version}")
            print(f"Operating System:   {operating_system}")
        else:
            print(f"{VersionHelper.get_semantic_version()}")
        return ApplicationResult.SUCCESS
