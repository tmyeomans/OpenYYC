# OpenYYC Project - Distribution of open data in Calgary

Scripts:


Datadownloader.py - Code modified from R. Burns to bulk extract all data from the Open Calgary website (https://data.calgary.ca/)

OpenYYC_script_shapefile)extraction.py - Code to extract all of the shapefile data and move it into a single folder

OpenYYC_script_projection_foldercreation - Code to separate shapefiles into new folders based on geometry and project into the desired coordinate system

OpenYYC_Script_tesslation_calculations - Code to count the number of data points within a tesselated area, normalize with respect to the total for that specific dataset and then combine with all the other tesselated files to build an aggregate layer.

Folders:

Archive - Previous code snippits to be removed at a later date

Data - The tessellated shapefiles zipped
