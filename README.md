# Between Bytes

> [!WARNING]
> This repo is currently undergoing a major renaming from "SelfScape Insight" to "Between Bytes". Please forgive any such discrepancies in the docs!

## Overview
**Between Bytes** is a Python project developed as part of the WWU Data Science Senior Project. It's designed to provide insights from Facebook data, making it easier for users to visualize and understand their social media interactions.

## Features
- **CLI Interface:** Easy-to-use command-line interface.
- **GUI Interface:** Even easier to use graphical wizard-style launcher.
- **Data Visualization:** Generate comprehensive visualizations of Facebook data.
- *COMING SOON* **Customizable Outputs:** Tailor the outputs based on user-specific needs.

## Installation

### From Binary
> *COMING SOON*
>
> An `.exe` version of the program is coming soon to make running it even easier!

Download the latest version as a `whl` file from the Releases section on the right sidebar of this repository.

```bash
pip install path/to/between_bytes-<version>-py3-none-any.whl
```

### Compiling from Source
This project uses **flit** for packaging and distribution and **sphinx** for generating documentation.

#### Set Up
Ensure you are in the project's root directory (`./between_bytes`).

#### Building & Installing the Wheel
Install `flit` if it is not already installed:
```bash
pip install flit
```
Build and install the project:
```bash
flit install
```

## Usage
Run the CLI version of **Between Bytes**:
```bash
btb-cli -h
```
for command-line help

For the GUI version, run:
```bash
btb-gui
```

## Documentation
### Building Reference Docs
> [!CAUTION]
> These instructions are untested and may require adjustments.

Follow the setup and build instructions above, then run:
```bash
pip install dist/<wheel_name>.whl[doc]
cd docs
make clean html
```
The generated documentation will be available in `docs/_build/html`.

## Contributing
Contributions are welcome! Please see our [contributing guidelines](.github/CONTRIBUTING.md) for more information on how to report bugs, submit patches, and propose new features.

## License
Between Bytes is licensed under [GNU AGPL-3.0]. See the [LICENSE](LICENSE) file for more details.

## Contact
For more support or to provide feedback, please refer to the [SECURITY](.github/SECURITY.md) guidelines and the [CODE OF CONDUCT](.github/CODE_OF_CONDUCT.md).