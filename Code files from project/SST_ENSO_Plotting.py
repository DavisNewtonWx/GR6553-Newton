# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 10:17:49 2024

@author: davis
"""

from netCDF4 import Dataset
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import netcdf
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


# Uses data that is for my thesis research. Please contact me if you would like to use it.
data = xr.open_dataset('HadISST_sst_fixICE.nc')

lat = data.variables['latitude'][:]
lon = data.variables['longitude'][:]
time = data.variables['time'][:]
sst = data.variables['sst'][:]
sst=data['sst']

mean_sst = np.mean(sst, axis=0)
#print(mean_sst)


# Calculates a rolling time average for December-January-February or March-April-May
# Slicing data here due to fact that I am only looking from 1980 until 2021
# Selecting 1979 is due to fact that we have to include previous year December data
nino34=sst.sel(longitude=slice(190,240),latitude=slice(-5,5)).mean(('longitude','latitude'))
nino_rolling=nino34.rolling(time=3).mean()
nino34_all=nino_rolling.resample(time='AS').mean()
nino34_sum=nino_rolling.sel(time=nino_rolling.time.dt.month.isin(8)) # summer
nino34_pwin=nino_rolling.sel(time=nino_rolling.time.dt.month.isin(2)) # previous winter
nino34_fwin=nino_rolling.sel(time=nino_rolling.time.dt.month.isin(2)) # future winter

nino34_all=nino34_all.sel(time=slice('1979','2021'))
nino34_sum=nino34_sum.sel(time=slice('1979','2021'))
nino34_pwin=nino34_pwin.sel(time=slice('1979','2021'))
nino34_fwin=nino34_fwin.sel(time=slice('1980','2022'))
nino34_all['time']=pd.date_range('1979-01-01',freq='1YS',periods=43)
nino34_sum['time']=pd.date_range('1979-01-01',freq='1YS',periods=43)
nino34_pwin['time']=pd.date_range('1979-01-01',freq='1YS',periods=43)
nino34_fwin['time']=pd.date_range('1979-01-01',freq='1YS',periods=43)


# Does same thing as above but looking at specifically the sea surface temperature data from this dataset
sst_rolling=sst.rolling(time=3).mean()
sst_all=sst_rolling.resample(time='AS').mean()
sst_sum=sst_rolling.sel(time=sst_rolling.time.dt.month.isin(8))
sst_pwin=sst_rolling.sel(time=sst_rolling.time.dt.month.isin(2))
sst_fwin=sst_rolling.sel(time=sst_rolling.time.dt.month.isin(2))

sst_all=sst_all.sel(time=slice('1979-01-01','2021-12-31'))
sst_sum=sst_sum.sel(time=slice('1979','2021'))
sst_pwin=sst_pwin.sel(time=slice('1979','2021'))
sst_fwin=sst_fwin.sel(time=slice('1980','2022'))

sst_all['time']=pd.date_range('1979-01-01',freq='1YS',periods=43)
sst_sum['time']=pd.date_range('1979-01-01',freq='1YS',periods=43)
sst_pwin['time']=pd.date_range('1979-01-01',freq='1YS',periods=43)
sst_fwin['time']=pd.date_range('1979-01-01',freq='1YS',periods=43)

# Select whatever years you would like to plot
#El_Nino_Years = [1980,1983,1987,1988,1992,1995,1998,2003,2005,2007,2010,2015,2016,2019]
#La_Nina_Years = [1984, 1985, 1989,1999,2000,2001,2006,2008,2009,2011,2012,2017,2018,2021]
La_Nina_Years = [2011]


# Calculate the number of rows needed for the subplot, with three plots per row.
#num_rows = len(El_Nino_Years)
num_rows = len(La_Nina_Years)
num_columns = 4  # 'sst_fwin', 'sum', and 'pwin'
fig, axs = plt.subplots(num_rows, num_columns, subplot_kw={"projection": ccrs.PlateCarree(central_longitude=180)}, figsize=(15, num_rows * 4))
#fig, axs2 = plt.subplots(num_rows2, num_columns, subplot_kw={"projection": ccrs.PlateCarree(central_longitude=180)}, figsize=(12, num_rows2 * 3))

for i, year in enumerate(La_Nina_Years):
    for j, dataset in enumerate(['sst_pwin', 'sst_sum', 'sst_fwin', 'sst_all']):
        ax = axs[j]  # Select the appropriate subplot.
        ax.coastlines()
        ax.gridlines()

        if dataset == 'sst_pwin':
            title = f"La Nina SST Anomaly for DJF of {year} (yr-1)"
            variable = 'SST Anomaly (degC)'
        elif dataset == 'sst_sum':
            title = f"La Nina SST Anomaly for MAM of {year}"
            variable = 'SST Anomaly (degC)'
        elif dataset == 'sst_fwin':
            title = f"La Nina SST Anomaly for DJF of {year} (yr+1)"
            variable = 'SST Anomaly (degC)'
        elif dataset == 'sst_all':
            title = f"La Nina SST Yearly Climatology Mean for {year}"
            variable = 'SST Anomaly (degC)'

        # Plotting the actual data here
        data = globals()[dataset]  # Assuming the datasets are named sst_fwin, sum, pwin

        filtered_data = data.sel(latitude=slice(-30, 30))

        mesh = (filtered_data.sel(time=str(year)) - filtered_data.mean('time')).squeeze().plot.contourf(
            ax=ax, transform=ccrs.PlateCarree(),
            levels=np.arange(-2.5, 2.6, 0.5),
            extend='neither',
            add_colorbar=False,
            cmap="RdBu_r"
        )
        
        # This area allows for me to plot to a specific range without having missing data
        (filtered_data.sel(time=str(year)) - filtered_data.mean('time')).squeeze().plot.contourf(
            ax=ax, transform=ccrs.PlateCarree(),
            levels=np.arange(-2.5, 2.6, 0.5),
            extend='both',
            add_colorbar=False,
            cmap="RdBu_r"
        )


        cbar = plt.colorbar(mesh, ax=ax, shrink=0.702, pad=0.0)
        cbar.ax.set_ylabel(variable, fontsize=8)  # Set the font size for the label
        cbar.ax.tick_params(labelsize=8)
        ax.set_extent((120, 300, 30, -30))
        ax.set_title(title, fontsize=9)

# Areas for grid lines
# Doesn't really work too well
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=0.2, color='gray', alpha=0.5, linestyle='--')
gl.top_labels = False
gl.bottom_labels = True
gl.left_labels = True
gl.right_labels = False
gl.xlocator = mticker.FixedLocator([-180, -45, 0, 45, 180])
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': 15, 'color': 'gray'}
gl.xlabel_style = {'color': 'black', 'weight': 'bold'}
plt.tight_layout(pad=0.70)
#plt.tight_layout(pad=0.45)
fig.subplots_adjust(hspace=-0.70)
#plt.savefig('ENSO_SST_anomalies_La_Nina_Events.png')
plt.show()