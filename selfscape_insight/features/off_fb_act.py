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
    0.1.0

Author:
    Liam Gore
"""

import argparse
# Add your other built-in imports here

import pandas as pd
import seaborn as sns
# Add your other third-party/external imports here
# Please update requirements.txt as needed!


def run(off_facebook_activity_v2):
    # TODO: Please refer to sample.py for run() docstring format!
    print("Running the off_fb_act feature module")
    return "The off_fb_act module did stuff!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='off_fb_act',
                                     description='A short description of what your code does')
    parser.add_argument('-off_facebook_activity_v2', metavar='OFF_FACEBOOK_ACTIVITY_V2_CSV',
                        help='path to off_facebook_activity_v2 csv file', required=True)
    args = parser.parse_args()
    print(run(args.off_facebook_activity_v2))
