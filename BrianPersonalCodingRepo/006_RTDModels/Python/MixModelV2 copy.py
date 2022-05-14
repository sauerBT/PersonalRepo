# -*- coding: utf-8 -*-
"""
Created on Thurday Sep 9 2021


@author: Brian Sauerborn
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint,RK45
import sympy as sym
from MixModelV2 import *
from tqdm import tqdm
#Set constants
print("Enter number of streams")
x = int(input())
print("Enter number of CSTRs (1, 2 or 3)")
Ncstr = int(input())

yin_intermediate = np.random.rand(x) # randomize input concentrations
yin = yin_intermediate/yin_intermediate.sum(axis=0,keepdims=1) # Force input concentrations to add up to zero

M = 100 # total mass
Mss = 100 # mass at steady state
q1 = .5 # % backmix
q2 = 0 # % backmix
m11 = 5 # input flow rate

# Update Mass
[M_cv, dMdt] = rossiter(M, Mss, m11)

yinit = cstrRandInit(x,Ncstr)

# Set time points
t0 = int(input("Enter initial time"))
tn = int(input("Enter end time"))

[x_old,y_rk4_old] = rk4_2d(cstrN, x0 = t0, y0 = yinit, xn = tn, n=(tn*10), args=(yin, M, dMdt, q1, m11, x, Ncstr))

xplot = np.empty((0))
yplot = np.empty((0))
plt.plot(x*[0], yinit.transpose(1,0)[0,::], 'go', x*[tn], yin, 'ro', x_old,y_rk4_old[::, ::, Ncstr - 1], 'k-') # initialize plot
plt.xlabel("time")
plt.ylabel("concentration(x)")
plt.pause(0.005)
for t in tqdm(range(tn+1)):
    # Solve ODE
    [x_n,y_rk4_n] = rk4_2d(cstrN, x0 = 0, y0 = yinit, xn = 1, n=10, args=(yin, M_cv, dMdt, q1, m11, x, Ncstr))
    if (t == 0): # base case
        xplot = np.append(xplot, t)
        yplot = y_rk4_n[9,::,::]
        yinit = yplot
        #print(yplot)
        plt.plot(x*[t+1], yplot[::, (Ncstr - 1)], 'm.')
        plt.pause(0.005)
    else:
        xplot = np.append(xplot, t)
        yplot = np.dstack([yplot, y_rk4_n[9,::,::]])
        yinit = yplot[::,::,t]
        #print(yplot[::,::,t])
        plt.plot(x*[t+1], yplot[::, (Ncstr - 1), t], 'm.')
        plt.pause(0.005)
yplot = yplot.transpose(2, 0, 1) # transpose y output to to following dimensions: yn[iteration #][component #][CSTR #]
plt.show()

'''
#plot ODE solutions
if (Ncstr == 1): #base case
    plt.plot(xplot,yplot[::, ::, 0], 'm.', x*[xplot[0]], yinit.transpose(1,0)[0,::], 'go', x*[xplot[tn]], yin, 'ro')
    plt.xlabel("time")
    plt.ylabel("concentration(x)")
    plt.show()
else:
    fig, axs = plt.subplots(Ncstr)
    for i in range(Ncstr): #iterate to plot output of each cstr
        axs[i].plot(xplot,yplot[::, ::, i], 'm.', x*[xplot[0]], yinit.transpose(1,0)[i,::], 'go', x*[xplot[tn]], yin, 'ro')
        title = 'CSTR %i output concetrations vs time' % (i+1)
        axs[i].set_title(title)
    plt.show()
'''

'''
plt.plot(x_n,y_rk4_n[::, ::, Ncstr - 1], 'm.', x_old,y_rk4_old[::, ::, Ncstr - 1], 'k-', x*[t0], yinit.transpose(1,0)[Ncstr-1,::], 'go', x*[tn], yin, 'ro')
plt.xlabel("time")
plt.ylabel("concentration(x)")
plt.show()

'''