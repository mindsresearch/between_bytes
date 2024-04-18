# -*- coding: utf-8 -*-
''' JSON Reader
WWU Facebook Data Science Project
Winter/Spring 2024

New docstring coming soon!

Examples:
    Running from the command line::

        $ python3 json_ingest.py -i /path/to/json_root
        $ python3 json_ingest.py -h (for commandline help)
    
    Accessing via another script/module::

        >>> from json_ingest import JsonReader
        >>> reader = JsonReader('/path/to/json_root')

Dependencies:
    tqdm for pretty progress bars

Todo:
    * Create group message json special case(?) (wontfix)
    * Other efficiency improvements as needed (wontfix)
    * argparse cleaning
    * Logging QoL improvements

Version:
    3.0.0rc1

Author:
    Noah Duggan Erickson
'''

__version__ = '3.0.0rc1'

### 3.0.0rc1 LIST OF CHANGES:
### Changed from CSVs as output filetype to pickles (PKLs)
### Changes to JsonReader class I/O:
###   - attr csvs now private
###   - attr path now private
###   - func read_json now private
###   - func enum_json now private
###   - rename func get_csv -> get_pkl
###   - func get_pkl now returns JSON object (list or dict) instead of path
### TODO: Update docstrings, clean up code, update examples
import argparse
import logging
import time
import tracemalloc
import os
import sys
import tempfile
import shutil
import pathlib
import json
import pickle

from tqdm import tqdm

# If running from the commandline, add the parent directory to the path
#
if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

from core import json_handling as jh # pylint: disable=wrong-import-position

