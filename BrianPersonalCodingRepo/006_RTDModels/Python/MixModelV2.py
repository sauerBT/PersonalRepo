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
    from tqdm import tqdm

    # Calculating step size
    h = (xn-x0)/n
    xout = np.linspace(x0,xn,n)
    yn = np.empty((0)) # initialize output array
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
            yn = np.dstack([yn, y0])
        x0 = x0+h
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

def cstrSimp(y, t, y0, M, dMdt, q, m11, x, N):

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
    Mn = M/N
    dMdt = (dMdt/N)

    if (N == 1):
        # CSTR 1 exit rate
        m31 = (m11 - dMdt)
    elif (N == 2):
        # CSTR 1 exit rate
        m31 = (m11 - dMdt)/(1-q)
        # CSTR 2 back flow
        m41 = m31*q
        #   CSTR 2 exit flow
        m32 = (m31 - m41 - dMdt)
    elif (N == 3):
        # CSTR 1 exit rate
        m31 = (m11 - dMdt)/(1-q)
        # CSTR 2 back flow
        m41 = m31*q
        # CSTR 2 exit flow
        m32 = (m31 - m41 - dMdt)/(1-q)
        # CSTR 3 back flow
        m42 = m32*q
        # CSTR 3 exit flow
        m33 = (m32 - m42 - dMdt)

    dydt = np.empty((0)) # initialize differential equation array
    '''
    for i in range(x):
        if (Ncstr == 1):
            # Single CSTR (Ncstr = 1)
            exp_CSTR = (1/Mn)*(m11*y0[i]- m31*y[i][0] - y[i][0]*(m11 - m31))
        elif (Ncstr == 2):
            cstrOne = (1/Mn)*(m11*y0[i] + m41*y[i][1] - m31*y[i][0] - y[i][0]*(m11 + m41 - m31))
            cstrTwo = (1/Mn)*(m31*y[i][0] - m32*y[i][1] - m41*y[i][1] - y[i][1]*(m31 - m32 - m41))
            exp_CSTR = np.array([cstrOne, cstrTwo])
        elif (Ncstr == 3):
            # Three CSTR (Ncstr = 3)
            cstrOne = (1/Mn)*(m11*y0[i] + m41*y[i][1]- m31*y[i][0] - y[i][0]*(m11 + m41 - m31)) # checked good
            cstrTwo = (1/Mn)*(m31*y[i][0] + m42*y[i][2] - m41*y[i][1] - m32*y[i][1] - y[i][1]*(m31 + m42 - m32 - m41)) # checked good
            cstrThree = (1/Mn)*(m32*y[i][1] - m33*y[i][2] - m42*y[i][2] - y[i][2]*(m32 - m33 - m42)) # checked good
            exp_CSTR = np.array([cstrOne, cstrTwo, cstrThree])
        '''
    for i in range(x):
        if (Ncstr == 1):
            # Single CSTR (Ncstr = 1)
            exp_CSTR = (m11*(y0[i] - y[i][0]))/Mn
        elif (Ncstr == 2):
            cstrOne = (m11*(y0[i] - y[i][0]) + m41*(y[i][1] - y[i][0]))/Mn
            cstrTwo = (m31*(y[i][0] - y[i][1]))/Mn
            exp_CSTR = np.array([cstrOne, cstrTwo])
        elif (Ncstr == 3):
            # Three CSTR (Ncstr = 3)
            cstrOne = (m11*(y0[i] - y[i][0]) + m41*(y[i][1] - y[i][0]))/Mn # checked good
            cstrTwo = (m31*(y[i][0] - y[i][1]) + m42*(y[i][2] - y[i][1]))/Mn # checked good
            cstrThree = (m32*(y[i][1] - y[i][2]))/Mn # checked good
            exp_CSTR = np.array([cstrOne, cstrTwo, cstrThree])

        if (i == 0):
            dydt = np.append(dydt, exp_CSTR)
        else:
            dydt = np.vstack([dydt, exp_CSTR])
    assert np.shape(dydt) == np.shape(y), 'CSTR ODE output wrong size'
   
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

    m = np.empty((0))
    for n in range(N):
        if (n + 1) == N:
            m3n = m_in - (N*dMndt)
            m = np.append(m,m3n)
        else:
            m3n = (m_in - ((n+1)*dMndt))/(1-q)
            m = np.append(m,m3n)
    n = 0

    dydt = np.empty((0)) # initialize differential equation array

    '''
    for i in range(x):
        CSTR_n = np.empty((0)) # initialize differential equation array
        if (N == 1):
            CSTR_One = m_in*(y0[i] - y[i])/Mn
            CSTR_n = np.append(CSTR_n, CSTR_One)
            #print('cnd1')
        elif (N > 1):
            for n in range(N):
                if (n == 0) and (n != (N-1)):
                    CSTR_One = (m_in*(y0[i] - y[i][0])/Mn) + (q*(m_in - dMndt)*(y[i][1] - y[i][0]))/((1 - q)*Mn)
                    #print('cnd2')
                    CSTR_n = np.append(CSTR_n, CSTR_One)
                elif (n > 0) and (n < (N-1)):
                    CSTR_x = ((m_in - (n)*dMndt)*(y[i][n-1] - y[i][n]) + (q*(m_in - (n+1)*dMndt)*(y[i][n+1] - y[i][n])))/((1 - q)*Mn)
                    #print('cnd3')
                    CSTR_n = np.append(CSTR_n, CSTR_x)
                elif (n == (N-1)):
                    CSTR_N = ((m_in - (n)*dMndt)*(y[i][n-1] - y[i][n]))/Mn
                    #print('cnd4')
                    CSTR_n = np.append(CSTR_n, CSTR_N)
    '''
    for i in range(x):
        CSTR_n = np.empty((0)) # initialize differential equation array
        if (N == 1):
            CSTR_One = m_in*(y0[i] - y[i])/Mn
            CSTR_n = np.append(CSTR_n, CSTR_One)
            #print('cnd1')
        elif (N > 1):
            for n in range(N):
                if (n == 0) and (n != (N-1)):
                    CSTR_One = (m_in*(y0[i] - y[i][n]) + q*m[n]*(y[i][n+1] - y[i][n]))/Mn
                    #print('cnd2')
                    CSTR_n = np.append(CSTR_n, CSTR_One)
                elif (n > 0) and (n < (N-1)):
                    CSTR_x = (m[n-1]*(y[i][n-1] - y[i][n]) + q*m[n]*(y[i][n+1] - y[i][n]))/Mn
                    #print('cnd3')
                    CSTR_n = np.append(CSTR_n, CSTR_x)
                elif (n == (N-1)):
                    CSTR_N = (m[n-1]*(y[i][n-1] - y[i][n]))/Mn
                    #print('cnd4')
                    CSTR_n = np.append(CSTR_n, CSTR_N)

        if (i == 0): # base case
            dydt = np.append(dydt, CSTR_n)
        else:
            dydt = np.vstack([dydt, CSTR_n])
    assert np.shape(dydt) == np.shape(y), 'CSTR ODE output wrong size'
    return dydt

