Command-Line Interface
======================

There is currently only one command available upon installing the package:

    persona-cli

`persona-cli` is a command-line interface for the Persona Sight package. It has the following command-line arguments:

    usage: persona-cli [-h] [-v] [-c CONFIG] [-d] [-l LOG] [-s] [-t] [-u] [-w]

    required arguments:
      -i PATH/TO/DATA, --in_path PATH/TO/DATA
                            path to root directory containing data files
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -c                    data files are csvs; used in development
      -d, --debug           enable debug-level logging
      -l LOG, --log LOG     specify the log file to use
      -s, --silent          disable console output

.. attention::
    The commandline argument structure defined above is not accurate. Please refer to the source file for the actual structure.