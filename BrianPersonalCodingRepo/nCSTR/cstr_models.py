# -*- coding: utf-8 -*-
"""
Created on Thurday Sep 9 2021


@author: Brian Sauerborn
"""
import numpy as np
import cstr_models_helper as cm

# y(i) is the output concentration of CSTR for each component
# y0(i) is the initial input concentration of CSTR for each component
# m_in is the input mass flow rate of CSTR
# m3n is the output mass flow rate of CSTR n of N
# m4n is the backflow mass flow rate from CSTR n to CSTR n-1 of N
# x is the number of material streams
# N is the number of total CSTRs (and consequently the total number of differential equations)
# n is the current CSTR differential equation (i.e. Differential equation of CSTR n of N)
# Ouput (dydt) is a matrix containing CSTR output concentration change w.r.t. time and is formatted as follows: dydt[component number i][CSTR number n]
def cstrN(y: list[list[float]], t, y0: list[float], mass: float, dMdt: float, backmix: float, m_in: float):
    # Below are the constants for the differential equations
    n_cstr = len(y[0])
    mass_n = mass/n_cstr # Mass term for the current CSTR differential equation (i.e. mass for CSTR n of N)
    dMndt = (dMdt/n_cstr) # Mass accumulation term for the current CSTR differential equation (i.e. mass accumulation for CSTR n of N)

    # Create a matrix defining the mass flow output term for each CSTR
    return np.array(cm.n_cstr_ode(y.tolist(),y0,cm.generate_mass_out_list(m_in,dMndt,backmix,n_cstr),mass_n,backmix,m_in))

def rossiter(M, Mss, m11):
    dMdt = (Mss - M)*(m11/M) # Rossiter Mass accumulation simulation
    M_cv = M + dMdt
    return [M_cv, dMdt]
    
def mass_update(M, Mss, m11, M_Select):

    if (M_Select == 1):
        [M_cv, dMdt] = rossiter(M, Mss, m11)
    return [M_cv, dMdt]

""" Function for generating 1, 2, and 3 CSTR systems of differential equations"""
def CSTR(y, t, y0, M, dMdt, q, m11, x, Ncstr):

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
            cstrOne = (m11*(y0[i] - y[i][0]) + m41*(y[i][1] - y[i][0]))/Mn
            cstrTwo = (m31*(y[i][0] - y[i][1]) + m42*(y[i][2] - y[i][1]))/Mn
            cstrThree = (m32*(y[i][1] - y[i][2]))/Mn
            exp_CSTR = np.array([cstrOne, cstrTwo, cstrThree])

        if (i == 0):
            dydt = np.append(dydt, exp_CSTR)
        else:
            dydt = np.vstack([dydt, exp_CSTR])
    assert np.shape(dydt) == np.shape(y), 'CSTR ODE output wrong size'
   
    return dydt

def cstrRandInit(x,N):
    #Set initial conditions
    yinit_intermediate = np.random.rand(x) # randomize initial concentration
    yinit = yinit_intermediate/yinit_intermediate.sum(axis=0,keepdims=1).T # Force initial concentrations to add up to zero
    yinit = np.expand_dims(yinit, axis = 1)
    yinit = np.tile(yinit,(1,N))
    return yinit

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
