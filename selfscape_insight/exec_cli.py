"""Runs an assortment of analyses on a Facebook profile data download

This is the main module that provides analysis of a facebook
profile. (will need to make this SIGNIFICANTLY longer...)

Functions:
    None

Example usage:
    $ python3 exec_cli.py -i /path/to/jsons/
    (does stuff...)

    $ python3 exec_cli.py -h
    (commandline arg help)

Dependencies:
    No external dependencies

Note:
    This module has no independent functionality.

Version:
    0.1

Author:
    Noah Duggan Erickson
"""
__version__ = '0.1'


import argparse
from pathlib import Path

from selfscape_insight.run import main


def exec():
    parser = argparse.ArgumentParser(prog="selfscape_insight",
                                     usage="scape_cli -i PATH/TO/DATA [options]",
                                     description="Runs an assortment of analyses on a Facebook profile data download",
                                     epilog="(C) 2024 The Authors, License: GNU AGPL-3.0"
                                     )
    fio = parser.add_argument_group("File I/O")
    fio.add_argument("-i", "--in_path", metavar="PATH/TO/DATA",
                     help="path to root of data", required=True)
    fio.add_argument('-o', '--out_path', metavar='PATH/TO/OUTPUT',
                     help='path to output directory', required=False,
                     default=Path.cwd())
    mod_group = parser.add_argument_group("Modules", "Select which modules to include/exclude.")
    mod_group.add_argument("--smp", help="sample module",
                           action=argparse.BooleanOptionalAction)
    mod_group.add_argument("--ipl", help="ip_loc module",
                           action=argparse.BooleanOptionalAction)
    mod_group.add_argument("--ofa", help="off_fb_act module",
                           action=argparse.BooleanOptionalAction)
    mod_group.add_argument("--tps", help="topics module",
                           action=argparse.BooleanOptionalAction)
    mod_group.add_argument("--fba", help="on-fb-act module",
                           action=argparse.BooleanOptionalAction)
    mod_group.add_argument("--fsb", help="filesize_sunburst module",
                            action=argparse.BooleanOptionalAction)
    mod_group.add_argument("--ntf", help="notifications module",
                            action=argparse.BooleanOptionalAction)
    adv = parser.add_argument_group("Advanced", "Advanced options.")
    adv.add_argument("-l", "--log", help="Log file path, else stdout",
                        metavar="PATH/TO/LOG", default=None)
    adv.add_argument("-v", "--verbose", action="count", dest="v",
                        default=0, help="Logs verbosity (-v, -vv)")
    adv.add_argument("--version", action="version",
                     version=f"%(prog)s {__version__}")
    args = parser.parse_args()

    run_mods = {"smp": args.smp,
                "ipl": args.ipl,
                "ofa": args.ofa,
                "tps": args.tps,
                "fba": args.fba,
                "fsb": args.fsb,
                "ntf": args.ntf}

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)
    out_path.mkdir(parents=True, exist_ok=True)
    main(in_path=in_path, out_path=out_path, mods=run_mods, verbose=args.v, log=args.log)


if __name__ == "__main__":
    print("Starting SelfScape Insight using CLI v.%s" % __version__)
    exec()
