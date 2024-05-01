# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 14:42:47 2024

@author: davis
"""

#Note: This code will require a netcdf made specifically from NOAA tornado data
#If you would like the file, please let me know through my contact on the GitHub ReadMe file


import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


#Import the data file
data = xr.open_dataset('tornado_actual_monthly_1950_2022_1p0.nc').shift(lat=1)

#Create a region mask of only the United States and get rid of the oceans
import regionmask
basins = regionmask.defined_regions.natural_earth_v5_0_0.land_110
oceanmask=basins.mask(data.lon,data.lat)#,wrap_lon=180)
mask=xr.where( ((data.tornado.mean(('month','year','mag','states'))==0)&(oceanmask.T.isnull())),0,1)

#Years to calculate the data
La_Nina_Years = [ 2011 ] #1984, 1985, 1989, 1999, 2000, 2001, 2006, 2008, 2009, 2011, 2012, 2017, 2018, 2021]

# Calculate composites for each category
# Also taking all the count data and composite data and putting it into a list
composite_data = []
total_counts = []


# Calculate composites for each category
# All data calculating the sum of all months in that year, the magnitude (EF rating) of the tornado, as well as finding out what states they occured in
# Looking at specifically the months of December (year prior), January, and February
# Second one deals with looking at March, April, and May by calculating the sum
# Third one is the same as the first, but with January and February going to be the following year
# Last one simply looks at climatological mean
composite_data = []
for category in range(4):  # Assuming 4 categories
    category_calculations = []
    for year in La_Nina_Years:
        if category == 0:
            calculation = ((data.tornado.sel(month=[12], year=year-1).sum(('month', 'mag', 'states'))) + (data.tornado.sel(month=[1, 2], year=year).sum(('month', 'mag', 'states'))))
        elif category == 1:
            calculation = data.tornado.sel(month=[3, 4, 5], year=year).sum(('month', 'mag', 'states'))
        elif category == 2:
            calculation = ((data.tornado.sel(month=[12], year=year).sum(('month', 'mag', 'states'))) + (data.tornado.sel(month=[1, 2], year=year+1).sum(('month', 'mag', 'states'))))
        else:  # category == 3
            calculation = data.tornado.sel(year=year).sum(('month', 'mag', 'states')) - data.tornado.sel(year=year).mean(('month', 'mag', 'states'))
        category_calculations.append(calculation)
    
    # Use xarray to concatenate and then calculate the mean across all years for the category
    composite = xr.concat(category_calculations, dim='year').mean(dim='year')
    composite_data.append(composite)
    total_counts.append(len(category_calculations))


# Now plot composites
fig, axs = plt.subplots(1, 4, figsize=(20, 5), subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)})

# Titles here to not have to repeat them over and over when plotting more than one year
titles = [
    '2011 Composite Average Prior to Main La Niña Event (DJF (yr-1))',
    '2011 Composite Average During Main La Niña Event (MAM)',
    '2011 Composite Average After Main La Niña Event (DJF (yr+1))',
    '2011 Entire Year Composite Average',
]

# Extent axis are in 360 degrees, not negative and positive values seen on map
for idx, (composite, count, title) in enumerate(zip(composite_data, total_counts, titles)):
    ax = axs[idx]
    ax.set_title(title, fontsize=10)
    ax.set_extent([230, 300, 24, 50], crs=ccrs.PlateCarree())
    #ax.set_extent([269, 277, 30, 36], crs=ccrs.PlateCarree())
    #ax.set_extent([-90, -83, 30, 38])
    #ax.set_extent([-125, -70, 20, 60])
    ax.add_feature(cfeature.STATES, edgecolor='black')
    ax.coastlines('50m')
    ax.add_feature(cfeature.BORDERS)
    
    # Plot composite data
    mesh = composite.where(mask == 1).where(composite > 0).T.plot.pcolormesh(
        ax=ax, transform=ccrs.PlateCarree(), levels=np.arange(1., 6.1, 1), extend='neither',
        cmap='jet', add_colorbar=False)
    
    # This part allows for a scale to be used without leaving out data
    composite.where(mask == 1).where(composite > 0).T.plot.pcolormesh(
            ax=ax, transform=ccrs.PlateCarree(), levels=np.arange(1., 6.1, 1), extend='both',
            cmap='jet', add_colorbar=False)

    cbar = plt.colorbar(mesh, ax=ax, shrink=0.650, pad=0.0)
    cbar.ax.set_ylabel("Number of Tornadoes in Area", fontsize=9)
    cbar.ax.tick_params(labelsize=9)
    
    # Set the title for each subplot
    ax.set_title(title, fontsize=10)
    #ax.annotate(f'Total Tornadoes: {int(composite.sum().values)}\nYears Summed: {count}', 
    #            xy=(0.00, 0.03), xycoords='axes fraction', fontsize=6) # Use these if you want to display how many tornadoes and years were used to find the composite

plt.tight_layout(pad=0.60)
#plt.savefig('Tornadoes_Composite_La_Nina_Patterns24.png')
plt.show()