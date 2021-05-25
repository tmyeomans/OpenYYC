#-------------------------------------------------------------------------------
# Name:        OPENYYC_JSON_READER
# Purpose:     To identify JSON files with pertinent information
#
# Author:      T. Yeomans
#
# Created:     20-02-2021

#-------------------------------------------------------------------------------

import os
import re
import shutil
import json
import csv



### "name" "averageRating" "category" "downloadCount" "numberOfComments" "provenance" numberOfComments "viewCount"
### "Update Frequency" "Time Period Covered" "mapType" "pointAggregation"

##def renameMetafiles():
metadata = []
##

#create a method to rename the files to acceptable shapefile names
def JSONextract():



    with open(r"C:\OpenCalgary_project\meta_list.csv", "w", newline = "") as file:

        writer = csv.writer(file)


        writer.writerow(["Name", "Category", "Provenance", "Average_rating", "Download_count", "Number_of_comments", "View_count", "Update Frequency", "Time Period Covered", "Map Type", "Point Aggregation", "Tags"])


    #walk through the directory where the files are stored
        for root, dirs, files in os.walk(r"C:\OpenCalgary_project\Main_data"):

        #iterate over each item in all of the files
            for name in files:
    ##            print(name)
    ##            if  name.endswith(".json"):
    ##                print (name)
    ##            else:
    ##                pass
                print (root)

    ##            with open (r"C:\OpenCalgary_project\Test_set_JSON" + "\\" + name) as json_file:
                if name == "metadata.json":

                    print(name)
    ##                with open(name) as json_file:
    ##                    data = json.loads(json_file.read())

                    with open (root + "\\" + name) as json_file:
                        data = json.loads(json_file.read())
                        print (data["name"])

                        pairs = data.items()
                        for key, value in pairs:
                            print (value)

                        with open (r"C:\OpenCalgary_project\meta_list.txt", "w", newline = "") as f:
                            metadata = []

                            try:
                                metadata.append(str(data["name"]))
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(data["category"])
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(data["provenance"])
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(data["averageRating"])
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(data["downloadCount"])
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(data["numberOfComments"])
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(data["viewCount"])
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(data["Update Frequency"])
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(data["Time Period Covered"])
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(data["mapType"])
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(data["pointAggregation"])
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(data["tags"])
                            except:
                                metadata.append("null")


                            writer.writerow(metadata)


                else:
                    pass


print (metadata)

JSONextract()
