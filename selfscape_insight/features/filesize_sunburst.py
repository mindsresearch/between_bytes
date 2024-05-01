''' Create a sunburst diagram of file sizes in a directory tree

Much like filesize_sankey, this script is designed to visualize
the sizes of files in a directory tree colored by type. However,
this script creates a sunburst diagram instead of a sankey.

Functions:
    run: The main function of the script. It takes in a path to a
         directory and returns a string indicating where the output
         HTML file was written. It can also take in a mode argument
        to specify whether to include all files, only JSON files,
        or both.

    enum_files: Enumerates all files in a directory tree and returns
                a DataFrame with columns for the file, path, size,
                parent directory, and label.

    get_mimetypes: Uses the mimetypes module to get the MIME type of
                     each file in a Series of Path objects.

    get_cmap: Creates a color map for the sunburst diagram based on
                the unique MIME types in a Series of MIME types.

    create_legend: Creates an HTML legend for the sunburst diagram
                    based on the color map.

    build_sunburst: Builds a sunburst diagram from a DataFrame of files.

Example usage:
    >>> from features import filesize_sunburst as fsb
    >>> fsb.run(root_path, out_path, logger, [mode])
    filepath to HTML page containing results of analysis

    $ python3 filesize_sunburst.py -i /path/to/jsons/ -o /path/to/output

Dependencies:
    pandas for data handling
    plotly for datavis
    seaborn for color palettes

Note:
    This sub-module is part of the 'selfscape_insight'
    package in the 'features' module.

Author:
    Noah Duggan Erickson

Version:
    1.1
'''

__version__ = '1.1'
import argparse
import sys
from pathlib import Path
import mimetypes
from collections import defaultdict

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns

if __name__ == '__main__':
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.various_helpers import pointless_function # pylint disable=wrong-import-position
from core.log_aud import SsiLogger, RootLogger # pylint disable=wrong-import-position

def enum_files(in_path:Path, json_only:bool=False) -> pd.DataFrame:
    if json_only:
        all_the_files = list(in_path.rglob('*.json'))
        all_the_files += list(in_path.rglob('*/'))
    else:
        all_the_files = list(in_path.rglob('*'))
    all_the_files.append(in_path)

    df = pd.DataFrame({'file': all_the_files,
                       'path': [str(f) for f in all_the_files],
                       'size': [f.stat().st_size for f in all_the_files],
                       'parent': [str(f.parent) for f in all_the_files],
                       'label':
                       [f.stem.replace('_', ' ') for f in all_the_files]})

    df.at[len(df)-1, 'parent'] = ''
    return df

def get_mimetypes(files:pd.Series) -> pd.Series:
    if not mimetypes.inited:
        mimetypes.init()
    types = defaultdict((lambda : 'dir/dir'), mimetypes.types_map)
    types['.json'] = 'data/json'
    t = files.apply((lambda x: types[x.suffix]))
    t.at[len(t)-1] = 'root/root'
    t = t.apply((lambda x: x.split('/')[0]))
    return t

def get_cmap(types:pd.Series) -> dict:
    cmap = sns.color_palette('rainbow', len(types.unique()))
    cmap = [f'rgb({int(c[0]*255)},{int(c[1]*255)},{int(c[2]*255)})'
            for c in cmap]
    return dict(zip(types.unique(), cmap))

def create_legend(cmap:dict) -> str:
    lines = ['<tr style="color:%s"><td>%s</td><td>%s</td></tr>' %
             (c, t, c) for t, c in cmap.items()]
    return '''
    <!DOCTYPE html>
    <html>
    <head>
    <title>Filesize_sunburst Legend</title>
    </head>
    <body>
    <h1>Filesize_sunburst Legend</h1>
    <table>
    %s
    </table>
    </body>
    </html>
    ''' % ''.join(lines)

def build_sunburst(df:pd.DataFrame) -> go.Sunburst:
    return go.Sunburst(parents=df['parent'],
                       ids=df['path'],
                       values=df['size'],
                       labels=df['label'],
                       hovertemplate='%{label}',
                       marker=dict(colors=df['colors'])
                       )

# mode: 0 = all files, 1 = json only, 2 = both
def run(in_path:Path, out_path:Path, logger:SsiLogger, mode:int=0):
    match mode:
        case 0:
            logger.use_file(Path('ALL'), 'metadata')
            df = enum_files(in_path)
        case 1:
            logger.use_file(Path('JSON'), 'metadata')
            df = enum_files(in_path, json_only=True)
        case 2:
            logger.use_file(Path('ALL'), 'metadata')
            df = enum_files(in_path)
            logger.use_file(Path('JSON'), 'metadata')
            df_json = enum_files(in_path, json_only=True)
        case _:
            logger.crit('Invalid mode', ValueError)

    logger.debug(df.head().to_string())
    if mode == 2:
        logger.debug(df_json.head().to_string())

    logger.info('Getting mimetypes...')
    df['type'] = get_mimetypes(df['file'])
    logger.info('(1) Found %i unique types: %s' %
                (len(df['type'].unique()),
                 str(df['type'].unique())))
    if mode == 2:
        df_json['type'] = get_mimetypes(df_json['file'])
        logger.info('(2) Found %i unique types: %s' %
                    (len(df_json['type'].unique()),
                     str(df_json['type'].unique())))

    cmap = get_cmap(df['type'])
    df['colors'] = df['type'].map(cmap)
    if mode == 2:
        df_json['colors'] = df_json['type'].map(cmap)

    logger.info('Building Sunburst diagram')
    if mode < 2:
        fig = go.Figure(build_sunburst(df))
    else:
        fig = make_subplots(rows=1, cols=2,
                            specs=[[{'type': 'domain'}, {'type': 'domain'}]],
                            subplot_titles=['All Files', 'JSON Files'])
        fig.add_trace(build_sunburst(df), 1, 1)
        fig.add_trace(build_sunburst(df_json), 1, 2)

    op = out_path / 'filesize_sunburst'
    op.mkdir(exist_ok=True)
    logger.wrote_file(op / 'sunburst.html')
    fig.write_html(op / 'sunburst.html')
    with open(op / 'legend.html', 'w', encoding='utf-8') as f:
        f.write(create_legend(cmap))
    logger.wrote_file(op / 'legend.html')
    return f'Wrote sunburst.html and legend.html to {op}'

if __name__ == '__main__':
    print(pointless_function()) # remove in production
    parser = argparse.ArgumentParser(prog='filesize_sunburst',
                                     description='Create a sunburst diagram of file sizes in a directory tree') # pylint disable=line-too-long
    parser.add_argument('-i', '--in_path', metavar='JSON_PATH',
                        required=True,
                        help='path to root of download')
    parser.add_argument('-o', '--out_path', metavar='OUTPUT_PATH',
                        required=False, default='.',
                        help='where to send output HTML')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='increase verbosity')

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('-j', '--json_only', action='store_true',
                            help='only process json files')
    mode_group.add_argument('-a', '--all_files', action='store_true',
                            help='process all files')
    mode_group.add_argument('-b', '--both', action='store_true',
                            help='process all files and json files side-by-side') # pylint disable=line-too-long

    args = parser.parse_args()

    m_logger = RootLogger()
    m_logger.setup(verb=args.verbose)

    if args.json_only:
        prog_mode = 1
    elif args.both:
        prog_mode = 2
    else:
        prog_mode = 0

    print(run(Path(args.in_path), Path(args.out_path),
              m_logger, mode=prog_mode))
