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
    This sub-module is part of the 'persona_sight' package in the 'features' module.

Version:
    0.1.0

Author:
    Trevor Le
"""

### LIST OF CHANGES COMPARED TO BASE ###
### - Refer to the "Noah's Shenanigans" section.
###   - better geocoding
###   - (semi-subsequent) spatial aggregation.
###   - NOTE: I have left the imports within that section
###       for sake of containment. Please relocate them
###       to top if you want to move forward with that version.
### - Added return string for CLI usage.

import argparse
import os
from datetime import timedelta, datetime
# Add your other built-in imports here

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import maxminddb
import folium
from folium.plugins import HeatMap, TimestampedGeoJson
import random
from io import BytesIO
import base64
import json

# Please update requirements.txt as needed!

def convert_to_gps(ip_address):
    path = os.path.join(os.path.dirname(__file__), 'GeoLite2-City.mmdb')
    with maxminddb.open_database(path) as reader:
        response = reader.get(ip_address)
     
    return response
  #################
  
  #################
def convert_time(timestamp):
     return (datetime.fromtimestamp(timestamp))

  #################
  
  #################
  
#For this to work time1 must be earlier than time2
def time_def(time1, time2):
    return time2 - time1;

  #################
  
  #################
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

def create_df(df):
    mydict = []

    start = 0
    end = 0
    df_len = len(df)

    for index in range(df_len - 1):
        if df['ip_address'][index] == df['ip_address'][index + 1]:
            end = index + 1
        else:
            location = convert_to_gps(df['ip_address'][index])
            temp_dict = {
                'Start_Time': df['timestamp'][start],
                'End_Time': df['timestamp'][end],  
                'City': df['city'][start],
                'State': df['region'][start],
                'timestamp': df['timestamp'][start],
                'latitude': location['location']['latitude'],
                'longitude': location['location']['longitude'],
                'ip_address' : df['ip_address'][start],
                'dense': density_report(df['timestamp'][start], df['timestamp'][end])
            }
            mydict.append(temp_dict)
            start = end + 1  # Adjusted indexing
            end = end + 1

    # Process the last group
    location = convert_to_gps(df['ip_address'][df_len - 1])
    temp_dict = {
        'Start_Time': df['timestamp'][start],
        'End_Time': df['timestamp'][df_len - 1],  
        'City': df['city'][start-1],
        'State': df['region'][start-1],
        'latitude': location['location']['latitude'],
        'longitude': location['location']['longitude'],
        'ip_address' : df['ip_address'][start-1],
        'dense': density_report(df['timestamp'][start], df['timestamp'][df_len - 1])  
    }
    mydict.append(temp_dict)
    return pd.DataFrame(mydict)

def generate_graph(df):
    ip_maps = {}
    unique_ip = df['ip_address'].unique()
    for ip in unique_ip:
        filtered_df = df[df['ip_address'] == ip].copy()
        
        filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'], unit='s')  # Convert timestamp to datetime
        filtered_df['year'] = filtered_df['timestamp'].dt.year
        filtered_df['month'] = filtered_df['timestamp'].dt.month
        
        year_month_counts =  filtered_df.groupby(['year', 'month']).size().unstack(fill_value=0)

        # Plotting
        year_month_counts.plot(kind='bar', figsize=(12, 6), colormap='viridis')

        plt.title('Total Occurrences of Year and Month for ' + ip)
        plt.xlabel('Year-Month')
        plt.ylabel('Total Occurrences')
        plt.xticks(rotation=45)
        plt.legend(title='Month', bbox_to_anchor=(1, 1))
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

# Function to handle click events on markers
def on_map_click(event):
    lat, lon = event.latlng
    
# Iterate through waypoints and add markers
def create_html(df):
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
    
    
    
    unique_ip = df['ip_address'].unique()
    ip_time = generate_graph(df)
    
    for index, row in df.groupby('ip_address')[['latitude', 'longitude']].first().iterrows():
        popup_text = index  # Access IP address directly
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
    return mymap


#account_activity_v2
def run(pathname):

    with open(pathname, 'r') as file:
        data = json.load(file)
    
    account_activity_v2_value = data.get("account_activity_v2")
    
    df = pd.DataFrame(account_activity_v2_value)
    
    print("Running the ip_loc feature module")
    
    # Assuming df is your DataFrame

    edited_df = create_df(df)

    print('====== STARTING NOAH\'S SHENANIGANS ======')
    from geopy.geocoders import Nominatim
    gc = Nominatim(user_agent="selfscape-insight") # Better geocoder. In PROD, append OS username to UA. (e.g. "selfscape-insight:noah")
    from tqdm import tqdm
    import time
    for i, r in tqdm(edited_df.iterrows(), total=len(edited_df), desc='Geocoding...'):
        time.sleep(0.5) # To avoid rate limiting
        loc = gc.geocode({'city': r['City'], 'state': r['State']})
        edited_df.at[i, 'latitude'] = loc.latitude
        edited_df.at[i, 'longitude'] = loc.longitude
        edited_df.at[i, 'ip_address'] = r['City'] # Lazy spatial aggregation instead of IP addresses drawing over eachother
    print('====== END OF NOAH\'S SHENANIGANS ======')

    folium_html = create_html(edited_df)
    folium_html.save("folium_occurance.html")
    return "Wrote folium_occurance.html"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='ip_loc',
                                     description='A short description of what your code does')
    parser.add_argument('-account_activity_v2', metavar='ACCOUNT_ACTIVITY_V2',
                        help='path to account_activity_v2 json file', required=True)
    args = parser.parse_args()
    run(args.account_activity_v2)
