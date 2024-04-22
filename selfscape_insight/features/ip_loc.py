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
            'latitude': location['location']['latitude'],
            'longitude': location['location']['longitude'],
            'ip_address' : df['ip_address'][start],
            'days spent/365 days(one year)': density_report(df['timestamp'][start], df['timestamp'][end])
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
    'days spent/365 days(one year)': density_report(df['timestamp'][start], df['timestamp'][df_len - 1])  
}
mydict.append(temp_dict)

finalDF = pd.DataFrame(mydict)

def generate_graph(df):
    ip_maps = {}
    unique_ip = df['ip_address'].unique()
    ip_list = list(unique_ip)
    for ip in ip_list:
        filtered_df = df[df['ip_address'] == ip] 
        
        filtered_df['timestamp'] = pd.to_datetime(filtered_df['timestamp'])  # Ensure 'timestamp' is datetime
        filtered_df['year'] =  filtered_df['timestamp'].dt.year
        filtered_df['month'] =  filtered_df['timestamp'].dt.month

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
        plt.clf()
        
    return ip_maps


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

min_lon, max_lon = -45, -35
min_lat, max_lat = -25, -15
mymap = folium.Map(location=[0, 0],
                zoom_start=2,
                min_lat=min_lat,
                max_lat=max_lat,
                min_lon=min_lon,
                max_lon=max_lon
                )

# Function to handle click events on markers
def on_map_click(event):
    lat, lon = event.latlng
    
# Iterate through waypoints and add markers
unique_ip = df['ip_address'].unique()
ip_time = generate_graph(finalDF)
for index, row in unique_ip.iterrows():
    location = [row['latitude'], row['longitude']]
    popup_text = row['ip_address']  # Access 'ip_address' from the current row
    folium.Marker(location=location, popup=ip_time[popup_text]).add_to(mymap)

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