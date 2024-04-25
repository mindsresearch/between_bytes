Build From Source
=================

This section provides information for developers who wish to interact with and/or contribute to the SelfScape Insight codebase.

.. note::

    This guide assumes you are using a Unix-like operating system. If you are using Windows, you may need to adjust the commands accordingly.

Prerequisites
-------------
Before you can install SelfScape Insight, you need to have the following software installed:

1. Python 3.10 or later
2. pip

Installation From Source
------------------------

1. Clone the repository from GitHub, and navigate to the project directory:

.. code-block:: bash

    git clone repository_url
    cd selfscape_insight

2. Use pip to install ``flit``: 

.. code-block:: bash

    pip install flit

3. Build the package wheel:

.. code-block:: bash

    flit build

4. Install the package:

.. code-block:: bash

    pip install dist/selfscape_insight-0.3.0-py3-none-any.whl

4. Refer to the *CLI* section for information on how to use the command line interface provided by ``scape-cli``.

Generating Documentation Locally (Optional)
-------------------------------------------
1. Build the package as described is steps 1-3 above.

2. Install the package with the docs extras:

.. code-block:: bash

    pip install dist/selfscape_insight-0.3.0-py3-none-any.whl[doc]

3. Navigate to the ``docs`` directory and generate the documentation:

.. code-block:: bash

    cd docs
    make html

4. Open the generated documentation in a web browser via your file explorer. The documentation is located at ``docs/_build/html/index.html``.