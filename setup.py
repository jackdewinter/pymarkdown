"""
Setup file for the PyMarkdown project.
"""

import runpy
from distutils import util

from setuptools import setup


def parse_requirements():
    lineiter = (line.strip() for line in open("install-requirements.txt", "r"))
    return [line for line in lineiter if line and not line.startswith("#")]


def get_semantic_version():
    version_meta = runpy.run_path("./version.py")
    return version_meta["__version__"]


def load_readme_file():
    with open("README.md", "r") as readme_file:
        return readme_file.read()


def ensure_scripts(linux_scripts):
    """
    Creates the proper script names required for each platform (taken from PyLint)
    """
    if util.get_platform()[:3] == "win":
        return linux_scripts + [script + ".cmd" for script in linux_scripts]
    return linux_scripts


PACKAGE_NAME = "PyMarkdown"
SEMANTIC_VERSION = get_semantic_version()
MINIMUM_PYTHON_VERSION = "3.8.0"

AUTHOR = "Jack De Winter"
AUTHOR_EMAIL = "jack.de.winter@outlook.com"

ONE_LINE_DESCRIPTION = "A GitHub Flavored Markdown compliant Markdown linter."
LONG_DESCRIPTION = load_readme_file()
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"
KEYWORDS = ["markdown", "linter", "markdown linter"]

PROJECT_CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3.7",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

setup(
    name=PACKAGE_NAME,  # check
    version=SEMANTIC_VERSION,  # check
    python_requires=">=" + MINIMUM_PYTHON_VERSION,  # check
    install_requires=parse_requirements(),  # check
    author=AUTHOR,  # check
    author_email=AUTHOR_EMAIL,  # check
    description=ONE_LINE_DESCRIPTION,  # check
    long_description=LONG_DESCRIPTION,  # check
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,  # check
    keywords=KEYWORDS,
    classifiers=PROJECT_CLASSIFIERS,  # check
    scripts=ensure_scripts(["scripts/pymarkdown"]),  # check
    packages=[
        "pymarkdown",
        "pymarkdown.extensions",
        "pymarkdown.plugins",
        "pymarkdown.resources",
    ],
    # py_modules=["pymarkdownz"],
    # entry_points={"console_scripts": ["pymarkdown=pymarkdown.main:main"]},
)
