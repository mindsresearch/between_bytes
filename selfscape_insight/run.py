"""Runs an assortment of analyses on a Facebook profile data download

This is the main module that provides analysis of a facebook
profile. (will need to make this SIGNIFICANTLY longer...)

Functions:
    main(): Runs the program.

Dependencies:
    No external dependencies

Note:
    To run this file from the command line, please use exec_cli.py

TODO:
    - "refactor" versioning following exec_cli.py split

Version:
    0.2

Author:
    Noah Duggan Erickson
"""
__version__ = '0.2'

import logging
import sys
from pathlib import Path

from selfscape_insight.features import sample as smp
from selfscape_insight.features import ip_loc as ipl
from selfscape_insight.features import off_fb_act as ofa
from selfscape_insight.features import topics as tps
from selfscape_insight.features import feelings as fba
from selfscape_insight.features import filesize_sankey as fsk

from selfscape_insight.core.various_helpers import pointless_function

# CHANGELOG:
#   0.6: (25 April 2024)
#     - Added filesize_sankey feature
#     - Refactor for wizard launcher
#   0.5.1: (25 April 2024)
#     - Abandon & destroy json_ingest
#     - Use pathlib for path handling
#     - Propogate logging to feature modules
#     - Add core helpers import (temporary as demo)
#     - Propogate common output path to features
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

def main(in_path:str, out_path:str, mods:dict, verbose:int=0, log:str=sys.stdout):
    print(pointless_function()) # remove in production
    if any(mods.values()):
        for key in mods:
            if mods[key] is None:
                mods[key] = False
    else:
        for key in mods:
            if mods[key] is None:
                mods[key] = True
    print(f"Modules: {mods}\nVerbose: {verbose}")
    match verbose:
        case 0:
            level = logging.WARNING
        case 1:
            level = logging.INFO
        case 2:
            level = logging.DEBUG
        case _:
            level = logging.DEBUG

    ch = logging.StreamHandler(log)
    logfmt = "%(asctime)s : [%(name)s - %(levelname)s] : %(message)s"
    # logging.basicConfig(format=LOGFMT, level=level, handlers=[ch])
    logger = logging.getLogger("main")
    logger.setLevel(level)
    logger.addHandler(ch)
    auditor = logging.getLogger('auditor')
    auditor.setLevel(min(level, logging.INFO))
    auditor.addHandler(ch)
    ch.setFormatter(logging.Formatter(logfmt))
    logger.info("Logger initialized.")

    feat_outs = []
    out_path = Path(out_path)
    
    # sample module
    #
    if mods['smp']:
        path = Path(in_path) / 'ads_information' / 'other_categories_used_to_reach_you.json'
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
        path = Path(in_path) / 'security_and_login_information' / 'account_activity.json'
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
        path = Path(in_path) / 'apps_and_websites_off_of_facebook' / 'your_activity_off_meta_technologies.json'
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
        path = [Path(in_path) / 'logged_information' / 'your_topics' / 'your_topics.json',
                Path(in_path) / 'logged_information' / 'other_logged_information' / 'ads_interests.json']
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
        path = Path(in_path)
        feat_outs.append(fba.run(path, out_path, logger.getChild('fba'), auditor.getChild('fba')))
    else:
        logger.info("Feelings module not run.")
    
    # filesize_sankey module
    #
    if mods['fsk']:
        path = Path(in_path)
        feat_outs.append(fsk.run(path, out_path, logger.getChild('fsk'), auditor.getChild('fsk')))
    else:
        logger.info("Filesize_sankey module not run.")

    for i in range(len(feat_outs)):
        print(f"F[{i}]:")
        print(feat_outs[i],"\n")