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
    

#Drop rows where any value is missing
def drop_na(data):
    if type(data) == type({}):
        dropped_data = {}
        for datum in data:
            dropped_data[datum] = data[datum].dropna(axis=0, how='any')
        return dropped_data
    else:
        print("Invalid argument. This function only accepts a data dictionary as its argument.")


#Drop columns where all the values are missing
def drop_na_columns(data):
    if type(data) == type({}):
        dropped_data = {}
        for datum in data:
            dropped_data[datum] = data[datum].dropna(axis=1, how='all')
        return dropped_data
    else:
        print("Invalid argument. This function only accepts a data dictionary as its argument.")


#Drop rows where all the values are missing
def drop_na_rows(data):
    if type(data) == type({}):
        dropped_data = {}
        for datum in data:
            dropped_data[datum] = data[datum].dropna(axis=0, how='all')
        return dropped_data
    else:
        print("Invalid argument. This function only accepts a data dictionary as its argument.")


def drop_datum_duplicates(datum):
    datum_size = len(datum)
    datum_type = datum['Type'][0]
    deduplicated_datum = datum.drop_duplicates()
    deduplicated_datum_size = len(deduplicated_datum)
    print(str(datum_size - deduplicated_datum_size) + " duplicate(s) were found and dropped in " + str(datum_type) + ".")
    return deduplicated_datum


def drop_data_duplicates(data):
    if type(data) == type({}):
        deduplicated_data = {}
        for datum in data:
            deduplicated_data[datum] = drop_datum_duplicates(data[datum])
        return deduplicated_data
    else:
        print("Invalid argument. This function only accepts a data dictionary as its argument.")


def remove_device_id(data):
    if type(data) == type({}):
        for datum in data:
            del data[datum]['DeviceId']
    else:
        print("Invalid argument. This function only accepts a data dictionary as its argument.")


def print_full_dataframe(df):
    pd.set_option('display.max_rows', len(df))
    print(df)
    pd.reset_option('display.max_rows')

