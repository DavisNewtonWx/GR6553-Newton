# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 22:58:49 2024

@author: davis
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import cartopy.crs as ccrs
import pyart
import pandas as pd
import nexradaws
import tempfile
import pytz
import cartopy.feature as cfeature
from metpy.plots import USCOUNTIES
import imageio


# Original code I used and altered can be found at the following link:
    # https://github.com/russ-schumacher/ats641_spring2022/blob/master/example_notebooks/pyart_nexrad_maps_reports.ipynb
    
templocation = tempfile.mkdtemp()

# Define the radar, start time, and end time
# Start and end time are in UTC
# First part will be the hour: 12
# Second part will be minutes: 00
radar_id = 'KBMX'
start = pd.Timestamp(2011, 4, 27, 18, 45).tz_localize(tz='UTC')
end = pd.Timestamp(2011, 4, 28, 5, 0).tz_localize(tz='UTC')

# Bounds of map we want to plot
min_lon = -89.00
max_lon = -84.00
min_lat = 33.00
max_lat = 36.00

# Connect and get the data
conn = nexradaws.NexradAwsInterface()
scans = conn.get_avail_scans_in_range(start, end, radar_id)
print("There are {} scans available between {} and {}\n".format(len(scans), start, end))

results = conn.download(scans, templocation)

# Load storm reports data
# This area used a CSV file due to SPC not having header at top of file
wind_rpts = pd.read_csv("2011_wind.csv")
wind_rpts['datetime'] = pd.to_datetime(wind_rpts['date'] + ' ' + wind_rpts['time'])
wind_rpts.set_index("datetime", inplace=True)
wind_rpts.index = wind_rpts.index.tz_localize("Etc/GMT+6").tz_convert("UTC")

# Download SPC tornado report file
tor_rpts = pd.read_csv("https://www.spc.noaa.gov/wcm/data/"+str(start.year)+"_torn.csv")
tor_rpts['datetime'] = pd.to_datetime(tor_rpts.date + ' ' + tor_rpts.time)
tor_rpts.set_index("datetime", inplace=True)
tor_rpts.index = tor_rpts.index.tz_localize("Etc/GMT+6", ambiguous='NaT', nonexistent='shift_forward').tz_convert("UTC")

# Similiar to wind reports, have to use own CSV file due to no header in reports
hail_rpts = pd.read_csv("2011_hail.csv")
hail_rpts['datetime'] = pd.to_datetime(hail_rpts['date'] + ' ' + hail_rpts['time'])
hail_rpts.set_index("datetime", inplace=True)
hail_rpts.index = hail_rpts.index.tz_localize("Etc/GMT+6").tz_convert("UTC")

# Plot and save radar images with storm reports
# Also creates a list to store all images to turn into a gif file
images = []
for i, scan in enumerate(results.iter_success(), start=1):
    if scan.filename[-3:] != "MDM":
        this_time = pd.to_datetime(scan.filename[4:17], format="%Y%m%d_%H%M").tz_localize("UTC")
        radar = scan.open_pyart()
        
        # Create a single figure with two subplots side by side
        fig, (ax1, ax2) = plt.subplots(figsize=[20, 10], ncols=2, subplot_kw={'projection': ccrs.PlateCarree()})
        
        # Plot radar data on the first subplot
        ax1.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())
        ax1.add_feature(USCOUNTIES.with_scale('500k'), edgecolor="gray", linewidth=0.4)
        ax1.add_feature(cfeature.STATES.with_scale('10m'), linewidth=1.0)
        gatefilter = pyart.filters.GateFilter(radar)
        gatefilter.exclude_below('reflectivity', -2.5)
        display = pyart.graph.RadarMapDisplay(radar)
        display.plot_ppi_map('reflectivity', 0, vmin=-7.5, vmax=65,
                             title=radar_id + " Reflectivity, " + this_time.strftime("%H%M UTC %d %b %Y"),
                             projection=ccrs.PlateCarree(), resolution='10m', gatefilter=gatefilter,
                             cmap='nipy_spectral', colorbar_flag=False, lat_lines=[0, 0], lon_lines=[0, 0], ax=ax1)
        
        # Plot storm reports on the second subplot
        ax2.set_extent([min_lon, max_lon, min_lat, max_lat], crs=ccrs.PlateCarree())
        ax2.add_feature(USCOUNTIES.with_scale('500k'), edgecolor="gray", linewidth=0.4)
        ax2.add_feature(cfeature.STATES.with_scale('10m'), linewidth=1.0)
        wind_rpts_now = wind_rpts[((start-pd.Timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")):this_time.strftime("%Y-%m-%d %H:%M")]
        ax2.scatter(wind_rpts_now.slon.values.tolist(), wind_rpts_now.slat.values.tolist(), s=20, facecolors='none', edgecolors='mediumblue', linewidths=1.8)
        tor_rpts_now = tor_rpts[((start-pd.Timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")):this_time.strftime("%Y-%m-%d %H:%M")]
        ax2.scatter(tor_rpts_now.slon.values.tolist(), tor_rpts_now.slat.values.tolist(), s=20, facecolors='red', edgecolors='red', marker="v",linewidths=1.5)
        hail_rpts_now = hail_rpts[((start-pd.Timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")):this_time.strftime("%Y-%m-%d %H:%M")]
        ax2.scatter(hail_rpts_now.slon.values.tolist(), hail_rpts_now.slat.values.tolist(), s=20, facecolors='none', edgecolors='green', linewidths=1.8)
        ax2.set_title("Storm Reports, " + this_time.strftime("%H%M UTC %d %b %Y"))
        ax2.legend(loc='upper left')
        
        # Save the figure
        plt.savefig(f"combined_{i}.png", bbox_inches='tight', dpi=100)
        plt.close()
        # Will save all images to your folder after done plotting the radar and storm reports
        images.append(f"combined_{i}.png")

# Optionally create an animated GIF
# Can comment out if not needed to make a gif
with imageio.get_writer("radar_storm_reports_side_by_side.gif", mode="I") as writer:
    for image in images:
        writer.append_data(imageio.imread(image))
