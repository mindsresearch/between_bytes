"""A short description of what your code does.

A longer description of what your code does,
including what csvs it takes in, and what it
contributes to the final output

Functions:
    run(account_activity_v2): Runs the feature.

Example usage:
    >>> from features import ip_loc as ipl
    >>> ipl.run(JsonReader.get_csv("account_activity_v2"))
    filepath to HTML page containing results of analysis

    $ python3 ip_loc.py -account_activity_v2 /path/to/account_activity_v2.csv
    filepath to HTML page containing results of analysis

Dependencies:
    pandas for data handling
    geopandas for geospatial data handling
    matplotlib.pyplot for basic datavis
    folium for more advanced datavis
    maxminddb for IP -> lat/long conversion
    [ADD DESCRIPTIONS FOR FURTHER THIRD-PARTY IMPORTS HERE]


Note:
    This sub-module is part of the 'persona_sight' package in the 'features' module.

Version:
    0.1.0

Author:
    Trevor Le
"""

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


map_of_graphs = {}
global df
# Add your other third-party/external imports here
# Please update requirements.txt as needed!

def convert_to_gps(ip_address):
     with maxminddb.open_database('GeoLite2-City.mmdb') as reader:
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
    
    
def generate_graph(ip_df):
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

    return html
    
    


x = df.loc[df['days spent/365 days(one year)'].idxmax()]
start_loc  = [x['latitude'], x['longitude']]

mymap = folium.Map(location=[start_loc[0], start_loc[1]], zoom_start=10, no_touch=True)
occuranceGraph()

def generate_graph(df):
    distinct_ips = df['ip_address'].unique().tolist()

    for ip in distinct_ips:
        filtered_df = df[df['ip_address'] == ip]
        filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'], unit='s')
        filtered_df['year'] = filtered_df['timestamp'].dt.year
        filtered_df['month'] = filtered_df['timestamp'].dt.month

        year_month_counts = filtered_df.groupby(['year', 'month']).size().unstack(fill_value=0)

        # Plotting
        year_month_counts.plot(kind='bar', figsize=(12, 6), colormap='viridis')

        plt.title('Total Occurrences of Year and Monthf for ' + ip)
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
        
        temp_dict = {ip : html}

        map_of_graphs.append(temp_dict)

# Function to handle click events on markers
def on_marker_click(event):
    lat, lon = event.latlng
    html = generate_graph(df)
    popup_text = f'<div>{html}</div>'
    folium.Marker(location=[lat, lon], popup=popup_text).add_to(mymap)

    for index, row in df.iterrows():
        location = [row['latitude'], row['longitude']]
        popup_text = row['ip_address']
        folium.Marker(location=location).add_to(mymap)

# Add click event listener to the map
    mymap.get_root().html.add_child(folium.Element("""
    <script>
    var map = document.getElementsByClassName('folium-map')[0];
    map.onclick = function(event){
        var lat = event.latlng.lat;
        var lon = event.latlng.lng;
        var kernel = IPython.notebook.kernel;
        kernel.execute('generate_graph(df)');
    }
    </script>
    """))

    # Display the map
    mymap


#account_activity_v2
def run():
    print("Running the ip_loc feature module")
    
    global df 
    df = pd.read_csv('/Users/trevorle/School/Senior_Project/csv/account_activity_v2.csv')
    return "The ip_loc module did stuff!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='ip_loc',
                                     description='A short description of what your code does')
    parser.add_argument('-account_activity_v2', metavar='ACCOUNT_ACTIVITY_V2_CSV',
                        help='path to account_activity_v2 csv file', required=True)
    args = parser.parse_args()
    print(run(args.account_activity_v2))


run()