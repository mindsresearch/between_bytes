"""A sample module for code format demonstration and boilerplate

This module provides a demonstration of a module for a simple
feature that tells the user how many ad-interests (bcts)
there are on the profile.

Functions:
    run(bcts): Runs the feature.

Example usage:
    >>> import sample_feature as sf
    >>> sf.run(PathLike, logger, auditor)
    There are X advertising-related topics in the profile!
    Go do more interesting things...

    $ python3 sample_feature.py -i /path/to/file.json
    There are X advertising-related topics in the profile!
    Go do more interesting things...

Dependencies:
    No external dependencies.

Note:
    This sub-module is part of the 'selfscape_insight' package in the 'feature' module.

Version:
    2.0

Author:
    Noah Duggan Erickson
"""

import argparse
from pathlib import Path
import sys

import pandas as pd
import requests

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from selfscape_insight.core.various_helpers import pointless_function # pylint disable=wrong-import-position
from selfscape_insight.core.log_aud import SsiLogger, RootLogger # pylint disable=wrong-import-position

def run(in_path:Path, out_path:Path, logger:SsiLogger) -> str:
    """Runs the feature.

    Tells how many ad-topics are on the user profile.
    (This description should be more verbose in a real feature!)

    Args:
        bcts (str): path to `other_categories_used_to_reach_you.json` file
    
    Returns:
        str: This feature's contribution to the profile info dashboard datavis thing
    
    Warnings:
        run() is a *required* function for the module! It *must*
        be the only interaction that main.py has with the module.
    """
    logger.info("Starting sample feature...")
    in_path = Path(in_path)
    out_path = Path(out_path)

    # categories stuff
    #
    # Purpose of this section:
    #   - Demonstration of basic operation
    #   - Demonstration of logging
    #   - Demonstration of basic auditor ethos
    #
    logger.use_file(in_path)
    df = pd.read_json(in_path, orient='records', typ='frame')
    logger.debug("Read json file into %i x %i dataframe" % df.shape)

    # image stuff
    #
    # Purpose of this section:
    #   - Demonstration of auditor ethos for things that require an internet connection
    #   - Demonstration of auditor ethos for file I/O

    # raise NotImplementedError(out_path.absolute())
    # Get a random image
    image_url = "https://source.unsplash.com/random"
    logger.use_inet(image_url)
    response = requests.get(image_url, timeout=15)
    logger.debug('GET request returned with status code %i' % response.status_code)

    # Save the image to 'random.jpg'
    out_file = out_path / 'random.jpg'
    with open(out_file, 'wb') as file:
        logger.wrote_file(out_file)
        b = file.write(response.content)
        logger.debug("Wrote %i bytes to %s" % (b, out_file.absolute()))

    # Confirm that the image has been saved
    logger.info("Image saved as %s" % out_file)
    # raise NotImplementedError("pause point")
    return f"There are {len(df['bcts'])} advertising-related topics in the profile!\nAn image was created at {out_file.absolute()}\nGo do more interesting things..."

# Below is more-or-less boilerplate code that can be copy/pasted
# and extended to allow the feature to run directly from the
# commandline as shown in Example 2
#
if __name__ == "__main__":
    print(pointless_function()) # remove in production
    parser = argparse.ArgumentParser(prog='sample_feature', description='A sample program feature for the purposes of demo-ing code structure and boilerplate')
    parser.add_argument('-i', '--in_file', metavar='BCTS_JSON', help='path to json file where \'bcts\' is tlk', required=True)
    parser.add_argument('-o', '--out_path', metavar='OUTPUT_PATH', help='where to send output(s)', required=False, default='.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity', required=False)
    args = parser.parse_args()

    logger = RootLogger()
    logger.setup(verb=args.verbose)

    print(run(args.in_file, args.out_path, logger))