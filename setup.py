"""
Setup file for the PyMarkdown project.
"""

import os
import runpy

from setuptools import setup

INSTALL_REQUIREMENT_FILE = "install-requirements.txt"
PROJECT_README_FILE = "README.md"
ALTERNATE_PYPI_README_FILE = "pypi.md"


def parse_requirements():
    with open(f"{INSTALL_REQUIREMENT_FILE}", "r", encoding="utf-8") as requirement_file:
        lineiter = [line.strip() for line in requirement_file]
    return [line for line in lineiter if line and not line.startswith("#")]


def get_semantic_version():
    version_meta = runpy.run_path(f"./{MODULE_NAME}/version.py")
    return version_meta["__version__"]


def get_project_name():
    version_meta = runpy.run_path(f"./{MODULE_NAME}/version.py")
    return version_meta["__project_name__"]


def get_description():
    version_meta = runpy.run_path(f"./{MODULE_NAME}/version.py")
    return version_meta["__description__"]


def load_readme_file():
    source_file = (
        ALTERNATE_PYPI_README_FILE
        if os.path.exists(ALTERNATE_PYPI_README_FILE)
        else PROJECT_README_FILE
    )
    with open(source_file, "r", encoding="utf-8") as readme_file:
        return readme_file.read()


# Note, the below function does not always work, so we use this until we can find out why it is not working.
PACKAGE_MODULES = [
    "pymarkdown",
    "pymarkdown.block_quotes",
    "pymarkdown.coalesce",
    "pymarkdown.container_blocks",
    "pymarkdown.extension_manager",
    "pymarkdown.extensions",
    "pymarkdown.general",
    "pymarkdown.html",
    "pymarkdown.inline",
    "pymarkdown.leaf_blocks",
    "pymarkdown.links",
    "pymarkdown.list_blocks",
    "pymarkdown.plugin_manager",
    "pymarkdown.plugins",
    "pymarkdown.plugins.utils",
    "pymarkdown.resources",
    "pymarkdown.tokens",
    "pymarkdown.transform_gfm",
    "pymarkdown.transform_markdown",
]


def get_package_modules():
    # return [
    #     next_item[0][2:]
    #     for next_item in os.walk(".")
    #     if os.path.exists(os.path.join(next_item[0], ".external-package"))
    # ]
    return PACKAGE_MODULES


AUTHOR = "Jack De Winter"
AUTHOR_EMAIL = "jack.de.winter@outlook.com"
PROJECT_URL = "https://github.com/jackdewinter/pymarkdown"
PROJECT_URLS = {
    "Documentation": "https://pymarkdown.readthedocs.io/",
    "Change Log": "https://pymarkdown.readthedocs.io/en/latest/changelog/",
}

MODULE_NAME = "pymarkdown"
PACKAGE_NAME = "pymarkdownlnt"
SEMANTIC_VERSION = get_semantic_version()
MINIMUM_PYTHON_VERSION = "3.10.0"

ONE_LINE_DESCRIPTION = get_description()
LONG_DESCRIPTION = load_readme_file()
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

KEYWORDS = ["markdown", "linter", "markdown linter"]
PROJECT_CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
]

setup(
    name=PACKAGE_NAME,
    version=SEMANTIC_VERSION,
    python_requires=f">={MINIMUM_PYTHON_VERSION}",
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
    project_urls=PROJECT_URLS,
    entry_points={
        "console_scripts": [
            "pymarkdown=pymarkdown.__main__:main",
            "pymarkdownlnt=pymarkdown.__main__:main",
        ],
    },
    packages=get_package_modules(),
    include_package_data=True,
    package_data={"": ["*.typed"]},
)
