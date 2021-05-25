# OpenYYC Project - Distribution of open data in Calgary

#Motivation
To explore open Calgary data and:

* Determine what data is collected and geographically where the data is located
* Consider the data as an aggregated whole and categorically
* Assess the influences of the data distribtion


#Workflow:

![OpenYYC Rough Workflow](https://user-images.githubusercontent.com/59377701/119421240-7bfcbf80-bcbb-11eb-8d8b-3e8bca066cad.png)


# Data Extraction

Data was extracted from the Open Calgary API using the Datadownloader.py code written by R. Burns and modified with RegEx to remove characters problematic for filenames nad shapefiles.  The data was saved into a unique folder per dataset.

The data was extracted over a 48 hour period between November 21st and November 22nd 2020.  
Downloading had to be completed in multiple runs due to issues with the connection timing out, the initial request not identifying all data available, and errors associated with a particular data request (2016 Census of Canada - Top 5 Languages Spoken Most Often at Home by Ward).  After 48 hours the list of downloaded data was manually inspected and compared to the website.  Shapefiles that were absent were manually downloaded and added to the set.

Later on it was noted that large datasets such as the 311 Service Requests did not properly download due to the size of the file.  As a result, the file was manually downloaded, and data added after November 22nd 2020 was removed from the files.

In total 759 datasets were downloaded.  



# File Management

To make spatial data mangement easier, the shapefiles were extracted from the individual dataset folders into a common folder.  The filenames assigned by the city to the shapefiles are not in a useful format, so they needed to be renamed with the parent folder name.  After renaming and moving to a common folder, the shapefiles were then projected into the Alberta 3TM coordinate system.  To facilitate different data analysis and review depending on the geometry, the shapefiles were then saved to new folders based on whether they were points, multipoints, lines or polygons.






# Scripts in the Repository:

Datadownloader.py - Code modified from R. Burns to bulk extract all data from the Open Calgary website (https://data.calgary.ca/)

OpenYYC_script_shapefile_extraction.py - Code to extract all of the shapefile data and move it into a single folder

OpenYYC_script_projection_foldercreation - Code to separate shapefiles into new folders based on geometry and project into the desired coordinate system

OpenYYC_Script_tesslation_calculations - Code to count the number of data points within a tesselated area, normalize with respect to the total for that specific dataset and then combine with all the other tesselated files to build an aggregate layer.

Folders:

Old - Previous code snippits to be removed at a later date

Data - The tessellated shapefiles zipped


