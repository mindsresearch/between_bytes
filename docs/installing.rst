Installation Instructions
=========================

.. note::

    This guide assumes you are using a Unix-like operating system. If you are using Windows, you may need to adjust the commands accordingly.

Prerequisites
-------------
Before you can install Persona Sight, you need to have the following software installed:

1. Python 3.6 or later
2. pip

Installation From Source
------------------------

1. Clone the repository from GitHub, and navigate to the project directory:

.. code-block:: bash

    git clone repository_url
    cd persona_sight

2. Use pip to install ``flit``: 

.. code-block:: bash

    pip install flit

3. Build and install the package:

.. code-block:: bash

    flit install

4. Refer to the *CLI* section for information on how to use the command line interface.

Generating Documentation Locally (Optional)
-------------------------------------------
1. Build the package as described above, then navigate to the ``docs`` directory

2. Install the required dependencies:

.. code-block:: bash

    pip install sphinx pydata-sphinx-theme

3. Generate the documentation:

.. code-block:: bash

    make html
