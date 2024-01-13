# -*- coding: utf-8 -*-
"""
Created on Thurday Sep 9 2021
@author: Brian Sauerborn
"""
import numpy as np
import matplotlib.pyplot as plt
from CSTR_Models import *
from NumericalMethods import *
import math
import pandas as pd
import statistics

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
    x3 = np.linspace(0, tn, tn)
    xplot = np.empty((0))
    yplot = np.empty((0))
    dMdt = [] # initialize change in mass calculations
    for m in range(len(massReal)): # calculate the change in mass at each interval
        if m == 0: # base case
            dMdt.append(0)
        else:
            dMdt.append(M[m] - M[m-1])
    apiStream = 1

    # Initiate plots
    #fig, axs = plt.subplots(4)
    #axs[3].plot(x3, dMdt, 'k-')
    #axs[2].plot(x3, massReal, 'k-')
    #axs[2].set_xlabel("time"), axs[2].set_ylabel("Total Mass(x)"), axs[2].set_title("Total Mass Over Time")
    #axs[1].plot(x_streams*[0], yCstr.transpose(1,0)[0,::], 'go', x3, measuredValue, 'b-' , x_streams*[(tn - 1)], yIn[(tn - 1),::], 'ro') # initialize plot
    #axs[1].set_xlabel("time"), axs[1].set_ylabel("concentration(x)"), axs[1].set_title("Concetrations of Each Stream Over Time")
    #axs[0].plot(0, yCstr.transpose(1,0)[0,apiStream], 'go', x3, measuredValue, 'b-', tn - 1, yIn[(tn - 1),1], 'ro',) # initialize plot
    #axs[0].set_xlabel("time"), axs[0].set_ylabel("concentration(x)"), axs[0].set_title("Concetration of Predicated vs Measured API Over Time")
    #plt.pause(0.005)
    # Start Solver
    for t in tqdm(range(tn)):
        # Solve ODE
        if (t == 0): # base case
            [x_n,y_rk4_n] = rk4_2d(cstrN, x0 = 0, y0 = yCstr, xn = 1, n=10, args=(yIn[t,::], massReal[t], dMdt[t], q, mIn[t], x_streams, Ncstr))
            assert y_rk4_n.shape[1] == x_streams, f'number of solution streams ({y_rk4_n.shape[2]}) does not match the number of input streams ({x_streams})'
            xplot = np.append(xplot, t)
            yplot = y_rk4_n[9,::,::]
            yCstr = yplot
            #axs[1].plot(x_streams*[t+1], yplot[::, (Ncstr - 1)], 'm.', markersize = 1)
            #axs[0].plot([t+1], yplot[apiStream, (Ncstr - 1)], 'm.', markersize = 1)
            #plt.pause(0.000000000001)
        else:
            [x_n,y_rk4_n] = rk4_2d(cstrN, x0 = 0, y0 = yCstr, xn = 1, n=10, args=(yIn[t,::], massReal[t], dMdt[t], q, mIn[t], x_streams, Ncstr))
            assert y_rk4_n.shape[1] == x_streams, f'number of solution streams ({y_rk4_n.shape[2]}) does not match the number of input streams ({x_streams})'
            xplot = np.append(xplot, t)
            yplot = np.dstack([yplot, y_rk4_n[9,::,::]])
            yCstr = yplot[::,::,t]
            #axs[1].plot(x_streams*[t+1], yplot[::, (Ncstr - 1), t], 'm.', markersize = 1)
            #axs[0].plot([t+1], yplot[apiStream, (Ncstr - 1), t], 'm.', markersize = 1)
            #plt.pause(0.000000000001)
    yplot = yplot.transpose(2, 0, 1) # transpose y output to to following dimensions: yn[iteration #][component #][CSTR #]
    return yplot

def readRTDExp(file):
    my_export = pd.read_csv(file, index_col = 0, header = 0, skiprows = 0) #before index_col = 0 but excluded first column
    df = my_export.set_index('Date')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return [df]

# Import and format RTD data
file = 'C:\\Users\\brian\\iCloudDrive\\nCSTR\\nCSTR\\IMA_RTD_Data-v1.csv'
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
yInitCnd = X_in[0,::]
yInitCndDiff = X_in[0,::]
#yInitCnd = np.tile(yInitCnd, reps=(Ncstr,1)).T
yInitCndDiff = np.tile(yInitCndDiff, reps=(Ncstr - 1,1)).T

print(f'API concentration array size: {np.shape(API_Conc)}')
print(f'y Initial Conditions shape is: {np.shape(yInitCnd)}')
#assert list(np.shape(yInitCnd)) == [x_streams, Ncstr], "Initial condition shape wrong"

