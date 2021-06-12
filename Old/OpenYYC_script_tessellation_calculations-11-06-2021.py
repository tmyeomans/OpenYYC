#-------------------------------------------------------------------------------
# Name:        OPENYYC_TESSELLATION_CALCULATIONS
# Purpose:     To count the number of feature class data points in a tessellation
#              and to build an aggregated tesselation with all of the data.
#
# Author:      T. Yeomans
#
# Created:     02-01-2021
# Notes:       Requires a tessellated shapefile that covers the area of interest
#              Contains separate functions for each geometry as well as a generic
#              function for bulk conversions.
#              *** Note - If additional large files are processed separate from this
#              script and need to be aggregated with the others, run the tessellate functions
#              on their own, add the tessellated data from the large files into the proper
#              folder, and then continue on to the join and combine functions
#-------------------------------------------------------------------------------
#Import the needed libraries
import arcpy
import os


#For large files like the 311 Service Requests in the Open Calgary repository the workspace has to be a geodatabase so this code will not work

#Build separate functions to spatially join points, multipoints, polylines and polygons to the input tessellation shapefile
#Constructs new shapefiles for each dataset

#Points and multipoints were joined using 'completely contains', polylines and polygons were joined using 'intersects'

#Define a function to tessellate the vectors with point geometries
def tessellatePoints():

    #Define the workspace where the point shapefiles are located
    arcpy.env.workspace = (r"C:\OpenCalgary_project\OpenCalgary_points")
    fcs = arcpy.ListFeatureClasses()

    #Iterate over all of the feature classes in the workspace
    for fc in fcs:

            #Provide a tessellation shapefile which will be joined to the data and will house the counts
            targetFC = (r"C:\OpenCalgary_project\Tessellation_05_km_All_Data.shp")
            joinFC = fc

            #Define a location to save the new point-based tessellated shapefiles
            outFC = (r"C:\OpenCalgary_project\Tessellation_points" + "\\TS_" + fc)

            #Join the input data layer to the tessellated shapefile.  For points use 'completely contains'
            joined_FC = arcpy.analysis.SpatialJoin(targetFC, joinFC, outFC, "join_one_to_one", "keep_all","", "completely_contains")

            #Comparing raw counts for datasets with large differences in count values leads to massive datasets consuming the analysis (example 311 Service Requests).
            #The following code works to divide each tessellation cell by the mean to allow for meaningful aggregation and comparissons between datasets.
            #While median values would better eliminate outliers, many of the datasets are dominated by tessellated cells with 0 count values, which is incompatible with the normalization.

            #Build a table to get the mean tessellated count value for each feature class. Provide a location to save these tables.
            in_table = joined_FC
            out_table = (r"C:\OpenCalgary_project\StatsTables" + "\\TS_Norm_" + fc)
            statsFields = [["Join_Count", "MEAN"]]
            statsTable = arcpy.analysis.Statistics(in_table, out_table, statsFields)

            #Assign the mean to a variable. Row 0 references the column MEAN_Join in the table
            mean_tess = 0
            with arcpy.da.SearchCursor(statsTable, "MEAN_Join_") as cursor:
                for row in cursor:
                    mean_tess += row[0]
                del cursor

            #Print the results to the screen as it iterates to visually quality check
            print(str(fc) + ": " + str(mean_tess))

            #Add a field for normalized count
            arcpy.AddField_management(in_table, "norm_ct", "FLOAT")

            #Use the update cursor to divide the Join_Count by the mean_tess variable and save the results to norm count
            with arcpy.da.UpdateCursor (in_table, ["Join_Count","norm_ct"]) as UC:

                for row in UC:
                    if mean_tess>0:
                        row[1] = row[0] / mean_tess
                        UC.updateRow(row)

                    else:
                        pass
            del UC

            #Code to determine the percent contribution of each tessellated cell to the total data count
            #Create a variable to contain the sum of all counts.  Note that this is different from the number of records, since a single shapefile could cross multiple tessellations
            sum_total = 0
            with arcpy.da.SearchCursor(in_table, "Join_Count") as cursor:
                for row in cursor:
                    sum_total = sum_total + row[0]

            #Add a field for the percent of the total dataset count
            arcpy.AddField_management(in_table, "perc_tot", "FLOAT")

            #If the tesselated cell count contains data, divide that cell by the sum total.  Multiply by 100 to get the percent and save that value
            with arcpy.da.UpdateCursor (in_table, ["Join_Count", "perc_tot"]) as UC:
                for row in UC:
                    if sum_total>0:
                        row[1] = (row[0] / sum_total) * 100
                        UC.updateRow(row)

                    else:
                        pass
            del UC

