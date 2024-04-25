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
from pathlib import Path

from features import sample as smp
from features import ip_loc as ipl
from features import off_fb_act as ofa
from features import topics as tps
from features import feelings as fba

from core.various_helpers import pointless_function

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
    mod_group.add_argument('--fgs', help='feelings module', action=argparse.BooleanOptionalAction)
    adv = parser.add_argument_group('Advanced Options')
    adv.add_argument('-l', '--log', help='Log file path, else stdout', metavar='PATH/TO/LOG', default=sys.stdout)
    adv.add_argument('-v', '--verbose', action='count', dest='v', default=0, help='Logs verbosity (-v, -vv)')
    args = parser.parse_args()

    mods = {'smp': args.smp, 'ipl': args.ipl, 'ofa': args.ofa, 'tps': args.tps, 'fgs': args.fgs}
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

    feat_outs = []
    featOuts = []
    
    # sample module
    #
    if mods['smp']:
        path = Path(args.in_path) / 'ads_information' / 'other_categories_used_to_reach_you.json'
        if path.exists():
            feat_outs.append(smp.run(path, out_path, logger.getChild('smp'), auditor.getChild('smp')))
        else:
            logger.error("The file for the sample module (%s) does not exist! Skipping..." % path.name)
            logger.debug("Expected path: %s" % path)
    else:
        logger.info("Sample module not run.")
    
    # ip_loc module
    #
    if mods['ipl']:
        path = Path(args.in_path) / 'security_and_login_information' / 'account_activity.json'
        if path.exists():
            feat_outs.append(ipl.run(path, out_path, logger.getChild('ipl'), auditor.getChild('ipl')))
        else:
            logger.error("The file for the IP Location module (%s) does not exist! Skipping..." % path.name)
            logger.debug("Expected path: %s" % path)
    else:
        logger.info("IP Location module not run.")
    
    # off_fb_act module
    #
    if mods['ofa']:
        path = Path(args.in_path) / 'apps_and_websites_off_of_facebook' / 'your_activity_off_meta_technologies.json'
        if path.exists():
            feat_outs.append(ofa.run(path, out_path, logger.getChild('ofa'), auditor.getChild('ofa')))
        else:
            logger.error("The file for the Off-Facebook Activity module (%s) does not exist! Skipping..." % path.name)
            logger.debug("Expected path: %s" % path)
    else:
        logger.info("Off-Facebook Activity module not run.")
    
    # topics module
    #
    if mods['tps']:
        path = [Path(args.in_path) / 'logged_information' / 'your_topics' / 'your_topics.json',
                Path(args.in_path) / 'logged_information' / 'other_logged_information' / 'ads_interests.json']
        for p in path: # make tps.run() only take one path at a time
            if p.exists():
                feat_outs.append(tps.run(p, out_path, logger.getChild('tps'), auditor.getChild('tps')))
            else:
                logger.error("A file for the Topics module (%s) does not exist! Skipping..." % p.name)
                logger.debug("Expected path: %s" % p)
    else:
        logger.info("Topics module not run.")
    
    # feelings module
    #
    if mods['fba']:
        path = Path(args.in_path)
        feat_outs.append(fba.run(path, out_path, logger.getChild('fba'), auditor.getChild('fba')))
    else:
        logger.info("Feelings module not run.")
    
    for i in range(len(feat_outs)):
        print(f"F[{i}]:")
        print(feat_outs[i],"\n")

if __name__ == "__main__":
    print(pointless_function()) # for sake of demo only. Remove in production.
    main()
