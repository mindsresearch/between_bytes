"""This script analyzes IP locations and their activity over time.

The script takes in account activity data (in CSV format) containing IP addresses and timestamps. It processes this data to identify the density of activity, duration, and location associated with each IP address. The final output is an HTML page containing visualizations of IP location occurrences and their activity over time.

Functions:
    - convert_to_gps(ip_address): Converts IP addresses to GPS coordinates using MaxMind GeoLite2 database.
    - convert_time(timestamp): Converts Unix timestamps to human-readable datetime objects.
    - time_def(time1, time2): Calculates the time difference between two timestamps.
    - density_report(time1, time2): Calculates the density of activity based on timestamps.
    - create_df(df): Processes the input DataFrame to create a new DataFrame with relevant information.
    - generate_graph(df): Generates bar graphs showing the occurrences of IPs over time.
    - on_map_click(event): Handles click events on the generated map.
    - create_html(df): Creates an HTML map with markers for IP locations and popups showing activity graphs.
    - run(df): Main function to run the IP location analysis feature.

Example usage:
    - From Python:
        >>> from features import ip_loc as ipl
        >>> ipl.run(JsonReader.get_csv("account_activity_v2"))
        filepath to HTML page containing results of analysis
    - From command line:
        $ python3 ip_loc.py -account_activity_v2 /path/to/account_activity_v2.csv
        filepath to HTML page containing results of analysis

Dependencies:
    - pandas: Data handling.
    - geopandas: Geospatial data handling.
    - matplotlib.pyplot: Basic data visualization.
    - folium: Advanced data visualization on maps.
    - maxminddb: IP to latitude/longitude conversion.

Note:
    This sub-module is part of the 'between_bytes' package in the 'features' module.

Version:
    1.2

Author:
    Trevor Le
"""

import argparse
import os
from datetime import datetime
from io import BytesIO
import base64
import json
from pathlib import Path
import sys
# Add your other built-in imports here

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import maxminddb
import folium
import requests
import time
import multiprocessing
from tqdm import tqdm

from between_bytes.core.log_aud import BtbLogger, RootLogger


def process_ip(ip, df):
    filtered_df = df[df['ip_address'] == ip].copy()
    return generate_graph(filtered_df)

class RateLimiter:
    def __init__(self, frequency):
        self.frequency = frequency
        self.last_time = None
    def get(self, url:str) -> requests.models.Response:
        if self.last_time is not None:
            time.sleep(self.frequency - (time.time() - self.last_time))
        response = requests.get(url)
        self.last_time = time.time()
        return response

rate_limiter = RateLimiter(frequency=1)

def convert_to_gps(ip_address, logger):
    response = rate_limiter.get(f'https://ipinfo.io/{ip_address}/json')
    logger.use_inet(response.url)
    data = response.json()  
    logger.debug(f'Fetching GPS data for IP: {ip_address}')

    loc = data.get('loc')
    if loc:
        latitude, longitude = loc.split(',')
        logger.debug(f'Location for IP {ip_address}: ({latitude}, {longitude})')
        return float(latitude), float(longitude)
    else:
        logger.info(f'No location data for IP: {ip_address}')
        return None, None


def convert_time(timestamp):
     return (datetime.fromtimestamp(timestamp))

#For this to work time1 must be earlier than time2
def time_def(time1, time2):
    return time2 - time1;


