__author__ = "Sait Hakan Sakarya"
__email__ = "shs5fh@virginia.edu"

import os
import pandas as pd

def write_csv(data, directory, file_name_prefix = ""):
	"""Writes the pandas dataframes contained in the data dictionary to csv files in the specified directory.
	The directory is created if it doesn't exist. A filename prefix can be specified as an argument. """

	if data is None:
		print("No data to write.")

	else:
		if not os.path.isdir(directory):
					command = "mkdir " + directory
					os.system(command)
		print("Writing " + str(len(data)) + " csv files.")
		for datum_name in data:
			if data[datum_name].empty:
				print(str(datum_name) + " dataframe is empty, did not write file.")
			else:
				file_name = directory + "/" + file_name_prefix + datum_name + ".csv"
				data[datum_name].to_csv(file_name, index = False)


def write_pickle(data, directory, file_name_prefix = ""):
	"""Writes the pandas dataframes contained in the data dictionary to pickles files in the specified directory.
	The directory is created if it doesn't exist. A filename prefix can be specified as an argument.
	Writing pickle files serializes the pandas dataframes making it much faster to read pickle files compared to parsing from json each time."""
	
	if data is None:
		print("No data to write")

	else:
		if not os.path.isdir(directory):
					command = "mkdir " + directory
					os.system(command)
		print("Writing " + str(len(data)) + " pickle files.")
		for datum_name in data:
			if data[datum_name].empty:
				print(str(datum_name) + " dataframe is empty, did not write file.")
			else:
				file_name = directory + "/" + file_name_prefix + datum_name + ".p"
				data[datum_name].to_pickle(file_name)