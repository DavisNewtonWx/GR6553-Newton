# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:08:20 2024

@author: davis
"""

import tarfile
import pygrib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import numpy as np

# This area at the top is used for looking at the gfs tar files and seeing which file I would like to use if I do not know what is there
# Specify the path to your tar file
#tar_file_path = 'gfs_4_2011042618.g2.tar'

# Open the tar file in read mode
#with tarfile.open(tar_file_path, 'r') as tar:
    # List all files in the tar archive
#    tar_contents = tar.getnames()

    # Print the names of the files
#    for content in tar_contents:
#        print(content)


# Extract and read GRIB files
tar_file_path = 'gfs_4_2011042718.g2.tar'
#'gfs_4_2011042700.g2.tar'
with tarfile.open(tar_file_path, 'r') as tar:
    tar.extractall(path='extracted_files')

grbGFS2 = pygrib.open('extracted_files/gfs_4_20110427_1800_003.grb2')
#gfs_4_20110427_0000_000.grb2
# Goes out by 3 hour incrementals
# Use grbGFS2.select() to find variables

# "vorticity500" is the variable I used to change around stuff to look at things like voriticty or relative humidity
# "gpheight500" remained as the geopotential height variable throughout entire process
# You can change both as needed
# Use "grbGFS2.select()" to find variable names you would like to use
vorticity500 = grbGFS2[274]
absvort2 = vorticity500.values
#vwind = grbGFS2[73]
#vwind300 = vwind.values
gpheight500 = grbGFS2[156]
gpheight3 = gpheight500.values
lats3, lons3 = vorticity500.latlons()

# First axis is looking specifically at Alabama, Mississippi, and parts of Tennessee and Georgia
# Second set extent is for entire United States
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': ccrs.LambertConformal(central_longitude=-96, central_latitude=40, standard_parallels=(40, 40))})
ax.set_extent([-90, -83, 30, 38])
#ax.set_extent([-125, -70, 20, 60])
ax.add_feature(cf.LAND, color='wheat')
ax.add_feature(cf.OCEAN, color='cornflowerblue')
ax.add_feature(cf.COASTLINE, edgecolor='black')
ax.add_feature(cf.STATES, edgecolor='black')
ax.add_feature(cf.BORDERS, edgecolor='black', linestyle='-')
ax.add_feature(cf.LAKES, color='cornflowerblue')

# This area is used for plotting whatever variable you'd like to look at
bounds2 = [200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950]

# Plot the filled contour map with specified levels
map = plt.contourf(lons3, lats3, absvort2, bounds2, cmap=plt.cm.gist_ncar, transform=ccrs.PlateCarree())
#map=plt.contourf(lons3,lats3,absvort2*100000,np.arange(-6.,78.,6), cmap=plt.cm.gist_ncar,transform=ccrs.PlateCarree())
#map=plt.contourf(lons3,lats3,absvort2,np.arange(np.min(absvort2), np.max(absvort2),6), cmap=plt.cm.gist_ncar,transform=ccrs.PlateCarree())
#map=plt.contourf(lons3,lats3,np.sqrt(absvort2**2 + vwind300**2)*1.94, bounds2, cmap=plt.cm.hot_r,transform=ccrs.PlateCarree())

cbar = plt.colorbar (location='bottom')
cbar.set_label ('m^2/s^2')

# Plotting height lines
height_levels = np.linspace(np.min(gpheight3 / 10), np.max(gpheight3 / 10), 22)  # Similarly for geopotential height
contour_lines = ax.contour(lons3, lats3, gpheight3 / 10, levels=height_levels, colors='black', transform=ccrs.PlateCarree())
d=plt.contour (lons3, lats3, gpheight3 / 10, np.arange(np.min(gpheight3 / 10),np.max(gpheight3 / 10),20), linewidths=2, colors='black', linestyle='-', transform=ccrs.PlateCarree())

# Used for plotting wind barbs
#plt.barbs(lons3[::9,::9],lats3[::9,::9],absvort2[::9,::9],vwind300[::9,::9],transform=ccrs.PlateCarree())

plt.title('April 27 21 UTC 850 mb Heights (dm) / 3km Storm Relative Helicity (m^2/s^2)')

plt.show()


