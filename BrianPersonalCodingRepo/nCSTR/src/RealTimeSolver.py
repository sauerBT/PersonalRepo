# -*- coding: utf-8 -*-
"""
Created on Thurday Sep 9 2021
@author: Brian Sauerborn
"""
import numpy as np
import matplotlib.pyplot as plt
from cstr_models import *
from numerical_methods import *
import pandas as pd
import os

def cstrRT(yCstr, yIn, massReal, q, mIn):
    """
    Simulates real time RTD model solver given a static set of sample data
    
    Arguments:
    yCstr -- given initial condition concentration values for the numerical solver, of shape (# streams, # CSTRs in series)
    yIn -- given measured input concentration values used for each cycle, of shape (# of samples, # of streams)
    massReal -- given measured input total mass, of shape (# of samples)
    q -- give backmix constant
    mIn -- give measured total mass flow rate input, of shape (# of samples)

    Returns:
    xout -- time array
    yn -- multi dimensional y output matrix, of shape (# of iterations, # of components, # of CSTRs), of data (sample #, component #, CSTR #)
    
    Internal Variables:
    dMdt -- calculated change in total mass at each interval
    x_stream -- # of input streams
    tn -- total amount of time
    x3 -- time array from 0 - tn
    
    """
    if yIn.shape[0] > 1: # check for updating concentration input over time.  If not, y_in will automatically be broadcast
            tn = len(yIn)
            assert len(mIn) == tn
    assert yIn.shape[1] > 0, 'Input concentration must have AT LEAST 1 stream'
    x_streams = len(yIn[0])
    xplot = np.empty((0))
    yplot = np.empty((0))
    dMdt = [] # initialize change in mass calculations
    for m in range(len(massReal)): # calculate the change in mass at each interval
        if m == 0: # base case
            dMdt.append(0)
        else:
            dMdt.append(M[m] - M[m-1])

    # Initiate plots
    fig, axs = plt.subplots(4)
    axs[3].plot(x3, dMdt, 'k-')
    axs[2].plot(x3, massReal, 'k-')
    axs[2].set_xlabel("time"), axs[2].set_ylabel("Total Mass(x)"), axs[2].set_title("Total Mass Over Time")
    axs[1].plot(x_streams*[0], yCstr.transpose(1,0)[0,::], 'go', x3, measuredValue, 'b-' , x_streams*[(tn - 1)], yIn[(tn - 1),::], 'ro') # initialize plot
    axs[1].set_xlabel("time"), axs[1].set_ylabel("concentration(x)"), axs[1].set_title("Concetrations of Each Stream Over Time")
    axs[0].plot(0, yCstr.transpose(1,0)[0,apiStream], 'go', x3, measuredValue, 'b-', tn - 1, yIn[(tn - 1),1], 'ro',) # initialize plot
    axs[0].set_xlabel("time"), axs[0].set_ylabel("concentration(x)"), axs[0].set_title("Concetration of Predicated vs Measured API Over Time")
    plt.pause(0.005)
    # Start Solver
    for t in tqdm(range(tn)):
        # Solve ODE
        if (t == 0): # base case
            [x_n,y_rk4_n] = rk4_2d(cstrN, x0 = 0, y0 = yCstr, xn = 1, n=10, args=(yIn[t,::], massReal[t], dMdt[t], q, mIn[t]))
            assert y_rk4_n.shape[1] == x_streams, f'number of solution streams ({y_rk4_n.shape[2]}) does not match the number of input streams ({x_streams})'
            xplot = np.append(xplot, t)
            yplot = y_rk4_n[9,::,::]
            yCstr = yplot
            axs[0].plot([t+1], yplot[apiStream, (Ncstr - 1)], 'm.', markersize = 1)
            plt.pause(0.000000000001)
        else:
            [x_n,y_rk4_n] = rk4_2d(cstrN, x0 = 0, y0 = yCstr, xn = 1, n=10, args=(yIn[t,::], massReal[t], dMdt[t], q, mIn[t]))
            assert y_rk4_n.shape[1] == x_streams, f'number of solution streams ({y_rk4_n.shape[2]}) does not match the number of input streams ({x_streams})'
            xplot = np.append(xplot, t)
            yplot = np.dstack([yplot, y_rk4_n[9,::,::]])
            yCstr = yplot[::,::,t]
            axs[0].plot([t+1], yplot[apiStream, (Ncstr - 1), t], 'm.', markersize = 1)
            plt.pause(0.000000000001)
    yplot = yplot.transpose(2, 0, 1) # transpose y output to to following dimensions: yn[iteration #][component #][CSTR #]
    # axs[0].plot(yplot[apiStream, (Ncstr - 1), t], 'm.', markersize = 1)
    return yplot

