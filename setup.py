#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""setup.py."""
from setuptools import find_packages, setup

CHECK_REQUIRES = ("docutils", "pygments", "readme-renderer")

CLASSIFIERS = (
    # complete classifier list:
    #    http://pypi.python.org/pypi?%3Aaction=list_classifiers
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Unix",
    "Operating System :: POSIX",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Utilities",
)

DOC_REQUIRES = "sphinx"

INSTALL_REQUIRES = (
    "python-dateutil",
    "pandas",
    "pymongo",
    "sqlalchemy",
    "gensim",
    "dsdk @ git+https://github.com/pennsignals/dsdk.git@master",
)

LINT_REQUIRES = (
    "black",
    "flake8",
    "flake8-bugbear",
    "flake8-commas",
    "flake8-comprehensions",
    "flake8-docstrings",
    "flake8-logging-format",
    "flake8-mutable",
    "flake8-sorted-keys",
    "isort",
    "mypy",
    "pep8-naming",
    "pre-commit",
    "pylint",
)

KEYWORDS = (
    # eg: 'keyword1', 'keyword2', 'keyword3',
)
PROJECT_URLS = {
    "Changelog": "https://dsdkexample.readthedocs.io/en/latest/changelog.html",
    "Documentation": "https://dsdkexample.readthedocs.io/",
    "Issue Tracker": "https://github.com/pennsignals/dsdkexample/issues",
}

SETUP_REQUIRES = ("pytest-runner", "setuptools_scm>=3.3.3")

TEST_REQUIRES = ("coverage", "pytest", "pytest-cov", "tox")


setup(
    name="dsdkexample",
    description="Sepsis predictor based on NLP on clinical notes.",
    author="Michael Becker",
    author_email="michael.becker@uphs.upenn.edu",
    classifiers=list(CLASSIFIERS),
    entry_points={"console_scripts": ["dsdkexample = dsdkexample.cli:main"]},
    extras_require={
        "check": CHECK_REQUIRES,
        "doc": DOC_REQUIRES,
        "lint": LINT_REQUIRES,
        "test": TEST_REQUIRES,
    },
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    keywords=list(KEYWORDS),
    packages=find_packages("src"),
    package_dir={"": "src"},
    project_urls=PROJECT_URLS,
    python_requires=">=3.7",
    setup_requires=SETUP_REQUIRES,
    tests_require=LINT_REQUIRES + TEST_REQUIRES,
    url="https://github.com/pennsignals/dsdkexample",
    use_scm_version={"fallback_version": "0.1.0", "local_scheme": "dirty-tag"},
    zip_safe=False,
)