# CHANGELOG:
#   3.0.0rc1: (18 April 2024)
#     - Major refactor away from CSV stuff
#     - Transition to PKLs
#     - Refer to detailed list of changes above imports.
#   2.3.1: (15 April 2024)
#     - Hotfix for issues with internal imports
#     - Removal of timeout decorator due to OS issues
#         (in json_handling)
#   2.3: (5 April 2024)
#     - Cleaned up some of the CLI args structure
#     - Cleaned up tempfile handling
#     - Added CSV creation/deletion/access audit logging
#   2.2: (15 March 2024)
#     - Added option to ignore messages folder (default true)
#     - Added docstrings, general cleaning
#   2.1: (7 March 2024)
#     - Refactored helpers into core package
#     - Major refactoring to align with OOP 'general idea'
#     - argparse improvements
#     - logging QoL improvements
#     - removed development-residual code, general cleaning
#   2.0: (29 February 2024)
#     - module-ified for PROD transition via JsonReader class
#     - Transitioned to tempfile in JsonReader (TL running
#         left untouched for ease of data access)
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
    '''
    A class used to read JSON files from a specified directory,
    and convert them into PKL files.

    Attributes:
        No public attributes.
    '''

    def __init__(self, jsonroot:str, pklroot:str='temp',
                 read_messages:bool=False, dev:bool=False,
                 logger:logging.Logger=logging.getLogger(__name__),
                 auditor:logging.Logger=logging.getLogger('jsonAuditor')):
        '''
        Initializes the JsonReader with paths and logging settings.

        Args:
            jsonroot (str): The root directory where the JSON files are located.
            pklroot (str, optional): The directory where the JSB files will be written. Defaults to 'temp'.
            read_messages (bool, optional): Flag to indicate whether to read messages. Defaults to False.
            loglevel (int, optional): The logging level. Defaults to logging.ERROR.
            ch (logging.StreamHandler, optional): The logging stream handler. If None, a new one is created.

        Prints the start message with configuration details.
        '''

        self._pkls = {}
        self._logger = logger
        self._auditor = auditor
        self._dev = dev
        self._logger.info(f'\n--------\nSTARTING JSON -> JSB INGEST {__version__}\n  json path: {jsonroot}\n  dest path: {pklroot} \n    (exists? {os.path.exists(pklroot)})\n  skip msgs: {not read_messages}\n  lgng levl: {self._logger.level}\n--------') # pylint: disable=line-too-long

        paths = self._enum_json(jsonroot, not read_messages)

        objs = {} # dict to hold de-ser. json objs
        for p in tqdm(paths, desc='reading json'):
            data = self._read_json(p)
            if data[0] in objs.keys():
                if not isinstance(objs[data[0]], list):
                    objs[data[0]] = [objs[data[0]]]
                objs[data[0]].append(data[1])
            else:
                objs[data[0]] = data[1]

        self._temp = pklroot == 'temp'
        self._path = pathlib.Path(tempfile.mkdtemp() if self._temp else pklroot)

        if self._temp:
            self._auditor.info(f'Temp directory created at {self._path}')
        elif not self._path.exists():
            self._path.mkdir()
            self._auditor.info(f'Created directory {self._path}')

        # This is where json -> pkl conversion happens.
        # Everything above this point is json objects.
        #
        if dev:
            for obj in tqdm(objs.items(), desc='writing jsons'):
                p = os.path.join(self._path, f'{obj[0]}.json')
                with open(p, 'w', encoding='utf-8') as file:
                    json.dump(obj[1], file)
                self._auditor.debug(f' Created {p}')
                self._pkls[obj[0]] = p
        else:
            for obj in tqdm(objs.items(), desc='writing pkls'):
                p = os.path.join(self._path, f'{obj[0]}.pkl')
                with open(p, 'wb') as file:
                    pickle.dump(obj[1], file)
                self._auditor.debug(f' Created {p}')
                self._pkls[obj[0]] = p

    def _enum_json(self, rootpath:str, ignore_messages:bool) -> list:
        '''
        Enumerates JSON files in the specified directory, optionally ignoring the messages folder(s).

        This method uses the `json_handling.enum_files` function to enumerate all
        JSON files in the given directory. It can optionally ignore the 'messages'
        folder(s) to speed up the process. This method also measures the time and
        memory usage during the enumeration process.

        Args:
            rootpath (str): The root directory from which JSON files will be enumerated.
            ignore_messages (bool): Whether to ignore the 'messages' directories.
            logger (logging.Logger): Logger instance for logging information during enumeration.

        Returns:
            list: A list of paths to the enumerated JSON files.
        '''
        tracemalloc.start()
        start = time.time()
        paths = jh.enum_files(rootpath, blacklist=(['messages'] if ignore_messages else []), logger=self._logger)
        end = time.time()
        c, p = tracemalloc.get_traced_memory()
        self._logger.info(f'Enumerated {len(paths)} files in {round((end-start) * 10**3, 3)} ms and used a peak of {round(p * 10**-6, 3)}MB RAM (Current: {round(c * 10**-6, 3)}MB)') # pylint: disable=line-too-long
        tracemalloc.stop()
        return paths

    def _read_json(self, path:tuple) -> tuple:
        '''
        Reads and processes a JSON file from the given path, converting it into a dict/list.

        This method attempts to process a JSON file into a pandas DataFrame by using the
        `json_handling.proc_file` function. It measures the processing time and memory usage,
        logging these metrics. If processing takes too long, it catches a `TimeoutError`
        and logs an error message.

        Args:
            path (tuple): A tuple containing the directory and filename of the JSON file to be processed.
            logger (logging.Logger): Logger instance for logging information during file processing.

        Returns:
            tuple: A tuple containing the name of the obj (as a string) and the obj itself.
        '''
        out = None
        start = time.time()
        tracemalloc.start()
        out = jh.proc_json(path, self._logger) # everything else here is logging
        end = time.time()
        c, p = tracemalloc.get_traced_memory()
        fp = os.path.join(path[0], path[1])
        self._logger.debug(f'Processed {out[0]} ({round(os.path.getsize(fp) * 10**-6, 3)}MB) in {round((end-start) * 10**3, 3)} ms using {round(c * 10**-6, 3)}MB RAM (peak: {round(p * 10**-6, 3)}MB)') # pylint: disable=line-too-long
        if p >= RAMWARN:
            self._logger.warning(f'HIGH RAM USAGE! Peaked at {round(p * 10**-9, 3)}GB')
        tracemalloc.stop()
        return out

    def get_pkl(self, name:str):
        '''
        Returns human JSON object from PKL of specified name.

        Args:
            name (str): The name of the JSB file to retrieve.

        Returns:
            list or dict: The JSON object from the specified JSB file.

        Raises:
            KeyError: If no JSB file with the given name exists.
        '''
        if name not in self._pkls.keys():
            self._logger.error(f'pkl "{name}" does not exist!')
            self._logger.error('Please report this error if you believe this file should exist!')
            raise KeyError(f'pkl "{name}" does not exist!')
        self._auditor.info(f'Retrieved {name}')
        path = self._pkls[name]
        if self._dev:
            with open(path, 'r', encoding='utf-8') as file:
                return json.load(file)
        with open(path, 'rb') as file:
            return pickle.load(file)

    def get_names(self) -> list:
        '''
        Returns a list of the names of all JSB files generated by the JsonReader.

        This method allows for easy access to the names of all JSB files that have
        been generated, which can be useful for iterating over the files or
        accessing specific ones.

        Returns:
            list: A list of strings, each representing the name of a generated JSON file.
        '''
        return list(self._pkls.keys())

    def key_info(self, key:str, indent=2) -> str:
        '''
        Provides detailed information about a specific JSB file identified by its key.

        This method reads the JSB file corresponding to the provided key, calculates
        its shape (number of rows and columns), and its memory usage, and returns
        this information as a formatted string.

        Args:
            key (str): The key (name) of the JSB file to retrieve information for.

        Returns:
            str: A formatted string containing details about the JSB file's shape and memory usage.

        Raises:
            KeyError: If the specified key does not correspond to any existing JSB file.
        '''
        if key not in self._pkls.keys():
            self._logger.error(f'{key} does not exist')
            raise KeyError(f'{key} does not exist')

        data = self.get_pkl(key)
        self._auditor.info(f'Retrieved info for {key}')

        return f'{key}:\n{' ' * indent}RAM: {sys.getsizeof(data) * 10**-3}KB\n{' ' * indent}structure:{jh.desc_json(data, indent=indent+2)}'

    def close(self, force:bool=False):
        '''
        Cleans up by deleting temporary PKL files, if applicable.

        This method is responsible for deleting any temporary JSB files created
        during the JsonReader's operation. It is typically called when the
        JsonReader instance is no longer needed, to ensure that no unnecessary
        files are left on the filesystem.
        '''
        if self._temp or force:
            shutil.rmtree(self._path)
            self._auditor.info(f'Deleted directory {self._path}')
            self._pkls = {}
            self._path = None

    def __str__(self) -> str:
        '''
        Returns a string representation of the JsonReader instance, listing all JSBs managed by it.

        This method provides an overview of the JSB files that have been generated by this instance,
        including their names, shapes, and memory usages. It is useful for quickly understanding
        the state and output of the JsonReader.

        Returns:
            str: A formatted string containing an overview of the JSON files managed by the JsonReader.
        '''
        out = '--------\nJSONS:'
        for k in self._pkls.keys():
            out += f'\n  {self.key_info(k, 4)}'
        out += '\n--------'
        self._auditor.info('Retrieved info for all keys')
        return out

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='json_ingest',
                                     description='Loads and consolidates JSON files',
                                     epilog='(C) 2024 Noah Duggan Erickson, License: GNU AGPL-3.0'
                                     )
    parser.add_argument('-i',  '--in_path',
                        required=True, dest='json_root', type=str,
                        metavar='/PATH/TO/JSON_ROOT/',
                        help='path to root of JSON data')
    parser.add_argument('-o', '--out_path',
                        dest='jsb_root', type=str, default='temp',
                        metavar='/PATH/TO/JSB_ROOT/',
                        help='path to root of JSB output data (default: temp)')
    parser.add_argument('-m', '--read_messages',
                        action='store_true', dest='m',
                        help='If present, don\'t skip the messages folder - may take significantly longer to run')
    parser.add_argument('-v', '--verbose',
                        action='count', dest='v', default=0,
                        help='Set stdout verbosity level (-v, -vv)')
    parser.add_argument('-d', '--delete', action='store_true', dest='force_delete',
                        help='Delete the output directory after completion (if not temp)')
    parser.add_argument('-x', help='Dev mode', action='store_true', dest='x')
    args = parser.parse_args()

    match args.v:
        case 0:
            level = logging.ERROR
        case 1:
            level = logging.INFO
        case 2:
            level = logging.DEBUG
        case _:
            level = logging.DEBUG

    ch = logging.StreamHandler()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=level, handlers=[ch])
    w = max((len(__version__)+3), 20)
    print('JSON -> PKL INGESTER'.center(w))
    print(f'V. {__version__}'.center(w), '\n')
    reader = JsonReader(jsonroot=args.json_root, pklroot=args.jsb_root,
                        read_messages=args.m, dev=args.x,
                        logger=logging.getLogger())
    print(reader)
    reader.close(args.force_delete)
