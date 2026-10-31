"""Module to provide features related to version reporting."""

import argparse
import os
import platform
import runpy
import shutil
import subprocess  # nosec

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
    def _linux_distribution_version() -> str:  # pragma: no cover

        # Try /etc/os-release (or /usr/lib/os-release) for VERSION_ID / NAME.
        # Return e.g. "Ubuntu 22.04" or "Fedora 39".
        # Return "" if not found.
        for path in ("/etc/os-release", "/usr/lib/os-release"):
            if os.path.exists(path):
                data = {}
                with open(path, "r", encoding="utf-8") as fh:
                    for line in fh:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            data[k] = v.strip('"')
                name = data.get("NAME", "").strip()
                version_id = data.get("VERSION_ID", "").strip()
                if name and version_id:
                    return f"{name} {version_id}"
                if version_id:
                    return version_id
        return ""

    @staticmethod
    def _macos_product_version() -> str:  # pragma: no cover

        # Run `sw_vers -productVersion` (or `sw_vers -productVersionName`
        # depending on macOS) to obtain e.g. "14.5".
        # Return "" on failure.
        try:
            if (executable := shutil.which("sw_vers")) is None:
                return ""
            return (
                subprocess.check_output(  # nosec
                    [executable, "-productVersion"],
                    stderr=subprocess.DEVNULL,
                    timeout=2,
                )
                .decode("utf-8", "ignore")
                .strip()
            )
        except (OSError, subprocess.SubprocessError):
            return ""

    @staticmethod
    def get_operating_system() -> str:  # pragma: no cover
        """
        Get a human-readable string describing the operating system.

        On Windows, platform.release() reports the "compatibility version"
        (always "10") rather than the real major version.  Use the NT
        build number (platform.version()) to distinguish Windows 11
        (build 22000+) from Windows 10 (build 15063 - 21999).

        On Linux and macOS, platform.release() only reports the kernel
        release.  Prefer the distribution version (e.g. "Ubuntu 22.04")
        or the macOS product version (e.g. "14.5"), falling back to the
        kernel release when those are unavailable.
        """
        system = platform.system()
        release = platform.release()

        if system == "Windows":
            try:
                nt_build = int(platform.version())
            except ValueError:
                nt_build = 0
            if nt_build >= 22000:
                release = "11"
        elif system == "Linux":
            if dist := VersionHelper._linux_distribution_version():
                release = dist
        elif system == "Darwin":
            if mac := VersionHelper._macos_product_version():
                release = mac
        # ... existing code ...
        return f"{system} {release}"

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

            print(f"PyMarkdown:         {VersionHelper.get_semantic_version()}")
            print(f"Python:             {python_version}")
            print(f"Operating System:   {VersionHelper.get_operating_system()}")
        else:
            print(f"{VersionHelper.get_semantic_version()}")
        return ApplicationResult.SUCCESS
