pip-autoremove
==============

.. image:: https://pypip.in/d/pip-autoremove/badge.png
        :target: https://pypi.python.org/pypi/pip-autoremove/

.. image:: https://pypip.in/v/pip-autoremove/badge.png
        :target: https://pypi.python.org/pypi/pip-autoremove/

.. image:: https://pypip.in/license/pip-autoremove/badge.png
        :target: https://pypi.python.org/pypi/pip-autoremove/


Remove a package and its unused dependencies.


Quickstart
----------

First, install ``pip-autoremove``::

    $ pip install pip-autoremove

Install a package which has dependencies, e.g. ``Flask``::

    $ pip install Flask

    ...
    Successfully installed Flask Werkzeug Jinja2 itsdangerous markupsafe
    Cleaning up...

Uninstall it and all its unused dependencies::

    $ pip-autoremove Flask -y

    Flask 0.10.1 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
        Werkzeug 0.9.6 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
        Jinja2 2.7.3 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
            MarkupSafe 0.23 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
        itsdangerous 0.24 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)

    Uninstalling MarkupSafe:
      Successfully uninstalled MarkupSafe
    Uninstalling Jinja2:
      Successfully uninstalled Jinja2
    Uninstalling itsdangerous:
      Successfully uninstalled itsdangerous
    Uninstalling Werkzeug:
      Successfully uninstalled Werkzeug
    Uninstalling Flask:
      Successfully uninstalled Flask

Remove multiple packages and their dependencies at once::

    $ pip install Flask Sphinx

    ...
    Successfully installed Flask Sphinx Werkzeug Jinja2 itsdangerous Pygments docutils markupsafe
    Cleaning up...

::

    $ pip-autoremove Flask Sphinx -y

    Sphinx 1.2.2 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
        Jinja2 2.7.3 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
            MarkupSafe 0.23 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
        Pygments 1.6 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
        docutils 0.12 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
    Flask 0.10.1 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
        Werkzeug 0.9.6 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
        Jinja2 2.7.3 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
            MarkupSafe 0.23 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
        itsdangerous 0.24 (/tmp/pip-autoremove/.venv/lib/python2.7/site-packages)
    ...

Usage
-----

::

    Usage: pip-autoremove [OPTION]... [NAME]...

    Options:
      --version     show program's version number and exit
      -h, --help    show this help message and exit
      -l, --list    list unused dependencies, but don't uninstall them.
      -L, --leaves  list leaves (packages which are not used by any others).
      -y, --yes     don't ask for confirmation of uninstall deletions.

Installation
------------

::

    $ pip install pip-autoremove
