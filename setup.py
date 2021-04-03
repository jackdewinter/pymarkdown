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
    version_meta = runpy.run_path("./pymarkdown/version.py")
    return version_meta["__version__"]


def load_readme_file():
    with open("README.md", "r") as readme_file:
        return readme_file.read()


def ensure_scripts(linux_scripts):
    """
    Creates the proper script names required for each platform (taken from PyLint)
    """
    if util.get_platform()[:3] == "win":
        return linux_scripts + [script + ".bat" for script in linux_scripts]
    return linux_scripts


AUTHOR = "Jack De Winter"
AUTHOR_EMAIL = "jack.de.winter@outlook.com"
PROJECT_URL = "https://github.com/jackdewinter/pymarkdown"

PACKAGE_NAME = "PyMarkdown"
SEMANTIC_VERSION = get_semantic_version()
MINIMUM_PYTHON_VERSION = "3.8.0"

ONE_LINE_DESCRIPTION = "A GitHub Flavored Markdown compliant Markdown linter."
LONG_DESCRIPTION = load_readme_file()
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

KEYWORDS = ["markdown", "linter", "markdown linter"]
PROJECT_CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    'Environment :: Console',
    "Programming Language :: Python :: 3.8",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

PACKAGE_MODULES=[
        "pymarkdown",
        "pymarkdown.extensions",
        "pymarkdown.plugins",
        "pymarkdown.resources",
    ]
PACKAGE_SCRIPTS=ensure_scripts(["scripts/pymarkdown"])

setup(
    name=PACKAGE_NAME,
    version=SEMANTIC_VERSION,
    python_requires=">=" + MINIMUM_PYTHON_VERSION,
    install_requires=parse_requirements(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=PROJECT_URL,
    description=ONE_LINE_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    keywords=KEYWORDS,
    classifiers=PROJECT_CLASSIFIERS,
    scripts=PACKAGE_SCRIPTS,
    packages=PACKAGE_MODULES,
    data_files=[('Lib/site-packages/pymarkdown/resources', ['pymarkdown/resources/entities.json'])]
)
