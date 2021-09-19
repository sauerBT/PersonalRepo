# -*- coding: utf-8 -*-
"""
Created on Thurday Sep 9 2021


@author: Brian Sauerborn
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint,RK45
import sympy as sym

def compute_cost(AL, Y):
    """
    Implement the cost function defined by equation (7).

    Arguments:
    AL -- probability vector corresponding to your label predictions, shape (1, number of examples)
    Y -- true "label" vector (for example: containing 0 if non-cat, 1 if cat), shape (1, number of examples)

    Returns:
    cost -- cross-entropy cost
    """
    
    m = Y.shape[0]

    # Compute loss from aL and y.
    ### START CODE HERE ### (≈ 1 lines of code)
    cost = (1/m)*np.sum((AL - Y)**2)  # Cost function as a sum square error
    #   cost = (-1/m)*np.sum(Y*np.log(AL) + (1-Y)*np.log(1-AL))
    ### END CODE HERE ###
    
    cost = np.squeeze(cost)      # To make sure your cost's shape is what we expect (e.g. this turns [[17]] into 17).
    assert(cost.shape == ())
    
    return cost

def rk4_1d(func,x0,y0,xn,n,args):
    from tqdm import tqdm

    # Calculating step size
    h = (xn-x0)/n
    xout = np.linspace(x0,xn,n)
    #xout = np.squeeze(xout)
    yn = np.empty((0))
    #print(np.shape(y0))
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
    from tqdm import tqdm

    # Calculating step size
    h = (xn-x0)/n
    y0_Shape = y0.shape[1]
    xout = np.linspace(x0,xn,n)
    #xout = np.squeeze(xout)
    yn = np.empty((0))
    #print(np.shape(y0))
    print("------------------------------------------------------------------------------------------------------------------------------")
    print("Solving Differential...")
    print("------------------------------------------------------------------------------------------------------------------------------")
    for i in tqdm(range(n)):
        #print(i)
        #print(np.shape(y0))
        k1 = h * (func(y0, x0,*args))
        k1 = np.expand_dims(k1, axis = 1)
        k1 = np.tile(k1, y0_Shape)
        #print(np.shape(k1))
        #print(k1)
        k2 = h * (func((y0+k1/2), (x0+h/2), *args))
        k2 = np.expand_dims(k2, axis = 1)
        k2 = np.tile(k2, y0_Shape)
        #print(np.shape(k2))
        k3 = h * (func((y0+k2/2), (x0+h/2), *args))
        k3 = np.expand_dims(k3, axis = 1)
        k3 = np.tile(k3, y0_Shape)
        #print(np.shape(k3))
        k4 = h * (func((y0+k3), (x0+h), *args))
        k4 = np.expand_dims(k4, axis = 1)
        k4 = np.tile(k4, y0_Shape)
        #print(np.shape(k4))
        k = (k1+2*k2+2*k3+k4)/6
        #print(np.shape(k))
        if (i==0): # base case
            y0 = y0 + k
            #print(y0)
            yn = y0
            #print(yn)
        else:
            y0 = y0 + k
            #print(yn)
            #print(y0)
            yn = np.dstack([yn, y0])
        x0 = x0+h
        #print(str((i/n)*100))
    yn = yn.transpose(2, 0, 1)
    return [xout,yn]

def rossiter(M, Mss, m11, Ncstr):
    dMdt = (Mss - M)*(m11/M)/Ncstr # Rossiter Mass accumulation simulation
    M_cv = M + dMdt
    return [M_cv, dMdt]

def cstr(y, t, y0, M, dMdt, q, m11, x, Ncstr):

    # y(i) is the output concentration of CSTR 1 for each component, i = 3
    # y0(i) is the initial input concentration of CSTR 1 for each component, i = 3
    # m11 is the input mass flow rate of CSTR 1
    # m31 is the output mass flow rate of CSTR 1
    # m41 is the backflow mass flow rate from CSTR 2 to CSTR 1
    # m32 is the output mass flow rate of CSTR 2
    # m42 is the backflow mass flow rate from CSTR 3 to CSTR 2
    # m33 is the output mass flow rate of CSTR 3
    # x is the number of material streams
    # Ncstr is the number of CSTRs
    
    # Below are the constants for the differential equations
    Mcstr = M/Ncstr
    dMdt_new = (dMdt/Ncstr)

    if (Ncstr == 1):
        # CSTR 1 exit rate
        m31 = (m11 - dMdt_new)
    elif (Ncstr == 2):
        # CSTR 1 exit rate
        m31 = (m11 - dMdt_new)/(1-q)
        # CSTR 2 back flow
        m41 = m31*q
        #   CSTR 2 exit flow
        m32 = (m31 - m41 - dMdt_new)
    elif (Ncstr == 3):
        # CSTR 1 exit rate
        m31 = (m11 - dMdt_new)/(1-q)
        # CSTR 2 back flow
        m41 = m31*q
        # CSTR 2 exit flow
        m32 = (m31 - m41 - dMdt_new)/(1-q)
        # CSTR 3 back flow
        m42 = m32*q
        # CSTR 3 exit flow
        m33 = (m32 - m42 - dMdt_new)

    dydt = np.empty((0)) # initialize differential equation array

    for i in range(x):
        if (Ncstr == 1):
            # Single CSTR (Ncstr = 1)
            exp_CSTR = (1/Mcstr)*(m11*y0[i]- m31*y[i] - y[i]*(m11 - m31))
        elif (Ncstr == 2):
            cstrOne = (1/Mcstr)*(m11*y0[i] + m41*y[i+1] - m31*y[i] - y[i]*(m11 + m41 - m31))
            cstrTwo = (1/Mcstr)*(m31*y[i] - m32*y[i+1] - m41*y[i+1] - y[i+1]*(m31 - m32 - m41))
            exp_CSTR = np.array([cstrOne, cstrTwo])
        elif (Ncstr == 3):
            # Three CSTR (Ncstr = 3)
            cstrOne = (1/Mcstr)*(m11*y0[i] + m41*y[i+1]- m31*y[i] - y[i]*(m11 + m41 - m31)) # checked good
            cstrTwo = (1/Mcstr)*(m31*y[i] + m42*y[i+2] - m41*y[i+1] - m32*y[i+1] - y[i+1]*(m31 + m42 - m32 - m41)) # checked good
            cstrThree = (1/Mcstr)*(m32*y[i+1] - m33*y[i+2] - m42*y[i+2] - y[i+2]*(m32 - m33 - m42)) # checked good
            exp_CSTR = np.array([cstrOne, cstrTwo, cstrThree])

        dydt = np.append(dydt, exp_CSTR)

    return dydt

def cstrN(y, t, y0, M, dMdt, q, m_in, x, N):

    assert N>0, "The number of CSTRs(N) must be greater than zero"
    # y(i) is the output concentration of CSTR 1 for each component, i = 3
    # y0(i) is the initial input concentration of CSTR 1 for each component, i = 3
    # m_in is the input mass flow rate of CSTR 1
    # m3n is the output mass flow rate of CSTR n of N
    # m4n is the backflow mass flow rate from CSTR n to CSTR n-1 of N
    # x is the number of material streams
    # N is the number of total CSTRs (and consequently the total number of differential equations)
    # n is the current CSTR differential equation (i.e. Differential equation of CSTR n of N)
    
    # Below are the constants for the differential equations
    Mn = M/N # Mass term for the current CSTR differential equation (i.e. mass for CSTR n of N)
    dMndt = (dMdt/N) # Mass accumulation term for the current CSTR differential equation (i.e. mass accumulation for CSTR n of N)
    dydt = np.empty((0)) # initialize differential equation array

    for i in range(x):
        if (N == 1):
            CSTR_n = m_in*(y0[i] - y[i])/Mn
            dydt = np.append(dydt, CSTR_n)
        elif (N > 1):
            for n in range(N):
                if (n == 1) and (n != N):
                    CSTR_n = (m_in*(y0[i] - y.item(i,0))/Mn) + (q*(m_in - dMndt)*(y.item(i,1) - y.item(i,0)))/((1 - q)*Mn)
                    dydt = np.append(dydt, CSTR_n)
                elif (n > 1) and (n > N):
                    CSTR_n = ((m_in - (n-1)*dMndt)*(y.item(i,n-1) - y.item(i,n)) + (q*(m_in - n*dMndt)*(y.item(i,n+1) - y.item(i,n))))/((1 - q)*Mn)
                    dydt = np.append(dydt, CSTR_n)
                elif (n == N):
                    CSTR_n = ((m_in - (n-1)*dMndt)*(y.item(i,n-1) - y.item(i,n)))/Mn
                    dydt = np.append(dydt, CSTR_n)
    return dydt
#Set constants
print("Enter number of streams")
x = int(input())
print("Enter number of CSTRs (1, 2 or 3)")
Ncstr = int(input())
y0_intermediate = np.random.rand(x) # randomize input concentrations
yin = y0_intermediate/y0_intermediate.sum(axis=0,keepdims=1) # Force input concentrations to add up to zero
#print(y0)
M = 100
Mss = 100
q = 0
m11 = 1

# Update Mass
[M_cv, dMdt] = rossiter(M, Mss, m11, Ncstr)

#Set initial conditions
yinit_intermediate = np.random.rand(x, Ncstr) # randomize initial concentration
yinit = yinit_intermediate/yinit_intermediate.sum(axis=0,keepdims=1) # Force initial concentrations to add up to zero
#print(yinit)
#print(np.sum(yinit, axis=0))
#print(np.sum(yinit, axis=1))
y_init = np.resize(yinit, (x*Ncstr))
y_init = np.squeeze(y_init)
#assert np.shape(y_init)[]
# Set time points
t0 = int(input("Enter initial time"))
tn = int(input("Enter end time"))
nsteps = int(input("Enter number of time steps"))
t = np.linspace(t0, tn, nsteps)
# Solve ODE
y_odeint = odeint(cstr, y_init, t, args=(yin, M_cv, dMdt, q, m11, x, Ncstr))
[x_n,y_rk4_n] = rk4_2d(cstrN, x0 = t0, y0 = yinit, xn = tn, n=nsteps, args=(yin, M_cv, dMdt, q, m11, x, Ncstr))
[x_old,y_rk4_old] = rk4_1d(cstr, x0 = t0, y0 = y_init, xn = tn, n=nsteps, args=(yin, M_cv, dMdt, q, m11, x, Ncstr))
#plt.plot(x,y_rk4[::1,::Ncstr], 'r-',t,y_odeint[::1,::Ncstr], 'b-')

plt.plot(x_n,y_rk4_n[::, ::, Ncstr - 1], 'r-',t,y_odeint[::1,::Ncstr], 'b-', x_old,y_rk4_old[::1,::Ncstr], 'k-', x*[t0], yinit.transpose(1,0)[Ncstr-1,::], 'go', x*[tn], yin, 'ro')
#plt.plot(t,y_odeint[::1,::Ncstr], 'b-')
#print(y[::1,::Ncstr])
#print(np.sum(y[::1,::Ncstr], axis=1)) # check values all add up to 1
# Plot results
#plt.plot(x,y[::1,::Ncstr])

plt.xlabel("time")
plt.ylabel("concentration(x)")
plt.show()

