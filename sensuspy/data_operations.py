import time
import pandas as pd
from geopy.geocoders import Nominatim

def get_all_timestamp_lags(data, unit_of_time = 'Second'):

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


#Returns a dataframe that has timestamps and addresses as its columns
def coordinates_to_addresses(data):

    latitudes = data['LocationDatum']['Latitude']
    longitudes = data['LocationDatum']['Longitude']
    timestamps = data['LocationDatum']['Timestamp']
    geolocator = Nominatim()

    #address_dict = {'Address': [], 'Timestamp': timestamps.apply(lambda x: x.strftime('%m/%d/%Y %H:%M:%S %Z'))}
    address_df = pd.DataFrame(columns=['Address','Timestamp'])
    addresses = []

    for index in range(len(data['LocationDatum'])):
        print(str(index) + " of " + str(len(data['LocationDatum'])-1))

        #These numbers work for S3Pickled but service timeout may occur with bigger data
        #Pause for a minute every 200 requests in order to reset request count so it doesn't timeout
        if not index == 0 and index % 200 == 0:
            time.sleep(60)

        cords = str(latitudes[index])+ ", " + str(longitudes[index])
        location = geolocator.reverse(cords,timeout=30)
        addresses.append(location.address)
        #address_df = address_df.append(data={'Address': location.address, 'Timestamp': timestamps.loc[index]},ignore_index=True)
        
        #address_dict['Address'].append(location.address)
    address_df['Address'] = addresses
    address_df['Timestamp'] = timestamps    
    #return address_dict
    return address_df
    
    
def drop_any_na_from_datum(datum):
    datum_size = len(datum)
    datum_type = datum['Type'][0]
    dropped_datum = datum.dropna(axis=0, how='any')
    dropped_datum_size = len(dropped_datum)
    print(str(datum_size - dropped_datum_size) + "rows were dropped from " + datum_type + " where any value was NA.")
    return dropped_datum


def drop_any_na_from_data(data):
    dropped_data = {}
    for datum in data:
        dropped_data[datum] = drop_any_na_from_datum(data[datum])
    return dropped_data
    

def drop_na_columns_from_datum(datum):
    datum_size = len(datum)
    datum_type = datum['Type'][0]
    dropped_datum = datum.dropna(axis=1, how='all')
    dropped_datum_size = len(dropped_datum)
    print(str(datum_size - dropped_datum_size) + " columns were dropped from " + datum_type + " where all values were NA.")
    return dropped_datum

#Drop columns where all the values are missing
def drop_na_columns_from_data(data):
    dropped_data = {}
    for datum in data:
        dropped_data[datum] = drop_na_columns_from_data(data[datum])
    return dropped_data


def drop_na_rows_from_datum(datum):
    datum_size = len(datum)
    datum_type = datum['Type'][0]
    dropped_datum = datum.dropna(axis=0, how='all')
    dropped_datum_size = len(dropped_datum)
    print(str(datum_size - dropped_datum_size) + " rows were dropped from " + datum_type + " where all values were NA.")
    return dropped_datum


#Drop rows where all the values are missing
def drop_na_rows_from_data(data):
    dropped_data = {}
    for datum in data:
        dropped_data[datum] = drop_na_rows_from_datum(data[datum])
    return dropped_data


def drop_duplicates_from_datum(datum):
    datum_size = len(datum)
    datum_type = datum['Type'][0]
    deduplicated_datum = datum.drop_duplicates()
    deduplicated_datum_size = len(deduplicated_datum)
    print(str(datum_size - deduplicated_datum_size) + " duplicate(s) were found and dropped in " + str(datum_type) + ".")
    return deduplicated_datum


def drop_duplicates_from_data(data):
    deduplicated_data = {}
    for datum in data:
        deduplicated_data[datum] = drop_datum_duplicates(data[datum])
    return deduplicated_data


def drop_device_from_datum(datum, device_id):
    datum_size = len(datum)
    datum_type = datum['Type'][0]
    reduced_datum = data[data.DeviceId != device_id]
    reduced_datum_size = len(reduced_datum)
    print(str(datum_size - reduced_datum) + " instances of device: " + str(device_id) + " were removed from " + str(datum_type))
    return removed_datum


def drop_device_from_data(data, device_id):
    reduced_data = {}
    for datum in data:
        reduced_data[datum] = drop_device_from_datum(data[datum], device_id)
    return removed_data
    
    
def print_full_dataframe(df):
    pd.set_option('display.max_rows', len(df))
    print(df)
    pd.reset_option('display.max_rows')

