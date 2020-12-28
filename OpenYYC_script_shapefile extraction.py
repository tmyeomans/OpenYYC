#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      rx99c
#
# Created:     12-12-2020
# Copyright:   (c) rx99c 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import re
import geopandas as gpd
import shutil
import matplotlib
import descartes


#create a class for the dataset extract  Properties are currently empty or zero
class dataDistribution:
    def __init__(self):
        self.vectorNames = []
        self.vectorFiles = []
        self.nonVectorData = []
        self.vectorPoints = []
        self.vectorLines = []
        self.vectorPolygons = []
        self.numPoints = 0
        self.numLines = 0
        self.numPolygons = 0
        self.numSpatial = 0
        self.numNonSpatial = 0


    #create a method to rename the files to acceptable shapefile names
    def renameFiles(self):

        #walk through the directory where the files are stored
        for root, dirs, files in os.walk(r"C:\OpenCalgary_project\Main_data"):

            #iterate over each item in all of the files
            for name in files:


                #assign the variable VecFilename to the parent folder name
                dirnames = root.split("\\")
                vecFilename = dirnames[-1]

                #Use regular expressions to remove characters unsuitable for shapefiles
                alphanum_vecname = re.sub(r"[-:%()]", "", vecFilename)
                clean_vecname = re.sub(r"[ ]", "_", alphanum_vecname)
                path =(os.path.join(root, name))

                #rename the vector file components from random IDs to the parent folder name. Append the shapfiles to the vectorFiles list
                if name.endswith('.shp'):
                    new_shape = os.rename(path, root + "\\" + clean_vecname + '.shp')

                elif name.endswith('.prj'):
                    new_proj = os.rename(path, root + "\\" + clean_vecname + '.prj')


                elif name.endswith('.dbf'):
                    new_dbf = os.rename(path, root + "\\" + clean_vecname + '.dbf')


                elif name.endswith('shx'):
                    new_shx = os.rename(path, root + "\\" + clean_vecname + '.shx')

                else:
                    pass


    #create a method to move the shapefiles from the original folders to a common folder
    def moveFiles(self):


        #walk through the directory where the files are stored
        for root, dirs, files in os.walk(r"C:\OpenCalgary_project\Main_data"):

            #iterate over each item in all of the files
            for name in files:

                #move the vector files components to the new location
                if name.endswith('.shp'):
                    shutil.copy(root + "\\" + name, r'C:\OpenCalgary_project\Main_shapes')

                elif name.endswith('.prj'):
                    shutil.copy(root + "\\" + name, r'C:\OpenCalgary_project\Main_shapes')

                elif name.endswith('.dbf'):
                    shutil.copy(root + "\\" + name, r'C:\OpenCalgary_project\Main_shapes')

                elif name.endswith('shx'):
                    shutil.copy(root + "\\" + name, r'C:\OpenCalgary_project\Main_shapes')

                else:
                    pass





    #create a method to get basic statistics from the data that has been moved
    def getStats(self):
        #walk through the directory where the new files are stored
        for root, dirs, files in os.walk(r'C:\OpenCalgary_project\Main_shapes'):
            #iterate over the files
            for name in files:
                #count the number of .shp files to determine how many individual shapefiles there are
                if name.endswith('.shp'):
                    #append the names to the vectorNames list
                    self.vectorNames.append(name)
                    #append the location to the vectorFiles List in case the full path is needed
                    self.vectorFiles.append(root + "\\" + name)

                else:
                    pass


        #count the length of the vectorFiles list to determine how many records there are
        self.numSpatial = len(self.vectorFiles)

        print (self.vectorNames)
        print (self.numSpatial)


##
##    def buildShapeLists(self):
##        for shape in self.vectorFiles:
##            gdf = gpd.read_file(shape)
##
##
##            points = gdf.loc[gdf['geometry']=='POLYGON']
##            points.plot();
######            print (gdf.head)
####
##
####            if 'geometry' == 'POINT':
##            self.vectorPoints.append(points)
##
##
##        self.numPoints = len(self.vectorPoints)
##        print(self.numPoints)

##            else:
##                pass


##            if data.geom_type == 'Points':
####            print (data.geom_type)
##
##                self.vectorPoints.append(shape)
##
##            else:
##                break

#instantiate the filex object
filex = dataDistribution()
#call the open method on filex
##filex.renameFiles()
##filex.moveFiles()
filex.getStats()



