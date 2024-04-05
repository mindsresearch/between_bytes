"""
A module for handling the reading, processing, and transformation of JSON files into pd.DataFrames.

This module provides functionalities to enumerate JSON files within a specified directory,
potentially excluding certain subdirectories. It offers a method to convert JSON data into
a flat pandas DataFrame, making nested JSON structures easier to analyze and work with.
Special processing logic is included for certain types of JSON files, such as
'browser_cookies.json', to accommodate their unique structures. The module utilizes a
timeout mechanism to prevent excessively long processing times for any given file.

Functions:
    enum_files(rootpath, ext='json', blacklist=[]):
        Enumerates files of a given extension within a root directory.
    json_df(data):
        Converts JSON data into a pandas DataFrame, expanding any nested structures.
    proc_file(path, logger=None):
        Processes a JSON file into a DataFrame with an appropriate name.

Dependencies:
    pandas: Used for creating and manipulating DataFrames.
    timeout_decorator: Utilized to set a maximum processing time for file conversion.
    flatsplode: A utility for flattening nested JSON structures.

Note:
    This module is designed with the expectation that JSON file structures
    can vary significantly. As such, it includes generic handling for diverse
    structures but may require modifications or extensions to handle new,
    unseen JSON formats efficiently.
"""

import os
import logging
import json

import pandas as pd
import timeout_decorator as time_dec
from flatsplode import flatsplode

def enum_files(rootpath:str, ext:str='json', blacklist:list=None, logger:logging.Logger=logging.getLogger(__name__)) -> list:
    """
    Lists files of a given extension within a root directory, optionally blacklisting subdirectories.

    This function recursively traverses the specified root directory and lists
    all files with the given extension.
    It can exclude files located within any of the subdirectories listed in the blacklist.

    Args:
        rootpath (str): The path to the root directory to search within.
        ext (str, optional): The file extension to search for. Defaults to 'json'.
        blacklist (list, optional): A list of directory names to exclude from the search.
            Defaults to None.

    Returns:
        list: A list of 2-tuples, each containing the directory path and the file name of found files.
    """
    print(f"BLACKLIST: (len: {len(blacklist)})\n  {blacklist}")
    fl = []
    for root, dirs, files in os.walk(rootpath): # pylint: disable=unused-variable
        for file in files:
            if file.endswith(f'.{ext}'):
                if (blacklist is not None) and (any(bad in root for bad in blacklist)):
                    logger.debug(f'denied by BL: {"/".join(root.split("/")[-5:])}')
                else:
                    fl.append((root, file))
    return fl

def json_df(data) -> pd.DataFrame:
    """
    Converts JSON data into a pandas DataFrame, expanding any nested structures.

    This function transforms nested JSON data into a flat pandas DataFrame using
    the 'flatsplode' function. It handles both dictionaries and lists as input.
    Certain prefixes in column names are removed to avoid potential
    issues with database column name length restrictions.

    Args:
        data (dict or list): The JSON data to convert, either as a dictionary or a list.

    Returns:
        pd.DataFrame: A DataFrame containing the flattened JSON data.
    """
    if not isinstance(data, dict):
        data = {'0': data}
    data = flatsplode(data, '_')
    df = pd.DataFrame(data)
    #df.dropna(axis=1, how='all', inplace=True)
    cols = df.columns
    if (len(cols) > 1) and (all([c.startswith('0_') for c in cols])):
        cols = [c[2:] for c in cols]
    cols = [c.replace("media_", "").replace("metadata_", "").replace("exif_", "") for c in cols]
    df.columns = cols
    return df

@time_dec.timeout(60)
def proc_file(path:tuple, logger:logging.Logger=None) -> tuple:
    """
    Processes a JSON file, converting it to a pd.DataFrame with an appropriate name.

    This function reads a JSON file from the specified path, handling different data structures within.
    For example, it has a special case for handling 'browser_cookies.json' files. The function applies
    a timeout decorator to limit processing time to 60 seconds, logging the processing attempt and outcome.

    Args:
        path (tuple): A 2-tuple containing the directory and file name of the JSON file to be processed.
        logger (logging.Logger, optional): A logging.Logger instance for logging information about the file processing.
                                          If None, logging is skipped.

    Returns:
        tuple: A 2-tuple containing a string with the canonical name for the data and the pandas DataFrame with the processed data.

    Raises:
        TimeoutError: If processing the JSON file takes longer than 60 seconds.
    """
    fp = os.path.join(path[0], path[1])
    l = logger is None
    with open(fp, 'r', encoding='utf-8') as file:
        if l:
            logger.debug(f"Processing {round(os.path.getsize(fp) * 10**-6, 3)}MB file: {fp}")
        data = json.load(file)

    if path[1] == 'browser_cookies.json':
        keys = list(data.keys())
        data = data[keys[0]]
        df = pd.DataFrame([[key, value] for key, values in data.items() for value in values],
                          columns=['cookie', 'timestamp'])
        return (keys[0], df)
    if isinstance(data, list):
        return (path[1][:-5], json_df(data))
    keys = list(data.keys())
    if len(keys) == 1:
        return (keys[0], json_df(data[keys[0]]))
    return (path[1][:-5], json_df(data))
