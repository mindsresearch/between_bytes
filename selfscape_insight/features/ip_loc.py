"""A short description of what your code does.

A longer description of what your code does,
including what csvs it takes in, and what it
contributes to the final output

Functions:
    run(account_activity_v2): Runs the feature.

Example usage:
    >>> from features import ip_loc as ipl
    >>> ipl.run(JsonReader.get_csv("account_activity_v2"))
    filepath to HTML page containing results of analysis

    $ python3 ip_loc.py -account_activity_v2 /path/to/account_activity_v2.csv
    filepath to HTML page containing results of analysis

Dependencies:
    pandas for data handling
    geopandas for geospatial data handling
    matplotlib.pyplot for basic datavis
    folium for more advanced datavis
    maxminddb for IP -> lat/long conversion
    [ADD DESCRIPTIONS FOR FURTHER THIRD-PARTY IMPORTS HERE]


Note:
    This sub-module is part of the 'selfscape_insight' package in the 'features' module.

Version:
    0.1

Author:
    Trevor Le
"""

import argparse
import os
from datetime import timedelta, datetime
# Add your other built-in imports here

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import maxminddb
import folium
# Add your other third-party/external imports here
# Please update requirements.txt as needed!


def run(account_activity_v2):
    # TODO: Please refer to sample.py for run() docstring format!
    print("Running the ip_loc feature module")
    return "The ip_loc module did stuff!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='ip_loc',
                                     description='A short description of what your code does')
    parser.add_argument('-account_activity_v2', metavar='ACCOUNT_ACTIVITY_V2_CSV',
                        help='path to account_activity_v2 csv file', required=True)
    args = parser.parse_args()
    print(run(args.account_activity_v2))
