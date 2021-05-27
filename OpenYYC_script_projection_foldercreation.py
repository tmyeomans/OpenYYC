
#-------------------------------------------------------------------------------
# Name:       OPENYYC_PROJECTION_FOLDER_CREATION
# Purpose:    Script to project Open YYC shapefiles and save into separate folders
#             based on shape geometry
# Author:     T.Yeomans
#
# Created:     20-12-2020
#
#-------------------------------------------------------------------------------
#Import the needed libraries
import arcpy
import os


#Define a function to get the workspace
def getWorkspace():
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Main_shapes")



#Define a function to project each vector file in the workspace
def projectVecdata ():

    #Use ListFeatureClasses and assign the list to a variable
    fcs = arcpy.ListFeatureClasses()

    #Count the length of the list to get the number of vector files in the workspace and print to user
    fccount = len(fcs)
    print("Number of vector files in this location: " + str(fccount))


    #loop over every feature class in the folder
    for fc in fcs:
        geometries = arcpy.CopyFeatures_management(fc, arcpy.Geometry())
        spatial_ref = arcpy.Describe(fc).spatialReference

      #If the spatial reference is unknown, let the user know that is was undefined, and assign it to a new projection
      #For Open Calgary data use EPSG 3780 - NAD83(CSRS) / Alberta 3TM ref merid 114 W
        if  spatial_ref.name =="Unknown":
            print ("{}:Unknown Spatial Reference".format(fc))
            sr = arcpy.SpatialReference(3780)
            arcpy.DefineProjection_management(fc,sr)

        #If the file has a spatial reference already defined, project it to the new coordinate system
        else:
            desc = arcpy.Describe(fc)

            sr = arcpy.SpatialReference(3780)
            fc_proj = os.path.join(r"C:\OpenCalgary_project\Main_shapes_projected", os.path.splitext(fc)[0])
            arcpy.Project_management(fc, fc_proj, sr)
            print("{}".format(fc))

#Define a function to separate features classes into folders based on geometry
def buildShapeFolders():

    #Provide new workspace where the projected files are located
    arcpy.env.workspace = (r"C:\OpenCalgary_project\Main_shapes_projected")
    fcs = arcpy.ListFeatureClasses()


    #loop over each feature class and add it to the appropriate folder based on geometry
    for fc in fcs:
        desc = arcpy.Describe(fc)
        if desc.shapeType == "Polygon":
            poly_outfc = (r"C:\OpenCalgary_project\OpenCalgary_polygons" + "\\" + fc)
            arcpy.CopyFeatures_management(fc, poly_outfc)


        if desc.shapeType == "Point":
            point_outfc = (r"C:\OpenCalgary_project\OpenCalgary_points" + "\\" + fc)
            arcpy.CopyFeatures_management(fc, point_outfc)

        if desc.shapeType == "Polyline":
            polyline_outfc = (r"C:\OpenCalgary_project\OpenCalgary_polylines" + "\\" + fc)
            arcpy.CopyFeatures_management(fc, polyline_outfc)

        if desc.shapeType == "Multipoint":
            multipoint_outfc = (r"C:\OpenCalgary_project\OpenCalgary_multipoint" + "\\" + fc)
            arcpy.CopyFeatures_management(fc, multipoint_outfc)

        else:
            pass


#Call the functions
getWorkspace()
projectVecdata()
buildShapeFolders()


