"""
Setup file for the PyMarkdown project.
"""

import runpy

from setuptools import setup


def parse_requirements():
    with open("install-requirements.txt", "r", encoding="utf-8") as requirement_file:
        lineiter = [line.strip() for line in requirement_file]
    return [line for line in lineiter if line and not line.startswith("#")]


def get_semantic_version():
    version_meta = runpy.run_path("./pymarkdown/version.py")
    return version_meta["__version__"]


def load_readme_file():
    with open("README.md", "r", encoding="utf-8") as readme_file:
        return readme_file.read()


AUTHOR = "Jack De Winter"
AUTHOR_EMAIL = "jack.de.winter@outlook.com"
PROJECT_URL = "https://github.com/jackdewinter/pymarkdown"
PROJECT_URLS = {
    "Change Log": "https://github.com/jackdewinter/pymarkdown/blob/main/changelog.md",
}

PACKAGE_NAME = "pymarkdownlnt"
SEMANTIC_VERSION = get_semantic_version()
MINIMUM_PYTHON_VERSION = "3.8.0"

ONE_LINE_DESCRIPTION = "A GitHub Flavored Markdown compliant Markdown linter."
LONG_DESCRIPTION = load_readme_file()
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

KEYWORDS = ["markdown", "linter", "markdown linter"]
PROJECT_CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Natural Language :: English",
]

PACKAGE_MODULES = [
    "pymarkdown",
    "pymarkdown.block_quotes",
    "pymarkdown.container_blocks",
    "pymarkdown.extension_manager",
    "pymarkdown.extensions",
    "pymarkdown.html",
    "pymarkdown.inline",
    "pymarkdown.leaf_blocks",
    "pymarkdown.links",
    "pymarkdown.list_blocks",
    "pymarkdown.plugin_manager",
    "pymarkdown.plugins",
    "pymarkdown.resources",
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
    packages=PACKAGE_MODULES,
    include_package_data=True,
)
