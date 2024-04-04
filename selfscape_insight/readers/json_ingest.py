# -*- coding: utf-8 -*-
""" JSON -> CSV converter
WWU Facebook Data Science Project
Winter 2024

This module reads the data provided by the Facebook GDPR data download
and converts it into CSV files via Pandas dataframes. If the module
is run from the commandline, the user is able to specify the directory
where the CSV files will be written. Otherwise, the CSVs are written
to the temp directory.

Examples:
    Running from the command line::

        $ python3 json_ingest.py -i /path/to/json_root -o /where/to/write/csvs
        $ python3 json_ingest.py -h (for commandline help)
    
    Accessing via another script/module::

        >>> from json_ingest import JsonReader
        >>> reader = JsonReader("/path/to/json_root")

Dependencies:
    Pandas for general data handling
    tqdm for pretty progress bars

Todo:
    * Create group message json special case(?)
    * Other efficiency improvements as needed
    * argparse cleaning
    * Logging QoL improvements

Version:
    2.2

Author:
    Noah Duggan Erickson
"""

__version__ = '2.2'

import argparse
import logging
import time
import tracemalloc
import os
import tempfile

import pandas as pd
from tqdm import tqdm

from persona_sight.core import json_handling as jh

# CHANGELOG:
#   2.2: (15 March 2024)
#     - Added option to ignore messages folder (default true)
#     - Added docstrings, general cleaning
#   2.1: (7 March 2024)
#     - Refactored helpers into core package
#     - Major refactoring to align with OOP "general idea"
#     - argparse improvements
#     - logging QoL improvements
#     - removed development-residual code, general cleaning
#   2.0: (29 February 2024)
#     - module-ified for PROD transition via JsonReader class
#     - Transitioned to tempfile in JsonReader (TL running left untouched for ease of data access)
#   1.4: (23 February 2024)
#     - Removed SQL mode
#     - Transitioned (mostly) to argparse
#     - Added CSV file dump mode
#   1.3: (14 February 2024)
#     - Added special case to procFile for RAM
#       kindness on browser_cookies.json file
#   1.2: (2 February 2024)
#     - logging and quality-of-life improvements
#   1.1:
#     - Debugging
#   1.0:
#     - Initial Release

RAMWARN = 4 * 10**9
'''int: Amount of RAM that will raise warnings if exceeded.

Default is 4GB. Use x*10**9 for xGB, x*10**6 for xMB.
'''

