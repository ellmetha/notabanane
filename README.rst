notabanane.com
##############

.. contents:: Table of Contents
    :local:

Requirements
============

Python_ 3.6+, Pipenv_ 3.5+, Django_ 2.2.

Installation
============

.. code-block:: shell

  $ git clone https://github.com/ellmetha/notabanane && cd machina-vanilla
  $ make
  $ cp .env.json.example .env.json     # Initializes the environment settings
  $ make db
  $ make migrate
  $ make superuser

Usage
=====

.. code-block:: shell

  $ make server

License
=======

GPLv3. See ``LICENSE`` for more details.

.. _Django: https://www.djangoproject.com
.. _Pipenv: https://github.com/kennethreitz/pipenv
.. _Python: https://www.python.org
