.. raw:: html

    <p align="center">
        <img src="main/static/img/logo_cranberry.svg" width="125px;" />
    </p>
    <h1 align="center">notabanane</h1>
    <p align="center">
        Healthy recipes for real life adventurers.
    </p>
    <p align="center">
        <a href="https://github.com/ellmetha/notabanane/actions" rel="nofollow"><img alt="Build status" src="https://github.com/ellmetha/django-precise-bbcode/workflows/ci-python/badge.svg?branch=master" style="max-width:100%;"></a>
        <a href="https://github.com/ellmetha/notabanane/actions" rel="nofollow"><img alt="Build status" src="https://github.com/ellmetha/django-precise-bbcode/workflows/ci-nodejs/badge.svg?branch=master" style="max-width:100%;"></a>
        <a href="https://codecov.io/github/ellmetha/notabanane" rel="nofollow"><img alt="Codecov status" src="https://codecov.io/gh/ellmetha/notabanane/branch/master/graph/badge.svg" style="max-width:100%;"></a>
    </p>

|
|

`Nota Banane <https://notabanane.com>`_ is a blog application about healthy food and diet. It features recipes and other
articles on various subjects.

.. contents:: Table of Contents
    :local:

System requirements
===================

* Python_ 3.8+
* PostgreSQL_ 9.4+
* Node_ 11.0+
* Poetry_ 1.0+

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
.. _Poetry: https://python-poetry.org/
.. _PostgreSQL: https://www.postgresql.org/
.. _Python: https://www.python.org
