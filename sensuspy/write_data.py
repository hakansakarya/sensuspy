#Write data to csv files
def write_csv(data, directory, file_name_prefix = ""):
	
	if data is None:
		print("No data to write.")

	else:
		print("Writing " + str(len(data)) + " csv files.")
		for datum_name in data:
			if data[datum_name].empty:
				print(str(datum_name) + " dataframe is empty, did not write file.")
			else:
				file_name = directory + "/" + file_name_prefix + datum_name + ".csv"
				data[datum_name].to_csv(file_name, index = False)


#Serialize data by writing pandas dataframes to pickle files
def write_pickle(data, directory, file_name_prefix = ""):

	if data is None:
		print("No data to write")

	else:
		print("Writing " + str(len(data)) + " pickle files.")
		for datum_name in data:
			if data[datum_name].empty:
				print(str(datum_name) + " dataframe is empty, did not write file.")
			else:
				file_name = directory + file_name_prefix + "/" + datum_name + ".p"
				data[datum_name].to_pickle(file_name)
	  
