# -*- coding: utf-8 -*-
"""
Created on Mon May  6 10:13:01 2019

@author: bsauer
"""

def importer():
    from tkinter.filedialog import askopenfilename, asksaveasfilename   # Import file explorer 
    import csv
    import pandas as pd
    import numpy as np
    import datetime as dt
    
    filename_temp = askopenfilename(title = "Select file a file to import")
    df = pd.read_csv(filename_temp)
    header = list(df)
    # header.remove('Time')
    df[header] = df[header].convert_objects(convert_numeric=True) 
    Data = df[header] 
    Data = Data.values
    x = Data[:,1]
    t = Data[:,0]
    
    return (x,t)

from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def run():
    
    
    import scipy.fftpack
    import numpy as np
    import datetime as dt
    import matplotlib.pyplot as plt
    from scipy.signal import freqz

    [Acceleration,Time] = importer()
    
    # Sample rate and desired cutoff frequencies (in Hz).
    
    T =  0.0001860             # Sampling period   
    fs = 1/T            # Sampling frequency   
    lowcut = 500.0
    highcut = 1250.0
    Initial_Velocity = 0;
    L = len(Time)             # Length of signal
    t = Time[L - 1];        # Time vector
    
    # Acceleration integration --> Velocity
    Velocity = np.zeros((L,1))
    for i in range(L):
    
        if i == 0:
            Velocity[i] = Initial_Velocity;
        else:
            Velocity[i] = ((Acceleration[i] - Acceleration[i - 1])/2)*((Time[i] - Time[i - 1])*1000);
    Velocity  = Velocity*39.3701

    

    

    # Plot the frequency response for a few different orders.
#    plt.figure(1)
#    plt.clf()
#    for order in [3, 6, 9]:
#        b, a = butter_bandpass(lowcut, highcut, fs, order=order)
#        w, h = freqz(b, a, worN=2000)
#        plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)#
#
#    plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
#             '--', label='sqrt(0.5)')
#    plt.xlabel('Frequency (Hz)')
#    plt.ylabel('Gain')
#    plt.grid(True)
#    plt.legend(loc='best')

    # Filter a noisy signal.
   # T = 0.05
   # nsamples = T * fs
   # t = np.linspace(0, T, nsamples, endpoint=False)
   # a = 0.02
    f0 = 0
   # x = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
   # x += 0.01 * np.cos(2 * np.pi * 312 * t + 0.1)
   # x += a * np.cos(2 * np.pi * f0 * t + .11)
   # x += 0.03 * np.cos(2 * np.pi * 2000 * t)
    #plt.figure(2)
    #plt.clf()
   # plt.plot(t, x, label='Noisy signal')

    y = butter_bandpass_filter(Velocity, lowcut, highcut, fs, order=4)
    plt.plot(Time, Velocity, label='Unfiltered signal (%g Hz)' % f0)
    plt.plot(Time, y, label='Filtered signal (%g Hz)' % f0)
    plt.xlabel('time (ms)')
    plt.ylabel('Velocity')
    #plt.hlines([-a, a], 0, T, linestyles='--')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')

    plt.show()
    N = L + 1
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    
    
    
    
    return (Velocity,y,Time, xf, yf, N)

[x,y,t,xf, yf, N] = run()

import matplotlib.pyplot as plt
import numpy as np
import matlab.engine

eng = matlab.engine.start_matlab()

yf = 2.0/N * np.abs(yf[0:int(N/2)])

eng.plot(xf,yf)

eng.quit()

plt.plot(xf,yf)