#Define a function to tessellate the vectors with multi-point geometries
def tessellateMultipoint():

    #Define the workspace where the multipoint shapefiles are located
    arcpy.env.workspace = (r"C:\OpenCalgary_project\OpenCalgary_multipoint")
    fcs = arcpy.ListFeatureClasses()

    #Iterate over all of the feature classes in the workspace
    for fc in fcs:

            #Provide a tessellation shapefile which will be joined to the data and will house the counts
            targetFC = (r"C:\OpenCalgary_project\Tessellation_05_km_All_Data.shp")
            joinFC = fc

            #Define a location to save the new multipoint-based tessellated shapefiles
            outFC = (r"C:\OpenCalgary_project\Tessellation_multipoint" + "\\TS_" + fc)

            #Join the input data layer to the tessellated shapefile.  For multipoints use 'completely contains'
            joined_FC = arcpy.analysis.SpatialJoin(targetFC, joinFC, outFC, "join_one_to_one", "keep_all","", "completely_contains")

            #Comparing raw counts for datasets with large differences in count values leads to massive datasets consuming the analysis (example 311 Service Requests).
            #The following code works to divide each tessellation cell by the mean to allow for meaningful aggregation and comparissons between datasets.
            #While median values would better eliminate outliers, many of the datasets are dominated by tessellated cells with 0 count values, which is incompatible with the normalization.


            #Build a table to get the mean tessellated count value for each feature class. Provide a location to save these tables.
            in_table = joined_FC
            out_table = (r"C:\OpenCalgary_project\StatsTables" + "\\TS_Norm_" + fc)
            statsFields = [["Join_Count", "MEAN"]]

            #Code to normalize by dividing each row by the mean of the total dataset
            #Calculate mean for each feature class
            statsTable = arcpy.analysis.Statistics(in_table, out_table, statsFields)

            #Assign the mean to a variable. Row 0 references the column MEAN_Join in the table
            mean_tess = 0
            with arcpy.da.SearchCursor(statsTable, "MEAN_Join_") as cursor:
                for row in cursor:
                    mean_tess += row[0]
                del cursor

            #Print the results to the screen as it iterates to visually quality check
            print(str(fc) + ": " + str(mean_tess))

            #Add a field for normalized count
            arcpy.AddField_management(in_table, "norm_ct", "FLOAT")

            #Use the update cursor to divide the Join_Count by the mean_tess variable and save the results to norm count
            with arcpy.da.UpdateCursor (in_table, ["Join_Count","norm_ct"]) as UC:

                for row in UC:
                    if mean_tess>0:
                        row[1] = row[0] / mean_tess
                        UC.updateRow(row)

                    else:
                        pass

            del UC

            #Code to determine the percent contribution of each tessellated cell to the total data count
            #Create a variable to contain the sum of all counts.  Note that this is different from the number of records, since a single shapefile could cross multiple tessellations
            sum_total = 0
            with arcpy.da.SearchCursor(in_table, "Join_Count") as cursor:
                for row in cursor:
                    sum_total = sum_total + row[0]

            #Add a field for the percent of the total dataset count
            arcpy.AddField_management(in_table, "perc_tot", "FLOAT")

            #If the tesselated cell count contains data, divide that cell by the sum total.  Multiply by 100 to get the percent and save that value
            with arcpy.da.UpdateCursor (in_table, ["Join_Count", "perc_tot"]) as UC:
                for row in UC:
                    if sum_total>0:
                        row[1] = (row[0] / sum_total) * 100
                        UC.updateRow(row)

                    else:
                        pass
            del UC

