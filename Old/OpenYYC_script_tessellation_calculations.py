#-------------------------------------------------------------------------------
# Name:        OPENYYC_TESSELLATION_CALCULATIONS
# Purpose:     To count the number of feature class data points in a tessellation
#
# Author:      T. Yeomans
#
# Created:     02-01-2021
# Notes:       Requires a tessellated shapefile
#-------------------------------------------------------------------------------
#import the needed libraries
import arcpy
import os


#build separate functions to spatially join points, multipoints, polylines and polygons to the input tessellation shapefile
#points and multipoints were joined using 'completely contains', polylines and polygons were joined using 'intersects'
#builds new shapefiles for each dataset

def tessellatePoints():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Pilot\Pilot_test.gdb")
    fcs = arcpy.ListFeatureClasses()

    for fc in fcs:

            targetFC = (r"C:\OpenCalgary_project\Test_normalization\Tess_05.shp")
            joinFC = fc
            outFC = (r"C:\OpenCalgary_project\Test_normalization\Tess_points" + "\\TS_" + fc)

            joined_FC = arcpy.analysis.SpatialJoin(targetFC, joinFC, outFC, "join_one_to_one", "keep_all","", "completely_contains")


#### PERSONAL NOTE - NEED TO EXPORT THIS SHAPEFILE TO A FEATURE CLASS IN A GEODATABASE TO NULL THE POINTS
###  SHOULDN'T NULL - REAL ZEROS?  USE AVERAGE INSTEAD
# Note - if you use arcpy.Statistics_analysis() there is no option for median statistics
# Use arcpy.analysis.Statistics instead

            in_table = joined_FC
            out_table = (r"C:\OpenCalgary_project\Test_normalization" + "\\TS_Norm_" + fc)
            statsFields = [["Join_Count", "MEAN"]]

#### Code to normalize by dividing each row by the mean of the total dataset
# Calculate mean for each feature class
            statsTable = arcpy.analysis.Statistics(in_table, out_table, statsFields)

# Assign the mean to a variable. Row 0 reference the column MEAN_Join in the table
            mean_tess = 0
            with arcpy.da.SearchCursor(statsTable, "MEAN_Join_") as cursor:
                for row in cursor:
                    mean_tess += row[0]
                del cursor

# Print the results to the screen as it iterates to visually quality check
            print(str(fc) + ": " + str(mean_tess))

# Add a field for normalized count
            arcpy.AddField_management(in_table, "norm_ct", "FLOAT")

# Use the update cursor to divide the Join_Count by the mean_tess variable and save the results to norm count
            with arcpy.da.UpdateCursor (in_table, ["Join_Count","norm_ct"]) as UC:

                for row in UC:
                    if mean_tess>0:
                        row[1] = row[0] / mean_tess
                        UC.updateRow(row)

                    else:
                        pass
            del UC

#### Code to normalize by dividing each row by the count of the total dataset

            sum_total = 0
            with arcpy.da.SearchCursor(in_table, "Join_Count") as cursor:
                for row in cursor:
                    sum_total = sum_total + row[0]

            arcpy.AddField_management(in_table, "perc_tot", "FLOAT")

            with arcpy.da.UpdateCursor (in_table, ["Join_Count", "perc_tot"]) as UC:
                for row in UC:
                    if sum_total>0:
                        row[1] = (row[0] / sum_total) * 100
                        UC.updateRow(row)

                    else:
                        pass
            del UC


def tessellateMultipoint():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\OpenCalgary_multipoint")
    fcs = arcpy.ListFeatureClasses()

    for fc in fcs:

            targetFC = (r"C:\OpenCalgary_project\Test_normalization\Tess_05.shp")
            joinFC = fc
            outFC = (r"C:\OpenCalgary_project\Test_normalization\Tess_mpoints" + "\\TS_" + fc)
            joined_FC = arcpy.analysis.SpatialJoin(targetFC, joinFC, outFC, "join_one_to_one", "keep_all","", "completely_contains")

            in_table = joined_FC
            out_table = (r"C:\OpenCalgary_project\Test_normalization" + "\\TS_Norm_" + fc)
            statsFields = [["Join_Count", "MEAN"]]

