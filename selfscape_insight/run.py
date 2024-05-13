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
    1.0

Author:
    Noah Duggan Erickson
"""
__version__ = '1.0'

from pathlib import Path

from features import sample as smp
from features import ip_loc as ipl
from features import off_fb_act as ofa
from features import topics as tps
from features import facebook_act as fba
from features import filesize_sunburst as fsb
from features import notifs as ntf

from core.log_aud import RootLogger

# CHANGELOG:
#   1.0: (08 May 2024)
#     - Added notifs feature
#     - Renamed feelings to on_fb_act
#     - Removed demo helper
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
#     - Assorted fixes to err handling and logging
#   0.4: (05 April 2024)
#     - Propogated readers/json_ingest.py logging abilities
#   0.3: (04 April 2024)
#     - Added flit building and packaging; subsequent
#       structural modifications
#   0.2: (15 March 2024)
#     - Added option to ingest CSVs for development purposes
#   0.1:
#     - Initial Release

def main(in_path:str, out_path:str, mods:dict, verbose:int=0, log:str=None):
    """Runs the program.

    Args:
        in_path (Path): Path to the directory containing the Facebook profile data
        out_path (Path): Path to the directory where output files will be saved
        mods (dict): Dictionary of modules to run
        verbose (int): Verbosity level for logging (0-3)
        log (Path): Path to the log file. If None, log to stdout.
    """
    if any(mods.values()):
        for key in mods:
            if mods[key] is None:
                mods[key] = False
    else:
        for key in mods:
            if mods[key] is None:
                mods[key] = True
    # print(f"Modules: {mods}\nVerbose: {verbose}")
    
    logger = RootLogger()
    logger.setup(verb=verbose, output=log)

    in_path = Path(in_path)
    out_path = Path(out_path)
    feat_outs = []
    
    # sample module
    #
    if mods['smp']:
        path = in_path / 'ads_information' / 'other_categories_used_to_reach_you.json'
        if path.exists():
            feat_outs.append(smp.run(path, out_path, logger.get_child('smp')))
        else:
            logger.err("The file for the sample module (%s) does not exist! Skipping..." % path.name)
            logger.debug("Expected path: %s" % path)
    else:
        logger.info("Sample module not run.")

    # notifications module
    #
    if mods['ntf']:
        path = in_path / 'logged_information' / 'notifications' / 'notifications.json'
        if path.exists():
            feat_outs.append(ntf.run(path, out_path, logger.get_child('ntf')))
        else:
            logger.err("The file for the Notifications module (%s) does not exist! Skipping..." % path.name)
            logger.debug("Expected path: %s" % path)

    # ip_loc module
    #
    if mods['ipl']:
        path = in_path / 'security_and_login_information' / 'account_activity.json'
        if path.exists():
            feat_outs.append(ipl.run(path, out_path, logger.get_child('ipl')))
        else:
            logger.err("The file for the IP Location module (%s) does not exist! Skipping..." % path.name)
            logger.debug("Expected path: %s" % path)
    else:
        logger.info("IP Location module not run.")

    # off_fb_act module
    #
    if mods['ofa']:
        path = in_path / 'apps_and_websites_off_of_facebook' / 'your_activity_off_meta_technologies.json'
        if path.exists():
            feat_outs.append(ofa.run(path, out_path, logger.get_child('ofa')))
        else:
            logger.err("The file for the Off-Facebook Activity module (%s) does not exist! Skipping..." % path.name)
            logger.debug("Expected path: %s" % path)
    else:
        logger.info("Off-Facebook Activity module not run.")

    # topics module
    #
    if mods['tps']:
        path = [in_path / 'logged_information' / 'your_topics' / 'your_topics.json',
                in_path / 'logged_information' / 'other_logged_information' / 'ads_interests.json']
        for p in path: # make tps.run() only take one path at a time
            if p.exists():
                feat_outs.append(tps.run(p, out_path, logger.get_child('tps')))
            else:
                logger.err("A file for the Topics module (%s) does not exist! Skipping..." % p.name)
                logger.debug("Expected path: %s" % p)
    else:
        logger.info("Topics module not run.")

    # on_fb_act module
    #
    if mods['fba']:
        path = in_path
        feat_outs.append(fba.run(path, out_path, logger.get_child('fba')))
    else:
        logger.info("On-Facebook Activity module not run.")
    
    # filesize_sankey module
    #
    if mods['fsb']:
        path = in_path
        feat_outs.append(fsb.run(path, out_path, logger.get_child('fsk')))
    else:
        logger.info("Filesize_sunburst module not run.")

    for i in range(len(feat_outs)):
        print(f"F[{i}]:")
        print(feat_outs[i],"\n")