#Define a function to tessellate the vectors with polyline geometries
def tessellatePolylines():

    #Define the workspace where the polyline shapefiles are located
    arcpy.env.workspace = (r"C:\OpenCalgary_project\OpenCalgary_polylines")
    fcs = arcpy.ListFeatureClasses()

    #Iterate over all of the feature classes in the workspace
    for fc in fcs:

            #Provide a tessellation shapefile which will be joined to the data and will house the counts
            targetFC = (r"C:\OpenCalgary_project\Tessellation_05_km_All_Data.shp")
            joinFC = fc

            #Define a location to save the new polyline-based tessellated shapefiles
            outFC = (r"C:\OpenCalgary_project\Tessellation_polylines" + "\\TS_" + fc)

            #Join the input data layer to the tessellated shapefile.  For polylines use 'intersects'
            joined_FC = arcpy.analysis.SpatialJoin(targetFC, joinFC, outFC, "join_one_to_one", "keep_all","", "intersect")

            #Comparing raw counts for datasets with large differences in count values leads to massive datasets consuming the analysis (example 311 Service Requests).
            #The following code works to divide each tessellation cell by the mean to allow for meaningful aggregation and comparissons between datasets.
            #While median values would better eliminate outliers, many of the datasets are dominated by tessellated cells with 0 count values, which is incompatible with the normalization.

            #Build a table to get the mean tessellated count value for each feature class. Provide a location to save these tables.
            in_table = joined_FC
            out_table = (r"C:\OpenCalgary_project\StatsTables" + "\\TS_Norm_" + fc)
            statsFields = [["Join_Count", "MEAN"]]

            #Code to normalize by dividing each row by the mean of the total dataset
            #Calculate mean for each feature class
            statsTable = arcpy.analysis.Statistics(in_table, out_table, statsFields)

            #Assign the mean to a variable. Row 0 references the column MEAN_Join in the table
            mean_tess = 0
            with arcpy.da.SearchCursor(statsTable, "MEAN_Join_") as cursor:
                for row in cursor:
                    mean_tess += row[0]
                del cursor

            #Print the results to the screen as it iterates to visually quality check
            print(str(fc) + ": " + str(mean_tess))

            #Add a field for normalized count
            arcpy.AddField_management(in_table, "norm_ct", "FLOAT")

            #Use the update cursor to divide the Join_Count by the mean_tess variable and save the results to norm count
            with arcpy.da.UpdateCursor (in_table, ["Join_Count","norm_ct"]) as UC:

                for row in UC:
                    if mean_tess>0:
                        row[1] = row[0] / mean_tess
                        UC.updateRow(row)

                    else:
                        pass

            del UC

            #Code to determine the percent contribution of each tessellated cell to the total data count
            #Create a variable to contain the sum of all counts.  Note that this is different from the number of records, since a single shapefile could cross multiple tessellations
            sum_total = 0
            with arcpy.da.SearchCursor(in_table, "Join_Count") as cursor:
                for row in cursor:
                    sum_total = sum_total + row[0]

            #Add a field for the percent of the total dataset count
            arcpy.AddField_management(in_table, "perc_tot", "FLOAT")

            #If the tesselated cell count contains data, divide that cell by the sum total.  Multiply by 100 to get the percent and save that value
            with arcpy.da.UpdateCursor (in_table, ["Join_Count", "perc_tot"]) as UC:
                for row in UC:
                    if sum_total>0:
                        row[1] = (row[0] / sum_total) * 100
                        UC.updateRow(row)

                    else:
                        pass
            del UC

