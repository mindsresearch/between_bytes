"""A short description of what your code does.

A longer description of what your code does,
including what csvs it takes in, and what it
contributes to the final output

Functions:
    run(off_facebook_activity_v2): Runs the feature.

Example usage:
    >>> from features import off_fb_act as ofa
    >>> ofa.run(Path(path_to_json_file))
    filepath to HTML page containing results of analysis

    $ python3 off_fb_act.py -i /path/to/json_file.json
    filepath to HTML page containing results of analysis

Dependencies:
    pandas for data handling
    plotly for datavis

Note:
    This sub-module is part of the 'selfscape_insight' package in the 'features' module.

Version:
    0.2

Author:
    Liam Gore
"""
__version__ = '0.2'

import argparse
from pathlib import Path
# Add your other built-in imports here

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Add your other third-party/external imports here
# Please update requirements.txt as needed!

def run(in_path:Path, out_path:Path) -> str:
    # Create new output directory
    out_path /= 'off_fb_activity'
    out_path.mkdir(exist_ok=True)

    # data reading and pre-processing
    data = pd.read_json(in_path, orient='records')

    websites = data['off_facebook_activity_v2']
    websites.index = list(range(len(websites)))

    site_names = []
    for w in websites:
        site_names.append(w['name'])

    num_of_entries_per_website = []

    for site in websites:
        num_of_entries_per_website.append(len(site['events']))
    website_names = []

    for i in range (len(site_names)):
      input_string = site_names[i]
      decoded_string = input_string.encode('latin-1').decode('utf-8')
      website_names.append(((decoded_string), num_of_entries_per_website[i]))

    d = {'Company':[], 'Number of Visits':[]}
    for w in website_names:
        d['Company'].append(w[0])
        d['Number of Visits'].append(w[1])
    df = pd.DataFrame(data = d)
    df.sort_values(by='Number of Visits', ascending=False, inplace=True, ignore_index=True)

    # top_cos visualization
    #
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Top 5 Most Visited Sites', 'Sites with more than 50 views'))
    tdf = df.head(5)
    fig.add_trace(go.Bar(x=tdf['Company'], y=tdf['Number of Visits']), row=1, col=1)
    tdf = df[df['Number of Visits'] >= 50]
    fig.add_trace(go.Bar(x=tdf['Company'], y=tdf['Number of Visits']), row=1, col=2)
    fig.write_html(out_path/'top_cos.html')

    # Add other visualizations here as see fit.

    return f"Wrote top_cos.html to {out_path}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='off_fb_act',
                                     description='A short description of what your code does')
    parser.add_argument('-i', '--in_file', metavar='(NAME)_JSON', help='path to json file where \'NAME\' is tlk', required=True)
    parser.add_argument('-o', '--out_path', metavar='OUTPUT_PATH', help='where to send output(s)', required=False, default='.')
    temp_args = ['-i', '~/Documents/nde-fb-data-2404/apps_and_websites_off_of_facebook/your_activity_off_meta_technologies.json']
    args = parser.parse_args(temp_args)

    print(run(Path(args.in_file), Path(args.out_path)))
