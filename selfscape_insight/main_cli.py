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
    0.5

Author:
    Noah Duggan Erickson
"""

import argparse
import logging
import sys

from readers.json_ingest import JsonReader
from features import sample as sf
from features import ip_loc as ipl
from features import off_fb_act as ofa
from features import topics as tps
from features import facebook_act as fba

# CHANGELOG:
#   0.5: (22 April 2024)
#     - Updated names of a few variables
#     - Removed CSV compatibility (see: json_ingest 3.0.0rc2)
#     - Added module output path argument
#   0.4.1: (15 April 2024)
#     - Assorted fixes to error handling and logging
#   0.4: (05 April 2024)
#     - Propogated readers/json_ingest.py logging abilities
#   0.3: (04 April 2024)
#     - Added flit building and packaging; subsequent
#       structural modifications
#   0.2: (15 March 2024)
#     - Added option to ingest CSVs for development purposes
#   0.1:
#     - Initial Release

def main():
    parser = argparse.ArgumentParser(prog='selfscape_insight',
                                     usage='scape_cli -i PATH/TO/DATA [options]',
                                     description='Runs an assortment of analyses on a Facebook profile data download',
                                     epilog='(C) 2024 The Authors, License: GNU AGPL-3.0'
                                     )
    fio = parser.add_argument_group('File I/O')
    fio.add_argument('-i', '--in_path', metavar='PATH/TO/DATA', help='path to root of data', required=True)
    fio.add_argument('-o', '--out_path', metavar='PATH/TO/OUTPUT', help='path to output directory', required=True)
    mod_group = parser.add_argument_group('Modules', 'Select which modules to include/exclude.')
    mod_group.add_argument('--smp', help='sample module', action=argparse.BooleanOptionalAction)
    mod_group.add_argument('--ipl', help='ip_loc module', action=argparse.BooleanOptionalAction)
    mod_group.add_argument('--ofa', help='off_fb_act module', action=argparse.BooleanOptionalAction)
    mod_group.add_argument('--tps', help='topics module', action=argparse.BooleanOptionalAction)
    mod_group.add_argument('--fba', help='facebook_act module', action=argparse.BooleanOptionalAction)
    adv = parser.add_argument_group('Advanced Options')
    adv.add_argument('-l', '--log', help='Log file path, else stdout', metavar='PATH/TO/LOG', default=sys.stdout)
    adv.add_argument('-v', '--verbose', action='count', dest='v', default=0, help='Logs verbosity (-v, -vv)')
    args = parser.parse_args()

    mods = {'smp': args.smp, 'ipl': args.ipl, 'ofa': args.ofa, 'tps': args.tps, 'fba': args.fba}
    if any(mods.values()):
        for key in mods:
            if mods[key] is None:
                mods[key] = False
    else:
        for key in mods:
            if mods[key] is None:
                mods[key] = True
    print(f"Modules: {mods}\nVerbose: {args.v}")
    match args.v:
        case 0:
            level = logging.ERROR
        case 1:
            level = logging.INFO
        case 2:
            level = logging.DEBUG
        case _:
            level = logging.DEBUG

    ch = logging.StreamHandler(args.log)
    LOGFMT = "%(asctime)s : [%(name)s - %(levelname)s] : %(message)s"
    # logging.basicConfig(format=LOGFMT, level=level, handlers=[ch])
    logger = logging.getLogger('main')
    logger.setLevel(level)
    logger.addHandler(ch)
    auditor = logging.getLogger('auditor')
    auditor.setLevel(logging.INFO)
    auditor.addHandler(ch)
    ch.setFormatter(logging.Formatter(LOGFMT))
    logger.info("Logger initialized.")

    fileHandler = JsonReader(args.in_path, logger=logger.getChild("pkl"), auditor=auditor.getChild("pkl"))
    featOuts = []
    
    # sample module
    #
    if mods['smp']:
        try:
            featOuts.append(sf.run(fileHandler.get_pkl("bcts")))
        except KeyError:
            logger.error("One of the files for the sample module does not exist! Skipping...")
    else:
        logger.info("Sample module not run.")
    
    # ip_loc module
    #
    if mods['ipl']:
        try:
            featOuts.append(ipl.run(fileHandler.get_pkl("account_activity_v2")))
        except KeyError:
            logger.error("One of the files for the ip_loc module does not exist! Skipping...")
    else:
        logger.info("IP Location module not run.")
    
    # off_fb_act module
    #
    if mods['ofa']:
        try:
            featOuts.append(ofa.run(fileHandler.get_pkl("off_facebook_activity_v2")))
        except KeyError:
            logger.error("One of the files for the off_fb_act module does not exist! Skipping...")
    else:
        logger.info("Off-Facebook Activity module not run.")
    
    # topics module
    #
    if mods['tps']:
    #     try:
    #         featOuts.append(tps.run(args.in_path + "\\logged_information\\your_topics\\your_topics.json"))
    #     except KeyError:
    #         logger.error("One of the files for the topics module does not exist! Skipping...")
    #     try:
    #         featOuts.append(tps.run(args.in_path + "\\logged_information\\other_logged_information\\ads_interests.json"))
    #     except KeyError:
    #         logger.error("One of the files for the topics module does not exist! Skipping...")
    # else:
        logger.info("Topics module not run.")
    
    # facebook_act module
    #
    if mods['fba']:
        try:
            featOuts.append(fba.run(args.in_path))
        except KeyError:
            logger.error("One of the files for the feelings module does not exist! Skipping...")
    else:
        logger.info("Feelings module not run.")
    
    fileHandler.close()
    for i in range(len(featOuts)):
        print(f"F[{i}]:")
        print(featOuts[i],"\n")

if __name__ == "__main__":
    main()