#Define a function to tessellate the vectors with polygon geometries
def tessellatePolygons():

    #Define the workspace where the polygon shapefiles are located
    arcpy.env.workspace = (r"C:\OpenCalgary_project\OpenCalgary_polygons")
    fcs = arcpy.ListFeatureClasses()

    #Iterate over all of the feature classes in teh workspace
    for fc in fcs:

            #Provide a tessellation shapefile which will be joined to the data and will house the counts
            targetFC = (r"C:\OpenCalgary_project\Tessellation_05_km_All_Data.shp")
            joinFC = fc

            #Define a location to save the new polygon-based tessellated shapefiles
            outFC = (r"C:\OpenCalgary_project\Tessellation_polygons" + "\\TS_" + fc)

            #Join the input data layer to the tessellated shapefile.  For polylines use 'intersects'
            joined_FC = arcpy.analysis.SpatialJoin(targetFC, joinFC, outFC, "join_one_to_one", "keep_all","", "intersect")

            #Comparing raw counts for datasets with large differences in count values leads to massive datasets consuming the analysis (example 311 Service Requests).
            #The following code works to divide each tessellation cell by the mean to allow for meaningful aggregation and comparissons between datasets.
            #While median values would better eliminate outliers, many of the datasets are dominated by tessellated cells with 0 count values, which is incompatible with the normalization.

            #Build a table to get the mean tessellated count value for each feature class. Provide a location to save these tables.
            in_table = joined_FC
            out_table = (r"C:\OpenCalgary_project\StatsTables" + "\\TS_Norm_" + fc)
            statsFields = [["Join_Count", "MEAN"]]

            #Code to normalize by dividing each row by the mean of the total dataset
            #Calculate mean for each feature class
            statsTable = arcpy.analysis.Statistics(in_table, out_table, statsFields)

            #Assign the mean to a variable. Row 0 references the column MEAN_Join in the table
            mean_tess = 0
            with arcpy.da.SearchCursor(statsTable, "MEAN_Join_") as cursor:
                for row in cursor:
                    mean_tess += row[0]
                del cursor

            #Print the results to the screen as it iterates to visually quality check
            print(str(fc) + ": " + str(mean_tess))

            #Add a field for normalized count
            arcpy.AddField_management(in_table, "norm_ct", "FLOAT")

            #Use the update cursor to divide the Join_Count by the mean_tess variable and save the results to norm count
            with arcpy.da.UpdateCursor (in_table, ["Join_Count","norm_ct"]) as UC:

                for row in UC:
                    if mean_tess>0:
                        row[1] = row[0] / mean_tess
                        UC.updateRow(row)

                    else:
                        pass
            del UC

            #Code to determine the percent contribution of each tessellated cell to the total data count
            #Create a variable to contain the sum of all counts.  Note that this is different from the number of records, since a single shapefile could cross multiple tessellations
            sum_total = 0
            with arcpy.da.SearchCursor(in_table, "Join_Count") as cursor:
                for row in cursor:
                    sum_total = sum_total + row[0]

            #Add a field for the percent of the total dataset count
            arcpy.AddField_management(in_table, "perc_tot", "FLOAT")

            #If the tesselated cell count contains data, divide that cell by the sum total.  Multiply by 100 to get the percent and save that value
            with arcpy.da.UpdateCursor (in_table, ["Join_Count", "perc_tot"]) as UC:
                for row in UC:
                    if sum_total>0:
                        row[1] = (row[0] / sum_total) * 100
                        UC.updateRow(row)

                    else:
                        pass
            del UC



