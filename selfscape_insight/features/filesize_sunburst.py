''' Create a sunburst diagram of file sizes in a directory tree

Much like filesize_sankey, this script is designed to visualize
the sizes of files in a directory tree colored by type. However,
this script creates a sunburst diagram instead of a sankey.

Functions:
    run: The main function of the script. It takes in a path to a
         directory and returns a string indicating where the output
         HTML file was written.

Example usage:
    >>> from features import filesize_sunburst as fsb
    >>> fsb.run(root_path, out_path, logger)
    filepath to HTML page containing results of analysis

    $ python3 filesize_sunburst.py -i /path/to/jsons/ -o /path/to/output

Dependencies:
    pandas for data handling
    plotly for datavis
    seaborn for color palettes

Note:
    This sub-module is part of the 'selfscape_insight' package in the 'features' module.

Author:
    Noah Duggan Erickson

Version:
    1.0
'''

__version__ = '1.0'
import argparse
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

def run(in_path:Path, out_path:Path, logger:SsiLogger):
    logger.use_file(Path('ALL'), 'metadata')
    all_the_files = list(in_path.rglob('*'))
    all_the_files.append(in_path)
    logger.debug(f"Found {len(all_the_files)} files and directories")

    df = pd.DataFrame({'file': all_the_files,
                       'path': [str(f) for f in all_the_files],
                       'size': [f.stat().st_size for f in all_the_files],
                       'parent': [str(f.parent) for f in all_the_files],
                       'label': [f.name for f in all_the_files]})

    df.at[len(df)-1, 'parent'] = ''

    logger.debug("Getting mimetypes...")
    if not mimetypes.inited:
            mimetypes.init()
    types = defaultdict((lambda : 'dir/dir'), mimetypes.types_map)
    df['type'] = df['file'].apply((lambda x: types[x.suffix]))
    df.at[len(df)-1, 'type'] = 'root/root'
    logger.debug(f"Found {len(df['type'].unique())} unique types")

    cmap = sns.color_palette('rainbow', len(df['type'].unique()))
    cmap = [f'rgb({int(c[0]*255)},{int(c[1]*255)},{int(c[2]*255)})' for c in cmap]
    cmap = dict(zip(df['type'].unique(), cmap))
    df['colors'] = df['type'].map(cmap)

    logger.info("Building Sunburst diagram")
    fig = go.Figure(
            go.Sunburst(parents=df['parent'], ids=df['path'], values=df['size'], labels=df['label'],
                        hovertemplate='%{label}', marker=dict(colors=df['colors']))
                    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    
    op = out_path / 'filesize_sunburst.html'
    logger.wrote_file(op)
    fig.write_html(op)
    return f"Wrote to {op}"

if __name__ == "__main__":
    print(pointless_function()) # remove in production
    parser = argparse.ArgumentParser(prog='filesize_sunburst',
                                     description='A short description of what your code does')
    parser.add_argument('-i', '--in_path', metavar='JSON_PATH', help='path to root of download', required=True)
    parser.add_argument('-o', '--out_path', metavar='OUTPUT_PATH', help='where to send output HTML', required=False, default='.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity', required=False)
    args = parser.parse_args()

    logger = RootLogger()
    logger.setup(verb=args.verbose)

    print(run(Path(args.in_path), Path(args.out_path), logger))