# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 10:02:38 2019

@author: bsauer
"""
from tkinter.filedialog import askopenfilename  # Import file explorer 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filename = askopenfilename() # Browse for file
colums = ['Date', 'FILTERED WEIGHT AT .0 SECONDS', 'SCREW SPEED SP', 'ACTUAL SCREW SPEED', 'FEEDRATE SP', 'REGRESSED FEEDRATE','FEEDFACTOR','SERVO CURRENT'];
data_mine = pd.read_csv(filename) # Store data in file

Data1 = data_mine['SERVO CURRENT']
Data2 = data_mine['SCREW SPEED SP']
Data3 = data_mine['ACTUAL SCREW SPEED']
Data1 = Data1.values
Data2 = Data2.values
Data3 = Data3.values
Data = np.vstack((Data1.T, (Data3.T - Data2.T))).T
Mew_j = np.sum(Data)/len(Data)
Covariance = (1/len(Data))*np.sum(((Data - Mew_j)**2))
p = (1/(np.sqrt(2*3.14))*np.sqrt(Covariance))*np.exp(-1*((((Data - Mew_j)**2))/(2*Covariance)))
plt.plot(Data,p)
plt.ylabel('p(x)', 'Current(amperes)')
plt.show()