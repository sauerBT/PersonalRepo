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

Noise_array_init = np.random.choice([0, 1], size=(1,Data.shape[0]), p=[1./2, 1./2])
a = np.array(Noise_array_init)
Noise_array = np.tile(a,(Data.shape[1],1))
X = Noise_array*Data.T
Y_int = Data.T
Y = Y_int[1]

layers_dims = [2, 2, 2, 2, 1]

L_layer_model(X, Y, layers_dims, learning_rate = 0.0075, num_iterations = 2000, print_cost=True)
#New_Data = Zero_Random(Data)