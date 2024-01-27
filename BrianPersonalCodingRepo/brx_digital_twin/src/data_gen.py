import numpy as np
# import scipy as sp
# import csv
from numpy import random
from scipy.integrate import odeint
import pandas as pd
# import matplotlib.pyplot as plt



def dSdt (t, S, kdQ, mG, YAQ, YLG, YXG, YXQ, KL, KA, kdmax, mumax, KG, KQ, mQ, kmu, KLYSIS, Cstari, qi, V, SG, SQ, pid_Kp, pid_Ki, G_setpoint):
    
 
    XT, XV, XD, G, Q, L, A, Ci, F = S
    
    # Calculate mu with unknown inhibitory factor
    mu = (mumax * G * Q * (Cstari - Ci))/(Cstari*(KG+G)*(KQ+Q)*((L/KL)+1)*((A/KA)+1))
    # Calculate mu without accounting for unknown inhibitory factor
    #mu = mumax * (G/(KG+G)) * (Q/(KQ+Q)) * (KL/(KL+L)) * (KA/(KA+A))

    kd = kdmax*(kmu/(mu+kmu))
    
    dXTdt = mu * XV - KLYSIS*XD - XT*(F/V)            # ROC of total cell density (cells/L*t^-1)
    dXVdt = (mu-kd)*XV - XV*(F/V)                     # ROC of viable cell density (cells/L*t^-1)
    dXDdt = kd*XV - KLYSIS*XD - XV*(F/V)              # ROC of dead cell density (cells/L*t^-1)
    dGdt = (F/V)*(SG-G) + ((-mu/YXG)-mG)*XV           # Glucose consumption over time (mM*t^-1)
    dQdt = (F/V)*(SQ-Q) + ((-mu/YXQ)-mQ)*XV - kdQ*Q   # Glutamine consumption over time (mM*t^-1)
    dLdt = (-YLG)*((-mu/YXG)-mG)*XV - (F/V)*L         # Lactose consumption over time (mM*t^-1)
    dAdt = (-YAQ)*((-mu/YXQ)-mQ)*XV - (F/V)*A + kdQ*Q # Ammonia production over time due to consumption and defradation of glutamine (mM*t^-1)
    dCidt = qi*XV - (F/V)*Ci                          # ROC of inhibitor concentration (mM/t)
    dFdt = pid_Kp*(-dGdt) + pid_Ki*(G_setpoint-G)     # ROC of feed rate (L/h*t^-1)
    #Don't allow feed to go negative
    if (F+dFdt) <=0:
        dFdt = -F
    
    return[dXTdt, dXVdt, dXDdt, dGdt, dQdt, dLdt, dAdt, dCidt, dFdt]

def matrixGen (mylist, arrSize): #mylist - tuple of tuples that are constant value, weight (0.1, 0.25) arrSize - size of array to generate
    listlen = len(mylist)
    matrix = np.ones((listlen,arrSize))

    def inner_f(lot,acc):
        for tup in iter(lot):
            tempTup  = (tup)
            num = tempTup[0]
            weight = tempTup[1]
            if weight == 0:
                stddev= 0
                matrix[acc] = random.normal(num, stddev, arrSize)      
            else: 
                stddev = (num - (num*(1-weight)))/3
                matrix[acc] = random.normal(num, stddev, arrSize)
            acc = acc + 1
        return matrix
    return inner_f(mylist,0)






    
