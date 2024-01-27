# -*- coding: utf-8 -*-
"""
Created on Thurday Sep 9 2021
@author: Brian Sauerborn
"""
import numpy as np
import matplotlib.pyplot as plt
from numerical_methods import *
import cstr_models_helper as ch
import list_funcs as lf
import pandas as pd
import os

def readRTDExp(file):
    my_export = pd.read_csv(file, index_col = 0, header = 0, skiprows = 0) #before index_col = 0 but excluded first column
    df = my_export.set_index('Date')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return [df]

# Import and format RTD data
file = os.path.realpath('nCSTR\\IMA_RTD_Data-v1.csv')
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

dMdt: list[float] = ch.change_in_mass(M)
args1: list[tuple] = lf.generate_arg_list([yIn,M,dMdt,lf.generate_list_from_number(q1,sampleSize), mIn])
args2: list[tuple] = lf.generate_arg_list([yIn,M,dMdt,lf.generate_list_from_number(0,sampleSize), mIn])
y_q = np.array(ch.replay_ode_funcs(ch.calculate_n_cstr,yInitCnd,args1))
y_diff = np.array(ch.replay_ode_funcs(ch.calculate_n_cstr,yInitCndDiff,args2))
y_norm = np.array(ch.replay_ode_funcs(ch.calculate_n_cstr,yInitCnd,args2))
y_single = np.array(ch.replay_ode_funcs(ch.calculate_n_cstr,yInitSingle,args2))
y_double = np.array(ch.replay_ode_funcs(ch.calculate_n_cstr,yInitDouble,args2))
y_triple = np.array(ch.replay_ode_funcs(ch.calculate_n_cstr,yInitTriple,args2))
print(f'ODE solution shape: {np.shape(y_q)}')
print(f'Total time interval: {np.shape(y_q)[0]}')

y_plot_q = y_q[::,9,1,Ncstr - 1]
y_plot_diff = y_diff[::,9,1,Ncstr - 2]
y_plot_norm = y_norm[::,9,1,Ncstr - 1]
y_plot_single = y_single[::,9,1,0]
y_plot_double = y_double[::,9,1,1]
y_plot_triple = y_triple[::,9,1,2]

yplotx = np.linspace(0, sampleSize, sampleSize)
ax = plt.subplot(1,1,1)
ax.plot(yplotx, API_Conc, 'b-') # initialize plot
ax.set_xlabel("time"), ax.set_ylabel("concentration(x)"), ax.set_title("Concetration of Predicated vs Measured API Over Time")
ax.plot(yplotx, y_plot_q, 'm-', yplotx, y_plot_diff, 'o-', yplotx, y_plot_single, 'g-', y_plot_double, 'k-', y_plot_triple, 'r-', markersize = 1)
ax.legend(["NIR API", f"API {Ncstr} CSTR w/ q={q1}", f"API {Ncstr - 1} CSTR w/ q=0", f"API 1 CSTR w/ q=0", f"API 2 CSTR w/ q=0", f"API 3 CSTR w/ q=0"])

plt.pause(0.005)
plt.show()