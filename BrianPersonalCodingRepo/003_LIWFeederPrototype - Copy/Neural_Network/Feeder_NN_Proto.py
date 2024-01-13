# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 09:38:17 2019

@author: bsauer
"""

import time
import numpy as np
import h5py
import matplotlib.pyplot as plt
import scipy
from PIL import Image
#from scipy import ndimage

from NN_Run import L_layer_model
from tkinter.filedialog import askopenfilename  # Import file explorer 
import pandas as pd
from Noise import Zero_Random
import random as rn


filename = askopenfilename() # Browse for file

"""
Selected File Columns
"""
colums = ['Weight', 'SCREW SPEED SP', 'FEEDRATE SP', 'REGRESSED FEEDRATE','FEEDFACTOR','SERVO CURRENT'];
data_mine = pd.read_csv(filename) # Store data in file

"""
Convert data to numerical values
"""
data_mine["Weight"] = data_mine["Weight"].convert_objects(convert_numeric=True)
data_mine["ACTUAL SCREW SPEED"] = data_mine["ACTUAL SCREW SPEED"].convert_objects(convert_numeric=True)
data_mine["SERVO CURRENT"] = data_mine["SERVO CURRENT"].convert_objects(convert_numeric=True)
data_mine["SCREW SPEED SP"] = data_mine["SCREW SPEED SP"].convert_objects(convert_numeric=True)
data_mine["FEEDRATE SP"] = data_mine["FEEDRATE SP"].convert_objects(convert_numeric=True)
data_mine["REGRESSED FEEDRATE"] = data_mine["REGRESSED FEEDRATE"].convert_objects(convert_numeric=True)
data_mine["FEEDFACTOR"] = data_mine["FEEDFACTOR"].convert_objects(convert_numeric=True)
"""
Define Data Arrays
"""
Data1 = data_mine['Weight']
Data2 = data_mine['SERVO CURRENT']
Data3 = data_mine['SCREW SPEED SP']
Data4 = data_mine['FEEDRATE SP']
Data5 = data_mine['REGRESSED FEEDRATE']
Data6 = data_mine['FEEDFACTOR']
Data7 = data_mine['ACTUAL SCREW SPEED']
Data8 = data_mine['SCREW VOLUME']
Data9 = data_mine['BULK DENSITY']
"""
Convert Data Arrays to Values
"""
Data1 = Data1.values
Data2 = Data2.values
Data3 = Data3.values
Data7 = Data7.values
Data4 = Data4.values
Data5 = Data5.values
Data6 = Data6.values
Data8 = Data8.values
Data9 = Data9.values

"""
Convert NaN to Zeros
"""
NaN_Idx_1 = np.isnan(Data1)
Data1[NaN_Idx_1] = 0


NaN_Idx_2 = np.isnan(Data2)
Data2[NaN_Idx_2] = 0

NaN_Idx_3 = np.isnan(Data3)
Data3[NaN_Idx_3] = 0

NaN_Idx_4 = np.isnan(Data4)
Data4[NaN_Idx_4] = 0

NaN_Idx_5 = np.isnan(Data5)
Data5[NaN_Idx_5] = 0

NaN_Idx_6 = np.isnan(Data6)
Data6[NaN_Idx_6] = 0

NaN_Idx_7 = np.isnan(Data7)
Data7[NaN_Idx_7] = 0

NaN_Idx_8 = np.isnan(Data8)
Data8[NaN_Idx_8] = 0

NaN_Idx_9 = np.isnan(Data9)
Data9[NaN_Idx_9] = 0
"""
Normalization parameters
"""
m = Data1.shape[0]
Sig_1 = (1/m)*np.sum(np.square(Data1))
Mean_1 = (1/m)*np.sum(Data1)

Sig_2 = (1/m)*np.sum(np.square(Data2))
Mean_2 = (1/m)*np.sum(Data2)

Sig_3 = (1/m)*np.sum(np.square(Data3))
Mean_3 = (1/m)*np.sum(Data3)

Sig_4 = (1/m)*np.sum(np.square(Data4))
Mean_4 = (1/m)*np.sum(Data4)

Sig_5 = (1/m)*np.sum(np.square(Data5))
Mean_5 = (1/m)*np.sum(Data5)

Sig_6 = (1/m)*np.sum(np.square(Data6))
Mean_6 = (1/m)*np.sum(Data6)

Sig_7 = (1/m)*np.sum(np.square(Data7))
Mean_7 = (1/m)*np.sum(Data7)

Sig_8 = (1/m)*np.sum(np.square(Data8))
Mean_8 = (1/m)*np.sum(Data8)

Sig_9 = (1/m)*np.sum(np.square(Data9))
Mean_9 = (1/m)*np.sum(Data9)

Data1 = Data1 - Mean_1
Data1 /= Sig_1

Data2 = Data2 - Mean_2
Data2 /= Sig_2

Data3 = Data3 - Mean_3
Data3 /= Sig_3

Data4 = Data4 - Mean_4
Data4 /= Sig_4

Data5 = Data5 - Mean_5
Data5 /= Sig_5

Data6 = Data6 - Mean_6
Data6 /= Sig_6

Data7 = Data7 - Mean_7
Data7 /= Sig_7

Data8 = Data8 - Mean_8
Data8 /= Sig_8

Data9 = Data9 - Mean_9
Data9 /= Sig_9

"""
Create Data Matrix Input

Data1 = data_mine['Weight']
Data2 = data_mine['SERVO CURRENT']
Data3 = data_mine['SCREW SPEED SP']
Data4 = data_mine['FEEDRATE SP']
Data5 = data_mine['REGRESSED FEEDRATE']
Data6 = data_mine['FEEDFACTOR']
Data7 = data_mine['ACTUAL SCREW SPEED']
"""
Data = np.vstack((Data1.T, Data2.T, Data4.T, Data6.T, Data7.T, Data8.T, Data9.T)).T
"""
Logic to randomize dataset

your_permutation = np.linspace(0,(Data.shape[0] - 1), num=Data.shape[0])
np.random.shuffle(your_permutation)
your_permutation = your_permutation.astype(int)
Data = Data[your_permutation,:]
"""

"""
Add noise to Input Data Matrix
"""
Noise_array_init = np.random.choice([0, 1], size=(1,Data.shape[0]), p=[1./2, 1./2])
a = np.array(Noise_array_init)
Noise_array = np.tile(a,(Data.shape[1],1))
X = Noise_array*Data.T
Y = Data5.T
"""
Start Neural Network Learning Algorithm
"""
layers_dims = [7, 1000, 100, 1] # Neural Network Layer and Node Set up

[p,AL] = L_layer_model(X, Y, layers_dims, learning_rate = 0.0075, num_iterations = 4000, print_cost=True, lambd = .1)


"""
Plot Learning Algorithm Outputs vs known values
"""
x1 = np.linspace(0,AL.shape[1], num=AL.shape[1])
x2 = np.linspace(0,Data5.shape[0], num=Data5.shape[0])
y1 = AL.T*Sig_5
y1 = y1 + Mean_5 
y2 = Data5*Sig_5
y2 = y2 + Mean_5
plt.figure(0)
plt.plot(x1,y1, 'ko', markersize=.1)
plt.plot(x2,y2, 'yo', markersize=.1)
plt.ylabel('Filtered Rate')
plt.xlabel('Data Point')
plt.title("Learned Filter")
plt.savefig('Filter.pdf')
plt.show()


#New_Data = Zero_Random(Data)