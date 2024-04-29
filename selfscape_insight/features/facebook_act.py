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
import os

def naive_converted(main_path):
    user_name = 'Peter Hafner'
    posts_path = main_path+'/your_activity_across_facebook/posts/your_posts__check_ins__photos_and_videos_1.json'

    f = open(posts_path)

    postsdata = json.load(f)

    # load as df
    postsdf = pd.read_json(posts_path)
    # print(postsdf)

    # create new df
    pdf = pd.DataFrame(columns=['timestamp', 'data', 'title'])

    # print(pdf)
    # print(pd.DataFrame.to_string(pdf))

    count = 0
    # for each item in json
    for i in postsdata:
        # print(count)
        # print(i.get('timestamp'))
        # print(i.get('data'))
        # print(i.get('title'))
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

    # print df
    # print(pd.DataFrame.to_string(yearlyposts))

    # make index year
    yearlyposts.set_index('Year', inplace=True)

    # hacky x tick fix, will clean up later
    years = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    # create area plot
    # ax = yearlyposts.plot.area(figsize=(12, 6))
    # ax.set_xlabel('Year')
    # ax.set_xticks(years)
    # ax.set_ylabel('Interactions')
    # ax.set_title('Facebook Use by Year')
    # ax.set_facecolor('gray')

    comments_path = r"{}\your_activity_across_facebook\comments_and_reactions\comments.json".format(main_path)
    # if (os.path.exists(comments_path)):
    #     f = open(comments_path)
    #     commentsdata = json.load(f)

    #     # load as df
    #     commentsdf = pd.read_json(comments_path)
    #     # print(commentsdf)
    # else:
    #     f = open('../../empty_comments.json')
    #     commentsdata = json.load(f)

    #     # load as df
    #     commentsdf = pd.read_json('../../empty_comments.json')
    #     # print(commentsdf)
    f = open(comments_path)
    commentsdata = json.load(f)

    # load as df
    commentsdf = pd.read_json(comments_path)

    # create new df
    cdf = pd.DataFrame(columns=['timestamp', 'data', 'title'])

    # print(cdf)
    # print(pd.DataFrame.to_string(cdf))

    count = 0
    # for each item in json
    for i in commentsdata['comments_v2']:
        # print(count)
        # print(i.get('timestamp'))
        # print(i.get('data'))
        # print(i.get('title'))
        count+=1
        cdf.loc[len(cdf)] =  {'timestamp': i.get('timestamp'), 'data': i.get('data'), 'title': i.get('title')}

    f.close()

    # plotting stuff
    cdf['timestamp'] = pd.to_datetime(cdf['timestamp'], unit='s')

    # add year column
    cdf['Year'] = cdf['timestamp'].dt.year

    # group by year
    yearlycomms = cdf.groupby('Year').size().reset_index(name='Comments')

    # print df
    # print(pd.DataFrame.to_string(yearlycomms))

    # make index year
    yearlycomms.set_index('Year', inplace=True)

    # hacky x tick fix, will clean up later
    years = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    # create area plot
    # ax = yearlycomms.plot.area(figsize=(12, 6))
    # ax.set_xlabel('Year')
    # ax.set_xticks(years)
    # ax.set_ylabel('Interactions')
    # ax.set_title('Facebook Use by Year')
    # ax.set_facecolor('gray')

    reactions_path = main_path+'/your_activity_across_facebook/comments_and_reactions/'

    # get all json files here except comments
    reactions_files = [file for file in os.listdir(reactions_path) if file.endswith('.json') and file !='comments.json']

    # create df
    ldf = pd.DataFrame(columns=['timestamp', 'data', 'title'])

    # load each file
    for reactions_file in reactions_files:
        with open(os.path.join(reactions_path, reactions_file)) as file:
            reactions_data = json.load(file)
            for i in reactions_data:
                ldf = pd.concat([ldf, pd.DataFrame([i], columns=['timestamp', 'data', 'title'])], ignore_index=True)

    # plotting stuff
    ldf['timestamp'] = pd.to_datetime(ldf['timestamp'], unit='s')

    # add year column
    ldf['Year'] = ldf['timestamp'].dt.year

    # group by year
    yearlylikes = ldf.groupby('Year').size().reset_index(name='Likes')

    # print df
    # print(pd.DataFrame.to_string(yearlylikes))

    # make index year
    yearlylikes.set_index('Year', inplace=True)

    # hacky x tick fix, will clean up later
    years = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    # create area plot
    # ax = yearlylikes.plot.area(figsize=(12, 6))
    # ax.set_xlabel('Year')
    # ax.set_xticks(years)
    # ax.set_ylabel('Interactions')
    # ax.set_title('Facebook Use by Year')
    # ax.set_facecolor('gray')
    # plt.show()

    messages_path = main_path + '/your_activity_across_facebook/messages/inbox/'

    # List to store file paths
    message_files = []

    # walk through subdirs (each message thread) in the inbox dir
    for root, dirs, files in os.walk(messages_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                message_files.append(file_path)

    # create list of message dfs
    mdfs = []

    # load each file
    for file_path in message_files:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            participants = data.get('participants')
            messages = data.get('messages')
            message_data = [[message.get('sender_name'), message.get('timestamp_ms'), message.get('content')]
                for message in messages if message.get('sender_name') == user_name]

            mdfs.append(pd.DataFrame(message_data, columns=['sender_name', 'timestamp_ms', 'content']))


    # concat once at the end, speeds up process immensely
    mdf = pd.concat(mdfs, ignore_index=True)

    # Display the DataFrame
    # print(pd.DataFrame.to_string(mdf))

    # plotting stuff
    mdf['datetime'] = pd.to_datetime(mdf['timestamp_ms'], unit='ms')

    # add year column
    mdf['Year'] = mdf['datetime'].dt.year

    # group by year
    yearlymessages = mdf.groupby('Year').size().reset_index(name='Messages')

    # print df
    # print(pd.DataFrame.to_string(yearlymessages))

    # make index year
    yearlymessages.set_index('Year', inplace=True)

    # hacky x tick fix, will clean up later
    years = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    # create area plot
    # ax = yearlymessages.plot.area(figsize=(12, 6))
    # ax.set_xlabel('Year')
    # ax.set_xticks(years)
    # ax.set_ylabel('Messages')
    # ax.set_title('Facebook Use by Year')
    # ax.set_facecolor('gray')
    # Merging 3 dataframes together
    # print(pd.DataFrame.to_string(yearlyposts))
    # print(pd.DataFrame.to_string(yearlycomms))
    # print(pd.DataFrame.to_string(yearlylikes))
    yearlyints = pd.merge(yearlyposts, yearlycomms, on="Year", how="outer")
    yearlyints = pd.merge(yearlyints, yearlylikes, on="Year", how="outer")
    yearlyints = pd.merge(yearlyints, yearlymessages, on="Year", how="outer")

    # fill NaN with zeroes
    yearlyints = yearlyints.fillna(0)

    # convert floats back to ints
    yearlyints = yearlyints.apply(pd.to_numeric, downcast='integer')

    # print df
    # print(pd.DataFrame.to_string(yearlyints))

    colors=['darkviolet', 'deeppink', 'c', 'midnightblue']

    # make graph
    ax = yearlyints.plot.line(figsize=(12,6), color=colors)
    ax.set_ylim(bottom=1)
    ax.set_facecolor('gray')
    ax.set_yscale('log')
    # plt.show()

    # testing 3d plot
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.collections import PolyCollection
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    xs = yearlyints.index
    verts = []
    zs = [0, 1, 2, 3]
    interaction_types = ['Posts', 'Comments', 'Likes', 'Messages']
    epsilon = 1e-6  # Small constant to avoid log(0)

    for z, interaction_type in zip(zs, interaction_types):
        ys = yearlyints[interaction_type] + epsilon  # epsilon to fix numeric stability
        ys = np.log(ys)  # Applying log transformation
        ys = np.where(ys > 0, ys, 0)  # Replace negative values (generated from epsilon) with 0
        ys[0], ys[-1] = 0, 0
        verts.append(list(zip(xs, ys)))
        ax.text(xs[-1]+1, z, 0, interaction_type, color='black', fontsize=8, ha='left', va='center')

    poly = PolyCollection(verts, facecolors=['darkviolet', 'deeppink', 'c', 'midnightblue'])
    poly.set_alpha(0.7)
    ax.add_collection3d(poly, zs=zs, zdir='y')

    ax.set_xlim3d(yearlyints.index.min(), yearlyints.index.max())
    ax.set_zlim3d(0, np.log(yearlyints.values + epsilon).max())
    ax.set_ylim3d(-1, 4)
    ax.set_yticklabels([])

    plt.show()
    
    # plt.savefig('Facebook_Use_by_Year.png')
    return

def run(main_path):
    # TODO: Please refer to sample.py for run() docstring format!
    print("Running the facebook_act feature module")
    print("Path: ", main_path)

    naive_converted(main_path)

    return "The facebook_act module did stuff!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='facebook_act',
                                     description='Analyses and visualizes activity across facebook')
    parser.add_argument('-csv_you_are_using', metavar='CSV_YOU_ARE_USING_CSV',
                        help='path to csv_you_are_using csv file', required=True)
    args = parser.parse_args()
    print(run(args.file_path))
