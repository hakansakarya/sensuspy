import math
import gmplot
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages


def plot_accelerometer_datum(data, save = False, separate = False):
 
    accelerometer_datum = data['AccelerometerDatum']

    if separate:
        fig1 = plot(accelerometer_datum['Timestamp'],accelerometer_datum['X'],"Time","X","Accelerometer Datum (X)",save_plot=False)
        fig2 = plot(accelerometer_datum['Timestamp'],accelerometer_datum['Y'],"Time","Y","Accelerometer Datum (Y)",save_plot=False)
        fig3 = plot(accelerometer_datum['Timestamp'],accelerometer_datum['Z'],"Time","Z","Accelerometer Datum (Z)",save_plot=False)

        if save:
            filename = input("Enter a filename (should be in pdf format, ex: figure.pdf): ")
            file = PdfPages(filename)
            file.savefig(fig1)
            file.savefig(fig2)
            file.savefig(fig3)
            file.close()

        plt.show()

    else:
        fig = plt.figure(figsize=(18,12))
        fig.subplots_adjust(hspace=1)

        x = fig.add_subplot(3,1,1)
        y = fig.add_subplot(3,1,2)
        z = fig.add_subplot(3,1,3)
       
        x.plot(accelerometer_datum['Timestamp'],accelerometer_datum['X'])
        x.set_title("Accelerometer Datum (X)")
        x.set_ylabel("X")
        x.set_xlabel("Time")
       

        y.plot(accelerometer_datum['Timestamp'],accelerometer_datum['Y'])
        y.set_title("Accelerometer Datum (Y)")
        y.set_ylabel("Y")
        y.set_xlabel("Time")
       

        z.plot(accelerometer_datum['Timestamp'],accelerometer_datum['Z'])
        z.set_title("Accelerometer Datum (Z)")
        z.set_ylabel("Z")
        z.set_xlabel("Time")
       

        tz = accelerometer_datum['Timestamp'][0].tz
        xfmt = mdates.DateFormatter('%m/%d/%Y %H:%M:%S', tz=tz)
        x.xaxis.set_major_formatter(xfmt)
        y.xaxis.set_major_formatter(xfmt)
        z.xaxis.set_major_formatter(xfmt)

        if save:
            filename = input("Enter a filename (include the extension): ")
            plt.savefig(filename)

        plt.show()


def plot_altitude_datum(data, save = False):

    altitude_datum = data['AltitudeDatum']
    plot(altitude_datum['Timestamp'],altitude_datum['Altitude'],"Time","Meters","Altitude Datum",save)
    plt.show()


def plot_battery_datum(data, save = False):

    battery_datum = data['BatteryDatum']
    plot(battery_datum['Timestamp'],battery_datum['Level'],"Time","Level(%)","Battery Datum",save)
    plt.show()


def plot_celltower_datum(data, save = False):

    celltower_datum = data['CellTowerDatum']

    if len(celltower_datum['CellTower']) > 0:

        frequencies = {}

        for celltower_id in celltower_datum['CellTower']:
            if celltower_id not in frequencies:
                frequencies[celltower_id] = 1
            else:
                frequencies[celltower_id] += 1

        labels = list(frequencies.keys())
        values = list(frequencies.values())

        fig1, ax1 = plt.subplots(figsize=(12,9))
        ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal') 

        if save:
            filename = input("Enter a filename (include the extension): ")
            plt.savefig(filename)

        plt.show()

    else:
        print("No Cell Tower IDs found")


def plot_compass_datum(data, save = False):

    compass_datum = data['CompassDatum']
    plot(compass_datum['Timestamp'],compass_datum['Heading'],"Time","Heading","Compass Datum",save)
    plt.show()


def plot_light_datum(data, save = False):

    light_datum = data['LightDatum']
    plot(light_datum['Timestamp'],light_datum['Brightness'],"Time","Brightness Level","Light Datum",save)
    plt.show()


def plot_location_datum(data, mapname = None, plot_type = "scatter"):

    location_datum = data['LocationDatum']

    center_latitude = location_datum['Latitude'].mean()
    center_longitude = location_datum['Longitude'].mean()
    
    gmap = gmplot.GoogleMapPlotter(center_latitude, center_longitude, 5)
        
    if mapname == None:
        mapname = input("Enter a name for the file (do not include an extension): ")

    if plot_type == "default":
        gmap.plot(location_datum['Latitude'],location_datum['Longitude'])
        gmap.draw(mapname + ".html")

    elif plot_type == "heatmap":
        gmap.heatmap(location_datum['Latitude'],location_datum['Longitude'])
        gmap.draw(mapname + ".html")

    elif plot_type == "scatter":
        gmap.scatter(location_datum['Latitude'],location_datum['Longitude'])
        gmap.draw(mapname + ".html")

    elif plot_type == "circle":
        for index in range(len(location_datum)):
            if location_datum['Accuracy'][index] > location_datum['Accuracy'].mean():
                gmap.circle(location_datum['Latitude'][index],location_datum['Longitude'][index],location_datum['Accuracy'].mean(),color="white")
            else:
                gmap.circle(location_datum['Latitude'][index],location_datum['Longitude'][index],location_datum['Accuracy'][index],color="white")
        gmap.draw(mapname + ".html")


    
def plot_screen_datum(data, save = False):

    screen_datum = data['ScreenDatum']
    plot(screen_datum['Timestamp'],screen_datum['On'],"Time","On/Off","Screen Datum",save)
    plt.show()


