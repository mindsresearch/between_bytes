# SelfScape Insight Code Standards

## Introduction
This document is intended to lay out a unified style for the code in the Facebook Senior Project repository. Python-related standards are based on [PEP 8](https://peps.python.org/pep-0008/), whereas structural standards are based on the [MVC](https://en.wikipedia.org/wiki/Model-view-controller) and [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) design patterns.

## Definitions
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Standards
### Python Standards
Refer to the [PEP 8](https://peps.python.org/pep-0008/) standard for python standards unless superceded by the rules below:
- REQUIRED naming styles
  - Use `ALLCAPS` for global constants
  - Use `CamelCase` for class names
  - Use `lowercase` or `mixedCase` for variables
  - Use `lower_underscored_case` for methods/functions and packages
- Other naming conventions:
  - Single letter variable names (e.g. `x`) SHOULD only be used in method/function internals

Generally speaking, `$ pylint your_py_file.py` and `$ pylint **/*.py` is a good place to start. While `pylint`'s recommendations are OPTIONAL, efforts SHOULD be made to address the issues it raises.
### Structural Standards
Each feature module is comprised of a multitude of parts:
1. The overarching script (with a short yet descriptive name) in the `features` folder providing command-line run capability and high-level module functionality.
2. If it is helpful to abstract away certain methods/functions, a feature "backend" script can be created called `${feature_name}_backend.py`. Scripts other than `${feature_name}.py` MUST NOT import these "backend" scripts.
3. CSV data MUST only be requested from `main.py` as an argument to `${feature_name}.run()`. A tempfile path will be given for the arg. **YOU** are responsible for making the subsequent changes to `main.py`.
4. With the exception of `json_ingest.py`, features SHOULD NOT touch the data download directories or files.

### Comments & DocStrings
1. Prefer self-documented code to commented code.
2. Comments should be verbose enough that another group member can look at the comment and get a general idea for what that block does.
3. Each module/file MUST have a docstring at the top explaining what it does.
4. Except for the trivial, methods/functions SHOULD have a descriptive docstring as well.
5. Docstrings MUST be in Google-style format (refer to `features/sample.py` for an example).
