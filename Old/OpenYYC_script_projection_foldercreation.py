
#-------------------------------------------------------------------------------
# Name:        Geog567 - Vector metadata and projections
# Purpose: To search a workspace containing vector data, provide projection
# details and assign a projection if missing
#
# Author:      T.Yeomans
#
# Created:     12-11-2020
#
#-------------------------------------------------------------------------------
#import the needed libraries
import arcpy
import os


#build a vector metadata class with useful properties defined.  They are all empty or zero
class vecMetadata:
    def __init__(self):
        self.fcs = []
        self.fccount = 0
        self.spatial_ref = ""

    #define a function to get the workspace from the user
    def getWorkspace(self):

        #Build a while loop to ask for a valid workspace location.  Keep looping until a valid location is provided
        while True:
            arcpy.env.workspace = (r"C:\OpenCalgary_project\Main_shapes")
            if arcpy.Exists(arcpy.env.workspace):
                print("Workspace location is valid\n")
                break
            else:
                print ("Workspace does not exist.  Please enter a valid workspace\n")


    #define a function to project each vector file in the workspace
    def projectVecdata (self):

        #use ListFeatureClasses and assign the list to a variable
        self.fcs = arcpy.ListFeatureClasses()

        #count the length of the list to get the number of vector files in the workspace and print to user
        self.fccount = len(self.fcs)
        print("Number of vector files in this location: " + str(self.fccount))


        #loop over every feature class in the folder
        for fc in self.fcs:
            geometries = arcpy.CopyFeatures_management(fc, arcpy.Geometry())
            self.spatial_ref = arcpy.Describe(fc).spatialReference

##            #if the spatial reference is unknown, let the user know that is was undefined, and assign it to a new projection
            if self.spatial_ref.name =="Unknown":
                print ("{}:Unknown Spatial Reference".format(fc))
                sr = arcpy.SpatialReference(3780)
                arcpy.DefineProjection_management(fc,sr)

            #if the file has a spatial reference already defined, project it to the new coordinate system
            else:
                desc = arcpy.Describe(fc)

                sr = arcpy.SpatialReference(3780)
                fc_proj = os.path.join(r"C:\OpenCalgary_project\Main_shapes_projected", os.path.splitext(fc)[0])
                arcpy.Project_management(fc, fc_proj, sr)
                print("{}".format(fc))

    #define a function to separate features classes into folders based on geometry
    def buildShapeFolders(self):

        #provide new workspace where the projected files are located
        arcpy.env.workspace = (r"C:\OpenCalgary_project\Main_shapes_projected")
        self.fcs = arcpy.ListFeatureClasses()

        for fc in self.fcs:
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


#instantiate the folderx object
folderx = vecMetadata()

#call the getVecdata method on folderx
folderx.getWorkspace()
folderx.projectVecdata()
folderx.buildShapeFolders()


