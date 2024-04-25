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
    * Add mimetypes-based color coding
    * Refactor helpers into separate module in core
    * Prettify the output

Version:
    1.0.1

Author:
    Noah Duggan Erickson
"""

# CHANGELOG:
#   1.0.1: (09 April 2024)
#     - Added docstrings & comments
#   1.0: (05 April 2024)
#     - Initial Release
#     - (transfer from notebook to script)

import argparse
import os
# import mimetypes

import pandas as pd
import plotly.graph_objects as go

def pdEnumFiles(rootPath):
    ''' Enumerates files in a root directory and returns as a pandas dataframe

    Enumerates files in a root directory, with `inbox` directories excluded,
    and returns as a pandas dataframe with columns for root, file, and path.

    Args:
        rootPath (str): The path to the root directory to enumerate
    
    Returns:
        pd.DataFrame: A pandas dataframe with columns for root, file, and path
        for each file in the root directory
    '''
    fileList = []
    rootList = []
    pathList = []
    for root, dirs, files in os.walk(rootPath):
        for file in files:
            if (not 'inbox' in root):
                fileList.append(file)
                rootList.append(root)
                pathList.append(f"{root}/{file}")
    return pd.DataFrame({'root': rootList, 'file': fileList, 'path':pathList})

def dEnumDirs(rootPath):
    ''' Generates ID values for directories in a root directory

    Walks through a root directory and maps sequential ID values
    to each subdirectory via a dictionary.

    Args:
        rootPath (str): The path to the root directory to enumerate
    
    Returns:
        dict: A dictionary mapping each subdirectory path to a unique ID value
    '''
    pathDict = {'-':0}
    pathDict[rootPath] = 1
    counter = 2
    for root, dirs, files in os.walk(rootPath):
        for dire in dirs:
            pathDict[f"{root}/{dire}"] = counter
            counter += 1
    return pathDict

def pdEnumDirs(rootPath):
    ''' Enumerates directories in a root directory and returns a dataframe

    Enumerates directories in a root directory and returns a pandas
    dataframe with columns for root, dir, and path.
    
    Args:
        rootPath (str): The path to the root directory to enumerate

    Returns:
        pd.DataFrame: A pandas dataframe with columns root, dir, and path
    '''
    dirList = [rootPath]
    rootList = ['-']
    pathList = [rootPath]
    for root, dirs, files in os.walk(rootPath):
        for dire in dirs:
            dirList.append(dire)
            rootList.append(root)
            pathList.append(f"{root}/{dire}")
    return pd.DataFrame({'root': rootList, 'dir': dirList, 'path':pathList})

def run(json_path:str, out_path:str):
    # Enumerate files and directories, get filesizes
    #
    fdf = pdEnumFiles(json_path)
    fdf['size'] = fdf.apply(lambda x: os.stat(x['path']).st_size, axis=1)
    pdict = dEnumDirs(json_path)
    ddf = pdEnumDirs(json_path)

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

    # Aggregate file sizes by directory
    #
    ddf['size'] = fdf.groupby('didx').sum()['size']
    ddf = ddf.fillna(0)
    for i in range(25): # Arbitrary number of iterations to ensure all directories are accounted for
        tsr = ddf.groupby('pidx').sum()['size']
        for j, v in tsr.items():
            ddf.at[j, 'size'] = v
    ddf = ddf.dropna()

    # Build Sankey diagram connections
    #
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
    # TODO: Replace dict with mimetype-based color coding
    #
    tldf = pd.DataFrame({'label':tls.apply((lambda x: x.split('.')[0])), 'ext':tls.apply((lambda x: x.split('.')[-1]))})
    colorDict = {'root': 'black', 'dir': 'purple', 'json': 'blue', 'txt': 'white', 'jpg': 'orange', 'mp4':'red'}
    tldf['colors'] = tldf['ext'].map(colorDict)

    # Generate Sankey diagram visuals
    #
    node = dict(label = tldf['label'], color = tldf['colors'])
    link = dict(source = bdf['source'], target = bdf['target'], value = bdf['value'])
    data = go.Sankey(node = node, link = link)
    fig = go.Figure(data)

    fig.write_html(os.path.join(out_path, 'filesize_sankey.html'))
    return f"Wrote to {os.path.join(out_path, 'filesize_sankey.html')}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='filesize_sankey',
                                     description='A short description of what your code does')
    parser.add_argument('-json_path', metavar='path/to/jsons/',
                        help='path to json files', required=True)
    parser.add_argument('-out_path', metavar='path/to/output(/filesize_sankey.html)',)
    args = parser.parse_args()
    print(run(args.json_path, args.out_path))