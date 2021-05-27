#-------------------------------------------------------------------------------
# Name:      OPENYYC_SHAPEFILE_EXTRACTION
# Purpose:   Script to rename Open YYC shapefiles and save from multiple folder
#            locations into a folder only contianing shapefiles
#
# Author:      T. Yeomans
#
# Created:     12-12-2020

#-------------------------------------------------------------------------------
#Import libraries
import os
import re
import shutil




#Create a class for the dataset extract  Properties are currently empty or zero
class dataDistribution:
    def __init__(self):
        self.vectorNames = []
        self.vectorFiles = []
        self.numSpatial = 0



    #Create a method to rename the files to acceptable shapefile names without spaces or special characters
    def renameFiles(self):

        #Walk through the directory where the files are stored
        for root, dirs, files in os.walk(r"C:\OpenCalgary_project\Main_data"):

            #Iterate over each item in all of the files
            for name in files:


                #Assign the variable VecFilename to the parent folder name
                dirnames = root.split("\\")
                vecFilename = dirnames[-1]

                #Use regular expressions to remove characters unsuitable for shapefiles
                alphanum_vecname = re.sub(r"[-:%()]", "", vecFilename)
                clean_vecname = re.sub(r"[ ]", "_", alphanum_vecname)
                path =(os.path.join(root, name))

                #Rename the vector file components from random IDs to the parent folder name. Append the shapfiles to the vectorFiles list
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


    #Create a method to move the shapefiles from the original folders to a common folder
    def moveFiles(self):


        #Walk through the directory where the files are stored
        for root, dirs, files in os.walk(r"C:\OpenCalgary_project\Main_data"):

            #Iterate over each item in all of the files
            for name in files:

                #Move the vector files components to the new location
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





    #Create a method to get basic statistics from the data that has been moved
    def getStats(self):
        #Walk through the directory where the new files are stored
        for root, dirs, files in os.walk(r'C:\OpenCalgary_project\Main_shapes'):
            #Iterate over the files
            for name in files:
                #Count the number of .shp files to determine how many individual shapefiles there are
                if name.endswith('.shp'):
                    #Append the names to the vectorNames list
                    self.vectorNames.append(name)
                    #Append the location to the vectorFiles List in case the full path is needed
                    self.vectorFiles.append(root + "\\" + name)

                else:
                    pass


        #Count the length of the vectorFiles list to determine how many records there are
        self.numSpatial = len(self.vectorFiles)

        print (self.vectorNames)
        print (self.numSpatial)



#Instantiate the filex object
filex = dataDistribution()

#Call the open method on filex
filex.renameFiles()
filex.moveFiles()
filex.getStats()