def plot_sound_datum(data, save = False):

    sound_datum = data['SoundDatum']
    plot(sound_datum['Timestamp'],sound_datum['Decibels'],"Time","Decibels","Sound Datum",save)
    plt.show()


def plot_speed_datum(data, save = False):

    speed_datum = data['SpeedDatum']
    plot(speed_datum['Timestamp'],speed_datum['KPH'],"Time","KPH","Speed Datum",save)
    plt.show()


def plot_telephony_datum(data, save = False):

    telephony_datum = data['TelephonyDatum']
    
    outgoing_frequencies = {}
    incoming_frequencies = {}
    
    for index in range(len(telephony_datum['PhoneNumber'])):
        if telephony_datum['State'][index] == 1:
            if telephony_datum['PhoneNumber'][index] not in outgoing_frequencies:
                outgoing_frequencies[telephony_datum['PhoneNumber'][index]] = 1
            else:
                outgoing_frequencies[telephony_datum['PhoneNumber'][index]] += 1
        elif telephony_datum['State'][index] == 2:
            if telephony_datum['PhoneNumber'][index] not in incoming_frequencies:
                incoming_frequencies[telephony_datum['PhoneNumber'][index]] = 1
            else:
                incoming_frequencies[telephony_datum['PhoneNumber'][index]] += 1

    if len(outgoing_frequencies) == 0 and len(incoming_frequencies) == 0: 
        print("No telephony_datum to plot")

    else:
        fig = plt.figure()
        fig.subplots_adjust(hspace=.5)
        outgoing_calls = fig.add_subplot(1,2,1)
        incoming_calls = fig.add_subplot(1,2,2)

        if len(outgoing_frequencies) > 0:
            outgoing_calls.pie(list(outgoing_frequencies.values()), labels = list(outgoing_frequencies.keys()), autopct='%1.1f%%', startangle=90)
            outgoing_calls.axis('equal')
            outgoing_calls.set_title("Outgoing Calls")

        if len(incoming_frequencies) > 0:
            incoming_calls.pie(list(incoming_frequencies.values()), labels = list(incoming_frequencies.keys()), autopct='%1.1f%%', startangle=90)
            incoming_calls.axis('equal')
            incoming_calls.set_title("Incoming Calls")
            
        if save:
            filename = input("Enter a filename (include the extension): ")
            plt.savefig(filename)

        plt.show()


def plot_wlan_datum(data, save = False):

    wlan_datum = data['WlanDatum']
    
    if len(wlan_datum['AccessPointBSSID']) > 0:

        frequencies = {}

        for bssid in wlan_datum['AccessPointBSSID']:
            if not bssid == "":
                if bssid not in frequencies:
                    frequencies[bssid] = 1
                else:
                    frequencies[bssid] += 1
        labels = list(frequencies.keys())
        values = list(frequencies.values())

        fig1, ax1 = plt.subplots(figsize=(12,9))
        ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal') 

        if save:
            filename = input("Enter a filename (include the extension): ")
            plt.savefig(filename)

        plt.show()

    else:
        print("No Access Point BSSIDs found")


def plot_datum_lags(datum_lags, bins = 10, save = False):

    datum_lags.hist(grid=False,bins=bins)
    
    min = datum_lags.min()
    max = datum_lags.max()
    range = max - min

    binwidth =  range / bins
    
    plt.xticks(np.arange(min, (max+binwidth), binwidth))
    plt.xlabel("Seconds")
    plt.ylabel("Frequency")

    if save:
            filename = input("Enter a filename (include the extension): ")
            plt.savefig(filename)

    plt.show()


def plot_datum_frequency_by_day(datum, save = False):

    datum_type = datum['Type'][0]
    frequencies = {}
    days = datum['DayOfYear']
    for day in days:
        if day not in frequencies:
            frequencies[day] = 1
        else:
            frequencies[day] += 1

    plt.figure(num=None, figsize=(12, 9), dpi=80, facecolor='w', edgecolor='k')
    plt.plot(list(frequencies.keys()),list(frequencies.values()))
    plt.title(str(datum_type) + "Frequency by Day (of year)")
    plt.xlabel("Study Day (of year)")
    plt.ylabel("Data Frequency")

    if save:
            filename = input("Enter a filename (include the extension): ")
            plt.savefig(filename)

    plt.show()
  


def plot_datum_lag_cdf(datum_lags, unit_of_time = 'Second', save = False):

    #lags = sensus_get_timestamp_lags(datum, unit_of_time = unit_of_time)
    x = np.sort(datum_lags)
    y = np.arange(1,len(x)+1) / len(x)
    plt.plot(x,y,marker='.',linestyle='none')
    #plt.xlabel("Inter-reading times (" + unit_of_time + "s)")
    plt.xlabel("Inter-reading times")
    plt.ylabel('Percentile')

    if save:
            filename = input("Enter a filename (include the extension): ")
            plt.savefig(filename)

    plt.show()


def plot(x, y, xlabel, ylabel, title, save_plot):

    fig, ax = plt.subplots(figsize=(12,9), dpi=80, facecolor='w', edgecolor='k')
    fig.autofmt_xdate()
    plt.plot(x,y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    tz = x[0].tz
    xfmt = mdates.DateFormatter('%m/%d/%Y %H:%M:%S', tz=tz)
    ax.xaxis.set_major_formatter(xfmt)

    if save_plot:
        filename = input("Enter a filename (include the extension): ")
        plt.savefig(filename)

    return fig