#### Code to normalize by dividing each row by the mean of the total dataset
# Calculate mean for each feature class
            statsTable = arcpy.analysis.Statistics(in_table, out_table, statsFields)

# Assign the mean to a variable. Row 0 reference the column MEAN_Join in the table
            mean_tess = 0
            with arcpy.da.SearchCursor(statsTable, "MEAN_Join_") as cursor:
                for row in cursor:
                    mean_tess += row[0]
                del cursor

# Print the results to the screen as it iterates to visually quality check
            print(str(fc) + ": " + str(mean_tess))

# Add a field for normalized count
            arcpy.AddField_management(in_table, "norm_ct", "FLOAT")

# Use the update cursor to divide the Join_Count by the mean_tess variable and save the results to norm count
            with arcpy.da.UpdateCursor (in_table, ["Join_Count","norm_ct"]) as UC:

                for row in UC:
                    if mean_tess>0:
                        row[1] = row[0] / mean_tess
                        UC.updateRow(row)

                    else:
                        pass

            del UC

#### Code to normalize by dividing each row by the count of the total dataset

            sum_total = 0
            with arcpy.da.SearchCursor(in_table, "Join_Count") as cursor:
                for row in cursor:
                    sum_total = sum_total + row[0]

            arcpy.AddField_management(in_table, "perc_tot", "FLOAT")

            with arcpy.da.UpdateCursor (in_table, ["Join_Count", "perc_tot"]) as UC:
                for row in UC:
                    if sum_total>0:
                        row[1] = (row[0] / sum_total) * 100
                        UC.updateRow(row)

                    else:
                        pass
            del UC


def tessellatePolylines():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\OpenCalgary_polylines")
    fcs = arcpy.ListFeatureClasses()

    for fc in fcs:

            targetFC = (r"C:\OpenCalgary_project\Test_normalization\Tess_05.shp")
            joinFC = fc
            outFC = (r"C:\OpenCalgary_project\Test_normalization\Tess_Line" + "\\TS_" + fc)
            joined_FC = arcpy.analysis.SpatialJoin(targetFC, joinFC, outFC, "join_one_to_one", "keep_all","", "intersect")

            in_table = joined_FC
            out_table = (r"C:\OpenCalgary_project\Test_normalization" + "\\TS_Norm_" + fc)
            statsFields = [["Join_Count", "MEAN"]]

#### Code to normalize by dividing each row by the mean of the total dataset
# Calculate mean for each feature class
            statsTable = arcpy.analysis.Statistics(in_table, out_table, statsFields)

# Assign the mean to a variable. Row 0 reference the column MEAN_Join in the table
            mean_tess = 0
            with arcpy.da.SearchCursor(statsTable, "MEAN_Join_") as cursor:
                for row in cursor:
                    mean_tess += row[0]
                del cursor

# Print the results to the screen as it iterates to visually quality check
            print(str(fc) + ": " + str(mean_tess))

# Add a field for normalized count
            arcpy.AddField_management(in_table, "norm_ct", "FLOAT")

# Use the update cursor to divide the Join_Count by the mean_tess variable and save the results to norm count
            with arcpy.da.UpdateCursor (in_table, ["Join_Count","norm_ct"]) as UC:

                for row in UC:
                    if mean_tess>0:
                        row[1] = row[0] / mean_tess
                        UC.updateRow(row)

                    else:
                        pass

            del UC

#### Code to normalize by dividing each row by the count of the total dataset

            sum_total = 0
            with arcpy.da.SearchCursor(in_table, "Join_Count") as cursor:
                for row in cursor:
                    sum_total = sum_total + row[0]

            arcpy.AddField_management(in_table, "perc_tot", "FLOAT")

            with arcpy.da.UpdateCursor (in_table, ["Join_Count", "perc_tot"]) as UC:
                for row in UC:
                    if sum_total>0:
                        row[1] = (row[0] / sum_total) * 100
                        UC.updateRow(row)

                    else:
                        pass
            del UC


