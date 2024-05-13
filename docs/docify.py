''' Generates a starting point for insight documentation and publication.

This script does a few things:
1. Duplicates select visuals (EXP_VIS) and copies them to the _static directory of the documentation.
2. Builds an rst file with a rudimentary structure for documenting insights.
2a. The intro text is read from a file and inserted into the document.
2b. A grid of cards is built to navigate to the visuals.
2c. Sections are built for each insight type, with placeholder text to be replaced.

There are a few steps involved to run this script:
1. Install dependencies: rstcloth, sphinx, and extensions thereof
1a. pip install rstcloth
1b. pip install sphinx
1c. pip install pydata-sphinx-theme
1c. pip install sphinx_design

2. Run and build
2a. Run the script with the required arguments
Example for Noah:
    .../docs$ python3 docify.py -o ~/Documents/noah_ssi_outs -d about/our_insights/devs -g duggann4 -n Noah
2b. Build the docs
    Linux & MacOS:
    .../docs$ make html
    Windows:
    PS .../docs> .\make html

3. View the docs
3a. Open the index.html file in the _build/html directory in a web browser. (.../docs/_build/html/index.html)
NOTE: The _build directory is not included in the repository (via .gitignore).
3b. Explore the docs and poke around!

TODO: Further develop ability to get content from text files (similar to the current dummy intro)

NOTE: Functionality that you want to add to your docs beyond this script (e.g. buttons on the cards)
      need to be added manually to the rst file. This script is meant to provide a starting point
      for documentation, not a complete solution.
'''

import argparse
from pathlib import Path
import shutil
import hashlib

from rstcloth import RstCloth

EXP_VIS = ['ads_interests.jpg',
           'notifications/2024_notifications.html',
           'ip_loc/interactive_occurance.html',
           'facebook_act/Facebook_Use_by_Year.png',
           'filesize_sunburst/sunburst.html',
           'off_fb_activity/top_cos.html']

def copy_visuals(vis_root, gh_name):
    vis_root = Path(vis_root)
    vis_dir = Path('_static') / gh_name
    vis_dir.mkdir(parents=True, exist_ok=True)
    for vis in EXP_VIS:
        vis_path = vis_root / vis
        if vis_path.exists():
            shutil.copy(vis_path, vis_dir)
        else:
            raise FileNotFoundError(f"Visual not found: {vis}")

def multiline_content(rc, text:str) -> None:
    for line in text.split('\n'):
        if len(line) > 0:
            rc.content(line)
            rc.newline()

def build_section(rc, name, content):
    rc.newline()
    rc.h3(name)
    rc.content(content)

def build_nav_card(rc, name, symbol, desc, ref):
    rc.directive('grid-item-card', arg=name,
                 fields=[('class-header', 'header-symbol-small'), ('link', ref), ('text-align', 'center')],
                 indent=3)
    rc.newline()
    rc.h5(symbol, indent=6)
    rc.newline()
    rc.content(desc, indent=6)

def build_nav_cards(rc, ghh:str):
    # rc.h2('My Insights')
    rc.directive('grid', arg='3', fields=[('gutter', '3')])
    rc.newline()
    build_nav_card(rc, 'Filesize Sunburst', 'folder_data',
                   'See how much space different types of data take up.',
                   f'../../../_static/{ghh}/sunburst.html')
    rc.newline()
    build_nav_card(rc, 'Topics', 'campaign',
                   'See what Facebook thinks I am interested in.',
                   f'../../../_static/{ghh}/ads_interests.jpg')
    rc.newline()
    build_nav_card(rc, 'Notifications', 'notifications',
                   'See how frequently Facebook sends notifications',
                   f'../../../_static/{ghh}/2024_notifications.html')
    rc.newline()
    build_nav_card(rc, 'Off-Facebook Activity', 'share',
                   'See what Facebook knows about my activity off of Facebook.',
                   f'../../../_static/{ghh}/top_cos.html')
    rc.newline()
    build_nav_card(rc, 'IP Location', 'person_pin',
                   'See where Facebook thinks I am.',
                   f'../../../_static/{ghh}/interactive_occurance.html')
    rc.newline()
    build_nav_card(rc, 'On-Facebook Activity', 'forum',
                   'See how I use Facebook.',
                   f'../../../_static/{ghh}/Facebook_Use_by_Year.png')

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--out_path', metavar='PATH/TO/VISUALS_ROOT',
                    help='path to root of directory containing program outputs', required=True
                    )
parser.add_argument('-d', '--doc_path', metavar='PATH/TO/OUT.rst',
                    help='path to file to write docs to', required=False,
                    default=Path.cwd())
parser.add_argument('-g', '--gh_name', metavar='GITHUB_USERNAME', required=True, type=str,
                    help='GitHub username of the user whose insights are being documented')
parser.add_argument('-n', '--rf_name', metavar='FIRST_NAME', required=True, type=str,
                    help='First name of the user whose insights are being documented')
args = parser.parse_args()

gh_name = args.gh_name
ghh = hashlib.md5(gh_name.encode()).hexdigest()
rf_name = args.rf_name
vis_root = Path(args.out_path)
doc_path = Path(args.doc_path) / ('%s.rst' % gh_name)

with open(doc_path, 'w') as out_file:
    rc = RstCloth(out_file)
    rc.title(f"{rf_name}'s Insights")
    rc.newline()
    with open('dummy_intro.txt', 'r') as intro_file:
        multiline_content(rc, intro_file.read())
    rc.h2('My Visuals')
    copy_visuals(vis_root, ghh)
    build_nav_cards(rc, ghh)
    rc.newline()
    rc.h2('My Insights')
    rc.newline()
    build_section(rc, 'Notifications', 'Sample text for insights gained from the notifications visual.')
    rc.newline()
    build_section(rc, 'IP Location', 'Sample text for insights gained from the IP location visual.')
    rc.newline()
    build_section(rc, 'Off-Facebook Activity', 'Sample text for insights gained from the off-Facebook activity visual.')
    rc.newline()
    build_section(rc, 'Filesize Sunburst', 'Sample text for insights gained from the filesize sunburst visual.')
    rc.newline()
    build_section(rc, 'On-Facebook Activity', 'Sample text for insights gained from the on-Facebook activity visual.')
    rc.newline()
    build_section(rc, 'Topics', 'Sample text for insights gained from the topics visual.')