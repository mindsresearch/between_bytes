"""A sample module for code format demonstration and boilerplate

This module provides a demonstration of a module for a simple
feature that tells the user how many ad-interests (bcts)
there are on the profile.

Functions:
    run(bcts): Runs the feature.

Examples:
    >>> from selfscape_insight.features import sample as smp
    >>> smp.run(Path('path/to/data'), Path('path/to/outs'), logger)
    There are X advertising-related topics in the profile!
    Go do more interesting things...

    $ python3 sample_feature.py -i /path/to/file.json
    There are X advertising-related topics in the profile!
    Go do more interesting things...

Dependencies:
    Pandas for data processing
    Requests for URL handling

Version:
    2.0

Author:
    Noah Duggan Erickson
"""

import argparse
from pathlib import Path

import pandas as pd
import requests

from selfscape_insight.core.log_aud import SsiLogger, RootLogger # pylint disable=wrong-import-position


def run(in_path: Path, out_path: Path, logger: SsiLogger) -> str:
    """
    Args:
        in_path: The path to the input file.
        out_path: The path to the output directory.
        logger: The logger object for logging messages.

    Returns:
        A string message containing the number of advertising-related topics in the profile and the path to the created image.

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
    parser = argparse.ArgumentParser(prog='sample_feature', description='A sample program feature for the purposes of demo-ing code structure and boilerplate')
    parser.add_argument('-i', '--in_file', metavar='BCTS_JSON', help='path to json file where \'bcts\' is tlk', required=True)
    parser.add_argument('-o', '--out_path', metavar='OUTPUT_PATH', help='where to send output image', required=False, default='.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity', required=False)
    args = parser.parse_args()

    main_logger = RootLogger()
    main_logger.setup(verb=args.verbose)

    print(run(args.in_file, args.out_path, main_logger))