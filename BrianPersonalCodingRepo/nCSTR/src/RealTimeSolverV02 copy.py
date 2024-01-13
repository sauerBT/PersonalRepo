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

def cstrRT(yCstr, yIn, massReal, q, mIn, Ncstr, measuredValue):
    """
    Simulates real time RTD model solver given a static set of sample data
    
    Arguments:
    yCstr -- given initial condition concentration values for the numerical solver, of shape (# streams, # CSTRs in series)
    yIn -- given measured input concentration values used for each cycle, of shape (# of samples, # of streams)
    massReal -- given measured input total mass, of shape (# of samples)
    q -- give backmix constant
    mIn -- give measured total mass flow rate input, of shape (# of samples)
    Ncstr -- given # of CSTRs
    measuredValue -- given measured API concentration, of shape (# of samples)

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

    # Start Solver
    for t in tqdm(range(tn)):
        # Solve ODE
        if (t == 0): # base case
            [x_n,y_rk4_n] = rk4_2d(cm.calculate_n_cstr, x0 = 0, y0 = yCstr, xn = 1, n=10, args=(yIn[t,::], massReal[t], dMdt[t], q, mIn[t]))
            assert y_rk4_n.shape[1] == x_streams, f'number of solution streams ({y_rk4_n.shape[2]}) does not match the number of input streams ({x_streams})'
            xplot = np.append(xplot, t)
            yplot = y_rk4_n[9,::,::]
            yCstr = yplot
        else:
            [x_n,y_rk4_n] = rk4_2d(cm.calculate_n_cstr, x0 = 0, y0 = yCstr, xn = 1, n=10, args=(yIn[t,::], massReal[t], dMdt[t], q, mIn[t]))
            assert y_rk4_n.shape[1] == x_streams, f'number of solution streams ({y_rk4_n.shape[2]}) does not match the number of input streams ({x_streams})'
            xplot = np.append(xplot, t)
            yplot = np.dstack([yplot, y_rk4_n[9,::,::]])
            yCstr = yplot[::,::,t]
    yplot = yplot.transpose(2, 0, 1) # transpose y output to to following dimensions: yn[iteration #][component #][CSTR #]
    return yplot

def readRTDExp(file):
    my_export = pd.read_csv(file, index_col = 0, header = 0, skiprows = 0) #before index_col = 0 but excluded first column
    df = my_export.set_index('Date')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return [df]

# Import and format RTD data
file = os.path.realpath('BrianPersonalCodingRepo\\nCSTR\\IMA_RTD_Data-v1.csv')
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
yIn = X_in[initTime:(sampleSize + initTime)][::]
mIn = list(Ftot_Flow[initTime:(initTime + sampleSize)][::])
M = list(Blend_Wt[initTime:(initTime + sampleSize)][::])
API_Conc = API_x2[initTime:(sampleSize + initTime)]
#x3 = np.linspace(0, sampleSize, sampleSize)
yInitCnd =     X_in[initTime,::]
yInitCndDiff = X_in[initTime,::]
yInitTriple =  X_in[initTime,::]
yInitDouble =  X_in[initTime,::]
yInitSingle =  X_in[initTime,::]

yInitCnd =     np.tile(yInitCnd,     reps=(Ncstr,1)).T
yInitTriple =  np.tile(yInitTriple,  reps=(3,1)).T
yInitDouble =  np.tile(yInitDouble,  reps=(2,1)).T
yInitSingle =  np.tile(yInitSingle,  reps=(1,1)).T
yInitCndDiff = np.tile(yInitCndDiff, reps=(Ncstr - 1,1)).T

print(f'API concentration array size: {np.shape(API_Conc)}')
print(f'y Initial Conditions shape is: {np.shape(yInitCnd)}')
assert list(np.shape(yInitCnd)) == [x_streams, Ncstr], "Initial condition shape wrong"
assert list(np.shape(yInitCndDiff)) == [x_streams, Ncstr - 1], "Initial condition shape wrong"
assert list(np.shape(yInitSingle)) == [x_streams, 1], "Initial condition shape wrong"
assert list(np.shape(yInitDouble)) == [x_streams, 2], "Initial condition shape wrong"
assert list(np.shape(yInitTriple)) == [x_streams, 3], "Initial condition shape wrong"

y_q =      cstrRT(yInitCnd,     yIn.tolist(), M, q1, mIn, Ncstr,     API_Conc)
y_diff =   cstrRT(yInitCndDiff, yIn.tolist(), M, 0,  mIn, Ncstr - 1, API_Conc)
y_norm =   cstrRT(yInitCnd,     yIn.tolist(), M, 0,  mIn, Ncstr,     API_Conc)
y_single = cstrRT(yInitSingle,  yIn.tolist(), M, 0,  mIn, 1,         API_Conc)
y_double = cstrRT(yInitDouble,  yIn.tolist(), M, 0,  mIn, 2,         API_Conc)
y_triple = cstrRT(yInitTriple,  yIn.tolist(), M, 0,  mIn, 3,         API_Conc)

y_plot_q = y_q[::, 1, Ncstr - 1]
y_plot_diff = y_diff[::, 1, Ncstr - 2]
y_plot_norm = y_norm[::, 1, Ncstr - 1]
y_plot_single = y_single[::, 1, 0]
y_plot_double = y_double[::, 1, 1]
y_plot_triple = y_triple[::, 1, 2]

yplotx = np.linspace(0, len(y_plot_q.T), len(y_plot_q.T))
ax = plt.subplot(1,1,1)
#axs[0].plot(0, yInitCnd.transpose(1,0)[0,1], 'go', yplotx, API_Conc, 'b-', len(yIn) - 1, yIn[(len(yIn) - 1),1], 'ro',) # initialize plot
ax.plot(yplotx, API_Conc, 'b-') # initialize plot
ax.set_xlabel("time"), ax.set_ylabel("concentration(x)"), ax.set_title("Concetration of Predicated vs Measured API Over Time")
"""ax.plot(yplotx, y_plot_q, 'm-', yplotx, y_plot_diff, 'o-', yplotx, y_plot_norm, 'g-', markersize = 1)
ax.legend(["NIR API", f"API {Ncstr} CSTR w/ q={q1}", f"API {Ncstr - 1} CSTR w/ q=0", f"API {Ncstr} CSTR w/ q=0"]) """
ax.plot(yplotx, y_plot_q, 'm-', yplotx, y_plot_diff, 'o-', yplotx, y_plot_single, 'g-', y_plot_double, 'k-', y_plot_triple, 'r-', markersize = 1)
ax.legend(["NIR API", f"API {Ncstr} CSTR w/ q={q1}", f"API {Ncstr - 1} CSTR w/ q=0", f"API 1 CSTR w/ q=0", f"API 2 CSTR w/ q=0", f"API 3 CSTR w/ q=0"])
#axs[0].plot(yplotx, y_plot_q, 'm.', yplotx, y_plot_norm, 'b-', markersize = 1)
#axs[1].plot(x_streams*[0], yInitCnd.transpose(1,0)[0,::], 'go', yplotx, API_Conc, 'b-' , x_streams*[(len(yIn) - 1)], yIn[(len(yIn) - 1),::], 'ro') # initialize plot
#axs[1].set_xlabel("time"), axs[1].set_ylabel("concentration(x)"), axs[1].set_title("Concetrations of Each Stream Over Time")
#print(1000000*np.square(API_Conc -cstrRT(yInitCnd, yIn, M, q1, mIn, round(Ncstr), API_Conc)[::, 1, Ncstr - 1]))


plt.pause(0.005)
plt.show()