import time
import pandas as pd
from geopy.geocoders import Nominatim

def get_all_timestamp_lags(data, unit_of_time = 'Second'):
    """ Computes the difference between timestamps for every dataframe in the provided data dictionary and
    returns a dictionary that has the datum types as its keys and a pandas series that consists of lags.
    Time units to choose from: 'Second' , 'Minute' and 'Hour'. """

    if data is None:
        print("Data dictionary is empty")
    else:
        lags = {}
       
        for datum in data:
            if len(data[datum]['Timestamp']) > 1:
                lags[datum] = get_timestamp_lags(data[datum], unit_of_time)
            else:
                print(str(datum) + " did not have enough timestamps to generate lags.")
        return lags


def get_timestamp_lags(datum, unit_of_time = 'Second'):
    """Computes the difference between timestamps for the provided pandas dataframe and returns a pandas
    series that consists of lags.
    Time units to choose from: 'Second' , 'Minute' and 'Hour'. """
    
    timestamps = datum['Timestamp']

    if len(timestamps) > 1:
        timedeltas = timestamps.diff()
        timedeltas = timedeltas.drop([0],axis=0)
        timedeltas.index = range(len(timedeltas))

        if unit_of_time == 'Second':
            lags = (timedeltas / pd.Timedelta(seconds=1))
        elif unit_of_time == 'Minute':
            lags = (timedeltas / pd.Timedelta(minutes=1))
        elif unit_of_time == 'Hour':
            lags = (timedeltas / pd.Timedelta(hours=1))
        else:
            print("Invalid time unit.")
            return None

        return lags

    else:
        print("Not enough timestamps to compute lags.")
        return None


def coordinates_to_addresses(data):
    """Returns a pandas dataframe that has 2 columns: timestamps and addresses. Addresses are reverse-geocoded using several services
    and there is a limit to the number of requests that can be sent, therefore the function pauses for a minute every 200 requests to reset
    the request count in order to avoid a timeout."""

    latitudes = data['LocationDatum']['Latitude']
    longitudes = data['LocationDatum']['Longitude']
    timestamps = data['LocationDatum']['Timestamp']
    geolocator = Nominatim()

    address_df = pd.DataFrame(columns=['Address','Timestamp'])
    addresses = []

    for index in range(len(data['LocationDatum'])):
        print(str(index) + " of " + str(len(data['LocationDatum'])-1))

        if not index == 0 and index % 200 == 0:
            time.sleep(60)

        cords = str(latitudes[index])+ ", " + str(longitudes[index])
        location = geolocator.reverse(cords,timeout=30)
        addresses.append(location.address)
        
    address_df['Address'] = addresses
    address_df['Timestamp'] = timestamps    
    return address_df
    
    
def drop_any_na_from_datum(datum):
    """Drops rows from the pandas dataframe where any value is NA."""

    datum_size = len(datum)
    datum_type = datum['Type'][0]
    dropped_datum = datum.dropna(axis=0, how='any')
    dropped_datum_size = len(dropped_datum)
    print(str(datum_size - dropped_datum_size) + "rows were dropped from " + datum_type + " where any value was NA.")
    return dropped_datum


def drop_any_na_from_data(data):
    """Drops rows from each pandas dataframe in the data dictionary where any value is NA."""

    dropped_data = {}
    for datum in data:
        dropped_data[datum] = drop_any_na_from_datum(data[datum])
    return dropped_data
    

def drop_na_columns_from_datum(datum):
    """Drops columns from the pandas dataframe where all values are NA."""

    datum_size = len(datum)
    datum_type = datum['Type'][0]
    dropped_datum = datum.dropna(axis=1, how='all')
    dropped_datum_size = len(dropped_datum)
    print(str(datum_size - dropped_datum_size) + " columns were dropped from " + datum_type + " where all values were NA.")
    return dropped_datum

def drop_na_columns_from_data(data):
    """Drops columns from each pandas dataframe in the data dictionary where all values is NA."""

    dropped_data = {}
    for datum in data:
        dropped_data[datum] = drop_na_columns_from_data(data[datum])
    return dropped_data


def drop_na_rows_from_datum(datum):
    """Drops rows from the pandas dataframe where all values are NA."""

    datum_size = len(datum)
    datum_type = datum['Type'][0]
    dropped_datum = datum.dropna(axis=0, how='all')
    dropped_datum_size = len(dropped_datum)
    print(str(datum_size - dropped_datum_size) + " rows were dropped from " + datum_type + " where all values were NA.")
    return dropped_datum


#Drop rows where all the values are missing
def drop_na_rows_from_data(data):
    """Drops rows from each pandas dataframe in the data dictionary where all values are NA."""

    dropped_data = {}
    for datum in data:
        dropped_data[datum] = drop_na_rows_from_datum(data[datum])
    return dropped_data


def drop_duplicates_from_datum(datum):
    """Drops duplicate rows from the pandas dataframe."""

    datum_size = len(datum)
    datum_type = datum['Type'][0]
    deduplicated_datum = datum.drop_duplicates()
    deduplicated_datum_size = len(deduplicated_datum)
    print(str(datum_size - deduplicated_datum_size) + " duplicate(s) were found and dropped in " + str(datum_type) + ".")
    return deduplicated_datum


def drop_duplicates_from_data(data):
    """Drops duplicate rows from each pandas dataframe in the data dictionary."""

    deduplicated_data = {}
    for datum in data:
        deduplicated_data[datum] = drop_datum_duplicates(data[datum])
    return deduplicated_data


def drop_device_from_datum(datum, device_id):
    """Drops all rows belonging to the provied device id from the pandas dataframe."""

    datum_size = len(datum)
    datum_type = datum['Type'][0]
    reduced_datum = data[data.DeviceId != device_id]
    reduced_datum_size = len(reduced_datum)
    print(str(datum_size - reduced_datum) + " instances of device: " + str(device_id) + " were removed from " + str(datum_type))
    return removed_datum


def drop_device_from_data(data, device_id):
    """Drops all rows belonging to the provied device id from each pandas dataframe in the data dictionary."""

    reduced_data = {}
    for datum in data:
        reduced_data[datum] = drop_device_from_datum(data[datum], device_id)
    return removed_data
    
    
def print_full_dataframe(df):
    """Prints the entire dataframe."""

    pd.set_option('display.max_rows', len(df))
    print(df)
    pd.reset_option('display.max_rows')

