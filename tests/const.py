from enum import Enum
from pathlib import Path

import git

import semantic_release
from semantic_release.cli.commands.main import Cli

PROJ_DIR = Path(__file__).parent.parent.absolute().resolve()


class RepoActionStep(str, Enum):
    CONFIGURE = "CONFIGURE"
    WRITE_CHANGELOGS = "WRITE_CHANGELOGS"
    GIT_CHECKOUT = "GIT_CHECKOUT"
    GIT_COMMIT = "GIT_COMMIT"
    GIT_MERGE = "GIT_MERGE"
    GIT_SQUASH = "GIT_SQUASH"
    GIT_TAG = "GIT_TAG"
    RELEASE = "RELEASE"
    MAKE_COMMITS = "MAKE_COMMITS"


A_FULL_VERSION_STRING = "1.11.567"
A_PRERELEASE_VERSION_STRING = "2.3.4-dev.23"
A_FULL_VERSION_STRING_WITH_BUILD_METADATA = "4.2.3+build.12345"

EXAMPLE_REPO_OWNER = "example_owner"
EXAMPLE_REPO_NAME = "example_repo"
EXAMPLE_HVCS_DOMAIN = "example.com"

DEFAULT_BRANCH_NAME = "main"
INITIAL_COMMIT_MESSAGE = "Initial commit"

MAIN_PROG_NAME = str(semantic_release.__name__).replace("_", "-")
SUCCESS_EXIT_CODE = 0

CHANGELOG_SUBCMD = Cli.SubCmds.CHANGELOG.name.lower()
GENERATE_CONFIG_SUBCMD = Cli.SubCmds.GENERATE_CONFIG.name.lower()
PUBLISH_SUBCMD = Cli.SubCmds.PUBLISH.name.lower()
VERSION_SUBCMD = Cli.SubCmds.VERSION.name.lower()

NULL_HEX_SHA = git.Object.NULL_HEX_SHA

COMMIT_MESSAGE = "{version}\n\nAutomatically generated by python-semantic-release\n"

SUPPORTED_ISSUE_CLOSURE_PREFIXES = [
    "Close",
    "Closes",
    "Closed",
    "Closing",
    "Fix",
    "Fixes",
    "Fixed",
    "Fixing",
    "Resolve",
    "Resolves",
    "Resolved",
    "Resolving",
    "Implement",
    "Implements",
    "Implemented",
    "Implementing",
]

ANGULAR_COMMITS_CHORE = ("ci: added a commit lint job\n",)
# Different in-scope commits that produce a certain release type
ANGULAR_COMMITS_PATCH = (
    *ANGULAR_COMMITS_CHORE,
    "fix: fixed voltage in the flux capacitor\n",
)
ANGULAR_COMMITS_MINOR = (
    *ANGULAR_COMMITS_PATCH,
    "feat: last minute rush order\n",
)
# Take previous commits and insert a breaking change
ANGULAR_COMMITS_MAJOR = (
    *ANGULAR_COMMITS_MINOR,
    "fix!: big change\n\nBREAKING CHANGE: reworked something for previous feature\n",
)

EMOJI_COMMITS_CHORE = (
    ":broom: updated lint & code style\n",
    ":none: updated ci pipeline\n",
)

EMOJI_COMMITS_PATCH = (
    *EMOJI_COMMITS_CHORE,
    ":bug: fixed voltage in the flux capacitor\n",
)
EMOJI_COMMITS_MINOR = (
    *EMOJI_COMMITS_PATCH,
    ":sparkles::pencil: docs for something special\n",
    # Emoji in description should not be used to evaluate change type
    ":sparkles: last minute rush order\n\n:boom: Good thing we're 10x developers\n",
)
EMOJI_COMMITS_MAJOR = (
    *EMOJI_COMMITS_MINOR,
    ":boom: Move to the blockchain\n",
)

# Note - the scipy commit fixtures for commits that should evaluate to the various scopes
# are in tests/fixtures/scipy

EXAMPLE_PROJECT_NAME = "example"
EXAMPLE_PROJECT_VERSION = "0.0.0"
EXAMPLE_PROJECT_LICENSE = "MIT"

# Uses the internal defaults of semantic-release unless otherwise needed for testing
# modify the pyproject toml as necessary for the test using update_pyproject_toml()
# and derivative fixtures
EXAMPLE_PYPROJECT_TOML_CONTENT = rf"""
[project]
license-expression = "{EXAMPLE_PROJECT_LICENSE}"

[tool.poetry]
name = "{EXAMPLE_PROJECT_NAME}"
version = "{EXAMPLE_PROJECT_VERSION}"
description = "Just an example"
license = "{EXAMPLE_PROJECT_LICENSE}"
authors = ["semantic-release <not-a.real@email.com>"]
readme = "README.md"
classifiers = [
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only"
]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.semantic_release]
version_variables = [
    "src/{EXAMPLE_PROJECT_NAME}/_version.py:__version__",
]
version_toml = ["pyproject.toml:tool.poetry.version"]
""".lstrip()