def tessellateGeneric():

    #Define the workspace where the shapefiles are located
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Category\Government")
    fcs = arcpy.ListFeatureClasses()

    #Iterate over all of the feature classes in the workspace
    for fc in fcs:

            #Provide a tessellation shapefile which will be joined to the data and will house the counts
            targetFC = (r"C:\OpenCalgary_project\Tessellation_05_km_All_Data.shp")
            joinFC = fc

            #Define a location to save the new tessellated shapefiles
            outFC = (r"C:\OpenCalgary_project\Category\Government\outFC" + "\\TS_" + fc)

            #Join the input data layer to the tessellated shapefile.  For generic bulk processing use 'intersects'
            joined_FC = arcpy.analysis.SpatialJoin(targetFC, joinFC, outFC, "join_one_to_one", "keep_all","", "intersect")

            #Comparing raw counts for datasets with large differences in count values leads to massive datasets consuming the analysis (example 311 Service Requests).
            #The following code works to divide each tessellation cell by the mean to allow for meaningful aggregation and comparissons between datasets.
            #While median values would better eliminate outliers, many of the datasets are dominated by tessellated cells with 0 count values, which is incompatible with the normalization.

            #Build a table to get the mean tessellated count value for each feature class. Provide a location to save these tables.
            in_table = joined_FC
            out_table = (r"C:\OpenCalgary_project\StatsTables" + "\\TS_Norm_" + fc)
            statsFields = [["Join_Count", "MEAN"]]

            #Code to normalize by dividing each row by the mean of the total dataset
            #Calculate mean for each feature class
            statsTable = arcpy.analysis.Statistics(in_table, out_table, statsFields)

            #Assign the mean to a variable. Row 0 references the column MEAN_Join in the table
            mean_tess = 0
            with arcpy.da.SearchCursor(statsTable, "MEAN_Join_") as cursor:
                for row in cursor:
                    mean_tess += row[0]
                del cursor

            #Print the results to the screen as it iterates to visually quality check
            print(str(fc) + ": " + str(mean_tess))

            #Add a field for normalized count
            arcpy.AddField_management(in_table, "norm_ct", "FLOAT")

            #Use the update cursor to divide the Join_Count by the mean_tess variable and save the results to norm count
            with arcpy.da.UpdateCursor (in_table, ["Join_Count","norm_ct"]) as UC:

                for row in UC:
                    if mean_tess>0:
                        row[1] = row[0] / mean_tess
                        UC.updateRow(row)

                    else:
                        pass
            del UC

            #Code to determine the percent contribution of each tessellated cell to the total data count
            #Create a variable to contain the sum of all counts.  Note that this is different from the number of records, since a single shapefile could cross multiple tessellations
            sum_total = 0
            with arcpy.da.SearchCursor(in_table, "Join_Count") as cursor:
                for row in cursor:
                    sum_total = sum_total + row[0]

            #Add a field for the percent of the total dataset count
            arcpy.AddField_management(in_table, "perc_tot", "FLOAT")

            #If the tesselated cell count contains data, divide that cell by the sum total.  Multiply by 100 to get the percent and save that value
            with arcpy.da.UpdateCursor (in_table, ["Join_Count", "perc_tot"]) as UC:
                for row in UC:
                    if sum_total>0:
                        row[1] = (row[0] / sum_total) * 100
                        UC.updateRow(row)

                    else:
                        pass
            del UC


#The next series of functions adds a binary count in each tessell if data is present [1] or not [0]
#If you have done any tessellations using other methods, such as for large datasets, and not included counts those tessellated results should be added to the folders containing the Python constructed ones before moving to the next step.

def binaryTessellationPoint():

    #Define the workspace where the shapefiles are located
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Tessellation_points")
    fcs = arcpy.ListFeatureClasses()

    #Iterate over all of the feature classes in the workspace
    for fc in fcs:

        arcpy.AddField_management(fc, "Cont_data", "Short")

        in_table = fc



        with arcpy.da.UpdateCursor (in_table, ["Join_Count","Cont_data"]) as UC:

            for row in UC:
                if row[0] > 0:
                    row[1] = 1
                    UC.updateRow(row)

            else:
                pass
            del UC


def binaryTessellationMultipoint():

    #Define the workspace where the shapefiles are located
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Tessellation_multipoint")
    fcs = arcpy.ListFeatureClasses()

    #Iterate over all of the feature classes in the workspace
    for fc in fcs:

        arcpy.AddField_management(fc, "Cont_data", "Short")

        in_table = fc



        with arcpy.da.UpdateCursor (in_table, ["Join_Count","Cont_data"]) as UC:

            for row in UC:
                if row[0] > 0:
                    row[1] = 1
                    UC.updateRow(row)

            else:
                pass
            del UC



def binaryTessellationPolyline():

    #Define the workspace where the shapefiles are located
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Tessellation_polylines")
    fcs = arcpy.ListFeatureClasses()

    #Iterate over all of the feature classes in the workspace
    for fc in fcs:

        arcpy.AddField_management(fc, "Cont_data", "Short")

        in_table = fc



        with arcpy.da.UpdateCursor (in_table, ["Join_Count","Cont_data"]) as UC:

            for row in UC:
                if row[0] > 0:
                    row[1] = 1
                    UC.updateRow(row)

            else:
                pass
            del UC


