"""A short description of what your code does.

A longer description of what your code does,
including what csvs it takes in, and what it
contributes to the final output

Functions:
    run(csv_you_are_using): Runs the feature.

Example usage:
    >>> from features import feelings as fgs
    >>> fgs.run(JsonReader.get_csv(csv_you_are_using))
    filepath to HTML page containing results of analysis

    $ python3 feelings.py -csv_you_are_using /path/to/csv_you_are_using.csv
    filepath to HTML page containing results of analysis

Dependencies:
    pandas for data handling
    matplotlib.pyplot for basic datavis
    spacy for natural language processing
    wordcloud for wordcloud datavis
    [ADD DESCRIPTIONS FOR FURTHER THIRD-PARTY IMPORTS HERE]


Note:
    This sub-module is part of the 'selfscape_insight' package in the 'features' module.

Version:
    0.1.0

Author:
    Peter Hafner
"""

import os
import argparse
# Add your other built-in imports here

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob # for sentiment analysis
from wordcloud import WordCloud, STOPWORDS, get_single_color_func
# Add your other third-party/external imports here
# Please update requirements.txt as needed!

def run(csv_you_are_using):
    # TODO: Please refer to sample.py for run() docstring format!
    print("Running the feelings feature module")
    return "The feelings module did stuff!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='feelings',
                                     description='A short description of what your code does')
    parser.add_argument('-csv_you_are_using', metavar='CSV_YOU_ARE_USING_CSV',
                        help='path to csv_you_are_using csv file', required=True)
    args = parser.parse_args()
    print(run(args.csv_you_are_using))
