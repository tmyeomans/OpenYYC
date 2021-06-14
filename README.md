# OpenYYC Project - Distribution of Open Data in Calgary


# Workflow:

![OpenYYC Rough Workflow](https://user-images.githubusercontent.com/59377701/119421240-7bfcbf80-bcbb-11eb-8d8b-3e8bca066cad.png)


# Data Extraction

Data was extracted from the Open Calgary API using the Datadownloader.py code written by R. Burns and modified with RegEx to remove characters problematic for filenames and shapefiles.  The data was saved into a unique folder per dataset.

The data was extracted over a 48 hour period between November 21st and November 22nd 2020.  
Downloading had to be completed in multiple runs due to issues with the connection timing out, the initial request not identifying all data available, and errors associated with a particular data request (2016 Census of Canada - Top 5 Languages Spoken Most Often at Home by Ward).  After 48 hours the list of downloaded data was manually inspected and compared to the website.  Shapefiles that were absent were manually downloaded and added to the set.

Later on it was noted that large datasets such as the 311 Service Requests did not properly download due to the size of the file.  As a result, the file was manually downloaded, and data added after November 22nd 2020 was removed from the files.

In total 759 datasets were downloaded.  



# File Management

To make spatial data management easier, the shapefiles were extracted from the individual dataset folders into a common folder.  The filenames assigned by the city to the shapefiles are not in a useful format, so they needed to be renamed with the parent folder name.  After renaming and moving to a common folder, the shapefiles were then projected into the Alberta 3TM coordinate system.  To facilitate geometry dependent analysis and review, the shapefiles were saved to new folders based on whether they were points, multipoints, polylines or polygons.

# Tessellation 

Several tessellated shapefiles were created manually with the extent set to the City Boundary shapefile and visually compared.  A size of 0.5 square kilometers per hexagonal tessell was chosen as the host shapefile for the individual data counts.

A copy of the tessellated host layer was spatially joined to each dataset.  

* Points and multipoints were joined using 'completely contains'
* Polylines and polygons were joined using 'intersects'

This join process provides a join count per tessell cell.  These values are used later for a simple sum of all the data per tessell for all of the Open Calgary datasets.

The simple sum, as will be seen later, is insufficient to review the Open Calgary data.  The number of records contained within each datasets varies by several orders of magnitude, and without normalization the larger datasets render the smaller ones insignificant.

Median values cannot be used since many of the datasets have a majority of the cells with no data, so the median value is 0.

As a result, the mean was used to normalize the data.  The mean tessell value was calculated for each tesselated layer.

Next each tessellated cell value was divided by the mean tessell value for that data layer, providing a normalized value.

Each tessellated cell was also divided by the total count number and multiplied by 100, providing the percentage of the dataset that the specific tessell holds.

In addition to looking at the total data per tessellated cell, a binary value was extracted, showing each tessellated cell as having at least one data item (coded 1) or no data present (coded 0).


# Aggregation

The points, multipoints, polylines and polygon tessellated shapefiles were first aggregated by the original geometry, then combined.  This results in a final tessellated shapefile with a total sum, normalized sum and a binary sum.

--------------------------------------------------

# Total Dataset Results

The first image shows the total count distribution of data, with no normalization, and no data removed.  The impacts of large datasets with anonymized data assigned to community centerpoints is obvious as indicated by isolated bright islands of colour.

<img width="584" alt="All Data Count" src="https://user-images.githubusercontent.com/59377701/120252671-6d298600-c242-11eb-9c97-47060435fcad.png">

The following image also shows all the data, normalised to stop large datasets from consuming the analysis.

<img width="595" alt="All Data Normalized Sum" src="https://user-images.githubusercontent.com/59377701/120252766-ae219a80-c242-11eb-9d0d-5bb9c5ea73e5.png">

An alternative approach is shown below.  This map shows the binary sum.  In this example, each input cell was only recorded as having data or not.  Beyond whether it is present or not, the amount of data in each cell in this example is irrelevant.  The resulting data is then summed.

<img width="410" alt="All Data Binary Sum" src="https://user-images.githubusercontent.com/59377701/121898797-02b42380-cce1-11eb-84f6-c595a8de74d3.png">


--------------------------------------------------

# Aggregated City-Assigned Categories, Suspected Duplicates Removed

The following maps were created using the normalized total sum for each city assigned category.  Suspected duplicates of data, such as when the city had a 'dataset' and 'map' with the same name were removed.

Basemaps

![Basemaps](https://user-images.githubusercontent.com/59377701/120404881-8dba1480-c304-11eb-91f8-a64632365786.png)

--------------------------------------------------

Business and Economic Activity

![Business and Economic Activity](https://user-images.githubusercontent.com/59377701/120404903-9dd1f400-c304-11eb-967e-39045b05a3bb.png)


--------------------------------------------------

Demographics

<img width="356" alt="Demographics" src="https://user-images.githubusercontent.com/59377701/119430656-6775f280-bcce-11eb-9473-637a3342963d.png">

--------------------------------------------------

Environment

<img width="341" alt="Environment" src="https://user-images.githubusercontent.com/59377701/119430659-680e8900-bcce-11eb-8561-8730df6db3a2.png">

--------------------------------------------------

Government

![Government](https://user-images.githubusercontent.com/59377701/120404913-a5919880-c304-11eb-8ef0-8a027ac5647e.png)


--------------------------------------------------


Health and Safety

<img width="344" alt="Health and Safety" src="https://user-images.githubusercontent.com/59377701/119430660-68a71f80-bcce-11eb-8fa8-ffaed642a541.png">

--------------------------------------------------

Help and Information

<img width="338" alt="Help and Information" src="https://user-images.githubusercontent.com/59377701/119430662-68a71f80-bcce-11eb-887b-a4d0e1d77961.png">

--------------------------------------------------

Recreation and Culture

![Recreation and Culture](https://user-images.githubusercontent.com/59377701/120404526-cd343100-c303-11eb-8a9e-4a2ce1a74340.png)


--------------------------------------------------

Services and Amenities

<img width="410" alt="Services and Amenities" src="https://user-images.githubusercontent.com/59377701/119430667-69d84c80-bcce-11eb-8fca-96cc60218bae.png">

--------------------------------------------------

Transportation

<img width="405" alt="Transportation" src="https://user-images.githubusercontent.com/59377701/119430653-66dd5c00-bcce-11eb-8927-d7b9260bba62.png">

--------------------------------------------------

Null Category

<img width="400" alt="Null Category" src="https://user-images.githubusercontent.com/59377701/119430663-693fb600-bcce-11eb-8a14-45264cf492db.png">

--------------------------------------------------



# Important Notes and Decisions to be Made

## Are we representing the data as it exists in the database, or are we trying to represent intention?

### Duplication

* Some data appears to be exact duplicates (ex. Community Sectors and Community Sectors Map both contain similar looking shapefiles). This is inconsistently done.  Should these both be included?
* Data records appear to have inconsistent treatment with regards to writing a new record versus replacing an original (example - sports surfaces - a single ball diamond has 200+ records associated with the space and surface of the shapefile, all geographically identical).  Should this be considered a single record, or multiple records?  Most datasets do not do this, but editing these records is interfering within a dataset and is untenable at scale.

### Data location shifting for privacy
* Several point geometry data layers have been shifted to a single location at the center of each community, most likely due to privacy considerations. Examples include Licensed Pets and 311 Service Requests.  This means that each pet licensed in a neighbourhood gets a unique record in the dataset, and a unique count in the tessellation at exactly the community centroid location.  This results in neighbourhood brightspots that do not correspond to the actual location of those features and do not represent a real distribution.  Should these datasets be included since this is how the city is choosing to represent this data?  Or should these layers be discarded?

### Repetition of polgyons

* Several data layers correspond to communities or municipal wards, such as census data.  As a result, any tessell cell that crosses one of those administrative boundaries gets a higher count.  In reality, we know that community level census data is spread throughout the region, and counting these layers does not truly represent more data within those cells.  


## Statistics Canada data
* There are several Statistics Canada layers in the datasets.  Should these be considered part of Calgary's data since they are on the Open Portal and the city has decided to include them or should this be treated separately?


------------------------------------------

# Work In Progress/Next Steps

* City of Calgary has been contacted regarding which ward boundaries to use for 2016 Statscan data.  There was a major redrawing of ward boundaries in 2017, and there are inconsistencies between the graphics and written description on the Ward profiles on the city website 
* Review JSON code for opportunities - datasets are inconsistent in content and completion
* Decide what to do with dataset tags
* Build PDF scraper for Community profiles

-------------------------------------------

# Personal Notes

* Frequency of updates - metadata
* Ephemeral vs permanent - data column headings? Possible manual separation
* Transportation data - check Innes
* Smaller tessellation cells for binary data
* Edmonton?

-----------------------------------------


# Scripts in the Repository:

Datadownloader.py - Code modified from R. Burns to bulk extract all data from the Open Calgary website (https://data.calgary.ca/)

OpenYYC_script_shapefile_extraction.py - Code to extract all of the shapefile data and move it into a single folder

OpenYYC_script_projection_foldercreation - Code to separate shapefiles into new folders based on geometry and project into the desired coordinate system

OpenYYC_Script_tesslation_calculations - Code to count the number of data points within a tesselated area, normalize with respect to the total for that specific dataset and then combine with all the other tesselated files to build an aggregate layer.

OpenYYC_JSON_Reader - Code to extract metadata from each dataset


# Folders:

Old - Previous code snippits to be removed at a later date

Data - Contains the individual tesellated shapefiles, the total data aggregate tessell, and the aggregated category tessells. 


