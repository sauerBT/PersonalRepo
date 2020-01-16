# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 16:45:25 2019

@author: bsauer
"""

from tkinter.filedialog import askopenfilename, asksaveasfilename   # Import file explorer 
import csv
import pandas as pd
import numpy as np
import datetime as dt

ask = input("How many CSV file to combine?")
print( "How man?: ", ask)
how_many = int(ask)

# first file:
for file_index in range(how_many):
    filename_temp = askopenfilename(title = "Select file a file to combine")
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
    """
    Duplicate timestamp removal
    """
    if file_index == 0:
        df_combined = df
    elif file_index > 0 and file_index < (how_many - 1):
        df_combined = pd.concat([df, df_combined])
    elif file_index == (how_many - 1):
        df_combined = pd.concat([df, df_combined], ignore_index=True)
        
        
        
df_sort = df_combined.loc[pd.to_datetime(df_combined.Time).sort_values(ascending=True).index]
#df_combined["Time"] = df_combined["Time"].convert_objects(convert_dates='coerce')
#df_combined.Time.map(lambda x: dt.datetime.strftime(x, '%Y-%m-%dT%H:%M:%SZ'))      
df_clean = df_sort.drop_duplicates(subset=['Time'])
#df_clean_sort = df_clean.sort_values(by=['Time'])


filename = asksaveasfilename(initialdir = "/",title = "Find location of new file and enter name",filetypes = [('CSV file', ".csv")])

with open((filename + '.csv'), 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    df_clean.to_csv(csvfile, index=None)




    