class JsonReader:
    """
    A class used to read JSON files from a specified directory, convert them into
    pandas DataFrames, and then write those DataFrames to CSV files in a specified
    output directory.

    Attributes:
        csvs (dict): A dictionary mapping CSV filenames to their paths.
        temp (bool): Indicates whether the CSV files are being written to a temporary directory.
    """

    def __init__(self, jsonroot:str, csvroot:str='temp', read_messages:bool=False,
                 loglevel:int=logging.ERROR, ch:logging.StreamHandler=None):
        """
        Initializes the JsonReader with paths and logging settings.

        Args:
            jsonroot (str): The root directory where the JSON files are located.
            csvroot (str, optional): The directory where the CSV files will be written. Defaults to 'temp'.
            read_messages (bool, optional): Flag to indicate whether to read messages. Defaults to False.
            loglevel (int, optional): The logging level. Defaults to logging.ERROR.
            ch (logging.StreamHandler, optional): The logging stream handler. If None, a new one is created.

        Prints the start message with configuration details.
        """
        print(f"--------\nSTARTING JSON -> CSV INGEST\n  json path: {jsonroot}\n  dest path: {csvroot} \n    (exists? {os.path.exists(csvroot)})\n  skip msgs: {not read_messages}\n  lgng levl: {loglevel}\n--------") # pylint: disable=line-too-long
        self.csvs = {}
        logger = logging.getLogger("json")
        logger.setLevel(loglevel)
        if ch is None:
            ch = logging.StreamHandler()
            ch.setLevel(loglevel)
        logger.addHandler(ch)

        paths = self.enum_json(jsonroot, not read_messages, logger)

        dfs = {}
        for path in tqdm(paths, desc='reading json'):
            dft = self.read_json(path, logger)
            if dft[0] in dfs:
                dfs[dft[0]].append(dft[1])
            else:
                dfs[dft[0]] = [dft[1]]

        dfs = {key: pd.concat(dfs[key]) for key in tqdm(dfs.keys(), desc='building dfs')}

        self.temp = (csvroot == 'temp')
        if ((not self.temp) and (not os.path.exists(csvroot))):
            os.mkdir(csvroot)
        for df in tqdm(dfs.items(), desc='writing csvs'):
            if self.temp:
                with tempfile.NamedTemporaryFile(delete=False) as f:
                    df[1].to_csv(f.name)
                    self.csvs[df[0]] = f.name
            else:
                path = os.path.join(csvroot, f"{df[0]}.csv")
                df[1].to_csv(path)
                self.csvs[df[0]] = path
    
    def enum_json(self, rootpath:str, ignore_messages:bool, logger:logging.Logger) -> list:
        """
        Enumerates JSON files in the specified directory, optionally ignoring the messages folder.

        This method uses the `json_handling.enum_files` function to enumerate all
        JSON files in the given directory. It can optionally ignore the 'messages'
        folder to speed up the process. This method also measures the time and
        memory usage during the enumeration process.

        Args:
            rootpath (str): The root directory from which JSON files will be enumerated.
            ignore_messages (bool): Whether to ignore the 'messages' directory.
            logger (logging.Logger): Logger instance for logging information during enumeration.

        Returns:
            list: A list of paths to the enumerated JSON files.
        """
        tracemalloc.start()
        start = time.time()
        paths = jh.enum_files(rootpath, blacklist=(['messages'] if ignore_messages else []))
        end = time.time()
        c, p = tracemalloc.get_traced_memory()
        logger.info(f"Enumerated {len(paths)} files in {round((end-start) * 10**3, 3)} ms and used a peak of {round(p * 10**-6, 3)}MB RAM (Current: {round(c * 10**-6, 3)}MB)") # pylint: disable=line-too-long
        tracemalloc.stop()
        return paths
    
    def read_json(self, path:tuple, logger=logging.Logger) -> tuple:
        """
        Reads and processes a JSON file from the given path, converting it into a DataFrame.

        This method attempts to process a JSON file into a pandas DataFrame by using the
        `json_handling.proc_file` function. It measures the processing time and memory usage,
        logging these metrics. If processing takes too long, it catches a `TimeoutError`
        and logs an error message.

        Args:
            path (tuple): A tuple containing the directory and filename of the JSON file to be processed.
            logger (logging.Logger): Logger instance for logging information during file processing.

        Returns:
            tuple: A tuple containing the name of the DataFrame (as a string) and the DataFrame itself.

        Raises:
            TimeoutError: If processing the JSON file takes too long.
        """
        out = None
        start = time.time()
        tracemalloc.start()
        try:
            out = jh.proc_file(path, logger)
        except TimeoutError:
            logger.error(f"Processing file {path[1]} took too long. Skipping...")
        end = time.time()
        c, p = tracemalloc.get_traced_memory()
        fp = os.path.join(path[0], path[1])
        logger.info(f"Processed {out[0]} ({round(os.path.getsize(fp) * 10**-6, 3)}MB) in {round((end-start) * 10**3, 3)} ms using {round(c * 10**-6, 3)}MB RAM (peak: {round(p * 10**-6, 3)}MB)") # pylint: disable=line-too-long
        if p >= RAMWARN:
            logger.warning(f"HIGH RAM USAGE! Peaked at {round(p * 10**-9, 3)}GB")
        tracemalloc.stop()
        return out

    def get_csv(self, name:str) -> str:
        """
        Retrieves the path to the CSV file corresponding to the given name.

        Args:
            name (str): The name of the CSV file to retrieve.

        Returns:
            str: The path to the CSV file.

        Raises:
            KeyError: If no CSV file with the given name exists.
        """
        if name in self.csvs and self.csvs[name] is None:
            raise KeyError(f"csv '{name}' does not exist!")
        return self.csvs[name]
    
    def get_names(self) -> list:
        """
        Returns a list of the names of all CSV files generated by the JsonReader.

        This method allows for easy access to the names of all CSV files that have
        been generated, which can be useful for iterating over the files or
        accessing specific ones.

        Returns:
            list: A list of strings, each representing the name of a generated CSV file.
        """
        return list(self.csvs.keys())
    
    def key_info(self, key:str) -> str:
        """
        Provides detailed information about a specific CSV file identified by its key.

        This method reads the CSV file corresponding to the provided key, calculates
        its shape (number of rows and columns), and its memory usage, and returns
        this information as a formatted string.

        Args:
            key (str): The key (name) of the CSV file to retrieve information for.

        Returns:
            str: A formatted string containing details about the CSV file's shape and memory usage.

        Raises:
            KeyError: If the specified key does not correspond to any existing CSV file.
        """
        if key not in self.csvs.keys():
            raise KeyError(f"{key} does not exist")
        
        df = pd.read_csv(self.csvs[key])
        sh = df.shape
        sp = df.memory_usage(deep=True).sum()
        return f"\n{key}:\n  shape: {sh} RAM: {round(sp * 10**-6, 3)}MB"
    
    def close(self):
        """
        Cleans up by deleting temporary CSV files, if applicable.

        This method is responsible for deleting any temporary CSV files created
        during the JsonReader's operation. It is typically called when the
        JsonReader instance is no longer needed, to ensure that no unnecessary
        files are left on the filesystem.
        """
        if self.temp:
            for k in self.csvs.keys():
                os.unlink(self.csvs[k])
                self.csvs[k] = None
    
    def __str__(self) -> str:
        """
        Returns a string representation of the JsonReader instance, listing all CSVs managed by it.

        This method provides an overview of the CSV files that have been generated by this instance,
        including their names, shapes, and memory usages. It is useful for quickly understanding
        the state and output of the JsonReader.

        Returns:
            str: A formatted string containing an overview of the CSV files managed by the JsonReader.
        """
        out = "--------\nCSVS:"
        for k in self.csvs.keys():
            df = pd.read_csv(self.csvs[k])
            sh = df.shape
            sp = df.memory_usage(deep=True).sum()
            out += f"\n{k}:\n  shape: {sh} RAM: {round(sp * 10**-6, 3)}MB"
        out += "\n--------"
        return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='python3 jsonIngest.py')
    parser.add_argument('-i',  '--in_path',
                        required=True, dest='json_root', type=str,
                        metavar='/PATH/TO/JSON_ROOT/',
                        help='path to root of JSON data')
    parser.add_argument('-o', '--out_path',
                        required=True, dest='csv_root', type=str,
                        metavar='/WHERE/TO/WRITE/CSVS/',
                        help='directory of where to put outputted csvs')
    parser.add_argument('-m', '--read_messages',
                        action='store_true', dest='m',
                        help="If present, don't skip the messages folder - may take significantly longer to run")
    parser.add_argument('-l', '--log',
                        action='store_true', dest='l',
                        help='If present, prints logging information to stdout')
    parser.add_argument('-v', '--log_v',
                        action='store_true', dest='v',
                        help='If present, prints debug-level logging information to stdout')
    args = parser.parse_args()

    v = args.v
    l = v or args.l

    if l:
        level = logging.DEBUG if v else logging.INFO
    else:
        level = logging.ERROR

    ch = logging.StreamHandler()
    ch.setLevel(level)
    print("JSON -> CSV INGESTER")
    print(f"       V. {__version__}       \n")
    reader = JsonReader(jsonroot=args.json_root, csvroot=args.csv_root,
                        read_messages=args.m, loglevel=level, ch=ch)
    print(reader)