def tessellatePolygons():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\OpenCalgary_polygons")
    fcs = arcpy.ListFeatureClasses()

    for fc in fcs:

            targetFC = (r"C:\OpenCalgary_project\Test_normalization\Tess_05.shp")
            joinFC = fc
            outFC = (r"C:\OpenCalgary_project\Test_normalization\Tess_polygon" + "\\TS_" + fc)
            joined_FC = arcpy.analysis.SpatialJoin(targetFC, joinFC, outFC, "join_one_to_one", "keep_all","", "intersect")

            in_table = joined_FC
            out_table = (r"C:\OpenCalgary_project\Test_normalization" + "\\TS_Norm_" + fc)
            statsFields = [["Join_Count", "MEAN"]]

#### Code to normalize by dividing each row by the mean of the total dataset
# Calculate mean for each feature class
            statsTable = arcpy.analysis.Statistics(in_table, out_table, statsFields)

# Assign the mean to a variable. Row 0 reference the column MEAN_Join in the table
            mean_tess = 0
            with arcpy.da.SearchCursor(statsTable, "MEAN_Join_") as cursor:
                for row in cursor:
                    mean_tess += row[0]
                del cursor

# Print the results to the screen as it iterates to visually quality check
            print(str(fc) + ": " + str(mean_tess))

# Add a field for normalized count
            arcpy.AddField_management(in_table, "norm_ct", "FLOAT")

# Use the update cursor to divide the Join_Count by the mean_tess variable and save the results to norm count
            with arcpy.da.UpdateCursor (in_table, ["Join_Count","norm_ct"]) as UC:

                for row in UC:
                    if mean_tess>0:
                        row[1] = row[0] / mean_tess
                        UC.updateRow(row)

                    else:
                        pass
            del UC

#### Code to normalize by dividing each row by the count of the total dataset

            sum_total = 0
            with arcpy.da.SearchCursor(in_table, "Join_Count") as cursor:
                for row in cursor:
                    sum_total = sum_total + row[0]

            arcpy.AddField_management(in_table, "perc_tot", "FLOAT")

            with arcpy.da.UpdateCursor (in_table, ["Join_Count", "perc_tot"]) as UC:
                for row in UC:
                    if sum_total>0:
                        row[1] = (row[0] / sum_total) * 100
                        UC.updateRow(row)

                    else:
                        pass
            del UC



#build separate functions to join the spatially joined dataset which contains the join count data to the original tessellated input shapefile

def joinFieldPoints():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Test_normalization\Tess_points")
    fcs = arcpy.ListFeatureClasses()
    #join the main tessellation to the feature classes with counts of data


    for fc in fcs:
        inTessell = (r"C:\OpenCalgary_project\Test_normalization\Tess_05.shp")
        inJoinField = "GRID_ID"
        joinFC = fc
        joinFCField = "GRID_ID"
        fieldList = ["Join_Count","norm_ct","perc_tot"]

        #add the count data to the main feature class
        arcpy.JoinField_management(inTessell, inJoinField, joinFC, joinFCField, fieldList)

        #sum the count data in the main feature class then delete the joined column
        field = "Points_sum"
        expression = "!Points_sum! + !Join_Count!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "Join_Count")


        field = "Pt_nrm_sum"
        expression = "!Pt_nrm_sum! + !norm_ct!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "norm_ct")


        field = "Pt_per_sum"
        expression = "!Pt_per_sum! + !perc_tot!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "perc_tot")



def joinFieldMultipoints():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Test_normalization\Tess_mpoints")
    fcs = arcpy.ListFeatureClasses()
    #join the main tessellation to the feature classes with counts of data
    for fc in fcs:
        inTessell = (r"C:\OpenCalgary_project\Test_normalization\Tess_05.shp")
        inJoinField = "GRID_ID"
        joinFC = fc
        joinFCField = "GRID_ID"
        fieldList = ["Join_Count","norm_ct","perc_tot"]

        #add the count data to the main feature class
        arcpy.JoinField_management(inTessell, inJoinField, joinFC, joinFCField, fieldList)

        #sum the count data in the main feature class then delete the joined column
        field = "Mpoint_sum"
        expression = "!Mpoint_sum! + !Join_Count!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "Join_Count")

        field = "MPtnrm_sum"
        expression = "!MPtnrm_sum! + !norm_ct!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "norm_ct")

        field = "MPtper_sum"
        expression = "!MPtper_sum! + !perc_tot!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "perc_tot")


