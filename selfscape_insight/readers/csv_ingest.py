""" Used for development only.
"""

__version__ = '1.0'

import os
import argparse

import pandas as pd

class CsvReader:
    def __init__(self, rootpath:str):
        self.csvs = {}
        for file in os.listdir(rootpath):
            self.csvs[file[:-4]] = os.path.join(rootpath, file)
    
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
        Returns a list of the names of all CSV files managed by the CsvReader.

        This method allows for easy access to the names of all CSV files that are
        being monitored, which can be useful for iterating over the files or
        accessing specific ones.

        Returns:
            list: A list of strings, each representing the name of a monitored CSV file.
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
    
    def __str__(self) -> str:
        """
        Returns a string representation of the CsvReader instance, listing all CSVs managed by it.

        This method provides an overview of the CSV files that are monitored by this instance,
        including their names, shapes, and memory usages. It is useful for quickly understanding
        the state and output of the CsvReader.

        Returns:
            str: A formatted string containing an overview of the CSV files managed by the CsvReader.
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
    parser = argparse.ArgumentParser(prog='python3 dev_csv_stuff.py')
    parser.add_argument('-i',  '--in_path',
                        required=True, dest='csv_root', type=str,
                        metavar='/PATH/TO/CSV_ROOT/',
                        help='path to root of CSV data')
    args = parser.parse_args('-i /home/duggann/nde-fb-csvs'.split())
    reader = CsvReader(args.csv_root)
    print(reader)