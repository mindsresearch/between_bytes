"""A short description of what your code does.

A longer description of what your code does,
including what csvs it takes in, and what it
contributes to the final output

Functions:
    run(off_facebook_activity_v2): Runs the feature.

Example usage:
    >>> from features import off_fb_act as ofa
    >>> ofa.run(JsonReader.get_csv("off_facebook_activity_v2"))
    filepath to HTML page containing results of analysis

    $ python3 off_fb_act.py -off_facebook_activity_v2 /path/to/off_facebook_activity_v2.csv
    filepath to HTML page containing results of analysis

Dependencies:
    pandas for data handling
    seaborn for datavis
    [ADD DESCRIPTIONS FOR FURTHER THIRD-PARTY IMPORTS HERE]


Note:
    This sub-module is part of the 'selfscape_insight' package in the 'features' module.

Version:
    0.1

Author:
    Liam Gore
"""

import argparse
import logging
import sys
from pathlib import Path
# Add your other built-in imports here

import pandas as pd
import seaborn as sns
# Add your other third-party/external imports here
# Please update requirements.txt as needed!

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from selfscape_insight.core.various_helpers import pointless_function # pylint disable=wrong-import-position

def run(in_path:Path, out_path:Path, logger:logging.Logger, auditor:logging.Logger) -> str:
    # TODO: Please refer to sample.py for run() docstring format!
    logger.info("Running the off_fb_act feature module")
    return "The off_fb_act module did stuff!"

if __name__ == "__main__":
    print(pointless_function()) # remove in production
    parser = argparse.ArgumentParser(prog='off_fb_act',
                                     description='A short description of what your code does')
    parser.add_argument('-i', '--in_file', metavar='(NAME)_JSON', help='path to json file where \'NAME\' is tlk', required=True)
    parser.add_argument('-o', '--out_path', metavar='OUTPUT_PATH', help='where to send output(s)', required=False, default='.')
    parser.add_argument('-v', '--verbose', action='store_true', help='increase verbosity', required=False)
    args = parser.parse_args()

    ch = logging.StreamHandler()
    logfmt = "%(asctime)s : [%(name)s - %(levelname)s] : %(message)s"
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG if args.verbose else logging.WARNING)
    logger.addHandler(ch)
    auditor = logging.getLogger('auditor')
    auditor.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    auditor.addHandler(ch)
    ch.setFormatter(logging.Formatter(logfmt))

    print(run(args.in_file, args.out_path, logger, auditor))