EXAMPLE_SETUP_CFG_CONTENT = rf"""
[metadata]
name = example
version = {EXAMPLE_PROJECT_VERSION}
description = Just an example really
long_description = file: README.md
long_description_content_type = text/markdown
author = semantic-release
author_email = not-a.real@email.com
url = https://github.com/python-semantic-release/python-semantic-release
python_requires = >=3.7


[options]
zip_safe = True
include_package_data = True
packages = find:
install_requires =
    PyYAML==6.0
    pydantic==1.9.0

[options.extras_require]
dev =
    tox
    twine==3.1.1

test =
    pytest
    pytest-cov
    pytest-mock
    pytest-aiohttp

lint =
    flake8
    black>=22.6.0
    isort>=5.10.1

[options.packages.find]
exclude =
    test*

[bdist_wheel]
universal = 1

[coverage:run]
omit = */tests/*

[tools:pytest]
python_files = tests/test_*.py tests/**/test_*.py

[isort]
skip = .tox,venv
default_section = THIRDPARTY
known_first_party = {EXAMPLE_PROJECT_NAME},tests
multi_line_output=3
include_trailing_comma=True
force_grid_wrap=0
use_parentheses=True
line_length=88

[flake8]
max-line-length = 88
""".lstrip()

EXAMPLE_SETUP_PY_CONTENT = rf"""
import re
import sys

from setuptools import find_packages, setup


def _read_long_description():
    try:
        with open("readme.rst") as fd:
            return fd.read()
    except Exception:
        return None


with open("{EXAMPLE_PROJECT_NAME}/_version.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

try:
    from semantic_release import setup_hook

    setup_hook(sys.argv)
except ImportError:
    pass

setup(
    name="{EXAMPLE_PROJECT_NAME}",
    version="{EXAMPLE_PROJECT_VERSION}",
    url="http://github.com/python-semantic-release/python-semantic-release",
    author="semantic-release",
    author_email="not-a.real@email.com",
    description="Just an example",
    long_description=_read_long_description(),
    packages=find_packages(exclude=("tests",)),
    license="MIT",
    install_requires=[
        "click>=7,<9",
        "click_log>=0.3,<1",
        "gitpython>=3.0.8,<4",
        "invoke>=1.4.1,<2",
        "semver>=2.10,<3",
        "twine>=3,<4",
        "requests>=2.25,<3",
        "wheel",
        "python-gitlab>=2,<4",
        # tomlkit used to be pinned to 0.7.0
        # See https://github.com/python-semantic-release/python-semantic-release/issues/336
        # and https://github.com/python-semantic-release/python-semantic-release/pull/337
        # and https://github.com/python-semantic-release/python-semantic-release/issues/491
        "tomlkit~=0.10",
        "dotty-dict>=1.3.0,<2",
        "dataclasses==0.8; python_version < '3.7.0'",
        "packaging",
    ],
    extras_require={{
        "test": [
            "coverage>=5,<6",
            "pytest>=5,<6",
            "pytest-xdist>=1,<2",
            "pytest-mock>=2,<3",
            "pytest-lazy-fixture~=0.6.3",
            "responses==0.13.3",
            "mock==1.3.0",
        ],
        "docs": ["Sphinx==1.3.6", "Jinja2==3.0.3"],
        "dev": ["tox", "isort", "black"],
        "mypy": ["mypy", "types-requests"],
    }},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
""".lstrip()

EXAMPLE_CHANGELOG_MD_CONTENT = r"""
# CHANGELOG
<!-- This is an example changelog -->

## v1.0.0

* Various bugfixes, security enhancements
* Extra cookies to enhance your experience
* ~Removed~ simplified cookie opt-out handling logic

""".lstrip()

EXAMPLE_CHANGELOG_RST_CONTENT = r"""
.. _changelog:
=========
CHANGELOG
=========

..
  example project base changelog

.. _changelog-v1.0.0:

v1.0.0 (1970-01-01)
===================

* Various bugfixes, security enhancements
* Extra cookies to enhance your experience
* ~Removed~ simplified cookie opt-out handling logic
""".lstrip()

EXAMPLE_RELEASE_NOTES_TEMPLATE = r"""
## What's Changed
{%    for type_, commits in release["elements"] | dictsort
%}{{    "### %s" | format(type_ | title)
}}{%    if type_ != "unknown"
%}{%      for commit in commits
%}{{        "* %s" | format(commit.descriptions[0] | trim)
}}{%      endfor
%}{%    endif
%}{%  endfor
%}
""".lstrip()  # noqa: E501

RELEASE_NOTES = "# Release Notes"
