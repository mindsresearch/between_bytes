"""A short description of what your code does.

A longer description of what your code does,
including what csvs it takes in, and what it
contributes to the final output

Functions:
    run(file_path): Runs the feature.

Example usage:
    >>> from features import facebook_act as fba
    >>> fba.run(args.in_path)
    filepath to HTML page containing results of analysis

    $ python3 facebook_act.py -csv_you_are_using /path/to/csv_you_are_using.csv
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
    0.1

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
import json

def create_post_df(file_path):
    posts_path = r"{}\your_activity_across_facebook\posts\your_posts__check_ins__photos_and_videos_1.json".format(file_path)
    f = open(posts_path)

    postsdata = json.load(f)

    # load as df
    postsdf = pd.read_json(posts_path)
    # print(postsdf)

    # create new df
    pdf = pd.DataFrame(columns=['timestamp', 'data', 'title'])

    count = 0
    for i in postsdata:
        count+=1
        pdf.loc[len(pdf)] =  {'timestamp': i.get('timestamp'), 'data': i.get('data'), 'title': i.get('title')}

    f.close()


    # plotting stuff
    pdf['timestamp'] = pd.to_datetime(pdf['timestamp'], unit='s')
    # pdf

    # add year column
    pdf['Year'] = pdf['timestamp'].dt.year
    # pdf

    # group by year
    yearlyposts = pdf.groupby('Year').size().reset_index(name='Posts')

    # make index year
    yearlyposts.set_index('Year', inplace=True)

    # hacky x tick fix, will clean up later
    years = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    # create area plot
    ax = yearlyposts.plot.area(figsize=(12, 6))
    ax.set_xlabel('Year')
    ax.set_xticks(years)
    ax.set_ylabel('Interactions')
    ax.set_title('Facebook Use by Year')
    ax.set_facecolor('gray')
    plt.savefig('Facebook_Use_by_Year.png')
    return

def run(file_path):
    # TODO: Please refer to sample.py for run() docstring format!
    print("Running the facebook_act feature module")
    print("Path: ", file_path)

    create_post_df(file_path)

    return "The facebook_act module did stuff!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='facebook_act',
                                     description='Analyses and visualizes activity across facebook')
    parser.add_argument('-csv_you_are_using', metavar='CSV_YOU_ARE_USING_CSV',
                        help='path to csv_you_are_using csv file', required=True)
    args = parser.parse_args()
    print(run(args.file_path))
