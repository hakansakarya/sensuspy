import sensuspy as sp

s3_bucket_path = "s3://path_to_your_bucket"
sp.sync_from_aws(s3_bucket_path, "/Users/Hakan/Desktop/S3Data", aws_client_path = "/Users/Hakan/anaconda3/bin/aws")
#If you are using a mac or a unix based machine, you can find the path of your aws client by running the command "which aws" on the terminal
#A similar command exists for windows, just google it

data = sp.read_json("/Users/Hakan/Desktop/S3Data")

#Serialize the data in case you have to load it again, this makes the process much faster
sp.write_pickle(data, "/Users/Hakan/Desktop/S3DataPickled")
#You can then do data = sp.read_pickle("/Users/Hakan/Desktop/S3DataPickled") and get the same data structure

data = sp.drop_duplicates_from_data(data)
accelerometer_datum = data['AccelerometerDatum']

lags = sp.get_all_timestamp_lags(data)
accelerometer_datum_lags = lags['AccelerometerDatum']
#alteratively, accelerometer_datum_lags = sp.get_timestamp_lags(accelerometer_datum)

sp.plot_datum_lags(accelerometer_datum_lags)


