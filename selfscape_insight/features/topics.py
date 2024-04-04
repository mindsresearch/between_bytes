"""A short description of what your code does.

A longer description of what your code does,
including what csvs it takes in, and what it
contributes to the final output

Functions:
    run(topics_v2, inferred_topics_v2): Runs the feature.

Example usage:
    >>> from features import topics as tps
    >>> tps.run(JsonReader.get_csv("topics_v2"), JsonReader.get_csv("inferred_topics_v2"))
    filepath to HTML page containing results of analysis

    $ python3 topics.py -topics_v2 /path/to/topics_v2.csv
                        -inferred_topics_v2 /path/to/inferred_topics_v2.csv
    filepath to HTML page containing results of analysis

Dependencies:
    pandas for data handling
    requests and BeautifulSoup4 for webscraping image acquisition
    pillow (PIL) for image handling
    [ADD DESCRIPTIONS FOR FURTHER THIRD-PARTY IMPORTS HERE]


Note:
    This sub-module is part of the 'selfscape_insight' package in the 'features' module.

Version:
    1.0.0

Author:
    Carter Jacobs
"""

import argparse
import os
import random
import tempfile
# Add your other built-in imports here

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
# Add your other third-party/external imports here
# Please update requirements.txt as needed!


def specialCharacter (df):
    temp_df = df.copy()
    for x in range(0, len(df)):
        temp_df.iloc[x] = df.iloc[x].encode("latin-1").decode("utf-8")
    return temp_df

def create_collage(image_folder, output_path, collage_size=(4096, 2160)):
    # Get all image files from the folder
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    
    # Shuffle the order of the image files
    random.shuffle(image_files)
    
    # Create a new blank image for the collage
    collage = Image.new('RGB', collage_size)
    draw = ImageDraw.Draw(collage)
    
    # Calculate the width and height for each image tile
    total_images = len(image_files)
    width = int(total_images ** 0.5)  # Calculate number of images that can fit horizontally
    height = (total_images + width - 1) // width  # Calculate number of images that can fit vertically

    tile_width = collage_size[0] // width
    tile_height = collage_size[1] // height

    # Paste each image onto the collage
    for i, image_file in enumerate(image_files):
        try:
            font_size = int(tile_height * 0.1)
            image_path = os.path.join(image_folder, image_file)
            img = Image.open(image_path)
            img = img.resize((tile_width, tile_height - int(font_size * 1.2)))  # Resize image to fit the tile size
            collage.paste(img, ((i % width) * tile_width, (i // width) * tile_height))  # Paste image onto the collage
            # Draw image name under each picture
            font = ImageFont.truetype("arial.ttf", font_size)
            topic = image_file.replace(".jpg","")
            # topic = topic[:20]
            draw.text(((i % width) * tile_width, (i // width) * tile_height + tile_height - int(font_size * 1.2)), topic, font=font, fill=(255, 255, 255))
        except (Image.UnidentifiedImageError):
            print(f"Skipping invalid image file: {image_file}")

    # Save the collage
    collage.save(output_path)


def run(topics_v2, inferred_topics_v2):
    print("Running the topics feature module")

    topics = pd.read_csv(topics_v2)
    topics = topics.drop(["Unnamed: 0"], axis=1)
    topics.columns = ["Ads_interests"]
    topics["Ads_interests"] = specialCharacter(topics["Ads_interests"])

    output_path_topics = "topics_collage.jpg"

    with tempfile.TemporaryDirectory() as temp_dir_topics:
        print(f"Created temporary directory: {temp_dir_topics}")
        
        # Download images to the temporary directory
        for index, row in tqdm(topics.iterrows(), desc="Topics: ", total=len(topics)):
            lead = row["Ads_interests"]
            params = {
                "q": lead,
                "tbm": "isch",
            }
            html = requests.get("https://www.google.com/search", params=params, timeout=30)
            soup = BeautifulSoup(html.content, features="lxml")
            image = soup.find_all("img")[1]["src"]
            data = requests.get(image).content
            with open(os.path.join(temp_dir_topics, f"{lead}.jpg"), "wb") as f:
                f.write(data)

        # Create collage using images in the temporary directory
        create_collage(temp_dir_topics, output_path_topics)


    inferred_topics = pd.read_csv(inferred_topics_v2)
    inferred_topics = inferred_topics.drop(["Unnamed: 0"], axis=1)
    inferred_topics.columns = ["Topics"]
    inferred_topics["Topics"] = specialCharacter(inferred_topics["Topics"])

    output_path_inferred = "inferred_topics_collage.jpg"
    with tempfile.TemporaryDirectory() as temp_dir_inferred:
        print(f"Created temporary directory: {temp_dir_inferred}")
        
        # Download images to the temporary directory
        for index, row in tqdm(inferred_topics.iterrows(), desc="Inferred Topics: ", total=len(inferred_topics)):
            lead = row["Topics"]
            params = {
                "q": lead,
                "tbm": "isch",
            }
            html = requests.get("https://www.google.com/search", params=params, timeout=30)
            soup = BeautifulSoup(html.content, features="lxml")
            image = soup.find_all("img")[1]["src"]
            data = requests.get(image).content
            with open(os.path.join(temp_dir_inferred, f"{lead}.jpg"), "wb") as f:
                f.write(data)

        # Create collage using images in the temporary directory
        create_collage(temp_dir_inferred, output_path_inferred)

    return "Your collages have been created: " + str(output_path_topics) + " and " + str(output_path_inferred)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='topics',
                                     description='A short description of what your code does')
    parser.add_argument('-topics_v2', metavar='TOPICS_V2_CSV',
                        help='path to topics_v2 csv file', required=True)
    parser.add_argument('-inferred_topics_v2', metavar='INFERRED_TOPICS_V2_CSV',
                        help='path to inferred_topics_v2 csv file', required=True)
    args = parser.parse_args()
    print(run(args.topics_v2, args.inferred_topics_v2))