""" y_q = cstrRT(yInitCnd, yIn, M, q1, mIn, Ncstr, API_Conc)
y_diff = cstrRT(yInitCndDiff, yIn, M, 0, mIn, Ncstr - 1, API_Conc)
y_norm = cstrRT(yInitCnd, yIn, M, 0, mIn, Ncstr, API_Conc)
y_plot_q = y_q[::, 1, Ncstr - 1]
y_plot_diff = y_diff[::, 1, Ncstr - 2]
y_plot_norm = y_norm[::, 1, Ncstr - 1]
yplotx = np.linspace(0, len(y_plot_q.T), len(y_plot_q.T))
ax = plt.subplot(1,1,1)
#axs[0].plot(0, yInitCnd.transpose(1,0)[0,1], 'go', yplotx, API_Conc, 'b-', len(yIn) - 1, yIn[(len(yIn) - 1),1], 'ro',) # initialize plot
ax.plot(yplotx, API_Conc, 'b-') # initialize plot
ax.set_xlabel("time"), ax.set_ylabel("concentration(x)"), ax.set_title("Concetration of Predicated vs Measured API Over Time")
ax.plot(yplotx, y_plot_q, 'm-', yplotx, y_plot_diff, 'b.', yplotx, y_plot_norm, 'g.', markersize = 1)
ax.legend(["NIR API", f"API {Ncstr} CSTR w/ q={q1}", f"API {Ncstr - 1} CSTR w/ q=0", f"API {Ncstr} CSTR w/ q=0"]) """
#axs[0].plot(yplotx, y_plot_q, 'm.', yplotx, y_plot_norm, 'b-', markersize = 1)
#axs[1].plot(x_streams*[0], yInitCnd.transpose(1,0)[0,::], 'go', yplotx, API_Conc, 'b-' , x_streams*[(len(yIn) - 1)], yIn[(len(yIn) - 1),::], 'ro') # initialize plot
#axs[1].set_xlabel("time"), axs[1].set_ylabel("concentration(x)"), axs[1].set_title("Concetrations of Each Stream Over Time")
#print(1000000*np.square(API_Conc -cstrRT(yInitCnd, yIn, M, q1, mIn, round(Ncstr), API_Conc)[::, 1, Ncstr - 1]))

def cost(x):
    N = int(math.ceil(x[1]))
    yInitCnd = np.tile(X_in[0,::], reps=(N,1)).T

    ConcPAT = cstrRT(yInitCnd, yIn, M, x[0], mIn, N, API_Conc)[::, 1, N - 1]
    c = 100*np.sum(np.square((API_Conc / np.linalg.norm(API_Conc)) - (ConcPAT / np.linalg.norm(ConcPAT))))
    print(f'Current Guesses: q={x[0]}, n={x[1]} -> {N}, Cost={c}')

    return (c)

""" def cost_MINP(x1,x2,X_in):
    print(f'Current Guesses: q={x1.value}, n={x2.value}')
    yInitCnd = np.tile(X_in[0,::], reps=(x2.value)).T
    ConcPAT = cstrRT(yInitCnd, yIn, M, x1.value, mIn, x2.value, API_Conc)[::, 1, x2 - 1]
    c = np.sum(np.square((API_Conc / np.linalg.norm(API_Conc)) - (ConcPAT / np.linalg.norm(ConcPAT))))
    print(f'Cost={c}')
    return (c) """


from scipy.optimize import minimize,brute



b1 = (0.0,.99)
b2 = slice(1,6,1)
bnds = (b1,b2)

""" from gekko import GEKKO
m = GEKKO() # create GEKKO model
#create integer variables
x1 = m.Var(lb=0,ub=.99)
x2 = m.Var(integer=True,lb=1,ub=8)
x1.value = q1
x2.value = Ncstr
#create continuous variable
m.Minimize(cost_MINP(x1,x2,X_in))
m.options.SOLVER = 1 # APOPT solver
m.solve(disp=False)
print('x1: ' + str(x1.value[0]))
print('x2: ' + str(x2.value[0])) """

sol = brute(cost, bnds, disp=True,finish=None)

x0 = np.array([sol[0],sol[1]])
b1 = (0.0,.99)
b2 = (sol[1],sol[1])
bnds = (b1,b2)

LSE = minimize(cost, x0, bounds= bnds)

print("Done")

# plt.pause(0.005)
# plt.show()cstrRT(yInitCnd, yIn, M, x[0], mIn, round(x[1]), API_Conc)[::, 1, Ncstr - 1]