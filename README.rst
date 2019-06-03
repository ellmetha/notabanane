notabanane.com
##############

.. image:: https://travis-ci.org/ellmetha/notabanane.svg?branch=master
    :target: https://travis-ci.org/ellmetha/notabanane

.. image:: https://codecov.io/gh/ellmetha/notabanane/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ellmetha/notabanane

|

Nota Banane is a blog application about healthy food and diet. It features recipes and other
articles on various subjects.

.. contents:: Table of Contents
    :local:

System requirements
===================

* Python_ 3.7+
* PostgreSQL_ 9.4+
* Node_ 11.0+
* Pipenv_ 3.5+

Installation
============

If all the above system dependencies are properly installed on the target system, it should be
possible to install the project using the following command:

.. code-block:: shell

  $ make init

This command will take care of installing the dependencies, initializing the environment-specific
configuration values, building the development assets and preparing the database.

Usage
=====

The development server can be started using the following command:

.. code-block:: shell

  $ make server

License
=======

GPLv3. See ``LICENSE`` for more details.

.. _Node: https://nodejs.org/en/
.. _Pipenv: https://github.com/kennethreitz/pipenv
.. _PostgreSQL: https://www.postgresql.org/
.. _Python: https://www.python.org