def csvWriter(tarr, XTarr, XVarr, XDarr, Garr, Qarr, Larr, Aarr, Ciarr, Farr, totkdQ, totmG, totYAQ, totYLG, totYXG, totYXQ, totKL, totKA, totkdmax, totmumax, totKG, totKQ, totmQ, totkmu, totKLYSIS, totCstari, totqi, totV, totSG, totSQ, batchNum):
        #Setup for writing to CSV
        #Create file name for CSV
        filename = "C:/pyDevelopment/test/Batch" + str(batchNum) + ".csv"
        
        list0 = [tarr, XTarr, XVarr, XDarr, Garr, Qarr, Larr, Aarr, Ciarr, Farr, totkdQ, totmG, totYAQ, totYLG, totYXG, totYXQ, totKL, totKA, totkdmax, totmumax, totKG, totKQ, totmQ, totkmu, totKLYSIS, totCstari, totqi, totV, totSG, totSQ]
        df = pd.DataFrame(list0)
        df = df.transpose()
        #return realdf
        #print(df)
        df.to_csv(filename, mode = 'a', index=False, header=False)
                

def monte (mylist, time, *initConds):

    resolveTimes = int(np.ceil(180/time))
    
    
    i = 0
    while i<100:
       
        S_0 = initConds[0]
        tottArr = ["TIME"]
        tottArr.extend(np.linspace(0,180,resolveTimes))
        totXTArr =["TOTAL CELL DENSITY"]
        totXVArr =["VIABLE CELL DENSITY"]
        totXDArr =["DEAD CELL DENSITY"]
        totGArr =["GLUCOSE CONC"]
        totQArr =["GLUTAMINE CONC"]
        totLArr =["LACTACE CONC"]
        totAArr =["AMMONIA CONC"]
        totCiArr =["INHIBITOR SAT"]
        totFArr =["FEED RATE"]
        totkdQ = ["DEG OF DEGRAD GLUTAMINE"]
        totmG = ["GLUC MAINT COEFF"]
        totYAQ = ["AMMONIA YIELD FROM GLUTAMINE"]
        totYLG = ["LACTACE YIELD FROM GLUCOSE"]
        totYXG = ["CELL YIELD FROM GLUCOSE"]
        totYXQ = ["CELL YIELD FROM GLUTAMINE"]
        totKL = ["LACTATE SAT CONST"]
        totKA = ["AMMONIA SAT CONST"]
        totkdmax = ["MAX DEATH RATE"]
        totmumax = ["MAX GROWTH RATE"]
        totKG = ["GLUCOSE SAT CONST"]
        totKQ = ["GLUTAMINE SAT CONST"]
        totmQ = ["GLUTAMINE MAINT COEF"]
        totkmu = ["INTRINSIC DEATH RATE"]
        totKLYSIS = ["CELL LYSIS RATE"]
        totCstari = ["INHIBITOR SAT CONC"]
        totqi = ["SPECIFIC INHIBITOR PROD RATE"]
        totV = ["VOLUME"]
        totSG = ["GLUCOSE CONC IN FEED"]
        totSQ = ["GLUTAMINE CONC IN FEED"]
    
        #Calculate the amount of ODE runs needed
        
        #Generate normal matrix for all constants, the size of the amount of ODE runs needed
        prodArr = matrixGen(mylist, resolveTimes)
        #Iterate through all DOE combinations
        j = 0
        init = 0
        end = time
        
        tfunc = np.linspace(init, end, 10)
        while j < resolveTimes:
            #Grab values from matrix to put into ODE Solver
            kdQ = prodArr[0, j]
            mG = prodArr[1, j]
            YAQ = prodArr[2, j]
            YLG = prodArr[3, j]
            YXG = prodArr[4, j]
            YXQ = prodArr[5, j]
            KL = prodArr[6, j]
            KA = prodArr[7, j]
            kdmax = prodArr[8, j]
            mumax = prodArr[9, j]
            KG = prodArr[10, j]
            KQ = prodArr[11, j]
            mQ = prodArr[12, j]
            kmu = prodArr[13, j]
            KLYSIS = prodArr[14, j]
            Cstari = prodArr[15, j]
            qi = prodArr[16, j]
            V = prodArr[17, j]
            SG = prodArr[18, j]
            SQ = prodArr[19, j]
            pid_Kp = prodArr[20, j]
            pid_Ki = prodArr[21, j]
            G_setpoint = prodArr[22, j]
            
            
            #t=np.linspace(init,end,10)
            #Solve ODE
            sol = odeint(dSdt, y0=S_0, t=tfunc, tfirst=True, args=(kdQ, mG, YAQ, YLG, YXG, YXQ, KL, KA, kdmax, mumax, KG, KQ, mQ, kmu, KLYSIS, Cstari, qi, V, SG, SQ, pid_Kp, pid_Ki, G_setpoint))
            #init = end
            #end = end+time
            
            #Create new initial conditions for next ODE run
            S_0 = (sol.T[0][-1], sol.T[1][-1], sol.T[2][-1], sol.T[3][-1], sol.T[4][-1], sol.T[5][-1], sol.T[6][-1], sol.T[7][-1], sol.T[8][-1])
            
            #Save current ODE solutions into accumulated list in a CSV file
            totXTArr.append(sol.T[0][-1])
            totXVArr.append(sol.T[1][-1])
            totXDArr.append(sol.T[2][-1])
            totGArr.append(sol.T[3][-1])
            totQArr.append(sol.T[4][-1])
            totLArr.append(sol.T[5][-1])
            totAArr.append(sol.T[6][-1])
            totCiArr.append(sol.T[7][-1])
            totFArr.append(sol.T[8][-1])
            totkdQ.append(kdQ)
            totmG.append(mG)
            totYAQ.append(YAQ)
            totYLG.append(YLG)
            totYXG.append(YXG)
            totYXQ.append(YXQ)
            totKL.append(KL)
            totKA.append(KA)
            totkdmax.append(kdmax)
            totmumax.append(mumax)
            totKG.append(KG)
            totKQ.append(KQ)
            totmQ.append(mQ)
            totkmu.append(kmu)
            totKLYSIS.append(KLYSIS)
            totCstari.append(Cstari)
            totqi.append(qi)
            totV.append(V)
            totSG.append(SG)
            totSQ.append(SQ)
    
            
            #plt.plot(t, XV_sol)
            #Iterator for loop
            j = j+1
        
        csvWriter(tottArr, totXTArr, totXVArr, totXDArr, totGArr, totQArr, totLArr, totAArr, totCiArr, totFArr,
                  totkdQ, totmG, totYAQ, totYLG, totYXG, totYXQ, totKL, totKA, totkdmax, totmumax, totKG,
                  totKQ, totmQ, totkmu, totKLYSIS, totCstari, totqi, totV, totSG, totSQ, i)
        i=i+1
    
    #PDF File name for saving plots     
    #filename = "2dplot.pdf"        
    #PDF Plot Saver Function Call
    #save_image(filename)
    #gc.collect()
    