def joinFieldPolylines():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Test_normalization\Tess_Line")
    fcs = arcpy.ListFeatureClasses()
    #join the main tessellation to the feature classes with counts of data
    for fc in fcs:
        inTessell = (r"C:\OpenCalgary_project\Test_normalization\Tess_05.shp")
        inJoinField = "GRID_ID"
        joinFC = fc
        joinFCField = "GRID_ID"
        fieldList = ["Join_Count","norm_ct","perc_tot"]

        #add the count data to the main feature class
        arcpy.JoinField_management(inTessell, inJoinField, joinFC, joinFCField, fieldList)

        #sum the count data in the main feature class then delete the joined column
        field = "Line_sum"
        expression = "!Line_sum! + !Join_Count!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "Join_Count")


        field = "Linnrm_sum"
        expression = "!Linnrm_sum! + !norm_ct!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "norm_ct")


        field = "Linper_sum"
        expression = "!Linper_sum! + !perc_tot!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "perc_tot")


def joinFieldPolygons():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Test_normalization\Tess_polygon")
    fcs = arcpy.ListFeatureClasses()
    #join the main tessellation to the feature classes with counts of data
    for fc in fcs:
        inTessell = (r"C:\OpenCalgary_project\Test_normalization\Tess_05.shp")
        inJoinField = "GRID_ID"
        joinFC = fc
        joinFCField = "GRID_ID"
        fieldList = ["Join_Count","norm_ct","perc_tot"]

        #add the count data to the main feature class
        arcpy.JoinField_management(inTessell, inJoinField, joinFC, joinFCField, fieldList)

        #sum the count data in the main feature class then delete the joined column
        field = "Poly_sum"
        expression = "!Poly_sum! + !Join_Count!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "Join_Count")


        field = "Polnrm_sum"
        expression = "!Polnrm_sum! + !norm_ct!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "norm_ct")


        field = "Polper_sum"
        expression = "!Polper_sum! + !perc_tot!"
        arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")
        arcpy.management.DeleteField(inTessell, "perc_tot")



# sum the results from each shapefile geometery for each category into a new field
def combineShapes():


# Check to see if all the fields exist before summing.  If not add empty columns

    fieldlist = arcpy.ListFields(inTessell)

    if "Points_sum" in fieldlist:
        print ("Points present in datasets")
    else:
        arcpy.management.AddFields(inTessell, [["Points_sum", "FLOAT"], ["Pt_nrm_sum", 'FLOAT'],["Pt_per_sum", "FLOAT"] ])


    if "Mpoint_sum" in fieldlist:
        print ("Points present in datasets")
    else:
        arcpy.management.AddFields(inTessell, [["Mpoint_sum", "FLOAT"], ["MPtnrm_sum", 'FLOAT'],["MPtper_sum", "FLOAT"] ])



    if "Line_sum" in fieldlist:
        print ("Points present in datasets")
    else:
        arcpy.management.AddFields(inTessell, [["Line_sum", "FLOAT"], ["Linnrm_sum", 'FLOAT'],["Linper_sum", "FLOAT"] ])


    if "Poly_sum" in fieldlist:
        print ("Points present in datasets")
    else:
        arcpy.management.AddFields(inTessell, [["Poly_sum", "FLOAT"], ["Polnrm_sum", 'FLOAT'],["Polper_sum", "FLOAT"] ])





    inTessell = (r"C:\OpenCalgary_project\Test_normalization\Tess_05.shp")


    field = "Count"
    expression = "!Points_sum! + !Mpoint_sum! + !Line_sum! + !Poly_sum!"
    arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")


    field = "Nrm_sum"
    expression = "!Pt_nrm_sum! + !MPtnrm_sum! + !Linnrm_sum! + !Polnrm_sum!"
    arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")


    field = "Per_sum"
    expression = "!Pt_per_sum! + !MPtper_sum! + !Linper_sum! + !Polper_sum!"
    arcpy.CalculateField_management(inTessell, field, expression, "", "", "FLOAT")



tessellatePoints()
tessellateMultipoint()
tessellatePolylines()
tessellatePolygons()


joinFieldPoints()
joinFieldMultipoints()
joinFieldPolylines()
joinFieldPolygons()

combineShapes()