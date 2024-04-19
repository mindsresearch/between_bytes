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
from flatsplode import flatsplode

def enum_files(rootpath:str, ext:str='json', blacklist:list=[], logger:logging.Logger=logging.getLogger(__name__)) -> list:
    """
    Lists files of a given extension within a root directory, optionally blacklisting subdirectories.

    This function recursively traverses the specified root directory and lists
    all files with the given extension.
    It can exclude files located within any of the subdirectories listed in the blacklist.

    Args:
        rootpath (str): The path to the root directory to search within.
        ext (str, optional): The file extension to search for. Defaults to 'json'.
        blacklist (list, optional): A list of directory names to exclude from the search.
            Defaults to empty list (deny nothing).

    Returns:
        list: A list of 2-tuples, each containing the directory path and the file name of found files.
    """
    logger.debug(f"BLACKLIST: (len: {len(blacklist)})\n  {blacklist}")
    fl = []
    for root, dirs, files in os.walk(rootpath): # pylint: disable=unused-variable
        for file in files:
            if file.endswith(f'.{ext}'):
                if (blacklist is not None) and (any(bad in root for bad in blacklist)):
                    logger.debug(f'denied by BL: {(os.sep).join(root.split(os.sep)[-5:])}')
                else:
                    fl.append((root, file))
    return fl

def proc_json(path:tuple, logger:logging.Logger=None) -> tuple:
    """
    Processes a JSON file, converting it to a dict/list with an appropriate name.

    This function reads a JSON file from the specified path, handling different data structures within.
    For example, it has a special case for handling 'browser_cookies.json' files.

    Args:
        path (tuple): A 2-tuple containing the directory and file name of the JSON file to be processed.
        logger (logging.Logger, optional): A logging.Logger instance for logging information about the file processing.
                                          If None, logging is skipped.

    Returns:
        tuple: A 2-tuple containing a string with the canonical name for the data and the obj with the processed data.
    """
    fp = os.path.join(path[0], path[1])
    l = logger is None
    with open(fp, 'r', encoding='utf-8') as file:
        if l:
            logger.debug(f"Processing {round(os.path.getsize(fp) * 10**-6, 3)}MB file: {fp}")
        data = json.load(file)

    n = get_name(data)
    if n is not None:
        return (n, data[n])
    return (path[1][:-5], data)

def get_name(obj) -> str:
    """
    Returns the canonical name of the object, if it has one (if not, returns None).
    """
    if isinstance(obj, dict) and (len(obj.keys()) == 1):
        return list(obj.keys())[0]
    return None

def desc_json(data, indent:int=0, sub_indent:int=0) -> str:
    """
    Returns a prettyprint string description of the JSON data.
    """
    if isinstance(data, dict):
        if len(data) == 0:
            return ''
        d = data.copy()
        k = list(d.keys())[0]
        v = d.pop(k)
        return f"\n{' ' * indent}{'-' * sub_indent}{k}:" + desc_json(v, indent, sub_indent+2) + desc_json(d, indent, sub_indent)
    elif isinstance(data, list):
        return f" list - " + (f"idx 0/{len(data)-1}:" + desc_json(data[0], indent, sub_indent) if len(data) > 0 else '[]')
    else:
        return f" {str(type(data))[8:-2]}"

if __name__ == '__main__':
    x = {'tlk': [{'k1': 1, 'k2': {'k2a': 'val', 'k2b': True}, 'k3': [4, 5, 6]}]}
    print(desc_json(x))