import geopandas
import matplotlib.pyplot as plt
from cartopy import crs as ccrs
import cartopy.feature as cf
from matplotlib.patches import Patch

# Read in the shapefile
cat_gdf = geopandas.read_file('day1otlk_20110427_2000_cat.shp')

# Extract the CRS parameters from the shapefile's CRS attribute
data_crs = ccrs.LambertConformal(
    central_latitude=cat_gdf.crs.to_dict().get('lat_0'),
    central_longitude=cat_gdf.crs.to_dict().get('lon_0'),
    standard_parallels=(cat_gdf.crs.to_dict().get('lat_1'), cat_gdf.crs.to_dict().get('lat_2'))
)

# Color scales used for the SPC outlook
cat_plot_colors = {
    # These are used for convective outlook
    2: 'palegreen',  # Thunderstorms
    3: 'green',      # Slight Risk
    4: 'yellow',     # Enhanced Risk
    5: 'orange',      # Moderate Risk
    6: 'red',        # High Risk
    8: 'magenta'     # Very High Risk
    
    #These are used for tornado risk
    #2: 'green',  
    #5: 'brown',      
    #10: 'yellow',        
    #15: 'red',     
    #30: 'magenta',
    #45: 'purple',
    #60: 'blue'
    
    # These are used for hail and wind risk
    #5: 'brown',  
    #15: 'yellow',     
    #30: 'red',       
    #45: 'magenta',    
    #60: 'purple'
}

risk_labels = {
    
    # Labes for the key in the bottom left
    2: "Thunderstorms",
    3: "Marginal Risk", # Should be marginal
    4: "Slight Risk", # Should be slight
    5: "Enhanced Risk",  # Should be enhanced
    6: "Moderate Risk", # Should be moderate
    8: "High Risk"
    
    # Key for tornado risk
    #2: "2%",
    #5: "5%", # Should be marginal
    #10: "10%", # Should be slight
    #15: "15%",  # Should be enhanced
    #30: "30%", # Should be moderate
    #45: "45%",
    #60: "60%"
    
    # Key for wind/hail risk
    #5: "5%", # Should be marginal
    #15: "15%",  # Should be enhanced
    #30: "30%", # Should be moderate
    #45: "45%",
    #60: "60%"
}

# Area for plotting SPC outlook
fig = plt.figure(1, figsize=(14,12))
ax = plt.subplot(1, 1, 1, projection=ccrs.LambertConformal(central_longitude=-96, central_latitude=40, standard_parallels=(40, 40)))
ax.set_extent([-130, -60, 25, 46], ccrs.PlateCarree())
#ax.add_feature(cf.LAND, color='white')
#ax.add_feature(cf.OCEAN, color='lightblue')
#ax.add_feature(cf.COASTLINE, edgecolor='black')
#ax.add_feature(cf.STATES, edgecolor='black')
#ax.add_feature(cf.BORDERS, edgecolor='black', linestyle='-')
#ax.add_feature(cf.LAKES, color='lightblue')
ax.add_feature(cf.COASTLINE)
ax.add_feature(cf.OCEAN)
ax.add_feature(cf.LAND)
ax.add_feature(cf.BORDERS)
ax.add_feature(cf.STATES)
ax.add_feature(cf.LAKES)

# Create legend patches
# Legend will be going in bottom left area
legend_patches = [Patch(facecolor=cat_plot_colors[key], edgecolor='black', label=risk_labels[key]) for key in cat_plot_colors]

for key, color in cat_plot_colors.items():
    geometries = cat_gdf[cat_gdf['DN'] == key]
    if not geometries.empty:
        ax.add_geometries(geometries['geometry'], crs=data_crs, facecolor=color, edgecolors='black', alpha=0.5)

# Add the legend to the plot
ax.legend(handles=legend_patches, loc='lower left', title="Risk Levels")

plt.title('SPC Day 1 Categorical Outlook for April 27, 2011 at 2000 UTC')
plt.show()
