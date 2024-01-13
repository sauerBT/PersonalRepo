# -*- coding: utf-8 -*-
"""
Created on Thurday Sep 9 2021


@author: Brian Sauerborn
"""
import numpy as np
from tqdm import tqdm

def rk4_1d(func,x0,y0,xn,n,args):
    from tqdm import tqdm

    # Calculating step size
    h = (xn-x0)/n
    xout = np.linspace(x0,xn,n)
    yn = np.empty((0))
    print("------------------------------------------------------------------------------------------------------------------------------")
    print("Solving Differential...")
    print("------------------------------------------------------------------------------------------------------------------------------")
    for i in tqdm(range(n)):

        k1 = h * (func(y0, x0,*args))
        k2 = h * (func((y0+k1/2), (x0+h/2), *args))
        k3 = h * (func((y0+k2/2), (x0+h/2), *args))
        k4 = h * (func((y0+k3), (x0+h), *args))
        k = (k1+2*k2+2*k3+k4)/6
        if (i==0): # base case
            y0 = y0 + k
            yn = y0
        else:
            y0 = y0 + k
            yn = np.vstack([yn, y0])
        x0 = x0+h
    return [xout,yn]

def rk4_2d(func,x0,y0,xn,n,args):
    """
    Implements a Runge Kutta numerical iteration on a 2-Dimensional input for y0. x-axis is assumed to be time
    
    Arguments:
    func -- ODE or system of ODE function.  REQUIREMENTS: 
    x0 -- input, starting time
    y0 -- data,  of shape (1, number of examples)
    xn -- input, ending time
    n -- input, # of iterations. Splits x into n pieces
    args -- inputs, functions specific inputs passed directly to func in order
    
    Returns:
    xout -- time array
    yn -- multi dimensional y output matrix, of shape (# of iterations, # of components, # of CSTRs), of data (sample #, component #, CSTR #)
    """
    h = (xn-x0)/n # Calculating step size
    assert h>0, "Step size less than zero"
    xout = np.linspace(x0,xn,n)
    yn = np.empty((0)) # initialize output array
    for i in (range(n)):
        k1 = h * (func(y0, x0,*args))
        k2 = h * (func((y0+k1/2), (x0+h/2), *args))
        k3 = h * (func((y0+k2/2), (x0+h/2), *args))
        k4 = h * (func((y0+k3), (x0+h), *args))
        k = (k1+2*k2+2*k3+k4)/6
        if (i==0): # base case
            y0 = y0 + k
            yn = y0
        else:
            y0 = y0 + k
            yn = np.dstack([yn, y0])
        x0 = x0+h
    yn = yn.transpose(2, 0, 1) # transpose y output to to following dimensions: yn[iteration #][component #][CSTR #]
    return [xout,yn]