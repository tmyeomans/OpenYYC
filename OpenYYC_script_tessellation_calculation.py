#-------------------------------------------------------------------------------
# Name:        OPENYYC_TESSELLATION_CALCULATIONS
# Purpose:     To count the number of feature class data points in a tessellation
#
# Author:      T. Yeomans
#
# Created:     02-01-2021
# Notes:       Requires a tessellated shapefile with numeric fields defined
#              for the points, multipoints, polylines and polygons
#-------------------------------------------------------------------------------
#import the needed libraries
import arcpy
import os


#build separate functions to spatially join points, multipoints, polylines and polygons to the input tessellation shapefile
#points and multipoints were joined using 'completely contains', polylines and polygons were joined using 'intersects'
#builds new shapefiles for each dataset

def tessellatePoints():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\OpenCalgary_points")
    fcs = arcpy.ListFeatureClasses()

    for fc in fcs:

            targetFC = (r"C:\OpenCalgary_project\Base_files\Tessellation_1km.shp")
            joinFC = fc
            outFC = (r"C:\OpenCalgary_project\Tessellation_points" + "\\TS_" + fc)
            arcpy.analysis.SpatialJoin(targetFC, joinFC, outFC, "join_one_to_one", "keep_all","", "completely_contains")




def tessellateMultipoint():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\OpenCalgary_multipoint")
    fcs = arcpy.ListFeatureClasses()

    for fc in fcs:

            targetFC = (r"C:\OpenCalgary_project\Base_files\Tessellation_1km.shp")
            joinFC = fc
            outFC = (r"C:\OpenCalgary_project\Tessellation_multipoint" + "\\TS_" + fc)
            arcpy.analysis.SpatialJoin(targetFC, joinFC, outFC, "join_one_to_one", "keep_all","", "completely_contains")




def tessellatePolylines():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\OpenCalgary_polylines")
    fcs = arcpy.ListFeatureClasses()

    for fc in fcs:

            targetFC = (r"C:\OpenCalgary_project\Base_files\Tessellation_1km.shp")
            joinFC = fc
            outFC = (r"C:\OpenCalgary_project\Tessellation_polylines" + "\\TS_" + fc)
            arcpy.analysis.SpatialJoin(targetFC, joinFC, outFC, "join_one_to_one", "keep_all","", "intersect")



def tessellatePolygons():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\OpenCalgary_polygons")
    fcs = arcpy.ListFeatureClasses()

    for fc in fcs:

            targetFC = (r"C:\OpenCalgary_project\Base_files\Tessellation_1km.shp")
            joinFC = fc
            outFC = (r"C:\OpenCalgary_project\Tessellation_polygons" + "\\TS_" + fc)
            arcpy.analysis.SpatialJoin(targetFC, joinFC, outFC, "join_one_to_one", "keep_all","", "intersect")


#build separate functions to join the spatially joined dataset which contains the join count data to the original tessellated input shapefile
#ensure that your input base tessellation has numeric fields for Points_sum, Mpoint_sum, Line_sum and Poly_sum

def joinFieldPoints():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Tessellation_points")
    fcs = arcpy.ListFeatureClasses()
    #join the main tessellation to the feature classes with counts of data
    for fc in fcs:
        inTessell = (r"C:\OpenCalgary_project\Base_files\Tessellation_1km_main_test.shp")
        inJoinField = "GRID_ID"
        joinFC = fc
        joinFCField = "GRID_ID"
        fieldList = "Join_Count"

        #add the count data to the main feature class
        arcpy.JoinField_management(inTessell, inJoinField, joinFC, joinFCField, fieldList)

        #sum the count data in the main feature class then delete the joined column
        field = "Points_sum"
        expression = "!Points_sum! + !Join_Count!"

        arcpy.CalculateField_management(inTessell, field, expression)
        arcpy.management.DeleteField(inTessell, "Join_Count")

def joinFieldMultipoints():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Tessellation_multipoint")
    fcs = arcpy.ListFeatureClasses()
    #join the main tessellation to the feature classes with counts of data
    for fc in fcs:
        inTessell = (r"C:\OpenCalgary_project\Base_files\Tessellation_1km_main_test.shp")
        inJoinField = "GRID_ID"
        joinFC = fc
        joinFCField = "GRID_ID"
        fieldList = "Join_Count"

        #add the count data to the main feature class
        arcpy.JoinField_management(inTessell, inJoinField, joinFC, joinFCField, fieldList)

        #sum the count data in the main feature class then delete the joined column
        field = "Mpoint_sum"
        expression = "!Mpoint_sum! + !Join_Count!"

        arcpy.CalculateField_management(inTessell, field, expression)
        arcpy.management.DeleteField(inTessell, "Join_Count")


def joinFieldPolylines():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Tessellation_polylines")
    fcs = arcpy.ListFeatureClasses()
    #join the main tessellation to the feature classes with counts of data
    for fc in fcs:
        inTessell = (r"C:\OpenCalgary_project\Base_files\Tessellation_1km_main_test.shp")
        inJoinField = "GRID_ID"
        joinFC = fc
        joinFCField = "GRID_ID"
        fieldList = "Join_Count"

        #add the count data to the main feature class
        arcpy.JoinField_management(inTessell, inJoinField, joinFC, joinFCField, fieldList)

        #sum the count data in the main feature class then delete the joined column
        field = "Line_sum"
        expression = "!Line_sum! + !Join_Count!"

        arcpy.CalculateField_management(inTessell, field, expression)
        arcpy.management.DeleteField(inTessell, "Join_Count")




def joinFieldPolygons():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Tessellation_polygons")
    fcs = arcpy.ListFeatureClasses()
    #join the main tessellation to the feature classes with counts of data
    for fc in fcs:
        inTessell = (r"C:\OpenCalgary_project\Base_files\Tessellation_1km_main_test.shp")
        inJoinField = "GRID_ID"
        joinFC = fc
        joinFCField = "GRID_ID"
        fieldList = "Join_Count"

        #add the count data to the main feature class
        arcpy.JoinField_management(inTessell, inJoinField, joinFC, joinFCField, fieldList)

        #sum the count data in the main feature class then delete the joined column
        field = "Poly_sum"
        expression = "!Poly_sum! + !Join_Count!"

        arcpy.CalculateField_management(inTessell, field, expression)
        arcpy.management.DeleteField(inTessell, "Join_Count")

#manually sum the columns after to determine the total sum

getWorkspace()
tessellatePoints()
tessellateMultipoint()
tessellatePolylines()
tessellatePolygons()


joinFieldPoints()
joinFieldMultipoints()
joinFieldPolylines()
joinFieldPolygons()