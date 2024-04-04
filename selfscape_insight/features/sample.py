"""A sample module for code format demonstration and boilerplate

This module provides a demonstration of a module for a simple
feature that tells the user how many ad-interests (bcts)
there are on the profile.

Functions:
    run(bcts): Runs the feature.

Example usage:
    >>> import sample_feature as sf
    >>> sf.run(JsonReader.get_csv("bcts"))
    There are X advertising-related topics in the profile!
    Go do more interesting things...

    $ python3 sample_feature.py -bcts /path/to/bcts.csv
    There are X advertising-related topics in the profile!
    Go do more interesting things...

Dependencies:
    Pandas package for data handling.

Note:
    This sub-module is part of the 'selfscape_insight' package in the 'feature' module.

Version:
    1.0

Author:
    Noah Duggan Erickson
"""

import pandas as pd
import argparse

def run(bcts):
    """Runs the feature.

    Tells how many ad-topics are on the user profile.
    (This description should be more verbose in a real feature!)

    Args:
        bcts (str): path to csv file specified by the parameter name
    
    Returns:
        str: This feature's contribution to the profile info dashboard datavis thing
    
    Warnings:
        run() is a *required* function for the module! It *must*
        be the only interaction that main.py has with the module.
    """
    df = pd.read_csv(bcts)
    return f"There are {len(df)} advertising-related topics in the profile!\nGo do more interesting things..."

# Below is more-or-less boilerplate code that can be copy/pasted
# and extended to allow the feature to run directly from the
# commandline as shown in Example 2
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='sample_feature', description='A sample program feature for the purposes of demo-ing code structure and boilerplate')
    parser.add_argument('-bcts', metavar='BCTS_CSV', help='path to bcts (ad topics) csv file', required=True)
    args = parser.parse_args()
    print(run(args.bcts))