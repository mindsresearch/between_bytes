# SelfScape Insight

This repository contains the (soon to be) public/PROD version of the SelfScape Insight program.

This is the Python project from the WWU Data Sci Senior Project Facebook group.

## Downloading the program

Download the latest version as a `whl` via the Releases section on the right sidebar!

*.exe download coming "soon" once I figure it out...*

## Compiling from source (this directory)

To compile the `selfscape_insight` from source, the project uses **flit** for wheel compilation and **sphinx** for reference documentation.

To start, please open *this directory* (`./selfscape_insight`) in your terminal of choice. The following instructions assume that you are using a UNIX-based system. Adapt the instructions as needed to fit your system.

### Compiling the Wheel

First, if you have not done so already, install flit.

```bash
pip install flit
```

Then, build the project.

```bash
flit build
```

If everything worked, this command will generate two files: a `.whl` and a `.tar.gz`. You are now ready to install `selfscape_insight` to your system (using a venv is recommended).

```bash
pip install dist/$(whl_name).whl
```

You can now run the CLI version of `selfscape_insight`!

```bash
scape-cli $(ArgsFor_main_cli.py)
```

### Compiling the Reference Docs

> [!NOTE]
> The instructions in this section are untested.

Follow the above steps up to (and including) `flit build`.

To install `selfscape_insight` with the necessary dependencies for building the docs, run the following command:

```bash
pip install dist/$(whl_name).whl[doc]
```

Once that has completed, navigate to the `docs/` directory, and build the docs.

```bash
cd docs
make html
```

Your local copy of the docs are now located at `docs/_build/html`!