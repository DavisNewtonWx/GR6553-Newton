# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 02:20:43 2024

@author: davis
"""

import tarfile
import pygrib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import numpy as np

# Path to your GRIB file
tar_file_path = 'gfs_4_2011042718.g2.tar'  # Adjust this as needed
with tarfile.open(tar_file_path, 'r') as tar:
    tar.extractall(path='extracted_files')

# Open GRIB file
grb_file = 'extracted_files/gfs_4_20110427_1800_003.grb2'  # Example GRIB file for April 27, 2011
grb = pygrib.open(grb_file)

# Area for selecting temperature at certain levels, geopotential heights at certain levels, as well as the u and v wind components at certain levels
temp850 = grb[157]  # or 310/268
temp = temp850.values
gpheight850 = grb[156]
gpheight = gpheight850.values
uwind = grb[160]
u_wind = uwind.values
vwind = grb[161]
v_wind = vwind.values
lats, lons = temp850.latlons()
lats2, lons2 = gpheight850.latlons()

# Calculate gradients of temperature
temp_x, temp_y = np.gradient(temp)

# Calculate temperature advection
temp_advection = -(u_wind * temp_x + v_wind * temp_y)

# Setting up the map
# First axis extent is for United States
# Second axis extent is for specifically the southeast United States
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.LambertConformal(central_longitude=-96, central_latitude=35)})
#ax.set_extent([-130, -60, 20, 50], crs=ccrs.PlateCarree())
ax.set_extent([-90, -83, 30, 38], crs=ccrs.PlateCarree())
ax.add_feature(cf.COASTLINE)
ax.add_feature(cf.BORDERS, linestyle=':')
ax.add_feature(cf.STATES, linestyle=':')

# Area for plotting the temperature advection
bounds = [-32, -24, -16, -8 , 0, 8, 16, 24, 32]

plt.contourf(lons, lats, temp_advection, bounds, cmap=plt.cm.coolwarm, transform=ccrs.PlateCarree())
cbar=plt.colorbar(location='bottom')
cbar.set_label ('Temperature Advection (K/s)')

# Plotting geopotential height and wind barbs
d=plt.contour (lons2, lats2, gpheight / 10, np.arange(np.min(gpheight / 10),np.max(gpheight / 10),3), linewidths=2, colors='black', linestyle='-', transform=ccrs.PlateCarree())
plt.barbs(lons2[::3,::3],lats2[::3,::3],u_wind[::3,::3],v_wind[::3,::3],transform=ccrs.PlateCarree())

#cbar = plt.colorbar(contour_fill, orientation='horizontal', pad=0.05)
#cbar.set_label('Temperature Advection (K/s)')

plt.title('Temperature Advection at 850 mb on April 27, 2011')
plt.show()