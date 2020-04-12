==================================
python-anyconfig-fortios-backend
==================================

.. image:: https://img.shields.io/pypi/v/anyconfig-fortios-backend.svg
   :target: https://pypi.python.org/pypi/anyconfig-fortios-backend/
   :alt: [Latest Version]

.. image:: https://img.shields.io/pypi/pyversions/anyconfig-fortios-backend.svg
   :target: https://pypi.python.org/pypi/anyconfig-fortios-backend/
   :alt: [Python versions]

.. image:: https://img.shields.io/pypi/l/anyconfig-fortios-backend.svg
   :target: https://pypi.python.org/pypi/anyconfig-fortios-backend/
   :alt: MIT License

.. image:: https://img.shields.io/travis/ssato/python-anyconfig-fortios-backend.svg
   :target: https://travis-ci.org/ssato/python-anyconfig-fortios-backend
   :alt: Test status

.. .. image:: https://img.shields.io/coveralls/ssato/python-anyconfig-fortios-backend.svg
   :target: https://coveralls.io/r/ssato/python-anyconfig-fortios-backend
   :alt: Coverage Status

.. image:: https://img.shields.io/lgtm/grade/python/g/ssato/python-anyconfig-fortios-backend.svg
   :target: https://lgtm.com/projects/g/ssato/python-anyconfig-fortios-backend/context:python
   :alt: [Code Quality by LGTM]

This is a backend module for python-anyconfig to support to load and parse
fortios' "show \*configuration" outputs.

- Author: Satoru SATOH <satoru.satoh@gmail.com>
- License: MIT

SEE ALSO:

- python-anyconfig: https://pypi.python.org/pypi/anyconfig
- Fortinet: https://www.fortinet.com/
- Download:

  - PyPI: https://pypi.python.org/pypi/anyconfig-fortios-backend
  - Copr RPM repos: https://copr.fedoraproject.org/coprs/ssato/python-anyconfig/

Build & Install
================

If you're Fedora or Red Hat Enterprise Linux user, try::

  $ python setup.py srpm && mock dist/<package>-<ver_dist>.src.rpm
  
or::

  $ python setup.py rpm

and install built RPMs. 

Otherwise, try usual ways to build and/or install python modules such like
'python setup.py bdist', etc.

.. vim:sw=2:ts=2:et:
