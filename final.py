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

def ReadInAttributeFromCSV(fileName, attribute):
	attributeValues = []
	f = open(fileName, 'r')
	# Create a csv reader that stores the each column of the first line of the file
	# as keys and then the rest of the lines of each column as values for those keys
	reader = csv.DictReader(f)
	for row in reader:
		if attribute in row:
			if attribute != 'date':
				value = float(row[attribute])
				attributeValues.append(value)
			else:
				date = datetime.datetime.strptime(row[attribute],'%Y/%m/%d')
				attributeValues.append(date)
	f.close()
	return attributeValues

def main():
	print ("Hello World")

if __name__ == '__main__':
	main()
