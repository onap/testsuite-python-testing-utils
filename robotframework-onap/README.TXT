Robotframework-ONAP
=======================

Robot framework plugin to work with ONAP.
It provides 3 packages:

* ONAPLibrary
* vcpeutils
* loadtest

A tox file has been created with the following targets:

* py3: run unit tests using python3 + provide unit test coverage information
* py27: run unit tests using python2.7
* pep8: python linting with flake8 (python3)
* pylint: python linting with pylint (python3), pylint provide a rate estimation

You can run all the target one after the other by typing `tox` from
robotframework-onap directory. Or if you want to specify a single target type
`tox -epep8` 
