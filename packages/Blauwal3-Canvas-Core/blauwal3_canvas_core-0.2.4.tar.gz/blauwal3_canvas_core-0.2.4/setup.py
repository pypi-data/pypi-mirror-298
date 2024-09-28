#! /usr/bin/env python
from setuptools import setup, find_packages

NAME = "Blauwal3-Canvas-Core"
VERSION = "0.2.4"
DESCRIPTION = "蓝鲸核心"

with open("README.rst", "rt", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

URL = "https://bo.dashenglab.com/"
AUTHOR = "大圣实验楼"
AUTHOR_EMAIL = 'dashenglab@163.com'

LICENSE = "GPLv3"
DOWNLOAD_URL = 'https://github.com/biolab/orange-canvas-core'
PACKAGES = find_packages()

PACKAGE_DATA = {
    "orangecanvas": ["icons/*.svg", "icons/*png", "locale/*.yml", "locale/*/*.yml"],
    "orangecanvas.styles": ["*.qss", "orange/*.svg"],
}

INSTALL_REQUIRES = (
    "AnyQt>=0.2.0",
    "docutils",
    "commonmark>=0.8.1",
    "requests",
    "requests-cache",
    "pip>=18.0",
    "dictdiffer",
    "qasync>=0.10.0",
    "importlib_metadata>=4.6; python_version<'3.10'",
    "importlib_resources; python_version<'3.9'",
    "typing_extensions",
    "packaging",
    "numpy",
    "python-i18n"
)

CLASSIFIERS = (
    "Development Status :: 1 - Planning",
    "Environment :: X11 Applications :: Qt",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Topic :: Scientific/Engineering :: Visualization",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
)

EXTRAS_REQUIRE = {
    'DOCBUILD': ['sphinx', 'sphinx-rtd-theme'],
}

PROJECT_URLS = {
    "Bug Reports": "https://github.com/biolab/orange-canvas-core/issues",
    "Source": "https://github.com/biolab/orange-canvas-core/",
    "Documentation": "https://orange-canvas-core.readthedocs.io/en/latest/",
}

PYTHON_REQUIRES = ">=3.8"

if __name__ == "__main__":
    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/x-rst",
        url=URL,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        license=LICENSE,
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        project_urls=PROJECT_URLS,
        python_requires=PYTHON_REQUIRES,
    )
