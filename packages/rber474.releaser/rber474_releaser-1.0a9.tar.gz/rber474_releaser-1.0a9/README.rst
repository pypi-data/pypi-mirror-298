
.. image:: https://coveralls.io/repos/github/rber474.releaser/badge.svg?branch=main
    :target: https://coveralls.io/github/rber474.releaser?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/rber474.releaser/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/rber474.releaser

.. image:: https://img.shields.io/pypi/v/rber474.releaser.svg
    :target: https://pypi.python.org/pypi/rber474.releaser/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/rber474.releaser.svg
    :target: https://pypi.python.org/pypi/rber474.releaser
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/rber474.releaser.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/rber474.releaser.svg
    :target: https://pypi.python.org/pypi/rber474.releaser/
    :alt: License


================
rber474.releaser
================

Custom releaser hooks for JIRA project based on zest.releaser and cs.zestreleaser.changelog.
This hook extract the commit messages from the last release tag to the current tag and create the towncrier news fragments, based on tbhe JIRA issue and the towncrier type.

Currently it only supports GIT VCS logs.

The commit messages must be in the following format::

    <optional prefix> <issue_name>-<issue_number> <towncrier type> <message> [<author>]


Author will be extracted from the git history.

Examples
--------

The following commit messages are valid:

Revert WEBAGL-1234 feature Add new feature
Add WEBAGL-1234 feature new feature
WEBAGL-1235 bugfix Fix AttributeError RequestContainer object has no attribute getClientForURL

Fragmentes files will be created in the following format:

**news/feature/WEBAGL-1234.feature** ::

    Add new feature [Rafael Bermúdez Horcajada <myemail@email.com>]
    Revert new feature [Rafael Bermúdez Horcajada <myemail@email.com>]


**news/feature/WEBAGL-1235.bugfix** ::

    Fix AttributeError RequestContainer object has no attribute getClientForURL [Rafael Bermúdez Horcajada <myemail@email.com>]
    


Installation
------------

Using pip::

    $ pip install rber474.releaser


Authors
-------

- Rafael Bermúdez Horcajada


Contributors
------------

Put your name here, you deserve it!

- ?


Contribute
----------

- Issue Tracker: https://github.com/rber474.releaser/issues
- Source Code: https://github.com/rber474.releaser


License
-------

The project is licensed under the GPLv2.
