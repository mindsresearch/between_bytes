""" Core functions for generating dataframes for file size sankey diagrams

Functions:
    pdEnumFiles(rootPath): Enumerates files in a root directory and returns as a pandas dataframe
    dEnumDirs(rootPath): Generates ID values for directories in a root directory
    pdEnumDirs(rootPath): Enumerates directories in a root directory and returns a dataframe
"""
import os
from pathlib import Path

import pandas as pd

def pdEnumFiles(root_path:Path):
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
    for root, dirs, files in root_path.walk():
        for file in files:
            if (not 'inbox' in str(root)):
                fileList.append(file)
                rootList.append(root)
                pathList.append(root / file)
    return pd.DataFrame({'root': rootList, 'file': fileList, 'path':pathList})

def dEnumDirs(root_path):
    ''' Generates ID values for directories in a root directory

    Walks through a root directory and maps sequential ID values
    to each subdirectory via a dictionary.

    Args:
        rootPath (str): The path to the root directory to enumerate
    
    Returns:
        dict: A dictionary mapping each subdirectory path to a unique ID value
    '''
    pathDict = {'-':0}
    pathDict[root_path] = 1
    counter = 2
    for root, dirs, files in root_path.walk():
        for dire in dirs:
            pathDict[f"{root}/{dire}"] = counter
            counter += 1
    return pathDict

def pdEnumDirs(root_path):
    ''' Enumerates directories in a root directory and returns a dataframe

    Enumerates directories in a root directory and returns a pandas
    dataframe with columns for root, dir, and path.
    
    Args:
        rootPath (str): The path to the root directory to enumerate

    Returns:
        pd.DataFrame: A pandas dataframe with columns root, dir, and path
    '''
    dirList = [root_path]
    rootList = ['-']
    pathList = [root_path]
    for root, dirs, files in root_path.walk():
        for dire in dirs:
            dirList.append(dire)
            rootList.append(root)
            pathList.append(f"{root}/{dire}")
    return pd.DataFrame({'root': rootList, 'dir': dirList, 'path':pathList})