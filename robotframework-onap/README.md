Robotframework-ONAP
=======================

Robot Framework library for ONAP testing.

Packages
--------
- ONAPLibrary - Robot keywords for ONAP components (AAI, SDC, SO, SDNC, etc.)
- vcpeutils - vCPE service orchestration utilities

Installation
------------

```bash
pip install -e .
```

Development Setup
-----------------

1. Create virtual environment (from repo root):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install in development mode with test dependencies:

```bash
pip install -e .
pip install -r test-requirements.txt
```

3. Run tests:

```bash
pytest tests/ -v
```

Or with coverage:

```bash
pytest tests/ --cov=ONAPLibrary --cov=vcpeutils --cov-report=html
```

Using tox
---------
Available targets:

- py3: Run unit tests with coverage
- pep8: Python linting with flake8
- pylint: Python linting with pylint

Run all targets:

```bash
tox
```

Run specific target:

```bash
tox -e py3
tox -e pep8
tox -e pylint
```

Requirements
------------
- Python 3.7+
- See requirements.txt for dependencies
