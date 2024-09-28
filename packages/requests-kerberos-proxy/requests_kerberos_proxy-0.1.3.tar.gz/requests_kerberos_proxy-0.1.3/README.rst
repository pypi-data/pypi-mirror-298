.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=======================
requests-kerberos-proxy
=======================


    An front end to requests in order to use Kerberos behind a proxy


This package provides a work around in order to deal with a proxy if you want to use kerberos


Install
=======

Before installing this module, the underlying Kerberos C libraries and Python development headers need to be installed.
An example of how to do this for some Linux distributions is shown below::

    # For Debian based distros
    apt-get install gcc python3-dev libkrb5-dev

    # For EL based distros
    dnf install gcc python3-devel krb5-devel

For Windows this is not required.


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
