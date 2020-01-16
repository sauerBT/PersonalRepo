# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 09:30:45 2019

@author: bsauer
"""

import numpy as np


def Zero_Random(X_unfiltered):
    
    
    Noise_array_init = np.random.choice([0, 1], size=(1,X_unfiltered.shape[0]), p=[1./2, 1./2])
    a = np.array(Noise_array_init)
    Noise_array = np.tile(a,(X_unfiltered.shape[1],1))
    X = Noise_array*X_unfiltered
    return X