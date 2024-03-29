#-------------------------------------------------------------------------------
# Name:        OPENYYC_JSON_READER
# Purpose:     To extract meaningful metadata from json files
#
# Author:      T. Yeomans
#
# Created:     20-02-2021
#-------------------------------------------------------------------------------
#import needed libraries
import os
import shutil
import json
import csv


#Build an empty list for the metadata information
metadata = []


#Create a method to rename the files to acceptable shapefile names
def JSONextract():

    #Create a new csv to host the metadata summaries
    with open(r"C:\OpenCalgary_project\meta_list.csv", "w", newline = "") as file:
        writer = csv.writer(file)

        #Write the first row with the desired column headings
        writer.writerow(["Name", "Category", "Provenance", "Average_rating", "Download_count", "Number_of_comments", "View_count", "Organization", "Business_unit", "How_data_collected", "Update_frequency","Time_period_Covered", "dataset_contains_geospatial", "Tags"])


    #walk through the directory where the files are stored
        for root, dirs, files in os.walk(r"C:\OpenCalgary_project\Main_data"):

        #iterate over each item in all of the files
            for name in files:
                if name == "metadata.json":

                    #Open and read each json file
                    with open (root + "\\" + name) as json_file:
                        data = json.loads(json_file.read())

                        #Try to look for specific fields in the json file. If they exist, append them to the list, if not, append null
                        with open (r"C:\OpenCalgary_project\meta_list_new.txt", "w", newline = "") as f:
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
                                metadata.append(str(data["metadata"]["custom_fields"]["Data Supplier"]["Organization"]))
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(str(data["metadata"]["custom_fields"]["Data Supplier"]["Business Unit"]))
                            except:
                                metadata.append("null")
                            try:
                                metadata.append(str(data["metadata"]["custom_fields"]["Time/Date"]["How Data is Collected"]))
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(str(data["metadata"]["custom_fields"]["Time/Date"]["Update Frequency"]))
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(str(data["metadata"]["custom_fields"]["Time/Date"]["Time Period Covered"]))
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(str(data["metadata"]["custom_fields"]["Geospatial Information"]["Dataset contains geospatial information"]))
                            except:
                                metadata.append("null")

                            try:
                                metadata.append(data["tags"])
                            except:
                                metadata.append("null")

                            print (metadata)

                            writer.writerow(metadata)

                else:
                    pass


JSONextract()
