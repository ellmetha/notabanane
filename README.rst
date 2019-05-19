notabanane.com
##############

.. contents:: Table of Contents
    :local:

System requirements
===================

* Python_ 3.6+
* PostgreSQL_
* Node_ 7.0+
* Pipenv_ 3.5+

Installation
============

.. code-block:: shell

  $ make
  $ cp .env.json.example .env.json     # Initializes the environment settings
  $ sed -i .bak "s/.*__whoami__.*/  \"DB_USER\": \"$USER\",/" .env.json
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

.. _Node: https://nodejs.org/en/
.. _Pipenv: https://github.com/kennethreitz/pipenv
.. _PostgreSQL: https://www.postgresql.org/
.. _Python: https://www.python.org
