import pandas as pd
import numpy as np
import matplotlib as mp
import spec_funcs as sf

# change to gui at later date

dir = 'C:\\Users\\sk88\\Desktop'
folder = '20220323_FP_Alignment' 
file = 'FRESH_02.csv' 
path = dir + '\\' + folder + '\\' + file
raw_data = pd.read_csv(path, delimiter=',', header=0)

time = raw_data.iloc[:,0]
scan_amp = raw_data.iloc[:,1]
transmitted = raw_data.iloc[:,2]

check = sf.bin_data(transmitted, 100)