def binaryTessellationPolyon():

    #Define the workspace where the shapefiles are located
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Tessellation_polygons")
    fcs = arcpy.ListFeatureClasses()

    #Iterate over all of the feature classes in the workspace
    for fc in fcs:

        arcpy.AddField_management(fc, "Cont_data", "Short")

        in_table = fc



        with arcpy.da.UpdateCursor (in_table, ["Join_Count","Cont_data"]) as UC:

            for row in UC:
                if row[0] > 0:
                    row[1] = 1
                    UC.updateRow(row)

            else:
                pass
            del UC

#If you have done any tessellations using other methods, such as for large datasets, those tessellated results should be added to the folders containing the Python constructed ones before moving to the next step.


#Build separate functions to aggregate the data from each geometry type into the host tessellation file.
def joinFieldPoints():

    #Add the workspace where your tessellated shapefiles containing point data resides
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Tessellation_points")
    fcs = arcpy.ListFeatureClasses()

    #Join the main tessellation to the feature classes with counts of data
    for fc in fcs:

        #Provide the main tessellation shapefile that will host the data
        inTessell = (r"C:\OpenCalgary_project\Tessellation_05_km_All_Data.shp")
        inJoinField = "GRID_ID"
        joinFC = fc
        joinFCField = "GRID_ID"
        fieldList = ["Join_Count","norm_ct"]

        #Add the count data to the main feature class
        arcpy.JoinField_management(inTessell, inJoinField, joinFC, joinFCField, fieldList)

        #Sum the count data in the main feature class then delete the joined column
        field = "Points_sum"
        expression = "!Points_sum! + !Join_Count!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "Join_Count")


        field = "Pt_nrm_sum"
        expression = "!Pt_nrm_sum! + !norm_ct!"

        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "norm_ct")


def joinFieldMultipoints():

    #Add the workspace where your tessellated shapefiles containing multipoint data resides
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Tessellation_multipoint")
    fcs = arcpy.ListFeatureClasses()

    #Join the main tessellation to the feature classes with counts of data
    for fc in fcs:

        #Provide the main tessellation shapefile that will host the data
        inTessell = (r"C:\OpenCalgary_project\Tessellation_05_km_All_Data.shp")
        inJoinField = "GRID_ID"
        joinFC = fc
        joinFCField = "GRID_ID"
        fieldList = ["Join_Count","norm_ct"]

        #Add the count data to the main feature class
        arcpy.JoinField_management(inTessell, inJoinField, joinFC, joinFCField, fieldList)

        #Sum the count data in the main feature class then delete the joined column
        field = "Mpoint_sum"
        expression = "!Mpoint_sum! + !Join_Count!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "Join_Count")

        field = "MPtnrm_sum"
        expression = "!MPtnrm_sum! + !norm_ct!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "norm_ct")


def joinFieldPolylines():

    #Add the workspace where your tessellated shapefiles containing polyline data resides
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Tessellation_polylines")
    fcs = arcpy.ListFeatureClasses()

    #Join the main tessellation to the feature classes with counts of data
    for fc in fcs:

        #Provide the main tessellation shapefile that will host the data
        inTessell = (r"C:\OpenCalgary_project\Tessellation_05_km_All_Data.shp")
        inJoinField = "GRID_ID"
        joinFC = fc
        joinFCField = "GRID_ID"
        fieldList = ["Join_Count","norm_ct"]

        #Add the count data to the main feature class
        arcpy.JoinField_management(inTessell, inJoinField, joinFC, joinFCField, fieldList)

        #Sum the count data in the main feature class then delete the joined column
        field = "Line_sum"
        expression = "!Line_sum! + !Join_Count!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "Join_Count")


        field = "Linnrm_sum"
        expression = "!Linnrm_sum! + !norm_ct!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "norm_ct")