def readRTDExp(file):
    my_export = pd.read_csv(file, index_col = 0, header = 0, skiprows = 0) #before index_col = 0 but excluded first column
    df = my_export.set_index('Date')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return [df]

# Import and format RTD data
file = os.path.realpath('nCSTR\\IMA_RTD_Data-v1.csv') #'C:\\Users\\bsauer\\OneDrive - Control Associates, Inc\\Desktop\\nCSTR\\IMA_RTD_Data-v1.csv'
[df] = readRTDExp(file)
F1_Flow = np.array(df['F1_CURR_FLW/PV.CV'])/3.6
API_Flow = np.array(df['F2_CURR_FLW/PV.CV'])/3.6
F3_Flow = np.array(df['F3_CURR_FLW/PV.CV'])/3.6
Ftot_Flow = (F1_Flow) + (API_Flow) + (F3_Flow)
x1_in = F1_Flow/Ftot_Flow
x2_in = API_Flow/Ftot_Flow
x3_in = F3_Flow/Ftot_Flow
Blend_Wt = np.array(df['BL_CURR_WGT/PV.CV'])*1000
API_x2 = (np.array(df['API_CONCEN1/PV.CV']) + .4)/100
RTD_X1 = np.array(df['RTD-4/XO_L1.CV'])
RTD_X2 = np.array(df['RTD-4/XO_L2.CV'])
RTD_X3 = np.array(df['RTD-4/XO_L3.CV'])
'''
present concentration inputs as mass % in a matrix of the following dimensions: 
X_in[concentration @ time tn, interval = 1 sec][concentration at steam x, stream increases (i.e. stream 1 is @ column 0)]
'''
X_in = np.array([x1_in, x2_in, x3_in]).T 

x_streams = len(X_in[0]) #Get number of streams
"""User inputs"""
Ncstr = int(input("Enter number of CSTRs (must be a whole number): "))
initTime = int(input("Enter initial sample time to use (must be a whole number): "))
sampleSize = int(input("Enter number of samples to use (must be a whole number): "))
q1 = float(input("Enter % backmix (value from 0-1): "))

"""Generate input matrices"""
yIn = X_in[initTime:(sampleSize + initTime)][::] #grab ALL ( [::] ) sampled concentrations (F1,F2,F3) starting from a specified time and ending with the specified offset
mIn = list(Ftot_Flow[initTime:(initTime + sampleSize)][::])
M = list(Blend_Wt[initTime:(initTime + sampleSize)][::])
API_Conc = API_x2[initTime:(sampleSize + initTime)]
yInitCnd = X_in[0,::] # give me [F1_0,F2_0,F3_0] 
yInitCnd = np.tile(yInitCnd, reps=(Ncstr,1)).T

print(f'API concentration array size: {np.shape(API_Conc)}')
print(f'y Initial Conditions shape is: {np.shape(yInitCnd)}')
assert list(np.shape(yInitCnd)) == [x_streams, Ncstr], "Initial condition shape wrong"

print(cstrRT(yInitCnd, yIn, M, q1, mIn))
# Initiate plots
# fig, axs = plt.subplots(4)
# axs[3].plot(x3, dMdt, 'k-')
# axs[2].plot(x3, massReal, 'k-')
# axs[2].set_xlabel("time"), axs[2].set_ylabel("Total Mass(x)"), axs[2].set_title("Total Mass Over Time")
# axs[1].plot(x_streams*[0], yCstr.transpose(1,0)[0,::], 'go', x3, measuredValue, 'b-' , x_streams*[(tn - 1)], yIn[(tn - 1),::], 'ro') # initialize plot
# axs[1].set_xlabel("time"), axs[1].set_ylabel("concentration(x)"), axs[1].set_title("Concetrations of Each Stream Over Time")
# axs[0].plot(0, yCstr.transpose(1,0)[0,apiStream], 'go', x3, measuredValue, 'b-', tn - 1, yIn[(tn - 1),1], 'ro',) # initialize plot
# axs[0].set_xlabel("time"), axs[0].set_ylabel("concentration(x)"), axs[0].set_title("Concetration of Predicated vs Measured API Over Time")
plt.show()