def cstrRandInit(x,N):
    #Set initial conditions
    yinit_intermediate = np.random.rand(x) # randomize initial concentration
    yinit = yinit_intermediate/yinit_intermediate.sum(axis=0,keepdims=1).T # Force initial concentrations to add up to zero
    yinit = np.expand_dims(yinit, axis = 1)
    yinit = np.tile(yinit,(1,N))
    return yinit

#Set constants
print("Enter number of streams")
x = int(input())
print("Enter number of CSTRs (1, 2 or 3)")
Ncstr = int(input())

yin_intermediate = np.random.rand(x) # randomize input concentrations
yin = yin_intermediate/yin_intermediate.sum(axis=0,keepdims=1) # Force input concentrations to add up to zero

M = 100 # total mass
Mss = 100 # mass at steady state
q1 = .9 # % backmix
q2 = 0 # % backmix
m11 = 1 # input flow rate

# Update Mass
[M_cv, dMdt] = rossiter(M, Mss, m11, Ncstr)

yinit = cstrRandInit(x,Ncstr)

# Set time points
t0 = int(input("Enter initial time"))
tn = int(input("Enter end time"))
nsteps = int(input("Enter number of time steps"))
t = np.linspace(t0, tn, nsteps)
# Solve ODE
#y_odeint = odeint(cstr, y_init, t, args=(yin, M_cv, dMdt, q, m11, x, Ncstr))
[x_n,y_rk4_n] = rk4_2d(cstrN, x0 = t0, y0 = yinit, xn = tn, n=nsteps, args=(yin, M_cv, dMdt, q1, m11, x, Ncstr))
[x_old,y_rk4_old] = rk4_2d(cstrSimp, x0 = t0, y0 = yinit, xn = tn, n=nsteps, args=(yin, M_cv, dMdt, q1, m11, x, Ncstr))

#plot ODE solutions
if (Ncstr == 1): #base case
    plt.plot(x_n,y_rk4_n[::, ::, 0], 'm.', x_old,y_rk4_old[::, ::, 0], 'k-', x*[t0], yinit.transpose(1,0)[0,::], 'go', x*[tn], yin, 'ro')
    plt.xlabel("time")
    plt.ylabel("concentration(x)")
    plt.show()
else:
    fig, axs = plt.subplots(Ncstr)
    for i in range(Ncstr): #iterate to plot output of each cstr
        axs[i].plot(x_n,y_rk4_n[::, ::, i], 'm.', x_old,y_rk4_old[::, ::, i], 'k-', x*[t0], yinit.transpose(1,0)[i,::], 'go', x*[tn], yin, 'ro')
        title = 'CSTR %i output concetrations vs time' % (i+1)
        axs[i].set_title(title)
    plt.show()



plt.plot(x_n,y_rk4_n[::, ::, Ncstr - 1], 'm.', x_old,y_rk4_old[::, ::, Ncstr - 1], 'k-', x*[t0], yinit.transpose(1,0)[Ncstr-1,::], 'go', x*[tn], yin, 'ro')
plt.xlabel("time")
plt.ylabel("concentration(x)")
plt.show()