def joinFieldPolygons():

    #Add the workspace where your tessellated shapefiles containing polygon data resides
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Tessellation_polygons")
    fcs = arcpy.ListFeatureClasses()

    #Join the main tessellation to the feature classes with counts of data
    for fc in fcs:

        #Provide the main tessellation shapefile that will host the data
        inTessell = (r"C:\OpenCalgary_project\Tessellation_05_km_All_Data.shp")
        inJoinField = "GRID_ID"
        joinFC = fc
        joinFCField = "GRID_ID"
        fieldList = ["Join_Count","norm_ct"]

        #Add the count data to the main feature class
        arcpy.JoinField_management(inTessell, inJoinField, joinFC, joinFCField, fieldList)

        #Sum the count data in the main feature class then delete the joined column
        field = "Poly_sum"
        expression = "!Poly_sum! + !Join_Count!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "Join_Count")


        field = "Polnrm_sum"
        expression = "!Polnrm_sum! + !norm_ct!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "norm_ct")


def joinFieldGeneric():

    #Add the workspace where your tessellated shapefiles containing data resides
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Category\Government\outFC")
    fcs = arcpy.ListFeatureClasses()

    #Join the main tessellation to the feature classes with counts of data
    for fc in fcs:

        #Provide the main tessellation shapefile that will host the data
        inTessell = (r"C:\OpenCalgary_project\Tessellation_05_km_All_Data.shp")
        inJoinField = "GRID_ID"
        joinFC = fc
        joinFCField = "GRID_ID"
        fieldList = ["Join_Count","norm_ct"]

        #Add the count data to the main feature class
        arcpy.JoinField_management(inTessell, inJoinField, joinFC, joinFCField, fieldList)

        #Sum the count data in the main feature class then delete the joined column
        field = "Shape_sum"
        expression = "!Shape_sum! + !Join_Count!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "Join_Count")


        field = "Shpnrm_sum"
        expression = "!Shpnrm_sum! + !norm_ct!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "norm_ct")



#Sum the results from each shapefile geometery for each category into a new field
def combineShapes():
    #Provide the main tessellation shapefile from the previous step that will host the data
    inTessell = (r"C:\OpenCalgary_project\Tessellation_05_km_All_Data.shp")


#Check to see if all the fields exist before summing.  If not add empty placeholder columns
    fieldlist = arcpy.ListFields(inTessell)

    if "Points_sum" in fieldlist:
        print ("Points present in datasets")
    else:
        arcpy.management.AddFields(inTessell, [["Points_sum", "FLOAT"], ["Pt_nrm_sum", 'FLOAT']])


    if "Mpoint_sum" in fieldlist:
        print ("Points present in datasets")
    else:
        arcpy.management.AddFields(inTessell, [["Mpoint_sum", "FLOAT"], ["MPtnrm_sum", 'FLOAT']])



    if "Line_sum" in fieldlist:
        print ("Points present in datasets")
    else:
        arcpy.management.AddFields(inTessell, [["Line_sum", "FLOAT"], ["Linnrm_sum", 'FLOAT'] ])


    if "Poly_sum" in fieldlist:
        print ("Points present in datasets")
    else:
        arcpy.management.AddFields(inTessell, [["Poly_sum", "FLOAT"], ["Polnrm_sum", 'FLOAT'] ])



    field = "Count"
    expression = "!Points_sum! + !Mpoint_sum! + !Line_sum! + !Poly_sum!"
    arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")


    field = "Nrm_sum"
    expression = "!Pt_nrm_sum! + !MPtnrm_sum! + !Linnrm_sum! + !Polnrm_sum!"
    arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")






##tessellatePoints()
##tessellateMultipoint()
##tessellatePolylines()
##tessellatePolygons()


#Shortened code for a single folder
##tessellateGeneric()
##joinFieldGeneric()
##
binaryTessellationPoint()
binaryTessellationMultipoint()
binaryTessellationPolyline()
binaryTessellationPolyon()

##
##joinFieldPoints()
##joinFieldMultipoints()
##joinFieldPolylines()
##joinFieldPolygons()
##
##
##combineShapes()