Build From Source
=================

This section provides information for developers who wish to interact with and/or contribute to the Between Bytes codebase.

.. note::

    This guide assumes you are using a Unix-like operating system. If you are using Windows, you may need to adjust the commands accordingly.

Prerequisites
-------------
Before you can install Between Bytes, you need to have the following software installed:

1. Python 3.10 or later
2. pip

Installation From Source
------------------------

.. hint::

    NEW: If you are using Linux, the script in ``build.sh`` can automatically build and install the package for you in a ``venv`` environment. The script can also optionally build the docs (which you are reading right now).

1. Clone the repository from GitHub, and navigate to the project directory:

.. code-block:: bash

    git clone repository_url_or_ssh
    cd between_bytes

2. Use pip to install ``flit``: 

.. code-block:: bash

    pip install flit

3. Build and install the package wheel:

.. code-block:: bash

    flit install

4. Refer to the *CLI* section for information on how to use the command line interface provided by ``btb-cli``.