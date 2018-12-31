__author__ = "Sait Hakan Sakarya"
__email__ = "shs5fh@virginia.edu"

import os
import json
import glob
import pandas as pd
from tzlocal import get_localzone
from datetime import datetime


def read_json(data_path, is_directory = True, recursive = True, convert_to_local_timezone = True):
    """Reads JSON-formatted Sensus data and returns a dictionary that has its keys as the data types 
    and its values as pandas dataframes."""

    local_timezone = get_localzone()

    if is_directory:
        if recursive:
            paths = glob.glob(data_path + '*/**/*.json', recursive=True)
        else:
            paths = glob.glob(os.path.join(data_path,'*.json'))

        if len(paths) == 0:

            print("Could not find any json files to read.")
            return None

    else:

        paths = data_path
        #Check file type, return None if path is not a pickle file
        path_check = paths.split(".")
        file_extension = path_check[len(path_check)-1]

        if not file_extension == "json":
            print("Path is not a json file.")
            return None

    
    data = {}

    file_number = 0

    for path in paths:
          
        try:  
            file_number += 1
            print("Parsing JSON file " + str(file_number) + " of " + str(len(paths)) + ": " + path)

            if os.path.getsize(path) == 0:
                continue

            with open(path) as file:
                json_file = json.load(file)

            if (json_file is None) or (not json_file) or (len(json_file) == 0):
                continue

            #Get OS and Datum type
            type = json_file[0]['$type']
            type_split = type.split(",")
            OS = type_split[1].strip()
            datum_split = type_split[0].split(".")
            datum_type = datum_split[len(datum_split)-1]

            #Create dataframe if one hasn't been created for the datum type
            if datum_type not in data:

                data[datum_type] = pd.DataFrame(json_file)
                data[datum_type]['Type'] = datum_type
                data[datum_type]['OS'] = OS

            else:
                
                json_data = pd.DataFrame(json_file)
                json_data['Type'] = datum_type
                json_data['OS'] = OS
                data[datum_type] = data[datum_type].append(json_data)

        except Exception as Error:
            print(Error)
                    

    if len(data) == 0:
        print("Could not create dataframes.")
        return None

    else:
        
        #Timestamp formats
        format_with_microseconds = "%Y-%m-%dT%H%M%S.%f%z"
        format_without_microseconds = "%Y-%m-%dT%H%M%S%z"

        #TIMESTAMP OPERATIONS
        for datum in data:
                    
            try:
                timestamps = list(map(lambda timestamp:
                    str("".join(timestamp.split(":"))),data[datum]['Timestamp']))

                timestamps = list(map(lambda ts: datetime.strptime(ts,
                    format_with_microseconds) if "." in list(ts)
                    else datetime.strptime(ts,format_without_microseconds),timestamps))
                    
                timestamps = list(map(lambda ts: ts.astimezone(local_timezone) if convert_to_local_timezone else ts,timestamps))

                data[datum]['Timestamp'] = timestamps
                data[datum]['Formatted Timestamp'] = list(map(lambda ts: ts.strftime(format="%m/%d/%Y %H:%M:%S"),timestamps))
                data[datum]['Year'] = list(map(lambda ts: ts.year,timestamps))
                data[datum]['Month'] = list(map(lambda ts: ts.month,timestamps))
                data[datum]['Day'] = list(map(lambda ts: ts.day,timestamps))
                data[datum]['Hour'] = list(map(lambda ts: ts.hour,timestamps))
                data[datum]['Minute'] = list(map(lambda ts: ts.minute,timestamps))
                data[datum]['Second'] = list(map(lambda ts: float(str(ts.second) + "." + str(ts.microsecond)),timestamps))
                data[datum]['DayOfWeek'] = list(map(lambda ts: ts.weekday(),timestamps))
                data[datum]['DayOfMonth'] = list(map(lambda ts: ts.day,timestamps))
                data[datum]['DayOfYear'] = list(map(lambda ts: ts.timetuple().tm_yday,timestamps))

                #sort each df by timestamp
                data[datum] = data[datum].sort_values(by='Timestamp')
                data[datum] = data[datum].reset_index() #reset indices
                data[datum].drop('index',axis=1, inplace=True)     
                del data[datum]["$type"]

                #remove columns that contain list or dict objects
                for key in data[datum]:
                    if isinstance(data[datum][key][0],list) or isinstance(data[datum][key][0],dict):
                        del data[datum][key]
                        
            except Exception as Error:
                print(Error)

        return data


def read_csv(data_path, is_directory = True, recursive = True):
    """Reads csv files, where each csv file is associated with a data type, and creates a data dictionary
    that has its keys as the data types and its values as pandas dataframes."""

    if is_directory:
        if recursive:
            paths = glob.glob(data_path + '*/**/*.csv', recursive=True)
        else:
            paths = glob.glob(os.path.join(data_path,'*.csv'))

        if len(paths) == 0:
            print("Could not find any csv files to read.")
            return None

    else:
        paths = data_path
    
        #Check file type, return None if path is not a pickle file
        path_check = paths.split(".")
        file_extension = path_check[len(path_check)-1]

        if not file_extension == "csv":
            print("Path is not a csv file.")
            return None


    data = {}

    for path in paths:

        try:

            path_split = path.split(".")
            path_split = path_split[0].split("/")
            datum_type = path_split[len(path_split)-1]
            data[datum_type] = pd.read_csv(path)

        except Exception as Error:
            print(Error)

    if len(data) == 0:
        print("Could not create dataframes.")
        return None

    else:
        return data



def read_pickle(data_path, is_directory = True, recursive = True):
    """Reads pickle files, where each pickle file is associated with a data type, and creates a data dictionary
    that has its keys as the data types and its values as pandas dataframes."""

    if is_directory:
        if recursive:
            paths = glob.glob(data_path + '*/**/*.p', recursive=True)
        else:
            paths = glob.glob(os.path.join(data_path,'*.p'))
        
        if len(paths) == 0:
            print("Could not find any pickle files to read.")
            return None
    else:
        paths = data_path

        #Check file type, return None if path is not a pickle file
        path_check = paths.split(".")
        file_extension = path_check[len(path_check)-1]

        if not file_extension == "p":
            print("Path is not a pickle file.")
            return None

    data = {}
    
    for path in paths:

        try:

            path_split = path.split(".")
            path_split = path_split[0].split("/")
            datum_type = path_split[len(path_split)-1]
            data[datum_type] = pd.read_pickle(path)

        except Exception as Error:
            print(Error)

    if len(data) == 0:
        print("Could not create dataframes.")
        return None

    else:
        return data
