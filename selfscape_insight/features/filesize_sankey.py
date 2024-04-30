"""A short description of what your code does.

A longer description of what your code does,
including what csvs it takes in, and what it
contributes to the final output

Functions:
    run(json_path): Runs the feature.

Example usage:
    >>> from features import filesize_sankey as fsk
    >>> fsk.run(json_path, out_path)
    filepath to HTML page containing results of analysis

    $ python3 filesize_sankey.py -json_path /path/to/jsons/ -out_path /path/to/output
    filepath to where to write filesize_sankey.html page containing results of analysis

Dependencies:
    pandas for data handling
    plotly for datavis

Note:
    This sub-module is part of the 'selfscape_insight' package in the 'features' module.

Todo:
    * Prettify the output

Version:
    1.1

Author:
    Noah Duggan Erickson
"""

# CHANGELOG:
#   1.1: (26 April 2024)
#     - Use mimetypes to color code file types
#     - Added legend (non-functional) to Sankey diagram
#     - Updated signatures and imports to match new standards
#     - Moved over to SsiLogger for logging
#     - Move helper functions to core
#   1.0.1: (09 April 2024)
#     - Added docstrings & comments
#   1.0: (05 April 2024)
#     - Initial Release
#     - (transfer from notebook to script)

import argparse
import os
import sys
from pathlib import Path
import mimetypes
from collections import defaultdict

import pandas as pd
import plotly.graph_objects as go
import seaborn as sns

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.various_helpers import pointless_function # pylint disable=wrong-import-position
from core.log_aud import SsiLogger, RootLogger # pylint disable=wrong-import-position
import core.filesize_sankey_core as fsc # pylint disable=wrong-import-position

def run(json_path:str, out_path:str, logger:SsiLogger) -> str:
    raise Exception("This feature is currently broken pending pathlib transition. Please use filesize_sunburst instead.")
    logger.info("Running the filesize_sankey feature module")

    logger.use_file(Path('ALL'), 'metadata')
    # Enumerate files and directories, get filesizes
    #
    fdf = fsc.pdEnumFiles(json_path)
    fdf['size'] = fdf.apply(lambda x: os.stat(x['path']).st_size, axis=1)
    pdict = fsc.dEnumDirs(json_path)
    ddf = fsc.pdEnumDirs(json_path)
    logger.debug(f"Found {len(fdf)} files and {len(ddf)} directories")

    # Map directories to parent directories via IDs
    #
    ddf['didx'] = ddf['path'].map(pdict)
    ddf['pidx'] = ddf['root'].map(pdict)

    # Assign files to directory IDs
    ddf.index = ddf['path']
    ddf.drop(['root', 'dir', 'path'], axis=1, inplace=True)
    fdf = fdf.join(ddf, on='root')
    ddf['path'] = ddf.index
    ddf.index = ddf['didx']
    logger.debug(f"Assigned IDs to directories and files")

    # Aggregate file sizes by directory
    #
    ddf['size'] = fdf.groupby('didx').sum()['size']
    ddf = ddf.fillna(0)
    for i in range(25): # Arbitrary number of iterations to ensure all directories are accounted for
        tsr = ddf.drop('path', axis=1).groupby('pidx').sum()['size']
        for j, v in tsr.items():
            ddf.at[j, 'size'] = v
    ddf = ddf.dropna()
    logger.debug(f"Aggregated file sizes by directory")

    # Build Sankey diagram connections
    #
    logger.info("Building Sankey diagram")
    tddf = pd.DataFrame({'source': ddf['pidx'], 'target': list(ddf.index), 'value': ddf['size'], 'label':ddf['path'].apply((lambda x: f"{x}.dir"))})
    tddf.index = list(range(len(tddf)))
    tddf['label'] = tddf['label'].apply((lambda x: x.split('/')[-1]))
    fdf['fidx'] = [i+ddf['didx'].max()+1 for i in list(range(len(fdf)))] # Assign file IDs
    tfdf = pd.DataFrame({'source': fdf['didx'], 'target': fdf['fidx'], 'value': fdf['size'], 'label':fdf['file']})
    tfdf.index = list(range(len(tfdf)))
    bdf = pd.concat([tddf, tfdf], ignore_index=True)

    tls = pd.Series(list(bdf['label']), index = list(bdf['target']))
    tls[0] = 'root'
    tls = tls.sort_index()

    # Assign colors based on file extension
    #
    tldf = pd.DataFrame({'label':tls.apply((lambda x: x.split('.')[0])), 'ext':tls.apply((lambda x: '.' + x.split('.')[-1]))})
    if not mimetypes.inited:
        mimetypes.init()
    types = defaultdict((lambda : 'unk/unk'), mimetypes.types_map)
    types['.dir'] = 'dir/dir'
    types['.root'] = 'root/root'
    tldf['type'] = tldf['ext'].map(types)
    cmap = sns.color_palette('rainbow', len(tldf['type'].unique()))
    cmap = [f'rgb({int(c[0]*255)},{int(c[1]*255)},{int(c[2]*255)})' for c in cmap]
    cmap = dict(zip(tldf['type'].unique(), cmap))
    tldf['colors'] = tldf['type'].map(cmap)

    # Generate Sankey diagram visuals
    #
    node = dict(customdata = tldf['label'], label=tldf['type'], color = tldf['colors'], pad = 15, hovertemplate = '%{customdata} (%{value} bytes)')
    link = dict(source = bdf['source'], target = bdf['target'], value = bdf['value'])
    data = go.Sankey(node = node, link = link, orientation='v')
    fig = go.Figure(data)

    for c in cmap.items():
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=10, color=c[1]), showlegend=True, name=c[0], ))
    fig.update_layout(legend=dict(orientation="v", yanchor="top", y=1.02, xanchor="right", x=0.01),
                      title_text="Filesize Sankey Diagram", font_size=10, autosize=True, plot_bgcolor='rgba(255,255,255,0)')

    logger.info("Sankey diagram built")

    op = out_path / 'filesize_sankey.html'
    logger.wrote_file(Path(op))
    fig.write_html(op)
    return f"Wrote to {op}"

if __name__ == "__main__":
    print(pointless_function()) # remove in production
    parser = argparse.ArgumentParser(prog='filesize_sankey',
                                     description='A short description of what your code does')
    parser.add_argument('-i', '--in_file', metavar='(NAME)_JSON', help='path to json file where \'NAME\' is tlk', required=True)
    parser.add_argument('-o', '--out_path', metavar='OUTPUT_PATH', help='where to send output(s)', required=False, default='.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity', required=False)
    args = parser.parse_args()

    logger = RootLogger()
    logger.setup(verb=args.verbose)

    print(run(args.in_file, args.out_path, logger))