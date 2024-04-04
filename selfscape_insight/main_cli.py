"""Runs an assortment of analyses on a Facebook profile data download

This is the main module that provides analysis of a facebook
profile. (will need to make this SIGNIFICANTLY longer...)

Functions:
    main(): Runs the program.

Example usage:
    $ python3 main_cli.py -in_path /path/to/jsons/
    (does stuff...)

    $ python3 main_cli.py -h
    (commandline arg help)

Dependencies:
    No external dependencies... yet...

Note:
    This is the main module.

Version:
    1.1.8

Author:
    Noah Duggan Erickson
"""

import argparse

from selfscape_insight.readers.json_ingest import JsonReader
from selfscape_insight.readers.csv_ingest  import CsvReader
from selfscape_insight.features import sample as sf
from selfscape_insight.features import ip_loc as ipl
from selfscape_insight.features import off_fb_act as ofa
from selfscape_insight.features import topics as tps
from selfscape_insight.features import feelings as fgs

# CHANGELOG:
#   1.1: (15 March 2024)
#     - Added option to ingest CSVs for development purposes
#   1.0:
#     - Initial Release

def main():
    parser = argparse.ArgumentParser(prog='selfscape_insight')
    parser.add_argument('-i', '--in_path', help='path to root of data', required=True)
    parser.add_argument('-c', help='If present, -i is a directory of CSVs (used for development)', action='store_true')
    parser.add_argument('-no_sf', help='Skip running the sample module', action='store_false')
    parser.add_argument('-no_ipl', help='Skip running the ip_loc module', action='store_false')
    parser.add_argument('-no_ofa', help='Skip running the off_fb_act module', action='store_false')
    parser.add_argument('-no_tps', help='Skip running the topics module', action='store_false')
    parser.add_argument('-no_fgs', help='Skip running the feelings module', action='store_false')
    args = parser.parse_args()

    if not args.c:
        fileHandler = JsonReader(args.in_path)
    else:
        fileHandler = CsvReader(args.in_path)
    featOuts = []
    
    # sample module
    #
    if args.no_sf:
        try:
            featOuts.append(sf.run(fileHandler.get_csv("bcts")))
        except ValueError:
            print("One of the files for the sample module does not exist! Skipping...")
    
    # ip_loc module
    #
    if args.no_ipl:
        try:
            featOuts.append(ipl.run(fileHandler.get_csv("account_activity_v2")))
        except ValueError:
            print("One of the files for the ip_loc module does not exist! Skipping...")
    
    # off_fb_act module
    #
    if args.no_ofa:
        try:
            featOuts.append(ofa.run(fileHandler.get_csv("off_facebook_activity_v2")))
        except ValueError:
            print("One of the files for the off_fb_act module does not exist! Skipping...")
    
    # topics module
    #
    if args.no_tps:
        try:
            featOuts.append(tps.run(fileHandler.get_csv("topics_v2"),
                                fileHandler.get_csv("inferred_topics_v2")))
        except ValueError:
            print("One of the files for the topics module does not exist! Skipping...")
    
    # feelings module
    #
    if args.no_fgs:
        try:
            featOuts.append(fgs.run(None))
        except ValueError:
            print("One of the files for the feelings module does not exist! Skipping...")
    
    fileHandler.close()
    for i in range(len(featOuts)):
        print(f"F[{i}]:")
        print(featOuts[i],"\n")

if __name__ == "__main__":
    main()
