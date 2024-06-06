"""Notifications History Feature

This module provides a GitHub-style heatmap
of Facebook push notifications

Functions:
    run(bcts): Runs the feature.

Example usage:
    >>> import sample_feature as sf
    >>> sf.run(PathLike, logger, auditor)
    There are X advertising-related topics in the profile!
    Go do more interesting things...

    $ python3 sample_feature.py -i /path/to/file.json
    There are X advertising-related topics in the profile!
    Go do more interesting things...

Dependencies:
    No external dependencies.

Note:
    This sub-module is part of the 'between_bytes' package in the 'feature' module.

Version:
    1.0

Author:
    Noah Duggan Erickson
"""

import json
import sys
from pathlib import Path
from datetime import date
import argparse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import plotly.graph_objects as go

from between_bytes.core.log_aud import BtbLogger, RootLogger # pylint disable=wrong-import-position


def weeks_in_year(year:int) -> int:
    last = date(year, 12, 28)
    return last.isocalendar().week

def first_week_of_months(year:int) -> list:
    return [date(year, month, 3).isocalendar().week - 1 for month in range(1, 13)]

def pretty_xlab(year) -> list:
    out = []
    m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    c = 0
    for i in range(weeks_in_year(year)):
        if i in first_week_of_months(year):
            out.append(m[c])
            c += 1
        else:
            out.append('')
    return out

def run(in_path:Path, out_path:Path, logger:BtbLogger) -> str:
    """Runs the feature.

    Tells how many ad-topics are on the user profile.
    (This description should be more verbose in a real feature!)

    Args:
        bcts (str): path to `other_categories_used_to_reach_you.json` file
    
    Returns:
        str: This feature's contribution to the profile info dashboard datavis thing
    
    Warnings:
        run() is a *required* function for the module! It *must*
        be the only interaction that main.py has with the module.
    """
    logger.info("Starting notifications feature...")
    out_path = out_path / 'notifications'
    out_path.mkdir(exist_ok=True)

    logger.use_file(in_path)
    with open(in_path) as f:
        data = json.load(f)
    df = pd.DataFrame(data['notifications_v2'])

    # data prep
    logger.info("Prepping data...")
    dts = pd.to_datetime(df['timestamp'], unit='s')
    ddf = pd.DataFrame({'timestamp': dts, 'value': 1})
    ddf.set_index('timestamp', inplace=True)
    cts = ddf.resample('D').sum()
    cts = cts.fillna(0)

    logger.debug("Creating colormap...")
    cl = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353']
    cm = LinearSegmentedColormap.from_list('GyGr', cl, N=256)



    years = cts.index.year.unique()

    for y in years:
        logger.info(f"Creating heatmap for year {y}...")
        grid= np.zeros((7, weeks_in_year(y)))
        for i, r in cts.loc[str(y)].iterrows():
            w = i.weekofyear - 1
            d = i.dayofweek
            grid[d, w] = r['value']
        maxv = grid.max()
        cmapper = lambda x: np.array(cm(x/maxv))*255
        color_grid = cmapper(grid)
        date_grid = np.array([date.fromisocalendar(y, j+1, i+1).isoformat()
                                  for i in range(7)
                                  for j in range(weeks_in_year(y))]).reshape(7, weeks_in_year(y))

        logger.debug("Building heatmap...")
        img = go.Image(z=color_grid,
                       customdata=grid,
                       text=date_grid,
                       hovertemplate='%{customdata} notifications on %{text}',
                       name=str(y))
        fig = go.Figure(img)

        fig.update_layout(paper_bgcolor="#0d1117",
                          plot_bgcolor="#0d1117",
                          font_color="#c9d1d9",
                          title=f'{y} Notifications')
        fig.update_xaxes(tickvals=np.arange(weeks_in_year(y)),
                         ticktext=pretty_xlab(y),
                         tickmode='array', title='Month')
        fig.update_yaxes(tickvals=np.arange(7),
                         ticktext=['M', 'T', 'W', 'R', 'F', 'S', 'U'],
                         tickmode='array', title='Day of Week')
        for i in range(grid.shape[0]):
            fig.add_hline(y=i-0.5, line_width=5, line_color="#0d1117")
        for i in range(grid.shape[1]):
            fig.add_vline(x=i-0.5, line_width=5, line_color="#0d1117")
        fig.write_html(out_path / f'{y}_notifications.html')
        logger.wrote_file(out_path / f'{y}_notifications.html')

    return f"Created {len(years)} notification heatmap(s) at {out_path}"

# Below is more-or-less boilerplate code that can be copy/pasted
# and extended to allow the feature to run directly from the
# commandline as shown in Example 2
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='sample_feature', description='A sample program feature for the purposes of demo-ing code structure and boilerplate')
    parser.add_argument('-i', '--in_file', metavar='JSON_FILE', help='path to notifications json file', required=True)
    parser.add_argument('-o', '--out_path', metavar='OUTPUT_PATH', help='where to send output(s)', required=False, default='.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity', required=False)
    args = parser.parse_args()

    logger = RootLogger()
    logger.setup(verb=args.verbose)

    print(run(args.in_file, args.out_path, logger))