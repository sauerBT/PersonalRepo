# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 16:04:39 2019

@author: bsauer
"""
from tkinter.filedialog import askopenfilename, asksaveasfilename   # Import file explorer 
import csv
import pandas as pd
import numpy as np
import datetime as dt

ask = input("How many CSV file to clean?")
print( "How man?: ", ask)
how_many = int(ask)

# first file:
for file_index in range(how_many):
    filename_temp = askopenfilename(title = "Select first file to clean")
    df = pd.read_csv(filename_temp)
    header = list(df)
    header.remove('Time')
    
    """
    NaN removal
    """
    df[header] = df[header].convert_objects(convert_numeric=True)
    NaN_Idx = np.isnan(df[header])
    NaN_Idx = NaN_Idx.values
    NaN_Idx = np.nonzero(NaN_Idx)
    df = df.drop(NaN_Idx[0])
    filename = asksaveasfilename(initialdir = "/",title = "Find location of new file and enter name",filetypes = [('CSV file', ".csv")])

    with open((filename + '.csv'), 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        df.to_csv(csvfile, index=None)
    

