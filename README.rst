pip-autoremove
==============

.. image:: https://pypip.in/d/pip-autoremove/badge.png
        :target: https://pypi.python.org/pypi/pip-autoremove/

.. image:: https://pypip.in/v/pip-autoremove/badge.png
        :target: https://pypi.python.org/pypi/pip-autoremove/

.. image:: https://pypip.in/license/pip-autoremove/badge.png
        :target: https://pypi.python.org/pypi/pip-autoremove/

Remove a package and its unused dependencies.


Usage
-----

.. code-block:: sh

    $ pip install Flask

    Installing collected packages: Flask, Werkzeug, Jinja2, itsdangerous, markupsafe
      Running setup.py install for Flask
      Running setup.py install for Werkzeug
      Running setup.py install for Jinja2
      Running setup.py install for itsdangerous
      Running setup.py install for markupsafe
    Successfully installed Flask Werkzeug Jinja2 itsdangerous markupsafe
    Cleaning up...

.. code-block:: sh

    $ pip-autoremove Flask -y

    Uninstalling:
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


Installation
------------

.. code-block:: bash

    $ pip install pip-autoremove
