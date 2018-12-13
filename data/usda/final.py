'''
NOTE:
To run for the first time, ensure it it exacutable by 
changing the permissions by running the following in the 
command line:
	sudo chmod +x final.py
To run the program use python3, run the following in
the command line:
	python3 ./final.py
'''

import pandas as pd
import numpy as np
import pickle
from pathlib import Path
import math

'''
description of what to do:
first read in the files we want to use 
store the data of crops yeild, price sold, etc. in something like an array.
for every temp value we are loking at, rate it on the scale
store those results in an array
do math to that temp array to compare to the crops yeild and such
    perhaps look at it as a percentage, ie, crops yeild for total availble fields
store if the year was good or bad
    potetially instead of year, use quarters, or by month
'''

'''
Function to find avocado harvested data
	input file, columns to drop 
	('path/to/file/filename.ext', ['some','array'])
	Function will read in a specified csv file
	and drop an empty column where are the entries are NaN
	Function will also filer for California and make the 
	data set condensed with only relevent data
'''	
def Avo_Data(file_name, col_to_drop):
	#read in the dataset
	data_set = pd.read_csv(file_name)
	#filter out null columns and for California
	#and for progrm to be a survey
	data_set = data_set.dropna(axis='columns', how='all')
	data_set = data_set[(data_set['State'].str.contains('CA')) \
						&(data_set['Program'].str.contains('SUR'))]
	data_set = data_set.drop(col_to_drop, axis=1)
	#if " (D)" or " (Z)" is in a row, drop it
	data_set = data_set[~data_set['Value'].isin([' (D)', ' (Z)'])]
	# drop data from 2002, so we can look at years 2007-2017
	data_set = data_set[~data_set['Year'].isin(['2002'])]
	#put the data in an array of touples
	subset = data_set[['Year','State','Value']]
	tuples = [tuple(x) for x in subset.values]
	#convert the value fata to floats
	tuples = [(x[0],x[1],float(x[2].replace(",",""))) for x in tuples]
	#print it so it looks pretty
	for i in range(0, len(tuples)):
		print (tuples[i])
	return 0

def main():
	#columns to drop from avocado yeild table
	col_to_drop_AVO_YEILD_TABLE = ['Program','Period','Geo Level',\
			'State ANSI', 'watershed_code','Commodity', \
			'Data Item', 'Domain','Domain Category']
	# call function to do stuff
	print ('\n Avocados_Yeild_Measured_In_Tons_Per_Acre \n')
	Avo_Data('Data_Files/Data_From_USDA/Avocados_Yeild_Measured_In_Tons_Per_Acre.csv', \
	 	col_to_drop_AVO_YEILD_TABLE)
	print ('\n Avocados_Acres_Bearing \n')
	Avo_Data('Data_Files/Data_From_USDA/Avocados_Acres_Bearing.csv', \
	 	col_to_drop_AVO_YEILD_TABLE)
	#print ('\n Avocados_Acres_Non_Bearing \n')
	#Avo_Data('Data_Files/Data_From_USDA/Avocados_Acres_Non_Bearing.csv', \
	# 	col_to_drop_AVO_YEILD_TABLE)
	'''TO DO:
	find what a good yeild for acocados be. compare to the 
	data that i have
	or, normalize the data, ith relation to the amount harvested
	to the acres available'''

if __name__ == '__main__':
	main()
