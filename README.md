Python Testing Utils
=======================

Robot Framework library and utilities for ONAP end-to-end testing.

Project Structure
-----------------
- robotframework-onap/ - Main Robot Framework library package
  - ONAPLibrary/ - Robot keywords for ONAP components (AAI, SDC, SO, etc.)
  - vcpeutils/ - vCPE-specific utilities
  - tests/ - Unit tests

Quick Start
-----------

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the package in development mode:

```bash
cd robotframework-onap
pip install -e .
pip install -r test-requirements.txt
```

3. Run tests:

```bash
pytest tests/ -v
```

4. Run linting:

```bash
tox -e pep8
tox -e pylint
```

Using tox
---------
Run all checks (tests, pep8, pylint):

```bash
cd robotframework-onap
tox
```

Run specific target:

```bash
tox -e py3      # Run tests with coverage
tox -e pep8     # Run flake8 linting
tox -e pylint   # Run pylint
```

Requirements
------------
- Python 3.7+
