# GR6553-Newton
**Computer Methods in Meteorology Final Project Code Upload Area**
-

#
**Hello and welcome!**
-

This area is full of code that was used in the Computer Methods for Meteorology Class taken during the Spring 2024 at Mississippi State.
All of the code that I used for my project is found here, as well as all plots, and the data I found as well.
Because some of the data was so big, I was not able to upload it all here, however, I will have links to those listed below.

This project looks at the 2011 La Nina season, looking specifically at sea surface temperatures in the Atlantic to confirm the La Nina. 
This was also looking at some of the events that came from the 2011 tornado outbreak from April 25-28.
A lot of the environmental factors, such as CAPE, were looked at through model GFS data from the 18Z run on April 27th, as I specifically focused on April 27th in North/Central Alabama.
Other radar data and storm reports were done as well, along with looking at the overall tornado composites from the 2011 year as a whole to see how tornadoes were during the 2011 year.
Generally, I was looking at the 2011 La Nina and how it affected tornadoes during that season, especially during the April 25-28 super outbreak.

If there are any questions about some code or a file will not download, please feel free to reach out to me here on GitHub or via my school email dbn64@msstate.edu.
Thank you for stopping by!

#
**Data**
-

**All data used in the project for this class can be found either in this section or in the "Data download" folder.**
Below are some of the websites I found my data from that could not be uploaded due to the files being too big:
    
  1. GFS Data downloaded from here: [Link to overall website](https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast) 
  2. [Link to 0.5 degree resolution data download that was used](https://www.ncei.noaa.gov/has/HAS.FileAppRouter?datasetname=GFSGRB24&subqueryby=STATION&applname=&outdest=FILE)
  3. [Link to download the archived data needed for running other WPC surface maps](https://www.mesonet.agron.iastate.edu/wx/afos/p.php?pil=CODSUS&e=202010201500)
  4. [Link to download the archived data needed for running other SPC Day 1 outlooks](https://www.spc.noaa.gov/archive/)

**Some of my additional data used in the project will not be uploaded here or found on the web.**
Part of that is due to the fact that both of the files are still very large and cannot be uploaded properly.
However, because they are part of my thesis research, I will not be uploading them, as I am currently using them for my own research.
If you would like the files used in either of the following programs:

    1. The tornado composite file data used in the Python script: "tornado_data_for_composite_on_PC"
    2. The sea surface temperature data used in the Python script: "SST_ENSO_Plotting"

Please reach out to me via email to ask about the files for your use in either program.

#
**Plots**
-

**All of the plots I ended up making for this project can be located in the "Images from project" folder.**
All the different plots that I ended up making will be listed below. However, please note that all of the plots I list off will not be in order as they are in the folder itself.

      1. 2011 La Nina SST Temperature Values
      2. 2011 Composite Averages of Tornadoes related to the La Nina event (United States and Southeast US)
      3. WPC Surface Analysis on April 27 from 21 UTC and 00/03 UTC on April 28
      4. April 27th Soundings at 12 and 18 UTC from Birmingham and Jackson
      
      *The following files were taken from the 18 UTC run of the GFS on April 27 looking at the 21 UTC 
      forecast hour*
      
      5. 300 mb heights and winds on April 27 at 21 UTC
      6. 850 mb Relative Humidity on April 27 at 21 UTC
      7. 850 mb Temperature Advection on April 27 at 21 UTC
      8. 850 mb Vertical Velocities on April 27 at 21 UTC
      9. 850 mb Storm Relative Helicity on April 27 at 21 UTC
      10. 850 mb CAPE on April 27 at 21 UTC
      11. 850 mb CIN on April 27 at 21 UTC
      12. SPC Day 1 Outlook for April 27th at 20 UTC (Convective, Tornado, Wind, and Hail risks)
      13. Birmingham Radar from April 27th at 1830 UTC through April 28th at 05 UTC and Storm Reports from the surveys after the storms

#
**Running the code on your machine**
-

**Please ensure before anything else that you have Python installed properly as well as conda.**
I also heavily used the following programs:

      1. pandas
      2. xarray
      3. matplotlib.pyplot, patches
      4. numpy
      5. scipy
      6. metpy
      7. cartopy.crs, features, and cartopy (standard)
      8. geopandas

  Please double check your own Python and the different things you have installed for your environment to ensure it will run correctly.
  All needed programs will be listed at the top of every coding file. If something is needed to run the file properly, please install it if you haven't already.
      
