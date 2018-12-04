import argparse
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime
import csv

'''
description of what to do:
* first read in the files we want to use 
* store the data of crops yeild, price sold, etc. in something like an array.
* for every temp value we are loking at, rate it on the scale
* store those results in an array
* do math to that temp array to compare to the crops yeild and such
    perhaps look at it as a percentage, ie, crops yeild for total availble fields
* store if the year was good or bad
    potetially instead of year, use quarters, or by month
'''