def density_report(time1, time2):
    t1_convert_time = datetime.fromtimestamp(time1)
    t2_convert_time = datetime.fromtimestamp(time2)

    spent = t2_convert_time - t1_convert_time
    days = spent.days

    days = days*-1
    
    if((spent.seconds//3600) > 20):
        days += 1
        
    if((days/365) > 1):
        return 1;
    else:
        return (days/365)

def create_df(df, logger):
    logger.info('Creating DataFrame from input data')
    mydict = []

    start = 0
    end = 0
    df_len = len(df)
    
    ip_addresses = df['ip_address'].unique()

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        gps_coords = pool.starmap(convert_to_gps, [(ip, logger) for ip in ip_addresses])

    ip_to_coords = dict(zip(ip_addresses, gps_coords))

    for index in range(df_len - 1):
        if df['ip_address'][index] == df['ip_address'][index + 1]:
            end = index + 1
        else:
            lat, long = ip_to_coords[df['ip_address'][index]]
            temp_dict = {
                'Start_Time': df['timestamp'][start],
                'End_Time': df['timestamp'][end],  
                'City': df['city'][start],
                'State': df['region'][start],
                'timestamp': df['timestamp'][start],
                'latitude': lat,
                'longitude': long,
                'ip_address' : df['ip_address'][start],
                'dense': density_report(df['timestamp'][start], df['timestamp'][end])
            }
            mydict.append(temp_dict)
            start = end + 1  # Adjusted indexing
            end = end + 1

    # Process the last group
    lat, long = ip_to_coords[df['ip_address'][df_len - 1]]
    temp_dict = {
        'Start_Time': df['timestamp'][start],
        'End_Time': df['timestamp'][df_len - 1],  
        'City': df['city'][start-1],
        'State': df['region'][start-1],
        'latitude': lat,
        'longitude': long,
        'ip_address' : df['ip_address'][start-1],
        'dense': density_report(df['timestamp'][start], df['timestamp'][df_len - 1])  
    }
    mydict.append(temp_dict)
    logger.info('DataFrame creation complete')
    return pd.DataFrame(mydict)

 

def generate_graph(df):
    ip_maps = {}
    unique_ip = df['ip_address'].unique()
    
    month_colors = {
    'January': '#1f77b4',   # blue
    'February': '#2ca02c',  # green
    'March': '#d62728',     # red
    'April': '#ff7f0e',     # orange
    'May': '#9467bd',       # purple
    'June': '#8c564b',      # brown
    'July': '#e377c2',      # pink
    'August': '#7f7f7f',    # gray
    'September': '#17becf', # cyan
    'October': '#e31a1c',   # magenta
    'November': '#ff00ff',  # yellow
    'December': '#33a02c'   # lime
    }
    
    for ip in unique_ip:
        filtered_df = df[df['ip_address'] == ip].copy()
        
        filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'], unit='s')  # Convert timestamp to datetime
        filtered_df['year'] = filtered_df['timestamp'].dt.year
        filtered_df['month'] = filtered_df['timestamp'].dt.month_name()
        
        year_month_counts =  filtered_df.groupby(['year', 'month']).size().unstack(fill_value=0)

        # Plotting
        ax = year_month_counts.plot(kind='bar', figsize=(12, 6))

        city = filtered_df['City'].iloc[0] 

        plt.title(f'Total Occurrences of Year and Month for {city}')
        plt.xlabel('Year-Month')
        plt.ylabel('Total Occurrences')
        plt.xticks(rotation=45)
        
        for i, month in enumerate(year_month_counts.columns):
            ax.get_children()[i].set_color(month_colors[month])
        
        months = year_month_counts.columns.tolist()
        ax.legend(months, title='Month', bbox_to_anchor=(1, 1))

        plt.tight_layout()

        # Save the plot to a BytesIO buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Create HTML content for popup with the image
        html = f'<img src="data:image/png;base64,{image_base64}">'
        
        # Update the ip_maps dictionary with IP address and its corresponding graph HTML
        ip_maps[ip] = html
        
        # Clear the current plot to prepare for the next iteration
        plt.close()
        
    return ip_maps

def graph_over_all_time(ip_df, logger):
    logger.info('Creating graph_over_all_time from input data')

    ip_df['timestamp'] = pd.to_datetime(ip_df['timestamp'], unit='s')
    ip_df['year'] = ip_df['timestamp'].dt.year
    ip_df['month'] = ip_df['timestamp'].dt.month

    year_month_counts = ip_df.groupby(['year', 'month']).size().unstack(fill_value=0)

    # Plotting
    year_month_counts.plot(kind='bar', figsize=(12, 6), colormap='viridis')

    plt.title('Total Occurrences of Year and Month')
    plt.xlabel('Year-Month')
    plt.ylabel('Total Occurrences')
    plt.xticks(rotation=45)
    plt.legend(title='Month', bbox_to_anchor=(1, 1))
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Create HTML content for popup with the image
    html = f'<img src="data:image/png;base64,{image_base64}">'
    logger.info('Finished graph_over_all_time from input data')

    return html

# Function to handle click events on markers
def on_map_click(event):
    lat, lon = event.latlng
    
# Iterate through waypoints and add markers
def create_html(df, logger):
    min_lon, max_lon = -45, -35
    min_lat, max_lat = -25, -15
    mymap = folium.Map(location=[0, 0],
                zoom_start=2,
                min_lat=min_lat,
                max_lat=max_lat,
                min_lon=min_lon,
                max_lon=max_lon,
                no_touch=True
                )
    
    
    logger.info('Creating interactive_occurance.html from input data')
    # Define the number of processes to use
    num_processes = 4
    # Create a pool of worker processes
    unique_ips = df['ip_address'].unique()
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Map the process_ip function to each IP address
        results = pool.starmap(process_ip, [(ip, df) for ip in unique_ips])

    ip_time = {k: v for d in results for k, v in d.items()}

    
    for index, row in df.groupby('ip_address')[['latitude', 'longitude']].first().iterrows():
        folium.Marker(location=[row['latitude'], row['longitude']], popup=ip_time[index]).add_to(mymap)

    mymap.add_child(folium.ClickForMarker(popup=None))
    mymap.get_root().html.add_child(folium.Element("""
    <script>
        document.getElementsByClassName('folium-map')[0].onclick = function(event){
            var lat = event.latlng.lat;
            var lon = event.latlng.lng;
            var kernel = IPython.notebook.kernel;
            kernel.execute('generate_graph([' + lat + ', ' + lon + '], df)');
        }
    </script>
    """))

    # Display the map
    logger.info('Finished interactive_occurance.html from input data')
    return mymap

def save_timeline_graph(html_content, file_path):
    with open(file_path, 'w') as f:
        f.write(html_content)

#account_activity_v2
def run(in_path:Path, out_path:Path, logger:BtbLogger):

    out_path = out_path / "ip_loc"
    out_path.mkdir(parents=True, exist_ok=True)

    with open(in_path, 'r') as file:
        data = json.load(file)
    
    account_activity_v2_value = data.get("account_activity_v2")
    
    df = pd.DataFrame(account_activity_v2_value)
    
    logger.info("Running the ip_loc feature module")
    
    # Assuming df is your DataFrame

    edited_df = create_df(df, logger)
    folium_html = create_html(edited_df, logger)
    folium_html.save(out_path / "interactive_occurance.html")
    logger.wrote_file(out_path / "interactive_occurance.html")
    
    ip_timeline = graph_over_all_time(edited_df, logger)
    save_timeline_graph(ip_timeline, out_path / 'graph_over_all_time.html')
    logger.wrote_file(out_path / 'graph_over_all_time.html')

    return "Wrote interactive_occurance.html and graph_over_all_time.html!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='ip_loc',
                                     description='A short description of what your code does')
    parser.add_argument('-i', '--in_file', metavar='(NAME)_JSON', help='path to account_activity json', required=True)
    parser.add_argument('-o', '--out_path', metavar='OUTPUT_PATH', help='where to send outputs', required=False, default='.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='increase verbosity', required=False)
    args = parser.parse_args()

    logger = RootLogger()
    logger.setup(verb=args.verbose)

    print(run(args.in_file, args.out_path, logger))
