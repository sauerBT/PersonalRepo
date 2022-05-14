import pandas as pd
import numpy as np


def readRTDExp(file):
	my_export = pd.read_excel(file, index_col = 0, header = 0, skiprows = 4) #before index_col = 0 but excluded first column
	df = my_export.set_index('Date')
	df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
	return [df]



file = 'IMA_RTD_Data-v1.xlsx'
[columns, values, df] = readRTDExp(file)
F1_Flow = np.array(df['F1_CURR_FLW/PV.CV'])/3.6
API_Flow = np.array(df['F2_CURR_FLW/PV.CV'])/3.6
F3_Flow = np.array(df['F3_CURR_FLW/PV.CV'])/3.6
Ftot_Flow = (F1_Flow) + (API_Flow) + (F3_Flow)
x1_in = F1_Flow/Ftot_Flow
x2_in = API_Flow/Ftot_Flow
x3_in = F3_Flow/Ftot_Flow
Blend_Wt = np.array(df['BL_CURR_WGT/PV.CV'])*1000
API_x2 = (np.array(df['API_CONCEN1/PV.CV']) - .4)/100
RTD_X1 = np.array(df['RTD-4/XO_L1.CV'])
RTD_X2 = np.array(df['RTD-4/XO_L2.CV'])
RTD_X3 = np.array(df['RTD-4/XO_L3.CV'])
X_in = np.array([x1_in, x2_in, x3_in]).T # present concentration inputs as mass % in a matrix of the following dimensions: X_in[concentration @ time tn, interval = 1 sec][concentration at steam x, stream increases (i.e. stream 1 is @ column 0)]
print(X_in.shape[0])
print(X_in.shape[1])
print(X_in[::, 0])