#Initial Constants
mylist = ((0.001, 0.25), #kdQ in l/h
          (1.1e-10, 0.25), #mG in mmol/cel/h
          (0.9, 0.25), #YAQ
          (2.0, 0.25), #YLG
          (2.2e08, 0.25), #YXG
          (1.5e09, 0.25), #YXQ
          (150, 0.25), #KL
          (40, 0.25), #KA
          (0.01, 0.25), #kdmax
          (0.044, 0.1), #mumax
          (1.0, 0.25), #KG
          (0.22, 0.25), #KQ
          (0, 0.05), #mQ
          (0.01, 0.25), #kmu
          (2.0e-02, 0.25), #KLYSIS
          (100, 0.25), #Cstari
          (2.5e-10, 0.25), #qi
          (3, 0), #V
          (653, 0), #SG
          (58.8, 0), #SQ
          (0.001, 0), #PID KP
          (1,0), #PID KI
          (11, 0) #G SETPOINT
          )

#Initial Conditions for ODE
initialConds = (0.2e9, #XT_0
                0.2e9, #XV_0 
                0, #XD_0
                29, #G_0
                4.5, #Q_0
                0, #L_0
                1.0, #A_0 
                0, #Ci_0
                0.0, #F_0
                )
#print(doematrix[21])
monte(mylist, 0.16666667, initialConds)



