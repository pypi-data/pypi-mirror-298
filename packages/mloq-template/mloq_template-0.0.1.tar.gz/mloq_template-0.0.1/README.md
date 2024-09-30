========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |github-actions| |codecov|
    * - package
      - |version| |wheel| |supported-versions| |supported-implementations| |commits-since|
.. |docs| image:: https://readthedocs.org/projects/mloq-template/badge/?style=flat
    :target: https://readthedocs.org/projects/mloq-template/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/guillemdb/mloq-template/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/guillemdb/mloq-template/actions

.. |codecov| image:: https://codecov.io/gh/guillemdb/mloq-template/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://app.codecov.io/github/guillemdb/mloq-template

.. |version| image:: https://img.shields.io/pypi/v/mloq-template.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/mloq-template

.. |wheel| image:: https://img.shields.io/pypi/wheel/mloq-template.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/mloq-template

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/mloq-template.svg
    :alt: Supported versions
    :target: https://pypi.org/project/mloq-template

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/mloq-template.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/mloq-template

.. |commits-since| image:: https://img.shields.io/github/commits-since/guillemdb/mloq-template/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/guillemdb/mloq-template/compare/v0.0.0...main



.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install mloq-template

You can also install the in-development version with::

    pip install https://github.com/guillemdb/mloq-template/archive/main.zip


Documentation
=============


https://mloq-template.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
