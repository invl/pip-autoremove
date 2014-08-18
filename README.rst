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

First, install ``pip-autoremove``

.. code-block:: sh

    $ pip install pip-autoremove

Install a package which has dependencies, e.g. ``Flask``:

.. code-block:: sh

    $ pip install Flask

    ...
    Successfully installed Flask Werkzeug Jinja2 itsdangerous markupsafe
    Cleaning up...

Uninstall it and all its unused dependencies:

.. code-block:: sh

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

Usage
-----

.. code-block:: sh

    Usage: pip-autoremove [-hy] NAME...

    Options:
      --version   show program's version number and exit
      -h, --help  show this help message and exit
      -y, --yes   don't ask for confirmation of uninstall deletions.


Installation
------------

.. code-block:: sh

    $ pip install pip-autoremove
