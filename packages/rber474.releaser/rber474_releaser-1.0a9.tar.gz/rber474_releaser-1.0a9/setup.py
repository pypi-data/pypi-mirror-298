"""Installer for the rber474.releaser package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="rber474.releaser",
    version="1.0a9",
    description="Custom releaser hooks for ONCE project based on zest.releaser",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Archiving :: Packaging",
        "Topic :: System :: Installation/Setup",
        "Topic :: Utilities",
    ],
    keywords="zest.releaser release upload custom PyPI SCP SFTP package sdist",
    author="Rafael Bermúdez Horcajada",
    author_email="rber474@gmail.com",
    url="https://github.com/rber474/rber474.releaser",
    project_urls={
        "PyPI": "https://pypi.org/project/rber474.releaser/",
        "Source": "https://github.com/rber474/rber474.releaser",
        "Tracker": "https://github.com/rber474/rber474.releaser/issues",
        # 'Documentation': 'https://rber474.releaser.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["rber474", "rber474.releaser"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.9",
    install_requires=[
        "setuptools >= 68.0.0",
        "zest.releaser",
        "zestreleaser.towncrier",
        "towncrier",
    ],
    extras_require={
        "test": [
            "wheel",
            "zope.testing",
            "zope.testrunner",
        ],
    },
    entry_points={
        "zest.releaser.prereleaser.before": [
            "create_newsfile = rber474.releaser.towncrier:create_newsfile",
        ],
    },
)
