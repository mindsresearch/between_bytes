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

    import spacy # for natural language processing
    from spacytextblob.spacytextblob import SpacyTextBlob # for sentiment analysis

    # natural language processing
    try:
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load('en_core_web_sm')
        
    nlp.add_pipe('spacytextblob')

    # defining a sentiment polarity function
    def calc_sentiment(msg):
        return msg._.blob.polarity
    
    # filling missing values with empty string
    mdf['content'] = mdf['content'].fillna('')

    # Apply sentiment analysis using spaCy's pipe method
    mdf['sentiment'] = [calc_sentiment(msg) for msg in nlp.pipe(mdf['content'])]

    # Sort the DataFrame by timestamp
    mdf.sort_values(by='timestamp_ms', inplace=True)
    # Process posts and add a "sentiment" column to postsdf
    postsdf['sentiment'] = postsdf['data'].apply(lambda data_list: max([calc_sentiment(nlp(data_item['post'])) for data_item in data_list if 'post' in data_item], default=None))

    # Sort the DataFrame by timestamp
    postsdf = postsdf.sort_values(by='timestamp')

    # Change color based on sentiment
    colors = postsdf.apply(lambda x: (max(0, min(1, 1-x.sentiment)), max(0, min(1, 1+x.sentiment)), 0), axis=1)

    ax = postsdf.plot.scatter(x='timestamp', y='sentiment', figsize=(12,6), color=colors)
    ax.axhline(0, color='black')
    ax.set_facecolor('gray')
    plt.show()
    # add year column
    postsdf['year'] = postsdf['timestamp'].dt.year

    # group by year and calc mean sentiment for each year
    yearlysent = postsdf.groupby('year')['sentiment'].mean()

    # change color based on sentiment
    colors = yearlysent.apply(lambda x: (max(0, min(1, 1-x)), max(0, min(1, 1+x)), 0))

    ax = yearlysent.plot(x='timestamp', y='sentiment', figsize=(12,6), color=colors)
    ax.set_ylim(-0.25, 0.25)
    ax.axhline(0, color='black')
    ax.set_facecolor('gray')
    # adjust timestamp to pacific time
    postsdf['timestamp_pacific'] = postsdf['timestamp'] + pd.DateOffset(hours=8)

    # add hour column
    postsdf['hour'] = postsdf['timestamp_pacific'].dt.hour

    # group by hour and calc mean sentiment for each hour
    hourlysent = postsdf.groupby('hour')['sentiment'].mean()

    # change color based on sentiment
    colors = hourlysent.apply(lambda x: (max(0, min(1, 1-x)), max(0, min(1, 1+x)), 0))

    ax = hourlysent.plot(kind='bar', x='timestamp', y='sentiment', figsize=(12,6), color=colors)
    ax.set_facecolor('gray')
    plt.show()

    # group by hour and count the number of entries for each hour
    hourly_counts = postsdf.groupby('hour').size()

    # group by hour and calc mean sentiment for each hour
    hourly_sentiment = postsdf.groupby('hour')['sentiment'].mean()

    # change color based on sentiment
    colors = hourly_sentiment.apply(lambda x: (max(0, min(1, 1-x)), max(0, min(1, 1+x)), 0))

    # plot bar chart with frequency as height and sentiment as color
    ax = hourly_counts.plot(kind='bar', figsize=(12,6), color=colors)
    ax.set_facecolor('gray')

    ax.set_ylabel('Post Count')

    # add labels for sentiment value
    for i, (index, val) in enumerate(hourly_sentiment.items()):
        ax.text(i, hourly_counts[index] + 0.1, f'{val:.2f}', ha='center', va='bottom')
    plt.show()

    # add hour column
    postsdf['day'] = postsdf['timestamp'].dt.day

    # Group by day of the week and calculate the mean sentiment for each day
    dailysent = postsdf.groupby(postsdf['timestamp'].dt.dayofweek)['sentiment'].mean()

    # change color based on sentiment
    colors = dailysent.apply(lambda x: (max(0, min(1, 1-x)), max(0, min(1, 1+x)), 0))

    ax = dailysent.plot(kind='bar', x='timestamp', y='sentiment', figsize=(12,6), color=colors)
    ax.set_facecolor('gray')
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6], ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    plt.show()

    # Change color based on sentiment
    colors = mdf.apply(lambda x: (max(0, min(1, 1-x.sentiment)), max(0, min(1, 1+x.sentiment)), 0), axis=1)

    ax = mdf.plot.scatter(x='timestamp_ms', y='sentiment', figsize=(12,6), color=colors)
    ax.set_facecolor('gray')
    plt.show()

    # add year column
    mdf['year'] = mdf['timestamp'].dt.year

    # group by year and calc mean sentiment for each year
    messageyearlysent = mdf.groupby('year')['sentiment'].mean()

    # change color based on sentiment
    colors = messageyearlysent.apply(lambda x: (max(0, min(1, 1-x)), max(0, min(1, 1+x)), 0))

    ax = messageyearlysent.plot(x='timestamp_ms', y='sentiment', figsize=(12,6), color=colors)
    ax.set_ylim(-0.25, 0.25)
    ax.axhline(0, color='black')
    ax.set_facecolor('gray')
    plt.show()

    # adjust timestamp to pacific time
    mdf['timestamp_pacific'] = mdf['timestamp_ms'] + pd.DateOffset(hours=8)

    # add hour column
    mdf['hour'] = mdf['timestamp_pacific'].dt.hour

    # group by hour and calc mean sentiment for each hour
    messagehourlysent = mdf.groupby('hour')['sentiment'].mean()

    # change color based on sentiment
    colors = messagehourlysent.apply(lambda x: (max(0, min(1, 1-x)), max(0, min(1, 1+x)), 0))

    ax = messagehourlysent.plot(kind='bar', x='timestamp_pacific', y='sentiment', figsize=(12,6), color=colors)
    ax.set_facecolor('gray')
    plt.show()

    # group by hour and count the number of entries for each hour
    message_hourly_counts = mdf.groupby('hour').size()

    # group by hour and calc mean sentiment for each hour
    message_hourly_sentiment = mdf.groupby('hour')['sentiment'].mean()

    # change color based on sentiment
    colors = message_hourly_sentiment.apply(lambda x: (max(0, min(1, 1-x)), max(0, min(1, 1+x)), 0))

    # plot bar chart with frequency as height and sentiment as color
    ax = message_hourly_counts.plot(kind='bar', figsize=(12,6), color=colors)
    ax.set_facecolor('gray')

    ax.set_ylabel('Post Count')

    # add labels for sentiment value
    for i, (index, val) in enumerate(message_hourly_sentiment.items()):
        ax.text(i, message_hourly_counts[index] + 0.1, f'{val:.2f}', ha='center', va='bottom')
    plt.show()

    # add hour column
    mdf['day'] = mdf['timestamp_pacific'].dt.day

    # Group by day of the week and calculate the mean sentiment for each day
    messagedailysent = mdf.groupby(mdf['timestamp_pacific'].dt.dayofweek)['sentiment'].mean()

    # change color based on sentiment
    colors = messagedailysent.apply(lambda x: (max(0, min(1, 1-x)), max(0, min(1, 1+x)), 0))

    ax = messagedailysent.plot(kind='bar', x='timestamp_pacific', y='sentiment', figsize=(12,6), color=colors)
    ax.set_facecolor('gray')
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6], ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    plt.show()

    from wordcloud import WordCloud, STOPWORDS, get_single_color_func
    import matplotlib.pyplot as plt

    # concatenate text data
    wc_text = ' '.join(mdf['content'].astype(str).apply(lambda x: x.encode('utf-8').decode('utf-8')))

    # define stop words
    stop_words = ['â'] + list(STOPWORDS)

    # function to assign colors based on sentiment scores
    def grouped_color_func(color_to_words, default_color, word):
        color_func_to_words = [(get_single_color_func(color), set(words)) for (color, words) in color_to_words.items()]
        default_color_func = get_single_color_func(default_color)

        def get_color_func(word):
            try:
                color_func = next(color_func for (color_func, words) in color_func_to_words if word in words)
            except StopIteration:
                color_func = default_color_func
            return color_func

        return get_color_func(word)(word)

    # tokenize messages into words
    mdf['tokenized_content'] = mdf['content'].str.split()

    # calculate sentiment scores for each word
    word_sentiments = {}
    for index, row in mdf.iterrows():
        for word in row['tokenized_content']:
            if word not in word_sentiments:
                word_sentiments[word] = {'total_sentiment': 0, 'count': 0}
            word_sentiments[word]['total_sentiment'] += row['sentiment']
            word_sentiments[word]['count'] += 1

    # calculate average sentiment scores
    for word, values in word_sentiments.items():
        word_sentiments[word]['average_sentiment'] = values['total_sentiment'] / values['count']

    # define colors based on sentiment scores
    color_to_words = {
        'red': [word for word, values in word_sentiments.items() if values['average_sentiment'] < -0.25],
        'green': [word for word, values in word_sentiments.items() if values['average_sentiment'] > 0.25],
    }

    default_color = 'grey'

    # randomize color tones
    grouped_color_func_result = lambda word, font_size, position, orientation, random_state, font_path: grouped_color_func(color_to_words, default_color, word)

    # create and display word cloud
    wc = WordCloud(stopwords=stop_words, width=800, height=400, max_words=200, background_color='black', collocations=False).generate(wc_text)
    wc.recolor(color_func=grouped_color_func_result)

    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    # define stop words
    stop_words = ['â', 'ð', 'Iâ', 've', 'm', 'll', 'thatâ', 's', 'd', 'donâ', 't', 'weâ', 're', 'itâ', 'heâ', 'whoâ', 'theyâ', 'havenâ', 'thereâ', 'isnâ', 'sheâ', 'heâ', 'Fredâ'] + list(STOPWORDS)

    grouped_data = mdf.groupby('Year')

    for year, group in grouped_data:
        # concatenate text data for the current year
        wc_text = ' '.join(group['content'].astype(str))

        # tokenize messages into words for the current year
        group['tokenized_content'] = group['content'].str.split()

        # calculate sentiment scores for each word for the current year
        word_sentiments = {}
        for index, row in group.iterrows():
            for word in row['tokenized_content']:
                if word not in word_sentiments:
                    word_sentiments[word] = {'total_sentiment': 0, 'count': 0}
                word_sentiments[word]['total_sentiment'] += row['sentiment']
                word_sentiments[word]['count'] += 1

        # calculate average sentiment scores for the current year
        for word, values in word_sentiments.items():
            word_sentiments[word]['average_sentiment'] = values['total_sentiment'] / values['count']

        # define colors based on sentiment scores for the current year
        color_to_words = {
            'red': [word for word, values in word_sentiments.items() if values['average_sentiment'] < -0.25],
            'green': [word for word, values in word_sentiments.items() if values['average_sentiment'] > 0.25],
        }

        default_color = 'grey'

        # randomize color tones for the current year
        grouped_color_func_result = lambda word, font_size, position, orientation, random_state, font_path: grouped_color_func(color_to_words, default_color, word)

        # create and display word cloud for the current year
        wc = WordCloud(stopwords=stop_words, width=800, height=400, max_words=200, background_color='black', collocations=False).generate(wc_text)
        wc.recolor(color_func=grouped_color_func_result)

        plt.figure(figsize=(12, 6))
        plt.imshow(wc, interpolation='bilinear')
        plt.title(f'Word Cloud for Year {year}')
        plt.axis('off')
        plt.show()
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
