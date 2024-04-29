"""A short description of what your code does.

A longer description of what your code does,
including what csvs it takes in, and what it
contributes to the final output

Functions:
    run(topics_v2, inferred_topics_v2): Runs the feature.

Example usage:
    >>> from features import topics as tps
    >>> tps.run(stuff, things)
    filepath to HTML page containing results of analysis

    $ python3 topics.py -i paths -o path
    filepath to HTML page containing results of analysis

Dependencies:
    pandas for data handling
    requests and BeautifulSoup4 for webscraping image acquisition
    pillow (PIL) for image handling
    [ADD DESCRIPTIONS FOR FURTHER THIRD-PARTY IMPORTS HERE]


Note:
    This sub-module is part of the 'selfscape_insight' package in the 'features' module.

Version:
    0.1

Author:
    Carter Jacobs
"""

import argparse
import os
import sys
import random
import tempfile
from pathlib import Path
# Add your other built-in imports here

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
# Add your other third-party/external imports here
# Please update requirements.txt as needed!

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.various_helpers import pointless_function # pylint disable=wrong-import-position
from core.log_aud import SsiLogger, RootLogger # pylint disable=wrong-import-position

def run(in_path:Path, out_path:Path, logger:SsiLogger) -> str:
    # TODO: Please refer to sample.py for run() docstring format!
    logger.info("Running the topics feature module")
    return "The topics module did stuff!"

if __name__ == "__main__":
    print(pointless_function()) # remove in production
    parser = argparse.ArgumentParser(prog='topics',
                                     description='A short description of what your code does')
    parser.add_argument('-i', '--in_file', metavar='JSON', help='path to json file', required=True, nargs='+')
    parser.add_argument('-o', '--out_path', metavar='OUTPUT_PATH', help='where to send output(s)', required=False, default='.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity', required=False)
    args = parser.parse_args()

    logger = RootLogger()
    logger.setup(verb=args.verbose)

    for f in args.in_file:
        print(run(f, args.out_path, logger))
