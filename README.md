# OpenYYC Project - Distribution of Open Data in Calgary

# Motivation
To explore open Calgary data and:

* Determine what data is collected and geographically where the data is located
* Consider the data as an aggregated whole and categorically
* Assess the influences of the data distribtion


# Workflow:

![OpenYYC Rough Workflow](https://user-images.githubusercontent.com/59377701/119421240-7bfcbf80-bcbb-11eb-8d8b-3e8bca066cad.png)


# Data Extraction

Data was extracted from the Open Calgary API using the Datadownloader.py code written by R. Burns and modified with RegEx to remove characters problematic for filenames nad shapefiles.  The data was saved into a unique folder per dataset.

The data was extracted over a 48 hour period between November 21st and November 22nd 2020.  
Downloading had to be completed in multiple runs due to issues with the connection timing out, the initial request not identifying all data available, and errors associated with a particular data request (2016 Census of Canada - Top 5 Languages Spoken Most Often at Home by Ward).  After 48 hours the list of downloaded data was manually inspected and compared to the website.  Shapefiles that were absent were manually downloaded and added to the set.

Later on it was noted that large datasets such as the 311 Service Requests did not properly download due to the size of the file.  As a result, the file was manually downloaded, and data added after November 22nd 2020 was removed from the files.

In total 759 datasets were downloaded.  



# File Management

To make spatial data mangement easier, the shapefiles were extracted from the individual dataset folders into a common folder.  The filenames assigned by the city to the shapefiles are not in a useful format, so they needed to be renamed with the parent folder name.  After renaming and moving to a common folder, the shapefiles were then projected into the Alberta 3TM coordinate system.  To facilitate geometry dependent analysis and review, the shapefiles were saved to new folders based on whether they were points, multipoints, polylines or polygons.

# Tessellation 

Several tessellated shapefiles were created manually with the extent set to the City Boundary shapefile and visually compared.  A size of 0.5 square kilometers per hexagonal tessell was chosen as the host shapefile for the individual data counts.

A copy of the tessellated host layer was spatially joined to each dataset.  

* Points and multipoints were joined using 'completely contains'
* Polylines and polygons were joined using 'intersects'

This join process provides a join count per tessell cell.  These values are used later for a simple sum of all the data per tessell for all of the Open Calgary datasets.

The simple sum, as will be seen later, is insufficient to review the Open Calgary data.  The number of records contained within each datasets varies by several orders of magnitude, and without normalization the larger datasets render the smaller ones insignificant.

Median values cannot be used since many of the datasets have a majority of the cells with no data, so the median value is 0.

As a result, the mean was used to normalize the data.  The mean tessell value was calculated for each tesselated layer.

Next each tessellated cell was divided by the mean tessell value for that data layer, providing a normalized value.

# Aggregation

The points, multipoints, polylines and polygon tessellated shapefiles were first aggregated by the original geometry, then combined.  This results in a final tessellated shapefile with a total sum and normalized sum (REVISIT PER_SUM - FIX or REMOVE).


# Important Notes and Decisions to be Made

## Are we representing the data as it exists in the database, or are we trying to represent concrete things?

### Duplication

* Some data appears to be exact duplicates (ex. Community Sectors and Community Sectors Map both contain similar looking shapefiles). This is inconsistently done.  Should these both be included?
* Data records appear to have inconsistent treatment with regards to writing a new record versus replacing an original (example - sports surfaces - a single ball diamond has 200+ records associated with the space and surface of the shapefile, all geographically identical).  Should this be considered a single record, or multiple records?

### Data location shifting for privacy
* Several point geometry data layers have been shifted to a single location at the center of each community, likely due to privacy considerations. Examples include Licensed Pets and 311 Service Requests.  This means that each pet licensed in a neighbourhood gets a unique record in the dataset, and a unique count in the tessellation.  This results in neighbourhood brightspots that do not correspond to the actual location of those feautures and do not represent a real distribution.  Should these datasets be included since this is how the city is choosing to represent this data?  Or should these layers be discarded?

### Repetition of Polgyons

* Several data layers correspond to communities or municipal wards, such as census data.  As a result, any tessell cell that crosses one of those administrative boundaries gets a higher count.  In reality, we know that community level census data is spread throughout the region, and counting these layers does not truly represent more data within those cells.  


## Whose data are we trying to represent?
* There are several Statistics Canada layers in the datasets.  Should these be considered part of Calgary's data since they are on the Open Portal or should this be treated separately?


------------------------------------------

# Work In Progress/Next Steps

* Clean up json code to extract all desired categories (jsons are not consistent)
* Clean previously written code
* Develop a code that indicates presence or absence of data, not the counts

-------------------------------------------

# Personal Notes

* Binary data representation
* Frequency of updates - metadata
* Ephemeral vs permanent - data column headings? Possible manual separation
* Transportation data - check Innes
* Edmonton?

-----------------------------------------


# Scripts in the Repository:

Datadownloader.py - Code modified from R. Burns to bulk extract all data from the Open Calgary website (https://data.calgary.ca/)

OpenYYC_script_shapefile_extraction.py - Code to extract all of the shapefile data and move it into a single folder

OpenYYC_script_projection_foldercreation - Code to separate shapefiles into new folders based on geometry and project into the desired coordinate system

OpenYYC_Script_tesslation_calculations - Code to count the number of data points within a tesselated area, normalize with respect to the total for that specific dataset and then combine with all the other tesselated files to build an aggregate layer.

# Folders:

Old - Previous code snippits to be removed at a later date

Data - The tessellated shapefiles zipped


