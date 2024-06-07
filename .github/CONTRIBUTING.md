# Contributing to Between Bytes

## Introduction
Welcome to the Between Bytes project! This document provides guidelines for contributing to the Facebook Senior Project repository. Our code standards are aligned with [PEP 8](https://peps.python.org/pep-0008/) for Python and follow the [MVC](https://en.wikipedia.org/wiki/Model-view-controller) and [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) design patterns to ensure maintainability and scalability.

## Definitions
The terms "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" are defined as per [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) to clarify requirement levels.

## Code Standards
### Python Standards
- **Naming Conventions**:
  - Global constants: `ALLCAPS`
  - Class names: `CamelCase`
  - Variables: `lowercase` or `lower_underscored_case`
  - Functions/methods and packages: `lower_underscored_case`
  - Single-letter variables (e.g., `x`): Use only within method/function internals
- **Linting**:
  - A `pylintrc` file is provided in the root directory to standardize linting practices.
  - Automatically run `pylint` on your code by pushing to GitHub; our workflow checks each push against the `pylintrc` standards.
  - Manual linting can also be performed locally:
    ```bash
    pylint your_py_file.py
    pylint **/*.py
    ```

### Structural Standards
- **Module Organization**:
  - Feature scripts in `features/` should be command-line executable with descriptive names.
  - Backend functionality can be abstracted to `${feature_name}_backend.py`, which must not be imported outside its primary feature script.

### Documentation Standards
- **Code Documentation**:
  - Use self-documenting code where possible.
  - Provide verbose comments for complex logic to aid understanding.
  - All modules/files require a docstring at the top explaining their purpose.
  - Non-trivial methods/functions should have detailed Google-style docstrings, see `features/sample.py` for examples.

## How to Contribute

> [!TIP]
> We are planning to introduce a testing suite using `pytest` in the near future. Contributions to this effort are welcome and appreciated!

1. **Fork the Repository**: Start by forking the repository and cloning your fork to your machine.
2. **Set Up Your Development Environment**: Set up a virtual environment and install dependencies.
3. **Make Your Changes**: Implement your feature or bug fix.
4. **Submit a Pull Request**: Push your changes to your fork and open a pull request against the main branch.

### Adding a Feature
When adding a new feature, ensure it integrates smoothly with the existing application structures. Changes to `run.py` should be minimal, ideally limited to integrating the new feature module.

## Reporting Bugs
- Report bugs through GitHub issues, providing detailed steps to reproduce the bug and expected versus actual results.

## Recognition
Contributors who make significant improvements or additions will be recognized in our project documentation.

We look forward to your contributions and are excited to see how you can help improve Between Bytes!
